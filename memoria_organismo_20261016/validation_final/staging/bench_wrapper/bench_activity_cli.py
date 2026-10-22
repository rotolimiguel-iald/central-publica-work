"""External local operator adapter; deploy alongside the queue, never in Bancada."""
import json,sys
from iald_orchestrator.runtime import Runtime
from iald_orchestrator import bench_activity

def main():
    request=json.load(sys.stdin);op=request.get('operation');runtime=Runtime(recover=False)
    if op=='admit' and set(request)=={'operation','request_id','command','action','payload'}:
        result=bench_activity.admit(runtime,request['request_id'],request['command'],request['action'],request['payload'])
    elif op in ('execute','get','reconcile','poll') and set(request)=={'operation','request_id'}:
        method={'execute':bench_activity.execute,'get':bench_activity.recover,'reconcile':bench_activity.reconcile,'poll':bench_activity.poll}[op]
        result=method(runtime,request['request_id'])
    else:raise ValueError('Unsupported/privileged argument; OS-local admission required')
    print(json.dumps(result,ensure_ascii=False,allow_nan=False))

if __name__=='__main__':main()
