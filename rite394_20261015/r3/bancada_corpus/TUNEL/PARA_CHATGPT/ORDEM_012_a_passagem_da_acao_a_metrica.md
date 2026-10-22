# ORDEM 012 — A PASSAGEM DA AÇÃO À MÉTRICA: tornar teorema de kernel o caminho da lagrangiana (o β que a matriz-S lê e o custo paga) até a equação de Friedmann modificada — com a hipótese importada NOMEADA e o teorema da diferença entre as duas rotas

**DATA:** 2026-09-14 14:33 · **DE:** Claude (gerência, sessão da Central de Patentes) · **PARA:** bancada ChatGPT (via Codex, nesta máquina) ·
**RESPONDE A:** as suas quatro `ENTREGA_011_A1_*` (última na via de volta: `ENTREGA_011_A1_potencias_imaginarias_mesmo_tomita.md`), incorporadas como **v353** (recompilação independente 19/19, axiomas no trio) ·
**PRECEDÊNCIA:** esta ordem entra na frente de A1(b) por ordem direta do operador; A1(b) continua sendo alvo da ORDEM 011 e retoma depois de B1–B6 (ou em paralelo, se a bancada tiver duas sessões abertas).

> **Ordem do operador (14/09/2026, verbatim):** «vamo formalizar a passagem no chagpt dê a ordem pra ele» — em resposta à própria pergunta dele,
> «como o kernel não tem o teorema que liga betatgl ou o ângulo de Miguel se isto está na lagrangiana, ou seja, é o fundamento da teoria?»,
> e na esteira da ordem de 14/09 12:54 sobre o D1: «esse afastamento da previsão ocorreu, porque quando realizamos o teste do D1 não tínhamos todas as
> formulações matemáticas que temos agora [...] é de se esperar alguns ajuste, não de parâmetros, porque a TGL é zero parâmetros livres, mas de aplicação da métrica».
> Régua da casa, sem exceção: o número corrige a frase; PROVADA = teorema em kernel; **CONFIRMADA é proibido**; `NOT_FALSIFIED` ≠ `CONFIRMED`; **β nunca literal**
> (variável real em todo enunciado; o VALOR α√e é leitura de runtime); cosmologia jamais vira prova matemática; nenhuma entrega move o gate — quem incorpora é a gerência e quem ratifica estatuto é o operador.

---

## 0. O OBJETIVO VINCULANTE DESTA ORDEM

**Tornar TEOREMA de kernel, com hipóteses nomeadas e sem parâmetro novo, a passagem que hoje é derivação de artigo:** da lagrangiana da teoria — o β que a
matriz-S de fronteira lê como `sin²θ_M` e que o custo geométrico paga como `α·√e` — até a lei de fundo `H² = (8πG/3)·ρ·[1 + β|1+w_eff|]` que o D1 testa;
passando pela entropia modificada do horizonte `S_TGL = S_BH/(1 + β|1+w|)` e pela rota de Jacobson–Padmanabhan–Cai–Kim, **importada** ([KNOWN], no modo de
`TheImportedEquilibrium`: citação na face, ponte provada, nenhum `axiom`). E, onde a passagem admitir DUAS leituras (o fator sobre o fluido TOTAL vs o fechamento
SETOR A SETOR), **provar o teorema da diferença** e o teorema do fator que as reconcilia — **não escolher**.

**O que isto NÃO é:** não é prova de que a natureza realiza a TGL; não move o gate; não é ajuste de parâmetro; não é a formalização do Lema 3 global (a passagem
local ⟹ global segue o mesmo [OPEN] de sempre); não é a escala de área (η = 1/4G segue [INPUT], `TGL/AreaScale.lean` diz por quê); não decide TGL-S vs TGL-L
(o fechamento perturbativo segue [OPEN]).

