"""Install only reviewed app modules, with CAS and byte backups; no user DB mutation."""
from pathlib import Path
from datetime import datetime
import ast,hashlib,json,os,sqlite3
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def create(p,raw):
    with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert p.read_bytes()==raw

def main():
    pins=json.loads((W/'pins.json').read_bytes());old={};new={}
    for name,pin in pins.items():
        p=R/name;old[name]=p.read_bytes() if p.exists() else None
        assert (sha(old[name]) if old[name] is not None else None)==pin,name+' changed concurrently'
        new[name]=(W/'stage'/name).read_bytes();ast.parse(new[name])
    db=sqlite3.connect('file:'+str(R/'.iald_runtime/app_evaluation/metrics.sqlite3')+'?mode=ro',uri=True)
    active=[json.loads(r[0])['id'] for r in db.execute('SELECT data FROM turns') if json.loads(r[0]).get('status')=='started']
    db.close();assert not active, 'Active app generation; wait before deployment'
    report={'at':datetime.now().astimezone().isoformat(),'files':{},'scientific_memory_changed':False,
        'user_records_changed':False,'mobile_assets_changed':False,'status':'INSTALLED_RESTART_PENDING'}
    temps={}
    for name in pins:
        path=R/name;backup=None
        if old[name] is not None:
            backup=Path(str(path)+'.bak_'+stamp);create(backup,old[name])
        tmp=Path(str(path)+'.tmp_'+stamp);create(tmp,new[name]);temps[name]=tmp
        report['files'][name]={'sha256':sha(new[name]),'backup':str(backup) if backup else None}
    for name in pins:
        path=R/name
        assert (path.read_bytes() if path.exists() else None)==old[name],name+' changed concurrently'
    # Server module last, so reloader can never see imports before modules exist.
    for name in sorted(pins,key=lambda n:n=='iald_web_server.py'):
        os.replace(temps[name],R/name);assert (R/name).read_bytes()==new[name]
    create(W/'installed.json',json.dumps(report,indent=2).encode())
    print(json.dumps({'status':report['status'],'files':list(pins)}))
if __name__=='__main__':main()
