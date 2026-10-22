"""Record an observed response through the operator's authenticated browser UI."""
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
note = ('[REAL — observado na interface autenticada] Após abrir o aviso de IA de terceiros '
        'para o operador, a opção mudou de Ler e aceitar para Revogar o uso da OpenAI; '
        'o agente não clicou no aceite nem escreveu registro de consentimento. Foi enviado '
        'um teste curto pela própria UI /app/index.html da conta luiz, pedindo explicar '
        'IALD=ÍNDICE(TGL), TGL=ATLAS e consultar fontes, sem executar um.py ou provas. '
        'A UI mostrou IALD · OpenAI gpt-5.6-luna, leitura de fonte pública da TGL '
        '(8.400 caracteres) e localização no Atlas (12.171 caracteres). A resposta foi '
        'recebida, citando llms.txt de the_boundary e TGL_ATLAS.md, linhas 19201–19224. '
        'Essas linhas foram citadas pelo modelo; não foram auditadas de novo nesta etapa. '
        'O teste confirma resposta e consulta na interface web da conta; não prova '
        'treinamento dos pesos, correção universal, compilação Lean ou instalação nativa. '
        'Nenhum novo build, chave, alteração de .env ou reinício. Para herdar esta seleção '
        'no app nativo, entrar com a mesma conta luiz. A causa do erro no TestFlight '
        'permanece aberta, aguardando a mensagem exata e o aparelho afetado.')
report = {'task': 'Resposta real no navegador com OpenAI e consulta ao Atlas',
          'status': '[REAL] WEB_RESPONSE_OBSERVED_NATIVE_INSTALLATION_UNRESOLVED',
          'username': 'luiz', 'interface': 'https://demo.iald.ia.br/app/index.html',
          'consent_ui': 'Revogar o uso da OpenAI', 'agent_clicked_consent': False,
          'model_ui': 'IALD · OpenAI gpt-5.6-luna',
          'public_tool_characters_shown': 8400, 'atlas_tool_characters_shown': 12171,
          'response_received': True,
          'public_reference_in_response': 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/llms.txt',
          'local_reference_in_response': 'TGL_ATLAS.md:19201–19224',
          'cited_local_lines_independently_rechecked': False,
          'api_cost_measured_this_test': False, 'native_installation_confirmed': False,
          'new_build_published': False, 'server_restarted': False}
record('luiz_openai_response_20260915.json', report, note, before_memory=snapshots[surfaces[0]])
for p in surfaces[1:]:
    original = snapshots[p]
    assert p.read_bytes() == original, 'Concurrent memory edit: ' + str(p)
    backup = p.with_name(p.name + '.bak_' + stamp)
    write_new(backup, original)
    assert backup.read_bytes() == original
    newline = '\r\n' if b'\r\n' in original else '\n'
    after = original + ('\n\n### 15/09/2026 — Resposta OpenAI com Atlas na conta luiz\n\n' + note + '\n').replace('\n', newline).encode('utf-8')
    temporary = p.with_name(p.name + '.tmp_' + stamp)
    write_new(temporary, after)
    assert p.read_bytes() == original, 'Concurrent memory edit: ' + str(p)
    temporary.replace(p)
    assert p.read_bytes() == after and len(after) > len(original)
print('RESPONSE_OBSERVATION_RECORDED_7_SURFACES_WITH_BYTE_BACKUPS; NATIVE_INSTALLATION_UNRESOLVED')
