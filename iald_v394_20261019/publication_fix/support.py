"""Local staging writes only; byte backups and atomic replacement."""
from pathlib import Path
from datetime import datetime
import hashlib,json
P=Path(__file__).resolve().parent
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def save(path,raw):
    path=Path(path).resolve();assert path.is_relative_to(P) and raw
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        old=path.read_bytes()
        if old==raw:return
        backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:stream.write(old)
        assert backup.read_bytes()==old
    temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as stream:stream.write(raw)
    assert temp.read_bytes()==raw;temp.replace(path)
def write(path,value):save(path,json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False).encode())
def pin(path):
    path=Path(path);raw=path.read_bytes();return {'path':str(path),'sha256':sha(raw),'bytes':len(raw)}