**Por que agora — medido em 14/09/2026 por sete leitores independentes da gerência (relatórios em `ORDEM_012_INSUMOS\`, §6):**

- **Kernel:** a ÚNICA lei de fundo em Lean é `TGLExt/RhoPlusPClosure.lean` (sha16 `cd80fbbe00300454`) — `closure_identity` e `hubble_form` são identidades de anel com β variável real; o «H² ∝ …» está só em
  comentário; o módulo é FOLHA no grafo (ninguém consome seus teoremas). Varredura dos fontes do `TGLExt`: **zero** ocorrências de Hubble, Friedmann, FLRW, redshift,
  fator de escala, distância de luminosidade/diâmetro angular.
- **Ângulo:** `TGLExt/SMatrix.lean` (sha16 `14f7e717a4ef7020`) tem θ GENÉRICO (`normSq_reflection : |R|² = sin²θ`); a relação `θ = arcsin√p` aparece em cinco cópias (`thetaMiguel`, `selectionAngle`, …) sempre
  com p/β como parâmetro; a identificação `sin²θ_M = β = α√e` é comentário («NO RUNTIME e só lá»). **Nenhum lema liga o β de `RhoPlusPClosure` ao `sin²θ` de `SMatrix`.**
- **Geometria:** a camada Clausius ⟺ balanço nulo de Ricci ⟹ Einstein com Λ existencial (`TGLExt/GeneralMetricEinstein.lean` (sha16 `5874bbdd22bf8530`), `TGLExt/GeneralMetricClausius.lean` (sha16 `d635b15c7197800a`), `TGLExt/LocalHorizonBalance.lean` (sha16 `b3dcb033522681ba`)) é **livre de β** e tem η [INPUT]; a única
  «resposta» tipada entra como stress aditivo de informação (`TGLExt/FisherCorrectedEinstein.lean` (sha16 `f5c7942dedef5d49`)), nunca como fator de fundo.
- **Artigo A:** a passagem existe como TEXTO — `tgl_paper_unified.py` Parte C.1 (linhas 3212–3262: «derived from S_TGL = S_BH/(1+β|1+w|) via Jacobson–Padmanabhan»)
  e a errata cosmológica de 14/05/2026 (`errata_cosmologica_TGL.tex`, §3 «Derivação termodinâmica», Passos 1–4, linhas 263–430) — estatuto [DERIVED], não kernel.
- **D1:** o worker do D1 implementa exatamente a forma de `hubble_form` (fator `1 + β|1+w_eff|` com `w_eff` do fluido TOTAL); resultado V2 Δχ² = 9,699
  (β livre mediano -0,017); com r_s por integral (diagnóstico da gerência, não-cego, `run_v3diag`) Δχ² = 9,033. A tensão não é artefato de r_s.
  **A correção «de aplicação da métrica» que o operador pede só pode vir de um teorema que diga qual é a lei — e é isso que esta ordem manda produzir.**

**Critério de parada do operador (inalterado):** cada alvo termina em **teorema**, em **teorema de parede** (negativo tipado) ou em **lema faltante nomeado**.

## 1. O ESTADO DE PARTIDA `[REAL — lido agora]`

| item | valor |
|---|---|
| `um.py` canônico | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` · sha256 `c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40` · 12,864,360 bytes · **v353** (intermediária; a completa vem depois) |
| teoremas limpos | 5594/5594 · fontes formais embutidos 942 · relatório de axiomas 8129 termos, todos no trio |
| montagem | `EIGHT_CLAUSES_VERIFIED__ACT_III_CERTIFICATE_CONSTRUCTED_ON_THE_PRODUCT_TOWER__PRINCIPAL_GATE_UNCHANGED` |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| bandeiras que esta ordem NÃO toca | `gpf_H3_local_horizon_equilibrium_discharged` = false · `gpi_H3_horizon_data_produced` = false · `qgf_continuous_modular_realization_constructed` = false (A1(b), ORDEM 011) |
| quebras de linha | o `um.py` tem **320 quebras só-LF** por construção: nenhum script seu converte CRLF/LF |

**Onde trabalhar:** crie `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\` (a sua pasta; só você escreve nela). Cópia de trabalho a partir de
`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` **conferindo o sha256 acima antes de copiar**; kernel materializado em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel` (só leitura). Nunca escreva em `Nós`, no kernel canônico,
em memórias, selos, Atlas, diários, no espelho ou na pasta `TETELESTAI_V351_FECHO_MATEMATICO` (que fica como está para A1(b)).

## 2. O PROTOCOLO DE APROVEITAMENTO — vale a §2 inteira da ORDEM 011 (`2457c9b136025aeb`), sem exceção

Ficha `REAPROVEITAMENTO_B<n>.md` + `.json` ANTES de cada alvo: consumidor (arquivo:linha), tipo exato, fornecedores (arquivo:linha, sha256, enunciado, casa exatamente?),
decisão REUSAR/ADAPTAR/NOVO, buscas feitas. **O consumidor desta ordem já existe na casa:** o mapa `ext_*_kernel_proved` do `um.py` (hoje
`"ext_rp_hubble_form_kernel_proved": "TGLExt.hubble_form"`, linha ≈133697 na v352) e a lista `EXTERNAL_KNOWN_THEOREMS` (linha ≈134757) — a gerência liga os
teoremas novos a esse mapa e ao protocolo D1 V3 (§3, B6); você nomeia na ficha qual entrada consome cada teorema.

**2.1 Fornecedores já pagos — USAR, não refazer** (linhas conferidas em 14/09 na v353; cite por nome e reconfira a linha na hora):

| objeto | onde |
|---|---|
| fundo algébrico ρ+p: `lambda_drops_out` :47 · `closure_identity` :52 · `hubble_form` :58 · `w_bounds` :64 · `the_background_closure` :90 | `TGLExt/RhoPlusPClosure.lean` (sha16 `cd80fbbe00300454`) |
| matriz-S: `Smat` :45 · `normSq_reflection`/`normSq_transmission` :241–254 · `Smat_spectral` :213 | `TGLExt/SMatrix.lean` (sha16 `14f7e717a4ef7020`) |
| o ângulo com β como parâmetro: `thetaMiguel` :126 · `sin_thetaMiguel` :139 · `the_pruning_threshold_is_the_reflection_amplitude` :156 | `TGLExt/TheVerbalCoupling.lean` (sha16 `912bf222f07256b1`) |
| a seleção abre o ângulo: `selectionAngle` :98 · `selection_angle_reflection` :101 · `the_selection_opens_the_boundary` :118 | `TGLExt/TheSelectionIsTheBallast.lean` (sha16 `71ebf9680af3d247`) |
| a lagrangiana da face finita (Three Locks): `action_locks_zero_iff` :71 · `action_hasDerivAt` :117 · `critical_pairing_iff` :166 · `lagrangian_zero_iff_mem_ker` (HilbertHome :130) | `TGLExt/TransportWitness.lean` (sha16 `f4219cc2c036999e`) · `TGLExt/HilbertHome.lean` (sha16 `449bdee93696fc5f`) |
| o custo √e como estrutura: `the_minimal_volume_exceeds_one` :52 · `the_geometric_cost_survives_absolute_zero` :79 · `boundary_extracts_the_radical` (TheFiveHalves :84) | `TGLExt/TheGeometricCostOfAbsoluteZero.lean` (sha16 `299ef10c96770aac`) · `TGLExt/TheFiveHalves.lean` (sha16 `456c66269b72d30f`) |
| β como taxa de vazamento: `leakage_strictly_loses` :66 · `beta_forbids_full_static_witness` :91 · `leakage_rate_unique` :135 | `TGLExt/NoFullWitness.lean` (sha16 `fde4ca999c40e689`) |
| Einstein em carta: `metric_einstein_equation_from_ricci_null_balance` :144 · `metricInverse` :191 · `metric_only_einstein_equation` (≈:245) | `TGLExt/GeneralMetricEinstein.lean` (sha16 `5874bbdd22bf8530`) |
| Clausius em carta: `MetricScreenFamily` :41 · `MetricScreenClausius` :45 · `metric_screen_clausius_iff_null_balance` :54 · `metric_einstein_from_screen_clausius` :83 | `TGLExt/GeneralMetricClausius.lean` (sha16 `d635b15c7197800a`) |
| balanço local: `horizonFluxResidual` :26 · `local_clausius_forces_ricci` :74 · `horizonBalancePrimitive` :132 · `heat_area_clausius_implies_local` :157 | `TGLExt/LocalHorizonBalance.lean` (sha16 `b3dcb033522681ba`) |
| coeficiente de Clausius e Raychaudhuri: `clausiusCoefficient` :24 · `clausius_coefficient_zero_iff` :46 · `coordinate_raychaudhuri` (CoordinateRaychaudhuri :96) · `area_quadratic_limit` (EquilibriumAreaExpansion :77) | `TGLExt/ScreenClausiusCoefficient.lean` (sha16 `b5418548f2ac69d5`) · `TGLExt/CoordinateRaychaudhuri.lean` (sha16 `4bbac36ebd8bbc87`) · `TGLExt/EquilibriumAreaExpansion.lean` (sha16 `e670ae6fba4e8f8a`) |
| variação da métrica (Levi-Civita, Ricci, Einstein): `levi_civita_metric_first_variation` :107 · `ricci_variation_congr_on` :191 · `metric_einstein_first_variation` :89 | `TGLExt/LeviCivitaMetricVariation.lean` (sha16 `165f6b36fe2859bf`) · `TGLExt/MetricRicciVariation.lean` (sha16 `ba322f76127f39a0`) · `TGLExt/MetricEinsteinVariation.lean` (sha16 `b6ec0383b49f4bfb`) |
| curvatura à mão numa variável (o molde para FLRW): `ansatzRicci00` :57 · `ansatzG00_zero` :110 · `vacuum_implies_flat` :137 · `full_cone_clausius_iff_field_equation` (EmergentEinstein :255) · `EmergentEinsteinData` :287 | `TGLExt/AnsatzEinstein.lean` (sha16 `88ed36908dbc290f`) · `TGLExt/EmergentEinstein.lean` (sha16 `836ac3e4035afc52`) |
| H3 tipado: `HorizonEquilibriumData` :56 (κ, G, dA, dS, dQ, `area_entropy : dS = dA/(4G)`, `clausius`) · `einstein_coefficient_from_clausius` :71 · `emergence_master_full_triad` :105 | `TGLExt/TriadMaster.lean` (sha16 `64e0899e25969392`) |
| o modo importado: `EquilibriumInput` :73 · `towerEquilibriumInput` :85 · `discharge_by_import` :129 · `the_trio_is_a_pair` :140 · `the_pair_still_needs_its_hypotheses` :149 | `TGLExt/TheImportedEquilibrium.lean` (sha16 `6ce0e9c29fd92670`) |
| escala de área é CALIBRAÇÃO: `newtonPlanck_equivalence` · `halfNat_over_two_faces_eq_quarter` · `invariance_does_not_fix_area` (HorizonAreaScale :150) · `two_global_covariant_calibrated_forms` (CovariantAreaCounterexample :255) | `TGL/AreaScale.lean` (sha16 `7058ae26f99f44f2`) · `TGLExt/HorizonAreaScale.lean` (sha16 `9dcd856be4084bce`) · `TGLExt/CovariantAreaCounterexample.lean` (sha16 `bb43910687f2a997`) |
| controles negativos: conforme não é Λ (`control_conformal_not_pure_trace`) · cone nulo fixa g a menos de c>0 (`common_positive_null_cone_proportional`) · Clausius finito falha em t⁴ (`optical_clausius_not_eventually_exact`) | `TGLExt/CurvatureControls.lean` (sha16 `8c27b78d1e672056`) · `TGLExt/ConeVolumeReconstruction.lean` (sha16 `1dd77be08104353e`) · `TGLExt/OpticalHeatClausius.lean` (sha16 `4914f81c11b7f9aa`) |
| stress de informação (a única «resposta» que hoje entra em Einstein): `correctedStress` :40 · `metric_einstein_from_information_balance` :103 | `TGLExt/FisherCorrectedEinstein.lean` (sha16 `f5c7942dedef5d49`) |
| α como FORMA, não valor: `the_form_does_not_fix_the_value` :110 | `TGLExt/TheDammingByExpansion.lean` (sha16 `f139c3e660a93d79`) |
| métrica selecionada e σ (NÃO é FLRW; não use como fundo): `reflectedMetric` :39 · `selected_sigma_einstein_from_area` (SelectedProbabilitySigma :192) | `TGLExt/SelectedFisherLorentzMetric.lean` (sha16 `346db9497cbebf18`) · `TGLExt/SelectedProbabilitySigma.lean` (sha16 `889e6c7dc0564ad7`) |

No `um.py` v353: `prove_alpha_form` (a FORMA de α: `sech(κ/2)`; o valor é [INPUT/QED]), `prove_rho_plus_p_closure`, `prove_the_cosmological_errata_verdict`,
`prove_the_damming_by_expansion`, `prove_d1_camb_protocol`, `prove_d1_camb_amendment_v2`, `prove_d1_camb_result_v2`, `prove_joint_coincidence_protocol`, `_MAPA_PILARES`.

**2.2 As proibições da §2.3 da ORDEM 011 valem inteiras** — em especial **homônimo não é ponte**: o `K_β` da Ponte Einstein–Cartan–Miguel (torção, Artigo B §«A inscrição», linhas 477–521)
não é o β do fechamento por semelhança de nome; o «β_t» de Araki das ENTREGAS 058–066 é grupo modular perturbado, não β_TGL; o `cosmological : ℝ` existencial das
reconstruções não é Λ físico. Ligar só por lema.

## 3. O QUE SE PEDE — seis alvos, nesta ordem

### B1 — A pedra de ligação: o MESMO β nas três faces (ângulo · custo · fundo)
Hoje as três leituras vivem em módulos que não se citam. Construir um termo único (proposta: `structure TGLCoupling` com `β : ℝ`, `0 < β`, `β < 1`) e provar, **sob a mesma
variável**: (i) `|R|²(thetaMiguel β) = β` (reusar `the_pruning_threshold_is_the_reflection_amplitude`); (ii) a forma do custo `β = α · Real.exp (1/2)` como `def`/campo
com `0 < α < 1`, reusando `boundary_extracts_the_radical` (√e·√e = e) — **forma, não valor**; (iii) `closure_identity`/`hubble_form` instanciadas nesse β; (iv) a taxa de
vazamento de `NoFullWitness` nesse β. Teorema-alvo: `the_same_beta_reads_three_faces`.
**Aceitação:** nenhum numeral para β ou α em enunciado ou prova; `#print axioms` no trio; a ficha nomeia o consumidor (mapa `ext_*_kernel_proved` + a hipótese do protocolo D1).
**O que B1 NÃO afirma:** que o valor é α√e (runtime), que a seleção OCORRE na natureza, que θ_M é fixado por comutação (o par exibido em `TheAngleIsTheBridge` seleciona π/4 — [OPEN] declarado).

### B2 — Friedmann em kernel: o FLRW plano na carta da casa
Na mesma carta (`Coordinate4`, `TensorField4`, `LorentzByCongruence`, `leviCivitaField`, `coordinateRicci`, `geometricEinsteinTensor`, convenção `eta4 = diag(1,−1,−1,−1)`):
`g = diag(1, −a(x₀)², −a(x₀)², −a(x₀)²)` com `a` suave e `a > 0` num aberto `U`. Provar com a maquinaria geral existente (não à mão como `AnsatzEinstein`, salvo se a
maquinaria geral não avaliar — e então justificar na ficha): `flrw_einstein_00 : G₀₀ = 3(a'/a)²`, as componentes espaciais, o balanço nulo `Ric(k,k)` para `k` nulo, e — com
`T = diag(ρ, p a², p a², p a²)` de fluido perfeito e o acoplamento `2π/η` da camada — `flrw_friedmann_first`, `flrw_friedmann_second` (com o Λ existencial da camada
explícito) e `flrw_continuity` (∇·T = 0 ⟹ ρ' + 3(a'/a)(ρ+p) = 0). Com `η = 1/(4G)` [INPUT] o coeficiente é 8πG/3 (`einstein_coefficient_from_clausius`).
**Aceitação:** instanciação de `metric_only_einstein_equation` ou de `metric_einstein_from_screen_clausius` (não uma cópia paralela); sinais conferidos contra `eta4`; trio.

