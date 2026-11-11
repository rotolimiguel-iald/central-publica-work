"""Generate scoped build candidates from the inspected preceding release, no execution."""
import ast
from prepare_mobile import HERE, PREVIOUS, REPO, read, report, put, require, sha

def main():
    baseline = read(HERE/'BASELINE.json')
    require((baseline['current_ios'],baseline['current_android'],baseline['version'])==(46,41,'4.1'), 'Re-audit adaptation for other versions')
    sources = {}
    def source(name):
        path = PREVIOUS/name
        raw = path.read_bytes()
        sources[name] = dict(path=str(path),sha256=sha(raw))
        return raw.decode('utf8')
    build = source('build_android41.py')
    build = build.replace('from stage_mobile import HERE, report, require','from prepare_mobile import HERE, report, require')
    build = build.replace('release 41','release 42').replace('build41','build42').replace('android41.init.gradle','android42.init.gradle')
    build = build.replace('versionCode=41','versionCode=42').replace('4.1(41)','4.1(42)').replace("versionCode='41'", "versionCode='42'")
    # Two artifacts/companion hashes, offline execution, no-repeat attempt, signer
    # comparison and archive checks are retained from the inspected procedure.
    ast.parse(build)
    put(HERE/'build_android42.py', build.encode())
    init = source('android41.init.gradle')
    init = init.replace('iald_owner_notice_20261105/mobile/release','app_scroll_20261106/mobile/release')
    init = init.replace('versionCode != 41','versionCode != 42').replace('versionCode = 41','versionCode = 42').replace('4.1(41)','4.1(42)')
    put(HERE/'android42.init.gradle',init.encode())
    log = source('build_log.py')
    ast.parse(log)
    put(HERE/'build_log.py', log.encode())
    tools = read(PREVIOUS/'ANDROID_TOOLS.json')
    source('ANDROID_TOOLS.json')
    apk = REPO.parent/'downloads/IALD-4.1-41.apk'
    audit = read(PREVIOUS/'release/AUDIT.json')
    source('release/AUDIT.json')
    require(audit['status']=='PASS' and audit['versionCode']==41 and sha(apk.read_bytes())==audit['apk_sha256'], 'Previous signed APK mismatch')
    tools['baseline_apk'] = dict(path=str(apk),sha256=sha(apk.read_bytes()))
    tools['status'] = 'PREVIOUS_TOOL_PINS_RECHECKED_BY_BUILD_BEFORE_EXECUTION'
    report(HERE/'ANDROID_TOOLS.json',tools)
    # References only: old deploy/commit/publish functions are not imported or run.
    for name in ('stage_mobile.py','prepare_release.py','release_controls.py','publish_apk41.py','ROTEIRO.md'):
        source(name)
    report(HERE/'PROVENANCE.json', dict(status='STATIC_PREPARATION_NOT_INDEPENDENT_APPROVAL',sources=sources))
    report(HERE/'PUBLICATION_MANIFEST.json', dict(
        status='WAITING_PARENT_STAGE_AND_INDEPENDENT_REVIEW',unit='F9.APP_SCROLL_20261106',
        reference=str(HERE.parent/'SESSION_REFERENCE.json'),baseline=baseline,
        proposed=dict(ios=47,android=42,version='4.1'),
        checkout_writes_performed=False,build_started=False,push_performed=False,
        android=dict(channel='existing authenticated APK download',google_play='NOT_REQUESTED',
                     filename='IALD-4.1-42.apk',audit_required=str(HERE/'release/AUDIT.json'),
                     previous_signed_apk=tools['baseline_apk'],
                     publication='Parent only: no-overwrite rename, preserve and hash all older APKs, authenticated download hash and anonymous denial'),
        ios=dict(branch=baseline['branch'],remote='existing private origin; validate fetch/push URLs before publication',
                 cloud='Parent: locate existing run by exact commit before starting anything; do not duplicate',
                 groups=['IALD Equipe','IALD Piloto'],availability='NOT_VERIFIED'),
        gates=['Parent stage READY_FOR_MOBILE with hashes','Independent exact-plan review',
               'Parent controlled install and post-install hashes','Parent BUILD_AUTHORIZED',
               'Offline build and APK/AAB resource/signature audit','Parent channel publication and availability receipts'],
        physical_installation='NOT_VERIFIED'))

if __name__ == '__main__':
    main()
