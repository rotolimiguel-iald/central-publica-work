import ast,hashlib,json,shutil,sys
from pathlib import Path
O=Path(__file__).resolve().parent;W=O.parent;H=W/'host_followup/availability_R1';D=W/'host_followup/availability_deploy_R1'
sys.path.insert(0,str(W));import task
p=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
def save(p,d):
    raw=json.dumps(d,ensure_ascii=False,indent=2).encode();p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+'.tmp');assert not p.exists() and not tmp.exists()
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p);assert p.read_bytes()==raw
replay=json.loads((O/'REPLAY.json').read_bytes());own=json.loads((O/'OWN_CONTROLS.json').read_bytes());assert replay['passed'] and own['passed']
pins=json.loads((O/'SOURCE_PINS.json').read_bytes())
for entry in pins['sources']+pins['historical_journals']:assert sha(entry['path'])==entry['sha256']
original=json.loads((H/'INSTALL_PLAN.json').read_bytes());rows=[]
D.mkdir(exist_ok=False)
for row in original['files']:
    s=Path(row['source']['path']);target=Path(row['target']);baseline=row.get('baseline_sha256')
    assert sha(s)==row['source']['sha256']
    assert (sha(target) if target.exists() else None)==baseline
    dst=D/'stage'/s.name;dst.parent.mkdir(exist_ok=True);shutil.copyfile(s,dst);assert sha(dst)==sha(s)
    if s.suffix=='.py':ast.parse(dst.read_bytes())
    rows.append(dict(source=str(dst),destination=str(target),sha256=sha(dst),baseline=baseline))
primitives=json.loads((W/'DEPLOYMENT_PRIMITIVES_PREPARED.json').read_bytes())
controls={}
for entry in primitives['files']:
    src=Path(entry['destination']);assert sha(src)==entry['sha256']
    dst=D/src.name;shutil.copyfile(src,dst);assert sha(dst)==entry['sha256'];ast.parse(dst.read_bytes());controls[src.name]=sha(dst)
save(D/'install_plan.json',dict(status='PREPARED_FOR_CONTROLLED_INSTALL',files=rows,adapted_from=pin(H/'INSTALL_PLAN.json'),source_receipt=pin(H/'AVAILABILITY_DELIVERY_R1.json'),adapter='Mechanical schema adaptation; source bytes copied beneath this WORK; exact targets, source hashes and current baselines unchanged.',provider_calls=0))
evidence=[pin(O/name) for name in ('REPLAY.json','OWN_CONTROLS.json','SOURCE_PINS.json','run_review.py')]
checks=dict(passed=True,status='PASS',actor='codex-mimo-capacity-reviewer',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=p['receipt']['revision'],plan_sha256=sha(D/'install_plan.json'),files=len(rows),unique_destinations=len({r['destination'] for r in rows}),runtime_baselines_match=True,source_pins_verified=True,primitive_pins=controls,tests_replayed=11,own_controls=6,historical_journals_unchanged=True,evidence=evidence,runtime_writes=False,new_provider_calls=0)
assert checks['files']==checks['unique_destinations']==2
save(D/'validation/final_checks.json',checks)
review=dict(status='PASS',phase='INSTALL_REVIEW_PASS_LIVE_AFTER_INSTALL',final_delivery_status='FINAL_DELIVERY_NOT_ACCEPTED',actor='codex-mimo-capacity-reviewer',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=p['receipt']['revision'],plan_sha256=checks['plan_sha256'],transaction_sha256=controls['transaction.py'],maintenance_sha256=controls['maintenance.py'],deploy_controlled_sha256=controls['deploy_controlled.py'],findings=[],final_checks=pin(D/'validation/final_checks.json'),evidence=evidence,
    conclusion='Technical approval covers controlled installation of these exact two files BEFORE the distinct live test. No live-before-install requirement. This is not acceptance of the mission deploy requirement.',
    install_conditions=['Parent confirms active manual video is terminal, no other jobs active, and maintenance quiet/CAS preflight succeeds. Do not restart during active request.','Use copied reviewed primitives, byte backups, exact two-file plan and unchanged current baselines; no journal edits, paid health reset or retries.'],
    verified_behavior=['Backend ready and historical selected both required.','Only received HTTP200 local BudgetRefusal skipped; historical exception bound to exact row plus scoped hashed response/result artifacts.','Network/auth/protocol/unknown failures continue to block.','Historical failed receipt remains failed; no fabricated selected record.'],
    limits=['Future connection_health is trusted host-generated local journal metadata recorded after validated HTTP200; it is not independent cryptographic authentication.','No remote calls or runtime writes by reviewer. No live success, maximum capacity, physical device installation or completed distribution asserted.','Final mission deploy acceptance remains pending parent submission, installed/live evidence and coordinated availability matrix. Existing build/push hold remains until those gates are reviewed.'])
save(D/'validation/review_final.json',review)
save(D/'validation/INSTALL_PHASE_ADDENDUM_R1.json',dict(status='INSTALL_REVIEW_PASS_LIVE_AFTER_INSTALL',final_delivery='FINAL_DELIVERY_NOT_ACCEPTED',review=pin(D/'validation/review_final.json'),plan=pin(D/'install_plan.json'),meaning='Controlled two-file installation is technically approved; post-install live validation necessarily follows installation. Wait for active video terminal and fresh quiet/preflight. No final task acceptance and no override of automatic approval review.'))
save(O/'REVIEW_FINAL.json',review|dict(prepared_deploy_directory=str(D),install_review=pin(D/'validation/review_final.json'),original_plan_unchanged=pin(H/'INSTALL_PLAN.json')))
print(json.dumps(dict(status='PASS',phase=review['phase'],prepared=str(D),plan_sha256=checks['plan_sha256'],review_sha256=sha(D/'validation/review_final.json'),mission_revision=p['receipt']['revision'])))
