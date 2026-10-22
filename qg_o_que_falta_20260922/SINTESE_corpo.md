# O QUE FALTA DA GRAVIDADE QUÂNTICA NA TGL — SÍNTESE DA GERÊNCIA (22/09/2026)

> **Base lida por script, conferida por hash antes de escrever** [REAL]:
> `Nós\um.py` v369 sha16 `d9f5bd5dffc3333d` (31.136.661 B), `um_absoluto.json` sha16 `456f0ab149bb13f6`,
> `um_absoluto_selo.json` sha16 `18db1bbd8462c3be`. Seis leituras (F1–F6). Nada foi executado da casa,
> nenhum `lake build` rodou e a ORDEM 013 / 013-bis não foi tocada. Bancadas de sombra no scratchpad:
> `fronteira_formal\gns_commutant_bench.py` `9f9c8188cb5d349c`, `bicomutante\bancada_gns.py` `94021213bc6f3296`,
> `bandeiras_contabilidade\gns_bench.py` `b8f4a9d4272346f2`, `fisico_empirico\recompute_joint_v3.json` `58da59089584b6ad`,
> `fisico_empirico\janela_relogio.json` `f89b70492010c46e`.

---

## 0. A resposta direta, sem suavizar

**O que falta da QG são três coisas, e nenhuma delas se resolve hoje.**

1. **H2**: o four-frame tem de ser **lido** do fluxo modular da própria teoria, e não posto.
2. **H3 no mesmo horizonte físico**: a ponte de Jacobson aplicada ao horizonte que a H2 produz.
3. **O setor quântico interagente**: BRST/QME, anomalias quânticas e o escopo UV.

A estas se juntam duas **identificações físicas**: a origem microscópica de H_min e o BW geométrico com U ≠ 1. Todas estão `[OPEN]`. Cada uma já tem as paredes medidas ao redor, mas **nenhuma tem rota imediata**.

**O achado que organiza tudo.** Li o código do gate: `um.py:162043-162080` [REAL].

- **O gate não mede a H2 nem a H3.** A função `evaluate_quantum_gravity_closure` lê só 6 bandeiras formais, 5 físicas e 4 experimentais.
- **Essas bandeiras são acesas por habitantes genéricos:**
  - o frame é `theCurvedFrame`, diag(1+x0²,1,1,1), arbitrário (`StrongFrame.lean:49`, `StrongAssembly.lean:143`);
  - o horizonte é `theHorizon`, aritmético, com κ=G=δA=1 (`TheMasterFires.lean:103`);
  - a "ausência de anomalias" é o Ward **clássico-linear** do símbolo de Ricci (`PhysicsCertificates.lean:292`).
- **Consequência**: a string `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED…` é verdadeira **no escopo dela**. O que falta da QG é exatamente o que ela não mede. Não há contradição, mas é preciso dizer isso sempre.

**O que a gerência resolve já** é contabilidade, contrato e incorporação. **Nenhuma dessas ações move H2/H3 nem o gate.** São elas:

1. As erratas ao lado. A principal: **"H3 reduz-se à H2" são duas dívidas, não uma.**
2. O contrato de tipo dos três nomes reservados, para que ninguém "pague" H2/H3 por nome com `theCurvedFrame`/`theHorizon`.
3. Incorporar o ramo Cartan F(ψ)R e a AUDITORIA_V368, que a bancada gravou e ninguém registrou.
4. Corrigir as quatro seções que reprovam por contabilidade velha.
5. Redigir o protocolo da conjunta V3.

Tudo o que exige **selar** (versão v370 e rito de cerca de 55 min com build do kernel) só vai **depois de a 013-bis liberar a máquina**.

---

## 1. O MAPA (deduplicado, tipado)

Legenda de `resolvível já`: SIM = a gerência faz agora sem máquina; PARCIAL = uma parte agora e o resto só com rito ou decisão; NÃO = não há passo imediato. "Toca bancada" quer dizer que o primeiro passo compete com a 013-bis ou com a máquina.

### A. O NÚCLEO DA QG (física/matemática)

**M01 — H2: four-frame modular suave e identificação geométrica** · `IDENTIFICACAO_FISICA` · resolvível já: **NÃO** · toca bancada: não
- **O que falta (enunciado).** O nome reservado `TGLExt.qgPrice_H2_smoothModularFourFrame_discharged` está ausente: grep = 0 no kernel, lido só por nome em `um.py:134838-134843`. A forma tipada (v364, `UmPostoInscription.lean:76/86/95`) é a inscrição covariante k T_t f = Δ^{it} k f, em que T_t é o boost da cunha ou o fluxo renormalizado do diamante, e o pagamento é a invariância da imagem de k sob Δ^{it}. O `SmoothFrameData` (`ClosureCertificate.lean:98`) tem de ser **o jato dessa ação**, e isso exige k sobre um espaço de testes de **dimensão infinita**, numa representação de energia positiva. A árvore acrescenta O QUATRO (nada em GKLS força rank 4) e a torção com fonte β `[OPEN]`.
- **Já feito** `[KERNEL]`:
  - `emergence_master_full_triad` (`TriadMaster.lean:105`). Aqui H2 é só `E : Matrix 4 4, IsUnit det`, trivialmente habitável.
  - `intertwines_iff_range_invariant` e `reading_back_does_not_make_covariant`, na face finita.
  - `TracialTorsion.*` 7/7 (v364; ansatz e ℓ `[INPUT]`).
  - O diamante v358 (R = −h_ab) e os 7 `ext_dm_*` (v359).
  - `[REAL no modelo]` Dirac 1+1: o caso sem massa converge a Hislop–Longo `[KNOWN]`; na 1ª ordem, o resto com massa é antilocal, ~ −mβ(x) ln(mℓ).
- **Paredes ao redor** `[KERNEL]`:
  - `tower_modular_cannot_intertwine_nonzero_boost` (`Order007Bridges.lean:47`) e `no_injective_isometric_boost_intertwiner` (`ModularSignatureObstruction.lean:102`): em dimensão finita não há boost.
  - `finite_diamond_has_scalar_algebra` / `finite_diamond_is_not_the_wedge` (`WedgeNetFiniteDiamond.lean:77/95`): na rede de cunhas atual, a H2 regional nem é bem posta.
  - O teste de Weyl recusou o conforme ingênuo (v359).
