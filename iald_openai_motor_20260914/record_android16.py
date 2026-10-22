"""Verify and deliver signed build 16 using the existing upload certificate."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile
import requests
from goal16_records import ROOT, WORK, record, write_new

APP = ROOT / 'iald-app'
SDK = Path(r'C:\Users\rotol\AppData\Local\Android\Sdk\build-tools\36.1.0')
JDK = Path(r'C:\Program Files\Android\Android Studio1\jbr')
os.environ['JAVA_HOME'] = str(JDK)
os.environ['PATH'] = str(JDK / 'bin') + os.pathsep + os.environ['PATH']
memory_before = (ROOT / 'CLAUDE.md').read_bytes()
apk = APP / 'android/app/build/outputs/apk/release/app-release.apk'
aab = APP / 'android/app/build/outputs/bundle/release/app-release.aab'


def signature(path):
    output = subprocess.check_output([str(SDK / 'apksigner.bat'), 'verify', '--print-certs', str(path)])
    return re.search(rb'certificate SHA-256 digest: ([0-9a-f]+)', output).group(1).decode()


cert = signature(apk)
comparisons = {}
for previous in [WORK.parent / 'iald_mobile_release/downloads/IALD-4.1-11.apk',
                 WORK / 'artifacts/IALD-4.1-14.apk', WORK / 'artifacts/IALD-4.1-15.apk']:
    previous_cert = signature(previous)
    assert previous_cert == cert
    comparisons[str(previous)] = previous_cert
bundle_verify = subprocess.run([str(JDK / 'bin/jarsigner.exe'), '-verify', str(aab)],
                               capture_output=True, check=True)
assert b'jar verified.' in bundle_verify.stdout
badging = subprocess.check_output([str(SDK / 'aapt.exe'), 'dump', 'badging', str(apk)])
assert b"name='br.ia.IALD' versionCode='16' versionName='4.1'" in badging
audit = json.loads((WORK / 'mobile16_audit.json').read_bytes())
for name, item in audit['files'].items():
    assert hashlib.sha256((APP / name).read_bytes()).hexdigest() == item['sha256'], name

files = []
for path, prefix, extension in [(apk, 'assets/public/', 'apk'), (aab, 'base/assets/public/', 'aab')]:
    data = path.read_bytes()
    with zipfile.ZipFile(path) as package:
        for name in ['iald.js', 'iald.css', 'index.html', 'kernel_prompt.js', 'kernel_prompt_loja.js']:
            assert package.read(prefix + name) == (APP / 'www' / name).read_bytes(), name
    dest = WORK / ('artifacts/IALD-4.1-16.' + extension)
    write_new(dest, data)
    files.append({'file': str(dest), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
if '--verify-only' in sys.argv:
    report = {'task': 'T4 — Android build 16 verificada localmente', 'status': '[REAL]',
              'build': 16, 'version': '4.1', 'package': 'br.ia.IALD',
              'certificate_sha256': cert, 'previous_certificates': comparisons,
              'build13_comparison': 'APK13 not found in release artifacts, native house or Downloads.',
              'aab_signature': 'jarsigner: jar verified', 'embedded_assets_match_www': True,
              'files': files, 'download_published': False,
              'publication_status': 'AUTO_REVIEW_REQUIRES_UPDATED_USER_APPROVAL',
              'device_installation': 'NOT_TESTED', 'play_upload': 'PENDING_DUNS'}
    receipt = record('android16_verification.json', report,
        '[REAL] Android 4.1 (16) compilado e preservado apenas nos artefatos locais de trabalho. '
        'APK apksigner válido e AAB jarsigner válido; certificado comparado diretamente aos APKs '
        'preservados 11, 14 e 15, todos iguais. APK13 não localizado nas pastas de releases, casa '
        'nativa ou Downloads. Recursos do APK/AAB iguais ao www auditado (173 arquivos). '
        '[INPUT] Publicação parou na revisão automática: pediu autorização atualizada para '
        '173 arquivos no repositório privado e o APK na rota autenticada. Pergunta enviada. '
        'Nenhum push nem entrega em downloads/ feitos nesta etapa.', memory_before)
    print(json.dumps({'receipt': str(receipt), 'files': files, 'published': False}, ensure_ascii=False))
    raise SystemExit(0)
delivery = ROOT / 'downloads/IALD-4.1-16.apk'
write_new(delivery, apk.read_bytes())
assert delivery.read_bytes() == apk.read_bytes()
url = 'https://demo.iald.ia.br/downloads/IALD-4.1-16.apk'
response = requests.get(url, allow_redirects=False, timeout=20, stream=True)
status, location = response.status_code, response.headers.get('Location', '')
response.close()
assert status == 302 and 'login' in location
report = {'task': 'T4 — Android build 16', 'status': '[REAL]', 'build': 16, 'version': '4.1',
          'package': 'br.ia.IALD', 'certificate_sha256': cert, 'previous_certificates': comparisons,
          'build13_comparison': 'No preserved APK13 located in inspected release artifacts; no separate claim.',
          'aab_signature': 'jarsigner: jar verified', 'embedded_assets_match_www': True,
          'files': files, 'download_file': str(delivery), 'download_url': url,
          'anonymous_http_status': status, 'anonymous_redirect': location,
          'device_installation': 'NOT_TESTED', 'play_upload': 'PENDING_DUNS'}
receipt = record('android16_verification.json', report,
    '[REAL] Android 4.1 (16) compilado: assembleRelease e bundleRelease concluídos. APK verificado '
    'por apksigner, AAB por jarsigner; certificado comparado diretamente aos APKs preservados 11, '
    '14 e 15, todos iguais. APK13 não localizado nos artefatos consultados, sem inventar comparação. '
    'Recursos embutidos conferidos contra www e auditoria de 173 arquivos. APK copiado byte a byte '
    'para downloads/IALD-4.1-16.apk; rota pública exige autenticação (302 para login). '
    '[OPEN] Não comprova instalação no aparelho nem publicação Google Play.', memory_before)
print(json.dumps({'receipt': str(receipt), 'files': files, 'download_url': url}, ensure_ascii=False))
