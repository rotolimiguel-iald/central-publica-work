from pathlib import Path
import datetime, hashlib, json, re, os, subprocess

ROOT=Path(__file__).resolve().parent
NAMES=['ModularRemainderAction.lean','ModularRemainderDensity.lean',
       'ModularCornerCounterexample.lean','DiamondConformalCurrent.lean',
       'ModularDephasingBridge.lean','TowerDephasingStationary.lean']
ALLOWED={'propext','Classical.choice','Quot.sound'}
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def newfile(p,data):
    assert not p.exists()
    q=p.with_name(p.name+'.tmp');q.write_bytes(data)
    assert q.read_bytes()==data
    os.replace(q,p)

result=[]
for name in NAMES:
    p=ROOT/name;info=pin(p);text=p.read_text(encoding='utf8')
    candidates=[]
    for record in (ROOT/'attempts').glob('*/run.json'):
        r=json.loads(record.read_text(encoding='utf8'))
        if r['source']==str(p) and r['sha256']==info['sha256'] and r['returncode']==0:
            candidates.append((record,r))
    assert candidates,('No matching successful compile',name)
    record,r=sorted(candidates)[-1]
    assert r['source_unchanged']
    out=(record.parent/'stdout.txt').read_text(encoding='utf8')
    err=(record.parent/'stderr.txt').read_text(encoding='utf8')
    assert not err.strip() and not re.search(r'\b(error|warning):|sorryAx',out),(name,out,err)
    assert not re.search(r'^\s*(axiom|sorry|admit)\b',text,re.M)
    expected=re.findall(r'^theorem\s+(\w+)',text,re.M)
    axiom_rows=re.findall(r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)",out,re.S)
    assert len(axiom_rows)==len(expected),(name,expected,axiom_rows)
    proofs=[]
    for qualified,deps in axiom_rows:
        axioms={x.strip() for x in deps.split(',') if x.strip()}
        assert axioms<=ALLOWED,(qualified,axioms)
        assert qualified.rsplit('.',1)[-1] in expected
        proofs.append(dict(name=qualified,axioms=sorted(axioms)))
    result.append(dict(source=info,compile_record=pin(record),proofs=proofs))

now=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
audit={'timestamp':datetime.datetime.now().astimezone().isoformat(),
       'files':result,'theorem_count':sum(len(r['proofs']) for r in result),
       'new_sources_elaborated':True,'imported_dependency_objects_reused':True,
       'independent_reviewer':False,'qft_geometricity_proved':False,
       'status':'POSITIVE_FORMAL_BLOCKS_CHECKED; FULL_GOAL_STILL_IN_PROGRESS'}
out=ROOT/f'AUDIT_{now}.json'
newfile(out,json.dumps(audit,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps({'audit':str(out),'theorems':audit['theorem_count']}))