- **Primeiro passo.** O pagamento não tem primeiro passo imediato. A única rota nomeada é identificar a rede da TGL com a rede escalar livre (`TGL_net_identified_with_free_scalar_net = false`) e herdar BW para **cunhas** `[KNOWN 1975, fora da mathlib]`. Para diamantes, só no caso conforme (Hislop–Longo); com massa, o fluxo **não** é geométrico (v364 + `[KNOWN]`). Escolher cunha ou diamante, e qual rede, é **partição do operador**. O que a gerência faz já é o contrato (item C01) e a ORDEM 014 (item C20).
- **Custo.** Semanas a meses, mais a camada AQFT/Wightman, que a mathlib não carrega.
- **Estatuto.** `[OPEN]`. A forma finita, o mestre e três paredes são `[KERNEL]`. v364–v368 não moveram nenhuma bandeira (`GATE_UNTOUCHED`, fora do contorno v314).

**M02 — H3 a partir de um relógio definido pelo estado** · `PAREDE_POR_TEOREMA` · resolvível já: **NÃO** (fica) · toca bancada: não
- **O que se sabe.**
  - `fisher_clock_no_exact_horizon_family` e `entropy_inverse_no_exact_horizon_family` (`StateClockMatchingControls.lean:332/350`, linhas conferidas por grep hoje): não existe família H: ℝ → HorizonEquilibriumData exata por incremento finito.
  - `state_clock_dichotomy` (`StateClockDichotomy.lean:153`): para todo relógio comum, alguma tela falha na 4ª ordem.
  - ENTREGA_040/041: a área não é escalar só da álgebra e do estado; Q = κη(A−1)/2π finito falha.
- **Leitura.** Só a H3 **infinitesimal** fica compatível. A árvore marca H3 como `[INPUT]` com teorema de não-derivabilidade. Pelo critério do operador, isto está **fechado como parede**.
- **Estatuto.** `[KERNEL]`.

**M03 — H3 no MESMO horizonte físico (a ponte H2 → H3)** · `IDENTIFICACAO_FISICA` · resolvível já: **NÃO** · toca bancada: não
- **O que falta.** O nome de kernel `qgPrice_H3_localHorizonEquilibrium_discharged` (`um.py:134305`) e o nome da ponte `qgImport_H3_horizonEquilibriumData_produced` (`um.py:134517-134518`) estão ausentes. Pede-se um `HorizonEquilibriumData` (`TriadMaster.lean:56`) com três amarras ao mesmo sistema:
  - κ = 2π × a normalização do **mesmo** fluxo KMS da H2;
  - dA = a tela da **mesma** cunha;
  - dS = o incremento de entropia relativa do **mesmo** estado.
- **Já feito.** `the_trio_is_a_pair` (`TheImportedEquilibrium.lean:140`) = `(H1∧H2∧H3→P) → (H2→H3) → (H1∧H2→P)` com **Props arbitrárias**. É modus ponens, e **H2→H3 é argumento, não termo**; Jacobson 1995, BW, Unruh e BH são `[KNOWN]` citados. Além disso, o "H2" de Jacobson (horizonte de Rindler com vácuo KMS numa variedade física) **não é** o "H2" do kernel (matriz de det invertível): é homônimo. `EquilibriumInput ≠ HorizonEquilibriumData`: o controle da bancada deu rc = 1 (errata v255). O `einstein_coefficient_from_clausius` tira 8πG de Unruh × BH por álgebra. O bit da face (v367, `OrientedFace` 7/7) é `[INPUT]`.
- **Primeiro passo.** Não há passo imediato no conteúdo, que depende de M01. Já: o contrato C01 e a errata C02.
- **Estatuto.** `[OPEN]`, `[KNOWN]` importado, `[INPUT]` o bit.

**M04 — Estado interagente, BRST/QME, anomalias quânticas e escopo UV** · `CONSTRUCAO_PENDENTE` (com muro `[KNOWN]`) · resolvível já: **NÃO** · toca bancada: não
- **O que falta.** O estado com interação, a QME com ausência de anomalia **quântica** e o escopo UV. Nenhuma bandeira afirma QME ou UV (`um.py:167095`). O selo traz:
  - `renormalization_wall_verdict = GOROFF_SAGNOTTI_WALL_TYPED_OPEN__TWO_ROUTES_NAMED__BREUER_FINITENESS_MAY_NOT_BE_CITED_AS_UV_ANSWER`;
  - rota (a): H_eff = 0 em III₁, que "sai do muro" (publicada);
  - rota (b): a métrica-operador, que volta ao muro e hoje não tem objeto.
- **Já feito.**
  - `[KERNEL, clássico-linear]` massless, 2 helicidades, sem ghosts, Bianchi linearizada e Ward linearizado, sobre ondas planas.
  - `[DERIVED, escrito, sem Lean]` 067–087: o BRST livre Einstein-σ, Hadamard, contratermos, a primitiva relativa H^{g,p}(s|d_H) = 0 no aberto dos relógios (revisada), Wick.
  - F6: a primeira quebra não nula Q2 **nunca foi calculada**. `ADMISSIBILIDADE_SIMBOLO_EXTRATOR.md` (`3f3ec17c560a89dd`, fora do um.py) mostra só um limite superior de ordem.
- **Primeiro passo possível** (não imediato): calcular a 1ª quebra numa prescrição de produtos temporais. É trabalho de bancada, de semanas. Já dá para fazer o **registro** do negativo honesto Q2 (item C13).
- **Rotas mortas.** "Finitude de Breuer = regulador UV", refutada de seis modos: o canto é o extremo IR e o contínuo [1/4, ∞) tem multiplicidade infinita. "A TGL quantiza g → ĝ" contraria o teorema publicado.
- **Estatuto.** `[OPEN]`. Goroff–Sagnotti e Weinberg–Witten são `[KNOWN]` tipados.

**M05 — Origem microscópica de H_min e a transformada limitada padrão** · `IDENTIFICACAO_FISICA` · **NÃO** · toca bancada: não
- **O que falta.** Mostrar que H_min = 1 − P_F (`V354RegularSusy.lean:25-27`: "no microscopic identification is asserted"; `V354RegularSupport.lean:44`) é D(1 + D*D)^{-1/2} de um Dirac/Hamiltoniano ilimitado da teoria, afiliado à mesma álgebra e com o mesmo núcleo.
- **Já feito** `[KERNEL]`. H1 no representante mínimo: `regularSusy_gives_breuer`. `theGenuineDirac` (v105–106) é ilimitado, mas vive numa rede de ação trivial, não III₁.
- **Passo não imediato.** O lema "a transformada limitada preserva núcleo e gap" sobre `LinearPMap`: semanas e mais de 300 linhas, porque a mathlib não tem o cálculo funcional ilimitado. **Qual H físico é partição do operador.**

