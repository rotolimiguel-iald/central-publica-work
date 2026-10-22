"""Record an observed execution handle without changing material requirements."""
import argparse
import copy
import json
from mission_io import REFERENCE, ACTOR, call


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('handle')
    parser.add_argument('agent')
    parser.add_argument('task')
    parser.add_argument('status', choices=['running', 'completed', 'failed'])
    parser.add_argument('event')
    args = parser.parse_args()
    state, _ = call('session_memory.py', {'operation': 'get', 'reference': str(REFERENCE)}, 'handle_get')
    handles = copy.deepcopy(state['p']['handles'])
    matching = [h for h in handles if h['id'] == args.handle]
    if matching:
        entry = matching[0]
        if entry.get('agent') != args.agent or entry.get('task_id') != args.task:
            raise ValueError('Handle identity mismatch')
        if entry['status'] == args.status:
            print(json.dumps({'status': 'ALREADY_RECORDED', 'revision': state['revision']}))
            return
        if entry['status'] != 'running':
            raise ValueError('Terminal execution cannot be reopened')
        entry['status'] = args.status
    else:
        handles.append({'id': args.handle, 'agent': args.agent, 'task_id': args.task,
                        'kind': 'agent', 'status': args.status, 'no_repeat': True})
    result, path = call('session_memory.py', {
        'operation': 'transition', 'reference': str(REFERENCE), 'actor': ACTOR,
        'expected_revision': state['revision'], 'event_id': args.event,
        'changes': {'flow': {'handles': handles}}}, 'handle_' + args.handle)
    print(json.dumps({'receipt': str(path), 'result': result}, ensure_ascii=False))


if __name__ == '__main__':
    main()
