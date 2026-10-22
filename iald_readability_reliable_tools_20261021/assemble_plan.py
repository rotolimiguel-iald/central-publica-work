from task import W,new,check
from pathlib import Path
import hashlib,json,ast
R=Path(r'C:\IALD\projetos_pyhton\IALD');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
check('implementation')
rows=[]
def row(src,dst):
    assert src.is_file() and dst.is_file()
    rows.append(dict(source=str(src),destination=str(dst),sha256=sha(src),baseline=sha(dst)))
for folder in [R/'app',R/'iald-app/www',R/'iald-app/ios/App/App/public',R/'iald-app/android/app/src/main/assets/public']:
    for name in ['iald.js','iald.css']:row(W/'client_stage/R2'/name,folder/name)
for item in json.loads((W/'provider_stage/INSTALL_PLAN.json').read_bytes())['files']:
    src=Path(item['install_from']['path']);dst=Path(item['destination']);assert sha(src)==item['install_sha256'] and sha(dst)==item['expected_destination_sha256'];ast.parse(src.read_text(encoding='utf-8'));row(src,dst)
for item in json.loads((W/'NATIVE_PLAN.json').read_bytes())['files']:
    src=Path(item['source']);dst=Path(item['destination']);assert sha(src)==item['sha256'] and sha(dst)==item['baseline'];row(src,dst)
new('install_plan.json',dict(status='PREPARED_NOT_INSTALLED',files=rows,science_baseline=str(W/'SCIENCE_BASELINE.json'),accounts_modified=False,wallet_modified=False))
(W/'validation').mkdir(exist_ok=True)
new('validation/final_checks.json',dict(passed=True,scope='Sources/baselines/Python syntax; independent client/provider behavioural tests and review required separately',plan_sha256=sha(W/'install_plan.json'),files=len(rows)))
print(json.dumps(dict(files=len(rows),plan_sha256=sha(W/'install_plan.json'))))
