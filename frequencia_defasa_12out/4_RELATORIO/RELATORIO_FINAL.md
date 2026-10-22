# RELATÓRIO FINAL — F1.FREQUENCIA (trilha POSTO)

**Para:** o operador (Luiz). **De:** o redator da unidade (subagente da gerência c1), em nome próprio. **Data:** 13/10/2026, madrugada (hora local), depois da rodada 2 dos construtores e das duas auditorias céticas da rodada 2.
**Pasta:** `C:\IALD\Central de Patentes\work\frequencia_defasa_12out\4_RELATORIO`. Este relatório escreve só aqui. Nada foi tocado no quadro, no mapa (os dois registros ficam gravados aqui, não registrados), na memória, no túnel, no Nós, no kernel do Nós, na Bancada_Um, no site ou no git.

**Leitura obrigatória antes de qualquer frase abaixo:** cada PASSA é **validade matemática na face testada** (kernel Lean em sandbox, modelo ótico 2×2 em numpy/mpmath), **não creditação**. Nada aqui move o gate, nada fala da natureza, e nenhum número de runtime recebe o nome de prova. As três FALHAs são negativos honestos **pré-registrados antes do ensaio** e provados como negação no kernel.

---

## 0. O que esta unidade testou, em uma frase

A cunhagem **POSTO = RANK** (V3, 10/10) e a dinâmica **Tudo = D_β(F(1))** (V4, 11/10) foram traduzidas, por pré-registro congelado em hash **antes** de qualquer ensaio, em 38 partes verificáveis (P1–P4 sobre posto, nulidade, pureza e leitura; B1–B9 sobre a unidade ρ*, o anticomutador {Q_θ, ρ*}, o vazamento β, a fractalização F = Ad S(θ), a defasagem D e os dois regimes; O1–O2 sobre o que não se testa), e cada parte foi ensaiada em duas faces independentes — o **kernel** (pedra Lean nova, `TheUnitIsTheRank.lean`, 177 teoremas + 13 definições, só os três axiomas de Lean, zero `sorry`) e o **modelo ótico** (2.000 estados sorteados, 60.502 pares de leitura, 12 ângulos, 7 tempos, mpmath a 50 dígitos em θ_M) — e depois auditada por dois céticos independentes (lente reprodução; lente estatuto e regra), que reproduziram tudo, compilaram a pedra de novo (mesmo `.olean`, bit a bit) e sondaram o contrário.

**Resultado em números [REAL, lido dos artefatos por hash]:** 29 PASSA · 3 FALHA pré-registradas (negativos honestos) · 1 CITADO · 3 CITADO_REAL · O1 NAO_TESTAVEL · O2 ABERTO · controles 14 de 14 falham sem a hipótese, como devem · duas auditorias dizem **pode fechar** (uma sem achado material; a outra **com ressalvas de texto e nome**, nenhuma de enunciado ou prova).

**O achado que importa para o operador (seção 6):** no cânone, o «1» que sobrevive à defasagem e ao colapso tipado é o **TRAÇO** — ω(I) = 1, o POSTO no sentido de 05/10 (posição, inscrição). O **posto 1** (rank) é propriedade do **átomo** (estado puro, projetor de posto 1) e **não sobrevive** à defasagem: D_∞F_θ(1) = diag(cos²θ, sin²θ) tem posto 2 sempre que sin 2θ ≠ 0 — e em θ_M isso dá diag(1−β, β). Logo **POSTO = RANK vale exatamente no átomo**, onde o nome (Tr ρ = 1) e o índice (Tr ρ² = 1) coincidem; fora dele, o traço é cego ao posto e o posto 1 só volta pela **leitura seletiva** (Lüders, P3). A frase de V1 l.7 («Ao colapsar a superposição … ganha posto definido») é verdadeira lendo «colapsar» como o ramo **selecionado** e «superposição» como a **mistura** de posto cheio; a superposição **pura** já tem posto 1, e o colapso tipado do próprio cânone (`Collapse057.qubitReduction` = `nameOp ρ*` = D_∞) a leva de posto 1 a posto 2, preservando só o traço. Esse é o conteúdo novo, com peso, que sobe para a v392.

---

## 1. Pinos e integridade [REAL — medidos aqui por script, `scripts_r2\pinos_r2.py` → `PINOS_R2.json`]

| objeto | bytes | sha256 (16 primeiros) | confere com o FREEZE |
|---|---|---|---|
| V1 `OPERADOR_10out_posto_rank_texto_verbatim.txt` | 2.937 | `8d252f24e2806ff3` | sim |
| V2 `OPERADOR_12out_rank_e_tempo_santo_verbatim.txt` | 6.673 | `2c8b7b712aa9ad7f` | sim; recorte l.1–33 = 2.852 B, `aa132de8c79f8e8b`; a l.34 começa em «O que mais me fascina» |
| V3 `OPERADOR_10out_posto_rank_verbatim.txt` | 10 | `5b9afcc691a0e1e4` | sim («POSTO=RANK», sem espaços) |
| V4 `OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt` | 1.942 | `b365591ceb346cdf` | sim |
| `1_PREREGISTRO\PREREGISTRO.json` | 46.753 | `0c20d7c196a4c7ef` | sim |
| `1_PREREGISTRO\PREREGISTRO.md` | 27.071 | `3c80ea21057c3371` | sim |
| `1_PREREGISTRO\FREEZE.json` (congelado 2026-10-12T16:22:52.525Z) | 3.993 | `4d8f97537eb04cd5` | — |
| `2_OPTICO\RESULTADO_OPTICO.json` (rodada 2) | 137.290 | `28758b3eebdac631` | — |
| `2_OPTICO\run_optico.py` | 113.600 | `48a8d8b0d9fd125b` | — |
| `3_KERNEL\rodada2\RESULTADO_KERNEL.json` | 82.922 | `9fd3c2044e410a57` | — |
| pedra r2 `3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean` | 103.662 | `3195ef8f0766384c` | — |
| `.olean` r2 `3_KERNEL\rodada2\olean\TheUnitIsTheRank.olean` | 5.061.736 | `d0830b4bc03dc561` | igual ao recompilado pelos DOIS auditores |
| pedra r1 (registro) `3_KERNEL\sandbox\TGLExt\TheUnitIsTheRank.lean` | 87.563 | `617155151fb0d9e1` | — |
| `um.py` v391 | 33.910.631 | `8e7b9927ceae64b8` | sim |
| `um_absoluto.json` (core v391) | 5.003.275 | `a74241ff380b1b0e` | sim |
| `um_absoluto_selo.json` | 113.926 | `95061f18c7102248` | sim |
| sonda do auditor de estatuto `AuditorEstatutoR2.lean` | — | `512ea820918c178f` | copiada em `auditorias_copia\POSTO_AUD_ESTATUTO\r2\sandbox` |

