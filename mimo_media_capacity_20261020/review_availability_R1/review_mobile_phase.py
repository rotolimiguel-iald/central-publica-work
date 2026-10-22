import ast,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent.parent;H=W/'client_stage/android30_R8_bound'
sys.path.insert(0,str(W));import task
p=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
delivery=json.loads((H/'DELIVERY_BOUND_R8.json').read_bytes())
checked=[]
for e in delivery['files']+[delivery['final19'],delivery['release_binding']]:
    assert sha(e['path'])==e['sha256'];checked.append(e)
spec=importlib.util.spec_from_file_location('review_mobile_lineage',H/'release_lineage_R8.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
build=json.loads((H/'ANDROID30_BUILD_PLAN_R1.json').read_bytes());publish=json.loads((H/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json').read_bytes())
state=g.verify_final_state(build,W);assert len(state)==19
root=Path(publish['repository'])
allowed={'www/iald.js','ios/App/App/public/iald.js','ios/App/App.xcodeproj/project.pbxproj','android/app/build.gradle'}
assert set(publish['files'])==allowed
def git(*args):
    r=subprocess.run(['git','-C',str(root),*args],capture_output=True,check=True);return r.stdout
assert git('branch','--show-current').decode().strip()==publish['branch']
assert git('rev-parse','HEAD').decode().strip()==publish['baseline_head']
assert git('remote','get-url','origin').decode().strip() in publish['exact_origins']
assert git('remote','get-url','--push','origin').decode().strip() in publish['exact_origins']
assert not git('diff','--cached','--name-only','-z')
assert set(filter(None,git('diff','HEAD','--name-only','-z').decode().split('\0')))==allowed
assert set(git('ls-files','--',*sorted(allowed)).decode().splitlines())==allowed
for name,s in publish['files'].items():assert sha(root/name)==s
for name in ('private_mobile_publish_R1.py','run_android30_R1.py','release_lineage_R8.py'):ast.parse((H/name).read_bytes())
# Explicitly reproduce stale admission as refusal, never issue a synthetic PASS receipt.
try:g.verify_release_admission({},build,W)
except RuntimeError:stale_guard_refuses=True
else:raise AssertionError('Expected missing-live receipt refusal')
result=dict(status='PASS_BUILD_PUSH_TECHNICAL_SCOPE',execution_binding_status='R8_REQUIRES_EXPLICIT_PHASE_REBIND_BEFORE_EXECUTION',actor='codex-mimo-capacity-reviewer',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=p['receipt']['revision'],final_delivery='FINAL_DELIVERY_NOT_ACCEPTED',effective_runtime_files_verified=19,science_baseline_verified=True,mobile_six_pins_verified=True,repository_allowlist=sorted(allowed),repository_branch=publish['branch'],baseline_head=publish['baseline_head'],pins=checked,build_plan=pin(H/'ANDROID30_BUILD_PLAN_R1.json'),publish_plan=pin(H/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json'),review_script=pin(Path(__file__)),
    checks=dict(all_bound_file_hashes_match=True,installed_chain_and_all19_current_hashes_match=True,science_and_client_R7_preserved=True,private_origin_allowlist_matches=True,exactly_four_tracked_changes=True,index_empty=True,stale_autotest_guard_refuses=stale_guard_refuses),
    phase_decision='The human-authorized local Android30 build and private four-file commit/push may progress as an engineering/distribution phase, independently of provider perception success. No extra provider call is authorized by this review.',
    required_binding_correction='Existing pinned R8 verify_release_admission still requires autotest PASS and dispatch_live_pass=true. Producer must make a new explicit immutable phase-specific binding/guard/receipt preserving final19/science/mobile pins, exact repo allowlist, human source, fresh deploy preflight and execution_authorized_now; retain old guard/history. Do not fabricate autotest_verification PASS, monkeypatch, disable the guard or reuse an old admission. Re-pin changed execution files before use.',
    limits=['Audio transport completed with negative perception; video failed/uncertain is preserved without retry. No provider PASS inferred.','Any additional USD0.50 automatic test requires the pending human choice; this artifact neither spends nor supplies that choice.','Push may trigger configured iOS CI; existing authorization covers scoped source publication, not proof of successful build, TestFlight groups or physical installation.','Review does not execute build, commit, push, restart, model call or task acceptance.','Final engineering delivery may state provider perception limitations honestly; it must report actual installed/live/distribution outcomes and unresolved uncertain operation status.'])
out=W/'REVIEW_BUILD_PUSH_PHASE_R8.json';raw=json.dumps(result,ensure_ascii=False,indent=2).encode()
with out.open('xb') as f:f.write(raw)
assert out.read_bytes()==raw
print(json.dumps(dict(status=result['status'],runtime_files=19,repo_files=4,phase_rebind_required=True,report=str(out),sha256=sha(out))))
