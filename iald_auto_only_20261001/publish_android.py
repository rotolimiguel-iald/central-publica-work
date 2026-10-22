from pathlib import Path
from datetime import datetime
import json,hashlib,os
W=Path(__file__).resolve().parent
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def save_safely(path,raw):
 old=path.read_bytes() if path.exists() else None
 if old is not None:
  backup=path.with_name(path.name+'.bak_'+stamp)
  with backup.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
  assert backup.read_bytes()==old
 temp=path.with_name(path.name+'.tmp_editor_'+str(os.getpid()))
 with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert temp.read_bytes()==raw and len(raw)>0
 assert (path.read_bytes() if path.exists() else None)==old
 os.replace(temp,path);assert path.read_bytes()==raw

d=json.loads((W/'android_verified.json').read_bytes())
assert d['passed'] and all(d['checks'].values()) and d['versionCode']==26
source=Path(d['apk']['path']);raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==d['apk']['sha256']
dest=Path(r'C:\IALD\projetos_pyhton\IALD\downloads\IALD-4.1-26.apk')
# Existing different release would require investigation, never overwrite it.
assert not dest.exists() or dest.read_bytes()==raw
save_safely(dest,raw)
receipt=dict(version='4.1',versionCode=26,signature_verified=True,embedded_client_matches_web=True,apk=dict(path=str(dest),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),aab={k:d['aab'][k] for k in ('path','bytes','sha256')},url='https://demo.iald.ia.br/downloads/'+dest.name,google_play='DUNS setup pending')
save_safely(W/'android_release.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
print(json.dumps({'published':str(dest),'bytes':len(raw),'existing_files_backed_up_if_present':True}))