- **β em runtime [REAL]:** a atribuição `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3` é a linha única 5557 dos bytes do um.py (igual a `SEALED_CODATA_ALPHA`, l.95); β = α·√e calculado aqui dá `repr` `0.012031300400803142`, igual ao texto de conferência do pré-registro; θ_M = arcsin√β = `0.10990843077787468`; o `leak_sin2_thetaM` do core v391 é **igual a β bit a bit**; |β − 0,012031| = 3,004e-7 (o 0,012031 foi lido dos bytes de V4, l.16). Nenhum script desta unidade traz β literal (varredura dos 55 arquivos de código pelos auditores; a minha pasta é varrida em `AUTO_AUDITORIA_REDATOR_R2.json`).
- **Ordem do tempo [REAL, auditor de reprodução]:** FREEZE às 16:22:52.525Z; o arquivo mais antigo de 2_OPTICO é de 16:31:07Z (+495,5 s) e o de 3_KERNEL de 16:30:36Z (+463,7 s); nenhum arquivo com mtime ou birthtime anterior ao FREEZE; 27 arquivos citam o hash do FREEZE e 50 o do PREREGISTRO.json. O levantamento anterior (0_LEVANTAMENTO) só rodou `#check`/`#print` — nenhuma afirmação foi ensaiada antes do congelamento.
- **tgl_kernel intacto [REAL]:** impressão digital medida agora (`IMPRESSAO_DIGITAL_KERNEL_REDATOR_R2.json`): 132.088 arquivos, metadados `a15d5e02d4f22bd6`, conteúdo dos 1.213 `.lean` fora de `.lake` `ca632c47de569952` — **idêntica ao FREEZE** e às medições de construtores e auditores antes, depois e após a limpeza. Toolchains, `.lake` e builds copiados foram apagados por quem os criou (recibos nos RESULTADOs e em `LIMPEZA.json`); nenhum `.lake` novo existe nas pastas copiadas (`MANIFESTO_COPIA_AUDITORIAS_R2.json`: 0 pastas vedadas).
- **Mapa de rotas [REAL, só leitura]:** consultei «posto_e_defasagem», «F1.FREQUENCIA», «TheUnitIsTheRank», «fractal_dephasing», «anticomutador», «posto rank» → 0 rotas cada (1.042 registros, cabeça `55530e87323c3a62`); «defasagem» → 1 rota (`kernel.inventario.cadeia_beta_v376`, que inventaria β no kernel, não esta trilha). O livro cresceu só por acréscimo desde o FREEZE (1.004 → 1.042; os seq 1041–1042 são `infra.bancada_um…` da gerência, não desta unidade). **A rota desta unidade ainda não existe no mapa**: os dois registros estão prontos aqui (seção 9).
- **ACOM [INPUT do redator]:** README lido. Não houve `init` nem `transition`: a ordem proíbe escrever na memória e a referência desta tarefa é da gerência c1. A inscrição desta etapa é ato da gerência.
- **Custódia das auditorias [REAL]:** as pastas r2 dos dois auditores (209 arquivos, scratchpad efêmero) foram copiadas byte a byte para `auditorias_copia\POSTO_AUD_REPRO\r2` e `auditorias_copia\POSTO_AUD_ESTATUTO\r2`, todas iguais à origem. As cópias da rodada 1 (feitas pelo redator da rodada 1, `MANIFESTO_COPIA_AUDITORIAS.json`) ficaram intactas.

---

## 2. Tabela por afirmação

Colunas: **pré** = esperado no pré-registro congelado; **O** = face ótica (rodada 2, `RESULTADO_OPTICO.json`); **K** = face kernel (pedra r2, termos citados); **audR** = auditoria de reprodução (confere?); **audE** = auditoria de estatuto (ressalva?); **final** = veredito da parte pela regra (f) do pré-registro (PASSA ⟺ PASSA_K e PASSA_O; onde há uma face só, ela decide).

