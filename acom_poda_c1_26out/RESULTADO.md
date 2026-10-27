# Poda da projecao ACOM da sessao c1 - 26/10/2026 - RESULTADO: PARADA (nenhuma transicao feita)

Referencia EXATA: C:\IALD\MEMORIA_IALD\sessions\claude-c1_exame-geral-12out.json (context_id a228d32a-518e-548e-998f-e58ddade6bbb). Nenhuma outra referencia, o um.py, o Nos e o MEMORY.md nao foram tocados.

## O que foi medido [REAL, lido por script via session_memory.py get/project/verify]
- Revisao 13, state_sha256 0db791034bd68ded..., 31 records (todos fact/decision/pending, REAL/INPUT), 3 handles (todos completed), 0 candidatos.
- project (max_chars padrao 24000): ProjectionOverflow, obrigatorio = 24373 caracteres; estouro de 373.
- Composicao (chars): objetivo 229 | restricoes 701 | fluxo p 460 (phase 98, next_action 166, 3 handles 161) | recibo 505 | records 21887 (no formato da projecao; 22533 pela soma de json.dumps por registro). Os 16 records de v394 a v401 (preparada, seladas, bancada) pesam 13876 chars em JSON.

## Por que NAO ha poda legitima para esta referencia [REAL, codigo lido]
1. lib/iald_memory/store.py (project_snapshot): so `candidate` e omissivel; todo fact/decision/contradiction/pending/erratum e obrigatorio, junto com a cadeia `supersedes`. Records sao imutaveis (id nao se reusa; sem delete). Uma "consolidacao" por supersedes ou nova entrada AUMENTA o obrigatorio (original + correcao formam unidade inseparavel).
2. A PODA de E2/E3 (terminal_handles, terminal_build_records) existe so em lib/iald_memory/mission.py e so na projecao de MISSAO (mission_cli.py project). Esta referencia nao e missao (mission_cli project -> MissionError mission_not_initialized); alem disso E3 indexa apenas records `track-build-...` com recibo pinado, e os records v394-v401 sao selos de versao (fatos materiais), nao acompanhamento mecanico. Os 3 handles terminais somam 161 chars.
3. O unico material reduzivel por transicao e flow.phase/next_action/status dos handles. Simulacao offline (store.project_snapshot sobre copia em memoria) com o minimo absoluto (phase="x", next_action="", handles "done", event_id curto): 24070 chars, ainda 70 acima de 24000, e destruiria a proxima acao viva. Por isso NAO apliquei nada.

## Provas de que nada foi perdido / nada mudou
- get antes e get depois: identicos (rev 13, state_sha256 0db791034bd68ded, 31 records, 3 handles); verify ok (event_count 14). Nenhum transition executado. Copia do get inicial: scratchpad get_before.json (nao versionada).

## O orcamento e configuravel (sem tocar no estado)
- Campo `max_chars` do JSON de entrada de `project` (session_memory.py linha 225: request.get("max_chars", 24000); validado em store.project_snapshot: inteiro 256..33554432). Tambem em mission_cli/MCP (MISSION_PROTOCOL.md: "passe max_chars explicito, ex.: 100000").
- Medido: max_chars 25000, 32000 e 100000 -> project OK (actual 24373, overflow false, 0 omitidos, rev 13). 24000 e o padrao -> overflow.
- Crescimento: cada versao selada custa ~1.8 mil chars (selada + bancada); 32000 estoura em ~4 versoes.

## Saidas que dependem de decisao da gerencia/operador (nao feitas por mim)
A. Passar `max_chars` (ex.: 100000) nas chamadas `project` de c1 (o bloco SESSION_BRIDGE/CLAUDE.md global chama sem max_chars; alterar o texto e ato do dono desses arquivos).
B. Rolar a sessao: nova inscricao (init) com parent_id=a228d32a... e um resumo de abertura; os 31 records ficam no pai (get/diario), o filho comeca magro. Cria nova referencia (decisao).
C. Mudanca de codigo em store.project_snapshot (marca de encerrado/indice para records de sessao, analogo a E3) com backup, testes e revisao independente.
