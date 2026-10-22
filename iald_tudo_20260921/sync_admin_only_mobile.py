from pathlib import Path
from datetime import datetime
import hashlib,json,os
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD');M=ROOT/'iald-app'
W=Path(__file__).resolve().parent;stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
backup=M/('_backups_admin_only_'+stamp);backup.mkdir()
rows=[]
def replace(path,data):
    old=path.read_bytes()
    if data==old:return
    # Backups stay outside packaged www/public directories.
    name=str(path.relative_to(ROOT)).replace('\\','__').replace('/','__')
    with (backup/name).open('xb')as f:f.write(old)
    tmp=path.with_name(path.name+'.tmp_'+stamp)
    with tmp.open('xb')as f:f.write(data)
    assert tmp.read_bytes()==data and path.read_bytes()==old
    os.replace(tmp,path)
    assert path.read_bytes()==data
    rows.append({'path':str(path),'sha256':hashlib.sha256(data).hexdigest()})

# Compatibility for cached web clients; never render administrative data.
stub=b"export function renderDeadlines() {\n  document.getElementById('iald-operational-deadlines')?.remove();\n}\n"
replace(ROOT/'app/operational_deadlines.js',stub)
for name in ('iald.js','operational_deadlines.js'):
    replace(M/'www'/name,(ROOT/'app'/name).read_bytes())
p=M/'ios/App/App.xcodeproj/project.pbxproj';data=p.read_bytes()
assert data.count(b'CURRENT_PROJECT_VERSION = 19;')==2
replace(p,data.replace(b'CURRENT_PROJECT_VERSION = 19;',b'CURRENT_PROJECT_VERSION = 20;'))
p=M/'android/app/build.gradle';data=p.read_bytes();assert data.count(b'versionCode 18')==1
replace(p,data.replace(b'versionCode 18',b'versionCode 19'))
out=W/('admin_only_mobile_sync_'+stamp+'.json')
with out.open('x',encoding='utf8')as f:json.dump(rows,f,indent=2)
print(out)
