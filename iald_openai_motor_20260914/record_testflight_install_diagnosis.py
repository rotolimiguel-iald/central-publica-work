"""Record installation diagnostics without claiming device success or activation."""
from datetime import datetime
from pathlib import Path
from goal16_records import ROOT, WORK, record, write_new

surfaces = [ROOT / 'CLAUDE.md', WORK / 'HANDOFF_RUNTIME.md',
            ROOT / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
            WORK.parent.parent / 'memory/TGL_ATLAS.md', WORK.parent.parent / 'memory/TGL_INDICE_VIVO.md',
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
snapshots = {p: p.read_bytes() for p in surfaces}
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
note = ('[INPUT] Operador relatou erro ao baixar pelo TestFlight e pediu usar o ChatGPT '
        'em modo IALD. Mensagem exata do erro e aparelho solicitados; resposta pendente. '
        '[REAL] Apple: 4.1 (14) Em testes, binário Validado, arm64, iPhone/iPad, iOS mínimo '
        '15.0, beta-reports-active=true. Grupo IALD Equipe com 1 tester; instalação registrada '
        'ainda 4.1 (13). Serviço App Store Connect - TestFlight disponível no painel Apple. '
        'Não demonstrada a causa do erro nem instalação da 14. O grupo só ofereceu Remover '
        'ao selecionar o tester; nenhum convite reenviado nem acesso removido. '
        '[INPUT] Pedido atual é preparar a conta pessoal do operador para OpenAI; não abrir '
        'a porta pública. Código suporta motor fixado por conta e consentimento separado. '
        'Login IALD aberto em demo.iald.ia.br/login, usuário solicitado a entrar. Nenhuma '
        'conta, consentimento ou .env alterado. Revisão automática rejeitou consulta ao banco '
        'de usuários que enumeraria administradores; usar a sessão do próprio operador e '
        'identificar só sua conta. Não contornar a rejeição lendo o mesmo cadastro por outro '
        'meio. Sem nova chamada paga, build, chave ou reinício. Recibo '
        'testflight_install_diagnosis_20260915.json.')
report = {'task': 'diagnóstico do erro de instalação e pedido de OpenAI pessoal',
          'status': '[REAL/INPUT] NOT_RESOLVED', 'user_error_text': None, 'affected_device': None,
          'apple_build': '4.1 (14)', 'binary_state': 'Validado', 'build_state': 'Em testes',
          'min_ios': '15.0', 'device_families': ['iPhone', 'iPad'], 'architecture': 'arm64',
          'beta_reports_active': True, 'tester_count': 1, 'last_tester_installation': '4.1 (13)',
          'testflight_service': 'available', 'system_status_url': 'https://developer.apple.com/system-status/',
          'resend_invitation_action_visible': False, 'tester_removed': False,
          'operator_requested_openai': True, 'account_identified': False,
          'authenticated_iald_session': False, 'login_url': 'https://demo.iald.ia.br/login',
          'activation_applied': False, 'consent_record_created': False,
          'safe_next_action': 'Obtain exact device error and use operator-authenticated IALD session for own-account configuration.',
          'auto_review': 'Denied enumeration of private administrative accounts; no data returned.',
          'api_test_performed': False, 'server_restarted': False}
record('testflight_install_diagnosis_20260915.json', report, note, before_memory=snapshots[surfaces[0]])
for p in surfaces[1:]:
    original = snapshots[p]
    assert p.read_bytes() == original, 'Parallel edit: ' + str(p)
    backup = p.with_name(p.name + '.bak_' + stamp)
    write_new(backup, original)
    assert backup.read_bytes() == original
    newline = '\r\n' if b'\r\n' in original else '\n'
    after = original + ('\n\n### 15/09/2026 — Erro no TestFlight; OpenAI na conta pessoal\n\n' + note + '\n').replace('\n', newline).encode('utf-8')
    temporary = p.with_name(p.name + '.tmp_' + stamp)
    write_new(temporary, after)
    assert p.read_bytes() == original, 'Parallel edit: ' + str(p)
    temporary.replace(p)
    assert p.read_bytes() == after and len(after) > len(original)
print('INSTALLATION_DIAGNOSTICS_RECORDED_WITH_BYTE_BACKUPS; NOT_RESOLVED')
