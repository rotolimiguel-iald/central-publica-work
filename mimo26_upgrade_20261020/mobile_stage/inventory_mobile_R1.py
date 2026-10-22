"""Read-only mobile inventory. No fetch, build, credential read or runtime write."""
from pathlib import Path
import hashlib, json, re, subprocess, datetime

S=Path(__file__).resolve().parent
W=S.parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
M=R/'iald-app'
OLD=Path(r'C:\IALD\Central de Patentes\work\memoria_organismo_20261016')
def pin(p):
    raw=Path(p).read_bytes()
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
def git(*args):
    p=subprocess.run(['git','-C',str(M),*args],capture_output=True)
    if p.returncode:raise RuntimeError('Read-only Git inspection failed: '+args[0])
    return p.stdout.decode('utf-8').strip()
head=git('rev-parse','HEAD');branch=git('branch','--show-current')
remote=git('rev-parse','--verify','refs/remotes/origin/'+branch)
status=git('status','--porcelain=v1','--untracked-files=no').splitlines()
paths=['app/iald.js','iald-app/www/iald.js','iald-app/ios/App/App/public/iald.js','iald-app/android/app/src/main/assets/public/iald.js']
assets=[pin(R/p) for p in paths]
assert len({p['sha256'] for p in assets})==1
gradle=(M/'android/app/build.gradle').read_text(encoding='utf-8-sig')
pbx=(M/'ios/App/App.xcodeproj/project.pbxproj').read_text(encoding='utf-8-sig')
android_code=int(re.search(r'\bversionCode\s+(\d+)',gradle)[1])
ios_codes=sorted(set(int(x) for x in re.findall(r'CURRENT_PROJECT_VERSION\s*=\s*(\d+)',pbx)))
ios_receipt=OLD/'live_followup_20261017/IOS_DISTRIBUTION_RESULT_R1.json'
ios=json.loads(ios_receipt.read_bytes())
archive=OLD/'mobile_build/ARCHIVE_REVIEW_R1.json'
ar=json.loads(archive.read_bytes())
prior=[OLD/'mobile_build/run_android28.py',OLD/'mobile_build/android28.init.gradle',
       OLD/'mobile_build/prepare_plan_r1.py',OLD/'mobile_build/audit_archives_r1.py',
       OLD/'tests_app/MOBILE_EXACT_RESOURCE_PLAN_R1.json',ios_receipt,archive,
       Path(ar['build_result']['path']),OLD/'live_validation/MOBILE_SOURCE_PUBLISH_R1.json']
ci=[M/'package.json',M/'package-lock.json',M/'capacitor.config.json',
    M/'scripts/validate-release.mjs',M/'ios/App/ci_scripts/ci_post_clone.sh',
    M/'.github/workflows/ios-build.yml',M/'.github/workflows/ios-dependencies.yml',
    M/'ios/App/App.xcodeproj/project.pbxproj',M/'android/app/build.gradle',
    M/'android/gradle/wrapper/gradle-wrapper.properties']
value=dict(schema='iald.mobile.preparation-inventory.v1',observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    reference=str(W/'SESSION_REFERENCE.json'),runtime_root=str(R),mobile_root=str(M),
    git=dict(head=head,branch=branch,origin_tracking_cached=remote,head_equals_cached_remote=head==remote,
        tracked_change_count=len(status),clean_tracked=not status,untracked_inventory='not requested',fetch_executed=False,
        remote_live_verified=False,origin_main='not present in local refs'),
    assets=assets,baseline_inputs=[pin(p) for p in ci],reuse=[pin(p) for p in prior],
    versions=dict(package=json.loads((M/'package.json').read_bytes())['version'],android_source_code=android_code,
        android_source_name=re.search(r'versionName\s+"([^"]+)"',gradle)[1],ios_source_codes=ios_codes,
        ios_marketing=sorted(set(re.findall(r'MARKETING_VERSION\s*=\s*([^;]+)',pbx))),
        last_ios_historical_receipt=ios['build'],last_android_historical_receipt='4.1(28) APK/AAB, local archive review',
        proposed_ios_build=34,proposed_android_code=29,numbers_reserved=False,
        decision='Recheck current store/cloud and local build receipts before selecting any number; no store query performed.'),
    ci=dict(node_pinned_in_xcode_cloud='24.21.0',capacitor='8.5.2',webDir='www',
        xcode_cloud='Existing ci_post_clone.sh downloads pinned Node, verifies SHA, npm ci, sync:ios, requires Package.resolved.',
        github_archive='manual unsigned archive; not TestFlight distribution',
        shared_schemes=sorted(p.name for p in (M/'ios/App/App.xcodeproj/xcshareddata/xcschemes').glob('*.xcscheme')),
        platform='Windows; iOS signed build requires existing macOS/Xcode Cloud route.'),
    executed=dict(build=False,push=False,fetch=False,sync=False,asset_write=False,credential_read=False,publication=False))
raw=json.dumps(value,ensure_ascii=False,indent=2).encode()
p=S/'MOBILE_BASELINE_R1.json'
with p.open('xb') as f:f.write(raw)
assert p.read_bytes()==raw
print(json.dumps(dict(inventory=str(p),sha256=hashlib.sha256(raw).hexdigest(),git_head=head,tracked_clean=not status,assets=len(assets))))
