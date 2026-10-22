"""Prepare isolated release and offline checks only. Never apply deployment."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
W=P/'audio_followup'
W.mkdir(exist_ok=True)
(W/'validation').mkdir(exist_ok=True)
R=Path('C:/IALD/projetos_pyhton/IALD')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def fresh(path,raw):
    with path.open('xb') as f:f.write(raw)
    assert path.read_bytes()==raw

primitives={}
for name in ('transaction.py','maintenance.py','deploy_controlled.py'):
    raw=(P/name).read_bytes();fresh(W/name,raw)
    primitives[name]=sha(raw)
candidate=P/'live_stage/audio_guidance_stage/iald_app_providers.py'
raw=candidate.read_bytes()
baseline=(R/'iald_app_providers.py').read_bytes()
preparation=json.loads((candidate.parent/'PREPARATION.json').read_bytes())
assert preparation['source_sha256']==sha(baseline)
assert preparation['candidate_sha256']==sha(raw)
fresh(W/'iald_app_providers.py',raw)
plan={'schema':'iald.mimo26-upgrade/v1','files':[{'source':str(W/'iald_app_providers.py'),
    'destination':str(R/'iald_app_providers.py'),'sha256':sha(raw),'baseline':sha(baseline)}],
    'revision':'AUDIO_GUIDANCE_ISOLATED_R1','science_preserved':'complete prefix unchanged; guidance suffix only',
    'task_reference':str(P/'SESSION_REFERENCE.json')}
plan_raw=json.dumps(plan,ensure_ascii=False,indent=2).encode();fresh(W/'install_plan.json',plan_raw)
plan_sha=sha(plan_raw)
shim='''"""Use the parent mission reference; no new task or context."""
from pathlib import Path
import importlib.util
_path=Path(__file__).resolve().parent.parent/'task.py'
_spec=importlib.util.spec_from_file_location('audio_followup_parent_task',_path)
_parent=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_parent)
W=_parent.W
REF=_parent.REF
UNIT=_parent.UNIT
OWNER=_parent.OWNER
call=_parent.call
project=_parent.project
act=_parent.act
check=_parent.check
new=_parent.new
'''
fresh(W/'task.py',shim.encode())
binding={'reference':str(P/'SESSION_REFERENCE.json'),'reference_sha256':sha((P/'SESSION_REFERENCE.json').read_bytes()),
    'parent_task_sha256':sha((P/'task.py').read_bytes()),'shim_sha256':sha(shim.encode()),'new_context_created':False}
fresh(W/'TASK_REFERENCE_BINDING.json',json.dumps(binding,indent=2).encode())

# Re-run the actual offline transport replay against THIS release candidate.
replay=(P/'live_stage/reproduce_audio_offline.py').read_text(encoding='utf-8')
replay=replay.replace("W=Path(__file__).resolve().parent;R=", "RELEASE=Path(__file__).resolve().parent\nW=RELEASE.parent/'live_stage';R=",1)
replay=replay.replace("provider_source=W/'audio_guidance_stage/iald_app_providers.py' if candidate else R/'iald_app_providers.py'", "provider_source=RELEASE/'iald_app_providers.py' if candidate else R/'iald_app_providers.py'",1)
replay=replay.replace("with (W/('AUDIO_OFFLINE_CANDIDATE.json' if candidate else 'AUDIO_OFFLINE_REPLAY.json')).open('x',encoding='utf-8') as f:", "with (RELEASE/'validation/audio_offline_replay.json').open('x',encoding='utf-8') as f:",1)
fresh(W/'test_audio_replay.py',replay.encode())
completed=subprocess.run([sys.executable,'-B','-X','utf8',str(W/'test_audio_replay.py'),'--candidate'],capture_output=True,timeout=45)
fresh(W/'validation/replay_stdout.txt',completed.stdout or b'(empty)')
fresh(W/'validation/replay_stderr.txt',completed.stderr or b'(empty)')
assert completed.returncode==0,completed.stderr.decode(errors='replace')
result=json.loads((W/'validation/audio_offline_replay.json').read_bytes())
assert result['transport_source_sha256']==sha(raw)
assert result['scientific_prefix_bytes_preserved'] and result['final_typed_user_parts_preserved']
assert result['remote_calls']==result['credential_reads']==result['runtime_writes']==0

# Existing transaction import is side-effect-free; do not call maintenance/apply.
spec=importlib.util.spec_from_file_location('audio_release_transaction',W/'transaction.py')
transaction=importlib.util.module_from_spec(spec);spec.loader.exec_module(transaction)
assert transaction.WORK==W
spec=importlib.util.spec_from_file_location('audio_release_task',W/'task.py')
task=importlib.util.module_from_spec(spec);spec.loader.exec_module(task)
assert task.REF==P/'SESSION_REFERENCE.json'
assert task.W==P
for name in ('transaction.py','maintenance.py','deploy_controlled.py','task.py','iald_app_providers.py'):
    ast.parse((W/name).read_bytes())
assert all((W/name).read_bytes()==(P/name).read_bytes() for name in primitives)
assert sha((R/'iald_app_providers.py').read_bytes())==plan['files'][0]['baseline']
assert len(plan['files'])==1 and Path(plan['files'][0]['source']).is_relative_to(W)
assert not (W/'deployment.json').exists()
checks={'passed':True,'plan_sha256':plan_sha,'tests':[
    'actual_installed_transport_functions_offline_with_original_job_audio_and_release_candidate:PASS',
    'complete_scientific_prefix_preserved:PASS','typed_audio_data_uri_unchanged:PASS',
    'no_remote_or_credential_reads:PASS','candidate_source_hash_matches_plan:PASS',
    'runtime_baseline_still_current:PASS','three_primitives_byte_identical_to_parent:PASS',
    'transaction_WORK_resolves_isolated_release:PASS','task_import_keeps_parent_reference:PASS',
    'python_syntax_five_files:PASS','one_file_plan_source_in_WORK:PASS'],
    'transaction_sha256':primitives['transaction.py'],'maintenance_sha256':primitives['maintenance.py'],
    'deploy_controlled_sha256':primitives['deploy_controlled.py'],
    'replay_receipt_sha256':sha((W/'validation/audio_offline_replay.json').read_bytes()),
    'scope':'Offline code/data integrity only; causal effect on model response unmeasured. Not an independent review or deployment.',
    'applied':False,'remote_calls':0,'same_mission_reference':binding['reference']}
fresh(W/'validation/final_checks.json',json.dumps(checks,ensure_ascii=False,indent=2).encode())
handoff={'status':'PREPARED_NOT_APPLIED_PENDING_INDEPENDENT_REVIEW','release_root':str(W),
    'plan_sha256':plan_sha,'primitives_sha256':primitives,
    'final_checks_sha256':sha((W/'validation/final_checks.json').read_bytes()),
    'review_required':'Reviewer must independently verify candidate/plan/runtime baseline and all three primitive hashes; review_final.json must pin plan_sha256,transaction_sha256,maintenance_sha256 and preferably deploy_controlled_sha256. No review result fabricated here.',
    'task_reference_binding':binding,'files':1,'no_application':True,
    'candidate_effectiveness':'NOT_MEASURED; clarifies system custody references versus effective typed media without forcing perception or inventing observations.'}
fresh(W/'HANDOFF_REVIEW.json',json.dumps(handoff,ensure_ascii=False,indent=2).encode())
print(json.dumps({'release':str(W),'passed':True,'plan_sha256':plan_sha,'applied':False}))
