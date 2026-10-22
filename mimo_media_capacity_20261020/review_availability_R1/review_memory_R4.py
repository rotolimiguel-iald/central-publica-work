import ast,hashlib,importlib.util,json,re,sys
from pathlib import Path
W=Path(__file__).resolve().parent.parent;H=W/'memory_stage/FINAL_R4'
sys.path.insert(0,str(W));import task
current=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
P=H/'PLAN.json';C=H/'audit_apply_parent.py';plan=json.loads(P.read_bytes());relay=json.loads((H/'PLANCK_PARENT_RELAY.json').read_bytes());report_text=(H/'RELATORIO.txt').read_text(encoding='utf-8')
assert sha(P) in report_text and sha(C) in report_text and sha(H/'SOURCES.json') in report_text
assert sha(P)==relay['plan']['sha256'] and sha(C)==relay['candidate']['sha256']
oldH=W/'memory_stage/DRAFT_R3_FINAL_ENGINEERING';old=json.loads((oldH/'PLAN_DRAFT.json').read_bytes())
assert {r['path'] for r in plan['surfaces']}=={r['path'] for r in old['surfaces']}
def funcs(path):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_bytes()).body if isinstance(n,ast.FunctionDef)}
assert funcs(C)==funcs(oldH/'audit_apply_parent.py')
spec=importlib.util.spec_from_file_location('memory_R4_reviewer',C);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.WORK==W and m.PLAN==P and m.REFERENCE==W/'SESSION_REFERENCE.json'
m.audit(plan)
text=[Path(r['append']['path']).read_text(encoding='utf-8') for r in plan['surfaces']]
assert len(set(text))==1
t=text[0];sizes=[Path(r['append']['path']).stat().st_size for r in plan['surfaces']];assert max(sizes)<=4500
assert 'DRAFT' not in t and 'NÃO APLICADO' not in t and 'não aplicado' not in t.lower()
for required in ('Evento1072 registra pergunta pendente por AGENT, não ordem/aceite humano','AGUARDA_OPERADOR','US$0.50 extra sem resposta','PERCEPTION_FAILURE','transporte/usage incertos','não consumo medido/fatura','não inspeção física nem confirmação humana','nem implica aceite final da missão','19/19','5/5'):
    assert required in t,required
assert sha(H/'SOURCES.json') in t
assert json.loads((W/'extra_test_pending_unit.json').read_bytes())[0]['status']=='AGUARDA_OPERADOR'
for number in ('0.000837816','0.12155292','0.478237695','0.6712981122'):assert number in t
# Reuse only exact unchanged applicator function tests; superseded R3 text/GO is not approval for any apply.
fixture=W/'review_memory_engineering_R3/INDEPENDENT_CHECKS.json';prior=json.loads(fixture.read_bytes());assert prior['status']=='PASS' and len(prior['fixture_checks'])==4
checks=dict(status='PASS',actor='codex-mimo-capacity-reviewer',scope='MEMORY_8_SURFACES',phase='TECHNICAL_MEMORY_APPLY_GO_FINAL_ACCEPTANCE_AFTER_RECEIPTS',technical_go=True,final_delivery='FINAL_DELIVERY_NOT_ACCEPTED',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=current['receipt']['revision'],plan_sha256=sha(P),candidate_sha256=sha(C),plan=pin(P),candidate=pin(C),sources_index=pin(H/'SOURCES.json'),source_count=len(plan['sources']['sources']),surfaces=8,append_bytes=sizes,findings=[],resolved=['Applied content has no DRAFT/NÃO APLICADO assertion.','Event1072 is explicitly pending agent question, no human authorization.'],
    verification=['All current source, runtime19/science5, eight baseline/append and expected-concatenation pins pass candidate read-only audit.','Eight authorized destinations exactly match previous surface allowlist; no originals written.','All applicator functions byte-equivalent by AST to previously fixture-tested code; only plan filename updated. Backup/CAS/restore/partial-failure guards preserved.','SOURCES hash read from actual file matches all applied texts; no scientific claim/promotion introduced.'],
    evidence=[pin(fixture),pin(Path(__file__)),pin(H/'PLANCK_PARENT_RELAY.json')],
    authorization='Parent may apply these exact eight FINAL_R4 append payloads using this script only after explicit plan/review/script-bound GO and fresh current own-actor deploy preflight. This supersedes R3 technical approval; R3 must not be applied.',
    limits=['Audit and review are read-only on authoritative memories. No application, final task acceptance, provider request or board/map movement by reviewer.','Fresh projection read here is a snapshot; actual owner must obtain current revision/lease preflight at apply time.','Application is atomic per surface, not globally across eight. Partial failure stops without automatic replay; preserve backups/intents/receipts.','Final acceptance follows actual eight application/backups/index-preservation receipts and real parent final delivery/submission.','Extra USD0.50 authorization remains unanswered; video uncertainty/audio perception negative and non-invoice costs remain explicit.'])
out=H/'REVIEW_MEMORY_8_SURFACES_R4.json';raw=json.dumps(checks,ensure_ascii=False,indent=2).encode();tmp=out.with_suffix('.json.tmp')
assert not out.exists()
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out);assert out.read_bytes()==raw
print(json.dumps(dict(status='PASS',revision=current['receipt']['revision'],append_max=max(sizes),sources=checks['source_count'],review=pin(out))))
