"""Run once after independent review, with real admissions excluded."""
from pathlib import Path
from transaction import apply_plan,quiet,write_evidence,digest,check_science_destinations
from maintenance import stopped_web,await_restart
import json
import sys
import operational_patch
W=Path(__file__).resolve().parent
def main():
    import task
    if sys.flags.optimize:
        raise RuntimeError('Release requires assertions')
    assert task.check('deploy')['ready']
    if (W/'deployment.json').exists():raise RuntimeError('Existing deployment; inspect receipt')
    review=json.loads((W/'validation/review_final.json').read_bytes())
    assert review['status']=='PASS' and review['plan_sha256']==digest((W/'install_plan.json').read_bytes())
    assert review['transaction_sha256']==digest((W/'transaction.py').read_bytes())
    assert review['maintenance_sha256']==digest((W/'maintenance.py').read_bytes())
    assert review['deploy_controlled_sha256']==digest(Path(__file__).read_bytes())
    assert review['verify_installed_sha256']==digest((W/'verify_installed.py').read_bytes())
    files = json.loads((W/'install_plan.json').read_bytes())['files']
    check_science_destinations(files)
    patch_pin, patch_rows = operational_patch.validated_rows()
    if (W/'maintenance.json').exists():
        raise RuntimeError('A maintenance attempt already exists; inspect it before continuing')
    quiet()
    identity=None
    try:
        with stopped_web(quiet) as identity:
            try:
                write_evidence(W/'maintenance.json',dict(status='ADMISSIONS_STOPPED',**identity))
                receipt=apply_plan(W/'install_plan.json')
                for row in files:
                    if digest(Path(row['destination']).read_bytes()) != row['sha256']:
                        raise RuntimeError('Incomplete deployment after installation')
                operational_patch.install(patch_pin, patch_rows)
            except BaseException:
                # Resume only a fully coherent baseline or a fully installed release.
                measured = [(digest(path.read_bytes()) if path.is_file() else None)
                            for path in (Path(row['destination']) for row in files)]
                old = all(pin == row['baseline'] for pin, row in zip(measured, files))
                new = all(pin == row['sha256'] for pin, row in zip(measured, files))
                identity['resume_allowed'] = (old or new) and operational_patch.coherent(patch_rows)
                write_evidence(W/'recovery.json', {'baseline_complete':old,'release_complete':new,
                                                   'resume_allowed':identity['resume_allowed']})
                raise
            identity['resume_allowed']=True
            print('INSTALLED; existing supervisor will resume',flush=True)
    finally:
        if identity and identity.get('resume_allowed'):
            restart=await_restart(identity)
            write_evidence(W/'restart.json',restart)
            print(json.dumps(restart),flush=True)
    print(json.dumps({'status':receipt['status'],'files':len(receipt['files'])}))
if __name__=='__main__':main()