| id | enunciado (resumo) | pré | O | K (termos) | audR | audE | **final** | estatuto do conteúdo |
|---|---|---|---|---|---|---|---|---|
| P1.a | ρ ⪰ 0, Tr ρ = 1: Tr ρ² = 1 ⟺ posto 1 ⟺ ρ² = ρ | PASSA | PASSA_O (2.000 estados, 0 violações) | `pure_iff_rank_one`, `pure_iff_idempotent`, `pure_core` | confere | — | **PASSA** | [KNOWN] Nielsen & Chuang Ex. 2.71; termo novo [REAL] |
| P1.b | M₂: Tr M² = (Tr M)² − 2 det M; Tr M = Tr M² = 1 ⟹ posto 1 (sem positividade) | PASSA | PASSA_O (resíduo 7,3e-15; 1.013 M′) | `trace_sq_fin_two`, `pure_iff_rank_one_fin_two` (vale o ⟺) | confere; sonda S2.3: sem Tr = 1 cai | — | **PASSA** | [KNOWN] Cayley–Hamilton 2×2; termo [REAL] |
| P1.d | ψ ≠ 0 ⟹ posto \|ψ⟩⟨ψ\| = 1 | PASSA | PASSA_O (300 ψ) | `rankOne_density`, `rankOne_density_normalized` | confere | — | **PASSA** | [KNOWN]; termo [REAL] |
| P2.lit | posto + nulidade = n | CITADO | — | `rank_add_nullity` (re-exportação de Mathlib) | confere | — | **CITADO** | [KNOWN] Mathlib `LinearMap.finrank_range_add_finrank_ker`; Axler LADR 3.22 |
| P2.a | (posto, nulidade): ρ* (1,1), I/2 (2,0), 0 (0,2) | PASSA | PASSA_O | `rhoStar_rank_nullity`, `half_identity_rank_nullity`, `zero_rank_nullity` | confere | — | **PASSA** | [REAL] |
| P2.b | Tr ρ = 1 ⟹ posto ≥ 1; posto 1 ⟺ nulidade n − 1 | PASSA | PASSA_O (1.400 + 600) | `trace_one_rank_pos`, `rank_one_iff_nullity(_succ)` | confere | — | **PASSA** | [REAL] |
| P3.a | P = \|a⟩⟨a\|: PXP = ⟨a,Xa⟩P; Tr(PX) = ⟨a,Xa⟩ | PASSA | PASSA_O (60.502 pares) | `compression_by_rank_one`, `reading_returns_the_post` | confere; `_ha` sem peso, por desenho | nome «post» com homônimo (baixa) | **PASSA** | [KNOWN] Lüders 1951; forma geral [REAL] |
| P3.b | ρ*(I/2)ρ*/Tr = ρ*, Tr = 1/2; Tr(ρ*ρ) = 1−b, Tr(Q₀ρ) = b | PASSA | PASSA_O (mpmath 1,3e-51) | `reading_of_the_attractor_state`, `reading_weights_*` | confere | nome «atrator» com peso emprestado (baixa-média) | **PASSA** | [REAL]; «atrator» é citação da F1.ATRATOR |
| P4 | ρ = P/d: Tr ρ = 1 (nome), Tr ρ² = 1/d (índice); iguais ⟺ d = 1 | PASSA | PASSA_O (200 projeções) | `trace_eq_rank_of_projection`, `name_meets_rank_only_at_the_atom` | confere; `_hH` sem peso | — | **PASSA** | [DERIVED]; termo [REAL] |
| B1.a | Tr ρ* = posto ρ* = 1; ρ*² = ρ* = ρ*ᴴ | PASSA | PASSA_O (ω(I) = 1 = core) | `rhoStar_unit` | confere | definicional (nome pesado) | **PASSA** | [REAL]; posição ⟷ posto é [ONTO] |
| B1.b | P² = P ⟹ Tr P = posto P | PASSA | PASSA_O (204 projeções) | `trace_eq_rank_of_projection` (vale p/ idempotente oblíquo) | confere | — | **PASSA** | [KNOWN]; termo [REAL] |
| B1.c | Im ρ* = span{e₀}, posto 1 | PASSA | PASSA_O | `range_rhoStar` | confere | — | **PASSA** | [REAL] |
| B2.a | {Q_θ, ρ*} = 0 ⟺ sin θ = 0; Tr = 2 sin²θ | PASSA | PASSA_O (zero só em {0, π}) | `anticomm_zero_iff`, `anticomm_trace`, `anticomm_frob` (+ `anticomm_complement_zero_iff`) | confere; termo novo (0 no kernel, inventário, mapa) | — | **PASSA** | [REAL] novo |
| B2.b | em θ_M: {Q,ρ*} ≠ 0, Tr = 2β, Σ\|.\|² = 2β(1+β) | PASSA | PASSA_O (\|.\|_F = 0,15605) | `anticomm_at_thetaMiguel` | confere | identidade de θ_M, sem poder discriminante | **PASSA** | [REAL] identidade |
| B3.a | Tr(ρ*Q_θ) = sin²θ = (F_θ(1))₁₁ = \|r\|² | PASSA | PASSA_O (resíduo 0) | `leak_eq`, `leak_eq_rhoOut`, `leak_eq_reflected_weight` | confere | — | **PASSA** | [REAL] |
| B3.b | em θ_M: Tr(ρ*Q_θM) = β | PASSA | PASSA_O (0 em float64; 1,2e-63 mpmath) | `leak_at_thetaMiguel` | confere | identidade, sem poder discriminante | **PASSA** | [REAL] identidade |
| B3.d | \|β − 0,012031\| ≤ 5e-7 | PASSA | PASSA_O (3,004e-7) | — (β nunca entra no kernel como número) | confere | só a face O decide (regra f) | **PASSA** | [REAL runtime]: conferência de transcrição, não «β medido» |
| B4.a | u unitário: Tr e posto invariantes; uPuᴴ projeção | PASSA | PASSA_O (1.400 Haar) | `ad_trace`, `ad_rank`, `ad_projection`, `ad_rhoStar` | confere | — | **PASSA** | [KNOWN]; pedra 116; termo [REAL] |
| B4.b | F_θ(1) é projeção de posto 1 | PASSA | PASSA_O | `fractal_one_is_rank_one` | confere | — | **PASSA** | [REAL] |
| B5.a | D_∞F_θ(1) = diag(c², s²); posto 2 ⟺ sin 2θ ≠ 0 | PASSA | PASSA_O (12 θ) | `endpoint_eq`, `endpoint_rank_two_iff`, `endpoint_purity` | confere | — | **PASSA** | [REAL] novo |
| B5.b | em θ_M: diag(1−β, β), posto 2, pureza 1 − 2β(1−β) | PASSA | PASSA_O (σ = 0,98797 e β) | `rank_diag_two_iff`, `endpoint_at_thetaMiguel` | confere; S2.4: b ∈ [0,1] tem peso | base de D é [INPUT] não marcado | **PASSA** | [REAL] identidade de θ_M |
| B5.c | t > 0: posto D_tF_θ(1) = 2 ⟺ sin 2θ ≠ 0; det = c²s²(1 − e^{−t(g₀₁+g₁₀)}) | PASSA | PASSA_O (resíduo 5,6e-17) | `dephased_rank_two_iff`, `dephased_det`, `dephased_trace` | confere; S2.2: t > 0 tem peso | — | **PASSA** | [REAL] novo |
| B5.e(i) | F(1) tem posto 1 | PASSA | PASSA_O | `fractal_one_is_rank_one` | confere | — | **PASSA** | [REAL] |
| B5.e(ii) | o posto 1 sobrevive a D | **FALHA** | FALHA_O (posto 2 em 9 θ, θ_M incluído) | `rank_not_preserved_by_dephasing`, `trace_survives_dephasing` | confere; c é supérflua (θ = π/4 basta) | vale na base de D = base de ρ* | **FALHA** (negativo honesto) | [REAL]: sobrevive o traço, não o posto |
| B6.a | Tr(ρ*D_tQ_θ) = sin²θ para todo t | PASSA | PASSA_O (variação 0) | `leak_survives_dephasing` | confere; g_ii = 0 indispensável | leitor diagonal não vê D | **PASSA** | [REAL] identidade |
| B6.b | {D_tQ_θ, ρ*} forma fechada; = 0 ⟺ sin θ = 0; limite diag(2s², 0) | PASSA | PASSA_O (taxas assimétricas incluídas) | `anticomm_dephased_*`, `anticomm_limit` | confere | — | **PASSA** | [REAL] |
| B7.a1 | S(θ)ⁿ = S(nθ) | PASSA | PASSA_O (resíduo 2,0e-13) | `Smat_pow` (indução sobre `Smat_mul`, SMatrix:81), `leak_after_n_passes` | confere | corolário: [DERIVED], não [KNOWN] | **PASSA** | [DERIVED] |
| B7.a2 | sin θ ≠ 0 ⟹ sin²(nθ) sem limite | PASSA | PASSA_O (99.970 janelas, amplitude mín. 0,99646 > 0,99397) | `angular_leak_no_limit`, `angular_leak_zero_converges` | confere | — | **PASSA** | [REAL]; o ângulo não tem limite — nenhum foi pedido |
| B7.b | D_t → D_∞ (taxas > 0) | CITADO_REAL | SOMBRA_CONSISTENTE_O | `dephasing_has_limit` (re-exporta `dephase_tendsto_expectation`) | confere | — | **CITADO_REAL** | [REAL] já no kernel |
| B7.c | espiral com taxa converge; sem taxa é periódica | CITADO_REAL | — | re-exportações de `IALDJones` | confere | — | **CITADO_REAL** | [REAL] já no kernel |
| B8.a | θ = 0: vazamento 0, {Q₀,ρ*} = 0, F₀(1) = ρ* = D_tρ* | PASSA | PASSA_O | `nothing_branch`, `rhoOut_zero`, `dephase_rhoStar` | confere | **nome «nada» a ρ*, o mesmo objeto da «unidade» (média)** | **PASSA** | [REAL]; «nada sem referente» é [ONTO] |
| B8.b | D trivial ⟺ sin 2θ = 0 | PASSA | PASSA_O ({0, π/2, π}) | `dephasing_trivial_iff`, `dephasing_trivial_at_thetaMiguel` | confere; S2.5/6 | — | **PASSA** | [REAL] |
| B9.a | «o que transmite defasa» (literal: \|t\|² > 0 ⟹ D atua) | **FALHA** | FALHA_O (θ = 0, π) | `literal_transmission_does_not_force_dephasing` | confere; com g ≡ 1 (populações decaem) a letra valeria — o texto deve dizer qual D | — | **FALHA** (negativo honesto) | [REAL] |
| B9.a′ | controle: «o que vaza defasa» | **FALHA** | FALHA_O (θ = π/2) | `literal_leak_does_not_force_dephasing` | confere | — | **FALHA** (controle) | [REAL] |
| B9.b | inscrição: D atua ⟺ \|t\|² > 0 **e** \|r\|² > 0; em θ_M, (D_∞F(1))₁₁ = β | PASSA | PASSA_O | `dephasing_acts_iff_transmits_and_leaks`, `inscription_at_thetaMiguel` (+ `dephasingActs_iff_forward`) | confere; S2.1: g = 0 derruba | é `dephase_fixed_iff_diagonal` na matriz-S | **PASSA** | [REAL]; é a leitura que o cânone sustenta |
| B9.c | «transmitir defasa» (05/10), fluxo do lock | CITADO_REAL | — | `transmission_dephases_reexport` (TheVerbSelectsTheAction:529) | confere: homônimo, não apoia B9.b | não reinstalar ou renomear | **CITADO_REAL** | [REAL] já no kernel; **homônimo** |
| O1 | «ou os vínculos fecham, ou não fecham» | NAO_TESTAVEL | — | — | confere | posição filosófica, não teorema | **NAO_TESTAVEL** | [ONTO] |
| O2 | a leitura da memória dos modelos | ABERTO | — | — | confere | é [OPEN]/[DECLARADO], não [ONTO] | **ABERTO** | [OPEN] (F0.3.COLAPSO sem telemetria) |