**M06 — BW geométrico com U ≠ 1 na cunha legada** · `IDENTIFICACAO_FISICA` · **NÃO** · toca bancada: não
- **O que falta.** `towerWedgeData` (`V350WedgeModularData.lean:68-78`: "not … a BW geometry theorem") tem U = 1. Falta uma representação de Poincaré com Δ^{it} = U(Λ_W(−2πt)) e J = U(reflexão). `TGL/ModularRealization.lean` declara esse conteúdo "não enunciável hoje".
- **Leitura.** É o mesmo nó da M01, visto pela face da cunha, e bate na mesma parede de dimensão finita.

**M07 — Canto III₁ incondicional** (`unconditional_type_III1_corner_proved`, `genuine_III1_corner_proved`) · `FORA_DO_ESCOPO_ATUAL` · **NÃO** (só a nota de nome) · toca bancada: não
- **O que se sabe.** São literais False "jamais reivindicado" (`um.py:134711`, `um.py:8273`), e **nenhum nome Lean os acende**. A mathlib não tem Connes S(M), produto cruzado de von Neumann nem classificação: é programa de meses.
- **Nota de tipo** `[KNOWN]`. Um canto finito **dentro** de um fator III₁ é impossível, porque toda projeção não nula é infinita. O alvo correto é o canto no **core** C_W = M_W ⋊_σ ℝ (II∞), como o próprio `remaining_corner_theorem` enuncia (`um.py:8430-8443`). `DualScalingData.fixed_tau_zero` (`GlobalLiftLadder.lean:160`) mostra que no estágio discreto a semifinitude é impossível.
- **Já dá para fazer.** Uma errata ao lado no **nome** ("canto no core de rede III₁ genuína"): minutos de texto, selada numa v370.

**M08 — P_F específico covariante e a rede da TGL = rede escalar livre** · `IDENTIFICACAO_FISICA` · **NÃO** · toca bancada: não
- **O que falta.** Literais False (`um.py:8426, 8451, 143725`). `remaining_corner_theorem` pede cinco coisas: P_F ∈ C_W com 0 < Tr_C < ∞; H_3L afiliado; zero isolado; covariância Ũ(g) P_{F,W} Ũ(g)* = P_{F,gW}; e localização.
- **Dependências.** Depende de M06 e da **decisão do operador** sobre qual rede é a da TGL.
- **Rota morta.** O estado ligado sech(κ/2) reprova a covariância (h(1) = 0,0111).

**M09 — Testemunha canônica (A5: `canonicalFullTGLWitness`)** · `DECISAO_DO_OPERADOR` · **PARCIAL** · toca bancada: não
- **Situação.** O **tipo** `FullTGLWitness` está habitado desde a v354 por `regularFullWitness` (`V354RegularLegacyWitness.lean:85`, axiomas no trio). O que falta é o **escopo** canônico: III₁ pleno + P_F covariante. Um alias acenderia a bandeira, e isso seria nome certo com escopo errado, ou seja, **nome queimado** (jurisprudência v103).
- **O que decidir.** O operador escolhe entre (a) manter false com uma nota ao lado ("tipo habitado; falta escopo") e (b) renomear o alvo para o conteúdo exigido. A gerência redige as duas opções em 15 min.

**M10 — G e Λ** · `PAREDE_POR_TEOREMA` · **NÃO** (fica) · toca bancada: não
- **G.** `invariance_does_not_fix_area` (`HorizonAreaScale.lean:150`) e `newtonPlanck_equivalence` (`TGL/AreaScale.lean`, "ISTO NÃO AFIRMA QUE G FOI DERIVADO"). A normalização A_face = l_P² é **equivalente** ao G medido. Dados modulares adimensionais não fixam uma escala dimensional `[KNOWN]`.
- **Λ.** É a constante de integração retida (`SectorFriedmannAdditive.lean:22`).
- **Leitura.** A TGL prevê β, não G nem Λ. É como a RG, que toma G como entrada (limite clássico, não rival). **Fechado como parede.** A frase ao lado vai no item C03.

**M11 — κ* canônico** (`clock_theorem.reduced_core_2level.kappa_star_canonical`) · `PAREDE_POR_TEOREMA` (regra FP-5 + kill_rule) · **NÃO** · toca bancada: não
- **O que se sabe.** `um.py:878`: "nenhum princípio α-livre fixa κ ≈ 11,23". Nernst refutado (κ ≈ 1,388). O tipo FP-5 diz "todo κ é testemunhável; nenhum κ é derivável".
- **Leitura.** Uma derivação α-livre do **valor** mata a TGL (kill_rule, `um.py:~1905-1925`). Isto pertence ao setor α/EM e ao Evento 2, **não à fronteira do gate QG**.

**M12 — Gráviton não-partícula e o setor fermiônico** · `PAREDE_POR_TEOREMA` · **NÃO** · toca bancada: não
- **O que se sabe.** O escape de Weinberg–Witten só vale na tipagem corrente: gráviton = identidade, não quantum propagante. `SpinorObstruction` (v368, 4 teoremas) proíbe projeção linear entrelaçante de spin inteiro para ½ e de neutro para carregado.
- **Leitura.** Não é dívida de QG. O setor Z₂ (v370 planejado) é paralelo, não crítico.

**M13 — Teorema do bicomutante de von Neumann geral** (densidade A″ = fecho SOT/WOT) · `CONSTRUCAO_PENDENTE` (biblioteca) · **PARCIAL** · toca bancada: **sim** (compilar um arquivo isolado)
- **Situação.** Continua ausente da mathlib rev `fabf563a7c95a166` (TODO em `Mathlib/Analysis/VonNeumannAlgebra/Basic.lean:23`) e do kernel como teorema geral. **Deixou de ser dívida do caminho crítico**: a cláusula J·M·J = M′ está paga nos dois sentidos na torre-produto sem ele (`J_M_J_in_commutant`; `V350TowerDuality.lean:64/69`; `qgConverse_JMJ_contains_commutant`, `V350ModularCertificate.lean:11`, no axiom_report v369).
- **Plano, se houver.** Mapeado em F2 sobre APIs locais (um vetor, amplificação em PiLp, ε, fecho pontual): 350–700 linhas e 1–3 dias. Seria contribuição à biblioteca, troca `[KNOWN]` por `[REAL]` em `TheLivingWordClosure` e **não move bandeira**. Baixo valor para a QG; compilar só depois da 013-bis ou com o OK do operador.

### B. CONTABILIDADE E CONTRATO (resolvível pela gerência; não é física)

