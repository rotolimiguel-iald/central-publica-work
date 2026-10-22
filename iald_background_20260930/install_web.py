"""Publish tested chat continuity with byte backups and concurrent-edit protection."""
from datetime import datetime
from pathlib import Path
import hashlib,json,os,shutil,sqlite3
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
checks=json.loads((W/'checks.json').read_bytes())
assert checks['passed'],'Tests must pass before deployment'
baseline=json.loads((W/'baseline_server.json').read_bytes())
client=json.loads((W/'client/build_manifest.json').read_bytes())
baseline['app/iald.js']=client['source_sha256']
pending=[]
for name in ('iald_chat_jobs.py','iald_chat_push.py','iald_notification_runtime.py','iald_web_server.py'):
    source=W/'server'/name;pending.append((source,ROOT/name,baseline.get(name)))
pending.append((W/'client/iald.js',ROOT/'app/iald.js',baseline['app/iald.js']))
for source,destination,expected in pending:
    raw=source.read_bytes()
    assert sha(raw)==checks['files'][str(source.relative_to(W))],'Changed after tests: '+source.name
    assert (sha(destination.read_bytes()) if destination.exists() else None)==expected,'Concurrent change: '+str(destination)
for path in ROOT.glob('*.reservas.sqlite3'):
    db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    try:assert db.execute("SELECT count(*) FROM calls WHERE status='reserved'").fetchone()[0]==0,'Active provider call'
    finally:db.close()
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');records=[]
for source,destination,expected in pending:
    raw=source.read_bytes();backup=None
    if destination.exists():
        before=destination.read_bytes();assert sha(before)==expected
        backup=destination.with_name(destination.name+'.bak_'+stamp)
        backup.write_bytes(before);assert backup.read_bytes()==before
    temp=destination.with_name(destination.name+'.tmp_'+stamp);temp.write_bytes(raw)
    assert temp.read_bytes()==raw and temp.stat().st_size>0
    os.replace(temp,destination);assert destination.read_bytes()==raw
    records.append({'path':str(destination),'sha256':sha(raw),'backup':str(backup) if backup else None})
dependency=ROOT/'.iald_runtime/push_dependencies'
assert not dependency.exists(),'Do not overwrite a dependency directory'
shutil.copytree(W/'python-dependencies',dependency)
for path in (W/'python-dependencies').rglob('*'):
    if path.is_file():assert (dependency/path.relative_to(W/'python-dependencies')).read_bytes()==path.read_bytes()
(W/'installed_web.json').write_text(json.dumps({'files':records,'at':stamp,'push_enabled':False},indent=2),encoding='utf-8')
print(json.dumps({'installed_files':len(records),'push_enabled':False,'requires_web_restart':True}))