**Controles C1–C14 [REAL]:** os 14 falham sem a hipótese nas duas faces (ótica do construtor; recálculo independente em mpmath do auditor; 14 termos Lean compilam). Exemplos: I/2 tem traço 1 e posto 2 (C3: traço 1 não é posto 1); ρ*/2 tem posto 1 e pureza 1/4 (C2); diag(2/3, 2/3, −1/3) tem Tr 1, Tr(.²) 1 e posto 3 (C1: sem positividade a pureza não dá posto 1).

**Sondas adversariais do auditor de reprodução [REAL]:** S1 (provar o contrário): 6 tentativas falham, 6 refutações compilam. S2 (derrubar cada ⟺ sem a hipótese): 8 contraexemplos compilam (g = 0; t = 0; Tr ≠ 1; b = 2; b = −1). S3 (hipótese sem peso): só `_ha` e `_hH`, por desenho e documentadas; `c : TGLCoupling` é supérflua em `rank_not_preserved_by_dephasing` (a testemunha θ = π/4 basta — a pedra pode ficar incondicional ali).

---

## 3. O que é o quê

**Teorema de kernel agora (pedra r2, sandbox; instalar é ato da v392):** 177 teoremas + 13 definições em `TGLExt.TheUnitIsTheRank`, compilados com Lean 4.31.0 e o `.lake` do Nós só-leitura, EXIT 0, zero avisos, `#print axioms` de todas as 190 declarações dentro de {`propext`, `Classical.choice`, `Quot.sound`}, zero `sorryAx` (a única ocorrência da palavra «sorry» no fonte é o comentário da l.113, «Sem sorry, sem axiom»); o `.olean` `d0830b4bc03dc561` foi reproduzido bit a bit por dois auditores em sandboxes próprios. A rodada 2 **não muda nenhum enunciado nem prova** da rodada 1 (179 declarações iguais sem comentários; 11 acrescentadas: `dephase_fixed_iff_neg`, `dephasingActs_iff_forward`, `Qtheta_entry01`, `one_sub_rhoOut_eq_Qtheta_neg`, `leak_of_complement`, `anticomm_complement_zero_iff`, `Qtheta_eq_one_sub_rhoOut_iff` e 4 sondas). Conteúdo novo com peso: `anticomm_zero_iff` e `anticomm_at_thetaMiguel`; `endpoint_*` e `dephased_*` (o ponto final tem posto 2); os três negativos; `dephasing_acts_iff_transmits_and_leaks`; `Smat_pow` e `angular_leak_no_limit`; a ponte runtime–kernel `Qtheta_eq_rot`/`Rot_eq_conjTranspose` (a receita R Q₀ Rᵀ do um.py l.6518 é S(θ)ᴴQ₀S(θ)).