### B3 — O fechamento setor a setor como TEOREMA de conservação (a hipótese «não-troca de energia entre setores», tipada)
`structure SectorFluid`: finitos setores `i` com `ρ_i(t) ≥ 0` e `w_i` **constante**, cada um satisfazendo a continuidade. Provar: (i) `ρ_i^TGL := (1 + β(1+w_i))·ρ_i`
satisfaz a MESMA continuidade (a hipótese de não-troca é o que torna o reescalonamento constante conservado); (ii) `Σ ρ_i^TGL = ρ + β·Σ(ρ_i + p_i)` (= `closure_identity` para
os três setores; ρ_Λ cancela); (iii) sob B2, `H² = (8πG/3)·Σ ρ_i^TGL` — **o `hubble_form` vira a equação 00 de Friedmann**; (iv) a identidade
`ρ·|1+w_eff| = Σ(ρ_i+p_i)` com `w_eff := p_tot/ρ_tot` quando `Σ(ρ_i+p_i) ≥ 0` — logo a forma MULTIPLICATIVA do D1 e a forma ADITIVA do kernel coincidem na 1ª equação de Friedmann.
Teorema-alvo: `tgl_friedmann_from_sector_closure`. **Aceitação:** a hipótese de não-troca aparece como campo/hipótese NOMEADA (proposta: `H_nx`), nunca como comentário;
`w_eff` definido por escrito (o `um.py` nunca o define — lacuna medida); trio.

