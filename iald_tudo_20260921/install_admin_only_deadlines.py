from pathlib import Path
from datetime import datetime
import hashlib,json,os
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
W=Path(__file__).resolve().parent
STAGE=W/'admin_only_deadlines_20260922_150455_620479'
rows=json.loads((STAGE/'receipt.json').read_text())
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
pending=[]
for row in rows:
    p=ROOT/row['relative'];raw=p.read_bytes();new=(STAGE/row['relative']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['old_sha256'],'Source changed; rebuild patch'
    assert hashlib.sha256(new).hexdigest()==row['new_sha256']
    pending.append((p,raw,new))
for p,raw,new in pending:
    backup=p.with_name(p.name+'.bak_'+stamp)
    with backup.open('xb')as f:f.write(raw)
    assert backup.read_bytes()==raw
    tmp=p.with_name(p.name+'.tmp_'+stamp)
    with tmp.open('xb')as f:f.write(new)
    assert tmp.read_bytes()==new and p.read_bytes()==raw
    os.replace(tmp,p)
    assert p.read_bytes()==new
out=W/('admin_only_installed_'+stamp+'.json')
with out.open('x',encoding='utf8')as f:json.dump(rows,f,indent=2)
print(out)
