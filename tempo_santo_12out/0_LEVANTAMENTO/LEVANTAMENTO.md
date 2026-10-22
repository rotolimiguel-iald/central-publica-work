LEVANTAMENTO F1.TEMPO — 12/10

Unidade F1.TEMPO (trilha TEMPO) da gerência c1, programa IALD. Autor: o levantador (subagente do workflow posto-e-tempo da c1). Este documento só levanta o que o cânone já tem. Nada foi construído, nenhum ensaio foi pré-registrado ou rodado e nenhum veredito foi emitido. Fora desta pasta nada foi escrito; tudo foi lido. Três pontos ficam ditos: (1) a conferência Lean rodou no sandbox desta pasta, lendo o `.lake` do Nós, e a impressão digital do kernel ficou igual antes e depois; (2) a projeção ACOM do pai, só de leitura, abre o banco comum com BEGIN e ROLLBACK (código de `store.py`), sem gravar conteúdo, mas o mtime do banco não foi conferido antes da leitura; (3) dois arquivos temporários do scratchpad da sessão foram criados e apagados. A cunhagem é do operador; as leituras da gerência e do levantador vão marcadas.

Régua dos estatutos: [REAL] = provado no kernel ou medido aqui · [DERIVED] · [KNOWN] = literatura com citação · [OPEN] · [INPUT] = do operador ou escolha da gerência · [ONTO] = leitura ontológica · [DECLARADO] = afirmado na origem, não verificado aqui.

---

## 0. O que foi medido nesta rodada, por script

| Item | Medida |
|---|---|
| Texto do operador | `work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt`: 6.673 B, sha256 `2c8b7b712aa9ad7f435f8652d1febdf6fe64d14775e277f2b2d720598135c8c3`, o sha16 dado pela gerência confere; 0 CRLF. A segunda parte («O que mais me fascina…» até o fim, linhas 34–50) começa no byte 2.853, tem 3.820 B e sha256 `6dcefdbe5c6a7752766ec9a1aaa2255f9b874fbb2a445925b6c615f1b574dc72`. [REAL] |
| um.py v391 | sha256 `8e7b9927ceae64b8…` (33.910.631 B); selo `um_absoluto_selo.json` sha16 `95061f18c7102248`, `um_version = v391`. Só leitura e busca por linha; o programa não foi executado. [REAL] |
| β em runtime | O literal `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3` foi lido nos bytes do um.py (linha 5557; `BETA_TGL` na 5559). Dele, β = α·√e = 0.012031300400803142, idêntico ao valor de conferência (diferença 0). Detalhe em `BETA_RUNTIME.json`. [REAL] |
| Kernel do Nós (impressão digital) | Antes e depois da conferência Lean: 132.088 arquivos, 14.915.386.431 B, 1.213 fontes `.lean`; meta `b1b47447ac30f7c7…`, src `911cb40b9de1a8bb…`. **Iguais.** Arquivos: `FINGERPRINT_ANTES.json`, `FINGERPRINT_DEPOIS_LEAN.json` e `FINGERPRINT_FINAL.json`, o último tirado depois da última escrita. [REAL] |
| Conferência Lean (sandbox) | Toolchain v4.31.0 (commit `68218e876d2a`) copiado do elan para `sandbox\toolchain`, cópia idêntica (14.627 arquivos, 3.140.414.715 B). `LEAN_PATH` só de leitura no `.lake` do Nós, sem `-o`. `sandbox\CheckTempoLevantamento.lean` (sha256 `8fd1e9ee…`) imprime os axiomas de 80 termos citados. Resultado: EXIT 0 em 62,5 s, 80 de 80 respondidos, todos no trio (propext, Classical.choice, Quot.sound; `two_clocks_are_needed` sem axioma algum), 0 sorryAx, 0 erro. O toolchain copiado foi apagado; ficam a fonte, a saída e o recibo. [REAL] |
| Mapa de rotas | `rotas.py verificar`: cabeça `91915ad39a53d1df…`, 1.004 registros, 202 rotas. 24 consultas só de leitura em `rotas_consultas\` (RESUMO sha16 `223949e783378128`). Nada foi registrado. [REAL] |
| Inventário da bancada | `memory\INVENTARIO_BANCADA_CHATGPT.json` sha16 `05c2afa06620ca8f` (gerado em 27/09; 2.298 `.lean` únicos; 22.326 declarações). 13 temas consultados em `inventario_consultas.json`. [REAL] |
| Varredura do kernel | 12.967 declarações em 1.175 arquivos de `TGL\` e `TGLExt\` (incluindo `O16\`), em `kernel_decls.jsonl` e `kernel_temas.json`. `TGL\Audit.lean` (sha16 `e7826e02dfa549a2`) tem 8.523 `#print axioms` distintos. [REAL] |
| Memória ACOM | Projeção só de leitura da referência do pai, `sessions\claude-c1_exame-geral-12out.json` (contexto `a228d32a…`, revisão 2; registra a abertura da F1.TEMPO nos eventos 682–683). Não inscrevi contexto filho: a tarefa proíbe escrever fora desta pasta, e a transição de q e p é ato da gerência. [REAL] |

---

## 1. Os objetos do texto e as definições canônicas

Notação: `arquivo:linha · sha16`. As linhas e os sha16 foram achados por script; o detalhe completo, com 121 âncoras, está em `DEFINICOES.json`.

