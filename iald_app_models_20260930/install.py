"""Reviewed app/provider patch only; compare-and-swap and byte backups."""
from pathlib import Path
from datetime import datetime
import ast
import hashlib
import json
import subprocess

W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
MOBILE=ROOT/'iald-app'
GIT=r'C:\Program Files\Git\cmd\git.exe'
def sha(raw):return hashlib.sha256(raw).hexdigest() if raw is not None else None
def create(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(data)
    assert path.read_bytes()==data

hashes=json.loads((W/'original_hashes.json').read_text(encoding='utf-8-sig'))
assert not subprocess.check_output([GIT,'-C',str(MOBILE),'status','--porcelain']).strip(),'Concurrent mobile edits'
changes={}
for name,digest in hashes.items():
    p=ROOT/name;old=p.read_bytes();new=(W/'stage'/name).read_bytes()
    assert sha(old).upper()==digest,name
    if p.suffix=='.py':ast.parse(new.decode('utf-8'))
    changes[p]=(old,new)
for name in ('iald_app_providers.py','iald_app_evaluation_page.py'):
    p=ROOT/name;assert not p.exists(),p
    new=(W/'stage'/name).read_bytes();ast.parse(new.decode('utf-8'));changes[p]=(None,new)
for name in ('iald.js','iald.css'):
    p=MOBILE/'www'/name;old=p.read_bytes();new=(W/'stage/app'/name).read_bytes()
    assert old==(ROOT/'app'/name).read_bytes(),p
    changes[p]=(old,new)
for name,old,new,n in [('ios/App/App.xcodeproj/project.pbxproj',b'CURRENT_PROJECT_VERSION = 23;',b'CURRENT_PROJECT_VERSION = 25;',2),
                       ('android/app/build.gradle',b'versionCode 21',b'versionCode 22',1)]:
    p=MOBILE/name;before=p.read_bytes();assert before.count(old)==n,name
    changes[p]=(before,before.replace(old,new))
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
for p,(old,new) in changes.items():
    assert new and (not p.exists() if old is None else p.read_bytes()==old),p
    if old is not None:create(p.with_name(p.name+'.bak_'+stamp),old)
for p,(old,new) in changes.items():
    assert (not p.exists() if old is None else p.read_bytes()==old),p
    temp=p.with_name(p.name+'.tmp_'+stamp);create(temp,new);temp.replace(p)
    assert p.read_bytes()==new
record={str(p):{'before':sha(old),'after':sha(new),'bytes':len(new)} for p,(old,new) in changes.items()}
create(W/('installed_'+stamp+'.json'),json.dumps(record,indent=2).encode())
print(json.dumps({'installed_files':len(changes),'receipt':'installed_'+stamp+'.json'}))
