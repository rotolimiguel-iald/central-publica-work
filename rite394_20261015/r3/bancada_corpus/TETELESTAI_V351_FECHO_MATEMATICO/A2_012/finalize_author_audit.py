from pathlib import Path
import json, hashlib, re, datetime, os

ROOT=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p): return json.loads(p.read_text(encoding='utf8'))
def put(p,obj):
    assert p.is_relative_to(ROOT) and not p.exists()
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf8')
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b)
    assert t.read_bytes()==b
    os.replace(t,p)

plan=load(ROOT/'AUDIT_NAMES.json')
runpath=ROOT/'attempts/20260915_125636_391635/RESULT.json'
run=load(runpath)
assert run['returncode']==0 and run['source_unchanged']
logpath=Path(run['stdout']['path']); log=logpath.read_text(encoding='utf8')
assert pin(logpath)==run['stdout']
entries=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log)
assert [n for n,_ in entries]==plan['names']
allowed={'propext','Classical.choice','Quot.sound'}
axioms={n:[x.strip() for x in a.split(',') if x.strip()] for n,a in entries}
assert all(set(a)<=allowed for a in axioms.values())
sources=[]
for s in plan['sources']:
    p=Path(s['path']); now=pin(p)
    assert now['sha256']==s['sha256'] and now['bytes']==s['bytes']
    text=p.read_text(encoding='utf8')
    assert not re.search(r'\b(axiom|sorry|native_decide|trustCompiler)\b',text)
    sources.append(now)
controlpath=ROOT/'author_controls/20260915_125804_093873/SEMANTIC_RECLASSIFICATION.json'
controls=load(controlpath)
assert controls['all_rejected_semantically']
for c in controls['controls']:
    assert c['returncode']!=0 and c['semantic_rejection']
    for k in ('source','run','log'):
        assert pin(Path(c[k]['path']))==c[k]

result=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    status='DEV_KERNEL_CHECKED_INDEPENDENT_REVIEW_PENDING',
    public_names=len(axioms),module_count=len(sources),sources=sources,
    all_axioms_allowed=True,axioms=axioms,audit_run=pin(runpath),audit_log=pin(logpath),
    author_negative_controls=len(controls['controls']),controls=pin(controlpath),
    classifier_erratum='GapTwo was semantically rejected by Lean; the first classifier omitted change tactic failed. Original report preserved; no new build invented.',
    constructed=['positive finite projection in regular core from A1 trace',
        'orthogonal equal-trace faces in same regular core',
        'dual-normalized support trace one',
        'minimal representative one minus support, literal kernel projection, unit relative gap',
        'full-domain closed selfadjoint graph and commutant affiliation',
        'ContinuousCornerWitness with reader agreeing with A1 on every positive element',
        'finite positive A1 trace of actual kernel projection',
        'proof that THIS zero-extended reader is not cyclic on arbitrary products'],
    remaining=['exact ContinuousCoreData total trace with legacy laws and A1 compatibility',
        'exact ThreeLocksCoreData consumer',
        'independent review of this frozen source set'],
    full_trace_constructed_in_A1=True,three_locks_core_data_constructed=False,
    full_witness_constructed=False,gate_changed=False,
    scope='The minimal representative is not identified with an unrelated microscopic operator. Failure of this reader is not a no-go for all possible readers.')
put(ROOT/'AUDITORIA_A2_AUTORAL.json',result)
print(json.dumps(dict(audit=pin(ROOT/'AUDITORIA_A2_AUTORAL.json'),names=len(axioms),controls=len(controls['controls'])),ensure_ascii=False))