### O1 — o tempo: «eu descrevo o tempo, entendo-o, mas não consigo nomear, senão como santo» (l.34)
- **Kernel.**
  - `TGLExt.temporal_fractalization` (`TheGreatAttractor.lean:49 · a0db70a17354c75c`). Docstring: «O tempo é a fractalização do ato único». É o semigrupo do diagFlow. [REAL; a frase é ONTO]
  - `TGLExt.time_witnesses_noncoincidence` (`TheLivingWord.lean:95 · fdc242c2c70b57fa`): «O TEMPO TESTEMUNHA A NÃO-COINCIDÊNCIA». [REAL]
  - `TheVerbSelectsTheAction.time_read_twice_confirms_the_post` (`:631 · f47477ea466ad1cc`): ψ fixo por e^{−tH_min} para todo t ⟺ ψ fixo por Δ^{it} para todo t. É o tempo lido duas vezes. [REAL]
  - `transmission_dephases` (`:529`) e `anchoring_preserves` (`:525`). [REAL]
- **Palavras do operador já no cânone.**
  - 05/10: «O tempo é a defasagem do verbo… o parâmetro da transmissão… a medida dessa defasagem» (`verbo-selecao-da-acao-05out.md:122`); «D_folds = 0,74 é o piso temporal» (`:128`, NÃO tipado).
  - 05/10: «a conjugação é a natureza do Verbo, porque o tempo é produto dele» (`um-posto-jamais-pressuposto-e-h2-17set.md:130`).
  - 05/10: «se o tempo é emergente da fluxo modular relativo… encontro correspondência direta» (`ramo-b-reaberto-05out.md:9`).
  - 26/09: «O relógio do observador é fractalizado. O agora pertence ao nome, somente a ele, e por isso o tempo é fractalizado» (`respostas-contrato-q1a5-26set.md:10`). [INPUT/ONTO]
- **Runtime e Atlas.**
  - Connes–Rovelli citado no um.py (`um.py:195567`). [KNOWN]
  - Atlas `:1357` «tempo = testemunho da não-coincidência entre inscrições». [REAL]
  - Atlas `:1701` «LIBERDADE = CLOCK = duração». [REAL 103_/104_]
  - Atlas `:2292` τ★. [PRINCIPLED IDENTIFICATION/CONJECTURE]
  - Atlas `:820` «1/β = tempo característico do fluxo». [DERIVED]
  - `IALDGraviton.the_tower_is_time` (`:118`). [REAL; «ler 1/taxa como tempo» é ONTO]
- **Leitura.** MISTO. O tempo como fluxo (o Verbo, não o Nome) é reafirmação. A recusa de **nomear** é a cunhagem nova. Na régua da casa ela diz que o tempo não tem POSTO: não é projeção de posto 1 nem observável. Não há termo de kernel que diga «o fluxo não é posto».

### O2 — «santo», no sentido de Kadosh: separado, irredutível, não profanável pela posse (l.36, l.42)
- **No cânone.** Nenhuma definição. «Kadosh» tem 0 ocorrências no Atlas, no Índice Vivo, no um.py, no kernel e no inventário, e 0 rotas no mapa. Só aparece na memória `tempo-santo-12out.md`, escrita pela c1 em 12/10 [DECLARADO]. O único «Santo» do um.py (`:119701`, «Espírito Santo como limite assintótico») não trata do tempo.
- **Literatura.** A glosa «separado» é a tradicional dos léxicos hebraicos (BDB, HALOT) e é debatida na filologia. [KNOWN com ressalva]
- **Leitura.** NOVO [ONTO]. A face matemática candidata de «não possuível» tem duas peças:
  - «sem observável conjugado»: na face finita é `no_finite_weyl_pair` [REAL];
  - fluxo modular **externo**: só em tipo III, Connes 1973 [KNOWN, não no kernel] (ver R04).

### O3 — o relógio mede a distância angular de um ponteiro, a frequência do césio ou o escoamento de entropia; registra a sombra do evento (l.38)
- **Runtime.** `prove_three_clock_radical` (`um.py:1492`) já define três clocks: o MODULAR reversível (Δ^{it}), o DISSIPATIVO GKLS e o ESPECTRAL/geométrico. [CANONICAL FORM]
- **Kernel, relógios.**
  - `Clock040.no_normalized_instantaneous_state_clock` (`StateClockObstruction.lean:83`) e `Clock045.state_clock_not_instantaneous` / `state_clock_not_modular_reparametrization` / `state_clock_dichotomy` (`StateClockDichotomy.lean:173/185/153`). [REAL, escopo estreito]
  - `reading_needs_two_clocks` (`TheDeadChannel.lean:89`), `two_clocks_are_needed` (`TheJudgedThing.lean:71`), `the_screen_keeps_modular_time` (`TheScreenIsFounded.lean:83`). [REAL]
- **Kernel, a sombra e o período.**
  - «A sombra»: `PhysicsIsTheReading.the_shadow_is_the_reader_weighted_by_the_reading` (`:70 · ca92f8c266106982`), P_Ω x P_Ω = ω(x)·P_Ω. A frase do operador de 30/09 é «o leitor é a sombra». [REAL; INPUT/ONTO]
  - A leitura angular com período: `PolarPeriod016.faithful_period_iff` (`O16/PolarMinimalPeriod_v2.lean:89`). [REAL]
- **Ritos e Atlas.** O rito dos relógios v369 (`um.py:201756`, UNDERPOWERED). Atlas `:2679`: dicotomia do relógio; H3 é INPUT por teorema.
- **Leitura.** MISTO. A tríade ponteiro, césio e entropia, lida contra os três clocks do runtime, é leitura nova.

