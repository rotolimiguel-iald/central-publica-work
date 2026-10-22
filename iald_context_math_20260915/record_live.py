"""Append measured deployment status to every task memory, preserving bytes."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
from record_prepared import TARGETS, create

WORK = Path(__file__).resolve().parent
MARKER = 'IALD_FIXED_NUCLEUS_LIVE_20260915'
NOTE = """[INPUT] O operador respondeu “prossiga” à implantação específica do núcleo, fórmulas, fontes móveis e reinício web. Durante o trabalho pediu orientar testes em grupo iOS/Android e relatou falhas ao identificar o autor/pesquisar; esses pontos foram incorporados.

[REAL — instalado] Sete documentos integrais fixos, leitura a cada chamada, sem corte silencioso. Verificação final mediu 324.352 tokens de contexto, janela 400.000. Autoria explícita: Luiz Antonio Rotoli Miguel. Remissões matemáticas acrescentadas para o Hamiltoniano positivo dos Three Locks (v22, regime finito) e H=-log(rho*) / resistencia_beta, com hipóteses e estatutos. O Atlas original permanece íntegro; registros históricos não são tratados automaticamente como pendências atuais. Catálogo disponível: 1.007 fontes, 1.003 Lean, extraído sem executar um.py; compilação nova não realizada.

[REAL — interface e API] Quatro cópias de iald.js iguais (web, www, iOS, Android), com fórmulas protegidas antes do Markdown e KaTeX seguro. A resposta técnica no navegador apresentou 47 fórmulas, 24 em bloco, zero katex-error. O teste direto de autoria recebeu HTTP 200, 324.211 tokens de entrada e resposta correta com fonte paper_PT.tex. O teste na UI também respondeu o autor e executou search_web (1.637 caracteres retornados), citando https://teoriadagravitacaoluminodinamica.com/entry/. Isso prova busca e resposta no teste, não leitura integral independente dessa página nem acurácia universal.

[REAL — limites e correção] Uma tentativa inicial teve 429; o diagnóstico seguinte mediu 500.000 TPM. Instalado retry apenas para rate_limit_exceeded temporário com prazo informado, até duas repetições/120 s de espera acumulada, mantendo keepalive e cancelamento; sem repetir stream parcial, falta de crédito, request too large ou falha de transporte. Testes: 7 novos, 218 regressões do motor e 3 do núcleo passaram; antes, 31 Python/87 JavaScript da preparação passaram. Cotas, segredos e contas preservados.

[REAL — operação] Reinício somente de filhos do supervisor web 47020. Última conferência: web PID 67884, /health 200; llama PID 34128 preservado. Recibos de instalação e verificações em work/iald_context_math_20260915. Os antigos recibos “restart pending” são retratos intermediários; este adendo registra o reinício concluído.

[OPEN — gasto] A verificação final do Hamiltoniano chegou a consultar kernel e Atlas, mas parou antes da resposta por teto local diário. Configuração lida: global US$1, operador US$1, usuário comum US$0,20; soma global liquidada US$0,852227, insuficiente para reservar outra chamada integral. Não foi falta de crédito comprovada na conta OpenAI. Pergunta enviada para elevar global/operador a US$5/dia, preservando usuários comuns; ainda sem resposta neste registro. Não elevar antes da autorização. Sem essa alteração, renovação diária às 21h de Brasília.

[OPEN — distribuição] Nenhum novo APK/AAB/IPA compilado/publicado nesta etapa. Fontes móveis atualizadas; binários antigos não contêm a nova renderização. Guia TESTES_EM_GRUPO.md preparado: TestFlight externo com análise beta/link e Play teste interno (até100, e-mails/Google Groups); último estado Google ainda aguardava D-U-N-S. Não houve envio de convites a terceiros. TGL=ATLAS; IALD=ÍNDICE(TGL). Núcleo no contexto não altera pesos, não move o gate e não confirma a física.
"""

receipt = WORK / 'runtime_status.json'
if receipt.exists():
    raise RuntimeError('Status receipt exists; append a new correction instead.')
paths = [*TARGETS, WORK / 'REVISAO_DO_NUCLEO.md']
before_all = {path:path.read_bytes() for path in paths}
if any(MARKER.encode() in data for data in before_all.values()):
    raise RuntimeError('Marker already recorded')
now = datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
rows = []
for path,before in before_all.items():
    assert path.read_bytes() == before, 'Concurrent memory edit'
    backup = path.with_name(path.name + '.bak_' + stamp)
    create(backup,before)
    nl = '\r\n' if b'\r\n' in before else '\n'
    addition = '\n\n### ' + now.strftime('%d/%m/%Y %H:%M %z') + ' — Núcleo instalado; autoria e busca verificadas\n\n'
    addition += '<!-- ' + MARKER + ' -->\n\n' + NOTE
    after = before + addition.replace('\n',nl).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    create(temp,after)
    assert path.read_bytes() == before, 'Concurrent memory edit before replacement'
    temp.replace(path)
    assert path.read_bytes() == after and len(after)>len(before)
    rows.append({'path':str(path),'backup':str(backup),'bytes_added':len(after)-len(before),
                 'sha256':hashlib.sha256(after).hexdigest()})
report = {'recorded_at':now.isoformat(),'status':'LIVE_VERIFIED__FURTHER_API_TEST_BLOCKED_BY_EXISTING_DAILY_CAP',
          'memories':rows,'distribution_guide':str(WORK / 'TESTES_EM_GRUPO.md'),
          'new_spending_approval_pending':True,'native_restarted':False,'stores_published':False}
temp = receipt.with_suffix('.tmp')
create(temp,json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8'))
temp.replace(receipt)
print(json.dumps({'status':report['status'],'memories_updated':len(rows),'receipt':str(receipt)}))
