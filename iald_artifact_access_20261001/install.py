from pathlib import Path
from datetime import datetime
import hashlib,json,os,sqlite3
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=json.loads((W/'checks.json').read_bytes());assert checks['passed']
base=json.loads((W/'baseline.json').read_bytes())
client=json.loads((W/'client/build_manifest.json').read_bytes())
base['app/iald.js']=client['source_sha256']
pending=[(W/'stage'/n,ROOT/n,base[n]) for n in base if n!='app/iald.js']
pending.append((W/'client/iald.js',ROOT/'app/iald.js',base['app/iald.js']))
for source,dest,expected in pending:
    assert sha(source.read_bytes())==checks['files'][str(source.relative_to(W))],source.name+' changed after tests'
    assert (sha(dest.read_bytes()) if dest.exists() else None)==expected,'Concurrent change: '+str(dest)
for path in ROOT.glob('*.reservas.sqlite3'):
    db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    try:assert db.execute("SELECT count(*) FROM calls WHERE status='reserved'").fetchone()[0]==0,'Active provider request'
    finally:db.close()
p=ROOT/'.iald_runtime/chat_jobs/jobs.sqlite3'
if p.exists():
    db=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)
    try:assert db.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]==0,'Active chat generation'
    finally:db.close()
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');result=[]
for source,dest,expected in pending:
    raw=source.read_bytes();backup=None
    if dest.exists():
        before=dest.read_bytes();assert sha(before)==expected
        backup=dest.with_name(dest.name+'.bak_'+stamp);backup.write_bytes(before);assert backup.read_bytes()==before
    tmp=dest.with_name(dest.name+'.tmp_'+stamp);tmp.write_bytes(raw)
    assert tmp.read_bytes()==raw and tmp.stat().st_size>0
    os.replace(tmp,dest);assert dest.read_bytes()==raw
    result.append({'path':str(dest),'sha256':sha(raw),'backup':str(backup) if backup else None})
(W/'installed.json').write_text(json.dumps({'files':result,'at':stamp},indent=2),encoding='utf-8')
print(json.dumps({'installed_files':len(result),'needs_web_restart':True}))
