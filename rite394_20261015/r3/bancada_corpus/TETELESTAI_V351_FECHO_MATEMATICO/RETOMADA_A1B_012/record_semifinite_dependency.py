from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert not p.exists() and p.is_relative_to(R)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
run=R/'existing_semifinite_dependency_attempts/20260914_231037_491709/run.json'
j=json.loads(run.read_text(encoding='utf8'));assert j['returncode']==0 and j['sources_unchanged_during_build']
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='REAL__OLD_WOT_CLOSURE_REPRODUCED',run=pin(run),sources=[pin(R/'k/TGLExt'/n) for n in ['V350FixedBaseEquivalence.lean','V351ExtendedBaseDualWeight.lean','V351ScalarWeightSemifiniteness.lean']],
    scope='The old WOT closure of the ORIGINAL dual-weight domain is imported, not re-proved. Lake reproduced three existing source modules, unchanged, for this dependency. They do not establish semifiniteness of the new limit by themselves, and do not count as new results. No author/DEV objects may be used for independent acceptance.')
put(R/'ADENDO_FICHA_SEMIFINITUDE_FORNECEDOR.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[REAL — fornecedor antigo reproduzido]\n\n'+d['timestamp']+'\n\n'+d['scope']+'\n\n'
for q in d['sources']:s+=q['path']+' — '+q['sha256']+'\n\n'
s+='Run: '+str(run)+'\n'
put(R/'ADENDO_FICHA_SEMIFINITUDE_FORNECEDOR.md',s.encode('utf8'))