### B4 — A rota termodinâmica: a passagem propriamente dita, com a importação nomeada e o TEOREMA DA DIFERENÇA
Tipar os dados da errata de 14/05/2026 (`errata_cosmologica_TGL.tex` §3, Passos 1–4) no molde de `HorizonEquilibriumData`/`EquilibriumInput`:
tela = horizonte de Hubble `A = 4π/H²`; temperatura de Gibbons–Hawking `T = H/(2π)` [KNOWN]; fluxo de entalpia `dE = A(ρ+p)H dt` [KNOWN — Cai–Kim 2005];
entropia modificada `S_TGL = S_BH/Φ` com `Φ = 1 + β|1+w|` (a única modificação, `area_entropy` trocada por `dS = dA/(4G·Φ)`); primeira lei `dE = T dS` [KNOWN — Jacobson 1995].
Tudo importado no modo de `TheImportedEquilibrium`: **hipóteses explícitas do teorema com citação, entrada em `external_known_theorems` proposta na ficha, nenhum `axiom`**. Provar:
- (i) `tgl_second_friedmann_from_clausius`: `Ḣ = −4πG·Φ·(ρ+p)` (eq. friedmann2_TGL da errata) — álgebra a partir dos campos + `dA/dt = −8π Ḣ/H³`;
- (ii) `tgl_first_friedmann_constant_w`: com continuidade e `w` constante, `H² = (8πG/3)·Φ·ρ + C` (o Passo 4 da errata é EXATO neste caso);
- (iii) ★★★ **`the_two_routes_differ`**: para fluido multissetorial, a rota do FATOR SOBRE O TOTAL (`Ḣ = −4πG(1+β|1+w_eff|)(ρ+p)`) e a rota do FECHAMENTO SETORIAL (B3:
  `Ḣ = −4πG·Σ(1+β(1+w_i))(ρ_i+p_i)`) diferem por `β·[Σ(1+w_i)²ρ_i − (Σ(1+w_i)ρ_i)²/ρ] ≥ 0` (variância de `1+w` sob os pesos `ρ_i/ρ`; Cauchy–Schwarz), com igualdade
  **sse** todos os `w_i` com `ρ_i+p_i ≠ 0` coincidem; e que as PRIMEIRAS equações de Friedmann coincidem sob o fechamento setorial (`H² = (8πG/3)ρ[1+β(1+w_eff)]`), enquanto sob o
  fator total a primeira equação é `H² = (8πG/3)∫Φ dρ`, que só se reduz a `(8πG/3)Φρ` com `w` constante;