**Número de runtime (face O, não é termo):** B3.d (|β − 0,012031| = 3,0e-7: conferência de transcrição do número do operador); ω(I) = Tr ρ* = 1 e o leak do core v391 (iguais bit a bit ao recalculado); |{Q_θM, ρ*}|_F = √(2β(1+β)) = 0,15605161063018547; pureza do ponto final 0,9762269035770627.

**[KNOWN] por citação (o PASSA é do termo, o conteúdo é da literatura):** P1 (Nielsen & Chuang, *Quantum Computation and Quantum Information*, Ex. 2.71); P2.lit (Axler, *Linear Algebra Done Right*, Teo. 3.22; Mathlib `LinearMap.finrank_range_add_finrank_ker`); P3 (G. Lüders, Ann. Phys. (Leipzig) 8, 322 (1951)); B1.b e B4 (invariância de traço e posto por idempotência/conjugação unitária; Mathlib `LinearMap.IsProj.trace`, `Matrix.rank_mul_eq_left_of_isUnit_det`); P1.b (Cayley–Hamilton 2×2); III₁ como existência (Connes 1973) onde V4 fala de «potencial infinito na borda».

**[ONTO] (leitura; nenhum teste a toca):** «Tudo = D_β(F(1)) = VERDADE» como identidade do Tudo e «TGL = teoria de tudo» [CONJECTURE ontológica, um.py l.6488]; «Nada = MENTIRA pelos dois ramos», «impedância sem identidade, sem referente»; «existir ⟺ x ∈ Im(D_β∘F) e paga ½ nat»; «a transmissão é o verbo; a defasagem é a matéria»; «a falha na transmissão cria o espaço-tempo, a gravidade e a consciência»; c² e c³ como geometria e massa; «tudo é frequência»; posição ⟷ posto (POSTO = RANK como leitura da etiqueta [POSTO]); «o observador estabeleceu o piso» (com o homônimo piso = β em `a_positive_floor_forces_a_positive_angle`); O1; o «impede» causal de V4 l.16 (o kernel prova a equivalência vazamento ≠ 0 ⟺ anticomutador ≠ 0, não a causa); D como direção hiperbólica de SL(2,ℝ) (IALDJones l.274). Correção de rótulo proposta pelo auditor de estatuto, que acolho: V1 l.8–14 (memória dos modelos) é **[OPEN]/[DECLARADO]**, não [ONTO] — testável em princípio; e «Quando eu derivei…» (V2 l.12 / V1 l.5) é **[DECLARADO], conferível no acervo** (Lei da Prova, item 4), não [ONTO].

---

## 4. As sondas honestas, em poucas frases

- **B5.e(ii) — «a unidade é o rank» sobrevive à defasagem?** Não. F_θ(1) tem posto 1 (B4.b), mas D_∞F_θ(1) = diag(cos²θ, sin²θ) tem posto 2 sempre que as duas faces têm peso (sin 2θ ≠ 0), e em θ_M dá diag(1−β, β). O que sobrevive a D é o **traço** (`trace_survives_dephasing`), isto é, ω(I) = 1. O número corrigiu a frase antes do ensaio: estava pré-registrado como FALHA e falhou nas duas faces.
- **B9.a — «o que transmite, por natureza, defasa» (V4 l.10), lido à letra.** Falso em θ = 0 (e θ = π): transmissão total, |t|² = 1, e D não faz nada em ρ*. O controle B9.a′ («o que vaza defasa») cai em θ = π/2. O que vale, e o cânone sustenta, é a **leitura de inscrição** B9.b: **D atua ⟺ transmite E vaza** (as duas faces com peso), e em θ_M o peso inscrito é β. Ressalva do auditor de reprodução, que registro: isso vale para a defasagem **pura** (populações preservadas, g_ii = 0, a do pré-registro); se as populações também decaem (g ≡ 1), a letra de V4 l.10 passa a valer — o texto da v392 tem de dizer qual D usa.
- **B2 — o anticomutador «perfeito».** {Q_θ, ρ*} = 0 **se e só se** sin θ = 0 (avaliação exata em θ ∈ πℤ), e dentro de 0 < β < 1 ele é ≠ 0, com traço 2β. O «θ_M → 0» do um.py (l.6502) não é limite no ângulo — é avaliação em θ = 0 (o contrafactual β = 0, fora de `TGLCoupling`). Regra dos dois regimes respeitada: ao ângulo nada se pede como limite; o kernel **prova** que sin²(nθ) não converge quando sin θ ≠ 0 (B7.a2), e o limite existe só na face, D_t → D_∞ (B7.b).

