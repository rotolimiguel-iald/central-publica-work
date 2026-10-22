"""Publish only the two reviewed mobile JS resources to the existing private repo."""
import json,subprocess
from pathlib import Path
from urllib.parse import urlsplit
from mission_io import WORK,pin,save,check

check('D')
root=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
out=WORK/'live_validation/MOBILE_SOURCE_PUBLISH_R1.json'
if out.exists():raise SystemExit('Existing publication receipt; inspect before retry')
def git(*args):
    p=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,encoding='utf-8')
    if p.returncode:raise RuntimeError('Git '+args[0]+' failed; no credential-bearing output retained')
    return p.stdout.strip()
baseline=json.loads((WORK/'live_validation/MOBILE_GIT_BASELINE_R1.json').read_bytes())
assert git('rev-parse','HEAD')==baseline['head']
assert git('branch','--show-current')=='codex/mobile-release'
assert git('diff','--cached','--name-only')==''
names=['ios/App/App/public/iald.js','www/iald.js']
assert set(git('diff','--name-only').splitlines())==set(names)
assert set(git('ls-files','--others','--exclude-standard').splitlines())==set()
url=git('remote','get-url','origin')
assert url in ('https://github.com/rotolimiguel-iald/iald-app',
    'https://github.com/rotolimiguel-iald/iald-app.git','git@github.com:rotolimiguel-iald/iald-app.git')
expected=pin(WORK/'staging/app/app/iald.js')['sha256']
for name in names:assert pin(root/name)['sha256']==expected
save(out.with_name('MOBILE_SOURCE_PUBLISH_INTENT_R1.json'),{'remote_repository':'github.com/rotolimiguel-iald/iald-app',
    'branch':'codex/mobile-release','baseline':baseline['head'],'files':[pin(root/n) for n in names],
    'review':pin(WORK/'deployment_r2/REVIEW_R1.json'),'purpose':'Shared activity review control; existing Xcode Cloud pipeline.'})
result={'status':'STARTED','prior_head':baseline['head'],'files':names,'new_store_build_verified':False}
try:
    git('add','--',*names)
    assert set(git('diff','--cached','--name-only').splitlines())==set(names)
    git('commit','-m','Integrate activity memory review in mobile conversation')
    result['commit']=git('rev-parse','HEAD')
    save(out.with_name('MOBILE_SOURCE_COMMIT_R1.json'),dict(result,status='COMMITTED'))
    git('push','origin','HEAD:codex/mobile-release')
    remote=git('ls-remote','origin','refs/heads/codex/mobile-release').split()[0]
    assert remote==result['commit']
    result.update(status='PUSHED_AND_VERIFIED',remote_head=remote,local_clean=git('status','--porcelain')=='')
except Exception as exc:
    result.update(status='STOPPED_REQUIRES_INSPECTION',error_type=type(exc).__name__,error=str(exc))
    raise
finally:save(out,result)
print(json.dumps(result))
