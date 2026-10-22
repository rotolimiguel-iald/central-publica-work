from pathlib import Path
from datetime import datetime
import hashlib,json,os,subprocess
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
manifest=json.loads((W/'client/build_manifest.json').read_bytes())
raw=(W/'client/iald.js').read_bytes();assert hashlib.sha256(raw).hexdigest()==manifest['output_sha256']
assert not subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain']).strip(),'Concurrent mobile changes'
js=ROOT/'www/iald.js';assert hashlib.sha256(js.read_bytes()).hexdigest()==manifest['source_sha256']
pbx=ROOT/'ios/App/App.xcodeproj/project.pbxproj';gradle=ROOT/'android/app/build.gradle'
pbxraw=pbx.read_bytes();gradleraw=gradle.read_bytes()
assert pbxraw.count(b'CURRENT_PROJECT_VERSION = 26;')==2
assert gradleraw.count(b'versionCode 23')==1
pending=[(js,raw),(pbx,pbxraw.replace(b'CURRENT_PROJECT_VERSION = 26;',b'CURRENT_PROJECT_VERSION = 27;')),(gradle,gradleraw.replace(b'versionCode 23',b'versionCode 24'))]
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
rows=[]
for p,new in pending:
    before=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(before);assert bak.read_bytes()==before
    tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(new);assert tmp.read_bytes()==new
    assert p.read_bytes()==before
    os.replace(tmp,p);assert p.read_bytes()==new
    rows.append({'path':str(p),'backup':str(bak),'sha256':hashlib.sha256(new).hexdigest()})
(W/'mobile_sync.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('Mobile source updated: iOS 4.1 (27), Android 4.1 (24)')
