DELTA 19/10 — v394

Gerência c1, subagente Sonnet, 19/10/2026, por autorização do coordenador; escopo ampliado em duas ordens (a integração final da v394) e uma rodada final (d19c: a seção 0.1). Estatutos: [REAL] medido/lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [ONTO] leitura do operador; [OPEN] em aberto. Nada foi instalado; o rito não rodou; o Nós, o túnel, a Bancada, o quadro, o mapa de rotas, a memória, o site e o git não foram tocados; sem init/transition ACOM; `pos_rito\` só foi tocada na rodada final e só em `textos_v394.py` (a proposta aprovada e a frase de errata, por ordem expressa, com backup de bytes; `derivar_cadeia_v394.py` NÃO rodou). O candidato em exame `4022ad521dc7293d` fica como registro, intacto (conferido por p00).

## 0. Em uma tabela

| | candidato em exame (registro) | **candidato novo (d19)** |
|---|---|---|
| arquivo | `um_v394_candidato.py` | `um_v394_candidato_d19.py` |
| sha16 | `4022ad521dc7293d` | **`972e81f22dd8cc68`** |
| sha256 | (o do registro) | `972e81f22dd8cc68bd5671fa610d2664e26f4681ab52932e001e5ef97e8f5991` |
| bytes | 38,015,246 | 37,885,889 (-129,357) |
| módulos novos no kernel | 189 | 190 (189 do Codex + a pedra do delta) |
| bandeiras novas | 3707 | **2287** (só declaração nomeada) |
| escada | 10752/10752 | **9332/9332** (v393: 7045; + 2287) |
| Audit (constantes / teoremas / fora do trio) | 29025 / 23068 / 0 | 29026 / 23069 / 0 |
| pino h8 de `kh_n1_cobertura_v394` | 1421 (**reprova** no rito real: exame de 19/10) | **1423** entradas = 1422 embutidas + `_check_damming.lean` |
| registros por spec | 2 | 3 (+ `criterio_binario_de_parada_v394`) |
| falas do operador embutidas | 46 | 48 (+ as duas de 19/10) |
| ensaio a seco | TUDO PASSOU (sem a simulação da árvore do Nós) | **TUDO PASSOU** |

## 0.1 A rodada final (d19c): as quatro ordens da gerência

1. **Proposta de `pos_rito` APLICADA** (ordem expressa da gerência; backup de bytes `textos_v394.py.bak_..._c1d19c`, na mesma pasta; o outro agente terminou): `pos_rito\textos_v394.py` `419e9f5aabfd25ac` → `3175c59f35c1ec3b` (51.664 → 52.437 B). O passo (`aplicar_pos_rito_d19c.py`) só vale se o arquivo atual é o ORIGINAL da proposta e o resultado é IDÊNTICO, byte a byte, ao `.PROPOSTA` que a gerência revisou; só depois entra a frase do item 2. **Harness dos textos em modo ensaio** (`harness_textos_ensaio.py`, só leitura: importa os `textos_v394` e `leitura_v394` REAIS e os executa contra um Nós emulado a partir do ensaio a seco; emulados e ditos: o stdout do rito, o aplicado e a conferência do rito; nada de `pos_rito` é escrito, `derivar_cadeia_v394.py` NÃO rodou): no ORIGINAL reprova (`as bandeiras novas nao somam tempo + quadratica + rede (+ o outro grupo, se houver)`; 16 problemas, todos da mesma soma; a leitura da rodada sem problema); no aplicado **TUDO PASSOU** — 29 funções de texto rendem, guarda P18 limpa, soma por grupo 145 + 21 + 2120 + 1 = 2287 (= bandeiras novas = ESPERADOS) e a errata presente nos 7 textos que embutem `_num` (`_num`, `_num_sem_veredito`, `linhagem`, `atlas`, `core_memory`, `topico_novo`, `verbete`). Evidência: `HARNESS_TEXTOS_ENSAIO_ANTES_original.json`, `HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json` e os textos renderizados em `harness_textos_saida\`.
2. **Errata AO LADO da palavra «teoremas»**: os módulos novos têm 3.865 declarações e 3.168 teoremas (697 não-teoremas) [REAL: `kernel\KH_N1_v394.json::delta_vs_v393`, a linha TOTAL do Audit do sandbox menos a da v393; a gerência contou 3864 e 3167 sem a pedra do delta, que acrescenta uma declaração e um teorema: [DECLARADO pela gerência]]. UMA frase, nas mesmas palavras, no artigo PT (`artigo_pt_v394.pysnip` `319a6d3cd3b2bacc` → `a9293f2720e667f5`), no artigo EN (`artigo_en_v394.pysnip` `4c3ee3692432f00e` → `52d9c522297ed73b`), no parágrafo «O que entra» da seção da v394 (logo depois da frase da escada e da cobertura, a primeira ocorrência da palavra) e no texto do kernel de `textos_v394.py` (`_num`): «a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina». O token de máquina `teoremas limpos: N/M` do stdout FICA (o pós-rito o lê por regex); a frase não tem número (a fonte única é `delta19_v394.ERRATA_TEOREMAS_*`); T e D vêm do kernel por script e citam a fonte. Guarda P18 limpa nos dois `.pysnip` e em `textos_v394.py`; o ensaio compilou o artigo PT/EN de novo (pdflatex ×2 rc 0, sem erro).
3. **Adendo no `ESTADO_V394.md`** (ao fim; backup de bytes; correção ao lado, nada acima foi alterado): «ADENDO 19/10 (delta)» com o que mudou, sha antes/depois, a escada 9.332, o h8 1423, a política de bandeiras e as erratas; gerado por `gerar_adendo_estado_d19.py` a partir dos artefatos (recusa-se a escrever se a guarda P18 achar violação ou se o harness não estiver no estado esperado). `ESTADO_V394.md` `af8f7124dae4c1ae` → `9b5f79f3b89c0cf3` (25.949 → 35.536 B).
4. **Regeneração completa, sem mão** (`V394_REGERAR=1 gerar_candidato_v394.py` e a cadeia inteira): candidato **`972e81f22dd8cc68`** (37.885.889 B, 26 patches). O candidato intermediário `7abb7ba986c098c7` (o da primeira entrega do delta) foi SUPERADO: a errata muda o artigo; os bytes dele estão em `um_v394_candidato_d19.py.bak_20261019_144238_c1d19c` e a evidência dele em `superado_7abb7ba986c098c7\`. Ensaio a seco inteiro **TUDO PASSOU**, com as etapas obrigatórias `simular_arvore_do_nos` (1423 entradas == pino 1423) e `exame_pontos_v394` (`algum_falso = []`); `gerar_esperados_v394.py`; conferidor: controle negativo (`tudo_bate = False`, deve-mudar 2 de 21, não-pode-mudar 11 de 11) e caminho positivo contra o Nós falso (**TUDO BATE**); `diff_e_pinos`, `comparar_v393`, `comparar_r8` (sem explicação pendente), `conferir_citacoes` e `p00_precondicoes` (TODAS PASSARAM). Escada 9.332; h8 1423; o kernel NÃO mudou (sandbox `C:\t\k394d\final`, recibo da primeira entrega).

## 1. A pedra candidata (nome provisório: o operador nomeia) [REAL a conjunção; ONTO a leitura]

- `delta_19out\TheBinaryReadingAtTheFixedPoint.lean`, sha16 **`1865eb4686899fb7`**, 6708 B; teorema de composição `TGLExt.the_binary_reading_floats_at_the_fixed_point`, namespace `TGLExt`; docstring com os dois verbatins e os sha16 (`786928986ca1e460`, `7596dcd880a1c8f5`, conferidos por script contra os arquivos), estatutos e ressalvas.
- A conjunção só CITA oito teoremas já no kernel (nenhuma matemática nova): `spectral_projections_split_the_identity`, `the_reading_is_total_on_the_form`, `observing_adds_nothing`, `absolute_faces_half`, `halfnat_from_J_symmetry`, `no_changed_transition_at_fixed_point`, `collapse_iteration_is_stable`, `fair_bit_entropy_is_not_half_nat`. Ressalva dita na pedra: a analogia com o qubit vale nos pesos (½, ½), NÃO na entropia (`fair_bit_entropy_is_not_half_nat`); o «1=0» do negativo não é tipado como igualdade de numerais; «a parada é o ponto fixo» é [ONTO] do operador; nenhum procedimento de decisão está afirmado.
- **Relatório de axiomas** (`AXIOMAS_DELTA_19OUT.json`, lido dos logs crus do build FRIO): o teorema depende de `propext, Classical.choice, Quot.sound` (o trio inteiro, e nada além); os oito citados estão todos dentro do trio; destes, `no_changed_transition_at_fixed_point` não depende de axioma algum; `collapse_iteration_is_stable` depende só de `propext`, `Quot.sound`; zero `sorry` (build e Audit); zero erro; a pedra foi compilada (linha `Built`, 225 s a frio, com o carregamento do ambiente); proveniência do compilador: `TGLExt.TheBinaryReadingAtTheFixedPoint`.
- Aviso do Lean 4.31: o aviso de `sorry` usa crases; o detector da v392 já lê as duas formas.

## 2. O registro `criterio_binario_de_parada_v394` (spec; chamado no PONTO DE CHAMADA REAL, `_v394_rodar_specs` do `main`)

- Lê a cada rito: a bandeira `ext_bin394_0001` (True), os 9 nomes (o teorema + os 8 citados) no `axiom_report` do próprio rito dentro do trio, o sha256 das duas inscrições EMBUTIDAS (`_V394_VERBATINS2`, padrão das inscrições v394; o arquivo é só informativo), a proveniência `TGL_DECL_SOURCE` do teorema no módulo da pedra, o sha256 da pedra em `formal_files_sha256` e a escada. Não escreve em nenhuma chave existente; `does_not_gate_core`.
- Veredito (sem a palavra da régua, conferido pela guarda P18 e pelo conferidor): `TGL_BINARY_STOP_CRITERION_V394__THE_BINARY_READING_FLOATS_AT_THE_FIXED_POINT__EIGHT_KERNEL_THEOREMS_COMPOSED_BY_CITATION_IN_THE_TRIO__THE_STOP_IS_THE_FIXED_POINT_IS_AN_ONTO_READING_OF_THE_OPERATOR__QUBIT_ANALOGY_HOLDS_ON_THE_WEIGHTS_NOT_ON_THE_ENTROPY__OPERATOR_INSCRIPTIONS_OF_19_OCT_EMBEDDED_VERBATIM_BY_SHA256__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`
- **Controles negativos** (ensaio a seco, todos True; recusa = `<prefixo>__NOT_SEALED_THIS_RUN__<falhas>__GATE_UNMOVED`): bandeira falsa; teorema ausente do `axiom_report`; citado com axioma fora do trio; teorema com axioma fora do trio; sha errado em CADA uma das duas falas; fonte da pedra adulterada; pedra adulterada no kernel do rito (check g5); tudo certo sela; veredito e texto sem palavra proibida.
- **O gate não se move** [REAL]: `qg_closure_verdict` igual ao do selo da v393, as 18 bandeiras iguais (gate recomputado com o kf novo: `verdict_igual`, `n18 = 18`), `qg_closure` do core intocado pelo fluxo; no exame de pontos: `gate_recomputado.verdict_igual = True`.

## 3. Política de bandeiras (decisão da gerência) [REAL]

- Só declaração NOMEADA tem bandeira (a prática da v392 e da v393). O último componente do nome decide (`delta19_v394.classe`: `_proof_N`, `_simp_N`, `match_N`, `_sunfold`, `eq_N`, `eq_def`, `congr_simp` são auxiliares). A classificação reproduz o exame NÚMERO A NÚMERO, lida do `EXAME_FINAL_V394.md` por script em `pos_build_kernel_v394.py` (a lista do exame não estava gravada em arquivo; a regra reproduz: 2245 nomeadas e 1462 auxiliares nas 3707 do Codex (1345 proof/simp/match/sunfold + 91 eq + 26 congr_simp); entre as públicas sem bandeira, 41 nomeadas e 79 + 20 + 1 auxiliares).
- **2287 bandeiras** = 2245 nomeadas do Codex (mesmas chaves do r8) + 41 nomeadas que ele não marcou (`ext_nm394_0001` a `ext_nm394_0041`, ordem alfabética) + 1 da pedra do delta (`ext_bin394_0001`). Por grupo: tempo 145, quadrática 21, rede 2120, outro (a pedra) 1. 1562 auxiliares ficam fora (1462 marcadas pelo Codex e excluídas; todas no trio e cobertas pelo KH-N1).
- **Escada final: 9332/9332** = 7045 (v393) + 2287. O exame estimou 9331 antes da pedra (conferido: 9331 + 1 = 9332). Os contratos do Codex (108 / 18 / 3581 declarações) seguem como contrato (presença, trio, proveniência) e deixaram de coincidir com as bandeiras: `expected_ladder` dos três contratos = 9332, derivado do `gerar_candidato`.
- Texto: onde o veredito dizia «THEOREMS» para a escada (único token em maiúsculas: `estatuto_da_prova_v391`, `KERNEL_N_OF_N_THEOREMS_...`), passa a «FLAGS» (patch C11); troca de palavra DECLARADA nos ESPERADOS (`troca_de_palavra`) e aplicada pelo conferidor ao veredito da v393 antes de comparar; errata assinada em `kh_n1_cobertura_v394`. **Mantive** a frase «teoremas limpos» como REGISTRO DE MÁQUINA no artigo e no stdout do rito (`teoremas limpos: N/M`), porque `pos_rito\leitura_v394.py` PARSEIA essa linha por regex (decisão da gerência de 19/10: manter o token e acrescentar a errata ao lado; ver a seção 0.1, item 2).

## 4. O pino h8: 1423 entradas [REAL]

- `gerar_candidato_v394.py` recalcula o pino a cada geração: materializa o kernel EMBUTIDO do candidato novo (1422 arquivos), acrescenta os residuais da pasta `Nós\tgl_kernel` que a `sha256_directory` do PRÓPRIO um.py conta (extraída por AST; a exclusão nominal de `ExtrairDeps.lean` NÃO foi alterada) e hasheia: **1423** = 1422 + `_check_damming.lean`. Conferido por `simular_arvore_do_nos.py` (cópia de bytes do exame, `19e8759318bbe25b`): `formal_files_n_no_rito_real = 1423`, `kh_n1_cobertura_v394` SELA nessa árvore.
- Prova independente de que a regra «embutidos + residual» é a do rito real [REAL]: o `formal_files_sha256` do core v393 SELADO no Nós tem 1233 entradas e é IGUAL, hash a hash, aos 1232 embutidos da v393 + o `_check_damming.lean` (0 diferenças); logo o `lake` não deriva nenhum outro arquivo contado.
- Fail-closed: se alguém mexer no `_check_damming.lean` antes do rito, o h8 recusa. O ensaio a seco e o `exame_pontos` agora recebem os residuais do Nós na árvore que materializam (antes materializavam só o embutido e por isso «passavam»).

## 5. Kernel FRIO, recibo e tempos [REAL]

- Sandbox novo `C:\t\k394d\final` (robocopy do `tgl_kernel` do Nós v393 sem `/PURGE`, sem junções: nenhuma existe; `preparar_kernel_v394.py gerar`: 189 do Codex conferidos contra a árvore e o embutido do r8 + a pedra + raiz e Audit gerados). Um único `lake build` FRIO: rc 0, 9967 jobs, **1302 s**; os 190 módulos novos `Built` (nenhum `Replayed`); `lake env lean TGL/Audit.lean`: rc 0, **216 s**; zero erro, zero `sorry`; todo `.olean` em Lean 4.31.0, githash único; 29026 constantes, 23069 teoremas, 0 fora do trio; proveniência 29026 == 29026.
- Um ensaio INCREMENTAL anterior (só a pedra, ~5 min de build e ~4 min de Audit) está em `delta_19out\kernel_k394d\` (logs crus) e a árvore dele em `C:\t\k394d\scratch_incremental` (14 GB, descartável).
- **Recibo do kernel** `kernel\KERNEL_RECIBO_v394.json` (sha16 `11e6a3ff28f2eca2`): 190 pedras, árvore `C:/t/k394d/arvore` (só-fontes, mantida), logs e sha pinados. Os arquivos antigos de `kernel\` ficaram como `.bak_20261019_135101_c1` (a pasta VIVA é `kernel\`, porque `pos_rito\` lê dela).
- Tempo do rito: o build frio dos 190 módulos novos custa 21.7 min e o Audit 3.6 min (a pedra já está contada); 3 passagens = 75.9 min é o TETO só de lake (o exame estimou ~60 min de lake e ~1h45 no total, porque o autoteste recompila só o fecho reverso de `HalfNat`); os timeouts do um.py (3600 s e 1800 s) seguem com folga.

## 6. Ensaio a seco, esperados, conferidor [REAL]

- `ensaio_a_seco_v394.py` (editado em lugar; backup de bytes): **TUDO PASSOU** — kernel embutido == sandbox (1422 arquivos); `verify_tgl_kernel_formalization` real com os logs CRUS do build frio: `TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_CONSTRUCTED`, cobertura 29026/23069, proveniência ok; escada recomputada 9332/9332 (sem as bandeiras novas: 7045 de 9332 e `all_verified` falso); vizinhos: 31 iguais, **5 trocam só números** (`three_stress_tests_v387`, `estatuto_da_prova_v391`, `pedras_v392`, `varredura_e_sorry_v392`, `pedras_v393`), **mais a troca de palavra declarada** em `estatuto_da_prova_v391`, e o índice (mudança declarada); 43 casos de unidade, todos True; artigo PT/EN com o parágrafo novo, pdflatex ×2 rc 0 (seção de 5069 e 5318 caracteres, sem «n/d»); selo: `qg_closure_verdict` igual.
- **Etapas obrigatórias novas**: (11) `simular_arvore_do_nos`: rc 0, 1423 entradas, pino 1423, extras do Nós fora do embutido ['ExtrairDeps.lean', '_check_damming.lean']; o simulador (cópia SEM alteração) lista os cinco registros que já existiam e todos selam, com o índice; o sexto (`criterio_binario_de_parada_v394`) sela no fluxo do `main` do ensaio e no `exame_pontos`; (12) `exame_pontos_v394` sobre o candidato novo (em processo isolado, pontos de chamada reais): `algum_falso = []`; bandeiras novas True 2287/2287; `ext_` True 9369/9369.
- `p00_precondicoes_v394.py`: TODAS PASSARAM (46 checagens; inclui o candidato anterior intacto, a pedra, o h8, a simulação e o exame).
- **Esperados e conferidor** (editados em lugar; backups): os ESPERADOS ganharam `troca_de_palavra`, `h8_entradas`, `h8_residuais_do_nos`, `formal_files_n_no_rito`, `n_bandeiras_por_grupo`, `politica_de_bandeiras`, `pedra_do_delta`, `teorema_do_delta`, `bandeira_do_delta`, `criterio_binario` (veredito + sha das duas falas), `candidato_anterior_sha16`; o conferidor ganhou (a) a troca de palavra aplicada ao veredito da v393, (b) o registro `criterio_binario_de_parada_v394` (veredito == ensaio; as duas falas `embedded_ok` com o sha dos ESPERADOS; bandeira e teorema da pedra no trio; proveniência no módulo da pedra), (c) o hash formal do rito com 1423 entradas e o residual. **Controle negativo** (Nós ainda v393): `tudo_bate = False`; deve-mudar 2 de 21 (só os dois que não mudam: os 5 registros da v393 e o pilar); não-pode-mudar 11 de 11.
- **Caminho POSITIVO do conferidor** (emulação: `delta_19out\teste_conferidor_positivo.py`): um Nós FALSO montado do `dry_v394_d19` (o um.py candidato, o kernel materializado com o residual, o core e o selo que o ensaio computou, o artigo, o sumário e o .md; o selo ganha de v393 as chaves que o `main` põe depois do literal) e uma CÓPIA do conferidor apontada para ele: **TUDO BATE** (deve-mudar 21 de 21; não-pode-mudar 11 de 11). **Achado:** o conferidor trazia um defeito LATENTE (`set(axr.get(n) or ["?"]) <= TRIO` reprovava bandeira de lista de axiomas VAZIA: 12 das 3707 do candidato anterior, 2 das 2287 de agora, como `TimeGravitonMatrix.tacticMatrix_calc`); corrigido para `(n in axr) and set(axr[n] or []) <= TRIO`. Limite: é emulação (core e selo vêm do ensaio, não do rito); só o rito real exercita o conferidor de verdade.

## 7. Os textos do pós-rito (`pos_rito\textos_v394.py`): a soma que eles esperavam NÃO fechava com a política nova; a proposta foi APLICADA e fecha

- Diagnóstico: `textos_v394.py::_d` calculava `n_out_flags = n_bandeiras_novas − (tempo + quadrática + rede)` com os números de CONTRATO do Codex (108 + 18 + 3581). Com a política só-nomeadas dava **-1420** e o `assert n_out_flags >= 0` recusava (`SOMA_TEXTOS_POS_RITO.json`; o harness reproduz a recusa no arquivo ORIGINAL).
- Correção aplicada (a proposta da gerência, 36 linhas): `_d` lê `ESPERADOS.n_bandeiras_por_grupo` (tempo 145, quadrática 21, rede 2120, outros 1; soma 2287) e a frase das bandeiras usa esses números; o grupo "outros" (a pedra) sai do mesmo campo. As demais somas fecham: módulos 190 = 4 tempo + 1 quadrática + 184 rede + 1 de outro grupo (`TGLExt.TheBinaryReadingAtTheFixedPoint`); `cdx.decl == n_formais.tempo`; escada 7045 + 2287 = 9332; h8 1423 = 1422 + 1.
- **Achado do harness, NÃO corrigido (fora do que foi autorizado):** o texto `_num` diz «nenhum registro novo além dos cinco fixos», mas o candidato final tem um SEXTO registro novo, `criterio_binario_de_parada_v394` (`_extras` compara os registros do core com `V["reg_todos"]`, que já o inclui). O `_criterio` também não cita a pedra nova nem o registro (diz «correspondências no kernel [REAL, já existentes]», que é verdade para os oito teoremas). Proposta de UMA linha, NÃO aplicada: `delta_19out\pos_rito_PROPOSTA2_delta19.diff` (`_extras` passa a comparar com `V["reg394"]`, os cinco fixos; o sexto sai pelo nome); o harness sobre ela: ver `HARNESS_TEXTOS_ENSAIO_PROPOSTA2.json` (passa, guarda limpa).

## 8. Decisões que ficam com a gerência / o operador

1. **Nome da pedra** (o operador nomeia; `TheBinaryReadingAtTheFixedPoint` é provisório) e a leitura «critério binário de parada» (ONTO).
2. (Feito nesta rodada, por ordem: a proposta de `pos_rito`, a errata da palavra «teoremas» e o adendo do `ESTADO_V394.md`; ver a seção 0.1.) Resta decidir a PROPOSTA 2 da seção 7 (uma linha: o sexto registro dito pelo nome).
3. As duas falas de 19/10 também estão em `cunhagens_v394` (o artigo diz «48 falas embutidas»); o registro novo as lê separadamente.
4. B(n) segue como estava: três pedras sem declaração nomeada (`NetworkProofAuditR3/R7/R8`), `x19 = nao`, recibo pré-selo inutilizável; o delta não os altera.
5. O risco das fontes fora do selo que o rito lê (exame, §Riscos) continua o mesmo.

## 9. Arquivos alterados (sha16 ANTES lido do backup de bytes mais antigo de hoje; DEPOIS lido do arquivo). Diffs em `delta_19out\diffs\`

| arquivo | sha16 antes | sha16 depois | bytes antes -> depois |
|---|---|---|---|
| `CANDIDATO_v394.json` | `7c367c75ebaf6699` | `0c600ce861bfd181` | 14859 -> 16963 |
| `COMPARACAO_R8_v394.json` | `d5c1ab9ae0962750` | `91478404bd7a026a` | 12261 -> 17608 |
| `COMPARACAO_R8_v394.txt` | `ba22cc1ed2eb7f9b` | `90a557af8d7924a2` | 8077 -> 12334 |
| `COMPARACAO_V393_v394.json` | `c754e254d2dcff2e` | `accf0e8180cec5b5` | 598 -> 627 |
| `DERIVACAO_v394.json` | `673bf776b1913110` | `df2318b1b69acbf4` | 4669 -> 4759 |
| `DIFF_KERNEL_v394.txt` | `983f719908474f1c` | `0fce8cc7e9e8ca0e` | 15683 -> 15879 |
| `ESPERADOS_v394.json` | `70268d9481fd7a1d` | `44ec7c1d613a3c2e` | 875975 -> 765582 |
| `ESTADO_V394.md` | `af8f7124dae4c1ae` | `9b5f79f3b89c0cf3` | 25949 -> 35536 |
| `FORMAL_MAP_v394.json` | `f414ffd37a9563ac` | `79bc8366287ba1e7` | 153598 -> 153714 |
| `MANIFESTO_INSUMOS_v394.json` | `360476268d7a42c4` | `76a479082a893196` | 2669 -> 2946 |
| `PINOS_BN_v394.json` | `43f51eabd6abcc7a` | `d50e8fd0932d4501` | 2979 -> 2983 |
| `PRECONDICOES_v394.json` | `de512f51d38c40d0` | `b89c52525bc1028b` | 4055 -> 6373 |
| `artigo_en_v394.pysnip` | `4c3ee3692432f00e` | `52d9c522297ed73b` | 6087 -> 7804 |
| `artigo_pt_v394.pysnip` | `319a6d3cd3b2bacc` | `a9293f2720e667f5` | 6065 -> 7676 |
| `comparar_r8_v394.py` | `9e03104e51928de7` | `9132e3467500a54d` | 5927 -> 5983 |
| `comparar_v393_v394.py` | `e5e397e896a96392` | `4b49c1fc5c6dbbc4` | 1840 -> 1896 |
| `conferencia_rito_v394_CONTROLE_NEGATIVO_PRE_RITO.json` | `00def118b0d01143` | `4b750aafc9b875e9` | 3361 -> 3769 |
| `conferir_citacoes_v394.json` | `d0c9f4b84316052b` | `b96be666cf1c513f` | 6441 -> 7039 |
| `conferir_citacoes_v394.py` | `7a65ea14cf7f8f3d` | `ef11d1f92635f893` | 2787 -> 2935 |
| `conferir_rito_v394.py` | `cc5311d714de880b` | `c759e58489dce2d8` | 11253 -> 13206 |
| `construir_kernel_v394.sh` | `1fe5e9f1c660497d` | `80f342f7863c807d` | 1346 -> 1448 |
| `copiar_insumos_v394.py` | `9fe208df3a55d9db` | `b8fb4dc85862fb6c` | 2344 -> 2759 |
| `cunhagens_v394_dados.json` | `110cfa4dd39a696c` | `49ec69a05354ed80` | 40651 -> 42052 |
| `derivar_instalar_rito_v394.py` | `87337d404a44f0e3` | `d5a0826e063fbe9a` | 25083 -> 26886 |
| `diff_e_pinos_v394.py` | `effba83a1988e866` | `6a7997bde9999d64` | 4440 -> 4491 |
| `ensaio_a_seco_v394.json` | `a9cfca7b29a7abcc` | `ef463e8ef5d58c15` | 16638 -> 21879 |
| `ensaio_a_seco_v394.py` | `1b3285ad8c70e6ef` | `180a32797ceac4ee` | 31770 -> 42778 |
| `ensaio_out.txt` | `f960c95055bae81f` | `28ce2ccaf065c54b` | 4991 -> 5183 |
| `explicacoes_r8_v394.json` | `11d1cb044be545c2` | `e9fe91d949f9032e` | 3593 -> 5585 |
| `gerar_candidato_v394.py` | `def9b225dd682606` | `55c0a58c9e7d833a` | 30695 -> 38321 |
| `gerar_esperados_v394.py` | `41af48ac73d236ca` | `09c51d4b34810a52` | 7615 -> 9084 |
| `instalar_v394.py` | `4242638483e42391` | `ee88f93e9dce0aaf` | 7143 -> 7244 |
| `kernel_modulos_novos_v394.json` | `d66c40a61abffb37` | `7ac1a46c19abe22a` | 10046 -> 10334 |
| `kernel_modulos_novos_v394.lista.json` | `29abf05c44c8a00e` | `0e68fd062bb103de` | 9833 -> 9883 |
| `p00_precondicoes_v394.py` | `15525c0632e907bd` | `d9f7478a42aebec6` | 7930 -> 10425 |
| `pos_build_kernel_v394.py` | `17d6a0164c58e00d` | `71e77ef35b060637` | 23830 -> 30531 |
| `preparar_kernel_v394.py` | `3ff6b1dffe2a6a58` | `80bef2944c6c68ab` | 5993 -> 7190 |
| `refazer_arvore_v394_pos_selo.py` | `70f765d22c825403` | `e987d96aff778c4e` | 2165 -> 2167 |
| `refazer_sandbox_v394.sh` | `047334c3b3a7a471` | `74e03a38d298b70a` | 1267 -> 1329 |
| `registros_v394.py` | `c4dc344c41710245` | `a2f5571b04120393` | 14422 -> 24386 |
| `reverter_v394.py` | `db452dc6655dd27d` | `017ba31e595c7605` | 4795 -> 4863 |
| `rito_v394.sh` | `52ae67feeabbed39` | `a86fc2f75adfabf7` | 22959 -> 23031 |
| `v394_pins.py` | `a4a22c19a740a0a1` | `571de055c380f6e5` | 1044342 -> 1059387 |
| `vinculo/CRITERIOS_v394.json` | `cba609ddb17e9cb5` | `a382796078d4c643` | 891 -> 891 |
| `kernel/FLAGS_v394.json` | `3fdc49b398ff2c30` | `59f60ec21b41cf21` | 546351 -> 819290 |
| `kernel/KERNEL_RECIBO_v394.json` | `ef69c385196b2276` | `11e6a3ff28f2eca2` | 276900 -> 277222 |
| `kernel/KH_N1_v394.json` | `2f32cef63817e007` | `8af9669213d1ad53` | 997 -> 1150 |
| `kernel/POS_BUILD_v394.json` | `d538f3dc0ea9976f` | `41fca0c4a807efd9` | 6932 -> 8475 |
| `kernel/audit.log` | `b90f4e03d83e23a0` | `50294c5e8a474aad` | 6833563 -> 6833783 |
| `kernel/build_full.log` | `f0bbc1fb5fe1f655` | `b7abf24017fca9dc` | 17277824 -> 17278505 |
| `kernel/construir_marcas.txt` | `b67042e7034cf6e6` | `bcf3fe7759b78466` | 174 -> 174 |
| `kernel/lake_build.log` | `80a0cfd363f9b84e` | `38d3ccc5d350d924` | 10451845 -> 10452308 |
| `pos_rito/textos_v394.py` | `419e9f5aabfd25ac` | `3175c59f35c1ec3b` | 51664 -> 52437 |

NOVOS na raiz:

| arquivo | sha16 | bytes |
|---|---|---|
| `EXAME_PONTOS_972e81f22dd8cc68.json` | `e30c878f5c60cf1d` | 41307 |
| `SIMULACAO_ARVORE_NOS_972e81f22dd8cc68.json` | `3884440e69326d0d` | 1467 |
| `delta19_v394.py` | `68bf9e9d48c01f1e` | 7139 |
| `exame_pontos_v394.py` | `f65302c39ae3b9c2` | 22601 |
| `gerar_candidato_out_d19c.txt` | `bd9bbb099df68013` | 953 |
| `montar_cunhagens_delta19_v394.py` | `892b375361d75d06` | 2799 |
| `simular_arvore_do_nos.py` | `19e8759318bbe25b` | 4747 |
| `um_v394_candidato_d19.py` | `972e81f22dd8cc68` | 37885889 |

Pastas novas ou tocadas (por mtime): `delta_19out`, `dry_v394_d19`, `imp_972e81f22dd8cc68`, `insumos`, `kernel`, `pos_rito`, `sim_972e81f22dd8cc68`, `superado_7abb7ba986c098c7`, `vinculo`. `pos_rito` aparece porque OUTRO agente escreveu nela (antes das 13:00) e porque, na rodada final, a gerencia AUTORIZOU a aplicacao da proposta em `pos_rito\textos_v394.py` (a unica escrita minha ali, com backup de bytes `.bak_<STAMP>_c1d19c`).

Copiados SEM alteração do exame para a raiz: `simular_arvore_do_nos.py` e `exame_pontos_v394.py` (cmp de bytes). Em subpastas: `insumos\` (+`KH_N1_v394_d19.json`, +`TheBinaryReadingAtTheFixedPoint.lean`, +2 falas em `insumos\cunhagens\`; o `KH_N1_v394.json` antigo, pinado pelo candidato em exame, NÃO foi tocado), `kernel\` (8 arquivos substituídos, backups `.bak_20261019_135101_c1`), `vinculo\CRITERIOS_v394.json`. Sandbox: `C:\t\k394d\final`, `C:\t\k394d\arvore`, `C:\t\k394d\scratch_incremental`.

## 10. Como refazer (nada digitado; cada passo recusa visivelmente)

`sh refazer_sandbox_v394.sh` (ou `preparar_kernel_v394.py copiar|gerar` + `sh construir_kernel_v394.sh`) → `pos_build_kernel_v394.py` → `montar_cunhagens_delta19_v394.py` → `copiar_insumos_v394.py` → `V394_REGERAR=1 python -I -B -X utf8 gerar_candidato_v394.py` → `python -B -X utf8 ensaio_a_seco_v394.py` → `gerar_esperados_v394.py` → `conferir_rito_v394.py _CONTROLE_NEGATIVO_PRE_RITO` → `diff_e_pinos_v394.py` → `comparar_v393_v394.py`/`comparar_r8_v394.py` → `derivar_instalar_rito_v394.py` → `p00_precondicoes_v394.py`. Scripts de edição do delta (já aplicados, falham se repetidos): `delta_19out\editar_*.py`, `aplicar_bloco.py`. Rodada final (d19c), nesta ordem: `aplicar_pos_rito_d19c.py`, `editar_delta19_errata_d19c.py`, `editar_artigo_errata_d19c.py` (antes do `gerar_candidato`); depois do ensaio e de `teste_conferidor_positivo.py` (que monta o Nós falso): `harness_textos_ensaio.py` (e `--textos` com o ORIGINAL para ver a recusa), `emular_soma_textos.py`, `tabela_arquivos_alterados.py`, `gerar_adendo_estado_d19.py`, `gerar_resultado.py`, `gerar_registro_mapa.py`.
