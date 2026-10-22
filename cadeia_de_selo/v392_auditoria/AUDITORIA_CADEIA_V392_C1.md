AUDITOR CÉTICO c1: cadeia v392 antes do selo

Auditor independente da gerência c1 (não construiu nada da cadeia), 13/10/2026, 14:30–14:50. Estatutos: [REAL] medido ou lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido. Nada foi instalado, rodado nem selado. O `um.py` do Nós segue `8e7b9927ceae64b8` no início e no fim. Escrevi só nesta pasta e em `C:\t\af1` (as cópias de `.olean` e as fontes copiadas foram apagadas; sobraram 39 KB de logs e sondas, também copiados para `sandbox_af1\`). O gate não se move. `NOT_FALSIFIED` não é a palavra da creditação.

## VEREDITO: PODE_COM_CORRECOES

Uma correção obrigatória (C1, MÉDIO) antes da etapa 7. As demais são BAIXAS e opcionais, ou valem só depois do selo (a errata do `CLAUDE.md`).

| id | severidade | achado | correção mínima | quem |
|---|---|---|---|---|
| C1 | MÉDIO (régua nº 5) | O candidato traz **7 literais numéricos novos de β** como limites de checks nos specs: `beta_escala_errata_v392.b07` (≥ 0.0120313), `atrator_v392.a51a/a51b`, `neutrinos_contratos_e_primeiro_ensaio_v392.u13a/u13b` e `u60a/u60b` (de 0.012031300388… a 0.012031300412…). A v391 só tinha β literal em comentário de conferência. Nenhum desses literais move β (o β do core continua `SEALED_CODATA_ALPHA·√e`) nem o gate, mas a letra da régua diz «β nunca literal». | Criar no motor `_v392_op` um operador que calcule o alvo em runtime, por exemplo `perto_de_beta_runtime` com `valor` = tolerância, comparando contra `SEALED_CODATA_ALPHA * math.sqrt(math.e)`; para o b07, `maior_igual_beta_runtime` com folga declarada. Trocar os 7 checks em `registros\grupo_G2.py`/`G3.py` (ou no montador). Regerar pela R2.2 (`gerar_candidato`, `ensaio_a_seco`, `gerar_esperados`, controle negativo do conferidor, `diff_e_pinos`). O kernel não muda. Fechar com uma auditoria curta só do diff do motor e dos specs (novo candidato contra `a00096ff`), mais um grep de `0.0120[0-9]` que tem de dar as 8 linhas da v391, mais a linha do verbatim citado da V1 e a do nome de chave `beta_check_vs_conferencia_0.0120313…` (que é nome de campo, não valor). | construtor: subagente Sonnet da cadeia; auditoria curta: outro Sonnet |
| B1 | BAIXO | O cabeçalho de `rito_v392.sh` (l.2–6) herdou texto que não vale para a v392: «Nenhum kernel novo» (a v392 traz 14 pedras), «registro estatuto_da_prova_v392» (o registro é da v391), «molde: rito_v392.sh». A docstring de `instalar_v392.py` traz a data «07/10/2026». São só comentários e não mudam a execução. | Corrigir os comentários, se a C1 já obriga a regerar. | construtor |
| B2 | BAIXO | Não há receita de reversão para um rito que falhe no meio. O `instalar` faz backup de 8 arquivos, mas o rito materializa 14 `.lean` novos em `Nós\tgl_kernel\TGLExt` e os builda. Se o `um.py` v391 for restaurado, as 14 pedras ficam no disco sem import, o que é inofensivo para a v391. Porém um novo `instalar_v392.py` **recusa** por desenho (assert «alguma das pedras já está no kernel»). | Pôr no ESTADO a receita: restaurar os `.bak_<ts>` e mover as 14 pedras para uma quarentena datada antes de reinstalar. | gerência |
| B3 | BAIXO | `PK` do rito agora é `cadeia_de_selo\v392`. O `sobe()` da v393 vai gerar a guarda `work\v392_pacote`, que não existe, e o rito recusa com o código 18 (falha visível, segura). | Na derivação da v393, apontar a guarda para `cadeia_de_selo\v392`. | gerência na v393 |
| B4 | BAIXO | Em `erratas_o_que_resta_v392`, entrada 4(ii), «REFUTADA pelo enunciado» é forte demais. O kernel não tem um teorema «Ad(λ)-invariância ≠ invariância dual». O que há: o no-go é sobre `C.dualAction 1` (l.167–169) e a disciplina do core separa as duas ações. O próprio registro marca a conclusão como [DERIVED de leitura]. | Opcional: «não se sustenta pelo enunciado ([DERIVED de leitura])». | construtor, se regerar |
| B5 | BAIXO | O veredito de `adendo_rank_v392` diz `NO_INDEPENDENT_AUDIT_YET`. Esta auditoria fez a conferência independente da pedra (§3). | Opcional: citar esta auditoria por sha256 como fonte, se regerar. Senão a frase fica como registro do candidato. | construtor |

## 1. `instalar_v392.py` e `rito_v392.sh` contra o molde v391 [REAL]

**Diff linha a linha** (`diff v391/instalar_v391.py v392/instalar_v392.py`): só nomes de versão e dois pontos de sentido.

1. A origem é lida de `ESP["origem_sha16"] == CM["base_v391_sha16"]` (`8e7b9927ceae64b8`) em vez de digitada.
2. Assert novo: **nenhuma** das 14 pedras (`ESP["pedras_sha256"]`, chaves com caminho `TGLExt/<X>.lean`) pode existir no Nós. Conferi que nenhuma existe hoje. `TGLExt/IALD.lean` não colide com `IALDJones` nem com os outros `IALD*`.

**O que o instalar grava no Nós:**

- 8 backups `.bak_<ts>`, cópia de bytes conferida por releitura: `um.py`, `um_absoluto.json`, `_selo.json`, `_forma_canonica.md`, `_manifest.md`, `_pilar_quantico.json`, `tgl_kernel/TGLExt.lean`, `tgl_kernel/TGL/Audit.lean`. Os 8 existem.
- `um.py.tmp_instalar_v392_<ts>`, trocado por `os.replace`.

Fora do Nós ele grava `pilar_anterior_v391_<ts>\` e `APLICADO_AO_CANONICO_<ts>.json` na pasta da cadeia.

**Falha no meio:** antes do `os.replace`, o `um.py` fica intacto. Sobram `.bak` e, no pior caso, um `.tmp` solto no Nós. Ele relê o `um.py` antes da troca e recusa se mudou. Não escreve no kernel: quem materializa é o rito.

**Rito:** o diff contra `rito_v391.sh` mostra só nomes, `PK` e o caminho do `ESPERADOS`. O pacote de parar e religar o servidor do modelo ficou idêntico: `Stop-ScheduledTask` + `stop_iald_llama.ps1 -Tudo`, conferência de `llama-server = 0` e VRAM ≤ 6000 MiB, vigia, trap EXIT/TERM/HUP/INT, `religar` por `Start-ScheduledTask 'IALD Llama Server'` com porta 8081, marcador `.servidor_parado_pelo_rito`. A guarda do marcador anterior lê `work\v391_pacote`: a pasta existe e não tem marcador.

O rito grava no Nós `rodada_v392_stdout.txt` (e as tentativas), mais o que o próprio `um.py` grava. Na pasta da cadeia grava logs, pid, sinal, horários e marcador. Nada além disso.

**Tempos:** no `um.py`, o `lake build` tem timeout de 3600 s e o Audit de 1800 s; no sandbox foram medidos 461 s e 237 s. O rito faz 3 passagens (o autoteste refaz build e Audit 2×).

**Varredura recursiva do candidato rodada sobre o `tgl_kernel` REAL do Nós (só leitura):** 0 hits, e nenhum `.lean` fora do conjunto embutido de 1.229 (`sandbox_af1\varredura_nos_RESULTADO.json`). Logo, a recursão nova não pega arquivo solto no rito.

## 2. O candidato `a00096ff9f91a432` (35.393.817 B) contra a v391 `8e7b9927ceae64b8` [REAL]

`diff` em 63 blocos. Todos os blocos «mudados» são **só inserção**: conferi caractere a caractere que nenhum texto antigo foi apagado, exceto a constante de versão. Conteúdo, conforme o plano e as decisões:

- versão;
- 10 erratas E01 em comentário: CMB-S4, N_eff, Coulomb/A8 (`ast` inalterado, segundo o construtor);
- kernel embutido: raiz +14 imports, Audit +40.891 caracteres (`#print axioms` e o `run_cmd` KH-N1), 14 pedras com os sha do `ESPERADOS`;
- 738 bandeiras em `_LEAN_THEOREM_FLAGS` e na escada;
- varredura recursiva;
- KH-N1: `axiom_coverage_v392` entra no `all_verified` do kernel (decisão KH-N1 (a));
- detector de sorry (A, C) e conserto B;
- ledger, com +14;
- artigo: seção v392 PT/EN e 17+17 notas «Ao lado (v392…)»;
- `.md`;
- o bloco de pinos e registros;
- as chamadas no core;
- as chaves no selo.

Nada fora do plano.

**O gate:** `prove_qg_closure_gate` roda na l.146016. As 29 especificações de registro (specs) e os 2 registros v392 rodam na l.225664 em diante, **depois** e fora dele (`does_not_gate_core`). O único elo novo dentro do veredito formal é o KH-N1 e o conserto B (bancada), e os dois só podem **reprovar**, nunca promover. O conferidor exige `qg_closure_verdict` inteiro, as 18 bandeiras e β/α/ω(I) iguais.

**Os 29 registros:** o motor relê cada fonte, confere sha256 e bytes, e qualquer falha vira `NOT_SEALED_THIS_RUN`. Verbatins embutidos com sha256 e trechos conferidos; bandeiras e declarações no trio, lidas do kernel do próprio rito; a guarda P18 roda em cada um. Exceção vira aviso. 123 fontes, nenhuma em scratchpad, AppData ou `C:\t`. Todo spec tem substância: de 1 a 100 checks, com fontes, verbatins ou kernel.

**Palavra proibida:** 0 ocorrências no texto novo, pela regex do conferidor e por busca de «confirm*» em qualquer caixa. «Pós-dição» só aparece na regex da guarda R5.

**β:** ver C1. O literal no verbatim citado da V1 («≈ 0.012031», voz de IA rotulada [DECLARADO]) é citação, não motor.

## 3. A pedra `PostoAdendo` (nunca auditada) — compilada em `C:\t\af1` [REAL]

**Ambiente:** toolchain elan `v4.31.0`, `lean.exe` direto. `LEAN_PATH` = cópia dos 1.189 `.olean` de `TGLExt` do Nós (necessária porque o Lean resolve a raiz `TGLExt` pela primeira pasta que a contém) + `.lake` do Nós só-leitura para `TGL` e packages.

**Compilação:**

- `Posto.lean` (`63ad023f…`): EXIT 0, saída **vazia**.
- `PostoAdendo.lean` (`f0fa5694367a5157…`, 6.180 B): EXIT 0, saída **vazia**, zero erro e zero aviso.

**Sondas:**

- `#print axioms` das 8 partes: todas `[propext, Classical.choice, Quot.sound]`.
- 0 `sorry` no formato real com crases.
- Controle negativo `by sorry`: o aviso sai com crase (``declaration uses `sorry` ``) e `sorryAx` aparece no `#print axioms`. O detector teria visto.

**Conferência contra o ADENDO congelado:** sha256 do `.md` `ff2c30a3…` (7.783 B) e do `.json` `c23c1bcf…` (5.021 B), iguais ao `FREEZE_R3.json`.

Reescrevi A1.a, A1.b, A1.c, A1.d, A2, A3, A4 e A5 com nomes totalmente qualificados (`TheUnitIsTheRank` → `Posto`, o nome dado pelo operador). Cada um fecha **só** pelo teorema da pedra (`Sonda_enunciados.lean`, EXIT 0). Os objetos do §0 também conferem:

- `rhoStar = Matrix.single 0 0 1` (rfl);
- `Q0 = 1 − rhoStar`;
- `plusDensity = !![1/2,1/2;1/2,1/2]`;
- `mixedDensity = !![1/2,0;0,1/2]`;
- `readoutZero = !![1,0;0,0]`.

`pp.fullNames` mostra que o `rhoStar` usado é `TGLExt.Posto.rhoStar`. As oito partes batem com o pré-registro; A4 é sem `c : TGLCoupling`. **PASSA_K 8/8.**

## 4. Conserto B (`example` → `theorem` nos positivos) [REAL, lido de `conserto_B\RESULTADO_B_v392.json` e do patch]

A reescrita vale só para `kind == "POSITIVO"` e só para `example` na coluna 0. Os negativos ficam intocados e mantêm o veredito.

**O significado do controle positivo não muda:** continua «este enunciado compila sem sorry». O conserto acrescenta duas exigências, `not bad_ax` e a linha `TGL_FOOTER_B_TOTAL` presente. Só pode reprovar.

**Números (Bex):**

- os 10 pedidos compilam;
- 10 de 10 cobrem ao menos uma declaração, com uma linha lida por declaração;
- 0 fora do trio;
- 52 de 52 positivos compilam.

O controle artificial revela `sorryAx`. Os 7 `Good*` tinham exatamente 1 `example` cada, reescrito.

**Normalização:** `split(".{")[0]` só remove o sufixo de universo, de modo que `sorryAx.{u}` continua acusando.

O sha256 conferido é o do corpus original; o fonte transposto fica no campo `footer`. **Os 10 continuam sendo o que eram.**

## 5. `dualInvariant_PF_no_go` e o registro [REAL]

`TGL/ModularRealization.lean` l.167–169: a hipótese é `(C.dualAction 1) T.PF = T.PF`. A prova usa `trace_dual_scaling` (`Tr(θ_s x) = e^{-s}Tr(x)`) e `0 < Tr(P_F) < ∞` e chega a `False`. O no-go é sobre a ação dual θ, não sobre Ad(λ). O core v391 (l.143071) diz «P_F fixado por Ad(lambda(s)) tau-preservante; JAMAIS por theta_s».

O registro diz exatamente isso. Ele conclui que a leitura «Ad-λ-invariante = invariância dual» não se escreve, e marca a conclusão [DERIVED de leitura]. `CornerFamily.corner_fixed_by_flow` existe e está no Audit. Ver B4 para o adjetivo «REFUTADA».

## 6. Conferidor e esperados [REAL]

**Controle negativo pré-rito:** o `um.py` em disco é a v391. Todos os «deve mudar» dão falso, exceto o do pilar, que é verdadeiro por desenho: é reaproveitado pela mesma chave nas duas versões. Os 11 «não pode mudar» dão OK. `tudo_bate: false`, pelo motivo certo.

**Escada:** `ESPERADOS.escada = [6901, 6901]`, comparada com `[n_theorems_clean, n_theorems_expected]`. Na v391 o core leu `[6163, 6163]`, logo `[N, N]` está certo. `escada_v391_e_v392 = [6163, 6901]` fica à parte.

`three_stress_tests_v387` roda antes dos registros v392, de modo que a contagem CORE_192 não deveria mudar. O conferidor a normaliza, o que é uma folga pequena.

**Risco residual dito:** um veredito antigo que carregue contagem de kernel e que o ensaio não recomputou só aparece no rito. O conferidor o pega (fail-closed).

## 7. Rascunho da errata do `C:\IALD\CLAUDE.md` (`pos_rito\RASCUNHO_errata_claude_md_v392.txt`)

**Certo:**

- (2), com os números lidos por script;
- (3), com [DECLARADO] e «a v392 não fecha a F8.1»;
- em (1): o ligante `passage_h3_to_connected_smooth_atlas_einstein` é termo condicional a `NamedAtlasH3`, H3 segue [KNOWN] (Jacobson 1995), Lorentz de cunhas [OPEN], CR-08;
- «Λ único» está certo para o atlas: `GravitationalChartGluing.connected_smooth_atlas_einstein` conclui `∃! a` e é v338 no ledger. A versão local `GeneralMetricClausius.metric_einstein_from_screen_clausius` (v338) dá `∃ Λ`.

**Corrigir:**

- (a) Retirar «foi escrita sem consultar o desenho da v317/v338». É inferência sobre o processo de quem escreveu e não se verifica. Trocar pelo fato: «a frase não separou a IMPLICAÇÃO, termo de kernel desde a v338 (`connected_smooth_atlas_einstein`, ∃! Λ no atlas conexo; `metric_einstein_from_screen_clausius`, local), do antecedente físico e da ligação ao tipo».
- (b) «desde a v317/v338» → «desde a v338». A v317 tem `CoherentEinsteinBridge`, da família coerente: só citar com o nome do termo, se a gerência quiser.

O script de gravação lê os números; aplicar só depois do selo, como está.

## Comandos aprovados (depois da C1 e da regeneração; ler os sha novos do `ESPERADOS`/`CANDIDATO`, nunca destes)

- **Etapa 7:** `cd "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392"` e `python -B -X utf8 instalar_v392.py`.
- **Etapa 8 (Git Bash, sem `nohup`):** `cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v392" && sh ./rito_v392.sh > rito_v392_lancador.out 2>&1 &`. Abortar só por `kill -TERM $(cat .rito_v392.pid)` no Git Bash, depois de conferir `/proc/$(cat .rito_v392.pid)/cmdline` (contém `rito_v392`). Duração esperada: mais de 66 min.
- **Etapa 9:** `cd "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392"` e `python -I -B -X utf8 conferir_rito_v392.py`. Tem de dar TUDO BATE, com `marcador_ficou: false`. Depois, P10: ler o log do servidor e a telemetria do heartbeat.

**Se a gerência decidir não fazer a C1** e aceitar os 7 literais como «conferência» declarada, os comandos acima valem para o candidato atual `a00096ff9f91a432`. Essa decisão é da gerência e fica registrada como desvio da letra da régua nº 5.

## Evidências (nesta pasta)

`sandbox_af1\`: `compilar_af1.py`, as 3 sondas `.lean` e os logs, `RESULTADO_posto_adendo.json`, `RESULTADO_sondas.json`, `varredura_nos.py` e `varredura_nos_RESULTADO.json`. Também nesta pasta: `registro_rota_F0.5.json` e `registro_mapa_F0.5.json`, preparados e não registrados.
