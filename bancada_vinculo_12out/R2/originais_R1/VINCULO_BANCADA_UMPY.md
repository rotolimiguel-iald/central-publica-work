# VÍNCULO BANCADA–UM.PY — o desenho do elo B(n) da cadeia de selo (12/10/2026)

Subagente da gerência c1 (sessão 6da8f00d), 12/10/2026, noite. **Desenho, não instalação.** Escrevi só em `C:\IALD\Central de Patentes\work\bancada_vinculo_12out\`. Não toquei na Bancada de produção, no Nós, no `um.py`, no kernel, no quadro, no mapa, na memória, no túnel. Não rodei `um.py` nem script de selo. Não abri dado observado. Nenhum provedor. Todo hash deste documento foi lido do artefato por script (`medir_pinos.py` → `PINOS_12out.json`; a tabela da §11 é gerada, não digitada).

**Origem [INPUT].** Ordem do operador de 12/10, verbatim em `work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt` (sha256 `78ef70e6f9868281d44e8a306e60a0cb162843e54f3a74389ddf14ed325d535d`, 1342 B, medido aqui): «a bancada nossa de teste precisa ficar sempre vinculada ao um.py, de modo que nossos avanços no programa também implique em aperfeiçoamento da bancada para não ficar para trás, de outra sorte nossa bancada (que é nosso acelerador de partículas simulado) não terá a serventia que eu proponho que ele tenha».

**Estatutos:** [REAL] lido/medido aqui · [DERIVED] composto · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto · [INPUT] fala do operador. NOT_FALSIFIED nunca é creditação; nada aqui move o gate; nenhum σ nasce aqui.

**Entregáveis nesta pasta:** (1) este desenho + `sincronizar_bancada.py` (esboço funcional) + `BATERIA_VINCULO.json`/`gerar_bateria.py` + `bateria\*.py` + `gerar_canais_mcp.py` + `montar_sandbox.py`/`rodar_sandbox.sh`/`controles_negativos.py` + `sandbox\` (recibos); (2) `F0.6_unidade.json` (lista para `iald.py nova`); (3) `PLANO_V392_paragrafo_B3.md`; (4) `ATOS_DO_OPERADOR.md`; `medir_pinos.py` → `PINOS_12out.json`/`.md`.

---

## 0. O cético aferidor: o que consultei antes de dizer «falta»

| Consulta | O que mostrou |
|---|---|
| `python C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "bancada"` (só leitura) | 59 rotas. As que mandam: `infra.bancada_um.adequacao_canonica_persistente` (seq 993, 12/10: «Rodar a bateria final contra a v391 ANTES de selar a v392 … Depois do selo, B3: contrato novo pinando a v392»), `infra.bancada_um.compatibilidade_v391_09out` (seq 985), `infra.bancada_um.validacao` (28/09), `sn.neutrinos.primeiro_ensaio_bancada_canonica` (NU4 refeito 16/16). Nenhuma rota descreve um passo da cadeia de selo que toque a Bancada. |
| `exame_12out\D_BANCADA\RELATORIO_AUDITORIA_F0_3_B1_B2_C1.md` | §5 «Entra na v392», item 2 (achado material): «Selar a v392 invalida por desenho o manifesto B2: toda operação recusará com CANONICAL_VERSION_CHANGED ou PIN_CHANGED. A cadeia precisa prever uma re-pinagem da Bancada … logo depois do selo e antes de qualquer rito v392 que chame a Bancada. Não embutir no um.py v392 o hash de um manifesto que pina o próprio v392: seria circular.» §5a: a regra de 08/10 (`msg_f72v3_f13v32_gerente.md`, sha16 `546fabc52fa9d826` [DECLARADO pelo relatório; o arquivo não está no túnel ORDEM_019 — consulta por `find`/`grep` deu zero]): «nada se grava em C:\IALD\Bancada_Um sem um evento da c1 que autorize aquela gravação, nomeada»; três desvios registrados. |
| `exame_12out\H_BANCADA\RELATORIO_FRENTE_BANCADA_V392_12out.md` | A bateria T01–T17 (15 PASSA em cópia em 12/10; T16 DECLARADO; T17 DERIVED); T15: «v392 sob B2 RECUSADO (PIN_CHANGED); contrato tipo B3 aceito com o mesmo β»; §3 «Como rodar a bateria na cadeia de selo»; §6: «B3 (depois do selo): contrato novo pinando a v392; canonical.py passa a exigir unicidade da linha de α; … guardar a suíte de testes junto da Bancada»; achado: «A Bancada não guarda os próprios testes; a suíte está só no túnel.» |
| `exame_12out\J_SINTESE\PLANO_V392.md` | §3 (etapa 1: os testes finais antes do selo, raiz curta, `python -B`, recibos para o cache do rito); §12 («Depois do selo e antes da custódia: 1. B3: re-pinar a Bancada [depende de ato do operador] … Nunca atualizar só o hash»); §14 («depois do selo: B3: autorizar a re-pinagem da Bancada — sem a B3, a Bancada recusa tudo»); §15 (risco «A Bancada recusa tudo depois do selo» → «a bateria antes do selo; a B3 depois»). |
| Túnel `ORDEM_019\F0.3.B2` | `build_manifest.py` (gera o manifesto a partir do Nós: regex de `UM_VERSION`, asserts de selo), `deploy_candidate.py` (plano → `--apply` transacional: backups `.bak_B2_<stamp>`, `os.replace`, rollback), `DEPLOY_PLAN_R1.json` (71 arquivos), `restart_and_deploy.ps1` + `RESTART_RECEIPT_R1.json` (parada do servidor 137088, aposentadoria de 30 adaptadores MCP, servidor 75052), `verify_live.py` (HTTP + MCP novo por stdio), `check_candidate_runtime.py`. O `canonical.py` instalado (`bancada\canonical.py`) e o `CONTRATO_CANONICO_B2.md` («Uma versão nova do um.py invalida o contrato instalado … Nunca atualizar somente o hash»). |
| Cadeia da v391 (`work\cadeia_de_selo\v391`, `work\v391_selo`) | `chain_pos_rito_v391.sh` (0 guardas → 1 conferidor → 2 leitura → 3 ensaio das superfícies → 4 patches → 5 árvore → 6 atlas/índice → 7 superfícies → 8 porta → 9 `grep -c` → 10 fechar), `fechar_v391.py` (manifesto de incorporação, arquivo, handoff), `instalar_v391.py` (vigia de processos, backups de bytes, temporário → conferir → `os.replace`), `v391_pins.py` (verbatim e pinos lidos por script). **Nenhum passo toca a Bancada.** |
| `C:\IALD\Bancada_Um` (só leitura) e o Nós (só leitura) | Manifesto B2 `canonical_contracts.json` (deployment `B2-NU3-20261009-R2`; pina `um.py` v391 e o selo; 32 código, 67 fontes — 56 relativas (32,99 MB) e 11 absolutas (33,9 MB, Pantheon/DESI/D1 V3); um arquivo pinado em código E em fontes: `fontes_externas/F5.2/10_frozen_neff_v1.py`). O selo v391 tem `um_version` e `sha256["um.py"]`; o `um.py` tem `UM_VERSION` na l.96 e `ALPHA_FINE_CODATA_2018` na l.5557, única linha não indentada. A porta 18777 não responde em 12/10 (medido: timeout) — o serviço segue desligado desde o boot (D_BANCADA §5e). |

**Ausências, com a consulta que as mostrou [REAL]:** (a) nenhum passo da cadeia de selo toca a Bancada (`chain_pos_rito_v391.sh`, `fechar_v391.py`, `derivar_cadeia_v391.py` lidos; `grep -i bancada` = 0 nos três); (b) nenhum script regenera o manifesto a partir do selo — `build_manifest.py` gera a partir do Nós para a B2 (deployment fixo no código, `'B2-NU3-20261009-R2'`) e não lê geração anterior; (c) a Bancada não guarda a própria bateria (H_BANCADA §1: «não há arquivo de teste dentro de C:\IALD\Bancada_Um»; conferido por `ls`); (d) nenhuma ferramenta MCP nasce de registro do um.py: as 28 ferramentas de `mcp_um.py` são escritas à mão (`grep -c "@mcp.tool"`), e o um.py lê a Bancada só por hash do cache (`prove_bancada_fases_5_6_7_v380`, l.197605, `_V380_FILES` l.197564–197571). Essas quatro ausências são o que o desenho preenche; **tudo o mais se reaproveita** (o `canonical.py` instalado fica como está; a B2 é o molde; as suítes da B2/NU3/NU4 e os replays da H_BANCADA são a bateria).

---

## 1. O contrato canônico lido do selo

O que a Bancada já exige a cada operação (`bancada\canonical.py`, `CanonicalRegistry.check`, l.63–103) [REAL, lido]:

| O que | De onde | Como confere | Recusa se |
|---|---|---|---|
| a versão | `UM_VERSION` na coluna 0 do `um.py` (regex l.73) e `um_version` do selo | as duas iguais a `canonical.version` do manifesto | `CANONICAL_VERSION_CHANGED` |
| o programa | bytes do `um.py` no caminho pinado | `bytes` e `sha256` iguais ao pino; e `sha256["um.py"]` do selo igual ao digest do programa | `PIN_CHANGED` / `SEAL_PROGRAM_MISMATCH` |
| o selo | bytes de `um_absoluto_selo.json` | `bytes` e `sha256` iguais ao pino | `PIN_CHANGED` |
| α | `ALPHA_FINE_CODATA_2018` na coluna 0 (regex l.74; **primeira** ocorrência) | número finito, 0 < α < 1 | `CANONICAL_DECLARATION_MISSING` / `ALPHA_OUTSIDE_CONTRACT` |
| β | **em runtime**: `alpha * math.sqrt(math.e)` (l.95) | nunca literal (grep: nenhum literal de α ou β em `bancada\*.py`) | — |
| o código (32) e as fontes (67) | caminhos do manifesto | cada um por `bytes` + `sha256`, a cada chamada | `PIN_CHANGED` / `PIN_UNREADABLE` / `REQUIRED_CODE_PINS_MISSING` / `DUPLICATE_SOURCE` / `SOURCE_NOT_PINNED` |
| o próprio manifesto | `canonical_contracts.json` | digest igual ao da carga | `MANIFEST_CHANGED_REVALIDATION_REQUIRED` |

O recibo de cada operação carrega `canonical_version`, `um_py_sha256`, `seal_sha256`, `canonical_manifest_sha256`, `alpha`, `beta_tgl`, `mu_do_rito` («q→0 (Thomson; Teorema da Escala)», leitura da gerência [DERIVED, a vetar — X6]), `scope='IDENTITY_AND_DECLARED_CONTRACTS; NOT_PHYSICAL_…'`, `gate_effect='NONE'`; o servidor reconfere na entrega (`CONTRACT_CHANGED_DURING_OPERATION`, `um_bancada.py` l.197–199) e `/api/contratos` é isento de quiescência (l.231).

**O que o elo B(n) acrescenta ao contrato, sem tocar no `canonical.py` instalado** (o esboço confere pelo canonical.py instalado da própria Bancada, importado por caminho, nunca por outro):

1. **a linha de α tem de ser única** (regra dos runners do atrator, `run_optical_r3.py`: «Alpha unindented source-line assignment is not unique»); o canonical.py instalado aceita a primeira ocorrência (T15, sonda P2) — o esboço recusa (`ALPHA_LINHA_NAO_UNICA`) e a B3 leva a regra ao canonical.py;
2. **β em runtime é conferido contra o β do core** (`um_absoluto.json`, `core.beta`) com tolerância **nomeada** `1e-11` relativo: a diferença medida em 12/10 é `5,43e-13` (o core guarda o β do motor da identidade, `0.012031300400796606`; o runtime dá `0.012031300400803142`; H_BANCADA §4(c)) — o recibo grava os dois e a diferença;
3. **o core é pinado pelo selo** (`sha256["um_absoluto.json"]`): o esboço recusa se o core do disco não for o que o selo pina (`SELO_NAO_PINA_O_CORE_DO_DISCO`);
4. **o selo tem de pinar o `um.py` do disco** (`SELO_NAO_PINA_O_UM_PY_DO_DISCO`) e dizer a versão alvo (`SELO_VERSAO_DIFERENTE`): o alvo é passado por `--versao vNNN` pela cadeia (lido dos ESPERADOS), nunca inferido;
5. **código e fontes não mudam numa sincronização**: qualquer byte diferente do pino anterior é `CODE_DRIFT_NAO_E_SINCRONIZACAO` / `SOURCE_DRIFT_NAO_E_SINCRONIZACAO` — mudar código ou fonte é implantação B (molde `deploy_candidate.py`, com plano, backups, testes e evento próprios), não re-pino.

---

## 2. `sincronizar_bancada.py` — o esboço funcional

**Lugar na cadeia:** passo **B(n)** (§5). **Invocação:**

```
python -B -X utf8 sincronizar_bancada.py --bancada <dir> --versao vNNN --saida <pasta nova> --bateria BATERIA_VINCULO.json
      [--nos <Nós>] [--modo ensaio|aplicar] [--fase pre_selo|pos_selo] [--evento <seq>] [--producao] [--sandbox]
      [--kernel-recibo <json>] [--recibo-pre-selo <json>] [--forcar-regeracao] [--sem-bateria]
