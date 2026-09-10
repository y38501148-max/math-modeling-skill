#!/usr/bin/env python3
"""Check declared artifact snapshots and numeric claims; never execute project code."""
import argparse
import hashlib
import json
import re
import sys
from decimal import Decimal, DecimalException
from pathlib import Path


class ContractError(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise ContractError('non-finite JSON number: ' + value)


def parse_json(text):
    return json.loads(text, parse_float=Decimal, parse_int=Decimal,
                      parse_constant=invalid_constant, object_pairs_hook=unique_object)


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
        raise ContractError(label + ' must be a JSON number')
    value = Decimal(value)
    if not value.is_finite():
        raise ContractError(label + ' must be finite')
    return value


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ContractError(label + ' must be a nonempty string')
    return value


def fields(obj, required, optional, label):
    if not isinstance(obj, dict):
        raise ContractError(label + ' must be an object')
    missing = set(required) - obj.keys()
    unknown = obj.keys() - set(required) - set(optional)
    if missing or unknown:
        raise ContractError(f'{label}: missing={sorted(missing)}, unknown={sorted(unknown)}')


def resolve_file(root, raw):
    path = Path(nonempty(raw, 'path'))
    if path.is_absolute():
        raise ContractError('artifact path must be relative to manifest directory')
    path = (root / path).resolve()
    if not path.is_relative_to(root):
        raise ContractError('artifact path escapes manifest directory')
    return path


def pointer_get(value, pointer):
    if not isinstance(pointer, str) or (pointer and not pointer.startswith('/')):
        raise ContractError('pointer must be empty or start with /')
    if not pointer:
        return value
    for token in pointer[1:].split('/'):
        if re.search(r'~(?![01])', token):
            raise ContractError('invalid JSON Pointer escape')
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict):
            if token not in value:
                raise ContractError('JSON Pointer key not found: ' + token)
            value = value[token]
        elif isinstance(value, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', token) or int(token) >= len(value):
                raise ContractError('JSON Pointer array index invalid: ' + token)
            value = value[int(token)]
        else:
            raise ContractError('JSON Pointer traverses a scalar')
    return value


def check(manifest):
    manifest = Path(manifest).resolve()
    data = parse_json(manifest.read_text(encoding='utf-8'))
    fields(data, ['version', 'artifacts', 'claims'], ['description'], 'manifest')
    if isinstance(data['version'], bool) or data['version'] != 1:
        raise ContractError('unsupported manifest version')
    for key in ('artifacts', 'claims'):
        if not isinstance(data[key], list) or not data[key]:
            raise ContractError(key + ' must be a nonempty array')
    artifacts = {}
    errors = []
    warnings = []
    for item in data['artifacts']:
        fields(item, ['id', 'path', 'sha256'], [], 'artifact')
        ident = nonempty(item['id'], 'artifact id')
        if ident in artifacts:
            raise ContractError('duplicate artifact id: ' + ident)
        if not isinstance(item['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', item['sha256']):
            raise ContractError('sha256 must be 64 lowercase hex characters')
        path = resolve_file(manifest.parent, item['path'])
        artifacts[ident] = None
        try:
            raw = path.read_bytes()
        except OSError:
            errors.append({'artifact': ident, 'issue': 'file missing or unreadable'})
            continue
        artifacts[ident] = raw
        if not raw:
            errors.append({'artifact': ident, 'issue': 'file is empty'})
            artifacts[ident] = None
            continue
        if hashlib.sha256(raw).hexdigest() != item['sha256']:
            errors.append({'artifact': ident, 'issue': 'sha256 mismatch; snapshot changed'})
    ids = set()
    parsed = {}
    checks = []
    for claim in data['claims']:
        fields(claim, ['id', 'artifact', 'pointer', 'value', 'unit', 'status', 'location'],
               ['scale', 'abs_tol', 'rel_tol'], 'claim')
        ident = nonempty(claim['id'], 'claim id')
        if ident in ids:
            raise ContractError('duplicate claim id: ' + ident)
        ids.add(ident)
        source = nonempty(claim['artifact'], 'claim artifact')
        if source not in artifacts:
            raise ContractError('unknown artifact: ' + source)
        nonempty(claim['unit'], 'unit')
        nonempty(claim['location'], 'location')
        if claim['status'] not in ('measured', 'model_estimate', 'synthetic', 'unverified'):
            raise ContractError('invalid claim status')
        expected = number(claim['value'], 'value')
        scale = number(claim.get('scale', 1), 'scale')
        atol = number(claim.get('abs_tol', 0), 'abs_tol')
        rtol = number(claim.get('rel_tol', 0), 'rel_tol')
        if scale <= 0 or atol < 0 or rtol < 0:
            raise ContractError('scale must be positive; tolerances must be nonnegative')
        if claim['status'] in ('synthetic', 'unverified'):
            warnings.append({'claim': ident, 'issue': claim['status'] + ': not real-world validation'})
        if artifacts[source] is None:
            continue
        if source not in parsed:
            parsed[source] = parse_json(artifacts[source].decode('utf-8'))
        actual = number(pointer_get(parsed[source], claim['pointer']), 'source value') * scale
        diff = abs(expected - actual)
        tolerance = max(atol, rtol * abs(actual))
        passed = diff <= tolerance
        checks.append({'claim': ident, 'actual_scaled': str(actual), 'declared': str(expected),
                       'difference': str(diff), 'tolerance': str(tolerance), 'matches': passed})
        if not passed:
            errors.append({'claim': ident, 'issue': 'numeric mismatch at declared pointer'})
    return {'status': 'FAIL' if errors else 'PASS',
            'scope': 'Declared file hashes and numeric fields only; no paper parsing or model validation.',
            'artifact_count': len(artifacts), 'claim_count': len(ids),
            'checks': checks, 'errors': errors, 'warnings': warnings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args(argv)
    try:
        report = check(args.manifest)
    except (ValueError, OSError, UnicodeError, DecimalException) as exc:
        print(json.dumps({'status': 'ERROR', 'error': str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['status'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
