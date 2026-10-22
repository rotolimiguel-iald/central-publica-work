"""Pin staged sources and record offline validation; never install."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
LIVE=Path('C:/IALD/projetos_pyhton/IALD')
def pin(p):
    raw=p.read_bytes()
    return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
result=subprocess.run([sys.executable,'-X','utf8',str(HERE/'test_host.py')],capture_output=True)
(HERE/'HOST_TEST_OUTPUT.txt').write_bytes(result.stdout+result.stderr)
assert result.returncode==0,(result.stdout+result.stderr).decode('utf-8',errors='replace')
baseline=json.loads((HERE/'BASELINE.json').read_text())
assert pin(LIVE/'iald_web_server.py')['sha256']==baseline['server_sha256']
assert pin(LIVE/'iald_app_spend.py')['sha256']==baseline['spend_sha256']
def definitions(path):
    return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_bytes()).body
            if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
old=definitions(LIVE/'iald_web_server.py');new=definitions(HERE/'iald_web_server.py')
changed=sorted(k for k,v in old.items() if new.get(k)!=v)
expected={'_RequisicaoIALD','_mimo_media_limits','api_task_capabilities','_chat_automatico_autorizado','_chat_avaliacao','_api_post_with_wallet'}
assert set(changed)<=expected,changed
backend=json.loads((WORK/'backend_stage/BACKEND_R4_HANDOFF.json').read_text())
for name,digest in backend['files'].items():
    assert pin(WORK/'backend_stage'/name)['sha256']==digest,name
files=[dict(source=pin(HERE/name),target=str(LIVE/name),baseline_sha256=(baseline['server_sha256'] if name=='iald_web_server.py' else baseline['spend_sha256'] if name=='iald_app_spend.py' else None))
       for name in ('iald_web_server.py','new_private_media_host.py','iald_app_spend.py')]
plan=dict(status='STAGED_ONLY_REQUIRES_DISTINCT_REVIEW_PARENT_ASSEMBLY',files=files,
          reference=str(WORK/'SESSION_REFERENCE.json'),backend_receipt=pin(WORK/'backend_stage/BACKEND_R4_HANDOFF.json'),
          dependencies=[pin(WORK/'backend_stage'/n) for n in ('private_media_store.py','private_media_routes.py','iald_mimo_multimodal.py','iald_app_providers.py')]+[pin(WORK/'routing_stage/iald_media_budget.py')],
          apply=False,backup='Parent must byte-backup current targets and CAS-check baselines before atomic installation; new module absent baseline requires parent check.')
(HERE/'HOST_INSTALL_PLAN_FINAL.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
report=dict(status='HOST_FINAL_OFFLINE_PASS_READY_FOR_DISTINCT_REVIEW',host_tests=15,
            actual_server_imported=False,real_auth_function_AST=True,token_verifier='synthetic stub',
            expected_partition='POST/GET required32hex, constant time, auth independent, mismatch403 before body/store; echo stripped before typed part',
            changed_existing_definitions=changed,production_baselines_unchanged=True,
            boundary=json.loads((HERE/'REAL_BYTE_BOUNDARY.json').read_text()),
            plan=pin(HERE/'HOST_INSTALL_PLAN_FINAL.json'),tests=pin(HERE/'HOST_TEST_OUTPUT.txt'),
            evidence=[pin(HERE/n) for n in ('test_host.py','test_real_boundary.py','REAL_BYTE_BOUNDARY.json','build_host.py','BASELINE.json')],
            provider_calls=0,network_calls=0,runtime_writes=0,installed=False,
            limits='Local synthetic WAV and stubbed auth identities; no remote capacity/perception benchmark, live server import or deployment. Parent owns final review and assembly.')
(HERE/'HOST_FINAL_RECEIPT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(plan=pin(HERE/'HOST_INSTALL_PLAN_FINAL.json'),receipt=pin(HERE/'HOST_FINAL_RECEIPT.json'),changed=changed)))
