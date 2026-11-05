"""Reload the enrolled credential in the existing web process only."""
from pathlib import Path
import json
import sys
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W.parent/'iald_v407_20261104'))
from transaction import quiet
sys.path.insert(0,str(W))
from maintenance_safe import stopped_web,await_restart
from install_release import record,require
import task


def main():
    require(task.check('credentials')['ready'],'Preflight refused')
    require(not (W/'CREDENTIAL_RELOAD.json').exists(),'Previous reload exists')
    require(not (W/'CREDENTIAL_RELOAD.json.tmp').exists(),'Previous partial receipt exists')
    probe=json.loads((W/'NEW_CREDENTIAL_PROBE.json').read_bytes())
    require(probe['http_status']==200 and probe['status']=='AUTHENTICATED','New credential not verified')
    quiet()
    with stopped_web(quiet) as identity:
        # No runtime files change in this window; the reviewed release is intact.
        identity['resume_allowed']=True
    try:result=await_restart(identity,timeout=55)
    except BaseException as exc:
        record('CREDENTIAL_RELOAD.json',{'status':'FAILED','identity':identity,'error_type':type(exc).__name__})
        raise
    record('CREDENTIAL_RELOAD.json',result)
    print(json.dumps(result))


if __name__=='__main__':main()
