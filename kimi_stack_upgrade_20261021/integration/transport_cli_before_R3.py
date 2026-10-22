"""JSON stdin bridge for automation; no model is called when checking an empty queue."""
import json
import sys

def main():
    request = json.load(sys.stdin)
    if not isinstance(request, dict):
        raise ValueError('Invalid local request object')
    operation = request.get('operation')
    if operation == 'retrieve_knowledge':
        from iald_orchestrator.layered_retrieval import retrieve
        if set(request) - {'operation','query','budget_bytes','mandatory_ids'}:
            result = {'ok':False,'status':'REFUSED','error':'unknown_arguments'}
        else:
            result = retrieve(request.get('query',''), budget_bytes=request.get('budget_bytes',48000),
                              mandatory_ids=request.get('mandatory_ids',()))
        sys.stdout.buffer.write(json.dumps(result, ensure_ascii=False, separators=(',',':')).encode('utf-8')+b'\n')
        return
    from iald_orchestrator.transport import Transport
    transport = Transport()
    if operation in ('activity_get','activity_project','activity_reconcile'):
        from iald_orchestrator.activity_bridge import invoke
        result=invoke(transport.coordination.runtime,request)
    elif operation == 'next':
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
