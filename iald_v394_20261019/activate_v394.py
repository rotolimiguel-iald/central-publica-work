"""Authorized v394 activation after distinct reviews; never executes science sources."""
from pathlib import Path
import hashlib,json,sys
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(W))
import task
from transaction import quiet,write_evidence

def main():
    # No retry after an intent: recover actual pointers/receipts before a new action.
    if (W/'ACTIVATION_INTENT.json').exists():raise RuntimeError('Activation intent exists; inspect actual state before proceeding')
    p=task.project()
    tasks={x['id']:x for group in ('active','settled') for x in p['projection'][group]}
    for name in ('sources','app','queue','reader_compat','all_engines_admission'):
        if tasks[name]['status']!='satisfied':raise RuntimeError('Unsatisfied prerequisite: '+name)
    task.check('deploy')
    for filename in ('install_plan.json','validation/review_final.json','validation/final_checks.json'):
        if not (W/filename).is_file():raise RuntimeError('Missing reviewed install artifact: '+filename)
    review=json.loads((W/'validation/review_final.json').read_bytes())
    plan_sha=hashlib.sha256((W/'install_plan.json').read_bytes()).hexdigest()
    if review['status']!='PASS' or review['plan_sha256']!=plan_sha:raise RuntimeError('Final reviewed plan mismatch')
    helper=Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013')
    sys.path.insert(0,str(helper))
    from scientific_memory_sync import ScientificMemorySync
    report=json.loads((W/'queue/R3/DELIVERY_PREPARED_R3.json').read_bytes())
    epoch=report['epoch']
    sync=ScientificMemorySync(work=W/'queue/R3',member=task.OWNER)
    verified=sync.verify(epoch)
    quiet()
    write_evidence(W/'ACTIVATION_INTENT.json',{'status':'REVIEWED_ACTIVATION_INTENT','plan_sha256':plan_sha,'epoch':epoch,'generation':verified['generation'],'order':['queue_existing_CAS_API','controlled_app_transaction_and_web_restart'],'partial_failure_policy':'No automatic retry or claim of joint completion. Preserve actual queue/app states and receipts; scientific jobs retain their pinned generations.'})
    queue=sync.activate(epoch)
    write_evidence(W/'queue_activation.json',queue)
    # Web controller independently rechecks idleness and exact plan/baselines.
    import deploy_controlled
    deploy_controlled.main()
    write_evidence(W/'ACTIVATION_RESULT.json',{'status':'APP_AND_QUEUE_ACTIVATED_REQUIRES_EFFECTIVE_USE_VERIFICATION','epoch':epoch,'queue':queue,'app_plan_sha256':plan_sha,'science_executed':False})
    print(json.dumps({'status':'ACTIVATED_REQUIRES_VERIFICATION','queue_epoch':epoch,'app_plan_sha256':plan_sha}))

if __name__=='__main__':main()
