"""Build release 42 with the existing offline Gradle signing/audit procedure."""
from pathlib import Path
import hashlib, os, re, sys, zipfile, json
from build_log import collect
from prepare_mobile import HERE, report, require
from release_controls import release_installed, remote_preflight, D

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,data): report(path,data)
def checked(): return release_installed()
def resource_pins(plan): return plan['assets']

def build():
    checked();D.mkdir(exist_ok=True);a=D/'build42';a.mkdir(exist_ok=False)
    p=json.loads((HERE/'ANDROID_TOOLS.json').read_bytes());env=os.environ.copy()
    for tool in p['tool_pins']+[p['baseline_apk']]:
        require(sha(Path(tool['path']))==tool['sha256'],'Tool or baseline APK changed')
    for n in ['DEBUG','JAVA_OPTS','GRADLE_OPTS','JAVA_TOOL_OPTIONS','JDK_JAVA_OPTIONS','_JAVA_OPTIONS']:env.pop(n,None)
    env.update(JAVA_HOME=str(Path(p['tools']['java']).parent.parent),ANDROID_HOME=p['android_sdk'],ANDROID_SDK_ROOT=p['android_sdk'])
    cmd=[p['wrapper'],'--offline','--no-daemon','--console=plain','--no-configuration-cache','-Dfile.encoding=UTF-8','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8','-Diald.mobile.output='+str(a),':app:bundleRelease',':app:assembleRelease']
    cmd[5:5]=['--gradle-user-home',p['gradle_user_home'],'--project-cache-dir',str(a/'project-cache'),'--init-script',str(HERE/'android42.init.gradle')]
    save(a/'INTENT.json',dict(no_repeat=True,versionCode=42))
    b=collect(cmd,cwd=p['android_project'],env=env,label='gradle',attempt=a)
    assert b['exit_code']==0 and b['filtered_lines']==0
    build_log=Path(b['log']['path']).read_text(encoding='utf-8');assert 'IALD_MOBILE_VERSION 4.1(42)' in build_log and 'IALD_MOBILE_OUTPUTS_ISOLATED' in build_log
    apk=a/'projects/app/outputs/apk/release/app-release.apk';aab=a/'projects/app/outputs/bundle/release/app-release.aab'
    assert apk.is_file() and aab.is_file()
    checked()
    resources=resource_pins(checked())
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
    assert "versionCode='42'" in logs['badging'] and "versionName='4.1'" in logs['badging']
    jarlog=logs['aab_signature'];assert 'jar verified.' in jarlog.lower()
    assert 'unsigned entries' not in jarlog.lower() and 'jar is unsigned' not in jarlog.lower()
    assert len(re.findall(r'^\s*s[mki? ]*\s+\d+\s+',jarlog,re.M))>0
    cert=lambda t:re.findall(r'certificate SHA-256 digest:\s*([0-9a-fA-F]+)',t)
    assert cert(logs['apk_signature']) and cert(logs['apk_signature'])==cert(logs['baseline_signature'])
    aab_cert=re.findall(r'SHA256:\s*([0-9A-Fa-f:]+)',logs['aab_certificate']);assert len(aab_cert)==1
    assert aab_cert[0].replace(':','').lower()==cert(logs['apk_signature'])[0].lower()
    save(D/'AUDIT.json',dict(status='PASS',versionCode=42,apk=str(apk),aab=str(aab),apk_sha256=sha(apk),aab_sha256=sha(aab),resources=resources,signer_matches_previous=True,build=b))

if __name__ == '__main__':
    require(not sys.flags.optimize, 'Python optimization refused')
    remote_preflight()
    build()