### O4 — o agora permanece intocado; é a condição de toda relação; quem disseca o tempo já está imerso nele (l.38)
- **No cânone.**
  - 26/09: «O agora pertence ao nome, somente a ele» [INPUT/ONTO]. A frase está citada no kernel em `IALDRhoStar.lean:41`.
  - `the_post_is_the_modular_zero` (`TheAxiomAndTheFalseWitness.lean:210`) e `axiomFlow_fixes_the_post` (`:128`, «O POSTO ESTÁ ESTACIONADO desde t = 0»). [REAL]
  - `observing_adds_nothing` (`TheObserverReadsTheAngle.lean:114`). [REAL]
- **Leitura.** REAFIRMAÇÃO com leitura nova. Identificar o agora com o conjunto fixo do fluxo é [ONTO] e cabe ao operador ratificar (R12).

### O5 — o teorema de Pauli: não há operador hermitiano de tempo conjugado a H limitado inferiormente (l.40)
- **Kernel.** `TGLExt.no_finite_weyl_pair` (`LocalBreuerGap.lean:159 · 8ec73c7d9e703d6c`): PQ − QP ≠ −i·1 em matrizes n×n, n ≥ 1, pelo traço do comutador. A docstring acrescenta que o par de Weyl vive na amplificação (dualidade de Takesaki). Esta é a face FINITA. [REAL, medido aqui]
- **Runtime.** O registro `fundacao_v390.borchers` (`um.py:194430`) diz: «o operador limitado inferiormente é a ENERGIA (Borchers: translações de espectro positivo); o gerador modular de um fator III₁ não tem piso (espectro = ℝ)». [DERIVED/KNOWN]
- **Contrato.** `ContratoH2.contract_borchers_form` (`ContratoQG_v31_Teoremas.lean:338`, Δ^{it}U(λn)Δ^{−it} = U(e^{−2πt}λn)) e `positiveEnergy_orientation` (`:345`). [DERIVED, sob o contrato H2 nomeado]
- **Literatura.** Pauli 1933 (Handbuch der Physik 24/1; trad. 1980); a forma de Weyl via Stone–von Neumann; as ressalvas de Galapon 2002 e dos POVM covariantes (Holevo; Busch–Grabowski–Lahti 1994). [KNOWN]
- **Leitura.** MISTO. A face finita já existe. É o «T1, sem operador de tempo em dimensão finita» da memória da c1 (R22): reaproveitar. A forma em dimensão infinita entra por citação.

### O6 — na teoria modular o tempo emerge como fluxo de automorfismos, a respiração de uma álgebra que nunca comuta por completo (l.40)
- **Kernel, o fluxo.**
  - `ModularFlow.lean:39 · 62cfa753d4b40a90`: σₜ(a) = ρ^{it}aρ^{−it}. Na face finita é automorfismo **interno**.
  - `cocycle_temporal` (`Cocycle.lean:91`).
  - `KMSAt` (`ContratoQG_v31.lean:158`, definição de tipo).
  - `unruh_is_kms` / `unruh_is_kms_temperature` (`ContratoQG_v31_Teoremas.lean:409/426`).
  - `gibbs_kms` (`FiniteTomita.lean:179`), `light_kms` e `lightDelta` (`TheImportedSecondQuantization.lean:440/410`).
  - `modularConjugation_preserves_state` (`ModularPower.lean:54`).
  - `PolarPeriod016.reciprocal_temperature` (1/P = κ/2π), `Wick016.wick_boost_two_pi`, `PolarPeriod016.boost_defect_with_derived_period` (a temperatura entra em Clausius) e `periodic_borchers_trivial`. [REAL]
- **Kernel, «nunca comuta por completo».**
  - `sigma_fixed_of_commute` (G0), `sigma_fixed_iff_diag` (G1d: setor fixo = centralizador) e `gibbs_tracial_on_centralizer` (G2), em `Ergodicity.lean:51/134/172 · 79bc3b939b6e4e59`.
  - `NonKMSProbe.identity_flow_not_kms` (`O16/ProbeNonKMS_v3.lean:50`): estado não tracial ⟹ o fluxo identidade não é KMS.
  - `Thermal025.gibbs_fixed_iff_tracial` e `absoluteOne_flow_trivial` (o Um absoluto não tem fluxo). [REAL]
- **Atlas.** `:2179` «tracial ⟹ o relógio para» [REAL 130_]; `:1702` «o estado gera o próprio relógio». [REAL]
- **Literatura.** Tomita–Takesaki (Takesaki 1970); KMS (Haag–Hugenholtz–Winnink 1967); Connes 1973; Connes–Rovelli 1994. [KNOWN]
- **Leitura.** REAFIRMAÇÃO. A matemática já está no kernel; novo é só o modo de dizer.

### O7 — o intervalo entre causa e efeito que impede o cosmos de virar uma fotografia estática e morta (l.40)
- **Kernel.**
  - `beta_forbids_full_static_witness` (`NoFullWitness.lean:91`).
  - `static_witness_iff_no_boundary` (`BoundaryException.lean:55`): a testemunha estática existe ⟺ β·g = 0.
  - `existence_forbids_full_static_witness` (`TheElementaryReason.lean:135`) e `verb_not_identity` (`NoFullWitness.lean:103`). [REAL]
