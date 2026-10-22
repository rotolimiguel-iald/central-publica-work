"""Record the local non-secret Android build plan; never start a build."""
from pathlib import Path
import ast
import datetime as dt
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
sys.path.insert(0, str(WORK))
from mission_io import pin, save, call

ROOT = Path('C:/IALD/projetos_pyhton/IALD/iald-app')
SOURCE = WORK / 'staging/app/app/iald.js'
RESOURCE_PLAN = WORK / 'tests_app/MOBILE_EXACT_RESOURCE_PLAN_R1.json'
source_pin = pin(SOURCE)
resources = json.loads(RESOURCE_PLAN.read_bytes())['files']
assert all(x['sha256'] == source_pin['sha256'] for x in resources)
expected_resources = {str(Path(x['destination']).resolve()): x['sha256'] for x in resources}
proc = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '-z'], capture_output=True, check=True)
names = [name for name in proc.stdout.decode('utf-8').split('\0') if name]
for name in names:
    lower = name.lower()
    assert not any(word in lower for word in ('.env', 'keystore', 'credential', 'secret', 'google-services', 'iald_stack_v7', 'iald_psion_state'))
    assert Path(name).suffix.lower() not in ('.jks', '.p12', '.p8', '.pem', '.key', '.mobileprovision')
inputs = []
for name in names:
    path = ROOT / name
    for parent in [path, *path.parents]:
        assert not parent.lstat().st_file_attributes & 0x400
    entry = pin(path)
    entry['sha256'] = expected_resources.get(str(path.resolve()), entry['sha256'])
    inputs.append(entry)
# Generated Gradle inputs are not all versioned. Only public build definitions
# are added; no local signing/configuration file is opened or copied.
extra = [ROOT / 'android/capacitor-cordova-android-plugins/build.gradle',
         ROOT / 'android/capacitor-cordova-android-plugins/cordova.variables.gradle']
settings = (ROOT / 'android/capacitor.settings.gradle').read_text(encoding='utf-8')
import re
for rel in re.findall(r"new File\('([^']+)'\)", settings):
    project = (ROOT / 'android' / rel).resolve()
    assert project.is_relative_to(ROOT / 'node_modules')
    extra.append(project / 'build.gradle')
for path in extra:
    if path.is_file() and str(path) not in {x['path'] for x in inputs}:
        inputs.append(pin(path))
baseline = Path('C:/IALD/projetos_pyhton/IALD/downloads/IALD-4.1-27.apk')
historical = json.loads(Path('C:/IALD/Central de Patentes/work/iald_monthly_wallet_20261007/android_release.json').read_bytes())
assert pin(baseline)['sha256'] == historical['apk']['sha256']
ast.parse((HERE / 'run_android28.py').read_text(encoding='utf-8'))
sdk = Path('C:/Users/rotol/AppData/Local/Android/Sdk')
jbr = Path('C:/Program Files/Android/Android Studio1/jbr')
tools = {'java': str(jbr / 'bin/java.exe'), 'jarsigner': str(jbr / 'bin/jarsigner.exe'),
         'keytool': str(jbr / 'bin/keytool.exe'), 'aapt': str(sdk / 'build-tools/36.1.0/aapt.exe'),
         'apksigner_jar': str(sdk / 'build-tools/36.1.0/lib/apksigner.jar')}
assert all(Path(x).is_file() for x in tools.values())
projection, receipt = call('mission_cli.py', {'operation': 'project', 'reference': str(WORK / 'SESSION_REFERENCE.json'),
    'actor': {'kind': 'agent', 'id': 'codex-mission-memory-review'}, 'max_chars': 125000}, 'android28_candidate_final_project')
