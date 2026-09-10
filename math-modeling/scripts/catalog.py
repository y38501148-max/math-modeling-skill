#!/usr/bin/env python3
"""Offline, provenance-preserving search of a pinned GitHub file inventory."""
import argparse
import gzip
import json
from pathlib import Path
from urllib.parse import quote

REFS = Path(__file__).resolve().parents[1] / 'references'

def read_rows(path=None):
    with gzip.open(path or REFS / 'catalog.jsonl.gz', 'rt', encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]

def permalink(row):
    return f'https://github.com/{row["repo"]}/blob/{row["commit"]}/' + quote(row['path'], safe='/')

def search(rows, query='', scope='undergraduate', kind=None, repo=None, unique=False):
    scopes = {'cumcm', 'mcmicm'} if scope == 'undergraduate' else {scope}
    terms = query.casefold().split()
    found = []
    for row in rows:
        if scope != 'all' and row['scope'] not in scopes:
            continue
        if kind and row['kind'] != kind:
            continue
        if repo and row['repo'] != repo:
            continue
        haystack = ' '.join([row['repo'], row['path'], *row.get('verified_titles', []), *row.get('source_ids', [])]).casefold()
        if all(term in haystack for term in terms):
            found.append(dict(row, url=permalink(row)))
    if not unique:
        return found
    groups = {}
    for row in found:
        sha = row['blob_sha']
        if sha not in groups:
            groups[sha] = dict(row, matching_aliases=[])
        groups[sha]['matching_aliases'].append({'repo': row['repo'], 'path': row['path'], 'url': row['url']})
    return list(groups.values())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('stats', help='Print inventory counts and pinned commits')
    source = sub.add_parser('source', help='Print a reviewed source record by ID')
    source.add_argument('id')
    find = sub.add_parser('search', help='AND-match whitespace-separated terms in metadata; not PDF full text')
    find.add_argument('--query', default='')
    find.add_argument('--scope', choices=['undergraduate', 'cumcm', 'mcmicm', 'graduate', 'general', 'all'], default='undergraduate')
    find.add_argument('--kind', help='paper, review, problem, code, data, template, archive, etc.')
    find.add_argument('--repo', choices=['zhanwen/MathModel', 'personqianduixue/Math_Model'])
    find.add_argument('--unique', action='store_true', help='Group byte-identical matching files by Git blob SHA')
    find.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()
    if args.command == 'stats':
        result = json.loads((REFS / 'inventory-summary.json').read_text(encoding='utf-8'))
    elif args.command == 'source':
        sources = json.loads((REFS / 'sources.json').read_text(encoding='utf-8'))['sources']
        result = next((s for s in sources if s['id'].casefold() == args.id.casefold()), None)
        if result is None:
            parser.error(f'Unknown reviewed source: {args.id}')
    else:
        if args.limit < 1:
            parser.error('--limit must be positive')
        rows = search(read_rows(), args.query, args.scope, args.kind, args.repo, args.unique)
        result = {'matching_count': len(rows), 'returned_count': min(len(rows), args.limit),
                  'search_type': 'metadata-only', 'rows': rows[:args.limit]}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