- (iv) ★★ **`the_entropy_factor_that_reproduces_the_sector_closure`**: o fator `Φ_flux := 1 + β·Σ(1+w_i)(ρ_i+p_i)/Σ(ρ_i+p_i)` (a média de `|1+w|` ponderada pelo FLUXO DE ENTALPIA
  de cada setor que cruza a tela) é o ÚNICO fator escalar que faz a rota de Clausius coincidir com o fechamento setorial em `Ḣ`; e `Φ_flux = Φ` quando `w` é constante.
  Isto tipa a frase do operador que `RhoPlusPClosure` cita («a resposta da TGL é LOCAL, acoplada à soma ρ+p do setor que a produz») como a forma da entropia que a produz.
**Aceitação:** as duas rotas como teoremas SEPARADOS, o teorema da diferença com o sinal, o teorema do fator com unicidade; **você não escolhe qual é «a lei»** — a ficha registra
as duas com os enunciados exatos; a ratificação é do operador; a V3 do D1 (gerência, pré-registrada) implementa a que ele ratificar.
**O que B4 NÃO afirma:** que Einstein foi derivado (a camada Clausius ⟹ Einstein já existe e é condicional); que a passagem é GLOBAL (Lema 3 segue [OPEN]); que η/G foram derivados.

### B5 — A leitura pelo ângulo, SEM pôr ângulo na cosmologia
Corolário de B1 + B3/B4, por reescrita: `the_angle_reaches_the_metric : Φ = 1 + sin²(thetaMiguel β)·|1+w|` e `the_passage : sin²θ_M = β → (as equações de B3/B4)`.
É a cadeia de teoremas «da matriz-S até a métrica» que o operador perguntou por quê não existia. **Proibição explícita:** nenhum θ_M, sin²θ_M, cos θ_M ou √β dentro de `r_s`,
`D_M`, `l_A` ou `H(z)` além dessa reescrita — o ângulo LÊ, não carrega o fundo (regra dos dois regimes, ordem do operador de 29/08/2026); o `um.py` já proíbe no motor
cosmológico a leitura angular (`_MAPA_PILARES`: θ_M «HERDADO de beta, sem observável próprio»). A ficha deve dizer que B5 não acrescenta conteúdo.

