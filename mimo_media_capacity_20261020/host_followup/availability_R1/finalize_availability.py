import ast,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;LIVE=Path('C:/IALD/projetos_pyhton/IALD')
sys.path.insert(0,str(HERE))
import test_availability as control
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
baseline=json.loads((HERE/'BASELINE.json').read_text())
assert pin(LIVE/'iald_auto_router.py')['sha256']==baseline['sha256']
(HERE/'iald_jev_connection_evidence.json').write_text(json.dumps(control.EVIDENCE,indent=2),encoding='utf-8')
# Run existing whole-chooser capability controls on this exact updated router.
(HERE/'test_capability_regression.py').write_bytes((HERE.parent/'capability_R2/test_capability.py').read_bytes())
outputs=[]
for test in ('test_availability.py','test_capability_regression.py'):
    r=subprocess.run([sys.executable,'-X','utf8',str(HERE/test)],capture_output=True)
    outputs.append(r.stdout+r.stderr);assert r.returncode==0,(r.stdout+r.stderr).decode()
(HERE/'TEST_RESULTS.txt').write_bytes(b'\n'.join(outputs))
def defs(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_bytes()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
old=defs(LIVE/'iald_auto_router.py');new=defs(HERE/'iald_auto_router.py')
changed=[k for k in old if old[k]!=new.get(k)]
assert set(changed)=={'available','choose'}
evidence_target=LIVE/'iald_jev_connection_evidence.json'
assert not evidence_target.exists(),'Parent must reconcile existing evidence instead of overwriting'
files=[dict(source=pin(HERE/'iald_auto_router.py'),target=str(LIVE/'iald_auto_router.py'),baseline_sha256=baseline['sha256']),
       dict(source=pin(HERE/'iald_jev_connection_evidence.json'),target=str(evidence_target),baseline='ABSENT')]
plan=dict(status='STAGED_NOT_INSTALLED_DISTINCT_REVIEW_REQUIRED',files=files,apply=False,
    guard='Parent byte-backup existing source; CAS baseline and evidence target absence; atomically install. Never modify routing journal, ACOM artifacts or activation. No retry of failed job.')
(HERE/'INSTALL_PLAN.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
report=dict(status='AVAILABILITY_LOCAL_REFUSAL_SEPARATION_PASS_STAGED',tests_passed=11,
    root='Latest route failed by local policy BudgetRefusal, but available required its status selected and disabled automatic mode globally despite received JEV200.',
    behavior='Backend ready AND previous selected remain required. Skip only started or dedicated local BudgetRefusal with verified received transport; preserve network/auth/unknown failure barriers. Legacy exception limited to exact row canonical hash plus verified scoped response/result artifact hashes, model and HTTP200. Future receive-only health recorded independently of routing outcome.',
    no_fake_success=True,no_reclassification_of_historical_journals=True,no_retry=True,
    actual_historical_evidence=[pin(control.FAILED_PATH),pin(control.SELECTED_PATH)],
    evidence=pin(HERE/'iald_jev_connection_evidence.json'),plan=pin(HERE/'INSTALL_PLAN.json'),
    tests=pin(HERE/'TEST_RESULTS.txt'),changed_existing_functions=changed,new_helper='_verified_local_routing_refusal',
    files=files,new_network_calls=0,new_provider_calls=0,runtime_writes=0,installed=False,
    limits='Backend health callback stubbed in AST tests; real immutable historic route and scoped received artifacts verified. No live availability claim before parent installs and checks.')
(HERE/'AVAILABILITY_DELIVERY_R1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(receipt=pin(HERE/'AVAILABILITY_DELIVERY_R1.json'),plan=pin(HERE/'INSTALL_PLAN.json'),files=files)))
