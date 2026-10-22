from task import W,new
from pathlib import Path
import hashlib
R=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app');D=W/'native_stage';D.mkdir(exist_ok=True)
rows=[]
for rel,old,newbytes,count in [('ios/App/App.xcodeproj/project.pbxproj',b'CURRENT_PROJECT_VERSION = 35;',b'CURRENT_PROJECT_VERSION = 36;',2),('android/app/build.gradle',b'versionCode 30',b'versionCode 31',1)]:
    p=R/rel;b=p.read_bytes();assert b.count(old)==count
    a=b.replace(old,newbytes);out=D/p.name;out.open('xb').write(a)
    rows.append(dict(source=str(out),destination=str(p),baseline=hashlib.sha256(b).hexdigest(),sha256=hashlib.sha256(a).hexdigest()))
new('NATIVE_PLAN.json',dict(files=rows,ios='4.1(36)',android='4.1(31)'))
print('Native versions staged only')