- **Selo e core.** `full_static_witness_exists = False`, com a leitura v370 «IMPOSSIBLE_BY_THEOREM_IN_FINITE_TIME_IN_THE_STATIC_MODE__DYNAMICALLY_STATIONED_NOT_STATIC» (`um.py:212293`). [REAL]
- **Leitura.** REAFIRMAÇÃO. Só a frase «intervalo sagrado» é nova. [ONTO]

### O8 — Liouville: o volume no espaço de fases é conservado; tudo gira sem pousar e nada se grava (l.44)
- **Kernel, análogos já provados.**
  - `IALDJones.angular_orbit_no_limit` (`IALDJones.lean:331 · 3070346c3571f340`): sem taxa, a órbita NÃO converge ao centro. É «o limite não nasce no regime angular».
  - `angular_orbit_periodic` (`:340`, período 2π/ω).
  - `flow_unitary_diag` (`TheHorizonRate.lean:78`, «o horizonte gira, não dissipa»).
  - `Smat_conjTranspose_mul` (`SMatrix.lean:100`, «nenhum peso se perde na fronteira»).
  - `modularConjugation_preserves_state`. [REAL]
- **Homônimo a não citar.** `measurePreserving_pAct` (`RegularRep.lean:83`) é a medida de Lebesgue de ℝ⁴ sob Poincaré, não o espaço de fases (R06).
- **O que não está no kernel.** O teorema de Liouville propriamente, a conservação de VOLUME. Consulta: grep `Liouville` = 0 no kernel, no um.py, no Atlas e no inventário; 0 rotas.
- **Literatura.** Liouville 1838; Gibbs 1902; Arnold §16; Poincaré 1890; Bennett 1973/1982. [KNOWN]
- **Leitura.** MISTO. O giro sem pouso é reafirmação (v371). A conservação de volume como teorema é nova. No modelo ótico existente, |det S| = 1 e os valores singulares de S valem 1; det T = 1 − 2β. São identidades algébricas da família F1.ATRATOR, calculadas aqui com β do runtime: det T = 0,975937399198394, a = −ln(1 − 2β)/2 = 0,0121784. Não são teste nem evidência (`IDENTIDADES_OTICAS.json`). [DERIVED]

### O9 — a dissipação contrai o volume e desenha a bacia de atração: ponto fixo ou ciclo limite (l.46)
- **Kernel, a espiral e o dephasing.**
  - `IALDJones.orbit_tendsto_center` (`:323`): com taxa positiva toda órbita converge ao centro, para qualquer giro.
  - `norm_orbit_sub_center` (`:317`, a distância cai como e^{−rs}).
  - `dephase_tendsto_expectation` (G3e, `Ergodicity.lean:234`), `ergodic_convergence_modular` (G3f, `:285`) e `dephase_fixes_diagonal` (G3c, `:207`: toda a diagonal é fixa, sem unicidade).
- **Kernel, o atrator.**
  - `axiomFlow_tendsto_the_post` (`TheAxiomAndTheFalseWitness.lean:144`).
  - `the_great_attractor` e `um_is_the_great_attractor` (`TheGreatAttractor.lean:115/133`, v156).
  - `lyapunov_decreases` (`DecisionCommutation.lean:223`, Spohn finito) e `leakage_strictly_loses` (`NoFullWitness.lean:66`). [REAL]
- **Fundação.** A lei τ∘θ_s = e^{−s}τ entra como DADO (`Fundacao.lean:21`). [KNOWN, Takesaki 1973]
- **F1.ATRATOR.** Túnel `ORDEM_019\F1.ATRATOR`, `RELATORIO_F1_ATRATOR_R1.md:7` e `:35`: A1–A4 PASSAM, A4 só sob contração estrita, com λ = 1 − 2β. São candidatas em sandbox (R24).
- **Literatura.** Milnor 1985; Lindblad 1976; GKS 1976; Spohn 1978; Frigerio 1978; Ruskai 1994; Nicolis–Prigogine 1977. [KNOWN]
- **Leitura.** MISTO. A convergência ao atrator é reafirmação. Novos: a contração de VOLUME como teorema e o «ciclo limite», que não está tipado (R08).

### O10 — o atrator é o chão firme que torna possível o espaço inscritível (l.46)
- **Kernel.**
  - `Fundacao.the_floor_fixes_the_cut` (`:127`), `agape` (`:135`), `the_fall_never_lands` (`:98`) e `abismo` (`:106`) (`66332d58fd216317`).
  - `the_observer_is_unique` e `judgment_of_correspondence` (`TheGreatAttractor.lean:93/80`). [REAL]
- **Atlas.** `:924` «Atrator de permanência ρ*… o piso de Hilbert… Existir é distinguir-se dele». [REAL, estrutura]
- **Memória.**
  - 10/10: «a singularidade é a leitura do atrator como única verdade universal» (`singularidade-e-a-leitura-do-atrator-10out.md:11`). [INPUT/ONTO]
  - POSTO = RANK: A4 é «a leitura R tem posto 1» (`posto-e-rank-10out.md:13`). [DECLARADO]
- **Leitura.** REAFIRMAÇÃO com leitura nova. «Chão» identifica dois objetos diferentes do kernel, o ponto fixo do semigrupo e o piso da escala dual (R15).

