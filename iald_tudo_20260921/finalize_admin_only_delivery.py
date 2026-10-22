"""Record observed release states; retain unknown expiry dates as unknown."""
from datetime import datetime
from pathlib import Path
import hashlib
import json
import subprocess

work = Path(__file__).resolve().parent
root = Path(r'C:\IALD\projetos_pyhton\IALD')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
now = datetime.now().astimezone().isoformat()
apk = root / 'downloads/IALD-4.1-19.apk'
url = 'https://demo.iald.ia.br/downloads/IALD-4.1-19.apk'
local_apk = apk.read_bytes()
commit = subprocess.check_output(
    [r'C:\Program Files\Git\cmd\git.exe', '-C', str(root / 'iald-app'), 'rev-parse', 'HEAD'],
    text=True).strip()
assert commit.startswith('e65d695')
status = {
    'checked_at': now,
    'commit': commit,
    'web': 'Correção instalada; avisos somente em /admin, API do aplicativo sem dados operacionais.',
    'ios_internal': {'version': '4.1 (20)', 'group': 'IALD Equipe', 'status': 'Em testes',
                     'operator_member_verified': True, 'operator_installed_observed': '4.1 (19)'},
    'ios_external': {'version': '4.1 (20)', 'group': 'IALD Piloto', 'status': 'Em testes',
                     'automatic_notifications': True, 'family_invitations': 'Alana e Liana: Convidado',
                     'link': 'https://testflight.apple.com/join/A5XEdy1H'},
    'android': {'version': '4.1 (19)', 'apk': url, 'public_download_bytes_verified': False,
                'download_requires_login': True,
                'download_observation': 'HEAD segue para /login com HTML200; GET Python recusado403. Não anunciado como download público livre.',
                'apk_local': str(apk),
                'apk_sha256': hashlib.sha256(local_apk).hexdigest(),
                'signature_matches_previous_release': True, 'aab_built': True,
                'google_play': 'Não enviado; cadastro depende de D-U-N-S.'},
    'physical_install_of_this_hotfix': 'Não verificada nos aparelhos.',
    'independent_review': 'admin_only_deadlines_review_20260922_182439_977129.json: sem achados na revisão estática.',
    'testflight_expiry': 'UI exibe Expira em 90 dias. Data exata não exposta; não inferida.',
    'overall_goal': 'ACTIVE; demais etapas não concluídas por esta entrega.'
}
target = work / 'admin_only_delivery_status.json'
with target.open('xb') as handle:
    handle.write(json.dumps(status, ensure_ascii=False, indent=2).encode('utf8'))

deadlines = root / 'iald_deadlines.json'
before = deadlines.read_bytes()
doc = json.loads(before)
doc['checked_at'] = now
for key, group in (('testflight_internal', 'IALD Equipe'), ('testflight_external', 'IALD Piloto')):
    doc['items'][key] = {
        'expires_at': None,
        'label': 'IALD 4.1 (20) — ' + group,
        'source': 'App Store Connect,22/09/2026: Em testes; Expira em90dias. Data exata não exibida; não inferida.',
        'build': '4.1 (20)', 'status': 'Em testes'
    }
backup = deadlines.with_name(deadlines.name + '.bak_' + stamp)
with backup.open('xb') as handle:
    handle.write(before)
assert backup.read_bytes() == before
after = (json.dumps(doc, ensure_ascii=False, indent=2) + '\n').encode('utf8')
temp = deadlines.with_name(deadlines.name + '.tmp_' + stamp)
with temp.open('xb') as handle:
    handle.write(after)
assert temp.read_bytes() == after and len(after) > 500
assert deadlines.read_bytes() == before, 'Concurrent change'
temp.replace(deadlines)
assert deadlines.read_bytes() == after
print(json.dumps({'delivery_status': str(target), 'admin_deadlines_updated': True,
                  'android_local_artifact_verified': True, 'android_download_requires_login': True}))
