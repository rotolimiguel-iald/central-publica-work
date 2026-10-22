from pathlib import Path
import datetime,hashlib,json,os,re

ROOT=Path(__file__).resolve().parent
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def replace(p,b):
    assert p.is_relative_to(ROOT) and b
    old=pin(p) if p.exists() else None
    if old:
        raw=p.read_bytes(); bak=p.with_name(p.name+'.bak_'+stamp)
        bak.write_bytes(raw);assert bak.read_bytes()==raw
    t=p.with_name(p.name+'.tmp_'+stamp);t.write_bytes(b)
    assert t.read_bytes()==b
    os.replace(t,p)
    return dict(before=old,after=pin(p))

assert not (ROOT/'DELTA01_PODA.json').exists()
specs=[
 ('V354FiniteTraceSupport','scalarTrace_finite_positive_seed',
  '/-- An actual finite positive seed in A1\'s regular core. -/',
  '/-- Kernel projections stay in the same von Neumann algebra.'),
 ('V354SpectralThreshold','scalarTrace_finite_projection_exists',
  'theorem scalarTrace_finite_projection_exists',
  '#print axioms positive_operator_has_threshold_projection')]
changes=[]
for module,name,start,end in specs:
    p=ROOT/'src/TGLExt'/(module+'.lean');s=p.read_text(encoding='utf8')
    a=s.index(start);z=s.index(end,a)
    removed=s[a:z]
    assert name in removed and re.search(r'^(?:theorem|def) ',removed,re.M)
    s=s[:a]+s[z:]
    assert s.count('#print axioms '+name+'\n')==1
    s=s.replace('#print axioms '+name+'\n','')
    changes.append(dict(module=module,name=name,removed=removed,**replace(p,s.encode('utf8'))))

old=json.loads((ROOT/'AUDIT_NAMES.json').read_text(encoding='utf8'))
names=[];sources=[]
for rec in old['sources']:
    p=Path(rec['path']);s=p.read_text(encoding='utf8')
    ns=re.findall(r'^(?:theorem|def)\s+(\w+)',s,re.M)
    names+=['TGLV350.Regular.'+n for n in ns]
    sources.append(dict(**pin(p),names=ns))
removed={'TGLV350.Regular.'+s[1] for s in specs}
assert set(old['names'])-set(names)==removed and len(names)==len(old['names'])-2
audit=ROOT/'src/TGLExt/AuditA2RegularSupport.lean'
audit_change=replace(audit,('import TGLExt.V354TraceReaderWall\n\n'+'\n'.join('#print axioms '+n for n in names)+'\n').encode('utf8'))
replace(ROOT/'AUDIT_NAMES_DELTA01.json',json.dumps(dict(names=names,sources=sources),ensure_ascii=False,indent=2).encode('utf8'))
replace(ROOT/'DELTA01_PODA.json',json.dumps(dict(timestamp=stamp,
    reviewer_finding='P2-01',reason='Remove only the two unused unit specializations; retain actual general suppliers; do not create artificial consumers.',
    changes=changes,audit_change=audit_change,public_names=len(names),
    previous_audit_preserved=pin(ROOT/'AUDITORIA_A2_AUTORAL.json'),
    proof_bodies_of_remaining_names_unchanged=True,gate_changed=False),ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(delta=pin(ROOT/'DELTA01_PODA.json'),public_names=len(names)),ensure_ascii=False))
