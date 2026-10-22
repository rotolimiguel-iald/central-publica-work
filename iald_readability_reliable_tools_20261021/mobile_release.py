"""Reviewed one-shot build and private mobile publication. Never reads signing credentials."""
from pathlib import Path
import sys,os,json,hashlib,subprocess,zipfile,re
from task import W,new,check
OLD=W.parent/'mimo_media_capacity_20261020/client_stage/android30_final19_label_R8'
sys.path.insert(0,str(OLD))
from run_android30_R1 import collect
D=W/'mobile_stage';R=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.open('xb').write(json.dumps(d,ensure_ascii=False,indent=2).encode())
def git(*args):
    p=subprocess.run(['git','-C',str(R),*args],capture_output=True)
    if p.returncode:raise RuntimeError('Git refused operation '+args[0])
    return p.stdout
def gs(*args):return git(*args).decode().strip()
def checked():
    review=json.loads((W/'validation/mobile_review.json').read_bytes());assert review['status']=='PASS' and review['runner_sha256']==sha(Path(__file__))
    assert review['init_sha256']==sha(W/'android31.init.gradle')
    check('deploy');plan=json.loads((W/'install_plan.json').read_bytes())
    for f in plan['files']:assert sha(Path(f['destination']))==f['sha256']
    for f in json.loads((W/'SCIENCE_BASELINE.json').read_bytes())['files']:assert sha(Path(f['path']))==f['sha256']
    return plan
def build():
    checked();D.mkdir(exist_ok=True);a=D/'build31';a.mkdir(exist_ok=False)
    p=json.loads((OLD/'ANDROID30_BUILD_PLAN_R1.json').read_bytes());env=os.environ.copy()
    for n in ['DEBUG','JAVA_OPTS','GRADLE_OPTS','JAVA_TOOL_OPTIONS','JDK_JAVA_OPTIONS','_JAVA_OPTIONS']:env.pop(n,None)
    env.update(JAVA_HOME=str(Path(p['tools']['java']).parent.parent),ANDROID_HOME=p['android_sdk'],ANDROID_SDK_ROOT=p['android_sdk'])
    cmd=[p['wrapper'],'--offline','--no-daemon','--console=plain','--no-configuration-cache','-Dfile.encoding=UTF-8','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8','-Diald.mobile.output='+str(a),':app:bundleRelease',':app:assembleRelease']
    cmd[5:5]=['--gradle-user-home',p['gradle_user_home'],'--project-cache-dir',str(a/'project-cache'),'--init-script',str(W/'android31.init.gradle')]
    save(a/'INTENT.json',dict(no_repeat=True,versionCode=31))
    b=collect(cmd,cwd=p['android_project'],env=env,label='gradle',attempt=a)
    assert b['exit_code']==0 and b['filtered_lines']==0
    build_log=Path(b['log']['path']).read_text(encoding='utf-8');assert 'IALD_MOBILE_VERSION 4.1(31)' in build_log and 'IALD_MOBILE_OUTPUTS_ISOLATED' in build_log
    apk=a/'projects/app/outputs/apk/release/app-release.apk';aab=a/'projects/app/outputs/bundle/release/app-release.aab'
    assert apk.is_file() and aab.is_file()
    resources={'iald.js':sha(W/'client_stage/R2/iald.js'),'iald.css':sha(W/'client_stage/R2/iald.css')}
    for archive,prefix in [(apk,'assets/public/'),(aab,'base/assets/public/')]:
        with zipfile.ZipFile(archive) as z:
            names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
            for n,h in resources.items():assert hashlib.sha256(z.read(prefix+n)).hexdigest()==h
            assert not any(re.search(r'(?i)(keystore\.properties|(?:^|/)\.env(?:\.|$)|\.(jks|keystore|p12|p8|pem|key)$)',n) for n in names)
    tools=p['tools'];commands={'badging':[tools['aapt'],'dump','badging',str(apk)],'apk_signature':[tools['java'],'-jar',tools['apksigner_jar'],'verify','--verbose','--print-certs',str(apk)],'baseline_signature':[tools['java'],'-jar',tools['apksigner_jar'],'verify','--print-certs',p['baseline_apk']['path']],'aab_signature':[tools['jarsigner'],'-J-Duser.language=en','-J-Duser.country=US','-verify',str(aab)]}
    commands['aab_certificate']=[tools['keytool'],'-J-Duser.language=en','-J-Duser.country=US','-printcert','-jarfile',str(aab)]
    commands['aab_signature'].insert(-1,'-verbose')
    logs={}
    for n,c in commands.items():
        out=collect(c,cwd=a,env=env,label=n,attempt=a);assert out['exit_code']==0 and not out['filtered_lines'];logs[n]=Path(out['log']['path']).read_text(encoding='utf-8')
    assert "versionCode='31'" in logs['badging'] and "versionName='4.1'" in logs['badging']
    jarlog=logs['aab_signature'];assert 'jar verified.' in jarlog.lower()
    assert 'unsigned entries' not in jarlog.lower() and 'jar is unsigned' not in jarlog.lower()
    assert len(re.findall(r'^\s*s[mki? ]*\s+\d+\s+',jarlog,re.M))>0
    cert=lambda t:re.findall(r'certificate SHA-256 digest:\s*([0-9a-fA-F]+)',t)
    assert cert(logs['apk_signature']) and cert(logs['apk_signature'])==cert(logs['baseline_signature'])
    aab_cert=re.findall(r'SHA256:\s*([0-9A-Fa-f:]+)',logs['aab_certificate']);assert len(aab_cert)==1
    assert aab_cert[0].replace(':','').lower()==cert(logs['apk_signature'])[0].lower()
    save(D/'AUDIT.json',dict(status='PASS',versionCode=31,apk=str(apk),aab=str(aab),apk_sha256=sha(apk),aab_sha256=sha(aab),resources=resources,signer_matches_previous=True,build=b))
