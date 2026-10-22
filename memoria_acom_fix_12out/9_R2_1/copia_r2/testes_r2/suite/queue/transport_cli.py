"""JSON stdin bridge for automation; no model is called when checking an empty queue."""
import json
import sys
from iald_orchestrator.transport import Transport

def main():
    request = json.load(sys.stdin)
    transport = Transport()
    operation = request.get('operation')
    if operation == 'next':
        result = transport.next_job()
    elif operation == 'submit':
        result = transport.submit(request['prompt'], request['request_id'], request.get('execution_constraints'))
    elif operation == 'preview_execution':
        result = transport.coordination.runtime.preview(request['prompt'],request.get('execution_constraints'))
    elif operation == 'submit_execution':
        runtime=transport.coordination.runtime
        task=runtime.submit(request['prompt'],request['request_id'],execution_constraints=request.get('execution_constraints'),start_worker=False)
        runtime._drain()  # Keep the official adapter alive until its bounded call ends.
        result=runtime.task(task['id'])
    elif operation == 'receipt':
        result = transport.receipt(request['state'], request.get('job_id'))
    else:
        raise ValueError('Operação de transporte inválida.')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
