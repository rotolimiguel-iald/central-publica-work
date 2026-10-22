"""Capture final staged tests and immutable source hashes. No provider requests."""
from pathlib import Path
import hashlib,json,subprocess,sys
W=Path(__file__).parent
node=r'C:\Program Files\nodejs\node.exe'
commands=[
 ('server',W/'server',[sys.executable,'-B','-X','utf8','-m','unittest','discover','-v']),
 ('adversarial',W,[sys.executable,'-B','-X','utf8','-m','unittest','-v','test_chat_jobs_adversarial','test_chat_jobs_response_contract','test_notification_runtime_adversarial']),
 ('push',W,[sys.executable,'-B','-X','utf8','-m','unittest','discover','-s',str(W/'notifications/tests'),'-p','test_*.py','-v']),
 ('client',W,[node,'--test',str(W/'client/test_chat_jobs.mjs')]),
 ('notification_settings',W,[node,'--test',str(W/'client/test_notification_settings.mjs')]),
 ('push_client',W,[node,'--test',str(W/'notifications/tests/notifications.test.mjs')]),
 ('syntax',W,[node,'--check',str(W/'client/iald.js')]),
]
results=[]
for name,cwd,command in commands:
    result=subprocess.run(command,cwd=cwd,capture_output=True)
    (W/(name+'_tests.log')).write_bytes(result.stdout+b'\n'+result.stderr)
    results.append({'suite':name,'passed':result.returncode==0})
checks={'passed':all(r['passed'] for r in results),'suites':results,'files':{}}
for p in list((W/'server').glob('iald_*.py'))+[W/'client/iald.js']:
    if p.suffix=='.py':compile(p.read_bytes(),str(p),'exec')
    checks['files'][str(p.relative_to(W))]=hashlib.sha256(p.read_bytes()).hexdigest()
(W/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks))
sys.exit(0 if checks['passed'] else 1)