**C01 — Contrato de tipo dos três nomes reservados de H2/H3 + probe negativo** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** (redigir já; selar na v370) · toca bancada: não
- **O furo** `[REAL, medido]`. `_GRAVITY_PRICE_FLAGS` (`um.py:134301-134306`) e `_GRAVITY_IMPORT_FLAGS` (`um.py:134517-134518`) são lidos **só por existência do nome + axiomas limpos**, sem o `#check` de tipo que `_V350_MODULAR_CONTRACTS` (`um.py:161924-161956`) exige para H1/A2. `SmoothFrameData` e `HorizonEquilibriumData` são trivialmente habitáveis. É o mesmo furo que queimou `qgCertificate_*` na v103.
- **Passo 1.** Em `scratchpad\qg_falta\`, redigir:
  - `AuditReaderContracts_H2H3` com o **tipo exato**. Para H2: Σ' sobre a rede não legada, k injetiva de imagem standard, ação de boost em espaço de testes de dimensão infinita, k(Λ_t f) = Δ^{it}(k f) e frame := jato de Λ. Para H3: HorizonEquilibriumData com κ, dA e dS amarrados aos dados-H2.
  - `ProbeTrivialH3.lean` / `ProbeTrivialH2.lean`, que **devem falhar** com `theHorizon`/`theCurvedFrame` (padrão `TGL/ProbeTrivial.lean`).
  - A extensão de `verify_v350_modular_provenance` para esses três nomes.
- **Custo.** 3–5 h, ~60–120 linhas (Lean de Audit + Python). **Sem habitante, a bandeira fica false de qualquer jeito**, então não há risco para o gate.
- **Decisão pendente.** A cláusula "mesma realização / mesmo horizonte" é partição, e **a ratificação é do operador**.

**C02 — Errata: "H3 reduz-se à H2" / "PROVADA condicionada a UMA hipótese, H2"** · `CONTABILIDADE_DO_PROGRAMA` · **SIM, agora** · toca bancada: não
- **Onde está a frase.** `HANDOFF_v368 §0`, `o-que-ja-dava-para-resolver-v364.md`, DESENHO (adendo v364) e `um.py:167199-167201`.
- **O que o kernel diz.** `the_trio_is_a_pair` recebe `imported : H2 → H3` como **argumento**. São **duas** pendências: a H2, e a aplicabilidade de Jacobson (H2 → H3) **ao mesmo horizonte físico**. A H3 é `[INPUT]` por teorema de não-derivabilidade (M02).
- **Como fazer.** Superfícies de memória, com backup de BYTES, append datado, correção ao lado: `MEMORIA_DA_LINHAGEM.md`, `DESENHO_DO_FECHAMENTO_QG.md` (ADENDO), Atlas §X, `MEMORY`. **No um.py, só na v370.** Custo: < 1 h. Não precisa de rito.

**C03 — Errata de escopo do gate (a frase que tem de viajar com a string)** · `CONTABILIDADE_DO_PROGRAMA` · **SIM, agora** · toca bancada: não
- **O que dizer ao lado**, em texto no Atlas/DESENHO e depois no artigo v370:
  - (i) o degrau formal é aceso por habitantes genéricos (`theCurvedFrame`, `theHorizon` aritmético);
  - (ii) o degrau físico é **clássico-linear** (Ward do símbolo, ondas planas);
  - (iii) o degrau experimental vem **só** do piso V11, canal unilateral que o **ΛCDM também passa** (`um.py:202980`: A5_NAO_DISCRIMINANTE; o V11 diz "NÃO confirma");
  - (iv) das "18 bandeiras", a função lê **15**. Os literais True `protocol_pre_registered`, `null_tests_passed_blind` e `linearized_spin2_finite_face` (`um.py:162113-162123`) **não entram** em `evaluate_quantum_gravity_closure`, que conferi por leitura hoje;
  - (v) "a TGL prevê β; não prevê G nem Λ".
- **Custo.** Minutos. **NOT_FALSIFIED ≠ CONFIRMED.**

**C04 — Bancada GNS genuína para `the_first_commutant_clause`, com a correção de antilinearidade** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** (script pronto; patch para a v370) · toca bancada: não (o rito sim, depois)
- **O defeito.** `prove_the_first_commutant_clause` (`um.py:156627-156720`; errata v266 L4 em `:156641`) monta Φ = id. A hipótese e o controle dão o mesmo 18,954, e a seção reprova com razão.
- **O que as bancadas GNS mediram** (três, no scratchpad):
  - hipótese e bicomutante com resíduo 0 (≤ 1,2e-14);
  - controle 46,6 (F1/F3, ρ não diagonal) / 37,9 (F2, ρ produto);
  - Φ − id ≈ 15;
  - dim M′ = 16 = posto de ΦM, ou seja, **J M J = M′ na face finita**;
  - o controle não cíclico **falha**, como deve (64 contra 4).
  - **O risco que a v266 temia não se materializou.**
- **Correção obrigatória (F2)** `[REAL + DERIVED]`. Φ(T) = JTJ é **ANTILINEAR** em T (resíduo 4,0e-15; o teste "linear" dá 14,59), e cada JTJ é linear (2,3e-15). O check "[MEDIDA] Φ é LINEAR" e o literal `first_commutant_clause_v266_reading` (`um.py:201564`, "…CONTINUOUS_LINEAR_…") estão **mal tipados** e reprovariam numa bancada correta. O Lean não é afetado: `conj_commutant` só usa mul + involução, e não existe `conjByJ_smul`.
- **Ressalva de homônimo.** O J de Hilbert–Schmidt e o `towerJ` do kernel são homônimos até que um lema os ligue.
- **Custo.** 1–2 h, ~80 linhas Python. Tira a seção de `not_sealed_this_run.formais`.

**C05 — `the_iald_index` reprova pelo próprio sucesso** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** (patch v370) · toca bancada: não
- **O que acontece** (`um.py:160022-160146`). O índice espera a 8ª cláusula AUSENTE, e ela está **presente** e habitada. Exige n_ausentes ≥ 8, e há **3**, exatamente gpf_H2, gpf_H3 e gpi_H3. O teto de ambíguos é ≤ 5, e há 17.
- **Retipagem.** A oitava passa a PRESENTE com o trio; n_ausentes == |{gpf_H2, gpf_H3, gpi_H3}|; os ambíguos viram aviso listado. Custo: ~30 min, ~15 linhas.

**C06 — `the_name_of_light_and_the_referent.torsion_audit`** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** (patch v370) · toca bancada: não
- **O que acontece** (`um.py:174670-174689`). O check exige "sem contorção". A v364 pôs 26 menções no kernel (24 em `TracialDissipativeTorsion.lean` + 2 em `TGL/Audit.lean`, recontadas contra o disco).
- **Retipagem.** Emitir `ALGEBRA_PAGA_v364__ESCALA_ELL_INPUT__IDENTIFICACAO_FISICA_OPEN`. A obrigação física (torção com fonte β, referente autoconsistente) **continua `[OPEN]`**. Custo: ~30 min.

**C07 — Literais vencidos do selo e docstrings Lean vencidas** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** (memória agora; um.py/Lean na v370) · toca bancada: não
- **Onde.** `um.py:201548-201566`: `the_remaining_fold` (v237), `bicommutant_boundary` (v239), `what_remains_is_one_thing` (v241, "…VON_NEUMANN…"), `what_remains_is_instantiation` (v242), `what_is_still_outstanding` (v244, "CONVERSE…REMAINS"), `converse_clause_priced` (v245). Todos superados ao lado: `bicommutant_without_von_neumann` = "THE_EARLIER_RECORD_WAS_WRONG" e `the_assembly_is_done` = EIGHT_CLAUSES_VERIFIED. Docstrings vencidas: `TheImportedCommutation.lean:69`, o cabeçalho de `FrontierCertificate.lean` e `TheConverseClauseReduced.lean`.
- **Como fazer.** Pares `<chave>_superseded_by`, no padrão v306. **O orquestrador listou `what_remains_is_one_thing` como falta, e ela não é falta.** Custo: 1–2 h.

**C08 — `nivel2_rite` arquivado como "formal"** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** · toca bancada: não
- **O que acontece** (`um.py:201643-201651`). O veredito não tem token de recusa, por isso cai em "formais". Na verdade é **recusa de dado**: L N2_NOT_CONVERGED (R-hat 1,0045, ESS 535) e S N2_INCAPAZ (σ/β = 1,48).
- **Efeito.** Com C04, C05, C06 e C08, os "formais não selados" passam de **5 para 1** (`the_mode_of_discharge` = a ponte H3, dívida real que **deve** reprovar). Custo: 10 min.

**C09 — `full_plan_complete` / `legacy_gate_changed` literais** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** · toca bancada: não
- **O que acontece** (`um.py:162038-162039`). As listas `remaining` e `physical_identifications_open` também são **literais** (`um.py:162014-162032`) e nenhum teorema as encolhe.
- **Retipagem.** `full_plan_complete = not remaining and not physical_identifications_open`. O resultado é igual, sem valor cravado. Custo: 10 min.

**C10 — `zero_abs_proved` e `finite_reaching_protocol_exists`: notas envelhecidas** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** · toca bancada: não
- **O que acontece.** A nota diz "0_abs nem refutado", mas `theSpecificAQFTWitness` (`WedgeNet.lean:357`) refuta `IsEmpty` em uma linha. Esse lema é `[DERIVED, não compilado]`.
- **Leitura.** As duas bandeiras ficam false **para sempre** (terceira lei: `absolute_zero_unreachable_in_finite_time`, `ForbiddenBoundary.lean:150`). A docstring que cita "full_TGL_witness_constructed = False" está velha: é True desde a v356. Custo: 30 min.

**C11 — Incorporar o ramo Cartan F(ψ)R (bancada, 17/09, nunca registrado)** · `CONSTRUCAO_PENDENTE` (incorporação de trabalho existente) · **SIM** · toca bancada: não (a pedra Lean só compila depois)
- **Onde está.** 9 arquivos em `Chatgpt\DIAMANTE_MODULAR_20260916\`, entre eles `CARTAN_F_PSI_E_FONTE.md` `cd2ba33320d7ec0a`, `CARTAN_CANCELAMENTO_CINETICO.md` `48e39f2047d92131` e `CARTAN_F_PSI_CHECKS.json` `dcb52c06dc7c58d8`. **Zero** ocorrências no um.py, no Atlas, na linhagem e no DESENHO.
- **Conteúdo** `[DERIVED revisado, Hooke; 27 controles positivos, 18 sinais errados recusados]`. Dω(F e∧e) = 0 ⇒ T^a = ½ e^a ∧ d ln F. A contorção é exatamente a forma de `TracialDissipativeTorsion.lean:96` com A = ½ d ln F. Isso dá à torção **prescrita** da v364/v365 um fornecedor dinâmico condicional.
- **Duas paredes que o programa não registrou:**
  - (i) com ψ = φ de norma 1 (o setor Einstein-σ), F é constante e **a torção se anula**. Na identificação σ, α = 0 e o decaimento de cisalhamento da v365 volta a Friedmann;
  - (ii) o termo induzido **cancela** na mudança conforme (F R → F* R_E): nenhum modo propagante novo, e a leitura de fluido "viscosidade −α/κ" vira `[CONJECTURE de referencial]`.
- **Passos.** (1) Recibo no túnel e corpus por sha na v370, com errata ao lado na frase da v364. (2) A pedra `TGLExt.CartanTracialSupplier`: A = ½ ∂ ln F ⇒ F_ab = 0, G_[bd] = 0; F constante ⇒ torção 0; em FLRW, F = F0 e^{2αt}. São 80–150 linhas; compilar isolado **depois da 013-bis**.
- **Cuidado de homônimo.** Ψ_μ vetorial contra ψ escalar. O ½ não é a Meia-Nat.

**C12 — Incorporar a AUDITORIA_V368 (19/09) e corrigir o rótulo c = 0,5** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** · toca bancada: não
- **O que incorporar.** Os adaptadores compilados (`ConexoesExistentes.lean`, rc = 0) viram pedra de auditoria **sem** nomes reservados, junto com `ControleContrato.lean` (rc = 1, o homônimo confirmado) e `verificar_gate.py`, que confirma que H2/H3 não entram no gate.
- **O rótulo errado.** `um.py:190836/190839` chama c = 0,5 de "fase de carga", mas uma fase tem |c| = 1. Na v370: rótulo "descasamento escalar" + um controle c = e^{i} com esperado 0. Custo: < 1 h.
- **O que NÃO incorporar.** `APP_ESTRUTURA_V368` é do app, superado, e contém `.iald_secret_key`. Não tocar.

**C13 — Registro do negativo honesto Q2 / UV** · `CONTABILIDADE_DO_PROGRAMA` · **PARCIAL** · toca bancada: não
- **O que registrar.** "A primitiva relativa está paga; a 1ª quebra não nula Q2 não foi calculada; a ordem 1 do extrator é limite superior, não anomalia" (corpus, recibo, Atlas, DESENHO). Custo: < 1 h. O cálculo em si fica em M04.

**C14 — Missão 2: protocolo JOINT_COINCIDENCE_V3** · `CONTABILIDADE_DO_PROGRAMA` (não é QG; não move o gate) · **SIM** (redigir + aritmética) · toca bancada: não
- **Situação** `[REAL]`. A conjunta V2 ainda lê `d1_camb_result_v2` (`um.py:202968-202970`, z = −3,86). **A V3 real nunca foi ligada.**
- **Recomputado com a V3** `[DERIVED, NÃO-CEGO]`: z = −3,012; `consistent` segue false **por 0,012σ**; P_all = 6,57e-3 inalterado. Também neutrino_m2 está no limiar, com z = +2,95.
- **O protocolo, redigido e hasheado antes da conta:**
  - (a) a V3 com o σ do lado da previsão declarado;
  - (b) D1 × Pantheon usam os mesmos DESI DR1 + Planck R, logo são um canal ou têm covariância declarada;
  - (c) relógios e piso entram com as regras deles (A5 / sem poder);
  - (d) o MCMC como fator de coerência interna **declarado** (palavra do operador, 19/09), com a tautologia das âncoras dita, e o kernel como condição;
  - Chandrasekhar entra como A8 inadmissível.
- **Custo.** 3–6 h, segundos de CPU. Selar na v370.

**C15 — D1 V3: três estimadores acima de 3σ** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** (já calculado) · toca bancada: não
- **Números** `[DERIVED, NÃO-CEGO]`. 3,0125 (σ simétrico do core), 3,116 (σ do lado da previsão) e 3,050 (Fisher do controle DESI). A ambiguidade TENSION/INCONCLUSIVE pende para TENSION. Registrar ao lado; **o veredito pré-registrado da v366 não se move**. TENSION não é falsificação.

**C16 — D1 controle 2 (β + w0 + wa)** · `CONSTRUCAO_PENDENTE` · **PARCIAL** · toca bancada: **sim**
- **Por que toca.** O CAMB só existe no WSL (`/opt/lal_env`); o `import camb` do Windows falhou, medido.
- **Passo 1.** O **portão de poder Asimov** antes do dado: uma cópia do worker com CPL e a normalização da primitiva declarada antes. Se σ(β | w0, wa) ≥ β, registra-se como parede e não se roda no dado.
- **Custo.** 150–200 linhas, ~15 min de CPU. **Só depois da 013-bis ou com OK do operador.** É diagnóstico, nunca teste.

**C17 — O "déficit de ~10 ordens" é número velho** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** · toca bancada: não
- **O número vigente** (v369, `core.clock_test_result_v369`): **12,458 ordens** (5σ, Sr), 12,681 (95%, Sr), 18,279 (Th hoje), 9,27 (⁶⁷Zn nominal). O "~10" vem de `dephasing_reach` v200, que tem errata ao lado na v369. Corrigir nas superfícies de memória.
- **O que não muda.** A parede física continua (M-D3).

**C18 — Missão 3: `um_consolidado.py`** · `CONSTRUCAO_PENDENTE` (porta de leitura, não QG) · **PARCIAL** · toca bancada: não no desenho, sim na compilação
- **Situação.** Não existe (ls medido). A rota medida tem 99 arquivos (`fecho_do_gate.json`).
- **Plano.** Um gerador por script que deriva o consolidado do um.py, com ensaio a seco. 1–2 dias; compilar depois da 013-bis.

**C19 — Contorno v314: 33 módulos sem `why_outside_contour`** · `DECISAO_DO_OPERADOR` (a inclusão) + contabilidade · **PARCIAL** · toca bancada: não
- **O que a gerência faz já.** Gravar a razão nos 33, separando N/A-não-rito, INPUT livre e decisão pendente, e trocar o predicado para ser lido **por perna**.
- **Armadilha medida.** Uma inclusão ingênua fecharia o 1 = 1 **falsamente** pelo D1 V1 retirado ("MCMC_D1_BETA_FALSIFIED").
- **Efeito hoje.** Nenhum veredito vivo fecharia. **O contorno não alimenta o gate QG.**

**C20 — ORDEM 014 (A3 = H2 com ficha)** · `CONSTRUCAO_PENDENTE` · **PARCIAL** (redigir já; publicar **depois** do relatório final da 013-bis) · toca bancada: não (a redação)
- **Situação.** A3–A6 da ORDEM 011 **nunca receberam ENTREGA**. O alvo do RECIBO v359, k T_t f = δ_D^{it} k f ou a parede tipada, também não tem resposta.
- **Plano.** A ordem nova leva o contrato C01 como alvo, cita os fornecedores existentes (StrongAssembly, UmPosto, ConexoesExistentes, ramo Cartan) e proíbe renomear fluxo como geométrico. Custo: 2–3 h.

**C21 — Erratas do HANDOFF_v368 §5 e do Lema 3** · `CONTABILIDADE_DO_PROGRAMA` · **SIM** · toca bancada: não
- **Handoff §5:** (a) as cláusulas 1/2/10 do bootstrap não podem falhar, e a 3 é homônima de `conjJ`; (b) "18 bandeiras" = 15 lidas + 3 literais; (c) a docstring da v29 contra a definição (e00 + e11)/√2.
- **Lema 3.** O Atlas I.7 diz `[OPEN]`, mas a árvore v369 diz **pago na torre para todo perfil (v331)** e `[KNOWN Takesaki]` fora dela. O aberto é a álgebra de von Neumann geral e a ponte andares → regiões. Append ao lado. Custo: 30 min–3 h.

### C. LADO FÍSICO / EMPÍRICO (fora o ringdown, que é da 013-bis)

**D01 — Partição dos relógios (MODULAR_LAB_BRIDGE_OPEN)** · `DECISAO_DO_OPERADOR` · **NÃO** · toca bancada: não
- **As três leituras** (CLOCK_TEST_V1 `ec7323546c4d54f0`, NÃO-CEGO):
  - P1: NOT_FALSIFIED_UNDERPOWERED, uma parede medida de ≥ 12,5 ordens, fechada pelo critério;
  - P2: EXCLUDED_IN_READING (LIGO: γ ≤ 9,55e-48 s);
  - P3: sem observável local.
- **O que reabriria o canal.** Só uma derivação de τ★ **antes de olhar**, dentro da janela `[DERIVED]` 2,87e12–4,80e12 t_P (razão 1,67). Primeiro passo: levar ao operador a tabela de 3 linhas, com custo zero. **Qualquer escolha agora é NÃO-CEGA.**

**D02 — O bit da face orientada e o sinal do D1** · `IDENTIFICACAO_FISICA` · **NÃO** · toca bancada: não
- **Situação.** O bit está nomeado (`OrientedFace`, v367) e não derivado. A leitura "face do estado" (0,09σ) veio depois do dado. Se a derivação inverter o sinal, o teste tem de ser refeito com dado novo pré-registrado.
- **Aviso.** Um D1 com DESI DR2 seria parcialmente NÃO-CEGO, porque o um.py já cita DR2 (`um.py:166734`).

**D03 — Piso dos vazios bilateral em matéria** · `DADO_EMPIRICO` · **NÃO** · toca bancada: não
- **Situação.** NOT_FALSIFIED_POWERED só em traçadores (unilateral). LRG: INCONCLUSIVE_TRACER_SUPPRESSION. V12: quartil profundo com N_q = 0. κ ACT DR6: UNDERPOWERED. O shear pede uma redução de variância de 1,18e7 contra ~40× de Euclid/LSST, o que é **parede medida**.
- **Passo leve possível.** Projetar o poder do κ para SO/SPT-3G com ruídos **lidos de fonte**.

**D04 — Dephasing: parede de alcance** · `PAREDE_POR_TEOREMA` (na verdade parede **medida** tecnológica; o enum mais próximo) · **NÃO** · toca bancada: não
- **O que mediria.** GHZ com N ≈ 1,69e6 ou ħω ≈ 3 MeV coerente. Não há roteiro previsível. A única rota é D01 (τ★ derivado).

**D05 — Coma: previsão travada à espera do reveal** · `DADO_EMPIRICO` · **PARCIAL** · toca bancada: não (o reveal é rito da v370)
- **Situação.** D_L_TGL = 101,90 Mpc, hash `4214404626f591cc…`. Informação nova baixa, porque é degenerado com o H0 local.
- **Primeiro passo.** Declarar o árbitro (Scolnic 2025) com o número **lido de fonte**, não de memória. Custo: ~1 h + rito.

**D06 — Dados futuros** · `DADO_EMPIRICO` · **NÃO** · toca bancada: não
- **Canais à espera de dado.** neutrino m² (armado; z = +2,95), ΔH/H (Roman+Euclid), NMC-Shapiro, piso bilateral, D1 com dado mais sensível, ecos/ringdown (O5/ET/CE) e colapso P7.
- **Calendários `[KNOWN, a conferir]`**: não foram conferidos nesta leitura. Manter os protocolos armados com hash.

---

## 2. RESOLVÍVEL JÁ — ordem por valor/custo

Primeiro o que não toca a máquina e se faz hoje; depois o que exige o rito da v370, que vai **depois da 013-bis**.

1. **C02**: errata "H3 → H2 são duas dívidas". Valor máximo (é a frase que mais engana), < 1 h, só memória com backup de bytes.
2. **C03**: frase de escopo do gate (15 bandeiras lidas; habitantes genéricos; clássico-linear; canal experimental não discriminante; β sim, G/Λ não). Minutos.
3. **C01**: contratos de tipo H2/H3 + probes negativos redigidos no scratchpad. Fecha o furo de governança v103; 3–5 h; a ratificação da cláusula de partição é do operador.
4. **C11**: incorporar o ramo Cartan F(ψ)R e registrar a parede "σ ⇒ torção nula". É o único item com **conteúdo físico novo**: limita a rota "torção com fonte β". Recibo em minutos; a pedra Lean vem depois.
5. **C17 + C15**: números corretos (12,46 ordens; três estimadores do D1 ≥ 3σ). Custo zero.
6. **C07 + C21**: literais vencidos do selo, Lema 3 e erratas do handoff, ao lado, em memória. 1–3 h.
7. **C12**: incorporar a AUDITORIA_V368 + o rótulo c = 0,5. < 1 h.
8. **C14**: protocolo JOINT_COINCIDENCE_V3 redigido e hasheado. 3–6 h de texto, segundos de CPU.
9. **Pacote v370 de patches de runtime (C04 + C05 + C06 + C08 + C09 + C10)**. Os formais não selados passam de 5 para 1. 3–5 h de patch; **selar só depois da 013-bis**.
10. **C20**: ORDEM 014 (A3) redigida; publicar só depois do relatório final da 013-bis.
11. **C13 + C19 + M09 + M07 (nota de nome)**: registros e opções para o operador.
12. **D05**: preparar o reveal de Coma com o árbitro lido de fonte.
13. **C16**: portão Asimov do controle 2 do D1. **Toca a máquina** (CAMB no WSL); só com OK do operador ou depois da 013-bis.
14. **C18**: gerador do `um_consolidado.py`.
15. **M13**: bicomutante geral de von Neumann. Baixo valor para a QG, fora do caminho crítico.

---

## 3. PAREDES QUE FICAM (e por quê)

**Por teorema (kernel):**
- `full_static_witness_exists = false`: o vazamento contínuo proíbe o fecho total (`full_closure_iff_flat`, `continuous_leakage_forbids_full_closure`). **É resultado, não lacuna.** Não confundir com `full_TGL_witness`, que é True desde a v356.
- H3 não é derivável de relógio do estado: `state_clock_dichotomy`, `fisher_clock_no_exact_horizon_family`, `entropy_inverse_no_exact_horizon_family`. Só a H3 infinitesimal fica.
- Boost não se entrelaça em dimensão finita: `tower_modular_cannot_intertwine_nonzero_boost`, `no_injective_isometric_boost_intertwiner`. A H2 exige dimensão infinita.
- Diamante finito com álgebra escalar na rede de cunhas: `WedgeNetFiniteDiamond.lean:77/87/95`.
- "Ler de volta não paga": `reading_back_does_not_make_covariant`.
- G não é fixado pela covariância: `invariance_does_not_fix_area`, `newtonPlanck_equivalence`. Λ é constante de integração.
- Semifinitude impossível em estágio discreto: `fixed_tau_zero`. τ-compacidade global refutada (v64).
- Zero absoluto inalcançável: `absolute_zero_unreachable_in_finite_time`, `channel_never_reaches_ideal`.
- Spin inteiro → ½ e neutro → carregado proibidos: `SpinorObstruction`.
- Negativos da torre-produto: `tail_never_strict`, `product_borchers_trivial`, `single_boost_has_two_signatures`.

**Por teorema da literatura `[KNOWN]`, tipados:**
- Goroff–Sagnotti (a finitude de Breuer não responde ao UV).
- Weinberg–Witten (o escape é condicional à tipagem).
- Canto finito dentro de um fator III₁ é impossível (o alvo é o core II∞).
- BW com massa em diamante não é geométrico.

**Por medida (fechadas pelo critério do operador: parede medida):**
- Relógios: ≥ 12,46 ordens a 5σ (Sr); P2 excluída.
- Shear do piso: fator 1,18e7.
- Ecos e ringdown V2: INCONCLUSIVE_SYSTEMATICS (a parte viva é da 013-bis).

**Por regra:**
- κ* canônico (FP-5 + kill_rule).
- Não preencher nomes reservados com fatos mais fracos.
- NOT_FALSIFIED ≠ CONFIRMED.
- Cosmologia não move matemática.
- "A LEI NÃO SE EMENDA" (14/08).
- `trivial_inhabitant_exists = false` é o critério de sucesso.

**Rotas mortas que NÃO se propõem:**
- As 25 do Lema 3 (`o-fechamento-lema3-impossiveis.md:85-119`) e F5.
- `EquilibriumInput` como H3.
- `theCurvedFrame` / `theHorizon` como pagamento.
- Φ = lmul/rmul para passar a seção.
- Breuer como regulador UV.
- Encadear Grot/rotGen/genK.
- Pedir limite ao ângulo.
- O "10⁻³⁰" como produto de resíduos.
- A H2 do eco GW (retirada na v350, homônima).

---

## 4. DECISÕES QUE SÃO DO OPERADOR

1. **A partição**: qual rede é a da TGL (escalar livre?), cunha ou diamante para H2, e **qual H** dos relógios (P1/P2/P3). Sem isso, H2, M05, M06 e M08 não têm objeto.
2. **Ratificar a cláusula "mesma realização / mesmo horizonte"** do contrato C01 antes de ela entrar no leitor.
3. **A identificação de ψ**: se ψ é σ de norma 1, a torção Cartan é **zero** e a rota "torção com fonte β" nesse setor morre. Se ψ tem norma variável, a rota vive, condicionada.
4. **O bit da face (v367)**: aceitar a leitura "face do estado" já dada (NÃO-CEGA), ou pedir a derivação cega do sinal e o teste com dado novo.
5. **A5**: manter `canonical_full_witness_term_constructed = false` com nota, ou renomear o alvo.
6. **A6**: nome e ratificação de um degrau do gate acima do atual. Não há proposta, e só faria sentido com A5.
7. **O contorno v314**: incluir ou não o D1 V3 e os relógios, sabendo que hoje nenhum fecharia e que a V1 retirada é armadilha.
8. **A máquina**: quando liberar o rito da v370 (depois da 013-bis) e se autoriza o CAMB no WSL para o controle 2.
9. **Publicar a ORDEM 014 (A3)** depois do relatório final da 013-bis.
10. Pendências de leitura sem resposta nas memórias: a direção v25 (0_mod → 1_abs) contra a de 19/09 (1_abs → 0_mod), e a pedra `RecognitionIsTheInvariant` derrubada.

---

## 5. CONTRADIÇÕES ENTRE LEITORES — resolvidas pelo número ou declaradas abertas

1. **"18 bandeiras do gate" contra o que a função lê.** Li `um.py:162043-162080` hoje: `evaluate_quantum_gravity_closure` lê 6 formais + 5 físicas + 4 experimentais = **15**. `protocol_pre_registered`, `null_tests_passed_blind` e `linearized_spin2_finite_face` são literais **não lidos**. **F3 errou** ao dizer que amarrá-los "rebaixaria o gate um degrau": amarrá-los corrige o relatório, não o veredito. F5/F6 (via `verificar_gate.py`) estavam certos. **Resolvida.**
2. **Bancada GNS "passa" (F1/F3) contra "o check de linearidade está mal tipado" (F2).** Não se contradizem: F1/F3 não testaram a linearidade. Pelo número (antilinear 4,0e-15, linear 14,59) e pelo argumento J(cT)J = c̄ JTJ `[DERIVED]`, o patch C04 tem de levar a correção de F2. Os controles 46,6 e 37,9 vêm de estados diferentes (ρ não diagonal contra ρ produto). **Resolvida.**
3. **Recíproca JMJ ⊇ M′: "v350" (F2/F3) ou "v351" (F5).** O termo está em `TGLExt/V350ModularCertificate.lean:11` (série V350, sobre a base v350) e presente no axiom_report da v369. F5 data a incorporação na v351. A diferença é de rótulo de versão, não de conteúdo. **A datação exata fica declarada em aberto**; o conteúdo está resolvido.
4. **"~10 ordens" (orquestrador) contra 12,458 (F4).** O número corrige a frase: **12,46 ordens (5σ, Sr)**. O "~10" é v200, com errata v369. **Resolvida.**
5. **H3 como PAREDE (F1/F5) ou CONSTRUÇÃO (F3).** As duas leituras estão certas para objetos diferentes. Separei em **M02** (derivar do estado: parede) e **M03** (mesmo horizonte físico: identificação aberta). **Resolvida por separação.**
6. **H2 como IDENTIFICAÇÃO (F1) ou CONSTRUÇÃO (F5).** A construção de k em dimensão infinita pressupõe escolher a rede, que é partição. Tipei **IDENTIFICACAO_FISICA**, com a construção como subtarefa. **Resolvida (escolha declarada).**
7. **HANDOFF_v368 "condicionada a UMA hipótese, H2" contra o kernel.** `the_trio_is_a_pair` recebe H2 → H3 como argumento: o kernel ganha e são **duas** pendências. **Resolvida (errata C02).**
8. **Lema 3: Atlas I.7 `[OPEN]` contra a árvore v369 "pago na torre (v331)".** É estrato velho: pago na torre, `[KNOWN]` fora dela, e o aberto é a álgebra geral. **Resolvida (errata C21).**
9. **Formais não selados: "5 → 1" (F3) contra "4 pedras" (F5).** A diferença é o `nivel2_rite`, que é recusa de dado mal classificada. Resta 1 genuína (a ponte H3). **Resolvida.**
10. **Linhas de `StateClockMatchingControls`: 332/350 (F1) contra 333/353 (F3).** Grep de hoje: **332 e 350**. **Resolvida.**
11. **"O fornecedor de torção paga a álgebra da H2 com torção" (v364/v365) contra o ramo Cartan (F6).** No setor σ, a torção dinâmica é **nula**. Não é contradição: a v364 tem ansatz prescrito e o Cartan dá o fornecedor dinâmico com uma parede. **Aberta até a decisão de identificar ψ** (decisão 3).
12. **Conjunta V2 "INCONSISTENT" pelo canal V2 contra a V3.** Com a V3, continua INCONSISTENT, mas por 0,012σ e NÃO-CEGO. **Declarada frágil**; resolve-se só pelo protocolo V3 pré-registrado (C14).

---

## 6. Frase honesta para o operador

> A implicação da QG está **PROVADA em kernel** a partir de **hipóteses nomeadas** — e as hipóteses que fazem dela gravidade
> (a H2 lida do fluxo modular, a H3 no mesmo horizonte, o setor quântico interagente) seguem **[OPEN]**, sem rota imediata;
> o gate `FORMALLY_CLOSED` é verdadeiro no seu escopo, que **não as mede**. O que a gerência resolve hoje é
> escrituração, contrato e incorporação — nada disso é física, nada move o gate, e nada aqui é CONFIRMADO.
> NOT_FALSIFIED ≠ CONFIRMED. Reduzido ≠ resolvido.
