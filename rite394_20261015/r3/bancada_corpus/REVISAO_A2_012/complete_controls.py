from review_a2 import *
from run_controls import CASES,COMMON

positive_records=sorted((ROOT/'control_attempts').glob('*/positive/RESULT.json'))
valid=[]
for p in positive_records:
    d=json.loads(p.read_text(encoding='utf-8'))
    if d['returncode']==0 and d.get('object'):
        assert info(Path(d['source']['path']))==d['source']
        assert info(Path(d['object']['path']))==d['object']
        valid.append((p,d))
assert valid
path,positive=valid[-1]
audit=json.loads((path.parent.parent/'audit'/'RESULT.json').read_text(encoding='utf-8'))
assert audit['returncode']==0 and info(Path(audit['source']['path']))==audit['source']
assert info(Path(audit['object']['path']))==audit['object']
names=['IndependentA2.'+n for n in re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev)\s+(\w+)',code_only((SRC/'IndependentA2Controls.lean').read_text(encoding='utf-8')),re.M)]
attempt=ROOT/'control_attempts'/stamp()
for name,body,wall in CASES:
    src=SRC/'controls'/('Bad'+name+'.lean')
    write(src,COMMON+body)
    (attempt/name).mkdir(parents=True,exist_ok=True)
    assert src.resolve().is_relative_to(ROOT) and (attempt/name).resolve().is_relative_to(ROOT)
def job(case):
    name,body,wall=case
    row,out=run(SRC/'controls'/('Bad'+name+'.lean'),attempt/name)
    row.update(name=name,wall=wall,diagnostic=out,
        semantic_rejection=row['returncode']!=0 and 'Type mismatch' in out and
        not re.search(r'unexpected token|unknown (identifier|constant|namespace|module)|object file .* does not exist|failed to',out,re.I))
    print(name,row['returncode'],row['semantic_rejection'],flush=True)
    return row
with futures.ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(job,CASES))
record(ROOT/'CONTROLS.json',dict(positive=positive,audit=audit,names=names,negative_controls=rows,
    all_pass=positive['returncode']==0 and audit['returncode']==0 and len(rows)==len(CASES) and all(r['semantic_rejection'] for r in rows),
    orchestration_note='Previous concurrent source creation hit a path-containment assertion before writing three cases; paths verified inside root, sources/log directories now prepared sequentially. Earlier compiler outputs are retained, and all nine negatives rerun here.'))