### O11 — «puro amor»: a física da doação; para haver um «onde» e um «quem», algo paga o preço termodinâmico da perda (l.48)
- **Kernel.**
  - `the_separation_is_not_free` (`TheExoneratedDemon.lean:71`).
  - `landauer_floor_pos` e `landauer_floor_vanishes_only_at_absolute_zero` (`TheCostIsDerived.lean:63/69`).
  - `the_two_floors_are_not_the_same` (`TheGeometricCostOfAbsoluteZero.lean:85`).
  - `dephase_preserves_trace` (`TheTraceIsNotErasable.lean:96`): «o que o sacrifício apaga são coerências — o registro fica». [REAL]
- **Fundação.** «A cláusula se chamará “ágape”» (`Fundacao.lean:13`). É o nome dado pelo operador em 07/10. [INPUT]
- **Verbo.** 05/10: «é justamente a razão da inscrição que cria o custo como condição inexorável da existência» (`TheVerbSelectsTheAction.lean:34`). [INPUT/ONTO]
- **Runtime e Atlas.** `fractal_dephasing_principle` (`um.py:6488`, «Existir = o vazamento β») [CONJECTURE ontológica; âncoras REAL]. Atlas `:1518`: «Haja Luz = o primeiro excesso que já não pode retornar integralmente ao atrator».
- **Literatura.** Landauer 1961; Bennett 1982; Bérut et al. 2012. [KNOWN]
- **Leitura.** NOVO [ONTO] sobre âncoras [REAL]. A ligação «puro amor» ↔ «ágape» é leitura que só o operador ratifica.

### O12 — o tempo é a assinatura indelével dessa generosidade (l.50)
- **Kernel, âncoras.** `absolute_zero_unreachable_in_finite_time` (`ForbiddenBoundary.lean:150`), `erasure_not_reached_in_finite_time` (`TheElementaryReason.lean:141`), `finite_time_imperfection` (`TheQuittanceLaw.lean:51`) e `the_dissipation_law_with_contrast_and_the_physical_arrow` (`TheFlowLawContrast.lean:188`). [REAL]
- **Leitura.** NOVO [ONTO], sem termo.

### O13 — o tempo como ato contínuo da criação que dá ao ser espaço para errar, aprender e encontrar redenção (l.42)
- **Leitura.** NOVO, face teológica [ONTO]. Pela regra dos quatro nomes (`four_names_reading_v371`, `um.py:212296`), nenhum estatuto atravessa domínios.

---

## 2. Teoremas de kernel que tocam o tema

Os 78 termos estão listados em `DEFINICOES.json → teoremas_existentes`, com arquivo, linha, sha16, enunciado e verificação. 68 foram medidos no trio nesta sessão. 9 constam só do `#print axioms` do `TGL\Audit.lean` do rito v391. 1 compila no build sem `#print` em livro (`Smat_conjTranspose_mul`; o vizinho `Smat_mem_unitary`, `SMatrix.lean:108`, consta no Audit.lean). Os principais:

