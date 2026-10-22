import hashlib,importlib.util,json,sys,tempfile
from pathlib import Path
W=Path(__file__).resolve().parent.parent;H=W/'memory_stage/DRAFT_R3_FINAL_ENGINEERING';O=W/'review_memory_engineering_R3';O.mkdir(exist_ok=False)
sys.path.insert(0,str(W));import task
current=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
def save(p,d):
    data=json.dumps(d,ensure_ascii=False,indent=2).encode();tmp=p.with_suffix(p.suffix+'.tmp')
    assert not p.exists()
    with tmp.open('xb') as f:f.write(data)
    assert tmp.read_bytes()==data;tmp.replace(p)
P=H/'PLAN_DRAFT.json';plan=json.loads(P.read_bytes());relay=json.loads((H/'PLANCK_PARENT_RELAY.json').read_bytes())
assert sha(P)==relay['plan']['sha256'] and sha(H/'audit_apply_parent.py')==relay['candidate']['sha256']
spec=importlib.util.spec_from_file_location('memory_engineering_candidate',H/'audit_apply_parent.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.WORK==W and m.REFERENCE==W/'SESSION_REFERENCE.json'
m.audit(plan) # read-only, all56 source pins + current19/science5 + eight baseline/append pins
inherited=json.loads(Path(plan['inherited_surface_list']['path']).read_bytes());assert sha(plan['inherited_surface_list']['path'])==plan['inherited_surface_list']['sha256']
assert {r['path'] for r in plan['surfaces']}=={r['path'] for r in inherited['surfaces']}
texts=[Path(row['append']['path']).read_text(encoding='utf-8') for row in plan['surfaces']]
assert len(set(texts))==1
text=texts[0]
for required in ('PERCEPTION_FAILURE','incertos','NÃO consumo medido','não fatura','US$0.50','AGUARDA_OPERADOR','NÃO inspeção física','não move mapa/quadro','19/19','5/5'):
    assert required in text,required
cost=json.loads((W/'live_stage/TEST_COST_ROLLUP_R1.json').read_bytes())
assert cost['additional_test_authorization']=='PENDING_USER_REPLY_NO_NEW_PAID_TEST'
for value in ('0.6712981122','0.478237695','0.12155292','0.000837816'):assert value in text
pending=json.loads((W/'extra_test_pending_unit.json').read_bytes());assert pending[0]['status']=='AGUARDA_OPERADOR'
baseline={Path(r['path']):sha(r['path']) for r in plan['surfaces']};index=pin(plan['index_policy']['path'])
fixture_checks=[]
with tempfile.TemporaryDirectory(dir=O) as d:
    d=Path(d);target=d/'MEMORY_2.md';suffix=d/'suffix.txt';before=b'original\r\nbytes\r\n';append=b'\r\nADDITIVE\r\n'
    target.write_bytes(before);suffix.write_bytes(append)
    row=dict(path=str(target),before_sha256=hashlib.sha256(before).hexdigest(),append=dict(path=str(suffix),sha256=sha(suffix)),expected_after_sha256=hashlib.sha256(before+append).hexdigest(),expected_after_bytes=len(before+append))
    receipt=m.append_one(row);assert target.read_bytes()==before+append and Path(receipt['backup']).parent==target.parent and Path(receipt['backup']).read_bytes()==before
    fixture_checks.extend(['exact CRLF append preserved','immediate same-folder byte backup exact'])
    try:m.append_one(row)
    except RuntimeError:fixture_checks.append('repeat baseline CAS refused')
    else:raise AssertionError('repeat accepted')
    original=d/'other.md';original.write_bytes(before);bad=dict(row,path=str(original));suffix.write_bytes(b'changed')
    try:m.append_one(bad)
    except RuntimeError:fixture_checks.append('tampered append refused before original write')
    else:raise AssertionError('tamper accepted')
    assert original.read_bytes()==before
for path,digest in baseline.items():assert sha(path)==digest
assert pin(plan['index_policy']['path'])==index
save(O/'INDEPENDENT_CHECKS.json',dict(status='PASS',mission_revision=current['receipt']['revision'],all_source_pins=56,actual_runtime_files=19,actual_science_hashes=5,surfaces=8,append_texts_identical=True,surface_allowlist_equals_inherited=True,fixture_checks=fixture_checks,all_original_memory_and_index_bytes_unchanged=True,provider_calls=0))
review=dict(status='PASS',scope='MEMORY_8_SURFACES',phase='TECHNICAL_MEMORY_APPLY_GO_FINAL_ACCEPTANCE_AFTER_RECEIPTS',technical_go=True,actor='codex-mimo-capacity-reviewer',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=current['receipt']['revision'],plan_sha256=sha(P),candidate_sha256=sha(H/'audit_apply_parent.py'),plan=pin(P),candidate=pin(H/'audit_apply_parent.py'),findings=[],evidence=[pin(O/'INDEPENDENT_CHECKS.json'),pin(Path(__file__))],
    semantic_verdict='Eight additive texts preserve audio PERCEPTION_FAILURE despite completed transport, video failed/uncertain and reserved-cap estimate rather than provider invoice, no retries, pending extra USD0.50 human choice/AGUARDA_OPERADOR, Apple-reported35 distinct from physical verification, and no new scientific theory or gate promotion.',
    authorization='Technical approval for parent application of exactly these eight append payloads using reviewed candidate, explicit plan/review/script-bound parent GO and fresh own-actor deploy preflight. Historical draft revision8 in text remains a dated snapshot; this review uses fresh revision.',
    apply_controls=['Immediate raw-byte backup in same folder, verified before replacement; source and append SHA checked; exact result length/hash.','Atomic per-file append with final baseline CAS and post-write verification/restore; no eight-file global transaction promised.','Exclusive durable intent and partial-failure receipt; stop without automatic replay, preserve all backups.','MEMORY.md index unchanged; diary goes to MEMORY_2.md. No board/map movement by this applicator.'],
    limits=['Review writes only own artifacts and temporary fixtures; original memory surfaces not edited.','No real application has occurred in this review. DRAFT/NÃO APLICADO wording identifies origin snapshot; actual APPLIED receipt must separately establish application.','No final mission acceptance. After application, verify all eight original-prefix/append hashes, immediate backups/index preservation and final delivery/submission.','Parent q/p handles and separately pending budget authorization retain their own state; no extra provider execution or scientific promotion is authorized.'])
save(H/'REVIEW_MEMORY_8_SURFACES_R3.json',review)
save(W/'REVIEW_MEMORY_ENGINEERING_R3.json',review)
print(json.dumps(dict(status='PASS',revision=current['receipt']['revision'],surfaces=8,fixture_checks=len(fixture_checks),review=pin(H/'REVIEW_MEMORY_8_SURFACES_R3.json'))))
