from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import zipfile
import requests

WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
APP=ROOT/'iald-app'
OLD=WORK.parent/'iald_openai_motor_20260914'
SDK=Path(r'C:\Users\rotol\AppData\Local\Android\Sdk\build-tools\36.1.0')
JDK=Path(r'C:\Program Files\Android\Android Studio1\jbr')
os.environ['JAVA_HOME']=str(JDK)
os.environ['PATH']=str(JDK/'bin')+os.pathsep+os.environ['PATH']
receipt=WORK/'android16_verification.json'
assert not receipt.exists()
apk=APP/'android/app/build/outputs/apk/release/app-release.apk'
aab=APP/'android/app/build/outputs/bundle/release/app-release.aab'
def cert(path):
    output=subprocess.check_output([str(SDK/'apksigner.bat'),'verify','--print-certs',str(path)])
    return re.search(rb'certificate SHA-256 digest: ([0-9a-f]+)',output).group(1).decode()
signature=cert(apk)
old_signatures={str(p):cert(p) for p in [OLD/'artifacts/IALD-4.1-14.apk',OLD/'artifacts/IALD-4.1-15.apk']}
assert all(v==signature for v in old_signatures.values())
result=subprocess.run([str(JDK/'bin/jarsigner.exe'),'-verify',str(aab)],check=True,capture_output=True)
assert b'jar verified.' in result.stdout
badging=subprocess.check_output([str(SDK/'aapt.exe'),'dump','badging',str(apk)])
assert b"name='br.ia.IALD' versionCode='16' versionName='4.1'" in badging
files=[]
(WORK/'artifacts').mkdir(exist_ok=True)
for path,prefix,ext in [(apk,'assets/public/','apk'),(aab,'base/assets/public/','aab')]:
    with zipfile.ZipFile(path) as package:
        assert not any('.bak_' in n or '.tmp_' in n or 'keystore.properties' in n for n in package.namelist())
        for name in ['iald.js','iald.css','index.html','kernel_prompt.js','kernel_prompt_loja.js']:
            assert package.read(prefix+name)==(APP/'www'/name).read_bytes(),name
    data=path.read_bytes()
    dest=WORK/('artifacts/IALD-4.1-16.'+ext)
    with dest.open('xb') as f:f.write(data)
    assert dest.read_bytes()==data
    files.append({'path':str(dest),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
report={'at':datetime.now().astimezone().isoformat(),'status':'VERIFIED_NOT_YET_DELIVERED',
        'build':16,'version':'4.1','package':'br.ia.IALD','certificate_sha256':signature,
        'previous_certificates':old_signatures,'aab_signature_verified':True,
        'embedded_assets_match_www':True,'no_backups_in_packages':True,'files':files}
with receipt.open('xb') as f:f.write(json.dumps(report,indent=2).encode())
print(json.dumps(report))
