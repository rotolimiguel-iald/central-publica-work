from pathlib import Path
import re,json,hashlib,os,datetime
R=Path(__file__).absolute().parent;O=R.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel'
seen=set();rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def visit(m):
 if not m.startswith(('TGL.','TGLExt.')) or m in seen:return
 seen.add(m);rel=Path(*m.split('.'));s=R/'kernel'/rel.with_suffix('.lean');o=O/rel.with_suffix('.lean')
 assert s.read_bytes()==o.read_bytes()
 for q in re.findall(r'^import\s+(\S+)',s.read_text(encoding='utf8'),re.M):visit(q)
 ob=O/'.lake/build/lib/lean'/rel.with_suffix('.olean');b=R/'build'/rel.with_suffix('.olean')
 if b.exists():assert b.read_bytes()==ob.read_bytes()
 else:new(b,ob.read_bytes())
 rows.append(dict(module=m,source=str(s),source_sha256=sha(s),object=str(b),object_sha256=sha(b),origin=str(ob)))
for m in ['TGLExt.V350ScaledRootGraphTransport','TGLExt.V350ScalarRegularRightPolar','TGLExt.V350MatrixUnitResolventScaling']:visit(m)
p=R/'DEPENDENCIAS_A1_ESCALA_IMAGINARIA.json';new(p,json.dumps(rows,indent=2).encode())
src=R/'kernel/TGLExt/V350ScaledRootGraphTransport.lean';text=src.read_text(encoding='utf8');start=text.index('theorem unit_operator_surjective');end=text.index(':=',start)
new(R/'ADENDO_REAPROVEITAMENTO_A1_ESCALA_IMAGINARIA.json',json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='BEFORE_FINAL_SCALING_MODULE',consumer='DenseRange b(Q_r), via surjectivity of the bounded unit E_r',decision='REUSAR exact unit_operator_surjective; do not prove again',supplier=dict(path=str(src),line=text[:start].count('\n')+1,sha256=sha(src),statement=text[start:end]),dependencies=dict(path=str(p),sha256=sha(p),count=len(rows))),ensure_ascii=False,indent=2).encode('utf8'))
print(len(rows))