| Tema | Termo (módulo:linha) | Enunciado em uma linha |
|---|---|---|
| o tempo lido duas vezes | `TheVerbSelectsTheAction.time_read_twice_confirms_the_post` (:631) | fixo por e^{−tH_min} ∀t ⟺ fixo por Δ^{it} ∀t |
| o posto é o zero modular | `TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero` (:210) | o mesmo conjunto fixo nas duas leituras |
| a leitura pousa no posto | `axiomFlow_tendsto_the_post` (:144); `axiomFlow_eq_exp` (:161) | F(t) = P + e^{−t}(1 − P) → P; F(t) = exp(−t(1 − P)) |
| fractalização temporal | `temporal_fractalization` (TheGreatAttractor:49) | diagFlow(t₁+t₂) = diagFlow(t₁)∘diagFlow(t₂) |
| o Grande Atrator | `the_great_attractor` (:115); `um_is_the_great_attractor` (:133); `the_observer_is_unique` (:93); `judgment_of_correspondence` (:80) | converge à leitura do observador único; o juízo não depende do instante |
| giro sem pouso | `IALDJones.angular_orbit_no_limit` (:331); `angular_orbit_periodic` (:340) | taxa 0: não converge; período 2π/ω |
| espiral que pousa | `IALDJones.orbit_tendsto_center` (:323); `norm_orbit_sub_center` (:317) | taxa > 0: converge ao centro; distância e^{−rs} |
| unitário não dissipa | `flow_unitary_diag` (TheHorizonRate:78); `Smat_conjTranspose_mul` (SMatrix:100) | fases de módulo 1; S unitária |
| dephasing (G3) | `dephase_add`, `dephase_fixes_diagonal`, `dephase_tendsto_expectation`, `ergodic_convergence_modular` (Ergodicity) | semigrupo; diagonal fixa; T_t → E_D |
| o registro fica | `dephase_preserves_trace` (TheTraceIsNotErasable:96) | tr(T_t x) = tr x |
| a entrega tem direção | `lyapunov_decreases` (DecisionCommutation:223) | o funcional de contraste desce |
| fluxo modular finito | `sigma` (ModularFlow:39); `cocycle_temporal` (Cocycle:91) | σₜ = Ad ρ^{it} (interno); u_{s+t} = u_s σ_s(u_t) |
| não comutar ⟹ tempo | `identity_flow_not_kms` (O16/ProbeNonKMS_v3:50); `sigma_fixed_iff_diag` (Ergodicity:134); `gibbs_tracial_on_centralizer` (:172); `gibbs_fixed_iff_tracial` (GibbsAffinity:88); `absoluteOne_flow_trivial` (AbsoluteOne:121) | não tracial ⟹ identidade não é KMS; setor fixo = centralizador; tracial no centralizador; o Um não tem fluxo |
| KMS, Unruh, período | `unruh_is_kms`, `unruh_is_kms_temperature` (ContratoQG_v31_Teoremas:409/426); `gibbs_kms` (FiniteTomita:179); `light_kms` (:440); `faithful_period_iff`, `reciprocal_temperature` (O16/PolarMinimalPeriod_v2:89/104); `wick_boost_two_pi` (O16/WickBoostRotation_v2:49); `boost_defect_with_derived_period` (O16/PeriodHeatCalibration_v3:12) | KMS a 2π/κ; κP = ±2π ⟺ leitura fiel; 1/P = κ/2π; o boost em ângulo fecha em 2π; a temperatura entra em Clausius |
| Borchers | `contract_borchers_form` (:338); `positiveEnergy_orientation` (:345); `periodic_borchers_trivial` (PeriodicBorchersObstruction:37) | Δ^{it} dilata as translações por e^{−2πt}; com fluxo periódico, as translações são triviais |
| Pauli, face finita | `no_finite_weyl_pair` (LocalBreuerGap:159) | PQ − QP ≠ −i·1 em n×n |
| sem fotografia estática | `beta_forbids_full_static_witness` (NoFullWitness:91); `static_witness_iff_no_boundary` (BoundaryException:55); `verb_not_identity` (NoFullWitness:103) | β > 0 proíbe a testemunha estática; ⟺ β·g = 0 |
| terceira lei, tempo finito | `absolute_zero_unreachable_in_finite_time` (ForbiddenBoundary:150); `erasure_not_reached_in_finite_time` (TheElementaryReason:141); `finite_time_imperfection` (TheQuittanceLaw:51) | nenhum zero em tempo finito |
| Landauer | `the_separation_is_not_free` (TheExoneratedDemon:71); `landauer_floor_pos`, `landauer_floor_vanishes_only_at_absolute_zero` (TheCostIsDerived:63/69); `the_two_floors_are_not_the_same` (TheGeometricCostOfAbsoluteZero:85) | kT ln 2 > 0; só se anula em T = 0; o piso geométrico não decorre do térmico |
| relógios | `no_normalized_instantaneous_state_clock` (StateClockObstruction:83); `state_clock_not_instantaneous`, `state_clock_not_modular_reparametrization`, `state_clock_dichotomy` (StateClockDichotomy); `reading_needs_two_clocks`; `two_clocks_are_needed`; `the_screen_keeps_modular_time` | nenhum relógio só do estado instantâneo; ler exige dois instantes |
| a sombra | `PhysicsIsTheReading.the_shadow_is_the_reader_weighted_by_the_reading` (:70) | P_Ω x P_Ω = ω(x)·P_Ω |
| a Fundação | `Fundacao.agape` (:135), `the_fall_never_lands` (:98), `abismo` (:106), `the_floor_fixes_the_cut` (:127), `agape_is_inhabited` (:154), `the_post_lives_in_the_passage` (:166) | a cláusula Ágape (9 de 9 no trio) |

---

## 3. Mapa de rotas e inventário: o que já foi examinado

