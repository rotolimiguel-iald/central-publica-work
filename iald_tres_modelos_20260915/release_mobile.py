from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import requests

WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
APP=ROOT/'iald-app'
audit=json.loads((WORK/'mobile16_audit.json').read_bytes())
assert json.loads((WORK/'suite_gate.json').read_bytes())['passed'] is True
publication=WORK/'mobile16_publication.json'
assert not publication.exists()

def git(*args):
    return subprocess.check_output(['git',*args],cwd=APP,stderr=subprocess.PIPE)

repo=json.loads(subprocess.check_output([r'C:\Users\rotol\AppData\Local\Programs\gh\bin\gh.exe',
    'repo','view','rotolimiguel-iald/iald-app','--json','isPrivate,nameWithOwner']))
assert repo=={'isPrivate':True,'nameWithOwner':'rotolimiguel-iald/iald-app'}
assert git('branch','--show-current').decode().strip()=='codex/mobile-release'
assert git('remote','get-url','origin').decode().strip()=='https://github.com/rotolimiguel-iald/iald-app.git'
git('fetch','origin','codex/mobile-release')
assert int(git('rev-list','--count','HEAD..origin/codex/mobile-release'))==0,'Remote advanced'
for name,item in audit['files'].items():
    assert hashlib.sha256((APP/name).read_bytes()).hexdigest()==item['sha256'],'Concurrent edit: '+name
paths=WORK/'mobile16_pathspec.bin'
with paths.open('xb') as f:f.write(b'\0'.join(n.encode() for n in audit['files'])+b'\0')
git('add','--pathspec-from-file='+str(paths),'--pathspec-file-nul')
staged=set(filter(None,git('diff','--cached','--name-only','-z').decode().split('\0')))
assert staged and staged<=set(audit['files']),'Unexpected staged path'
git('diff','--cached','--check')
git('commit','-m','Update build 16 with model selection, response labels and usage display')
commit=git('rev-parse','HEAD').decode().strip()
git('push','origin','HEAD:codex/mobile-release')
remote=git('ls-remote','origin','refs/heads/codex/mobile-release').decode().split()[0]
assert remote==commit
report={'at':datetime.now().astimezone().isoformat(),'status':'PUSH_VERIFIED',
        'repository':'https://github.com/rotolimiguel-iald/iald-app','private':True,
        'branch':'codex/mobile-release','commit':commit,'changed_files':sorted(staged),
        'audited_files':len(audit['files']),'xcode_cloud':'AWAITING_VERIFICATION'}
with publication.open('xb') as f:f.write(json.dumps(report,indent=2).encode())

verification=json.loads((WORK/'android16_verification.json').read_bytes())
apk=next(f for f in verification['files'] if f['path'].endswith('.apk'))
data=Path(apk['path']).read_bytes()
assert hashlib.sha256(data).hexdigest()==apk['sha256'] and len(data)==apk['bytes']
target=ROOT/'downloads/IALD-4.1-16.apk'
assert not target.exists(),'Existing published APK must be reviewed first'
temporary=target.with_suffix('.apk.tmp_release')
with temporary.open('xb') as f:f.write(data)
assert temporary.read_bytes()==data
temporary.replace(target)
assert target.read_bytes()==data
url='https://demo.iald.ia.br/downloads/IALD-4.1-16.apk'
with requests.get(url,allow_redirects=False,timeout=20,stream=True) as response:
    status,location=response.status_code,response.headers.get('Location','')
assert status==302 and 'login' in location
delivery={'at':datetime.now().astimezone().isoformat(),'status':'DELIVERED_AUTHENTICATED',
          'url':url,'apk':apk,'anonymous_http_status':status,'installation_on_device':'NOT_VERIFIED',
          'google_play':'REGISTRATION_PENDING_DUNS'}
with (WORK/'android16_delivery.json').open('xb') as f:f.write(json.dumps(delivery,indent=2).encode())
print(json.dumps({'commit':commit,'files':len(staged),'apk_url':url,'xcode_cloud':'AWAITING_VERIFICATION'}))
