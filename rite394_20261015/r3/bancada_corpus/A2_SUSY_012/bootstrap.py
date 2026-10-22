from support import *
import shutil,time
base=ROOT.parent/'TETELESTAI_V351_FECHO_MATEMATICO'
k=base/'RETOMADA_A1B_012/k'
a2=base/'A2_012'
start=stamp();rows=[]
for p in k.rglob('*'):
 if not p.is_file() or '.git' in p.relative_to(k).parts: continue
 assert not p.is_symlink()
 dst=ROOT/'k'/p.relative_to(k); dst.parent.mkdir(parents=True,exist_ok=True)
 assert not dst.exists()
 tmp=dst.with_name(dst.name+'.copytmp');shutil.copyfile(p,tmp)
 h=digest(p); assert tmp.stat().st_size==p.stat().st_size and digest(tmp)==h
 os.replace(tmp,dst);rows.append(dict(source=str(p),local=str(dst),bytes=dst.stat().st_size,sha256=h))
 if len(rows)%10000==0: print('copied',len(rows),flush=True)
record(ROOT/'COPIA_A1.json',dict(start=start,finish=stamp(),method='byte copy, SHA256 both ends; no hardlinks',files=rows))
plan=json.loads((a2/'AUDIT_NAMES_DELTA01.json').read_text(encoding='utf8'))
for row in plan['sources']:
 p=Path(row['path']); assert digest(p)==row['sha256']
 atomic(ROOT/'k/TGLExt'/p.name,p.read_bytes())
record(ROOT/'COPIA_A2.json',plan)
print('COPY_COMPLETE',len(rows),flush=True)
