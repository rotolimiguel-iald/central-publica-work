"""Record the observed CIAL reply and the requirement-level release impasse."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from goal16_records import ROOT, WORK, record, write_new

sys.stdout.reconfigure(encoding='utf-8')
APP = ROOT / 'iald-app'
surfaces = [ROOT / 'CLAUDE.md', WORK / 'HANDOFF_RUNTIME.md',
            APP / 'HANDOFF_MOTOR_OPENAI_20260914.md',
            WORK.parent.parent / 'memory/TGL_ATLAS.md',
            WORK.parent.parent / 'memory/TGL_INDICE_VIVO.md',
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
snapshots = {p: p.read_bytes() for p in surfaces}
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def load(name):
    return json.loads((WORK / name).read_bytes())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

android = load('android16_verification.json')
artifact_checks = [dict(file=item['file'], sha256=sha(item['file']),
                       matches_verified=sha(item['file']) == item['sha256'])
                   for item in android['files']]
audit = load('mobile16_audit.json')
js_paths = ['www/iald.js', 'ios/App/App/public/iald.js',
            'android/app/src/main/assets/public/iald.js']
expected_js = audit['files']['www/iald.js']['sha256']
js_checks = {name: {'sha256': sha(APP / name),
                    'matches_audit': sha(APP / name) == expected_js} for name in js_paths}
head = subprocess.check_output(['git', '-C', str(APP), 'rev-parse', 'HEAD'], text=True).strip()
delivered = (ROOT / 'downloads/IALD-4.1-16.apk').exists()
assert all(item['matches_verified'] for item in artifact_checks), 'Artifact changed; stop.'
assert all(item['matches_audit'] for item in js_checks.values()), 'App changed; stop.'
assert not delivered, 'Delivery changed; reassess before recording an impasse.'
assert not (WORK / 'mobile16_publication.json').exists(), 'Publication changed; reassess.'

reply = ('Não há solicitações para o CNPJ 62.757.606/0001-23 em nosso sistema. '
         'Pode seguir com a solicitação com o link enviado acima, Luiz')
note = (
    '[REAL] Retorno humano da CIAL observado em 15/09: Erica informou que não há '
    'solicitações para o CNPJ 62.757.606/0001-23 em seu sistema e orientou o formulário '
    'gratuito já indicado. Isso NÃO comprova ausência de D-U-N-S em toda a base; nenhum '
    'número foi recebido. [INPUT/LEGAL] Conta Dunsguide, termos e CAPTCHA continuam '
    'pendentes do aceite solicitado. [REAL] Apple permanece no login pelo iPhone; '
    'OpenAI mostra zero chaves admin, modal IALD Custos/30 dias/Usage Read preparado; '
    'contador ainda usa o razão local. APK/AAB16 e os três JS preservados; APK16 não '
    'entregue e publicação privada não realizada. [INPUT] Aprovações específicas da '
    'chave administrativa e dos envios continuam pendentes após rejeição automática; '
    'painel de publicação da política ainda não informado. T1/T3 concluídas conforme '
    'recibos, T2/T4/T5/T6 não integralmente concluídas. Impasse recorrente por pelo '
    'menos três rodadas; aguardar participação do operador sem repetir builds ou '
    'criar chaves. Nenhum reinício ou alteração de gate. Próximos passos e evidências '
    'por requisito no recibo goal16_impasse_20260915.json.'
)
report = {
    'task': 'auditoria do impasse e retorno da consulta D-U-N-S',
    'status': '[REAL/INPUT] GOAL_NOT_COMPLETE',
    'previous_goal_turn_classification': 'NO_PROGRESS_FOR_BUILD16_GOAL; public index separately reverified',
    'current_turn_progress': 'New human CIAL reply resolves the existing-request inquiry; receipts updated.',
    'duns': {'agent': 'Erica', 'reply_exact': reply, 'reply_timestamp': 'Not available; UI relative time only',
             'observed_date': '2026-09-15', 'number_received': False,
             'interpretation': 'No requests in the support system; not proof of no DUNS worldwide.',
             'account_created': False, 'terms_accepted': False, 'captcha_completed': False,
             'paid_service': False},
    'T1': {'state': 'COMPLETE_PER_ACCEPTANCE', 'receipt': 'saldo_openai_ancora_20260915.json',
           'latest_cli_observation': '2026-09-15T15:53:40+00:00', 'nivel': 'atencao', 'saldo_usd': 9.9},
    'T2': {'state': 'BLOCKED_PENDING_SPECIFIC_APPROVAL', 'saved': False,
           'admin_keys_visible': 0, 'prepared_permission': 'api.usage.read', 'validity_days': 30,
           'fonte_gasto': 'registro da IALD (só o uso que passa por este servidor)',
           'helper_session_confirmed_live': 89066},
    'T3': {'state': 'COMPLETE_PER_ACCEPTANCE', 'receipt': 'moderations_permission_20260915.json'},
    'T4': {'state': 'LOCAL_ANDROID_COMPLETE_PUBLICATION_AND_TESTFLIGHT_INCOMPLETE',
           'artifact_checks': artifact_checks, 'js_checks': js_checks, 'git_head': head,
           'apk16_delivered': delivered, 'apple_ui': 'Login; Inicie sessão com o iPhone',
           'build13_certificate_comparison': android['build13_comparison'],
           'publication_approval': 'PENDING_173_AUDITED_FILES_AND_AUTHENTICATED_APK_ROUTE'},
    'T5': {'state': 'INQUIRY_RECEIPT_COMPLETE_REGISTRATION_AND_DISTRIBUTION_INCOMPLETE',
           'play_last_observation': 'Developer account signup incomplete; no internal release',
           'next_step': 'After pending approval, free Dunsguide account and DUNS request; no paid service'},
    'T6': {'state': 'BLOCKED_OPERATOR_HAS_NOT_IDENTIFIED_HOSTING_PANEL',
           'receipt': 'privacy16_pending.json', 'published_by_this_task': False},
    'blocking_audit': {'recurring_blockers': ['admin credential approval', 'release upload approval',
        'Apple authentication', 'Dunsguide agreement approval', 'hosting destination'],
        'recurrence': 'At least three goal turns, including original order and continuations',
        'independent_work_remaining_now': False, 'requires_user_input_or_external_change': True},
    'server_restarted': False, 'keys_generated_this_turn': False,
}
for path, before in snapshots.items():
    assert path.read_bytes() == before, 'Parallel edit: ' + str(path)
record('goal16_impasse_20260915.json', report, note, before_memory=snapshots[ROOT / 'CLAUDE.md'])
for path in surfaces[1:]:
    before = snapshots[path]
    assert path.read_bytes() == before, 'Parallel edit: ' + str(path)
    backup = path.with_name(path.name + '.bak_' + stamp)
    write_new(backup, before)
    assert backup.read_bytes() == before
    newline = '\r\n' if b'\r\n' in before else '\n'
    append = ('\n\n### 15/09/2026 — Build 16: retorno CIAL e impasse de conclusão\n\n' + note + '\n')
    after = before + append.replace('\n', newline).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    write_new(temp, after)
    assert path.read_bytes() == before, 'Parallel edit: ' + str(path)
    temp.replace(path)
    assert path.read_bytes() == after and len(after) > len(before)
print(json.dumps({'recorded': True, 'receipt': str(WORK / 'goal16_impasse_20260915.json'),
                  'memory_surfaces': len(surfaces), 'byte_backups_verified': True}, ensure_ascii=False))
