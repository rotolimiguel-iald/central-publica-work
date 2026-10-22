from pathlib import Path
from datetime import datetime
import os, hashlib, json
root=Path(r'C:\IALD\projetos_pyhton\IALD')
mobile=root/'iald-app'
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
backup=mobile/('_backups_consent_'+stamp)
backup.mkdir()
rows=[]
def replace(p,data):
 old=p.read_bytes()
 (backup/p.name).write_bytes(old)
 tmp=p.with_name(p.name+'.tmp_'+stamp)
 tmp.write_bytes(data)
 assert tmp.read_bytes()==data and p.read_bytes()==old
 os.replace(tmp,p)
 rows.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest()})
for name in ('index.html','iald.css','iald.js'):
 data=(root/'app'/name).read_bytes()
 replace(mobile/'www'/name,data)
p=mobile/'ios/App/App.xcodeproj/project.pbxproj'
raw=p.read_bytes();assert raw.count(b'CURRENT_PROJECT_VERSION = 18;')==2
replace(p,raw.replace(b'CURRENT_PROJECT_VERSION = 18;',b'CURRENT_PROJECT_VERSION = 19;'))
p=mobile/'android/app/build.gradle'
raw=p.read_bytes();assert raw.count(b'versionCode 17')==1
replace(p,raw.replace(b'versionCode 17',b'versionCode 18'))
out=Path(__file__).parent/('consent_release_'+stamp+'.json')
out.write_text(json.dumps(rows,indent=2),encoding='utf8')
print(out)
