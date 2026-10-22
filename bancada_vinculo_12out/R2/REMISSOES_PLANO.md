# As duas remissões que faltam no PLANO_V392.md (texto a inserir; o plano NÃO foi editado aqui)

Achado documental da auditoria independente (AUDITORIA_VINCULO_BANCADA_C1.md, §1 e §6(d), 13/10/2026): o bloco «12-bis» foi colado inteiro no `PLANO_V392.md` (a partir da l.529), mas as duas remissões prometidas — uma na §3 (etapa 1) e uma na §14 (atos do operador) — **não** foram inseridas nos seus lugares; «12-bis» só aparece dentro do próprio bloco colado (l.521/529/541). Abaixo, o texto exato de cada remissão e o lugar onde entra. Quem edita o plano é a gerência c1 (backup de bytes antes; append ao lado, nunca por cima).

Estatutos: [DERIVED] composto a partir do desenho (`VINCULO_BANCADA_UMPY.md`) e do bloco 12-bis já colado; [REAL] onde diz «R2» e cita hash. Nada aqui move o gate.

---

## Remissão 1 — na §3 («Etapa 1: os testes finais da Bancada (antes do selo, contra a v391)»)

**Onde entra:** logo depois do item 5 da §3 («A v392 **lê esses recibos por hash e nunca recalcula** …») e antes da frase «Não há ato do operador nesta etapa», como bloco «⚠ R3, ao lado».

**Texto:**

> ⚠ **R3, ao lado (13/10/2026) — remissão ao §12-bis.** Os «testes finais da Bancada» desta etapa rodam por **`sincronizar_bancada.py --modo ensaio --fase pre_selo --versao v391 --bancada C:\IALD\Bancada_Um --producao`** (R2 do esboço, `work\bancada_vinculo_12out\R2\`; a R1 foi reprovada pela auditoria de 13/10 e fica como registro), em **raiz curta** (`C:\t\…` ou `work\…`, por causa do T16) e com `python -B`: a bateria inteira (`R2\BATERIA_VINCULO.json`, pinada por `--bateria-sha256` e por teste), T12–T14 incluídos, contra a v391 ainda canônica, e deixa o **`RECIBO_SINCRONIZACAO_v391_<stamp>.json`** («JA_SINCRONIZADA__ENSAIO…») **que o B(3) do §12-bis exige por hash e por identidade** (`--recibo-pre-selo`: versão anterior, um.py antes pinado, mesma Bancada). O T17 não corre aqui: entra no B(3) pelo recibo do build do kernel da etapa 2 (`KERNEL_RECIBO_v392.json`: `versao`, `rc`, `sorry`, `build_full_log_sha256`), nunca recompilado na Bancada. Os recibos desta etapa vão ao cache do rito como o item 4 já diz. O que não muda: nenhum ato do operador nesta etapa; nenhum dado observado; o gate.

---

## Remissão 2 — na §14 («O que depende de ato seu, em ordem»)

**Onde entra:** na tabela da §14, logo abaixo da linha «| depois do selo | **B3**: autorizar a re-pinagem da Bancada | sem a B3, a Bancada recusa tudo |», como linha nova marcada «⚠ R3».

**Texto (uma linha da tabela):**

> | ⚠ R3 (13/10) · depois do selo | **B3, agora como passo nomeado da cadeia (§12-bis):** autorizar a gerência a executar `sincronizar_bancada.py --modo aplicar --producao --fase pos_selo --versao v392 --evento <seq> --recibo-pre-selo <etapa 1> --kernel-recibo <etapa 2> --bateria-sha256 <vNNN_pins>` sob **evento c1** `SINCRONIZACAO_BANCADA` (verificado pela cadeia de hash do `eventos.jsonl`, com versão, Bancada, um.py e selo nomeados por JSON), com o **serviço parado** (quiesce → parada com recibo) e, depois, o **religamento do `um_bancada.py` com recibo de identidade** e a **reconexão dos adaptadores MCP** das sessões (passo 10-ter). Consequência a dizer-lhe por inteiro: **sem a sua palavra para a B3, a cadeia da v392 para em 10-bis (`AGUARDA_OPERADOR`) e o fechar, o handoff e a custódia (§13) não acontecem** — é o que o desenho §5 quer, e tem de estar dito. Da v393 em diante, se o senhor assim decidir, o B(n) corre sob a ordem permanente de 12/10 (`78ef70e6f9868281`) com evento c1 e veto preservado | sem a B3: a Bancada recusa toda operação científica (`PIN_CHANGED`, provado), e a custódia da v392 espera |

---

## Ressalva documental, para a mesma edição (a corrigir ao lado, não por cima)

O bloco colado no plano a partir da l.529 traz o cabeçalho «Parágrafo a acrescentar ao PLANO_V392.md (só o texto; o plano não foi editado)» — frase agora falsa dentro do próprio plano. Conserto proposto: uma linha «⚠ R3: este cabeçalho era do rascunho (`work\bancada_vinculo_12out\PLANO_V392_paragrafo_B3.md`, `54134728176b45dd`); o bloco foi colado em 12/10 e as remissões entraram em 13/10» ao lado do cabeçalho, sem apagar nada. E no item 1 do 12-bis, onde o comando do B(n) omite `--recibo-pre-selo`, `--kernel-recibo` e `--bateria-sha256` (ressalva (b) da auditoria, §6), acrescentar ao lado: «(R2: obrigatórios em `aplicar` fora do sandbox; ver §5 do desenho)».

Nada aqui é leitura física; NOT_FALSIFIED nunca é creditação.