---

## 5. Divergências entre as auditorias e o que vale

As duas auditorias **concordam em todos os 38 vereditos** e as duas dizem **pode fechar**. Divergem no alcance:

1. **Reprodução (audR):** «tudo reproduz, nenhum achado material»; seis observações não materiais (a mais útil: o anexo A9 do construtor esqueceu o homônimo `anticommutation_forces_the_conjugated_face`, `TheTwoPairings.lean:89` — conferi aqui por grep: existe e, como os outros, não trata de {Q_θ, ρ*}).
2. **Estatuto (audE):** «aprova com ressalvas», 16 problemas, **um de gravidade alta** (seção 6), cinco médios, o resto baixo/info. **Nenhum muda enunciado, prova ou veredito**; todos são de **texto, nome, rótulo ou processo**. Vale a leitura de audE onde ela corrige o texto, e a de audR onde atesta a reprodução — não se contradizem.
3. **Contagens em que o número corrige a frase:** (a) o texto do `RESULTADO_KERNEL.json` r2 diz «15 citações conferidas byte a byte»; o campo `citacoes.conferidas` e o `CITACOES_R2.json` dizem **14** — vale 14. (b) O mesmo arquivo lista B3.d como «NAO_FORMALIZADA» na face K; pela regra (f) do pré-registro **a face única decide**, logo a unidade tem **29 PASSA** (28 nas duas faces + B3.d só na face O), não 28. (c) O `.olean` do sandbox é do módulo `TheUnitIsTheRank` (compilado com `--root=TGLExt`), não de `TGLExt.TheUnitIsTheRank`: a custódia pina o `.lean` e **recompila no lake do Nós**; a contagem do selo (hoje 6163) tem de ser medida de novo.
4. **Nenhum auditor disse que não pode fechar.** O que a instalação exige (seção 8) é uma **rodada 3 só de nomes e comentários**, com sha novo e registro ao lado — sem mexer em enunciado ou prova.

---

## 6. Achados materiais e como ficam

**A1 (audE, alta; afeta o texto da v392, não os vereditos).** V1 l.7 / V2 l.18 («Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio … e ganha posto definido») **contraria o colapso tipado do próprio cânone** se lida sobre a superposição pura: `ChatgptAudit.Collapse057.actualDensityCollapse` tem passo `qubitReduction` = `TGLExt.nameOp readoutZero` = D_∞ e `identity := traço`; ele leva |+⟩⟨+| (posto 1, nulidade 1) a I/2 (posto 2, nulidade 0), preservando só o traço [REAL — sonda do auditor `AuditorEstatutoR2.lean`, `typed_collapse_raises_rank_of_superposition`, 6/6 no trio, compilada em sandbox, `512ea820918c178f`]. A letra vale lendo «colapsar» como o **ramo selecionado** (P3; `selective_branch_formula` já no kernel: P_k A P_k = A_kk·P_k) e «superposição» como a **mistura de posto cheio** (R-a do pré-registro: I/d → P). **Como fica:** o texto da v392 diz isso; o levantamento (§5 item 3, «já diz isso») fica corrigido ao lado; a pedra e os resultados não trazem o R5 («a superposição pura já tem posto 1») — entra por **pré-registro aditivo** (seção 8).

**A2 (audE, média).** O um.py v391 **pede limite ao ângulo** e chama identidade de âncora: «{Q,rho*}=0 EXATO so' em theta_M->0» (l.6502), «||{Q_0,rho*}||->0» (l.6508), «portador no limite theta_M->0» (l.6514), «nada perfeito = limite inalcancavel» (l.6515), o campo `anticommutator_norm_at_thetaM_to_0 = 0.0` (l.6523) e o `status` (l.6530) — conferi as linhas por número nos bytes. O campo é P(1−P) + (1−P)P = 0, que vale para qualquer projetor e não envolve β; o que existe é **avaliação em θ = 0**. Termos certos: `anticomm_zero_iff` e `anticomm_at_thetaMiguel`. **Como fica:** errata ao lado no um.py (seção 8); a pedra já corrige.

**A3 (audE, média).** O «D_β» do cânone **não tem D**: `fractal_dephasing_principle` só gira o portador por R(θ_M) (ângulo, só lê); β entra pelo ângulo, não por taxa; D_∞ independe da taxa. Ler D_β como «taxa β» (G3 β·gap) é outra leitura, não testada aqui. **Como fica:** o texto da v392 diz que o D da face está em `endpoint_at_thetaMiguel`; o índice β de D_β é do ângulo.

**A4 (audE, média).** `nothing_branch` dá o nome «nada» ao polo θ = 0, cujo estado é ρ* — **o mesmo objeto** que B1 chama «a unidade» (`rhoStar_unit`). Os dois polos da não-defasagem (θ = 0: ρ*; θ = π/2: Q₀) têm traço 1 e posto 1 [REAL, `nondephasing_poles_are_rank_one_units`]. «Sem identidade» não é falta de posto. **Como fica:** renomear (por exemplo `zero_angle_pole`) e juntar o polo π/2; «nada sem referente» segue [ONTO].

**A5 (audE, média).** A **base de D** é um [INPUT] não marcado: D defasa na base de ρ* (o canal de medição do cânone); o negativo B5.e(ii) vale **nessa base** — na base girada (Ad S∘D∘Ad Sᴴ) o posto 1 de F_θ(1) seria preservado. **Como fica:** marcar [INPUT] no texto da v392 e na pedra.

