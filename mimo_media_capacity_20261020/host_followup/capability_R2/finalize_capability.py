import ast,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;LIVE=Path('C:/IALD/projetos_pyhton/IALD')
def pin(p):
    raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
baselines=json.loads((HERE/'BASELINES.json').read_text())
for name,digest in baselines.items():assert pin(LIVE/name)['sha256']==digest,name
result=subprocess.run([sys.executable,'-X','utf8',str(HERE/'test_capability.py')],capture_output=True)
(HERE/'TEST_RESULTS.txt').write_bytes(result.stdout+result.stderr);assert result.returncode==0
def definitions(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_bytes()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
changed={}
for name in baselines:
    before=definitions(LIVE/name);after=definitions(HERE/name)
    changed[name]=[key for key in before if before[key]!=after.get(key)]
assert changed=={'new_private_media_host.py':['video_proposals'],'iald_auto_router.py':['choose'],'iald_web_server.py':['_chat_automatico_autorizado','_chat_avaliacao']},changed
files=[dict(source=pin(HERE/name),target=str(LIVE/name),baseline_sha256=digest) for name,digest in baselines.items()]
plan=dict(status='STAGED_NOT_APPLIED_DISTINCT_REVIEW_REQUIRED',files=files,
    reference=str(HERE.parent.parent/'SESSION_REFERENCE.json'),apply=False,
    installation='Parent verifies baselines, byte backups and atomic staged installation under existing controlled process. No replay of failed job; any authorized live test uses a distinct unit.')
(HERE/'INSTALL_PLAN_R2.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
diagnosis=json.loads((HERE.parent/'DIAGNOSIS_FIX_RECEIPT.json').read_text())
receipt=dict(status='CAPABILITY_R2_LOCAL_PASS_PENDING_DISTINCT_REVIEW_NOT_INSTALLED',
    supersedes_diagnostic_only_solution=True,failed_job_preserved=diagnosis['job_id'],
    root='Audio-only full history offered two equivalent video policies; JEV confidence0.68 fell below unchanged0.70 multi-option gate.',
    change='Host emits one audio_full plan for audio-only full history. Router requires one ESTIMADO validated plan, nonempty all-audio items with exact occurrence count, no video count; omits redundant question and returns exact host ID. JEV executor selection/auth/ledger remain; no retry. Other cases keep normal policy choice/gate.',
    compatibility='Internal policy schema fps/resolution remains for backend compatibility; audio payload and quality are not transformed.',
    tests=dict(passed=5,whole_choose_AST=True,captured_post_mock=True,full_public_science=True,context_and_cost_bound_equal=True,
        multi_option_audio_068_refused=True,video_and_mixed_068_refused=True,invalid_plan_before_post=True,extra_answer_refused=True,
        collaborations='Control/capability/memory/wallet collaborators stubbed; entire staged choose and real budget engine used; no live provider.',output=pin(HERE/'TEST_RESULTS.txt')),
    historical_actual_dispatch_evidence=diagnosis['actual_dispatch_evidence'],historical_ledger=diagnosis['ledger'],
    changed_functions=changed,plan=pin(HERE/'INSTALL_PLAN_R2.json'),sources=files,
    evidence=[pin(HERE/name) for name in ('test_capability.py','BASELINES.json')],
    new_provider_calls=0,new_network_calls=0,runtime_writes=0,installed=False)
(HERE/'CAPABILITY_DELIVERY_R2.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(dict(receipt=pin(HERE/'CAPABILITY_DELIVERY_R2.json'),plan=pin(HERE/'INSTALL_PLAN_R2.json'),files=files)))
