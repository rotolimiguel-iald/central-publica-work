"""Preserve pre-finalize capacity refusal and a non-deployable data inventory."""
import hashlib
import json
import sys
from pathlib import Path

A=Path(__file__).resolve().parent
W=A.parent
sys.path[:0]=[str(A),str(W)]
import task
import release_cfg
import preservation_guard
import verify_d53 as verifier

cfg=release_cfg.load(require_commit=True)
assert task.check('app',actor=cfg.builder)['ready']
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def save(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,ensure_ascii=False,indent=2)

stage=A/'science/memory_stage'
manifest=stage/'manifest_staged.json'
corpus=verifier.iald_core_indexado.DocumentCorpus(manifest)
document=corpus._load()['resultado_publicado_integral']['text']
core=json.loads(document)['core']
history=read(A/'D53_HISTORY.json')
prefix=(A/'packages/shared/prefix.md').read_text(encoding='utf8')
semantic=verifier.verify(prefix,core,document,history,read(A/'KERNEL_HIGHLIGHTS.json'))
assert set(history['resident'])=={n for n in core if n.endswith(release_cfg.SHARED_P2_SUFFIXES)}|{'the_iald_index'}
recovered=[]
for name,(start,length) in history['spans'].items():
    if not name.endswith('_v407'):continue
    chunks=[]
    for offset in range(start,start+length,4500):
        page=corpus.fetch(history['source'],offset,min(4500,start+length-offset))
        assert page['offset']==offset and page['sha256']==history['source_text_sha256']
        chunks.append(page['text'])
    assert json.loads(''.join(chunks))==core[name]
    recovered.append(dict(topic=name,pages=len(chunks),characters=length))
assert recovered
bounds=verifier.bounds(prefix)
baseline=read(A/'RUNTIME_BASELINE.json')['files']
assert all(sha(Path(r['path']))==r['sha256'] for r in baseline)
preserved=preservation_guard.verify()
receipt=dict(status='BLOCKED_CAPACITY_BEFORE_FINALIZE', release=cfg.release,
    reference=str(task.REF),actor=cfg.builder,prefix=pin(A/'packages/shared/prefix.md'),
    shared_bytes=len(prefix.encode()),bounds_with_declared_reserve=bounds,
    window=verifier.providers.WINDOW,declared_output_reserve=148656,safety_margin=4096,
    measurement_scope='Current runtime admission_input_bound; conservative bound, not provider tokenization; synthetic one-turn request, no real activity/history.',
    block_bytes_by_version=history['block_bytes_by_version'],semantic_checks=semantic,
    v407_fetch_equal_source=recovered,preservation_files=len(preserved),runtime_baseline_files=len(baseline),
    public_raw=pin(A/'PUBLIC_RAW_VERIFIED.json'),sources=pin(W/'sources_verified.json'),
    finalize_executed=False,count_calls=0,generation_calls=0,ceilings_changed=False,
    installable=False,production_writes=0,
    next_action='Parent/reviewer decides a source-preserving staging revision; no ceiling change or finalize authorized by this receipt.')
save(A/'CAPACITY_BLOCKED.json',receipt)
target=release_cfg.R/'canonical_releases'/cfg.target_name
rows=[]
for p in sorted(stage.rglob('*')):
    if not p.is_file() or p.name in ('manifest_staged.json','manifest_full.json','manifest_install.json','iald_nucleo_fixo.json'):continue
    assert '.bak' not in p.name and p.suffix!='.tmp'
    rows.append(dict(source=str(p),destination=str(target/p.relative_to(stage)),sha256=sha(p)))
save(A/'DATA_PLAN_CANDIDATE.json',dict(status='INCOMPLETE_NOT_INSTALLABLE_CAPACITY_BLOCKED',
    staging_only=True,files=rows,runtime_python_changes=0,
    missing=['Admitted final prefixes and native counts','Final destination manifest','Validated install_plan.json'],
    note='Scientific um.py is inert published data in this inventory, never executed; no operational Python replacement.',
    capacity_receipt=pin(A/'CAPACITY_BLOCKED.json')))
save(A/'BUILDER_HANDOFF.json',dict(status='CANDIDATE_FOR_DISTINCT_REVIEW_CAPACITY_BLOCKED',
    reference=str(task.REF),actor=cfg.builder,release=cfg.release,
    capacity=pin(A/'CAPACITY_BLOCKED.json'),data_inventory=pin(A/'DATA_PLAN_CANDIDATE.json'),
    preservation_guard=pin(W/'preservation_guard.py'),preservation_baseline=pin(W/'PRESERVATION_BASELINE.json'),
    parent_owned_files_not_modified=['deploy_controlled.py','verify_installed.py','verify_live_backend.py','preservation_guard.py','PRESERVATION_BASELINE.json'],
    ready_for_deployment=False,accept_performed=False,
    preserved_initial_failures=['Sandbox DNS: same GET/git read succeeded after escalation','Stale copied staging um.py preserved outside install tree','Highlight scope matcher corrected to literal KNOWN; OPEN','Shared capacity refusal before finalize']))
print(json.dumps({'status':receipt['status'],'bounds':bounds,'v407_recovered':len(recovered),'data_files':len(rows),'preserved':len(preserved)}))