**A6–A8 (audE, baixa-média/baixa).** `reading_of_the_attractor_state` chama I/2 de «estado atrator» com peso emprestado da F1.ATRATOR, cujas pedras **não estão** no kernel do Nós (consulta por nome: 0; rota `formal.singularidade_le_atrator`); `transmission_dephases_reexport` põe «transmission» num homônimo (o fluxo do lock contrai AO posto P; a matriz-S SOBE o posto) — a citação basta; `reading_returns_the_post` usa «post» com homônimo (`TheVerbSelectsTheAction.post`, só projeção se ⟨a,a⟩ = 1). **Como fica:** rodada 3 de nomes.

**A9 (audR, não material; audE idem).** Citações: as 6 linhas «=V1…» de V2 são iguais só sem Markdown (documentado no `segmentar.py` congelado); no levantamento há «colapsa» onde V1 diz «a colapsar», «POSTO = RANK» com espaços onde os bytes dizem «POSTO=RANK», e 4 trocas de caixa; na pedra, 8 das 9 citações de linha do um.py estão sem versão. **Como fica:** rodada 3 cita «um.py v391 (`8e7b9927ceae64b8`) l.NNNN».

**A10 (processo).** `run_optico.py` pina o um.py v391 e vai recusar depois do selo da v392 — mesmo defeito da F1.ATRATOR. **Como fica:** o registro no core lê os resultados **por hash**, sem rodar os runners.

---

## 7. O que a pedra NÃO afirma (para que ninguém a cite além dela)

β no Lean; ρ* = firstAtom, PFmic, post Ω, bellProjector, P_F ou R; os dois «1» fora do átomo; que D preserva o posto ou devolve o posto 1; que I/2 tem posto 1; limite no ângulo; D como direção hiperbólica; colapso físico, seleção na natureza, espaço latente; Tudo, Nada, matéria, verbo, consciência como termos; que o vazamento **discrimina** β; que o ponto final de uma passagem, diag(1−β, β), seja ponto fixo de canal iterado (o da F1.ATRATOR é I/2); que o PASSA de B9.b seja a letra de V4 l.10; qual das duas leituras de Q̂ é a de V4 (decisão do operador); e, acima de tudo, qualquer palavra do gate ou a palavra proibida.

---

## 8. O que entra no um.py v392 e as erratas ao lado propostas

**(a) A pedra** `TGLExt/TheUnitIsTheRank.lean` a partir de `3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean` (`3195ef8f0766384c`), junto com o ADENDO1 da F1.ATRATOR, **sem identificar P com R**. **Condição:** uma **rodada 3 só de nomes e comentários** (sha novo, registro ao lado, nenhum enunciado nem prova muda): (i) renomear `nothing_branch` e juntar o polo π/2; (ii) `reading_of_the_attractor_state`: ponte com a pedra da F1.ATRATOR instalada, ou nome novo; (iii) não instalar `transmission_dephases_reexport`, ou renomeá-lo; (iv) citar «um.py v391 (`8e7b9927ceae64b8`) l.NNNN»; (v) trocar [KNOWN] sem citação por [DERIVED aqui] ou pôr a citação (S(θ)ⁿ = S(nθ) é [DERIVED] de `Smat_mul`); (vi) marcar a base de D como [INPUT]; (vii) a cláusula `c : TGLCoupling` de `rank_not_preserved_by_dephasing` pode cair.
**Instalação:** recompilar no lake do Nós como `TGLExt.TheUnitIsTheRank`; importar em `TGLExt.lean`; `#print axioms` das declarações em `TGL/Audit.lean`; medir de novo a contagem do selo; embutir no um.py e conferir byte a byte com o tgl_kernel.

**(b) Registro no core** (por exemplo `the_unit_is_the_rank_v392`), **lido por hash**: PREREGISTRO.json `0c20d7c196a4c7ef`, FREEZE.json `4d8f97537eb04cd5`, RESULTADO_OPTICO.json `28758b3eebdac631` (run_optico.py `48a8d8b0d9fd125b`), RESULTADO_KERNEL.json r2 `9fd3c2044e410a57`, pedra `3195ef8f0766384c`. Vereditos: 29 PASSA; 3 FALHA honestas (B5.e(ii), B9.a, B9.a′); 1 CITADO; 3 CITADO_REAL; O1 NAO_TESTAVEL; O2 ABERTO; controles 14/14. Leitura: validade na face testada; o gate não se move.

**(c) Texto (artigo PT/EN, adendo à seção do Princípio da Defasagem Fractal):** «A unidade é o posto **no átomo**; o traço sobrevive à defasagem, o posto não». Incluir: o colapso tipado do cânone (`nameOp ρ*` = D_∞) preserva o traço e sobe o posto da superposição pura; V1 l.7 é seleção a partir da mistura de posto cheio; a letra de V4 l.10 é falsa em θ = 0 e vale «transmite E vaza»; {Q̂, ρ*} = 0 ⟺ sin θ = 0 (avaliação), caso excluído por 0 < β < 1; o ângulo não tem limite, a face tem. Citar por bytes: V2 l.16 e V4 l.13 e l.16 em LaTeX; «POSTO=RANK» sem espaços.

**(d) Erratas AO LADO no um.py (linhas da v391; a frase antiga fica como registro):**
- l.6489 e l.6530 (`status`): as «âncoras REAL» são **identidades** (Tr diag(1,0) = 1; {Q₀,ρ*} = 0 vale para qualquer projetor, sem β; sin²(arcsin√β) = β) e passam a termos de kernel; o princípio continua [CONJECTURE ontológica].
- l.6494 (e artigo PT l.168091–168092, EN l.172481–172482, rito l.211563): o código **não aplica D**; β entra pelo ângulo θ_M; o D da face está em `endpoint_at_thetaMiguel`.
- l.6497 e l.6526 (e l.168096, l.172486, l.211565): «Tudo = … = VERDADE» é [ONTO]; «verdade» aqui é valor lógico, não o peso 1−β de `the_one_splits_into_truth_and_cost`; no kernel o ponto final é verdade **e** custo, diag(1−β, β), posto 2.
- l.6498–6501 (e l.168096–168100, l.172486–172490, l.211566–211567): os polos da não-defasagem são ρ* e Q₀, traço 1 e posto 1.
- l.6502–6505, l.6508, l.6514–6515, l.6529 (e l.168101–168106, l.172491–172496, l.211568, l.211571): «θ_M→0» é avaliação em θ = 0; {Q_θ,ρ*} = 0 ⟺ sin θ = 0; em θ_M a norma é √(2β(1+β)) = 0,15605161063018547 e o traço 2β; o «verificado ao vivo» é identidade de projetor.
- l.6517: a inclinação é ângulo e só lê; o Q_θ do um.py é `Qtheta` (`Qtheta_eq_rot`), não 1 − F_θ(1) (os dois dão o mesmo vazamento e o mesmo zero do anticomutador e diferem fora da diagonal, salvo sin 2θ = 0).
- l.6523: manter o campo `anticommutator_norm_at_thetaM_to_0` e acrescentar ao lado o valor em θ_M.