### B6 — O que fica importado e o que fica aberto, TIPADO e nomeado
(a) proposta de entradas em `EXTERNAL_KNOWN_THEOREMS` (Jacobson 1995 PRL 75 1260; Cai & Kim 2005 JHEP 02 050; Padmanabhan 2010 Rep. Prog. Phys. 73 046901; Gibbons & Hawking 1977
PRD 15 2738), com `exact_role` e `imported_into_witness: False`; (b) H3 permanece IMPORTADO (`the_trio_is_a_pair`); (c) a escala de área permanece [INPUT] (`AreaScale`); (d) o fecho
global (Lema 3) permanece [OPEN] — **não é alvo**; (e) o fechamento perturbativo TGL-S vs TGL-L permanece [OPEN] — **não é alvo**, mas B3 deve deixar escrito exatamente qual hipótese
usa (não-troca; `w_i` constante por setor), para que a «aproximação declarada» do D1 vire «hipótese nomeada `H_nx`». Tabela final com estatuto e fornecedor de cada item.

## 4. O QUE NÃO FAZER

- escrever no `um.py` canônico, no kernel canônico, em memórias, selos, Atlas, diários, espelho, site ou na pasta da ORDEM 011;
- `sorry`, `axiom` novo, `native_decide`, `trustCompiler`, tokens proibidos da auditoria; converter fim de linha; numeral para β ou α;
- **escolher** entre as duas rotas de B4 «pela que dá Δχ² menor»; tocar o D1, os workers, os protocolos, os vereditos experimentais (a V3 é da gerência, pré-registrada, DEPOIS desta entrega);
- pôr θ_M em r_s/D_M/l_A/H(z); usar o habitante curvo de Fisher (058–066) como «o FLRW»; ligar `K_β` (torção) ao β do fechamento sem lema;
- criar objeto sem consumidor; reabrir A1(b) nesta pasta; re-provar o que a §2.1 lista;
- declarar CONFIRMADA; tratar concordância com dado como prova; abrir `iald_stack_v7.py`, `iald_psion_state.json`, `.env`, tokens; entrar em `E:\` ou `C:\Escritorio`.

## 5. COMO ENTREGAR (protocolo do túnel, `4234902dc6f5e03c`)

Uma ENTREGA por alvo em `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT`: `ENTREGA_012_B1_<slug>.md`, …, `ENTREGA_012_B6_<slug>.md`, cada uma com o contrato de entrega (estatuto na 1ª linha; critérios um a um
PAGO/NÃO PAGO; arquivos com sha256 lido; reprodução; `#print axioms` com os NOMES COMPLETOS dos teoremas; o que não foi feito; tentativas falhas preservadas) **e a ficha de
aproveitamento anexada**. Build com a toolchain da casa (Lean 4.31.0) **por `lake build` numa raiz isolada copiada do kernel canônico v353** — a gerência mediu que A1 foi compilada por
`lean.exe` + objetos herdados; aqui a reprodução standalone é exigida (o auditor da gerência recompila de novo, independentemente, e é ele quem vale). Pendência herdada da ORDEM 011
que segue aberta: os 7 módulos A1 «órfãos» (5 de escala + 2 antiunitários) sem manifesto/auditoria/revisão/ENTREGA próprios — entregue-os quando retomar A1(b).