plan = {
    'schema': 'iald-mobile-build-plan/v1', 'status': 'DECLARADO_CANDIDATE_NOT_EXECUTED',
    'author': 'codex-mission-memory-review', 'unit': 'F9.MEMORIA_ORGANISMO_20261016',
    'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'reference': pin(WORK / 'SESSION_REFERENCE.json'), 'project': pin(receipt), 'revision': projection['receipt']['revision'],
    'candidate_files': [pin(HERE / n) for n in ('android28.init.gradle', 'run_android28.py')],
    'plan_generator': pin(__file__), 'resource_plan': pin(RESOURCE_PLAN), 'accepted_js': source_pin,
    'accepted_js_sha256': source_pin['sha256'], 'protected_inputs': inputs,
    'wrapper': str(ROOT / 'android/gradlew.bat'), 'android_project': str(ROOT / 'android'),
    'android_sdk': str(sdk), 'gradle_user_home': 'C:/Users/rotol/.gradle', 'tools': tools,
    'tool_pins': [pin(x) for x in tools.values()], 'baseline_apk': pin(baseline),
    'source_anchors': [
        {'path': str(ROOT / 'android/app/build.gradle'), 'lines': [3, 8, 9, 31, 34, 43, 55],
         'meaning': 'Existing signing loader/guard and original4.1(27); signing unchanged.'},
        {'path': str(ROOT / 'android/app/capacitor.build.gradle'), 'lines': [3, 5, 10],
         'meaning': 'Existing Java21 and Capacitor plugin definitions reused.'},
        {'path': str(ROOT / 'android/gradle/wrapper/gradle-wrapper.properties'), 'lines': [3],
         'meaning': 'Existing Gradle8.14.3 wrapper reused offline.'}],
    'viability': 'Gradle init callback registers Android finalizeDsl after plugin application; only defaultConfig.versionCode becomes28. All project buildDirectory values are redirected before evaluation and checked afterwards. This is a candidate verified by source, not a successful Gradle execution.',
    'build_tasks': [':app:bundleRelease', ':app:assembleRelease'],
    'execution_command': 'C:\\Python314\\python.exe -B -X utf8 "' + str(HERE / 'run_android28.py') + '" --run --preflight "<fresh D check receipt in WORK/receipts>"',
    'default_command': 'C:\\Python314\\python.exe -B -X utf8 "' + str(HERE / 'run_android28.py') + '"',
    'preconditions': [
        'Independent root review of candidate and complete plan hash; no execution implied by this delivery.',
        'All three embedded JS copies installed to accepted A hash, other protected source bytes unchanged.',
        'Root serializes original-project builds and holds D; --run requires a matching current D check receipt, revision/hash/context/lease, without impersonating root for check.',
        'No previous RUN_INTENT_R1.json. Interrupted/running/failed intent must be reconciled; never delete it or automatically replay.',
        'No global Gradle init hooks; existing Gradle/JDK/SDK/wrapper/dependency cache available offline. Missing cache fails, no download fallback.',
        'Original configured signing loader must succeed. Runner/init never opens, logs, copies or changes keystore.properties/private keys or IALD_ANDROID_* values.'],
    'output': {
        'root': str(HERE / 'attempts'), 'project_cache': 'Each attempt/project-cache',
        'build_directories': 'Each attempt/projects/<Gradle project path>; root project is _root.',
        'logs': 'UTF-8, sanitized before persistence; raw combined stdout/stderr is hashed in memory only, not stored. Filtering is visible/countable and blocks a clean PASS; no debug/info/environment dump.',
        'receipts': 'Exclusive durable intent, child PID/command, terminal exit/elapsed time/log hashes and final result. Crash without receipt stays uncertain.',
        'cache_limit': 'Original global Gradle caches/native services may receive routine cache/lock writes. This plan isolates build outputs and project cache, not all Gradle runtime writes. No source edit or existing build-output cleanup is requested.'},
    'verification_criteria': [
        'Gradle EXIT0, both init markers present, no filtered sensitive-looking output; candidate bytes and all protected inputs remain unchanged.',
        'APK/AAB archive CRC and member uniqueness; accepted JS hash at assets/public/iald.js and base/assets/public/iald.js; forbidden secret filenames absent.',
        'aapt dump badging APK: applicationId br.ia.IALD, versionName4.1, versionCode28.',
        'apksigner verify APK EXIT0; a single signer and public SHA256 equals pinned released27 APK.',
        'jarsigner verifies signed AAB; keytool -printcert -jarfile inspects only the public AAB certificate and must match APK27/28.',
        'Existing archive audit must additionally decode AAB manifest and inspect complete embedded assets before distribution. Runner reports pending archive review, never published/installed.'],
    'limits': [
        'No build or Gradle configuration phase was executed. finalizeDsl timing/compatibility will be established only by the single reviewed run; failure is preserved, no blind retry.',
        'Byte guards detect source changes and refuse validation; they are not an OS filesystem write sandbox for third-party Gradle plugins. Root must ensure exclusive operation and review any change.',
        'No publish/downloads-copy/git/version source mutation/restart/phone install/store query. Apple login remains pending in a separate step.',
        'Signing credentials already configured are consumed only by the original Gradle flow during a future authorized build; this is not a secret-free signing operation.'
    ],
    'executed': {'build': False, 'gradle': False, 'signature_tools': False, 'production_write': False, 'secret_contents_read': False},
}
save(HERE / 'ANDROID28_BUILD_PLAN_R1.json', plan)
print(json.dumps({'plan': pin(HERE / 'ANDROID28_BUILD_PLAN_R1.json'), 'candidate_files': plan['candidate_files'],
                  'protected_input_count': len(inputs), 'revision': projection['receipt']['revision']}, ensure_ascii=False))
