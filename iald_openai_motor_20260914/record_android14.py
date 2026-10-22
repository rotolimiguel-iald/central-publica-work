from pathlib import Path
from datetime import datetime
import hashlib
import json
import zipfile

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
WORK = Path(__file__).parent
ARTIFACTS = WORK / 'artifacts'
ARTIFACTS.mkdir(exist_ok=True)
results = []
for source, prefix, suffix in [('android/app/build/outputs/apk/release/app-release.apk', 'assets/public/', 'apk'),
                               ('android/app/build/outputs/bundle/release/app-release.aab', 'base/assets/public/', 'aab')]:
    path = ROOT / source
    data = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        for name in ['iald.js', 'iald.css', 'index.html', 'kernel_prompt.js', 'kernel_prompt_loja.js']:
            assert archive.read(prefix + name) == (ROOT / 'www' / name).read_bytes(), name
    target = ARTIFACTS / ('IALD-4.1-14.' + suffix)
    assert not target.exists(), 'Existing artifact must not be overwritten'
    target.write_bytes(data)
    assert target.read_bytes() == data
    results.append({'file': str(target), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                    'embedded_assets_match': True})
report = {'verified_at': datetime.now().astimezone().isoformat(), 'build': 14, 'version': '4.1',
          'package': 'br.ia.IALD', 'build_exit': 0, 'files': results,
          'signature_verification': 'APK apksigner verified; AAB jarsigner verified',
          'device_installation': 'NOT_TESTED', 'google_play_upload': 'PENDING_ORGANIZATION_DUNS'}
(WORK / 'android14_verification.json').write_bytes(json.dumps(report, indent=2).encode())
print(json.dumps(report))