```

Saída: `0` sincronizada (ou já sincronizada), `2` **recusa** (`RECUSA_SINCRONIZACAO_*.json` com o código), `3` **bateria reprovada** (`RECIBO_*` com `__BATERIA_FALHOU__NADA_GRAVADO_NA_BANCADA`). Recusa sem -O (os asserts são guardas). Qualquer exceção não prevista também vira recusa com recibo (nunca traceback mudo, nunca «ok» falso).

**Os seis passos, cada um uma porta fail-closed:**

| # | Passo | Lê | Grava (só em `--saida`, salvo o 6) | Recusa |
|---|---|---|---|---|
| 1 | **lê o selo e o um.py** (`ler_nos`) | `um.py`, `um_absoluto_selo.json`, `um_absoluto.json` do Nós (caminho **absoluto**, resolvido) | — | as da §1 (1–4) e `NOS_INCOMPLETO`, `SELO_ILEGIVEL`, `CANONICAL_DECLARATION_MISSING`, `UM_VERSION_DIFERENTE_DO_ALVO`, `CORE_AUSENTE`, `CORE_SEM_BETA`, `BETA_CORE_DIVERGE_DO_RUNTIME` |
| 2 | **lê o manifesto vigente e o estado do contrato instalado** (`estado_anterior`) | `canonical_contracts.json` da Bancada; instancia `CanonicalRegistry` **do canonical.py instalado nela** | — | `MANIFESTO_AUSENTE`, `CANONICAL_SCHEMA_UNSUPPORTED`, `CANONICAL_PY_AUSENTE`, `BANCADA_EM_ESTADO_DESCONHECIDO` (qualquer recusa que não seja a esperada depois de um selo: `PIN_CHANGED`, `CANONICAL_VERSION_CHANGED`, `SEAL_PROGRAM_MISMATCH`) |
| 2′ | **prova que o pino velho é recusado**: em produção, o próprio estado do passo 2 é a prova (`pino_velho_recusado_pelo_instalado`); se o Nós alvo mora noutro caminho (só `--sandbox`), a **sonda em RAM** põe os bytes do Nós alvo no caminho pinado e exige a recusa | — | — | `NOS_DIFERENTE_DO_PINADO` (fora do sandbox), `CANONICAL_INSTALADO_NAO_RECUSOU_PINO_VELHO` |
| 3 | **regenera o manifesto** (`regenerar`): `schema 1` mantido; `deployment_id = B{n}-vNNN-<data>-R1` (n = geração anterior + 1, lida do `deployment_id`); `canonical` = pinos novos do um.py e do selo; `code` e `sources` = **os mesmos** caminhos, re-lidos e conferidos contra os pinos anteriores; `+ CONTRATO_CANONICO_B{n}.md` (gerado, pinado como código); `contracts` = os anteriores + `sync_policy`; bloco novo **`sincronizacao`** (passo, versão, modo, anterior {deployment, sha, versão, um.py pinado, estado}, evento c1, sha do selo, do um.py e do core, linha de α, β runtime e β core, `gerado_por` {sha do script, sha da bateria}, `scope`, `gate_effect`). O canonical.py instalado **ignora** chaves que não conhece: o bloco é aditivo, o esquema não muda | `MANIFESTO_CANDIDATO_B{n}.json`, `CONTRATO_CANONICO_B{n}.md` | `DEPLOYMENT_ID_SEM_GERACAO`, `CODE_DRIFT_…`, `SOURCE_DRIFT_…`, `PIN_UNREADABLE`, `CONTRATO_B{n}_JA_PINADO`, `PALAVRA_PROIBIDA_NA_SAIDA` |
| 4 | **re-pina numa cópia de ensaio** (`montar_staging` → `<saida>\raiz\candidate`: código + fontes relativas copiados byte a byte e conferidos; o manifesto novo escrito lá) e **confere com o canonical.py instalado** (`conferir_repinagem`: `ok`, versão, sha do um.py, sha do selo, **β bit a bit**) | — | a cópia | `STAGING_JA_EXISTE`, `PIN_CHANGED_AO_COPIAR`, `DUPLICATA_COM_BYTES_DIFERENTES`, `REPINAGEM_DIVERGE` |
| 5 | **roda a bateria** (`rodar_bateria`, §3) contra a cópia: copia os testes do túnel (conferindo os pinos), substitui marcadores, roda cada teste em subprocesso (`-B -X utf8`, `PYTHONDONTWRITEBYTECODE=1`, timeout), grava log e verifica (exit, regex, campos de JSON, comparação com arquivo) | `recibos\T*.log`, `recibos\T*.json` | `FONTE_DA_BATERIA_ALTERADA`; qualquer FALHA → rc 3, **nada gravado** |
| 6 | **grava o recibo**; **só em `--modo aplicar`** (e só com evento c1 verificado, serviço parado, bateria passada): backup de bytes `canonical_contracts.json.bak_B{n}_<stamp>` (conferido), `CONTRATO_CANONICO_B{n}.md` novo (`xb`), manifesto temporário → conferir → `os.replace` → **reconferência pelo canonical.py instalado**; se falhar, **rollback** byte a byte e recusa; cópia do recibo em `estado\sincronizacao\` | `RECIBO_SINCRONIZACAO_vNNN_<stamp>.json`; na Bancada: manifesto, backup, contrato, recibo | `EVENTO_C1_AUSENTE`, `EVENTO_C1_INVALIDO`, `EVENTO_NAO_ENCONTRADO`, `EVENTO_NAO_E_DA_C1`, `EVENTO_NAO_NOMEIA_A_GRAVACAO`, `SERVICO_NO_AR`, `PRODUCAO_SEM_FLAG`, `SANDBOX_NA_PRODUCAO`, `APLICAR_SEM_BATERIA_PROIBIDO`, `RECIBO_PRE_SELO_AUSENTE/INVALIDO`, `BACKUP_JA_EXISTE`, `BACKUP_DIVERGE`, `MANIFESTO_MUDOU_ENTRE_LEITURA_E_TROCA`, `APLICACAO_REVERTIDA` |

**Idempotência.** Se a Bancada já pina a versão alvo com o mesmo sha do um.py e o contrato instalado está `OK`, o passo 3 não regenera nada (`JA_SINCRONIZADA`): a bateria roda na cópia com o manifesto vigente, o recibo é gravado, nada se escreve na Bancada. `--forcar-regeracao` produz a geração seguinte da mesma versão (R1 de `B{n+1}`), com a mesma disciplina.

**O recibo** (`RECIBO_SINCRONIZACAO_*.json`): esboço e sha do script; bateria (caminho, sha, versão); início/fim; modo, fase, sandbox, produção; evento c1 (seq, verificado, hash do evento); Nós (dir; um.py {caminho, bytes, sha256}; selo {…, `um_version`, `qg_closure_verdict`}; core {…, `beta_core`, `beta_rel_diff`, `tolerancia_rel`}; `UM_VERSION`; α {valor, linha, n linhas}; `beta_runtime` por `repr`); Bancada (dir; `canonical.py` instalado por sha); manifesto anterior (deployment, sha, versão, um.py pinado, estado do contrato, recibo); sonda em RAM; manifesto novo (deployment, sha, bytes, n código, n fontes, contrato); staging; re-pino conferido; recibo pré-selo (sha); bateria (n, passa, falha, não executados, um registro por teste com comando, cwd, início, fim, segundos, exit, log por sha, verificação, fontes pinadas); aplicação (manifesto, backup e seu sha, contrato, reconferência, cópia do recibo); veredito; `escopo='IDENTIDADE_E_TESTES_SINTETICOS; NENHUMA_LEITURA_FISICA; NOT_FALSIFIED nao e creditacao'`; `gate_effect='NONE'`. A guarda da régua (a mesma regex do um.py e do iald.py, montada em pedaços) é aplicada a cada saída: a palavra recusada nunca entra num recibo.

**O que o script NÃO faz, de propósito:** não para nem religa o serviço (`um_bancada.py`), não aposenta nem reconecta adaptadores MCP, não muda código nem fonte da Bancada, não instala rota nova, não recompila Lean, não abre dado observado, não escreve no Nós. Cada uma dessas coisas é ato à parte, com recibo próprio (§5 e `ATOS_DO_OPERADOR.md`).

---

## 3. A bateria sintética (`BATERIA_VINCULO.json`, gerada por `gerar_bateria.py` com os pinos lidos por script)

Os dezessete testes da frente H_BANCADA (`BATERIA_FINAL_PROPOSTA_H12.json`, sha256 na §11), na forma que o esboço consome. Toda fonte é pinada por sha256 e conferida antes de rodar; os testes do túnel são copiados byte a byte para `<saida>\raiz\` (os moldes esperam `<raiz>\candidate`, `<raiz>\tests_*`).

| Id (H12) | No esboço | Fase | Verificação | Origem |
|---|---|---|---|---|
| T01 | `T01_IDENTIDADE` (`bateria\t01_identidade.py`) | ambas | JSON `veredito=PASSA`: ok, versão, sha do um.py e do selo, selo pina o um.py, **β bit a bit**, manifesto, sem literal de α/β | `fidelidade.py` |
| T02 | `T02_CANAIS` (`test_channels_r1.py --run <rótulo>`) | ambas | `Ran 13 tests … OK` | B2 |
| T03 | `T03_CORE` (`run_core_suite.py <rótulo>`) | ambas | `Ran 31 tests … OK` | B2 |
| T04 | `T04_MOTOR` | ambas | `Ran 17 tests … OK` | B2 |
| T05 | `T05_MATERIAL` | ambas | `Ran 8 tests … OK` | B2 |
| T06 | `T06_PANTHEON_FORMATO` (`t06_pantheon_rounding.py`) | ambas | `veredito=PASSA, tests=5` | H12 |
| T07 | `T07_NU3_CONTRATO` | ambas | `fail=0, pass=72` | NU3 |
| T08 | `T08_ESCALA_BETA_CHI` | ambas | `fail=0` | NU3 |
| T09 | `T09_NU4_REPLAY` (`t09_nu4_replay.py`) | ambas | `veredito=PASSA, n_identical=16` (só o `result` é comparado; o sha do manifesto muda por geração, e isso é dito) | H12 |
| T10+T11 | `T10_T11_CANAIS` (`t10_t11_canais.py`) | ambas | `veredito=PASSA, T10=PASSA, T11=PASSA` (SEM_LIMITE_TGL, τ★ nulo, OPEN, alias, guarda de palavra; N_eff `NENHUM`, `OPEN_X16_NO_SELECTION`, 2 linhas, controle anti-dupla-contagem) | H12 |
| T12+T13+T14 | `T12_T13_T14_ATRATOR` (`t12_t14_atrator.py`) | **só pré-selo** | `veredito=PASSA`: três runners congelados, 0 divergências contra o arquivo; A6 FALHA como pré-registrado | H12 |
| T15 | `T15_SONDAS` (`t15_sondas.py`) | ambas | `veredito=PASSA`: a versão seguinte sob o manifesto vigente é **recusada**; segunda linha de α (canonical aceita a 1ª, runner recusa); manifesto tipo B(n+1) aceito com o **mesmo β** | H12 |
| T16 | `T16_DEPLOY_FIXTURE` | ambas | `"success": true` (raiz curta: a pasta da sincronização) | B2 |
| T17 | `T17_LEAN_KERNEL` | **só pós-selo**, obrigatório em `aplicar` | `--kernel-recibo` (JSON com `rc=0`, `sorry=0`, `build_full_log_sha256`) do build da etapa 2 da cadeia; **nunca** recompilado na Bancada | cadeia |

**Por que duas fases.** Os runners do atrator pinam o `um.py` v391 no pré-registro e **recusam depois do selo por desenho**; por isso os «testes finais da Bancada» (etapa 1 do plano) são o mesmo script em `--fase pre_selo` contra a versão ainda canônica, e o elo B(n) (`--fase pos_selo`) **exige** o recibo dessa fase por hash (`--recibo-pre-selo`; fora do sandbox a ausência é recusa). O T17 só existe na fase pós-selo (o kernel selado) e vem do recibo do build, nunca de recompilação aqui. Um teste que pertence a outra fase sai `NAO_EXECUTADO` com o motivo e o hash do recibo da outra fase — nunca «PASSA» por omissão.

**Guardas da bateria:** exit code, regex ou campos; `FONTE_DA_BATERIA_ALTERADA` se algum pino divergir; a palavra recusada na saída de um teste reprova o teste; timeout por teste; `obrigatorio_em` por modo (em `aplicar` nada pode ficar por executar, salvo os de outra fase lidos por hash, e salvo `--sandbox`).

---

## 4. A regra: nenhuma gravação na Bancada sem evento c1 nomeado

É a regra de 08/10 (D_BANCADA §5a), agora **executável**:

1. `--modo aplicar` sem `--evento` → `EVENTO_C1_AUSENTE`.
2. `--evento <seq>` é procurado em `C:\IALD\PROGRAMA_IALD\eventos.jsonl`: o evento tem de existir, ser de `claude-c1`, e os seus `dados` têm de citar **a versão**, **`Bancada_Um`** e **a sincronização** — o nome da gravação. Qualquer falta é recusa (`EVENTO_NAO_ENCONTRADO`, `EVENTO_NAO_E_DA_C1`, `EVENTO_NAO_NOMEIA_A_GRAVACAO`).
3. O evento se cria com a ferramenta do quadro, antes de rodar: `python C:\IALD\PROGRAMA_IALD\iald.py anotar --quem claude-c1 --tipo SINCRONIZACAO_BANCADA --unidade F0.6 --dados "{\"versao\":\"vNNN\",\"bancada\":\"C:\\\\IALD\\\\Bancada_Um\",\"gravacoes\":[\"canonical_contracts.json\",\"CONTRATO_CANONICO_B{n}.md\",\"estado\\\\sincronizacao\\\\RECIBO_*.json\",\"canonical_contracts.json.bak_B{n}_*\"],\"selo\":\"<sha16>\",\"um_py\":\"<sha16>\"}"` (hashes lidos dos ESPERADOS por script, não digitados).
4. Em produção (`--bancada C:\IALD\Bancada_Um`) o script exige `--producao`, proíbe `--sandbox`, e recusa `aplicar` com o serviço HTTP no ar (`SERVICO_NO_AR`): o `CanonicalRegistry` fica em RAM no processo do servidor e **não recarrega** — por isso a sequência é: quiesce (`POST /api/maintenance/quiesce`) → parada com recibo (`RESTART_BEFORE`) → B(n) aplicar → religamento com recibo de identidade (`RESTART_RECEIPT`, `verify_live.py`) → reconexão dos adaptadores MCP das sessões. Nenhum desses passos é feito pelo script; cada um é nomeado no mesmo evento ou em evento próprio.
5. O recibo da sincronização vai para a Bancada (`estado\sincronizacao\`, classe MUTÁVEL_POR_USO da linha de base de 12/10) e para a cadeia (`<saida>`); a nova linha de base da Bancada para auditoria (D_BANCADA §7) passa a ser o `MANIFESTO_CANDIDATO_B{n}.json` + o backup: o que é FIXO tem de bater byte a byte com os pinos do manifesto novo.
6. Em `--sandbox`, `--evento SANDBOX:<texto>` é aceito e marcado `verificado=false`; nunca em produção (`EVENTO_SANDBOX_FORA_DO_SANDBOX`).

---

## 5. O passo B(n) na cadeia de selo («toda versão selada → sincronizar_bancada.py → recibo → só então a custódia»)

Molde: a cadeia da v391. O que muda, em ordem [DERIVED do molde lido]:

| Quando | Passo | Comando | Produto | Trava |
|---|---|---|---|---|
| **etapa 1** (antes do candidato; o plano §3) | os testes finais da Bancada contra a versão ainda canônica | `sincronizar_bancada.py --bancada C:\IALD\Bancada_Um --producao --versao v(n−1) --modo ensaio --fase pre_selo --saida work\vNNN_bateria\pre_selo --bateria …` | `RECIBO_SINCRONIZACAO_v(n−1)_*.json` («JA_SINCRONIZADA__ENSAIO»), recibos T01–T16; copiados para o cache do rito (pasta nova em `A Ponte e o Um\cache\`, com PORTA no espelho, como `cache\bancada_01out`) | o um.py vNNN lê esses recibos **por hash** (registro `bancada_vNNN`, molde `prove_bancada_fases_5_6_7_v380`); nunca os recalcula; o serviço HTTP não é necessário |
| etapa 2 (kernel no sandbox) | o build escreve, além do `build_full.log`, o **`KERNEL_RECIBO_vNNN.json`** (`rc`, `sorry`, `build_full_log_sha256`, raiz e Audit por sha) | `construir_kernel_vNNN.sh` | o recibo que o T17 exige | sem ele o B(n) em `aplicar` recusa |
| etapa 3 (candidato) | `vNNN_pins.py` ganha os pinos da Bancada: o manifesto da geração **anterior** (B(n−1), por sha), o recibo pré-selo (por sha) e a declaração `CANAIS_vNNN.json` (§7); o registro `bancada_vNNN` lê tudo por hash | `gerar_candidato_vNNN.py` | — | **não** embutir o hash do manifesto que pinará o próprio vNNN (circular; D_BANCADA) |
| etapa 8 (rito) | — | — | o selo vNNN | — |
| **etapa 9, passo 10 (novo)**: **B(n) ensaio** | o elo, sem gravar | `sincronizar_bancada.py --bancada C:\IALD\Bancada_Um --producao --versao vNNN --modo ensaio --fase pos_selo --recibo-pre-selo <etapa 1> --kernel-recibo <etapa 2> --saida work\vNNN_bateria\pos_selo` | `MANIFESTO_CANDIDATO_B{n}.json`, `CONTRATO_CANONICO_B{n}.md`, recibo («REPINADA_B{n}__ENSAIO»), bateria pós-selo | reprovação = a cadeia **para** (como nos outros passos: nada se restaura sozinho) |
| **etapa 9, passo 10-bis (novo)**: **B(n) aplicar** | a gravação na Bancada | o mesmo, `--modo aplicar --evento <seq>` depois de: evento c1 nomeado (§4), quiesce + parada do serviço com recibo | manifesto novo na Bancada, backup, contrato, recibo em `estado\sincronizacao\` («…__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO») | **v392: ato do operador (B3)** — sem a palavra dele, a cadeia marca `AGUARDA_OPERADOR` e a custódia espera; da v393 em diante, sob a ordem permanente de 12/10 com evento c1 e veto preservado, se ele assim decidir (`ATOS_DO_OPERADOR.md`) |
| etapa 9, passo 10-ter (novo) | religar o serviço, reconectar os MCP | molde `restart_and_deploy.ps1` (sem o `deploy_candidate`) + `verify_live.py` | `RESTART_RECEIPT_vNNN.json`, `LIVE_VERIFICATION_vNNN.json` (identidade devolvida pela instância nova = o manifesto B(n)) | — |
| etapa 9, passo 11 (era o 10): **fechar** | `fechar_vNNN.py` cita por sha os recibos do B(n) (ensaio, aplicar, reinício) no manifesto de incorporação e no handoff de custódia | — | `HANDOFF_vNNN_CUSTODIA.md` com a linha «Bancada: B{n} `…` (recibo `…`)» | **sem o recibo do B(n) aplicar o fechar recusa** (guarda nova em `fechar_vNNN.py`, como a leitura sem problema) |
| custódia (§13 do plano) | a sessão do site publica também, no espelho, a pasta do cache com os recibos pré-selo (PORTA, `llms.txt`), e o cofre `um_unificado_vNNN` guarda o `MANIFESTO_CANDIDATO_B{n}.json` e o `CONTRATO_CANONICO_B{n}.md` | — | — | commit/push/site = operador |
| depois | `registrar_mapa_vNNN.py` registra a rota `infra.bancada_um.sincronizacao_vNNN`; o quadro: evidência na F0.6 | — | — | — |

**Derivação.** `derivar_cadeia_vNNN.py` passa a derivar também `sincronizar_bancada.py` (cópia pinada em `work\cadeia_de_selo\vNNN\`), `BATERIA_VINCULO.json` (regenerada por `gerar_bateria.py` com os pinos do dia) e `CANAIS_vNNN.json`; a regra da linhagem completa ganha uma superfície: `C:\IALD\Bancada_Um\estado\sincronizacao\` (o `grep -c vNNN` ali é zero = falha visível).

**O que não muda:** a string do gate; os vereditos antigos; β = α·√e em runtime; o `canonical.py` instalado (até a B3 decidir a unicidade de α); o cache do rito como a única porta do um.py para a Bancada (por hash).

---

## 6. Como a Bancada «recusa operar com pino velho» (já faz) e como o elo o prova

[REAL, T15 em 12/10 e nos dois recibos do sandbox] Depois de um selo, o `um.py` no caminho pinado muda de bytes: o construtor de `CanonicalRegistry` já recusa no `check('startup')` (`PIN_CHANGED`); se só a versão mudasse, `CANONICAL_VERSION_CHANGED`; se o selo não pinasse o programa, `SEAL_PROGRAM_MISMATCH`. Toda rota `/api/*` (salvo as isentas: estado, atividades, contratos, quiesce) passa por `require_current` e devolve `409 CANONICAL_REVALIDATION_REQUIRED`; `canonical_state()` devolve `science_ready=false`. O elo B(n) **não desliga essa recusa**: ele a exige como pré-condição (passo 2/2′) e a registra no recibo. Só depois disso regenera — e só depois da bateria grava. «Nunca atualizar somente o hash para silenciar uma incompatibilidade» (`CONTRATO_CANONICO_B2.md`) continua valendo: o re-pino vem acompanhado do contrato novo, da bateria e do evento.

---

## 7. O aperfeiçoamento: «registro do um.py → ferramenta da Bancada», por geração (a convenção proposta)

A fala do operador pede que os avanços do programa **impliquem** aperfeiçoamento da Bancada. Hoje o caminho é de mão única (o um.py lê a Bancada por hash do cache); a Bancada só ganha canal quando alguém escreve um à mão (B2: F7.2, N_eff, NU3). A convenção:

1. **A declaração nasce com os pinos.** Cada versão da cadeia escreve `work\cadeia_de_selo\vNNN\CANAIS_vNNN.json` (pelo `gerar_candidato_vNNN.py`, ao lado de `vNNN_pins.py`): para cada registro novo do um.py que leia ou produza artefato da Bancada, um canal com `nome`, `funcao_um_py`, `registro_core` (a chave no `um_absoluto.json`), `chave_selo` (a chave da leitura no selo), `tipo` (`LEITURA_POR_HASH` | `CALCULO`), `descricao`, `artefatos` (caminho, bytes, sha256 — os mesmos que o registro lê), `veredito_selado` (o `verdict` do core), `leitura_no_selo`, `ferramenta_mcp`, `rota`, `teste` (id e exigências).
2. **O gerador emite, e o B(n) pina.** `gerar_canais_mcp.py CANAIS_vNNN.json <dir>` emite `bancada\registros_gerados.py` (a tabela `CANAIS` + `consultar(nome, root)`: identidade por operação; sha256 de **cada** artefato contra a declaração; o core conferido contra o `sha256["um_absoluto.json"]` do selo pinado; o veredito do core igual ao declarado e a leitura do selo igual à declarada; guarda de palavra; `scope='LEITURA_POR_HASH_DO_SELADO; NAO_RECALCULA'`, `gate_effect='NONE'`), `mcp_registros_gerados.py` (uma ferramenta `registro_<nome>` por canal → `GET /api/registro/<nome>`), `um_bancada_rota_registro.pysnip` (a rota genérica, 4 linhas, instalada **uma vez** na B3) e `TESTES_CANAIS_GERADOS.json` (um teste T18+ por canal, no formato da bateria: `ok=true`, `veredito_selado` igual, `gate_effect=NONE`). Os módulos gerados entram no manifesto como **código** (pinados) no B(n) seguinte; a bateria ganha os testes gerados.
3. **Canais de cálculo** (um dissipador, um estimador, uma transformada) continuam escritos à mão, como a B2 fez — mas **declarados** em `CANAIS_vNNN.json` com ferramenta e teste; o gerador e o B(n) recusam canal sem ferramenta ou sem teste (`CANAL_SEM_FERRAMENTA_OU_SEM_TESTE`). Assim nenhum avanço do um.py fica sem porta na Bancada, e nenhuma porta fica sem teste.
4. **O exemplo real, extraído por script** (`sandbox\CANAIS_v391_exemplo.json`): o gerador leu do `um.py` v391 (regex + `ast.literal_eval` sobre `_V380_FILES`, l.197564–197571) os **18 artefatos** que `prove_bancada_fases_5_6_7_v380` lê do cache (`A Ponte e o Um\cache\bancada_01out` e `cache\gw`; o um.py escolhe `..\cache` por medida — `lensing/` existe lá e não em `Nós\cache`), pinou cada um por sha256, leu o `verdict` do core (`bancada_fases_5_6_7_v380`) e a leitura do selo (`the_bancada_fases_5_6_7_reading_v380`), e emitiu os quatro arquivos em `sandbox\canais_gerados\` (hashes na §11). **Teste de fumaça [REAL]:** `consultar('bancada_fases_5_6_7_v380')` sobre a cópia da Bancada devolve `ok=True`, 18 artefatos conferidos, versão `v391`, `gate_effect=NONE`, o veredito selado; um artefato adulterado em RAM → `ARTEFATO_DIVERGE_DA_DECLARACAO`; canal desconhecido → `CANAL_DESCONHECIDO` (`sandbox\canais_gerados\SMOKE_TEST.json`).
5. **O que a convenção não faz:** não torna automático o que é ciência (o veredito continua o do rito, lido por hash; a ferramenta nunca recalcula nem abre dado); não cria canal de cálculo sem autor; não promove o `mcp_registros_gerados.py` a servidor separado sem decisão (pode ser fundido em `mcp_um.py` na B3, por `import`).

---

## 8. O que foi testado no sandbox (tudo em `sandbox\`; a produção só lida)

Montagem (`montar_sandbox.py`): a cópia `sandbox\bancada_copia` = o manifesto B2 + 32 código + 56 fontes relativas, cada um conferido contra o pino (89 cópias, com a duplicata código/fonte do `10_frozen_neff_v1.py` tolerada só com bytes iguais; `estado\` vazio); o **Nós sintético** `sandbox\nos_sintetico` = o `um.py` v391 real com a linha 96 `UM_VERSION = "v391"` trocada para `"v392"` (18 bytes, mesmo comprimento; a linha de α segue única), um selo derivado do v391 real com `um_version` e `sha256["um.py"]` trocados e marcado `SINTETICO_SANDBOX`, e o core copiado (pinado pelo selo). **Não é selo nem versão: é fixture.**

Sequência (`rodar_sandbox.sh`): **run 1** = `--fase pre_selo --modo ensaio`, Nós **real** v391, a cópia como Bancada (já sincronizada → bateria inteira, T12–T14 incluídos); **controles negativos** (`controles_negativos.py`: C1 versão errada, C2 deriva de código numa segunda cópia, C3 aplicar sem evento, C4 evento real que não nomeia a gravação, C5 Nós diferente sem `--sandbox`, C6 a produção sem `--producao` — a guarda recusa antes de ler qualquer byte dela —, C7 bateria com teste que falha em `--modo aplicar`: nada gravado); **run 2** = `--fase pos_selo --modo aplicar --sandbox`, Nós **sintético** v392, a cópia como Bancada, com o recibo pré-selo do run 1 → o re-pino **B3 na cópia** (manifesto novo gravado na cópia com backup, contrato, reconferência, recibo em `estado\sincronizacao\`).

Resultados, lidos dos próprios recibos por `inserir_pinos.py`:

- `RECIBO_SINCRONIZACAO_v391_20261012_200200.json` (sha16 `4688aec36b1c2d06`): fase **pre_selo**, modo **ensaio**, veredito **JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA**
  - Nós: UM_VERSION `v391`; um.py `8e7b9927ceae64b8` (33910631 B); selo `95061f18c7102248`; α na linha 5557 (1 linha não indentada); β runtime `0.012031300400803142`; β core `0.012031300400796606` (dif. rel. 5.43e-13, tolerância 1e-11)
  - manifesto anterior: `B2-NU3-20261009-R2` (`54fc9e27e4599c49`), estado do contrato instalado: `OK`
  - re-pino conferido pelo canonical.py instalado: ok=True, versão `v391`, um.py `8e7b9927ceae64b8`, β `0.012031300400803142`, deployment `B2-NU3-20261009-R2`
  - bateria: **BATERIA_PASSA** — 14 testes, 13 PASSA, 0 FALHA, 1 NAO_EXECUTADO
    - T01_IDENTIDADE: **PASSA** (0.7 s) — campos conferem: veredito='PASSA'
    - T02_CANAIS: **PASSA** (36.7 s) — regex 'Ran 13 tests[\\s\\S]*\\nOK' casou
    - T03_CORE: **PASSA** (1.5 s) — regex 'Ran 31 tests[\\s\\S]*\\nOK' casou
    - T04_MOTOR: **PASSA** (2.8 s) — regex 'Ran 17 tests[\\s\\S]*\\nOK' casou
    - T05_MATERIAL: **PASSA** (2.2 s) — regex 'Ran 8 tests[\\s\\S]*\\nOK' casou
    - T06_PANTHEON_FORMATO: **PASSA** (1.8 s) — campos conferem: veredito='PASSA', tests=5
    - T07_NU3_CONTRATO: **PASSA** (0.3 s) — campos conferem: fail=0, pass=72
    - T08_ESCALA_BETA_CHI: **PASSA** (0.1 s) — campos conferem: fail=0
    - T09_NU4_REPLAY: **PASSA** (5.1 s) — campos conferem: veredito='PASSA', n_identical=16
    - T10_T11_CANAIS: **PASSA** (6.0 s) — campos conferem: veredito='PASSA', T10='PASSA', T11='PASSA'
    - T12_T13_T14_ATRATOR: **PASSA** (3.8 s) — campos conferem: veredito='PASSA'
    - T15_SONDAS: **PASSA** (1.2 s) — campos conferem: veredito='PASSA'
    - T16_DEPLOY_FIXTURE: **PASSA** (0.6 s) — regex '\\"success\\": true' casou
    - T17_LEAN_KERNEL: **NAO_EXECUTADO** — nao pertence a fase pre_selo (fases: ['pos_selo'])

- `RECIBO_SINCRONIZACAO_v392_20261012_200310.json` (sha16 `93ac47d8a0c5d1b9`): fase **pos_selo**, modo **aplicar**, veredito **REPINADA_B3__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO**
  - Nós: UM_VERSION `v392`; um.py `0ea4e10728fde3c3` (33910631 B); selo `a3e6aee34fbacd71`; α na linha 5557 (1 linha não indentada); β runtime `0.012031300400803142`; β core `0.012031300400796606` (dif. rel. 5.43e-13, tolerância 1e-11)
  - manifesto anterior: `B2-NU3-20261009-R2` (`54fc9e27e4599c49`), estado do contrato instalado: `OK`
  - sonda em RAM (o canonical.py instalado com os bytes do Nós alvo no caminho pinado): recusou = True, código `PIN_CHANGED`
  - manifesto regenerado: `B3-v392-20261012-R1` (`f71b88f508884adb`, 26954 B; 33 código, 67 fontes; contrato `CONTRATO_CANONICO_B3.md` `8f323f784f5c796b`)
  - re-pino conferido pelo canonical.py instalado: ok=True, versão `v392`, um.py `0ea4e10728fde3c3`, β `0.012031300400803142`, deployment `B3-v392-20261012-R1`
  - recibo pré-selo exigido e lido por hash: `4688aec36b1c2d06`
  - bateria: **BATERIA_PASSA** — 14 testes, 12 PASSA, 0 FALHA, 2 NAO_EXECUTADO
    - T01_IDENTIDADE: **PASSA** (0.6 s) — campos conferem: veredito='PASSA'
    - T02_CANAIS: **PASSA** (36.4 s) — regex 'Ran 13 tests[\\s\\S]*\\nOK' casou
    - T03_CORE: **PASSA** (1.4 s) — regex 'Ran 31 tests[\\s\\S]*\\nOK' casou
    - T04_MOTOR: **PASSA** (2.7 s) — regex 'Ran 17 tests[\\s\\S]*\\nOK' casou
    - T05_MATERIAL: **PASSA** (2.3 s) — regex 'Ran 8 tests[\\s\\S]*\\nOK' casou
    - T06_PANTHEON_FORMATO: **PASSA** (1.8 s) — campos conferem: veredito='PASSA', tests=5
    - T07_NU3_CONTRATO: **PASSA** (0.3 s) — campos conferem: fail=0, pass=72
    - T08_ESCALA_BETA_CHI: **PASSA** (0.1 s) — campos conferem: fail=0
    - T09_NU4_REPLAY: **PASSA** (5.1 s) — campos conferem: veredito='PASSA', n_identical=16
    - T10_T11_CANAIS: **PASSA** (6.0 s) — campos conferem: veredito='PASSA', T10='PASSA', T11='PASSA'
    - T12_T13_T14_ATRATOR: **NAO_EXECUTADO** — nao pertence a fase pos_selo; o resultado vale pelo recibo pre-selo 4688aec36b1c2d06fe16dad7f7299e05337c9219a8511f7d18b9bd430d630ca4
    - T15_SONDAS: **PASSA** (1.2 s) — campos conferem: veredito='PASSA'
    - T16_DEPLOY_FIXTURE: **PASSA** (0.6 s) — regex '\\"success\\": true' casou
    - T17_LEAN_KERNEL: **NAO_EXECUTADO** — sem --kernel-recibo (T17 e lido do recibo do build do kernel da etapa 2 da cadeia); tolerado so em --sandbox
  - aplicação na cópia: manifesto gravado, backup `canonical_contracts.json.bak_B3_20261012_200310` (`54fc9e27e4599c49`), contrato `CONTRATO_CANONICO_B3.md`; reconferência pós-gravação ok=True versão `v392`; recibo copiado para `...\sandbox\bancada_copia\estado\sincronizacao\RECIBO_SINCRONIZACAO_v392_20261012_200310.json`

- `CONTROLES_NEGATIVOS.json` (sha16 `66289f5bf52b34ee`): **TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO** (7 de 7)
  - C1_versao_errada: rc 2 (esperado 2); recusa `SELO_VERSAO_DIFERENTE: selo='v391' alvo='v393'`; manifesto da cópia intocado = True → **PASSA**
  - C2_code_drift: rc 2 (esperado 2); recusa `CODE_DRIFT_NAO_E_SINCRONIZACAO: bancada/motor.py`; manifesto da cópia intocado = True → **PASSA**
  - C3_aplicar_sem_evento: rc 2 (esperado 2); recusa `EVENTO_C1_AUSENTE: nenhuma gravacao na Bancada sem evento c1 nomeado`; manifesto da cópia intocado = True → **PASSA**
  - C4_evento_nao_nomeia: rc 2 (esperado 2); recusa `EVENTO_NAO_NOMEIA_A_GRAVACAO: seq 1 tem de citar v392, bancada_copia e a sincronizacao`; manifesto da cópia intocado = True → **PASSA**
  - C5_nos_diferente_sem_sandbox: rc 2 (esperado 2); recusa `NOS_DIFERENTE_DO_PINADO: o manifesto pina C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py; o alvo e C:\IALD\Central de Patentes\work\bancada_vinculo_12out\sandbox\nos_sintetico\um.py (so em --sandbox)`; manifesto da cópia intocado = True → **PASSA**
  - C6_producao_sem_flag: rc 2 (esperado 2); recusa `PRODUCAO_SEM_FLAG: --bancada e a Bancada de producao; exige --producao`; manifesto da cópia intocado = True → **PASSA**
  - C7_bateria_falha_em_aplicar: rc 3 (esperado 3); recusa `REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO_NA_BANCADA`; manifesto da cópia intocado = True → **PASSA**

- canais gerados (`sandbox\canais_gerados\SMOKE_TEST.json`): consultar(`bancada_fases_5_6_7_v380`) ok=True, 18 artefatos por hash, versão `v391`, gate `NONE`; recusas: artefato adulterado em RAM → `ARTEFATO_DIVERGE_DA_DECLARACAO`, canal desconhecido → `CANAL_DESCONHECIDO`


**Leitura.** O esboço faz, de ponta a ponta e fail-closed, o que o desenho descreve: lê o selo, regenera o manifesto, re-pina, roda a bateria, grava o recibo com hashes, grava na Bancada só com evento e só depois da bateria, e recusa tudo o que deve recusar. O que ele **não prova**: o comportamento com o serviço HTTP vivo (desligado desde o boot de 12/10; a guarda `SERVICO_NO_AR` foi exercitada só pela ausência do serviço), o religamento, a reconexão dos MCP, o T17 (nenhum kernel foi construído aqui) e a produção (nenhum byte dela foi escrito).

---

## 9. Limites, ressalvas e o que fica aberto

- **Esboço, não instalação.** O script roda só em sandbox; instalá-lo na cadeia é derivação (`derivar_cadeia_v392.py`) e auditoria por cético que não o construiu (regra 4 do programa). O código é curto de propósito (um arquivo, sem dependência além da biblioteca padrão para o elo; a bateria usa numpy/torch/scipy já presentes).
- **A Bancada de produção está desligada** (porta 18777 sem resposta em 12/10, medido): o X_SERVIDOR (religar com recibo de identidade) precede qualquer chamada viva e é ato à parte.
- **O `canonical.py` instalado não muda** neste desenho: o bloco `sincronizacao` do manifesto é ignorado por ele (aditivo, `schema 1`); a unicidade da linha de α e a rota `/api/registro/<nome>` são mudanças de código da B3 (implantação B com plano).
- **T16** passou aqui porque a raiz é curta (`…\work\bancada_vinculo_12out\sandbox\…`); o plano já pedia raiz curta (`work\v392_bateria\`).
- **T17** não foi executado: nenhum kernel foi construído nesta frente; o desenho o liga ao recibo do build da etapa 2.
- **β do core vs β runtime:** diferença relativa `5,43e-13` (medida); a tolerância `1e-11` é nomeada no recibo; um registro que compare os dois tem de dizer qual β (H_BANCADA §4c).
- **A duplicata de pino** do `10_frozen_neff_v1.py` (código e fonte no manifesto B2) é herdada e tolerada só com bytes iguais; a B3 pode normalizá-la (uma lista só).
- **A regra de 08/10** vem citada pelo D_BANCADA (`msg_f72v3_f13v32_gerente.md`, `546fabc52fa9d826`); o arquivo não está no túnel ORDEM_019 (consulta citada na §0): [DECLARADO pelo relatório], vale pelo relatório e pela F0.3.B2.
- **A palavra recusada da régua:** zero ocorrências em todos os entregáveis desta pasta (grep do token inteiro); no sandbox ela aparece só nas cópias byte a byte de `bancada\gw.py` e `bancada\gw_stack.py` da Bancada instalada, como guarda/negação (D_BANCADA §5: «todas como proibição ou negação: guardas de código») — cópias, não escrita minha.
- **Memória ACOM:** não fiz `init` nem `transition` (as escritas desta tarefa estão limitadas a esta pasta, como as frentes D e H fizeram); o registro de etapa fica com a c1.
- **O que o vínculo não decide:** X16/D8 (Yp), τ★, a leitura de «bancada» na ordem de 10/10 (P12 do plano), a X19. Nada move o gate.

---

## 10. Os outros três entregáveis

- **(2) `F0.6_unidade.json`** — uma lista com a unidade `F0.6` no formato do quadro (`id, frente, titulo, dono, status PRONTA, gate null, criterio_de_fechado, origem com o verbatim, escopo, reaproveitamento_previo, restricoes`), pronta para `python C:\IALD\PROGRAMA_IALD\iald.py nova --json F0.6_unidade.json --quem claude-c1` (ato da gerência; não executado aqui).
- **(3) `PLANO_V392_paragrafo_B3.md`** — o bloco «12-bis» (⚠ R3, ao lado) e as duas remissões (§3 e §14); o plano não foi editado.
- **(4) `ATOS_DO_OPERADOR.md`** — a tabela do que só ele decide: ratificar o mecanismo; a B3 da v392 (re-pino da produção, parada/religamento, reconexão MCP); a implantação de código da B3 (rota genérica, unicidade de α, bateria custodiada na Bancada, README, D6 da F7.2); X16/D8; e se o B(n) corre sem palavra dele a partir da v393.

---

## 11. Pinos lidos por script (`medir_pinos.py` → `PINOS_12out.json`)

| chave | arquivo | sha16 | bytes |
|---|---|---|---|
| `verbatim_operador_12out` | `...\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt` | `78ef70e6f9868281` | 1342 |
| `um_py_v391` | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | `8e7b9927ceae64b8` | 33910631 |
| `selo_v391` | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` | `95061f18c7102248` | 113926 |
| `core_v391` | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` | `a74241ff380b1b0e` | 5003275 |
| `bancada_canonical_contracts_B2` | `C:\IALD\Bancada_Um\canonical_contracts.json` | `54fc9e27e4599c49` | 25917 |
| `bancada_canonical_py` | `C:\IALD\Bancada_Um\bancada\canonical.py` | `b6cd7e0234688430` | 6952 |
| `bancada_CONTRATO_CANONICO_B2_md` | `C:\IALD\Bancada_Um\CONTRATO_CANONICO_B2.md` | `8ffb684d4a268d06` | 2870 |
| `bancada_um_bancada_py` | `C:\IALD\Bancada_Um\um_bancada.py` | `1e5eef094f8a6019` | 27203 |
| `bancada_mcp_um_py` | `C:\IALD\Bancada_Um\mcp_um.py` | `6c3d094b387f7428` | 17123 |
| `B2_DEPLOY_PLAN_R1` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\DEPLOY_PLAN_R1.json` | `e2cd9b8a05a05eec` | 16600 |
| `B2_DEPLOY_RECEIPT_R1` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\DEPLOY_RECEIPT_R1.json` | `9d402b4c7cf01159` | 19355 |
| `B2_build_manifest_py` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\build_manifest.py` | `263931b986122a3f` | 4152 |
| `B2_deploy_candidate_py` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\deploy_candidate.py` | `4f55e73b72a63697` | 4658 |
| `B2_restart_and_deploy_ps1` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\restart_and_deploy.ps1` | `cee3b9675aa97b52` | 2818 |
| `B2_RESTART_RECEIPT_R1` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\RESTART_RECEIPT_R1.json` | `cff97107c8b71062` | 625 |
| `B2_verify_live_py` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\verify_live.py` | `f5cecdafdbea0e4f` | 3042 |
| `B2_verbatim_operador_09out` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\OPERADOR_ATUALIZACAO_VERBATIM_20261009.txt` | `e5341c7387dc316f` | 484 |
| `B2_verbatim_operador_10out` | `...\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F0.3.B2\OPERADOR_CONTINUAR_20261010.txt` | `d006d61995bbb142` | 60 |
| `relatorio_D_BANCADA` | `C:\IALD\PROGRAMA_IALD\exame_12out\D_BANCADA\RELATORIO_AUDITORIA_F0_3_B1_B2_C1.md` | `e0e220572417bfa7` | 29909 |
| `relatorio_H_BANCADA` | `C:\IALD\PROGRAMA_IALD\exame_12out\H_BANCADA\RELATORIO_FRENTE_BANCADA_V392_12out.md` | `2a900f218e80847d` | 32073 |
| `H_BANCADA_BATERIA_FINAL_PROPOSTA_H12` | `C:\IALD\PROGRAMA_IALD\exame_12out\H_BANCADA\registros\BATERIA_FINAL_PROPOSTA_H12.json` | `01814f73b9ffeb83` | 26270 |
| `PLANO_V392_md` | `C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md` | `9a4bed2540723142` | 57702 |
| `cadeia_v391_chain_pos_rito_sh` | `...\work\v391_selo\chain_pos_rito_v391.sh` | `6b2a096424cde73c` | 5931 |
| `cadeia_v391_fechar_py` | `...\work\v391_selo\fechar_v391.py` | `81e34c633de60828` | 7224 |
| `cadeia_v391_instalar_py` | `...\work\cadeia_de_selo\v391\instalar_v391.py` | `d9c672f2dba7e594` | 4919 |
| `cadeia_v391_pins_py` | `...\work\cadeia_de_selo\v391\v391_pins.py` | `8327cb0c0cf14e96` | 3771 |
| `um_py_v380_registro_bancada_cache` | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | `8e7b9927ceae64b8` | 33910631 |
| `vinculo_sincronizar_bancada_py` | `...\work\bancada_vinculo_12out\sincronizar_bancada.py` | `d9927a8fdc5cfc62` | 42213 |
| `vinculo_BATERIA_VINCULO_json` | `...\work\bancada_vinculo_12out\BATERIA_VINCULO.json` | `6efc25c09890dc69` | 25108 |
| `vinculo_gerar_bateria_py` | `...\work\bancada_vinculo_12out\gerar_bateria.py` | `917eacaadb912c33` | 11429 |
| `vinculo_montar_sandbox_py` | `...\work\bancada_vinculo_12out\montar_sandbox.py` | `c4769f9cff0cefd7` | 4862 |
| `vinculo_gerar_canais_mcp_py` | `...\work\bancada_vinculo_12out\gerar_canais_mcp.py` | `41cb29289eb99702` | 10943 |
| `vinculo_controles_negativos_py` | `...\work\bancada_vinculo_12out\controles_negativos.py` | `eb8c3aeb0ac26cc9` | 5723 |
| `vinculo_t01` | `...\work\bancada_vinculo_12out\bateria\t01_identidade.py` | `41bff7ab8b731621` | 3587 |
| `vinculo_t06` | `...\work\bancada_vinculo_12out\bateria\t06_pantheon_rounding.py` | `a71242ace974489b` | 2007 |
| `vinculo_t09` | `...\work\bancada_vinculo_12out\bateria\t09_nu4_replay.py` | `8903512b543a5aa6` | 4202 |
| `vinculo_t10_t11` | `...\work\bancada_vinculo_12out\bateria\t10_t11_canais.py` | `be1d88150555710f` | 4258 |
| `vinculo_t12_t14` | `...\work\bancada_vinculo_12out\bateria\t12_t14_atrator.py` | `00415a09ac5b6c99` | 5089 |
| `vinculo_t15` | `...\work\bancada_vinculo_12out\bateria\t15_sondas.py` | `2662806fe9142abb` | 5132 |
| `sandbox_SANDBOX_MANIFEST` | `...\work\bancada_vinculo_12out\sandbox\SANDBOX_MANIFEST.json` | `d374009160d35856` | 23836 |
| `sandbox_nos_sintetico_um_py` | `...\work\bancada_vinculo_12out\sandbox\nos_sintetico\um.py` | `0ea4e10728fde3c3` | 33910631 |
| `sandbox_nos_sintetico_selo` | `...\work\bancada_vinculo_12out\sandbox\nos_sintetico\um_absoluto_selo.json` | `a3e6aee34fbacd71` | 108511 |
| `F0.6_unidade_json` | `...\work\bancada_vinculo_12out\F0.6_unidade.json` | `a984dbd0ff1e53e9` | 4507 |
| `PLANO_V392_paragrafo_B3_md` | `...\work\bancada_vinculo_12out\PLANO_V392_paragrafo_B3.md` | `54134728176b45dd` | 5113 |
| `ATOS_DO_OPERADOR_md` | `...\work\bancada_vinculo_12out\ATOS_DO_OPERADOR.md` | `f6c53701c5bf31eb` | 3911 |
| `sandbox_saida_1_pre_selo_v391/RECIBO_SINCRONIZACAO_v391_20261012_200200.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\RECIBO_SINCRONIZACAO_v391_20261012_200200.json` | `4688aec36b1c2d06` | 41034 |
| `sandbox_saida_2_pos_selo_v392_sintetico/RECIBO_SINCRONIZACAO_v392_20261012_200310.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\RECIBO_SINCRONIZACAO_v392_20261012_200310.json` | `93ac47d8a0c5d1b9` | 39705 |
| `sandbox_saida_2_pos_selo_v392_sintetico/MANIFESTO_CANDIDATO_B3.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\MANIFESTO_CANDIDATO_B3.json` | `f71b88f508884adb` | 26954 |
| `sandbox_controles_negativos/CONTROLES_NEGATIVOS.json` | `...\work\bancada_vinculo_12out\sandbox\controles_negativos\CONTROLES_NEGATIVOS.json` | `66289f5bf52b34ee` | 6273 |
| `sandbox_canais_gerados/mcp_registros_gerados.py` | `...\work\bancada_vinculo_12out\sandbox\canais_gerados\mcp_registros_gerados.py` | `783bddb20ca337be` | 1113 |
| `sandbox_canais_gerados/registros_gerados.py` | `...\work\bancada_vinculo_12out\sandbox\canais_gerados\registros_gerados.py` | `08b54409bf62d5b7` | 9390 |
| `sandbox_canais_gerados/GERACAO_RECIBO.json` | `...\work\bancada_vinculo_12out\sandbox\canais_gerados\GERACAO_RECIBO.json` | `42af64a5ba261c09` | 708 |
| `sandbox_canais_gerados/SMOKE_TEST.json` | `...\work\bancada_vinculo_12out\sandbox\canais_gerados\SMOKE_TEST.json` | `f316db3ab6ed3e16` | 1348 |
| `sandbox_canais_gerados/TESTES_CANAIS_GERADOS.json` | `...\work\bancada_vinculo_12out\sandbox\canais_gerados\TESTES_CANAIS_GERADOS.json` | `f86203931a33b1e6` | 1748 |
| `sandbox_bancada_copia/canonical_contracts.json` | `...\work\bancada_vinculo_12out\sandbox\bancada_copia\canonical_contracts.json` | `f71b88f508884adb` | 26954 |
| `sandbox_bancada_copia/canonical_contracts.json.bak_B3_20261012_200310` | `...\work\bancada_vinculo_12out\sandbox\bancada_copia\canonical_contracts.json.bak_B3_20261012_200310` | `54fc9e27e4599c49` | 25917 |
| `sandbox_bancada_copia/CONTRATO_CANONICO_B2.md` | `...\work\bancada_vinculo_12out\sandbox\bancada_copia\CONTRATO_CANONICO_B2.md` | `8ffb684d4a268d06` | 2870 |
| `sandbox_bancada_copia/CONTRATO_CANONICO_B3.md` | `...\work\bancada_vinculo_12out\sandbox\bancada_copia\CONTRATO_CANONICO_B3.md` | `8f323f784f5c796b` | 1214 |
| `sandbox_saida_1_pre_selo_v391/recibos/T01_IDENTIDADE.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T01_IDENTIDADE.json` | `895e98bd4c9f92d8` | 1350 |
| `sandbox_saida_1_pre_selo_v391/recibos/T06_PANTHEON_FORMATO.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T06_PANTHEON_FORMATO.json` | `51dde7c42c0ffbbd` | 1052 |
| `sandbox_saida_1_pre_selo_v391/recibos/T07_NU3_CONTRATO.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T07_NU3_CONTRATO.json` | `0937bee05e187f8e` | 10153 |
| `sandbox_saida_1_pre_selo_v391/recibos/T08_ESCALA_BETA_CHI.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T08_ESCALA_BETA_CHI.json` | `275449a759b047a2` | 950 |
| `sandbox_saida_1_pre_selo_v391/recibos/T09_NU4_REPLAY.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T09_NU4_REPLAY.json` | `bf0ea08a8977b7c4` | 7146 |
| `sandbox_saida_1_pre_selo_v391/recibos/T10_T11_CANAIS.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T10_T11_CANAIS.json` | `549e65cd908a2634` | 1663 |
| `sandbox_saida_1_pre_selo_v391/recibos/T12_T13_T14_ATRATOR.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T12_T13_T14_ATRATOR.json` | `f56ce4acb00f5fea` | 3495 |
| `sandbox_saida_1_pre_selo_v391/recibos/T15_SONDAS.json` | `...\work\bancada_vinculo_12out\sandbox\saida_1_pre_selo_v391\recibos\T15_SONDAS.json` | `bda9e5745677c040` | 710 |
| `sandbox_saida_2_pos_selo_v392_sintetico/recibos/T01_IDENTIDADE.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\recibos\T01_IDENTIDADE.json` | `2e5985333b899185` | 1395 |
| `sandbox_saida_2_pos_selo_v392_sintetico/recibos/T06_PANTHEON_FORMATO.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\recibos\T06_PANTHEON_FORMATO.json` | `29b7a1fe19107051` | 1052 |
| `sandbox_saida_2_pos_selo_v392_sintetico/recibos/T07_NU3_CONTRATO.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\recibos\T07_NU3_CONTRATO.json` | `7d324a8186f09b79` | 10163 |
| `sandbox_saida_2_pos_selo_v392_sintetico/recibos/T08_ESCALA_BETA_CHI.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\recibos\T08_ESCALA_BETA_CHI.json` | `fde3556e75990e3b` | 950 |
| `sandbox_saida_2_pos_selo_v392_sintetico/recibos/T09_NU4_REPLAY.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\recibos\T09_NU4_REPLAY.json` | `2f650cae19af9306` | 7207 |
| `sandbox_saida_2_pos_selo_v392_sintetico/recibos/T10_T11_CANAIS.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\recibos\T10_T11_CANAIS.json` | `3d636844403341a1` | 1663 |
| `sandbox_saida_2_pos_selo_v392_sintetico/recibos/T15_SONDAS.json` | `...\work\bancada_vinculo_12out\sandbox\saida_2_pos_selo_v392_sintetico\recibos\T15_SONDAS.json` | `f5f5e2f22575f719` | 710 |


---

Nada aqui é leitura física, nada move o gate; um PASSA é validade na face testada. NOT_FALSIFIED nunca é creditação; a creditação é ato de quem observa de fora.
