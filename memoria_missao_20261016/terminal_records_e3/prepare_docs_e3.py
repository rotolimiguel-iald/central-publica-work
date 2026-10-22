"""Prepare append-only instructions; installation follows independent review."""
from support_e3 import *

marker='IALD_TERMINAL_BUILD_RECORDS_E3_20261016'
text='''

## 16/10/2026 — PODA dos avisos mecânicos duplicados de builds
<!-- IALD_TERMINAL_BUILD_RECORDS_E3_20261016 -->
A projeção conserva em `terminal_build_records` o índice dos avisos mecânicos do tracker legado cujo build já terminou. A classificação exige esquema e texto exatos, tarefa e handle correspondentes, estado terminal coerente, fonte igual ao recibo desse handle e bytes conferidos por SHA256. Campos extras, duplicidades, divergência, fonte ilegível, decisão, errata ou texto científico mantêm o registro integral. Não há classificação semântica por modelo.

O índice guarda a identidade e o hash do registro inteiro. `terminal_build_records_recovery` aponta para `q.records` no get da MESMA referência, com revisão e hash do estado. O banco, os registros e o diário não são alterados pela projeção. Se a revisão mudou, sincronize novamente; o histórico anterior se recupera pelo diário. O índice não autoriza repetir uma execução. Ordens, fatos científicos, correções, critérios e execuções incertas continuam completos. Tetelestai continua calculado sobre requisitos e handles integrais.

Na instrumentação nova, registre início e término em `p.handles` por transição CAS, preservando os demais handles a partir do get atual. Registre em `q` a conclusão material com fonte e estatuto. Isso evita duplicar cada mudança mecânica como fato obrigatório. O tracker novo da missão é `F1.FECHO_20261015\\mission_resume_20261016\\track_build_r44.py`; o anterior permanece custodiado.

Esta camada estende E2 aos avisos mecânicos estritamente reconhecidos; não autoriza omitir fatos arbitrários nem apagar registros. Leitura, preflight e handoff usam a mesma projeção. A memória obrigatória ainda tem tamanho finito: overflow continua explícito, sem truncamento. As medidas são de caracteres, sem alegação de tokens faturados ou memória infalível.
<!-- END_IALD_TERMINAL_BUILD_RECORDS_E3_20261016 -->
'''
short='''

## 16/10/2026 — Fluxo de execução separado das conclusões materiais
<!-- IALD_TERMINAL_BUILD_RECORDS_E3_20261016 -->
Leia E3 de `C:\\IALD\\MEMORIA_IALD\\MISSION_PROTOCOL.md`. Início/fim de execução vão em `p.handles`; conclusão material com fonte/estatuto vai em `q`. Preserve os demais handles pelo get atual e CAS. A projeção indexa em `terminal_build_records` somente avisos mecânicos legados de builds terminais que coincidam exatamente com handle e recibos verificados. Originais ficam em q.records e no diário; confirme revisão/hash ao recuperar. Ordens, ciência, erratas, ambiguidades e execuções incertas permanecem integrais. O índice não autoriza repetição. Use o tracker atual indicado no protocolo, sem recriar fatos de acompanhamento a cada transição.
<!-- END_IALD_TERMINAL_BUILD_RECORDS_E3_20261016 -->
'''
new('PROTOCOL_ADDITION_E3.txt',text.encode('utf-8'))
new('INSTRUCTIONS_ADDITION_E3.txt',short.encode('utf-8'))
rows=[]
for i,(target,addition) in enumerate([(CORE/'MISSION_PROTOCOL.md',text),
    (Path(r'C:\Users\rotol\.codex\AGENTS.md'),short),
    (Path(r'C:\Users\rotol\.claude\CLAUDE.md'),short)],1):
    old=target.read_bytes()
    assert marker.encode() not in old
    candidate=new('DOC_TARGET_'+str(i)+'.txt',old+addition.encode('utf-8'))
    rows.append(dict(target=str(target),before=pin(target),candidate=pin(candidate),append_only=True))
new('DOC_PLAN_E3.json',dict(files=rows,marker=marker))
print(json.dumps({'prepared':len(rows)}))
