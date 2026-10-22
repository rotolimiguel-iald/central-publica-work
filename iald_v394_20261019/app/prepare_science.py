from pathlib import Path
import hashlib,json
from datetime import datetime
W=Path(__file__).resolve().parent
C=Path(r'C:\IALD\Central de Patentes')
S=W/'science'
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,b):
 p=Path(p);assert p.resolve().is_relative_to(W.resolve());p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  if p.read_bytes()==b:return
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
  tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b and b;tmp.replace(p)
 else:
  tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b and b;tmp.replace(p)
def write(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2).encode())
