"""Run once after independent review, with real admissions excluded."""
from pathlib import Path
from transaction import apply_plan,quiet,write_evidence,digest
from maintenance import stopped_web,await_restart
import json
W=Path(__file__).resolve().parent
def main():
    import task
    assert task.check('deploy')['ready']
    if (W/'deployment.json').exists():raise RuntimeError('Existing deployment; inspect receipt')
    review=json.loads((W/'validation/review_final.json').read_bytes())
    assert review['status']=='PASS' and review['plan_sha256']==digest((W/'install_plan.json').read_bytes())
    assert review['transaction_sha256']==digest((W/'transaction.py').read_bytes())
    assert review['maintenance_sha256']==digest((W/'maintenance.py').read_bytes())
    quiet()
    identity=None
    try:
        with stopped_web(quiet) as identity:
            write_evidence(W/'maintenance.json',dict(status='ADMISSIONS_STOPPED',**identity))
            receipt=apply_plan(W/'install_plan.json')
            print('INSTALLED; existing supervisor will resume',flush=True)
    finally:
        if identity:
            restart=await_restart(identity)
            write_evidence(W/'restart.json',restart)
            print(json.dumps(restart),flush=True)
    print(json.dumps({'status':receipt['status'],'files':len(receipt['files'])}))
if __name__=='__main__':main()
