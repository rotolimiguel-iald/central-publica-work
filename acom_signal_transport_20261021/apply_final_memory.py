"""Apply reviewed additive memory plan with all-target preflight."""
import hashlib,json,sys
from pathlib import Path
import task
sys.path.insert(0,str(task.W/'memory_prepare'))
from atomic_append import append_reviewed

def sha(b): return hashlib.sha256(b).hexdigest()
plan=json.loads((task.W/'memory_prepare/FINAL_R1/PLAN.json').read_bytes())
task.check('deployment')
for item in plan['receipts']+[plan['append']]:
    assert sha(Path(item['path']).read_bytes())==item['sha256']
chunk=Path(plan['append']['path']).read_bytes()
for item in plan['surfaces']:
    raw=Path(item['path']).read_bytes()
    assert sha(raw)==item['before_sha256'], 'Concurrent memory change: '+item['path']
    assert sha(raw+chunk)==item['expected_after_sha256']
if '--apply' not in sys.argv:
    print('PREFLIGHT_PASS');sys.exit(0)
out=[]
for item in plan['surfaces']:
    out.append(append_reviewed(item['path'],chunk,item['before_sha256'],item['expected_after_sha256'],apply=True))
task.new('MEMORY_APPLIED_FINAL.json',{'status':'PASS','surfaces':out,'plan_sha256':sha((task.W/'memory_prepare/FINAL_R1/PLAN.json').read_bytes())})
print('APPLIED_8_SURFACES')
