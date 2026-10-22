"""Small exact-reference mission transitions; no external calls or fabricated reviewer."""
import argparse
import json
from pathlib import Path
from mission_io import WORK, ACTOR, REFERENCE, call, pin, project, save

def action(op, task, extra=None, actor=None):
    p, _ = project()
    row = next((r for r in p['projection']['active'] + p['projection']['settled'] if r['id'] == task), None)
    request = {'operation': op, 'reference': str(REFERENCE), 'actor': actor or ACTOR,
        'task_id': task, 'expected_revision': p['receipt']['revision'],
        'projection_sha256': p['projection_sha256'],
        'event_id': f'organism-{task}-{op}-{p["receipt"]["revision"]}'}
    if op == 'submit':
        request['lease_id'] = row['lease']['id']
    request.update(extra or {})
    return call('mission_cli.py', request, op + '_' + task)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('op', choices=['claim','submit'])
    parser.add_argument('task')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    fields = {'lease_seconds': 14400} if args.op == 'claim' else {'evidence': [pin(x) for x in args.files]}
    result, receipt = action(args.op, args.task, fields)
    print(json.dumps({'receipt': str(receipt), 'revision': result['receipt']['revision']}, ensure_ascii=False))