def commit():
    checked();assert not (D/'COMMIT_INTENT.json').exists();assert gs('branch','--show-current')=='codex/mobile-release'
    allowed=['www/iald.js','www/iald.css','ios/App/App/public/iald.js','ios/App/App/public/iald.css','ios/App/App.xcodeproj/project.pbxproj','android/app/build.gradle']
    urls={'https://github.com/rotolimiguel-iald/iald-app.git','git@github.com:rotolimiguel-iald/iald-app.git'}
    assert gs('remote','get-url','origin') in urls and gs('remote','get-url','--push','origin') in urls
    assert not git('diff','--cached','--name-only').strip()
    assert set(gs('diff','HEAD','--name-only').splitlines())==set(allowed)
    base=gs('rev-parse','HEAD');save(D/'COMMIT_INTENT.json',dict(baseline=base,allowed=allowed,no_repeat=True))
    for n in allowed:
        mode=gs('ls-files','--stage','--',n).split()[0];assert mode=='100644'
        oid=gs('hash-object','-w','--no-filters','--',n);git('update-index','--cacheinfo',mode,oid,n)
        assert hashlib.sha256(git('show',':'+n)).hexdigest()==sha(R/n)
    assert set(gs('diff','--cached','--name-only').splitlines())==set(allowed)
    git('commit','-m','Refine chat reading and disable unvalidated media uploads')
    head=gs('rev-parse','HEAD');assert gs('rev-parse','HEAD^')==base
    save(D/'COMMIT.json',dict(status='COMMITTED_NOT_PUSHED',baseline=base,commit=head,files={n:sha(R/n) for n in allowed}))
def push():
    checked();d=json.loads((D/'COMMIT.json').read_bytes());assert not (D/'PUSH_INTENT.json').exists()
    urls={'https://github.com/rotolimiguel-iald/iald-app.git','git@github.com:rotolimiguel-iald/iald-app.git'}
    assert gs('remote','get-url','origin') in urls and gs('remote','get-url','--push','origin') in urls
    assert gs('rev-parse','HEAD')==d['commit'] and not git('status','--porcelain').strip()
    remote=gs('ls-remote','--heads','origin','refs/heads/codex/mobile-release').split();assert remote[0]==d['baseline']
    save(D/'PUSH_INTENT.json',dict(commit=d['commit'],no_repeat=True))
    git('push','--porcelain','origin','HEAD:refs/heads/codex/mobile-release')
    assert gs('ls-remote','--heads','origin','refs/heads/codex/mobile-release').split()[0]==d['commit']
    save(D/'PUSH.json',dict(status='PUSHED_VERIFIED',commit=d['commit'],ios_build='4.1(36)',cloud_pending=True))
if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ['build','commit','push']:raise SystemExit('Explicit phase required')
    dict(build=build,commit=commit,push=push)[sys.argv[1]]()
