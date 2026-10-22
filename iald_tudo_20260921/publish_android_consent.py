from pathlib import Path
import zipfile,hashlib,json
from datetime import datetime
root=Path(r'C:\IALD\projetos_pyhton\IALD')
apk=root/'iald-app/android/app/build/outputs/apk/release/app-release.apk'
aab=root/'iald-app/android/app/build/outputs/bundle/release/app-release.aab'
with zipfile.ZipFile(apk) as z:
 for name in ('index.html','iald.css','iald.js'):
  assert z.read('assets/public/'+name)==(root/'app'/name).read_bytes(),name
dest=root/'downloads/IALD-4.1-18.apk'
data=apk.read_bytes()
with dest.open('xb') as out:out.write(data)
assert dest.read_bytes()==data
receipt={'android_version':18,'assets_match':True,'artifacts':[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in (apk,aab,dest)],'google_play':'NOT_UPLOADED','physical_test':'PENDING'}
out=Path(__file__).parent/('android18_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
out.write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(out)