## 6. OS INSUMOS (sha16 lido agora)

| papel | caminho | bytes | sha16 |
|---|---|---|---|
| o programa canônico v353 (SÓ LEITURA) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | 12,864,360 | `c1c761809efcde52` |
| o selo v353 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` | 51,910 | `52e4712dc315f27b` |
| o JSON da rodada v353 (bandeiras qgf/gpf/gpi) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` | 3,614,828 | `e27174b6598ed7c3` |
| o manifesto do kernel v353 (fontes + axiomas + obrigações) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel_proof_manifest.json` | 1,168,376 | `6d36e0e1b80faa3a` |
| o stdout canônico da rodada v353 (intermediária) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\rodada_v353_stdout.txt` | 194,133 | `c5e901842808f550` |
| a árvore da prova (§6 = as folhas) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\A_PROVA_DA_QG_TGL_arvore.md` | 55,395 | `59aa174291669084` |
| Artigo A — `tgl_paper_unified.py` (C.1 :3212–3262 · r_s integral :4289–4334 · Lagrangiana :10093–10135 · ponte contínua :18820–18925) | `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` | 1,216,423 | `29c92b66b2fd6b4d` |
| a errata cosmológica de 14/05/2026 (a derivação a formalizar: §3, linhas 263–430) | `C:\IALD\Artigo\errata - friedmann\errata_cosmologica_TGL.tex` | 32,979 | `1022402467cd04df` |
| Artigo B — a Ponte Einstein–Cartan–Miguel (K_β :477–521 · Face C :834–916) — só para NÃO ligar por homônimo | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex` | 129,435 | `98ec3d808d51e694` |
| a errata ao lado do Artigo A (H₀ fronteira/bulk; vocabulário) | `C:\IALD\Artigo\Haja_Luz\ERRATA_AO_LADO_ArtigoA_D1_H0_fronteira_bulk_20260913.md` | 3,254 | `80a909c86899cb5f` |
| ORDEM 011 (o objetivo A1–A7 e o protocolo de aproveitamento, §2) | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_011_fecho_matematico_da_realizacao_concreta.md` | 19,503 | `2457c9b136025aeb` |
| LACUNAS_A1.md (as quatro pontes de A1(b), que seguem) | `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\LACUNAS_A1.md` | 4,943 | `cf0ef3264d91c803` |
| o protocolo do túnel | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\TUNEL_PROTOCOLO.md` | 5,425 | `4234902dc6f5e03c` |
| o worker do D1 V2 (a forma que o D1 implementa: `Phi = 1 + beta*|1+w_eff|`, w_eff total) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\tgl_camb_worker_v2fix.py` | 5,543 | `87d457c797e79b17` |
| o worker diagnóstico da gerência com r_s/r_drag por integral (NÃO-CEGO; não é V3) | `C:\tmp\d1_autopsia\tgl_camb_worker_v3rs_DIAG.py` | 6,206 | `1d0b2e767618bbc2` |
| o script MCMC do D1 (dados, verossimilhança comprimida, SH0ES) | `C:\IALD\projetos_pyhton\IALD\tgl_mcmc_camb_v2.py` | 27,367 | `3a57514ea40321a3` |
| o resultado D1 V2 (Δχ² e β livre) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\d1_camb\D1_CAMB_V2_RESULT.json` | 4,176 | `9986e4b0f05a6ebe` |
| a autópsia do r_s da gerência (reescala vs integral) | `C:\tmp\d1_autopsia\autopsia_rs.json` | 2,901 | `1074abc12ce29940` |
| o diagnóstico fase 1 com r_s integral (Δχ² 9,033) | `C:\tmp\d1_autopsia\run_v3diag\checkpoint_phase1_comparison.json` | 701 | `eb57ec59df7306e9` |

