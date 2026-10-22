"""Verify and publish the Android hotfix without mixing parallel web changes."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import zipfile

root = Path(r'C:\IALD\projetos_pyhton\IALD')
mobile = root / 'iald-app'
apk = mobile / 'android/app/build/outputs/apk/release/app-release.apk'
aab = mobile / 'android/app/build/outputs/bundle/release/app-release.aab'
metadata = json.loads((apk.parent / 'output-metadata.json').read_text())
assert metadata['applicationId'] == 'br.ia.IALD'
assert metadata['elements'][0]['versionCode'] == 19
assert metadata['elements'][0]['versionName'] == '4.1'
assets = ('index.html', 'iald.css', 'iald.js', 'operational_deadlines.js')
for package, prefix in ((apk, 'assets/public/'), (aab, 'base/assets/public/')):
    with zipfile.ZipFile(package) as archive:
        for name in assets:
            assert archive.read(prefix + name) == (mobile / 'www' / name).read_bytes(), (package, name)
        js = archive.read(prefix + 'iald.js')
        assert b'/api/alertas' not in js
        assert b'renderOperationalDeadlines' not in js
dest = root / 'downloads/IALD-4.1-19.apk'
data = apk.read_bytes()
if dest.exists():
    assert dest.read_bytes() == data, 'Existing download differs; preserve it.'
else:
    with dest.open('xb') as handle:
        handle.write(data)
assert dest.read_bytes() == data
receipt = {
    'android_version': '4.1 (19)',
    'assets_match_mobile_www': True,
    'consumer_operational_alerts_removed': True,
    'parallel_web_export_changes_included': False,
    'artifacts': [{'path': str(p), 'bytes': p.stat().st_size,
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                  for p in (apk, aab, dest)],
    'google_play': 'NOT_UPLOADED',
    'physical_test': 'PENDING',
}
out = Path(__file__).parent / ('android19_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
with out.open('x', encoding='utf8') as handle:
    handle.write(json.dumps(receipt, indent=2))
print(json.dumps({'receipt': str(out), 'download': str(dest)}))
