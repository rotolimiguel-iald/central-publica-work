"""CAS installation of the reviewed server-only default; no provider calls."""
from pathlib import Path
from datetime import datetime
import hashlib,json,os,sqlite3,sys

W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def quiet():
    jobs=R/'.iald_runtime/chat_jobs/jobs.sqlite3'
    if not jobs.is_file():raise RuntimeError('Cannot verify active chat jobs')
    with sqlite3.connect(jobs.as_uri()+'?mode=ro',uri=True) as db:
        active=db.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]
    if active:raise RuntimeError('Active chat jobs; installation postponed')
    holds=[]
    for p in list(R.glob('*.reservas.sqlite3'))+[R/'.iald_runtime/app_evaluation/public_spend.sqlite3']:
        if not p.is_file():continue
        with sqlite3.connect(p.as_uri()+'?mode=ro',uri=True) as db:
            n=db.execute("SELECT count(*) FROM calls WHERE status='reserved'").fetchone()[0]
        holds.append(dict(file=p.name,active=n))
        if n:raise RuntimeError('Active model reservation; installation postponed')
    return dict(active_jobs=active,reservations=holds)

def atomic(path,raw):
    temp=path.with_name(path.name+'.tmp_jev_'+str(os.getpid()))
    with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(raw):raise RuntimeError('Incomplete temporary file')
    os.replace(temp,path)
    if path.read_bytes()!=raw:raise RuntimeError('Post-write mismatch')

if len(sys.argv)>1 and sys.argv[1]=='quiet':
    print(json.dumps(quiet()));sys.exit(0)

baseline=json.loads((W/'baseline.json').read_bytes())
checks=json.loads((W/'checks.json').read_bytes())
assert checks['passed'] and checks['tests_run']>=222
old,new={},{}
for name,digest in baseline.items():
    old[name]=(R/name).read_bytes();new[name]=(W/'stage'/name).read_bytes()
    assert sha(old[name])==digest,('Concurrent source change',name)
    assert sha(new[name])==checks['files'][name],('Unverified stage change',name)
    compile(new[name],name,'exec')
activity=quiet()
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
users_sha=sha((R/'iald_users.json').read_bytes())
written=[];backups={}
try:
    for name,raw in old.items():
        p=R/name;backup=p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(raw)
        assert backup.read_bytes()==raw
        backups[name]=str(backup)
    for name,raw in new.items():
        p=R/name
        assert p.read_bytes()==old[name],('Concurrent source change',name)
        atomic(p,raw);written.append(name)
except BaseException:
    for name in reversed(written):
        p=R/name
        if p.read_bytes()==new[name]:atomic(p,old[name])
    raise
record=dict(installed_at=datetime.now().astimezone().isoformat(),files={n:sha(b) for n,b in new.items()},
    backups=backups,activity=activity,users_sha_before=users_sha,
    users_untouched=sha((R/'iald_users.json').read_bytes())==users_sha,
    tests=checks['tests_run'],skipped=checks['skipped'],provider_calls=0,
    client_changes=False,policy='jev_default_20261001')
atomic(W/'deployment.json',json.dumps(record,ensure_ascii=False,indent=2).encode())
print(json.dumps({k:record[k] for k in ('installed_at','users_untouched','tests','skipped','client_changes','policy')}))