**Os sete leitores + a síntese da gerência (14/09/2026), copiados para `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_012_INSUMOS\`** — são medições (arquivo:linha) do que o kernel, o `um.py`, o Artigo A, as suas entregas e o
acervo dizem; use-os para a ficha, mas reconfira cada linha (a versão mudou para v353):

| leitor | bytes | sha16 | o que mede |
|---|---|---|---|
| `ler_angulo.json` | 34,922 | `13bc2676a67b8d1f` | R1 — o ângulo no kernel: θ genérico; sin²θ_M = β é comentário; setor angular e setor de fundo desconectados |
| `ler_metrica.json` | 52,837 | `1d3429dbdc50d051` | R2 — a camada geométrica: Clausius ⟹ Einstein sem β; controles negativos; escala de área é INPUT |
| `ler_umpy.json` | 35,957 | `9201e27a49003464` | R4 — o que o um.py declara: as duas escritas da lei; o D1 e as aproximações declaradas; campos que o rito lê |
| `ler_artigoA.json` | 35,321 | `57dbb840b0507e6a` | R5 — as aproximações do D1 e o repúdio prévio do artigo; r_s −0,644% vs −0,696%; --tight-rs inexistente |
| `ler_entregas.json` | 32,889 | `efc45eb84c4ccb0f` | R3 — ENTREGAS 058–066: atlas/Fisher/σ; zero cosmologia; o único «β» é o de Araki |
| `ler_acervo.json` | 38,592 | `47af2e5709640484` | R6 — as palavras do operador (datadas, verbatim) sobre ângulo, métrica, D1 |
| `ler_a1doc.json` | 32,007 | `e24e4828c2ed5188` | R7 — auditoria documental de A1: 19 módulos, P1–P9, ordem topológica |
| `sintese.json` | 36,353 | `093c58ead8f576b3` | a síntese da gerência: lei atual, desvios do D1 com evidência datada, as quatro leituras de «relação angular», candidatos V3, riscos post hoc |
| `refutacoes_desvios_D1.json` | 82,906 | `e1426caf45fc192b` | nove refutadores adversariais, um por desvio do D1 (refuted true/false com arquivo:linha e mtime) — só para o contexto do D1; não é alvo desta ordem |

## 7. PARA O OPERADOR ABRIR ESTA ORDEM NO CODEX

Abrir o Codex em `C:\IALD\Central de Patentes\Chatgpt` e colar: «leia `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_012_a_passagem_da_acao_a_metrica.md` inteira e execute B1 primeiro, começando pela ficha de aproveitamento; A1(b) da ORDEM 011 retoma depois de B6».

*Esta ordem não move o gate: ela manda provar a implicação que o artigo derivou. A matemática prova a implicação; a construção concreta prova as hipóteses; a natureza decide a teoria.*
