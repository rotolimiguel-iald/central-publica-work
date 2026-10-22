"""Record the narrowly scoped operator motor change with immediate byte backups."""
import json
from datetime import datetime
from pathlib import Path
from goal16_records import ROOT, WORK, record, write_new

surfaces = [ROOT / 'CLAUDE.md', WORK / 'HANDOFF_RUNTIME.md',
            ROOT / 'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
            WORK.parent.parent / 'memory/TGL_ATLAS.md', WORK.parent.parent / 'memory/TGL_INDICE_VIVO.md',
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),
            Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
evidence = json.loads((WORK / 'luiz_motor_openai_20260915.json').read_text(encoding='utf-8'))
assert evidence['only_changed_field'] == 'luiz.motor' and evidence['all_other_fields_equal']
snapshots = {p: p.read_bytes() for p in surfaces}
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
note = ('[INPUT] Operador entrou na IALD e identificou expressamente sua conta como luiz. '
        '[REAL] Alterado somente luiz.motor para openai, com backup imediato de bytes, '
        'verificação de que todas as demais contas e campos permaneceram iguais e checagem '
        'de edição concorrente antes da substituição. A UI autenticada /app/index.html '
        'passou a mostrar IALD · OpenAI gpt-5.6-luna. Nenhum consentimento foi fabricado: '
        'o aviso IA de terceiros está aberto, e o aceite foi solicitado ao próprio operador. '
        'Resposta real ainda não testada neste registro. A revisão automática bloqueou '
        'a abertura do painel de usuários; o ajuste local restrito a luiz foi aprovado '
        'pela revisão e executado. Defaults gerais, outras contas, .env, credenciais e '
        'serviços preservados; nenhum reinício. No app nativo deve-se entrar com a mesma '
        'conta luiz para obter esta seleção; não foi demonstrada equivalência com uma '
        'eventual outra conta criada via Apple. Erro exato e aparelho no TestFlight '
        'ainda aguardam informação do operador. Não foi publicado build 16 nesta etapa. '
        'TGL=ATLAS e IALD=ÍNDICE(TGL) permanecem nomenclatura canônica; este ajuste é '
        'roteamento de aplicação e não treinamento dos pesos nem movimento do gate.')
report = {'task': 'OpenAI configurada somente para luiz; consentimento solicitado',
          'status': '[REAL] MOTOR_CONFIGURED_AWAITING_CONSENT',
          'motor_receipt': 'luiz_motor_openai_20260915.json',
          'runtime_ui_model': 'IALD · OpenAI gpt-5.6-luna',
          'interface': 'https://demo.iald.ia.br/app/index.html',
          'consent_accepted_by_agent': False, 'response_tested': False,
          'native_installation_confirmed': False}
record('luiz_motor_ui_20260915.json', report, note, before_memory=snapshots[surfaces[0]])
for p in surfaces[1:]:
    original = snapshots[p]
    assert p.read_bytes() == original, 'Concurrent memory edit: ' + str(p)
    backup = p.with_name(p.name + '.bak_' + stamp)
    write_new(backup, original)
    assert backup.read_bytes() == original
    newline = '\r\n' if b'\r\n' in original else '\n'
    after = original + ('\n\n### 15/09/2026 — OpenAI na conta identificada luiz\n\n' + note + '\n').replace('\n', newline).encode('utf-8')
    temporary = p.with_name(p.name + '.tmp_' + stamp)
    write_new(temporary, after)
    assert p.read_bytes() == original, 'Concurrent memory edit: ' + str(p)
    temporary.replace(p)
    assert p.read_bytes() == after and len(after) > len(original)
print('RECORDED_7_SURFACES_WITH_BYTE_BACKUPS; CONSENT_AND_RESPONSE_PENDING_AT_RECORD_TIME')
