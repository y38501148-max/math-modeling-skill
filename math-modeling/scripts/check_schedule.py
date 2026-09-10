#!/usr/bin/env python3
"""Check explicit exclusive-resource schedules. Does not prove model completeness or optimality."""
import argparse
from collections import defaultdict, deque
import json
import math
from pathlib import Path


def number(value, label, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{label} must be a finite number')
    if value < 0 or (positive and value <= 0):
        raise ValueError(f'{label} must be {"positive" if positive else "nonnegative"}')
    return value


def interval(value, label):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f'{label} must be [start, end]')
    start, end = [number(v, label) for v in value]
    if end <= start:
        raise ValueError(f'{label} end must exceed start')
    return start, end


def check_schedule(data, tolerance=1e-9):
    number(tolerance, 'tolerance')
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('schema_version must be 1')
    if not isinstance(data.get('units'), str) or not data['units'].strip():
        raise ValueError('units must name the common time unit')
    horizon = number(data.get('horizon'), 'horizon', positive=True)
    resources = data.get('resources')
    if not isinstance(resources, dict) or not resources:
        raise ValueError('resources must be a nonempty object of exclusive resources')
    calendars = {}
    for name, spec in resources.items():
        if not isinstance(name, str) or not name or not isinstance(spec, dict):
            raise ValueError('resource names must be nonempty strings; specs must be objects')
        windows = spec.get('unavailable', [])
        if not isinstance(windows, list):
            raise ValueError(f'{name}.unavailable must be a list')
        calendars[name] = [interval(w, f'{name}.unavailable') for w in windows]
    records = data.get('operations')
    if not isinstance(records, list) or not records:
        raise ValueError('operations must be a nonempty list')
    operations = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError('each operation must be an object')
        key = record.get('id')
        if not isinstance(key, str) or not key or key in operations:
            raise ValueError('operation IDs must be unique nonempty strings')
        start, end = interval([record.get('start'), record.get('end')], key)
        used = record.get('resources')
        if not isinstance(used, list) or not used or any(not isinstance(r, str) for r in used):
            raise ValueError(f'{key}.resources must be a nonempty list of names')
        if len(used) != len(set(used)) or any(r not in resources for r in used):
            raise ValueError(f'{key} has duplicate or unknown resources')
        minimum = number(record.get('min_duration', 0), key + '.min_duration')
        release = number(record.get('release', 0), key + '.release')
        deadline = number(record.get('deadline', horizon), key + '.deadline')
        predecessors = record.get('predecessors', [])
        if not isinstance(predecessors, list):
            raise ValueError(f'{key}.predecessors must be a list')
        parsed = []
        for pred in predecessors:
            if isinstance(pred, str):
                parsed.append((pred, 0))
            elif isinstance(pred, dict) and isinstance(pred.get('id'), str):
                parsed.append((pred['id'], number(pred.get('lag', 0), key + '.lag')))
            else:
                raise ValueError(f'{key}: predecessor must be an ID or an object with id and optional lag')
        if len(parsed) != len({p[0] for p in parsed}):
            raise ValueError(f'{key}: duplicate predecessors')
        operations[key] = dict(start=start, end=end, resources=used, minimum=minimum,
                               release=release, deadline=deadline, predecessors=parsed)
    for key, op in operations.items():
        for pred, _ in op['predecessors']:
            if pred not in operations:
                raise ValueError(f'{key}: unknown predecessor {pred}')
    violations = []
    def fail(code, **details):
        violations.append(dict(code=code, **details))
    timeline = defaultdict(list)
    successors = defaultdict(list)
    indegree = {k: 0 for k in operations}
    for key, op in operations.items():
        start, end = op['start'], op['end']
        if end - start + tolerance < op['minimum']:
            fail('DURATION', operation=key, actual=end-start, required=op['minimum'])
        if start + tolerance < op['release']:
            fail('RELEASE', operation=key, start=start, release=op['release'])
        if end > op['deadline'] + tolerance:
            fail('DEADLINE', operation=key, end=end, deadline=op['deadline'])
        if end > horizon + tolerance:
            fail('HORIZON', operation=key, end=end, horizon=horizon)
        for pred, lag in op['predecessors']:
            required = operations[pred]['end'] + lag
            if start + tolerance < required:
                fail('PRECEDENCE', predecessor=pred, operation=key, start=start, earliest=required)
            successors[pred].append(key)
            indegree[key] += 1
        for resource in op['resources']:
            timeline[resource].append((start, end, key))
            for down_start, down_end in calendars[resource]:
                if min(end, down_end) - max(start, down_start) > tolerance:
                    fail('UNAVAILABLE', resource=resource, operation=key, unavailable=[down_start, down_end])
    ready = deque(k for k, v in indegree.items() if v == 0)
    visited = 0
    while ready:
        key = ready.popleft()
        visited += 1
        for child in successors[key]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if visited != len(operations):
        fail('PRECEDENCE_CYCLE', affected_operations=[k for k, v in indegree.items() if v > 0])
    for resource, spans in timeline.items():
        active = []
        for start, end, key in sorted(spans):
            active = [(s, e, k) for s, e, k in active if e - start > tolerance]
            for old_start, old_end, old_key in active:
                if min(end, old_end) - max(start, old_start) > tolerance:
                    fail('RESOURCE_OVERLAP', resource=resource, operations=[old_key, key],
                         overlap=[max(start, old_start), min(end, old_end)])
            active.append((start, end, key))
    return {'valid': not violations, 'checked_operations': len(operations),
            'units': data['units'], 'makespan': max(op['end'] for op in operations.values()),
            'violations': violations,
            'scope': 'Only declared intervals, exclusive resources, calendars, durations, windows and precedence are checked; no completeness or optimality claim.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('schedule', type=Path)
    parser.add_argument('--tolerance', type=float, default=1e-9, help='Absolute tolerance in the declared time unit')
    args = parser.parse_args()
    try:
        data = json.loads(args.schedule.read_text(encoding='utf-8'))
        result = check_schedule(data, args.tolerance)
    except (OSError, ValueError) as error:
        print(json.dumps({'valid': False, 'error': str(error), 'type': 'input-error'}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
