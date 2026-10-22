"""Offline release audit. Only writes two reports and their byte-preserving backups in W.

Run after the main agent finishes sync and the Android rebuild. No publishing,
native changes, keystore access, cloud calls, package installation or build.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile

W = Path(__file__).resolve().parent
R = Path(r'C:/IALD/projetos_pyhton/IALD')
A = R / 'iald-app'
BT = Path(r'C:/Users/rotol/AppData/Local/Android/Sdk/build-tools/36.1.0')
JBR = Path(r'C:/Program Files/Android/Android Studio1/jbr/bin')
EXPECTED_HEAD = (W / 'mobile_commit.txt').read_text().strip()
TOOLS = dict(aapt=BT / 'aapt.exe', aapt2=BT / 'aapt2.exe',
             apksigner=BT / 'apksigner.bat', apksigner_jar=BT / 'lib/apksigner.jar',
             java=JBR / 'java.exe', jarsigner=JBR / 'jarsigner.exe', keytool=JBR / 'keytool.exe')
PATTERNS = {
    'private_key_pem': rb'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----',
    'github_token': rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b',
    'google_api_key': rb'\bAIza[0-9A-Za-z_-]{30,}\b',
    'aws_access_key': rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    'provider_key': rb'\bsk-(?:proj-|ant-api[0-9]*-)?[A-Za-z0-9_-]{32,}\b',
    'jwt_literal': rb'\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{20,}\b',
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(args):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True,
                            encoding='utf-8', errors='replace', timeout=90)
    return result.returncode, result.stdout + '\n' + result.stderr


def git(*args):
    result = subprocess.run(['git', '-c', 'safe.directory=' + A.as_posix(),
        '--no-optional-locks', '-C', str(A), *args], capture_output=True, check=True, timeout=30)
    return result.stdout.decode('utf-8').strip()


def name_issues(name):
    parts = PurePosixPath(name.lower()).parts
    base = PurePosixPath(name.lower()).name
    found = []
    if any(p in ('.git', '.svn', '__pycache__', 'backups') or p.startswith('_backups') for p in parts):
        found.append('backup_or_private_directory')
    if re.search(r'\.(?:bak|backup|orig|rej|tmp)(?:[._-]|$)|\.candidate$|~$', base):
        found.append('backup_or_temporary_file')
    if (base == '.env' or base.startswith('.env.') or base in (
            'keystore.properties', 'local.properties', 'iald_users.json',
            'iald_stack_v7.py', 'iald_psion_state.json', 'userdb.json')
            or re.search(r'\.(?:jks|keystore|p12|pfx|key|pyc)$', base)):
        found.append('credential_or_private_file')
    if '..' in parts or name.startswith('/') or '\\' in name:
        found.append('unsafe_archive_path')
    return found


def secret_matches(raw):
    # Report categories/counts only, never credential bytes.
    return [{'pattern': key, 'occurrences': len(matches)} for key, pattern in PATTERNS.items()
            if (matches := re.findall(pattern, raw))]


def signatures(paths):
    out = {'artifact_sha256': {key: sha(path.read_bytes()) for key, path in paths.items()},
           'tools': {key: str(path) for key, path in TOOLS.items()}}
    for key in ('apk', 'previous_apk'):
        code, log = run([TOOLS['java'], '-jar', TOOLS['apksigner_jar'], 'verify',
                         '--verbose', '--print-certs', paths[key]])
        certs = re.findall(r'^Signer #\d+ certificate SHA-256 digest: ([0-9a-f]+)$', log, re.M)
        out[key] = dict(exit_code=code, verified=code == 0 and len(certs) == 1,
                        certificate_sha256=certs, schemes=re.findall(r'^Verified using.*$', log, re.M))
    code, log = run([TOOLS['aapt'], 'dump', 'badging', paths['apk']])
    line = next((x for x in log.splitlines() if x.startswith('package:')), '')
    out['apk_metadata'] = dict(exit_code=code, attributes=dict(re.findall(r"(\w+)='([^']*)'", line)))
    code, log = run([TOOLS['jarsigner'], '-J-Duser.language=en', '-verify', '-verbose', paths['aab']])
    out['aab_signature'] = dict(exit_code=code, jar_verified='jar verified.' in log.lower(),
        unsigned_entries_warning='unsigned entries' in log.lower(),
        signed_entries=len(re.findall(r'^\s*s[mki? ]*\s+\d+\s+', log, re.M)),
        warnings=sorted(set(x.strip() for x in log.splitlines() if any(t in x.lower() for t in
            ('self-signed', 'invalid certificate chain', 'not timestamped', 'will expire', 'expired', 'unsigned entries', 'jar is unsigned')))))
    code, log = run([TOOLS['keytool'], '-J-Duser.language=en', '-printcert', '-jarfile', paths['aab']])
    certs = [x.replace(':', '').lower() for x in re.findall(r'SHA256:\s*([A-Fa-f0-9:]+)', log)]
    out['aab_signature'].update(certificate_exit_code=code, certificate_sha256=certs)
    out['all_same_certificate'] = (len(certs) == 1 and certs == out['apk']['certificate_sha256']
                                   == out['previous_apk']['certificate_sha256'])
    out['artifacts_unchanged_during_verification'] = all(
        sha(path.read_bytes()) == out['artifact_sha256'][key] for key, path in paths.items())
    return out


def protobuf_fields(raw):
    def varint(pos):
        value = shift = 0
        while pos < len(raw) and shift <= 70:
            byte = raw[pos]; pos += 1; value |= (byte & 127) << shift
            if byte < 128: return value, pos
            shift += 7
        raise ValueError('Invalid protobuf varint')
    pos = 0
    while pos < len(raw):
        tag, pos = varint(pos); number, wire = tag >> 3, tag & 7
        if not number: raise ValueError('Invalid protobuf field')
        if wire == 0: value, pos = varint(pos)
        else:
            if wire == 2: size, pos = varint(pos)
            elif wire in (1, 5): size = 8 if wire == 1 else 4
            else: raise ValueError('Unsupported protobuf field')
            if pos + size > len(raw): raise ValueError('Truncated protobuf data')
            value = raw[pos:pos + size]; pos += size
        yield number, wire, value


def manifest_attributes(raw):
    element = list(protobuf_fields(next(v for n, w, v in protobuf_fields(raw) if n == 1 and w == 2)))
    if next(v.decode() for n, w, v in element if n == 3 and w == 2) != 'manifest':
        raise ValueError('Not an Android manifest')
    out = {}
    for number, wire, value in element:
        if number != 4 or wire != 2: continue
        attr = list(protobuf_fields(value))
        name = next((v.decode() for n, w, v in attr if n == 2 and w == 2), '')
        if name not in ('package', 'versionCode', 'versionName'): continue
        if name in out: raise ValueError('Duplicate manifest identity attribute')
        out[name] = next(v.decode() for n, w, v in attr if n == 3 and w == 2)
        if name == 'versionCode':
            item = next(v for n, w, v in attr if n == 6 and w == 2)
            primitive = next(v for n, w, v in protobuf_fields(item) if n == 7 and w == 2)
            out['compiled_versionCode'] = next(v for n, w, v in protobuf_fields(primitive) if n == 6 and w == 0)
            if int(out[name]) != out['compiled_versionCode']: raise ValueError('Compiled versionCode mismatch')
    return out


def save_report(path, data):
    """Preserve the exact prior JSON bytes, then atomically replace inside W."""
    if path.parent.resolve() != W.resolve(): raise ValueError('Report outside W')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    before = path.read_bytes() if path.exists() else None
    if before is not None:
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as handle:
            handle.write(before); handle.flush(); os.fsync(handle.fileno())
        if backup.read_bytes() != before: raise OSError('Report backup verification failed')
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + stamp)
    with temporary.open('xb') as handle:
        handle.write(raw); handle.flush(); os.fsync(handle.fileno())
    if temporary.read_bytes() != raw: raise OSError('Report candidate verification failed')
    if (path.read_bytes() if path.exists() else None) != before:
        raise RuntimeError('Concurrent report modification; candidate and backup preserved')
    os.replace(temporary, path)
    if path.read_bytes() != raw: raise OSError('Report replacement verification failed')


def audit():
    checks = {}; pins = {}
    def read(path):
        raw = path.read_bytes(); pins[path] = sha(raw); return raw
    head = git('rev-parse', 'HEAD'); status = git('status', '--porcelain=v1', '--untracked-files=all')
    tracked = [p for p in git('ls-files', '-z', '--', 'www', 'ios/App/App/public').split('\0') if p]
    tracked_bad = [p for p in tracked if name_issues(p)]
    checks.update(head_matches_requested_commit=head == EXPECTED_HEAD, working_tree_clean=not status,
                  tracked_mobile_assets_exclude_backups=not tracked_bad)
    roots = dict(web=R / 'app', www=A / 'www', ios=A / 'ios/App/App/public',
                 android=A / 'android/app/src/main/assets/public')
    changed = {}
    for name in ('iald.js',):
        staged = sha(read(W / 'stage' / 'app' / name))
        surfaces = {key: sha(read(root / name)) for key, root in roots.items()}
        changed[name] = dict(stage_sha256=staged, surfaces=surfaces)
        checks['all_surfaces_match_' + name] = all(value == staged for value in surfaces.values())
    inventories = {}; scans = {}
    for key in ('www', 'ios', 'android'):
        inv = {}; names = []; findings = []
        for path in roots[key].rglob('*'):
            if not path.is_file(): continue
            relative = path.relative_to(roots[key]).as_posix(); bad = name_issues(relative)
            raw = read(path); inv[relative] = sha(raw)
            if bad: names.append(dict(file=relative, categories=bad))
            elif matches := secret_matches(raw): findings.append(dict(file=relative, matches=matches))
        inventories[key] = inv
        scans[key] = dict(files_checked=len(inv), forbidden_names=names, secret_pattern_findings=findings)
    mirrors = {}
    for key in ('ios', 'android'):
        missing = sorted(set(inventories['www']) - set(inventories[key]))
        mismatch = sorted(n for n in inventories['www'] if n in inventories[key] and inventories['www'][n] != inventories[key][n])
        mirrors[key] = dict(missing=missing, mismatch=mismatch,
                            generated_extras=sorted(set(inventories[key]) - set(inventories['www'])))
        checks[key + '_mirrors_all_www'] = not missing and not mismatch
    mapped_count = 0; mapped_bad = []
    for relative, expected in inventories['www'].items():
        origin = roots['web'] / ('kernel_prompt_bundle.js' if relative == 'kernel_prompt.js' else relative)
        if origin.is_file():
            mapped_count += 1
            if sha(read(origin)) != expected: mapped_bad.append(relative)
    checks['mapped_web_assets_match'] = not mapped_bad
    paths = dict(apk=A / 'android/app/build/outputs/apk/release/app-release.apk',
                 aab=A / 'android/app/build/outputs/bundle/release/app-release.aab',
                 previous_apk=R / 'downloads/IALD-4.1-24.apk')
    sig = signatures(paths); packages = {}
    for key in ('apk', 'aab'):
        path = paths[key]; raw = read(path)
        item = dict(path=str(path), bytes=len(raw), sha256=sha(raw))
        prefix = ('base/' if key == 'aab' else '') + 'assets/public/'
        with zipfile.ZipFile(path) as archive:
            entries = [entry for entry in archive.infolist() if not entry.is_dir()]
            names = [entry.filename for entry in entries]
            duplicate = sorted(name for name, count in Counter(names).items() if count > 1)
            bad_names = []; findings = []; inv = {}
            for entry in entries:
                bad = name_issues(entry.filename)
                content = archive.read(entry)
                if entry.filename.startswith(prefix): inv[entry.filename[len(prefix):]] = sha(content)
                if bad: bad_names.append(dict(file=entry.filename, categories=bad))
                elif matches := secret_matches(content): findings.append(dict(file=entry.filename, matches=matches))
            missing = sorted(set(inventories['android']) - set(inv))
            extra = sorted(set(inv) - set(inventories['android']))
            mismatch = sorted(n for n in inv if n in inventories['android'] and inv[n] != inventories['android'][n])
            registry = ('base/' if key == 'aab' else '') + 'assets/capacitor.plugins.json'
            registry_match = sha(archive.read(registry)) == sha(read(A / 'android/app/src/main/assets/capacitor.plugins.json'))
            item.update(entries=len(entries), duplicate_entries=duplicate, crc_error=archive.testzip(),
                        public_assets=len(inv), public_asset_sha256=inv, missing_native_assets=missing,
                        extra_public_assets=extra, different_native_assets=mismatch,
                        forbidden_names=bad_names, secret_pattern_findings=findings,
                        plugin_registry_matches_native=registry_match)
            if key == 'aab': item['manifest'] = manifest_attributes(archive.read('base/manifest/AndroidManifest.xml'))
        packages[key] = item
        checks[key + '_signature_hash_stable'] = item['sha256'] == sig['artifact_sha256'][key]
        checks[key + '_assets_match_native'] = not (missing or extra or mismatch) and registry_match
        checks[key + '_zip_integrity'] = not duplicate and item['crc_error'] is None
        checks[key + '_no_backups_or_secret_findings'] = not (bad_names or findings)
    checks['native_assets_no_backups_or_secret_findings'] = all(not x['forbidden_names'] and not x['secret_pattern_findings'] for x in scans.values())
    pbx = read(A / 'ios/App/App.xcodeproj/project.pbxproj')
    gradle = read(A / 'android/app/build.gradle')
    versions = dict(ios_builds=[int(x) for x in re.findall(rb'CURRENT_PROJECT_VERSION\s*=\s*(\d+);', pbx)],
                    ios_versions=[x.decode() for x in re.findall(rb'MARKETING_VERSION\s*=\s*([^;]+);', pbx)],
                    android_codes=[int(x) for x in re.findall(rb'\bversionCode\s+(\d+)', gradle)],
                    android_versions=[x.decode() for x in re.findall(rb'\bversionName\s+"([^"]+)"', gradle)])
    checks['native_versions_correct'] = versions == dict(ios_builds=[30, 30], ios_versions=['4.1', '4.1'], android_codes=[27], android_versions=['4.1'])
    apk_meta = sig['apk_metadata']['attributes']; aab_meta = packages['aab']['manifest']
    checks['apk_manifest_correct'] = sig['apk_metadata']['exit_code'] == 0 and all(apk_meta.get(k) == v for k, v in dict(name='br.ia.IALD', versionCode='27', versionName='4.1').items())
    checks['aab_manifest_correct'] = all(aab_meta.get(k) == v for k, v in dict(package='br.ia.IALD', versionCode='27', versionName='4.1', compiled_versionCode=27).items())
    checks['apk_signatures_verified'] = sig['apk']['verified'] and sig['previous_apk']['verified']
    signed = sig['aab_signature']
    checks['aab_signature_verified'] = signed['exit_code'] == 0 and signed['jar_verified'] and not signed['unsigned_entries_warning'] and signed['signed_entries'] > 0 and signed['certificate_exit_code'] == 0
    checks['same_certificate_as_build24'] = sig['all_same_certificate']
    checks['signature_inputs_stable'] = sig['artifacts_unchanged_during_verification']
    checks['files_stable_at_end'] = all(sha(path.read_bytes()) == expected for path, expected in pins.items())
    checks['git_stable_at_end'] = git('rev-parse', 'HEAD') == head and git('status', '--porcelain=v1', '--untracked-files=all') == status
    common = dict(at=datetime.now(timezone.utc).isoformat(), passed=all(checks.values()), commit=head, checks=checks,
                  tools={key: str(path) for key, path in TOOLS.items()}, limitations=[
                      'Offline: sem verificação do IPA/Xcode Cloud/TestFlight, push remoto ou instalação física.',
                      'Busca de segredos por nomes e seis padrões; ausência de matches não prova ausência de todo segredo possível.',
                      'Certificado autoassinado é comparado ao APK24; advertência JAR é registrada.',
                      'Nenhuma publicação, alteração nativa ou leitura de keystore/credenciais locais.'])
    android = dict(common, version='4.1', versionCode=27, apk=packages['apk'], aab=packages['aab'], signature_evidence=sig, published=False)
    mobile = dict(common, versions=versions, local_git_status=status, changed_assets=changed, native_mirrors=mirrors,
                  surface_scans=scans, mapped_web_assets=dict(checked_files=mapped_count, mismatches=mapped_bad),
                  tracked_assets=dict(www=sum(p.startswith('www/') for p in tracked), ios_public=sum(p.startswith('ios/App/App/public/') for p in tracked), forbidden=tracked_bad),
                  ci_post_clone_sha256=sha(read(A / 'ios/App/ci_scripts/ci_post_clone.sh')),
                  android_report=str(W / 'android_verified.json'))
    save_report(W / 'android_verified.json', android)
    save_report(W / 'mobile_audit.json', mobile)
    print(json.dumps(dict(passed=common['passed'], failed_checks=[key for key, value in checks.items() if not value],
                         assets={key: value['stage_sha256'] for key, value in changed.items()},
                         package_sha256={key: value['sha256'] for key, value in packages.items()},
                         reports=[str(W / 'android_verified.json'), str(W / 'mobile_audit.json')]), ensure_ascii=False))
    return 0 if common['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(audit())
