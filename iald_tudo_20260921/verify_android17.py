"""Verify built artifacts and install the authorized APK in downloads."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
APP = ROOT / 'iald-app'
WORK = Path(r'C:\IALD\Central de Patentes\work\iald_build18_20260921')
apk = APP / 'android/app/build/outputs/apk/release/app-release.apk'
aab = APP / 'android/app/build/outputs/bundle/release/app-release.aab'
previous = ROOT / 'downloads/IALD-4.1-16.apk'
java = Path(r'C:\Program Files\Android\Android Studio1\jbr\bin\java.exe')
signer = Path(r'C:\Users\rotol\AppData\Local\Android\Sdk\build-tools\36.1.0\lib\apksigner.jar')


def certificate(path):
    result = subprocess.run([str(java), '-jar', str(signer), 'verify', '--print-certs', str(path)],
                            capture_output=True, text=True, check=True)
    matches = re.findall(r'^Signer #1 certificate SHA-256 digest: ([0-9a-f]+)$', result.stdout, re.M)
    if len(matches) != 1:
        raise ValueError('Signer not unique')
    return matches[0]


def main():
    digest = certificate(apk)
    assert digest == certificate(previous)
    artifacts = []
    for path, prefix in ((apk, 'assets/public/'), (aab, 'base/assets/public/')):
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            public = [name for name in names if name.startswith(prefix)]
            assert public and not any('.bak_' in name or '.env' in name or '.jks' in name for name in public)
            for name in ('iald.js', 'index.html', 'operational_deadlines.js'):
                assert archive.read(prefix + name) == (APP / 'www' / name).read_bytes()
            registry_name = ('base/' if path == aab else '') + 'assets/capacitor.plugins.json'
            registry = archive.read(registry_name).decode()
            for plugin in ('FilesystemPlugin', 'SharePlugin', 'PrinterPlugin'):
                assert plugin in registry, 'Missing native plugin: ' + plugin
        raw = path.read_bytes()
        artifacts.append({'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    target = ROOT / 'downloads/IALD-4.1-17.apk'
    raw = apk.read_bytes()
    if target.exists() and target.read_bytes() != raw:
        raise ValueError('A different build17 already exists; no overwrite')
    if not target.exists():
        temp = target.with_name(target.name + '.tmp_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
        with temp.open('xb') as handle:
            handle.write(raw)
        assert temp.read_bytes() == raw
        temp.replace(target)
    assert target.read_bytes() == raw
    WORK.mkdir(parents=True, exist_ok=True)
    report = {'time_utc': datetime.now(timezone.utc).isoformat(), 'android_version_code': 17,
              'version_name': '4.1', 'build_successful': True, 'certificate_sha256': digest,
              'same_certificate_as_16': True, 'embedded_assets_match_www': True,
              'native_plugins_present': True, 'artifacts': artifacts, 'download_apk': str(target),
              'physical_export_test': 'PENDING', 'google_play_upload': 'NOT_DONE',
              'ios_build18': 'SOURCES_PREPARED_LOCK_AND_CLOUD_BUILD_PENDING'}
    out = WORK / ('android17_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
    with out.open('xb') as handle:
        handle.write((json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report))


if __name__ == '__main__':
    main()
