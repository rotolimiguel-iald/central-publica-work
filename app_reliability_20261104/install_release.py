"""Install reviewed release; resume only with a verified coherent state."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import subprocess
import sys

W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(W.parent/'iald_v407_20261104'))
from transaction import quiet
sys.path.insert(0,str(W))
from maintenance_safe import stopped_web,await_restart,assert_quiesced
import task
from prepare_release import staged_bytes,sha


def require(condition,message):
    if not condition:raise RuntimeError(message)


def record(name,value):
    raw=json.dumps(value,ensure_ascii=False,indent=2).encode('utf8')
    dest=W/name;temp=W/(name+'.tmp')
    with temp.open('xb') as handle:
        handle.write(raw);handle.flush();os.fsync(handle.fileno())
    require(temp.read_bytes()==raw,'Receipt verification failed')
    os.link(temp,dest)
    temp.unlink()


def protected(path,raw):
    with path.open('xb'):pass
    owner=subprocess.run(['whoami'],capture_output=True,text=True,check=True).stdout.strip()
    subprocess.run(['icacls',str(path),'/inheritance:r','/grant:r',owner+':F','*S-1-5-18:F'],capture_output=True,check=True)
    with path.open('r+b') as handle:
        handle.write(raw);handle.flush();os.fsync(handle.fileno())
    require(path.read_bytes()==raw,'Protected write verification failed')


def current_hash(path):return sha(path.read_bytes()) if path.exists() else None


def restore_originals(plan,backups,stamp):
    errors=[]
    for row in reversed(plan['files']):
        p=Path(row['path'])
        try:
            require(p.resolve().parent==ROOT.resolve() and not p.is_symlink(),'Rollback path changed')
            current=current_hash(p)
            if current==row['before']:continue
            require(current==row['after'],'Rollback conflict; unknown bytes preserved')
            assert_quiesced()
            if row['before'] is None:p.unlink()
            else:
                raw=Path(backups[p.name]).read_bytes()
                require(sha(raw)==row['before'],'Backup changed')
                temp=p.with_name(p.name+'.rollback_'+stamp)
                protected(temp,raw);os.replace(temp,p)
        except BaseException as exc:
            errors.append({'file':p.name,'error_type':type(exc).__name__})
    try:coherent=all(current_hash(Path(row['path']))==row['before'] for row in plan['files'])
    except BaseException:coherent=False
    return coherent,errors


def main():
    require(not sys.flags.optimize,'Optimized execution refused')
    require(task.check('delivery')['ready'],'Mission preflight refused')
    receipts=('INSTALL_INTENT.json','MAINTENANCE.json','DEPLOYMENT.json','RECOVERY.json','RESTART.json')
    for name in receipts:
        require(not (W/name).exists() and not (W/(name+'.tmp')).exists(),'Existing attempt evidence; inspect before continuing')
    plan=json.loads((W/'INSTALL_PLAN.json').read_bytes())
    review=json.loads((W/'review/RELEASE_REVIEW.json').read_bytes())
    require(review['status']=='PASS' and review['plan_sha256']==sha((W/'INSTALL_PLAN.json').read_bytes()),'Release review missing or changed')
    require(review['installer_sha256']==sha(Path(__file__).read_bytes()),'Installer not reviewed')
    for row in plan['sources']:
        require(sha(Path(row['path']).read_bytes())==row['sha256'],'Staged source changed')
    outputs=staged_bytes()
    for row in plan['files']:
        p=Path(row['path'])
        require(p.parent==ROOT and not p.is_symlink(),'Unexpected destination')
        require(current_hash(p)==row['before'],'Runtime baseline changed')
        require(sha(outputs[p.name])==row['after'],'Output mismatch')
    quiet()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    backups={};identity=None
    record('INSTALL_INTENT.json',{'status':'PREPARED','stamp':stamp,'files':plan['files'],
        'plan_sha256':sha((W/'INSTALL_PLAN.json').read_bytes()),
        'recovery':'Verify all target pins; resume only if all match before or all match after. Unknown bytes require operator inspection.',
        'at':datetime.now(timezone.utc).isoformat()})
    try:
        with stopped_web(quiet) as identity:
            try:
                record('MAINTENANCE.json',identity)
                for row in plan['files']:
                    p=Path(row['path'])
                    require(current_hash(p)==row['before'],'CAS conflict before installation')
                for row in plan['files']:
                    p=Path(row['path'])
                    if row['before'] is not None:
                        backup=p.with_name(p.name+'.bak_'+stamp)
                        protected(backup,p.read_bytes())
                        require(sha(backup.read_bytes())==row['before'],'Backup baseline mismatch')
                        backups[p.name]=str(backup)
                for row in plan['files']:
                    assert_quiesced()
                    p=Path(row['path']);temp=p.with_name(p.name+'.tmp_reliability_'+stamp)
                    protected(temp,outputs[p.name])
                    require(current_hash(p)==row['before'],'Concurrent file change')
                    os.replace(temp,p)
                    require(current_hash(p)==row['after'],'Installed bytes differ')
                require(all(current_hash(Path(r['path']))==r['after'] for r in plan['files']),'Release incomplete')
                record('DEPLOYMENT.json',{'status':'INSTALLED','files':plan['files'],'backups':backups,
                    'restart_pending':True,'at':datetime.now(timezone.utc).isoformat()})
                identity['resume_allowed']=True
            except BaseException as exc:
                coherent,errors=restore_originals(plan,backups,stamp)
                identity['resume_allowed']=coherent
                record('RECOVERY.json',{'status':'ROLLED_BACK' if coherent else 'HOLD_FOR_RECOVERY',
                    'original_error_type':type(exc).__name__,'rollback_errors':errors,
                    'backups':backups,'supervisor':identity,
                    'next_action':'Verify restart' if coherent else 'Do not resume until all release files match one reviewed state'})
                raise
    finally:
        if identity and identity.get('resume_allowed'):
            try:result=await_restart(identity,timeout=55)
            except BaseException as exc:
                record('RESTART.json',{'status':'FAILED','error_type':type(exc).__name__,'identity':identity,
                    'files':[{'name':Path(r['path']).name,'sha256':current_hash(Path(r['path']))} for r in plan['files']],
                    'next_action':'Inspect existing supervisor and child; preserve files and do not repeat deployment'})
                raise
            else:
                record('RESTART.json',result)
                print(json.dumps(result))
    print('Installed verified runtime release; no client or scientific source changes')


if __name__=='__main__':main()
