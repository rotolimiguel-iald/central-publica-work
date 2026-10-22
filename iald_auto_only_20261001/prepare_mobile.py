from pathlib import Path
import subprocess,hashlib,json,os,re
from datetime import datetime
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');N=R/'iald-app'
def git(*args):return subprocess.check_output(['git','-C',str(N),*args],text=True,encoding='utf-8').strip()
assert git('status','--porcelain')=='','Concurrent mobile changes'
assert git('branch','--show-current')=='codex/mobile-release'
assert git('remote','get-url','origin')=='https://github.com/rotolimiguel-iald/iald-app.git'
assert not (W/'mobile_prepared.json').exists()
ios='ios/App/App.xcodeproj/project.pbxproj';android='android/app/build.gradle'
old={name:(N/name).read_bytes() for name in ['www/iald.js',ios,android]}
assert re.findall(rb'CURRENT_PROJECT_VERSION = (\d+);',old[ios])==[b'28',b'28']
assert re.findall(rb'versionCode (\d+)',old[android])==[b'25']
new={'www/iald.js':(W/'stage/app/iald.js').read_bytes(),ios:old[ios].replace(b'CURRENT_PROJECT_VERSION = 28;',b'CURRENT_PROJECT_VERSION = 29;'),android:old[android].replace(b'versionCode 25',b'versionCode 26')}
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');backup=W/'backups'/('mobile_'+stamp);backup.mkdir(parents=True)
for name,raw in old.items():
 b=backup/(name.replace('/','__')+'.before');b.write_bytes(raw);assert b.read_bytes()==raw
for name,raw in new.items():
 assert (N/name).read_bytes()==old[name]
 tmp=backup/(name.replace('/','__')+'.candidate');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,N/name)
receipt={'ios':'4.1 (29)','android':'4.1 (26)','head_before':git('rev-parse','HEAD'),'files':{k:hashlib.sha256(v).hexdigest() for k,v in new.items()},'backups':str(backup)}
(W/'mobile_prepared.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(json.dumps(receipt))
