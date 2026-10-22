from pathlib import Path
import hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k';OLD=R.parent
V350=OLD.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel'
D=R/'dev_dependencies';assert not D.exists();D.mkdir()
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(D) and not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
seen=set();rows=[]
def walk(n):
 if n in seen or not n.startswith(('TGL.','TGLExt.')):return
 seen.add(n);rel=Path(*n.split('.'));src=K/rel.with_suffix('.lean');code=src.read_text(encoding='utf8')
 for line in re.findall(r'^import (.+)$',code,re.M):
  for x in line.split():walk(x)
 if n=='TGLExt.V351ScalarImaginaryLeftTransport':return
 obj=OLD/'build'/rel.with_suffix('.olean');origin=OLD/'kernel'/rel.with_suffix('.lean')
 if not obj.exists():obj=V350/'.lake/build/lib/lean'/rel.with_suffix('.olean');origin=V350/rel.with_suffix('.lean')
 assert obj.exists(),n
 assert origin.read_bytes()==src.read_bytes(),n
 put(D/rel.with_suffix('.olean'),obj.read_bytes())
 rows.append(dict(module=n,source=pin(src),matching_source=pin(origin),object=pin(obj),dev_copy=pin(D/rel.with_suffix('.olean'))))
walk('TGLExt.V351ScalarImaginaryLeftTransport')
put(D/'PROVENIENCIA.json',json.dumps(dict(status='DEVELOPMENT_ONLY__INHERITED_PROJECT_OBJECTS__NOT_LAKE_ACCEPTANCE',files=rows),ensure_ascii=False,indent=2).encode('utf8'))
print('Dev dependency closure copied:',len(rows))
