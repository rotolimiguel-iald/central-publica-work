"""Verify installed pins and prior scientific release; never imports web server."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import sys

W=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    plan=json.loads((W/'INSTALL_PLAN.json').read_bytes())
    baseline=json.loads((W/'science/SCIENCE_STATUS.json').read_bytes())
    exceptions={row['path']:row['after'] for row in plan['files']}
    installed=[{'file':Path(row['path']).name,'match':sha(Path(row['path']))==row['after']} for row in plan['files']]
    kept=[];changed=[];fail=[]
    for row in baseline['installed_files']['checks']:
        actual=sha(Path(row['path']))
        expected=exceptions.get(row['path'],row['actual_sha256'])
        if actual!=expected:fail.append(row['path'])
        elif row['path'] in exceptions:changed.append(Path(row['path']).name)
        else:kept.append(row['path'])
    result={'at':datetime.now(timezone.utc).isoformat(),'status':'PASS' if all(x['match'] for x in installed) and not fail else 'FAIL',
            'runtime':installed,'prior_release_total':len(baseline['installed_files']['checks']),
            'prior_release_unchanged':len(kept),'prior_runtime_replaced_explicitly':changed,'mismatches':fail,
            'science_executed':False,'client_changed':False,'live_provider_test':False}
    with (W/'INSTALLED_VERIFICATION.json').open('x',encoding='utf8') as h:json.dump(result,h,indent=2)
    print(json.dumps(result))
    raise SystemExit(0 if result['status']=='PASS' else 1)


if __name__=='__main__':main()