**Rotas consultadas.** 24 padrões, só de leitura (`rotas_consultas\`).

- **Nenhuma rota examinou:** Pauli · Liouville · Kadosh/santo/sagrado · tempo térmico, Rovelli e tempo modular · Landauer, doação, generosidade, puro amor · F1.TEMPO, tempo santo. A consulta «operador de tempo / limitado inferiormente» trouxe só um homônimo: `umpy.v388.selo_beta_corre_e_fase9_aberta`, onde «limitado inferiormente» é β, não H.
- **Rotas examinadas que tocam a trilha:**
  - `formal.singularidade_le_atrator` (EXAMINADA, REAL). F1.ATRATOR: A1–A3 PASSAM, A4 condicional, A5 só no mapeamento declarado, A6 FALHA a minimalidade. *Não refazer* a recompilação nem os ensaios A1–A6. Próximo passo: pedra nova com atrator de saltos não comutantes, se se quiser A4 ligado ao GKLS v384.
  - `kernel.v386_tipagem_do_verbo` (REAL). O tempo lido duas vezes é re-export. c³ e τ★ ficaram fora. D_folds = 0,74 NÃO tipado. V_tempo ↔ σ₂ é nomeação.
  - `quantica.inventario_gkls_um_py_kernel` (REAL). O kernel não tem dissipador GKLS; *não pedir ao dephasing puro um atrator único*.
  - `quantica.pilar_v384_rodada_completa` (REAL). Atrator único em 672 de 672 pontos [COMPUTED, não medido; não move o gate].
  - `kernel.inventario.cadeia_beta_v376` (Unruh = KMS ligado).
  - `kernel.lema3.superposicao_e_a_passagem_07out` e `umpy.v390.selo_fundacao_agape` (Fundação selada; *não reabrir*).
  - `kernel.leitura_cria_o_objeto_07out` (PALAVRA, 7 declarações, instalação na v392).
  - `ontologia.um_posto_dimensao_do_nome_07out` (ONTO).
  - `gw.eco_acoplado.kms` (EXAMINADA_COM_DEFEITO: lei de atraso KMS).
  - `relogios.v1` e `dephasing.alcance` (relógios v369, sem poder).
  - `d1.orientacao_do_sinal` (PROPOSTA: qual face fecha Clausius).
  - `umpy.v391.estatuto_da_prova`.

**Inventário da bancada.** sha16 `05c2afa06620ca8f`.
- Pauli/operador de tempo: 0 arquivos.
- Liouville: só homônimos (`orbitSymplectic`, `symplecticPolarizer`, `*_measurePreserving` de cartas de rapidez).
- Kadosh/santo: 0. Ágape: 0. Terceira lei em tempo finito: 0 na bancada (está no kernel).
- Fluxo modular: 20 arquivos (`ModularFlowHilbert`, `ModularPower`, `TheModularFlowIsAHorizon`…).
- O instantâneo: `StateClockDichotomy` e `StateClockObstruction`.
- Tracialidade: `gibbs_fixed_iff_tracial`, `modular_variance_zero_iff_tracial`, `tracial_tower_has_no_effective_witness` e a ENTREGA_016 «A-1.b4: fluxo identidade rejeitado por KMS em estado não tracial».

---

## 4. Novo × reafirmação

**Reafirmação: o cânone já tem.**
1. O tempo como fluxo, o Verbo e não o Nome. O tempo lido duas vezes (v386). O posto como zero modular (v385). O agora é do Nome (26/09).
2. O tempo modular: fluxo de automorfismos, KMS, Unruh, período 2π/κ e temperatura, cociclo de Connes, e a hipótese do tempo térmico citada [KNOWN].
3. «A álgebra que nunca comuta»: o setor fixo do fluxo é o centralizador; estado não tracial ⟹ o fluxo trivial não é KMS; tracial ⟹ o relógio para.
4. Nenhuma fotografia estática: `full_static_witness_exists = False` por teorema.
5. Giro sem pouso × espiral que pousa: IALDJones (v371), o análogo de Liouville × dissipação na face finita.
6. A dissipação entrega ao atrator: o Grande Atrator (v156), G3e/G3f, o posto como limite (v385), Spohn finito, a F1.ATRATOR.
7. O zero nunca em tempo finito, nas faces finitas da terceira lei, e o abismo da Fundação.
8. O custo da distinção: Landauer; o registro fica.
9. A face finita de Pauli: `no_finite_weyl_pair`.
10. A premissa de Pauli (H ≥ 0) é a ENERGIA; o gerador modular de III₁ não tem piso (leitura v390).
11. «O leitor é a sombra» (30/09), na forma P_Ω x P_Ω = ω(x)·P_Ω.

**Novo: o cânone não tem.**
1. O nome «santo»/Kadosh para o tempo [ONTO]. Consultas: 0 em todas as superfícies.
2. A recusa de nomear como matemática: «o tempo não tem posto». Falta o termo, por exemplo F(t)² = F(t) ⟺ t = 0 com P ≠ 1. É candidato.
3. Liouville propriamente: conservação de VOLUME no regime unitário, contra a contração de volume no dissipativo. Nenhum termo de kernel. No modelo ótico, as identidades |det S| = 1 e det T = 1 − 2β ainda não estão escritas.
4. O «ciclo limite», sem tipo no cânone.
5. «Puro amor» como nome da física da doação, e a leitura de que ele é o mesmo «ágape» da cláusula. Cabe ao operador.
6. «O tempo é a assinatura da generosidade» e «o tempo como criação e redenção» [ONTO].
7. A tríade dos relógios (ponteiro, césio, entropia) lida contra os três clocks do runtime.
8. Por citação: o teorema de Pauli em dimensão infinita (forma de Weyl), a exterioridade do fluxo modular em tipo III (Connes) e a etimologia de Kadosh [KNOWN].

---

## 5. Riscos de leitura e de estatuto

O texto integral está em `DEFINICOES.json → riscos`. Em resumo:

- **R01 Homônimo «Pauli».** As ~1.200 ocorrências no kernel são matrizes e interações de Pauli. Para o tempo só vale `no_finite_weyl_pair`.
- **R02 Precisão de Pauli.** É teorema na forma de Weyl/covariante (Stone–von Neumann). Na forma de Heisenberg há contraexemplos (Galapon 2002), e existem POVM de tempo covariantes. «Hermitiano» lê-se «autoadjunto e covariante».
- **R03 O tempo modular escapa de Pauli.** K = −log Δ não tem piso (JKJ = −K; v390). Nunca escrever que Pauli proíbe o fluxo modular.
- **R04 «Não profanável pela posse» × face finita.** O σₜ finito do kernel é INTERNO (Ad ρ^{it}). A exterioridade só vale em tipo III [KNOWN, Connes 1973] e não é termo de kernel.
- **R05 Dois regimes.**
  - Δ^{it} é unitário: a órbita de um vetor não pousa.
  - Na tabela da casa o boost é FACE porque dilata as translações (e^{−2πt}).
  - A leitura euclidiana (período, temperatura) é o ÂNGULO.
  - Pousar é dos semigrupos e da espiral com taxa. Nunca pedir limite ao ângulo.
- **R06 Homônimos de Liouville.** `measurePreserving_pAct`, `symplecticPolarizer` e `orbitSymplectic`. `dephase_preserves_trace` preserva o traço, não o volume.
- **R07 Contração no quântico.** É contração CPTP (Ruskai) ou colapso da bola de Bloch. θ_s da Fundação é um automorfismo reversível que escala o traço, e a sua lei é DADO [KNOWN]. Lê-lo como dissipação é leitura.
- **R08 Ciclo limite.** Não está tipado; a A1 cobre só Cesàro.
- **R09 Unicidade.** O dephasing puro fixa a diagonal inteira; o chão único exige hipótese NOMEADA.
- **R10 Não refazer.** A F1.ATRATOR não citou TheGreatAttractor (v156) nem a espiral de IALDJones (v371), que já provam o análogo de A1–A3 e a unicidade do observador.
- **R11 Relógios de estado.** Clock040/045 têm escopo estreito; lê-los como «o agora intocado» é [ONTO].
- **R12 O agora.** A coerência entre 26/09 e 12/10 depende de identificar o agora com o posto fixo pelo fluxo [ONTO].
- **R13 Domínios.** As palavras teológicas são [ONTO] e nenhum estatuto atravessa domínios. A glosa «Kadosh = separado» é tradicional e debatida.
- **R14 «Nada se grava» é forte demais.** Copiar pode ser reversível (Bennett); o que custa é apagar (Landauer) e manter memória estável.
- **R15 Atrator × chão.** O ponto fixo de semigrupo e o piso da escala dual são objetos distintos.
- **R16 β.** Nenhum literal. det T = 1 − 2β e a ≈ β são identidades, não medida.
- **R17 Palavras.** A palavra recusada pela régua nunca entra como veredito. PASSA é validade na face testada.
- **R18 Tempo térmico.** É hipótese (Connes–Rovelli), não teorema.
- **R19 Dependência do estado.** O fluxo modular depende do estado; só a classe externa é intrínseca.
- **R20 Livro de auditoria.** 13 termos citados não estão no `#print axioms` do Audit.lean (os O16 e oito sem `#print` algum). Medidos no trio aqui; acrescentá-los é fiação, se a v392 os citar.
- **R21 Tensão aparente.** Em 05/10 o operador DEFINIU o tempo; em 12/10 diz não conseguir NOMEÁ-LO. Conciliação candidata: descrever ≠ nomear. Decide o operador.
- **R22 T1 já existe.** O T1 da memória da c1 é `no_finite_weyl_pair`: reaproveitar.
- **R23 Cabeçalho velho.** O de `IALDRhoStar.lean` diz «não transposta», mas o módulo está importado e auditado.
- **R24 F1.ATRATOR no túnel.** É candidata de sandbox até a v392.
- **R25 Sigla.** O T de «TGL» (10/10) é o gradiente, não o tempo.
- **R26 Encadeamento.** «O fixo é o verbo… o verbo é betatgl» (08/10): não encadear «tempo = β».

---

## 6. Para a construção: sugestões do levantador, que a gerência decide [INPUT]

Nenhuma destas é pré-registro. A gerência congela o que quiser, por hash, antes de construir.

- **T1, Pauli na face finita.** Reaproveitar `no_finite_weyl_pair`, no máximo com um re-export de nome novo. A forma de Weyl entra por citação [KNOWN].
- **T2, o tempo não tem posto.** Termo novo pequeno: F(t)² = F(t) ⟺ t = 0, quando P ≠ 1. Junto, `verb_not_identity`.
- **T3, Liouville × dissipação.**
  - No kernel: reaproveitar `angular_orbit_no_limit` / `orbit_tendsto_center`. Termo novo possível: o determinante do diagFlow vale exp(−tβΣd), ou seja, contrai volume com d ≥ 0 não nulo, e vale 1 no caso unitário.
  - No modelo ótico: |det S| = 1 contra det T = 1 − 2β < 1, com o volume λⁿ → 0.
- **T4, o agora intocado.** Reaproveitar `the_post_is_the_modular_zero` / `time_read_twice_confirms_the_post`.
- **T5, a álgebra que não comuta.** Reaproveitar `identity_flow_not_kms`, `sigma_fixed_iff_diag` e `gibbs_tracial_on_centralizer`.
- **T6, o atrator como chão.** Reaproveitar `the_great_attractor` com a Fundação. A unicidade só sob hipótese nomeada.
- **Só por citação:** Pauli (dimensão infinita), Liouville, Connes–Rovelli, a exterioridade de Connes, Landauer e o léxico de Kadosh. «Santo», «puro amor» e «generosidade» ficam ditos como [ONTO].

---

## 7. O que esta pasta contém

- `LEVANTAMENTO.md` (este arquivo) e `DEFINICOES.json`: 13 objetos, 121 âncoras, 78 teoremas, 26 riscos e as medidas com sha256. `DEFINICOES_COMPACTO.json` é a forma curta, com o sha256 do completo.
- `BETA_RUNTIME.json`, `FINGERPRINT_ANTES.json`, `FINGERPRINT_DEPOIS_LEAN.json`, `FINGERPRINT_FINAL.json`, `LEAN_AXIOMAS.json`, `IDENTIDADES_OTICAS.json`, `auditoria_nomes.json`, `inventario_consultas.json`, `kernel_decls.jsonl`, `kernel_temas.json`.
- `rotas_consultas\`: 24 respostas e o `RESUMO.json`.
- `sandbox\`: `CheckTempoLevantamento.lean`, `saida_check_tempo.txt` e `RECIBO_LEAN_CHECK.json`. O toolchain copiado foi apagado.
- `scripts\`: todos os scripts usados, só de leitura sobre as fontes.

Os sha256 dos arquivos de evidência estão em `DEFINICOES.json → medidas.arquivos`. Nada foi escrito no quadro, no mapa, na memória, no túnel, no Nós, no kernel, na Bancada, no site ou no git. O gate não se move.