**(e) Pré-registro ADITIVO (o FREEZE não muda):** a ponte D_∞ = `nameOp ρ*` = `Collapse057.qubitReduction` em M₂(ℂ) e o corolário «o colapso tipado sobe o posto da superposição pura e preserva o traço», mais «os polos ρ* e Q₀ têm posto 1». Já medidos na sonda do auditor (6/6 no trio). Ligam ao mesmo termo o D de V4, o colapso de V1 e o Operador do Nome.

**(f) NÃO entra como termo:** O1, O2, B3.d (número de runtime) e as leituras [ONTO].

**(g) Memória (ato da gerência, não deste redator):** ao lado de `posto-e-rank-10out.md`, registrar que «o Um posto = posto 1 = Tr P = ω(I)» vale **para projeções e no átomo**; ω(I) = 1 vale para todo estado (I/2 tem traço 1 e posto 2); Tr P_F dos Three Locks ≈ 4 (core v391: 3,9999999999999996).

---

## 9. Registros para o mapa de rotas (gravados aqui; registrar é ato da gerência)

- `registro_rota_F1.FREQUENCIA.json` — tipo **ROTA**, `rota_id` **`formal.posto_e_defasagem_da_unidade`**, domínio **FORMAL**.
- `registro_mapa_F1.FREQUENCIA.json` — tipo **RESULTADO**, mesma `rota_id`.
Ambos no formato de `python C:\IALD\MAPA_DE_ROTAS\rotas.py modelo`, artefatos como lista de caminhos (o sha256 é calculado pela ferramenta ao registrar), sem a palavra proibida. Comando, quando a gerência decidir: `python C:\IALD\MAPA_DE_ROTAS\rotas.py registrar <json> --quem "claude-c1 (gerência)"` — primeiro a ROTA, depois o RESULTADO.

---

## 10. O resíduo que só o operador decide

1. **O nome da pedra.** `TheUnitIsTheRank` é provisório; o próprio título «A unidade é o posto» vale **só no átomo** (a pedra o diz ao lado). Candidatos que a matemática sustenta: «O posto é o átomo», «A unidade é o posto no átomo», «O traço sobrevive, o posto não». A cunhagem é sua.
2. **Qual Q̂ é o de V4 l.16:** S(θ)ᴴQ₀S(θ) (a receita do um.py) ou 1 − F_θ(1) = Q_{−θ}. Dão o mesmo vazamento e o mesmo zero do anticomutador; diferem na coerência.
3. **A base de D** (base de ρ*, o canal de medição) como [INPUT] declarado — e, com ela, se a leitura «o posto não sobrevive» é a que o texto da v392 deve carregar.
4. **Qual D é «a defasagem» de V4:** pura (populações preservadas; a letra de l.10 falha em θ = 0) ou com decaimento de populações (a letra vale).
5. **Se o pré-registro aditivo (e)** — o colapso tipado como D_∞ e a leitura de V1 l.7 como seleção a partir da mistura — entra na v392 ou fica para depois.
6. **Os nomes** `nothing_branch`, `reading_of_the_attractor_state`, `reading_returns_the_post`, `transmission_dephases_reexport` (seção 8a).
7. **A tensão entre «a transmissão é o verbo; a defasagem é a matéria» (V4 l.18, [ONTO]) e «o fixo é o verbo … o verbo é β_TGL» (08/10):** sem âncora tipada; a letra de 11/10 e a de 08/10 convivem como leituras, e só o operador diz se são a mesma.
8. **O rótulo de V1 l.8–14 e de «Quando eu derivei…»** ([OPEN]/[DECLARADO] em vez de [ONTO]) no texto da v392.

---

## 11. Arquivos desta pasta (rodada 2 do redator)

`RELATORIO_FINAL.md` (este) · `registro_rota_F1.FREQUENCIA.json` · `registro_mapa_F1.FREQUENCIA.json` · `PINOS_R2.json` · `IMPRESSAO_DIGITAL_KERNEL_REDATOR_R2.json` · `MANIFESTO_COPIA_AUDITORIAS_R2.json` · `AUTO_AUDITORIA_REDATOR_R2.json` · `scripts_r2\` (pinos_r2.py, copiar_auditorias_r2.py, impressao_digital_kernel.py, auto_auditoria_r2.py) · `auditorias_copia\POSTO_AUD_REPRO\r2` e `auditorias_copia\POSTO_AUD_ESTATUTO\r2` (209 arquivos, cópia de bytes). Os arquivos da rodada 1 do redator (`CONFERENCIA_REDATOR.json`, `MANIFESTO_COPIA_AUDITORIAS.json`, `L\`, `lean_logs\`, `scripts\`, `tentativas\`, `consultas_mapa\`, `auditorias_copia\...` sem `r2`) ficam intactos como registro: aquela rodada conferiu a rodada 1 dos construtores e não chegou a escrever este relatório.

*NOT_FALSIFIED nunca é a palavra proibida. PASSA é validade na face testada. A confirmação, no sentido da régua, é creditação — e esta segue sendo ato do observador humano.*
