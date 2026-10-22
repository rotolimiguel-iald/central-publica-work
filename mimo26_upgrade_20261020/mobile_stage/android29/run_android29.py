"""Plan by default; --run plus a fresh deploy preflight is required for one local build.

The Gradle project's existing signing loader is the only signing authority.
This runner never opens/copies signing files, publishes artifacts, or edits sources.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid
import zipfile

HERE = Path(__file__).resolve().parent
WORK = HERE.parent.parent
PLAN = HERE / 'ANDROID29_BUILD_PLAN_R1.json'
REFERENCE = WORK / 'SESSION_REFERENCE.json'
PYTHON = Path('C:/Python314/python.exe')
CLI = Path('C:/IALD/MEMORIA_IALD/mission_cli.py')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pin(path):
    return {'path': str(path), 'sha256': digest(path)}


def save(path, value):
    path = Path(path)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == data
    os.rename(temporary, path)  # Windows refuses an existing destination.


def no_reparse(path):
    for item in [Path(path), *Path(path).parents]:
        if item.exists() and item.lstat().st_file_attributes & 0x400:
            raise RuntimeError('Reparse point refused')


def verify_files(plan):
    differences = []
    for entry in plan['protected_inputs'] + plan['candidate_files'] + plan['tool_pins'] + plan['resource_files'] + [plan['reference'],plan['registry']]:
        no_reparse(entry['path'])
        if not Path(entry['path']).is_file() or digest(entry['path']) != entry['sha256']:
            differences.append(entry['path'])
    return differences


def safe_line(text):
    # Raw bytes are hashed in memory, never persisted. Sensitive-looking output
    # is omitted before UTF-8 custody, including multi-line private key content.
    if re.search(r'(?i)(password|passwd|storepass|keypass|authorization|bearer\s|token\s*[=:]|api[_-]?key|private key|keystore\.properties|\.jks\b|\.keystore\b)', text):
        return '[sensitive-looking build output omitted]\n', True
    if re.search(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,})', text):
        return '[credential-shaped build output omitted]\n', True
    return text, False


def collect(command, *, cwd, env, label, attempt):
    log = attempt / (label + '.utf8.log')
    raw_hash = hashlib.sha256()
    raw_size = 0
    filtered = 0
    errors = []
    key_block = False
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, shell=False)
    save(attempt / (label + '.started.json'), {
        'pid': process.pid, 'command': command, 'cwd': str(cwd),
        'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'no_repeat': True})
    with log.open('xb') as output:
        for raw in iter(process.stdout.readline, b''):
            raw_hash.update(raw)
            raw_size += len(raw)
            text = raw.decode('utf-8', errors='replace')
            if '-----BEGIN ' in text and 'PRIVATE KEY-----' in text:
                key_block = True
            end_block = '-----END ' in text and 'PRIVATE KEY-----' in text
            if key_block:
                clean, omitted = '[private-key block omitted]\n', True
            else:
                clean, omitted = safe_line(text)
            if end_block:
                key_block = False
            filtered += int(omitted)
            output.write(clean.encode('utf-8'))
            output.flush()
            if re.search(r'(?i)(error|failure|exception|failed|what went wrong|sensitive-looking|omitted)', clean):
                errors.append(clean.rstrip()[:1200])
        os.fsync(output.fileno())
    code = process.wait()
    result = {'exit_code': code, 'seconds': time.monotonic() - started,
              'log': pin(log), 'raw_stream_sha256': raw_hash.hexdigest(),
              'raw_stream_bytes': raw_size, 'raw_stream_persisted': False,
              'filtered_lines': filtered, 'errors': errors[-40:]}
    save(attempt / (label + '.receipt.json'), result)
    return result


def fresh_preflight(path, attempt):
    path = Path(path).resolve(strict=True)
    if not path.is_relative_to(WORK.resolve()):
        raise RuntimeError('Preflight must be a receipt in this exact mission')
    no_reparse(path)
    check = json.loads(path.read_bytes())
    if not check.get('ok') or not check['result'].get('ready') or check['result']['task_id'] != 'deploy':
        raise RuntimeError('Ready D preflight required')
    payload = {'operation': 'project', 'reference': str(REFERENCE), 'max_chars': 125000}
    cp = subprocess.run([str(PYTHON), '-B', '-X', 'utf8', str(CLI)],
                        input=json.dumps(payload), capture_output=True, text=True,
                        encoding='utf-8', check=False)
    state = json.loads(cp.stdout)
    save(attempt / 'fresh_project.json', state)
    if cp.returncode or not state.get('ok'):
        raise RuntimeError('Mission project refused')
    old, new = check['result'], state['result']
    for key in ('context_id', 'scope', 'revision', 'state_sha256'):
        if old['receipt'][key] != new['receipt'][key]:
            raise RuntimeError('Stale or different-context preflight')
    if old['projection_sha256'] != new['projection_sha256']:
        raise RuntimeError('Stale preflight projection')
    task = next(x for x in new['projection']['active'] if x['id'] == 'deploy')
    lease = task['lease']
    if task['status'] != 'working' or lease['id'] != old['lease_id'] or lease['owner'] != 'codex-app-01a094df' or lease['expires_at'] <= time.time():
        raise RuntimeError('Current deploy lease required')
    return pin(path)


def public_artifact_checks(plan, attempt, env):
    apk = attempt / 'projects/app/outputs/apk/release/app-release.apk'
    aab = attempt / 'projects/app/outputs/bundle/release/app-release.aab'
    for artifact, asset in [(apk, 'assets/public/iald.js'), (aab, 'base/assets/public/iald.js')]:
        with zipfile.ZipFile(artifact) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)) or archive.testzip() is not None:
                raise RuntimeError('Duplicate or invalid archive entry')
            if hashlib.sha256(archive.read(asset)).hexdigest() != plan['accepted_js_sha256']:
                raise RuntimeError('Embedded JavaScript differs from accepted A')
            if any(re.search(r'(?i)(keystore\.properties|\.env(?:\.|$)|\.(jks|keystore|p12|p8|pem|key)$)', n) for n in names):
                raise RuntimeError('Forbidden archive member name')
    tools = plan['tools']
    inspections = {}
    commands = {
        'apk_badging': [tools['aapt'], 'dump', 'badging', str(apk)],
        'apk_signature': [tools['java'], '-jar', tools['apksigner_jar'], 'verify', '--verbose', '--print-certs', str(apk)],
        'baseline_signature': [tools['java'], '-jar', tools['apksigner_jar'], 'verify', '--print-certs', plan['baseline_apk']['path']],
        'aab_signature': [tools['jarsigner'], '-J-Duser.language=en', '-J-Duser.country=US', '-verify', str(aab)],
        'aab_certificate': [tools['keytool'], '-J-Duser.language=en', '-J-Duser.country=US', '-printcert', '-jarfile', str(aab)]}
    for name, command in commands.items():
        result = collect(command, cwd=attempt, env=env, label=name, attempt=attempt)
        if result['exit_code'] or result['filtered_lines']:
            raise RuntimeError('Public artifact inspection failed: ' + name)
        inspections[name] = result
    texts = {name: Path(result['log']['path']).read_text(encoding='utf-8') for name, result in inspections.items()}
    if not re.search(r"package: name='br\.ia\.IALD' versionCode='29' versionName='4\.1'", texts['apk_badging']):
        raise RuntimeError('APK identity or version mismatch')
    pattern = r'Signer #1 certificate SHA-256 digest:\s*([0-9a-fA-F]+)'
    apk_cert = re.search(pattern, texts['apk_signature'])
    old_cert = re.search(pattern, texts['baseline_signature'])
    aab_cert = re.search(r'SHA256:\s*([0-9A-Fa-f:]+)', texts['aab_certificate'])
    if not all([apk_cert, old_cert, aab_cert]) or len(re.findall(pattern, texts['apk_signature'])) != 1:
        raise RuntimeError('Expected single public signing certificate not established')
    if apk_cert[1].lower() != old_cert[1].lower() or apk_cert[1].lower() != aab_cert[1].replace(':', '').lower():
        raise RuntimeError('APK/AAB signing identity differs from previous28')
    if 'jar verified.' not in texts['aab_signature']:
        raise RuntimeError('AAB JAR verification did not establish a signed archive')
    return {'apk': pin(apk), 'aab': pin(aab), 'public_certificate_sha256': apk_cert[1].lower(),
            'inspections': inspections, 'aab_manifest_version': 'Not separately decoded; pending existing mobile archive audit',
            'published': False, 'installed_on_device': False}


def require_approval(path, operation, plan_path):
    """Verify authorization SOURCE pins; never infer a human identity."""
    path=Path(path).resolve(strict=True)
    if not path.is_relative_to(WORK.resolve()): raise RuntimeError("Authorization receipt must be in this mission")
    no_reparse(path)
    receipt=json.loads(path.read_bytes())
    if (receipt.get("operation") != operation or receipt.get("reference") != str(REFERENCE)
            or receipt.get("plan_sha256") != digest(plan_path)
            or receipt.get("authority") != "source_linkage_not_identity_authentication"
            or not receipt.get("sources")):
        raise RuntimeError("Matching source-linked authorization receipt required")
    for source in receipt["sources"]:
        item=Path(source["path"]).resolve(strict=True)
        if not item.is_relative_to(WORK.resolve()): raise RuntimeError("Authorization source outside this mission")
        no_reparse(item)
        if digest(item) != source["sha256"]: raise RuntimeError("Authorization source changed")
    return pin(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--preflight', type=Path)
    parser.add_argument('--authorization', '--approval', dest='approval', type=Path)
    args = parser.parse_args()
    plan = json.loads(PLAN.read_bytes())
    differences = verify_files(plan)
    if not args.run:
        print(json.dumps({'mode': 'PLAN_ONLY', 'build_started': False, 'plan': pin(PLAN),
                          'input_mismatches': differences, 'run_requires': '--run --preflight <fresh deploy receipt> --authorization <pinned operator source linkage>'}, ensure_ascii=False))
        return 0
    if differences or not args.preflight or not args.approval:
        raise RuntimeError('Run refused: exact installed inputs and fresh deploy preflight required')
    require_approval(args.approval, 'android29_build', PLAN)
    if digest(plan['baseline_apk']['path']) != plan['baseline_apk']['sha256']:
        raise RuntimeError('Previous28 comparison artifact changed')
    for path in plan['tools'].values():
        if not Path(path).is_file():
            raise RuntimeError('Missing existing verification tool')
    no_reparse(HERE)
    gradle_home = Path(plan['gradle_user_home'])
    if any((gradle_home / name).exists() for name in ('init.gradle', 'init.gradle.kts')) or list((gradle_home / 'init.d').glob('*.gradle*')):
        raise RuntimeError('Unreviewed global Gradle init script exists')
    intent = HERE / 'RUN_INTENT_R1.json'
    if intent.exists():
        raise RuntimeError('Existing build intent: reconcile that attempt; no automatic replay')
    attempt = HERE / 'attempts' / dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    attempt.mkdir(parents=True, exist_ok=False)
    preflight = fresh_preflight(args.preflight, attempt)
    if verify_files(plan):
        raise RuntimeError('Inputs changed during preflight')
    wrapper = plan['wrapper']
    command = [wrapper, '--offline', '--no-daemon', '--console=plain', '--no-configuration-cache',
               '--gradle-user-home', str(gradle_home),
               '--project-cache-dir', str(attempt / 'project-cache'), '--init-script', str(HERE / 'android29.init.gradle'),
               '-Dfile.encoding=UTF-8', '-Dsun.stdout.encoding=UTF-8', '-Dsun.stderr.encoding=UTF-8',
               '-Diald.mobile.output=' + str(attempt), ':app:bundleRelease', ':app:assembleRelease']
    if any(re.search(r'[&|<>^%!\r\n]', arg) for arg in command):
        raise RuntimeError('Unsafe command character')
    env = os.environ.copy()
    for name in ('DEBUG', 'JAVA_OPTS', 'GRADLE_OPTS', 'JAVA_TOOL_OPTIONS', 'JDK_JAVA_OPTIONS', '_JAVA_OPTIONS'):
        env.pop(name, None)
    env['JAVA_HOME'] = str(Path(plan['tools']['java']).parent.parent)
    env['ANDROID_HOME'] = plan['android_sdk']
    env['ANDROID_SDK_ROOT'] = plan['android_sdk']
    # The original Gradle loader may use protected IALD_ANDROID_* variables or
    # keystore.properties. No values are inspected, copied or logged here.
    with intent.open('x', encoding='utf-8') as stream:
        json.dump({'attempt': str(attempt), 'plan': pin(PLAN), 'preflight': preflight,
                   'command': command, 'no_repeat': True}, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    result = {'status': 'INTERRUPTED_OR_UNCERTAIN', 'attempt': str(attempt), 'plan': pin(PLAN), 'preflight': preflight}
    try:
        build = collect(command, cwd=plan['android_project'], env=env, label='gradle', attempt=attempt)
        result['build'] = build
        build_text = Path(build['log']['path']).read_text(encoding='utf-8')
        markers = all(marker in build_text for marker in ('IALD_MOBILE_VERSION 4.1(29)', 'IALD_MOBILE_OUTPUTS_ISOLATED'))
        result['init_markers_present'] = markers
        changed = verify_files(plan)
        result['protected_inputs_unchanged'] = not changed
        result['changed_inputs'] = changed
        if changed or build['exit_code'] or build['filtered_lines'] or not markers:
            result['status'] = 'FAILED_REVIEW_REQUIRED'
        else:
            result['artifacts'] = public_artifact_checks(plan, attempt, env)
            if verify_files(plan):
                raise RuntimeError('Inputs changed during artifact checks')
            result['status'] = 'BUILT_PUBLIC_CHECKS_PASS_PENDING_ARCHIVE_REVIEW'
    except Exception as exc:
        result['status'] = 'FAILED_OR_UNCERTAIN_REVIEW_REQUIRED'
        result['error_type'] = type(exc).__name__
        result['error'] = safe_line(str(exc))[0]
    finally:
        save(attempt / 'RESULT_R1.json', result)
    print(json.dumps({'result': pin(attempt / 'RESULT_R1.json'), 'status': result['status'], 'published': False}, ensure_ascii=False))
    return 0 if result['status'] == 'BUILT_PUBLIC_CHECKS_PASS_PENDING_ARCHIVE_REVIEW' else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'build_started': False, 'error_type': type(exc).__name__, 'error': safe_line(str(exc))[0]}, ensure_ascii=False))
        raise SystemExit(2)
