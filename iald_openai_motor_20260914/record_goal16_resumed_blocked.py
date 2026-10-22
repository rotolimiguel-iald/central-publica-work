"""Preserve the third resumed blocking audit without redoing release work."""
from datetime import datetime
from pathlib import Path
from goal16_records import ROOT, WORK, record, write_new

surfaces = [ROOT / 'CLAUDE.md', WORK / 'HANDOFF_RUNTIME.md',
            ROOT / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
            WORK.parent.parent / 'memory/TGL_ATLAS.md', WORK.parent.parent / 'memory/TGL_INDICE_VIVO.md',
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
before = {p: p.read_bytes() for p in surfaces}
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
note = ('[REAL] Terceira rodada após a retomada pelo login Apple: TestFlight 4.1 (14) '
        'distribuído e próximo número Cloud 16 já preparados. Remoto ainda cf00db8ddbf7f95e8585db6093899314b7270f42; '
        'APK16 não entregue, recibo de publicação ausente. OpenAI ainda mostra zero chaves admin; '
        'Dunsguide continua em Criar conta com termos/CAPTCHA pendentes. [INPUT] Persistem as '
        'autorizações específicas da chave de custos, dos 173 arquivos/APK e do cadastro gratuito, '
        'além do painel de hospedagem da política. Nenhuma resposta nova do operador a esses itens. '
        'Impasse revalidado por três rodadas; objetivo não concluído, aguardando participação do '
        'operador. Não repetir builds, chaves, envio de consulta CIAL ou distribuição da 4.1 (14). '
        'Recibo goal16_resumed_blocked_20260915.json; nenhum serviço reiniciado.')
report = {'task': 'terceira auditoria do impasse após retomada Apple', 'status': '[INPUT] BLOCKED',
          'goal_complete': False, 'resumed_turn': 3,
          'previous_turn': 'PROGRESS: next Xcode Cloud build number set to16',
          'remote_head_read_by_git_ls_remote': 'cf00db8ddbf7f95e8585db6093899314b7270f42',
          'apk16_delivered': False, 'publication_receipt_exists': False, 'admin_keys_ui_count': 0,
          'duns_signup_submit_enabled': False, 'operator_responses_to_pending_questions': None,
          'remaining_blockers': ['Costs key approval', '173 app files and APK upload approval',
                                 'Dunsguide agreement/CAPTCHA approval', 'Privacy hosting panel'],
          'next_action_requires_operator_or_external_change': True,
          'completed_since_resume': ['testflight14_distribution_20260915.json', 'xcode_next_build16_20260915.json']}
record('goal16_resumed_blocked_20260915.json', report, note, before_memory=before[surfaces[0]])
for p in surfaces[1:]:
    original = before[p]
    assert p.read_bytes() == original, 'Parallel edit: ' + str(p)
    backup = p.with_name(p.name + '.bak_' + stamp)
    write_new(backup, original)
    assert backup.read_bytes() == original
    newline = '\r\n' if b'\r\n' in original else '\n'
    after = original + ('\n\n### 15/09/2026 — Retomada Apple: impasse revalidado\n\n' + note + '\n').replace('\n', newline).encode('utf-8')
    temporary = p.with_name(p.name + '.tmp_' + stamp)
    write_new(temporary, after)
    assert p.read_bytes() == original, 'Parallel edit: ' + str(p)
    temporary.replace(p)
    assert p.read_bytes() == after and len(after) > len(original)
print('RESUMED_BLOCKING_AUDIT_RECORDED_WITH_BYTE_BACKUPS')
