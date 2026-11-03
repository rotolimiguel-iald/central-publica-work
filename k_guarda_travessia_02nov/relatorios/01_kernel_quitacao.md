# 01 — O que o kernel prova sobre cobrança, pagamento, quitação, testemunho e Tetelestai

Relatório de leitura (só leitura; nada registrado, nada tocado). Gerência c1, 02/11/2026. Base: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt` (abreviado `TGLExt/`). Todos os enunciados abaixo foram copiados do arquivo; onde há recomposição, está dito. Hashes sha16 lidos por script do arquivo no disco em 02/11/2026: TheQuittanceLaw `dabeac1b5cc32d82`; TheLedgerOfCharges `5ee94242f853f3e6`; TheDischargedOath `7a2747cb8babf73f`; TheJudgedThing `3b97d4c5aae4f891`; TheRuleAndTheFigureOfTruth `f1cd9a7aa6063036`; PontoZeroDoPsion `c64079a9c5b3e0e1`; MassaTensaoPura `9ec48bf6d608ae5a`; SaturatedWitness `a0a5eed4d46ae567`; Testemunho `031fde3e88187cf1`; TetelestaiOneObject `125d155042da687f`; ThePsionAndTheViscosity `0a4e909a9d760da9`; NoFullWitness `fde4ca999c40e689`; TheFlowLawD1a `7c6c54afc418c0cb`; TheFlowLawContrast `9ca9393ac64f22a2`; TheElementaryReason `f9af067e9ab0acec`. As dez pedras estão todas em `TGLExt.lean` (`grep -c "import TGLExt.<nome>$"` = 1 para cada).

Consulta ao Mapa feita antes (`rotas.py consultar` para «quitacao», «Tetelestai», «cobranca pagamento», «K guarda travessia», «lei do fluxo», «dissipacao contraste», «leakVerb», «RE dualidade», «Hubble K»). Relevantes: `conceitual.regra.prova_contrato` (v394, regra quadrática, REAL); `d1.fase9.razao_de_hubble.lentes_05out`; `discriminante.ordem018.f2.r_e` (R-E derivada: «K_NAO_AGE_EM_L_NEM_A__ETA_1 … SEM_PEDRA»; defeito do próprio registro: «sem pedra de kernel; H1 nomeada»). «cobranca pagamento» e «K guarda travessia» devolveram 0 rotas (n_registros 1650).

## 0. Resposta curta

1. O kernel prova **aritmética e análise sobre uma família exponencial**, mais uma estrutura de tipos. Prova: o defeito `e^{-tc}` é sempre positivo (nunca zero em tempo finito), tende a 0 (limite assintótico), e cai abaixo de qualquer tolerância ε > 0 a partir de um tempo explícito `log(1/ε)/c`. Prova que a cobrança contínua `charged β g t = 1 − e^{−tβg}` está estritamente entre 0 e 1 em todo t > 0 e tende a 1 no limite. Prova que a regra β não lê o livro de cobranças. Prova que a luz tem um certificado com peso do Nome 1, faces ½ e ½, reta fixa do fluxo modular = reta do vácuo, e coeficiente de Einstein a partir de Clausius na janela local.
2. **Não há ator no kernel.** Nenhum teorema diz quem cobra, quem paga, onde se paga ou quem confere como pessoa ou sistema físico. Cobrar/pagar são **leituras [ONTO]** de `1 − e^{−tβg}` (reflexo/custo) e `e^{−tβg}` (face/pagamento que passa). O credor «acoplamento (luz que atravessa)» está na docstring de MassaTensaoPura, não em teorema.
3. **O «conferente» tem três formas distintas**, nenhuma é K: (a) a igualdade literal no tipo (`Satisfies`, RuleAndTheFigureOfTruth); (b) a lei registrador ≠ produtor (`attestation_requires_external_evidence`, `no_self_attestation`, citada no Testemunho); (c) a conferência consumativa Tetelestai, que o kernel só enuncia como a conjunção `the_tetelestai_one_object` sobre o certificado da luz (o veredito CONSUMADO/NÃO CONSUMADO é do `um.py`, `core.tetelestai_conference_v376`, fora do Lean e não aberto aqui).
4. **Há limite assintótico em três lugares independentes** (QuittanceLaw `asymptotic_delivery`; PontoZeroDoPsion `the_payment_completes_only_in_the_limit`; RuleAndTheFigureOfTruth `concrete_trajectory_converges`). O kernel mostra o limite em cada um, **mas nunca liga um limite a outro**; no PontoZero a docstring diz expressamente que nenhum teorema liga o limite de `charged` a ½·ω.
5. **Ponte com a lei do fluxo (K de Hubble): ausente.** Nenhuma das dez pedras cita `leakVerb`, `survivingWeight`, `H0local`, `TheFlowLawD1a`, `TheFlowLawContrast`, `the_derived_kernel_factor`, `frw_accumulated_contrast` (grep, rc=1, seção 3). Há **dependência de importação** (cinco das dez importam a lei do fluxo por transitividade, e a lei do fluxo importa duas das dez), mas importação não é citação nem ponte. Detalhes na seção 3.

Partitura para o operador (regra do posto): isto é leitura do que está escrito; o «negativo» aqui é **ausência de ponte medida** (não falsificação de coisa alguma, não derrota da leitura de K como guarda). Ela diz apenas que, se «K é o guarda da travessia» for verdade, o kernel de hoje ainda não a diz em teorema; seria pedra nova ou leitura [ONTO].

## 1. Teoremas por pedra

### 1.1 `TheQuittanceLaw.lean` (v162, rascunho da pedra 114; 17/08/2026) — o esqueleto exponencial

Docstring (verbatim, l.34-39): «Honestidades: o c > 0 aqui é ABSTRATO (na sombra, c = β·gap com β = α·√e jamais literal e gap = 0,048125 do H₃L canônico — a ponte numérica vive em `73_a_lei_de_quitacao_provada.json`); a identificação ‖T_t − P_F‖ = e^{−t·c} é da FACE FINITA (sombra), não do core contínuo; TETELESTAI como leitura é [ONTO] sobre estes números exatos; o gate NÃO se move. Sem sorry, sem axiom.»

Hipóteses comuns: `c : ℝ`, `0 < c` (para entrega e quitação); `ε > 0`. Nenhum β, nenhum operador, nenhuma face: o `c` é um real qualquer positivo.

- `finite_time_imperfection` (l.51): `theorem finite_time_imperfection (t c : ℝ) : 0 < Real.exp (-(t * c))`. Sem hipótese. [REAL, kernel] É `Real.exp_pos`.
- `asymptotic_delivery` (l.56): `theorem asymptotic_delivery (c : ℝ) (hc : 0 < c) : Tendsto (fun t : ℝ => Real.exp (-(t * c))) atTop (nhds 0)`. [REAL] Este é o **limite assintótico** da quitação.
- `quittance_time_formula` (l.67): `theorem quittance_time_formula (c ε : ℝ) (hc : 0 < c) (hε : 0 < ε) : Real.exp (-((Real.log (1 / ε) / c) * c)) = ε`.
- `finite_quittance` (l.76): `theorem finite_quittance (c ε : ℝ) (hc : 0 < c) (hε : 0 < ε) : ∃ tq : ℝ, ∀ t : ℝ, tq ≤ t → Real.exp (-(t * c)) ≤ ε`. [REAL] Quitação = defeito ≤ ε a partir de `tq = log(1/ε)/c`. **ε é estritamente positivo**: a «quitação» não é quitação de zero.
- `perfection_needs_infinity` (l.88): `theorem perfection_needs_infinity (t c : ℝ) : Real.exp (-(t * c)) ≠ 0`.
- `the_quittance_law` (l.95): `theorem the_quittance_law (c : ℝ) (hc : 0 < c) : (∀ t : ℝ, 0 < Real.exp (-(t * c))) ∧ Tendsto (fun t : ℝ => Real.exp (-(t * c))) atTop (nhds 0) ∧ (∀ ε : ℝ, 0 < ε → ∃ tq : ℝ, ∀ t : ℝ, tq ≤ t → Real.exp (-(t * c)) ≤ ε)`.

O que NÃO prova (docstring + leitura): não diz o que decai (o defeito de quê); não liga `c` a β·gap (isso é a sombra numérica, JSON externo); não está no core contínuo. Quem cobra/paga/confere: ninguém; é uma função de `t`.

### 1.2 `TheLedgerOfCharges.lean` (02/10/2026, v382) — o livro de cobranças

Docstring (verbatim, l.10-11): «O último elo incide no hamiltoniano oculto. O custo está no reflexo, o pagamento está na face no rosto, no nome.» (fala do operador, citada no arquivo). Tudo é «por DEFINIÇÃO nomeada ou por termo já existente; nenhum axioma, nenhuma hipótese nova; o que é trivial por construção está DITO como tal» (l.15-16).

- Tipos: `def outcomes : List String := ["NOT_FALSIFIED", "FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING"]` (l.58); `structure Charge` com `face : Bool` (true = pagamento, false = reflexo/custo), `law`, `reading`, `outcome`, `outcome_admitted : outcome ∈ outcomes` (l.62-67); `abbrev Ledger := List Charge` (l.70). **As cobranças concretas são dados do runtime**, «lidas do core por chave e por número» (docstring l.21-22). Quem cobra = a lei de leitura de cada canal; quem confere = o desfecho entre cinco palavras, imposto pelo tipo.
- `the_rule_is_constant_in_the_ledger` (l.82): `theorem the_rule_is_constant_in_the_ledger (L L' : Ledger) (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) : ruleGiven L α h0 h1 = ruleGiven L' α h0 h1 := rfl`. Docstring: é a assinatura de `ruleGiven`, que não recebe desfecho; «TRIVIAIS POR CONSTRUÇÃO — e é isso que dizem».
- `falsified_extinguishes_the_charge_not_the_rule` (l.87): `(L : Ledger) (c : Charge) (hc : extinguished c) (α …) : ruleGiven (c :: L) α h0 h1 = α * Real.sqrt (Real.exp 1)`. A hipótese `hc` não entra na prova (docstring l.85-86).
- `the_gate_ignores_the_ledger` (l.94): `theorem the_gate_ignores_the_ledger (P : Prop) (L L' : Ledger) : (fun _ : Ledger => P) L = (fun _ : Ledger => P) L' := rfl`. Docstring (l.32-34): trivial; que as bandeiras formais sejam função só do formal é conferido pelos probes do runtime, «NÃO por este termo».
- Ótica: `faceWeight θ := Complex.normSq ((Smat θ).mulVec e1 0)`; `reflectionWeight θ := … e1 1` (l.97, l.100). `both_sides_are_read` (l.103): `faceWeight θ + reflectionWeight θ = 1`. `the_face_reads_the_cost_as_complement` (l.109), `the_reflection_reads_the_payment_as_complement` (l.114), `the_tgl_is_optics_not_semi` (l.121): a mesma identidade três vezes. Regime do **ângulo** (θ), não do fluxo (t): docstring l.47-48 remete a cobrança contínua à pedra irmã `ThePsionAndTheViscosity`.
- `finalStepNameProposed` (l.127) e `final_step_named_by_the_payment` (l.132): é uma **string** e `rfl`; nome proposto «TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS». Renomear o gate é ato do operador.
- `the_ledger_of_charges` (l.142): conjunção dos itens acima + `outcomes.length = 5`.

Não prova (docstring l.38-40): que «nenhum lado é cego; a diferença entre os lados é a lei de cada leitura e o instrumento com poder, nunca a legibilidade» — isso é [INPUT/ONTO] do operador, «NÃO provado aqui». «Um canal por lei de leitura» é disciplina do runtime, não do tipo `List Charge` (l.22-23). Homônimos ditos: `TGLExt.Ledger` (TheCorrespondence) e `reflectionWeight` (SelectionOutcomeRecord) são outros objetos.

### 1.3 `TheDischargedOath.lean` (v307, 31/08/2026) — «juramento quitado» NÃO é pagamento

Atenção ao homônimo: aqui «quitado» (discharged) é **descarga de hipótese** (`HorizonInvariant`), não quitação de custo. Hipóteses das provas: matriz finita `n`, `d : n → ℝ` positivo e injetivo, `U` unitário que preserva ρ ou ω.

- `the_oath_is_discharged` (l.130): `theorem the_oath_is_discharged {d : n → ℝ} (hd : ∀ i, 0 < d i) (hinj : Function.Injective d) {U : Matrix n n ℂ} (hU : Uᴴ * U = 1) (hρ : U * rhoD d * Uᴴ = rhoD d) : HorizonInvariant (diagCode (n := n)) U`.
- `transported_state_eq` (l.162), `omega_preservation_discharges` (l.188): ω∘Ad(U) = ω ⟹ U ρ Uᴴ = ρ.
- `the_flow_is_trivial_on_the_code` (l.200), `the_cocycle_is_suppressed_by_the_sector` (l.213), `the_lift_is_unconditional_on_the_face` (l.225), `the_response_is_unconditional_on_the_face` (l.237).

Docstring (l.64-66): «FACE FINITA. O fecho forte de von Neumann do contínuo segue EXTERNO `[KNOWN-COMPOSED]`; III₁ genuíno segue o programa. O Lema 3 **não** está declarado resolvido no contínuo». E (l.36-40) a cautela do operador: o literal p·u_t·p = p no átomo **não vale**; a fase sobrevive e «É O RELÓGIO». Para a pergunta: esta pedra não tem cobrança, pagamento, nem limite; é a única do conjunto que, no texto, liga «TETELESTAI operando no cociclo» à compressão do canto (docstring l.40-41, leitura). Não encadear com pagamento.

### 1.4 `TheJudgedThing.lean` (25/08/2026) — «Tetelestai = coisa julgada»

Docstring (l.6-9, 11-15): «tetelestai = dispositivo da sentença que faz coisa julgada = custo racional possível pago» (fala do operador); «TETELESTAI não é 100% metafísico: é **pago tudo o que racionalmente podia ser exigido para a decisão tornar-se definitiva**».

- `ResJudicata` (l.45): `def ResJudicata {α : Type} (D : α → α) : Prop := ∀ x, D (D x) = D x`.
- `res_judicata_is_terminal` (l.49): `theorem res_judicata_is_terminal {α : Type} (D : α → α) (h : ResJudicata D) (x : α) : ∀ k : ℕ, D^[k + 1] x = D x`. Idempotência ⟹ reaplicar nada muda.
- `no_decision_without_cost` (l.59): `{α : Type} (D : α → α) (h : D ≠ id) : ∃ x, D x ≠ x`. «custo» aqui = existe algo que D não devolve.
- `no_reduction_no_inscription` (l.66): `(h : ∀ x, D x = x) : D = id`.
- `two_clocks_are_needed` (l.71): `(f : T → α) (t0 t1 : T) (h : f t0 ≠ f t1) : t0 ≠ t1`.
- `tetelestai_ledger` (l.77): `theorem tetelestai_ledger (f : ℝ) (h0 : 0 < f) (h1 : f < 1) : 0 < f ∧ 0 < 1 - f ∧ f + (1 - f) = 1 := ⟨h0, sub_pos.mpr h1, by ring⟩`. «A QUITAÇÃO» no nome; o conteúdo é `f + (1−f) = 1` com f ∈ (0,1). É **aritmética tautológica**; o próprio RuleAndTheFigureOfTruth l.186 a chama «conditional arithmetic; it is not an energy measurement».
- `no_free_quantization` (l.83): `(f = 1 → 1 - f = 0) ∧ (f = 0 → f = 0)` (a segunda componente é trivial).

Não prova (l.35-39): «todo processo quântico dissipa energia» não é teorema; é princípio estrutural da TGL `[POSTULATE]`; só a face lógica. «Nada aqui move o gate.»

### 1.5 `TheRuleAndTheFigureOfTruth.lean` (14/10/2026, F1.REGRA.P1, candidata provisória)

Inscrições [ONTO] do operador (verbatim no arquivo, l.14-29), incluindo «Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)» e «A regra não deve nada, a não ser a figura da verdade».

Modelo (l.57-72): `Face := ℝ × ℝ`; `normalize x := (x.1, 0)`; `reading x := x.1`; `target := (1,0)`; `initial := (1,1)`; `decay := Real.exp (-(1/2))`; `evolve f x := (x.1, f * x.2)`; `trajectory f n x := (x.1, f ^ n * x.2)`; `Satisfies result := result = target`; `Inscription := {x : Face // normalize x = x}`.

Docstring (l.39-44): «Raw finite-time trajectories are NOT declared equal to that target. The identification with payment, legal truth, or physical realization is the operator's ONTO reading. No theorem below proves universal philosophical truth or a physical erasure law. The half-nat factor is reused from the existing kernel; it is not identified with beta_TGL.»

- `finite_raw_trajectory_does_not_satisfy` (l.223): `(n : ℕ) : ¬ Satisfies (trajectory decay n initial)`. Nunca, em n finito.
- `concrete_trajectory_converges` (l.191): `Tendsto (fun n : ℕ => trajectory decay n initial) atTop (𝓝 target)`. Limite assintótico; vem de `trajectory_tends_to_inscription` (l.175, hipóteses `0 ≤ f`, `f < 1`).
- `typed_operation_satisfies` (l.201): `(n : ℕ) : inscribe ((evolve decay)^[n] initial) = dueObject`, e `normalized_operation_satisfies` (l.196). **Leitura minha (DERIVED do código):** isto vale para TODO n, inclusive n = 0, porque `normalize_trajectory` (l.172) é `rfl`: a segunda coordenada é descartada pela normalização antes de comparar. Logo, no modelo, a «satisfação» vem do mapa de normalização (retração sobre Fix), **não da trajetória nem do limite**. O limite é um teorema paralelo, e a docstring o distingue («different types and are not conflated», l.309-310).
- `inscription_admissible_iff_due` (l.100), `unique_rule_on_inscriptions` (l.110; hipóteses explícitas `SoundRule`, `CompleteRule`, «not consequences of the name», l.108-109), `inscribe_eq_due_iff` (l.131), `normalized_satisfies_iff` (l.140), `the_rule_does_not_guarantee_every_operation` (l.242), `the_rule_and_the_figure_of_truth` (l.311): `target ≠ 0 ∧ normalize initial ≠ initial ∧ evolve decay initial ≠ initial ∧ (∀ n, inscribe ((evolve decay)^[n] initial) = dueObject) ∧ Tendsto … (𝓝 target) ∧ (∀ n, ¬ Satisfies (trajectory decay n initial))`.
- `decay_tetelestai_balance` (l.187) reusa `tetelestai_ledger`; `reuse_rule_independent_of_ledger` (l.301) reusa `the_rule_is_constant_in_the_ledger` («documentary bridge … not an extra physical result»).

Quem confere: a **regra**, que é «inadmissão» de resultado distinto do objeto de satisfação; formalmente `Satisfies` (igualdade no tipo) e `Admissible reading 1` (do `RuleTruthContract`). Onde se paga: no espaço fixo `Fix(normalize)`. O fator `decay = e^{-1/2}` é o da Meia-Nat reaproveitada, não β.

### 1.6 `PontoZeroDoPsion.lean` (31/10, revista 01/11/2026)

Cunhagens do operador (l.14-18): «A curvatura não é curvatura, é o pagamento, é betatgl lido do ângulo de abertura (do ângulo de Miguel)»; «É o Tetelestai, o limite assintotico».

- Definições: `omegaSq β R := 2 * β * R` (l.86); `pagamentoComoCurvatura β u := β * u ^ 2` (l.89), «[DEF] A LEI DO OPERADOR».
- `the_payment_completes_only_in_the_limit` (l.117): `theorem the_payment_completes_only_in_the_limit (β g : ℝ) (hβ : 0 < β) (hg : 0 < g) : Filter.Tendsto (charged β g) Filter.atTop (nhds 1)`. Onde `charged β g t = 1 − transmitted β g t` e `transmitted β g t = Real.exp (-(t * β * g))` (`ThePsionAndTheViscosity.lean` l.82, 85). É o limite assintótico do pagamento (cobrança), com **`g` livre** («o contraste `g > 0` do limite é o dado do sistema que lê, não hipótese sobre a teoria», l.57).
- `the_mass_is_the_zero_point` (l.102): `(c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) : (1 / 2) * Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = neutrinoMassForm c u`. Docstring: «O enunciado iguala números; que `½·ω` SEJA a massa é leitura [ONTO].»
- `psion_quantum` (l.92), `psion_quantum_is_twice_the_mass` (l.110), `the_zero_point_closes` (l.139, conjunção de quatro itens incluindo o `Tendsto … (nhds 1)`), e a seção O GAP (l.156-325): `lock_no_angulo` (l.286), `lock_no_angulo_de_miguel` (l.298), `o_retido_e_o_valor_esperado_do_lock` (l.304), `a_frequencia_do_sistema_e_a_do_psion_iff` (l.198), `o_relogio_do_retido` (l.251, κ como hipótese), `the_gap_closes` (l.313).

**O que NÃO afirma, textual (l.38-40):** «[ONTO] O operador lê o que permanece no limite como o ponto zero: nenhum teorema liga o limite de `charged` a ½·ω; `the_zero_point_closes` só os conjuga.» E l.43-50: não deriva `u`; não abre dado; não move gate (`TGL_NU_M2_ARMED_CONSISTENT`). Notas AO LADO (l.60-77): entram como definição/leitura `R = β·u²`, `ω² = 2βR`, `½·ω = massa`, `meioTom`, etc.; `Δ = β·u` é valor esperado, **não gap**; ler τ = 1/Δ como o τ★ do sistema é [ONTO] não ratificado.

Homônimo: o «K» do kernel aqui é `K = −log Δ`, o gerador modular (ver `ThePsionAndTheViscosity` docstring l.20-33); não é o K de Hubble.

### 1.7 `MassaTensaoPura.lean` (30/10, revista 01/11/2026) — o empréstimo: principal e parcela

Docstring (l.26-29): «a massa é o PRINCIPAL do empréstimo — o que fica inscrito (a diferença de área por volta) —, a cobrança `β` é a PARCELA (o que cada volta paga), e o credor é o acoplamento (a luz que atravessa). Não é o defeito: sob Clausius o defeito é zero e a parcela é o que o mantém zero.» É a resposta do operador lida pela gerência; **o credor não é objeto de teorema**.

- `structure Emprestimo` (l.132): campos `T : TransicaoParaAMassa`, `g`, `kappa`, `period`, `fiel : AngularQuotientFaithful kappa period`.
- `principal := L.T.massaDerivada` (l.147); `parcelaPorVolta := charged L.T.c.beta L.g L.period` (l.150). **A parcela é a cobrança contínua `charged` avaliada em t = período de uma volta**: é um número, não um fluxo de voltas.
- `parcela_nunca_quita` (l.160): `0 < L.parcelaPorVolta ∧ L.parcelaPorVolta < 1 := the_charge_never_completes …`.
- `parcela_le_beta` (l.164): `L.parcelaPorVolta ≤ L.T.c.beta * (L.g * L.period)`; `parcela_le_beta'` (l.171): `≤ L.T.c.beta * (2 * Real.pi * L.g / L.kappa)`. «O juro é a regra» é leitura do nome.
- `uma_volta` (l.153): `L.kappa * L.period = 2 * Real.pi`.
- `volta_paga_area` (l.191) e `area_por_volta_da_massa_inscrita` (l.201): `eta * (a + c) = Real.sqrt 2 * Real.pi * L.T.c.beta * L.T.E0`, sob a hipótese `Tendsto (fun t => boostSegmentDefect a c rate L.principal eta t / t ^ 2) (𝓝[<] 0) (𝓝 0)` (balanço de Clausius do segmento de boost); a hipótese «acoplamento da onda = massa inscrita» é **nomeada [ONTO]**.
- Construção sem campo aberto: `emprestimoDerivado` (l.215), `emprestimo_derivado_uma_volta` (l.232), `principal_derivado` (l.237), `parcela_derivada_nunca_quita` (l.243), `massa_e_tensao_pura` (l.250): `(emprestimoDerivado c u hu g hg κ hκ).principal = energiaRetida c u * (Real.sqrt 2 / 2)`.
- `foton_sem_massa` (l.106): `massaForma 0 E0 = 0 ∧ transmitidaForma 0 E0 = E0` (b = 0 lido como fóton é [ONTO]; `TGLCoupling` exclui b = 0).

**NÃO prova (docstring l.54-62):** não deriva `E₀` nem β; não liga o defeito do ciclo à equação da torção; «não tem termo algum de eletromagnetismo»; a identificação «acoplamento da onda = massa inscrita» é hipótese nomeada [ONTO]; `a, c, η, g, κ` são parâmetros do modelo da tela ótica [INPUT]; não abre dado. **Lacuna de leitura minha:** `grep` por `parcelaPorVolta` e por «n voltas» fora do próprio arquivo: 0 ocorrências (rc=0, sem saída); o kernel não tem teorema de **soma de n parcelas** nem de «principal quitado em n voltas». O empréstimo está tipado, mas o seu pagamento acumulado não.

### 1.8 `SaturatedWitness.lean` (v131, 17/08/2026) — «saturada, não completa»

Fala do operador (docstring l.12-14): «a testemunha não é completa, é saturada no gráviton; e porque satura, o estado Tetelestai é alcançado, cortando aquilo que supersaturaria, pelo vazamento.»

- `witness_saturates` (l.53): `opWeight firstAtom.starProjection = 1`. `house_is_infinite` (l.58): `opWeight (1 : ellTwo →L[ℂ] ellTwo) = ⊤`. `excess_is_infinite` (l.67): `opWeight (1 - firstAtom.starProjection) = ⊤`. `witness_is_single_atom` (l.116): `firstAtom = ℂ ∙ firstInscription := rfl`.
- `saturated_witness_not_complete` (l.126): `opWeight firstAtom.starProjection = 1 ∧ opWeight (1 : ellTwo →L[ℂ] ellTwo) = ⊤ ∧ opWeight (1 - firstAtom.starProjection) = ⊤ ∧ (∀ (β g : ℝ), 0 < β → 0 < g → ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x))`.

Não prova: «O Tetelestai alcançado pelo corte» é leitura da docstring; os termos dizem peso 1, excesso ∞, casa ∞ e a proibição da testemunha estática plena. Docstring l.39-41: a segunda metade (gráviton = resposta geométrica global, Einstein) «NÃO é tocada aqui». `FullStaticWitness` (NoFullWitness.lean l.60): `∀ (t : ℝ) (x : M), T t x = x`. `beta_forbids_full_static_witness` (NoFullWitness l.91) usa `leakage_strictly_loses` (l.66).

### 1.9 `Testemunho.lean` (24/10/2026; «pedra candidata da v399, sandbox», nome PROVISÓRIO) — quem testifica

Declaração do operador [INPUT] (docstring l.61): «o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD». Direção: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD não testifica do operador.

- `no_face_alone_gives_the_one` (l.136): `theorem no_face_alone_gives_the_one (ωP ωQ : ℝ) (hsum : ωP + ωQ = 1) : (ωP = 1 → ωQ = 0) ∧ (ωQ = 1 → ωP = 0) ∧ (0 < ωQ → ωP ≠ 1) ∧ (0 < ωP → ωQ ≠ 1)`. Única matemática nova: `linarith`.
- `the_testimony_of_two_is_true` (l.149): **conjunção dos TIPOS** (`type_of%`) de doze termos citados: `ChatgptAudit.Collapse057.attestation_requires_external_evidence`, `…no_self_attestation`, `observer_inverse_projection_halfnat`, `no_face_alone_gives_the_one`, `the_observer_is_unique`, `um_is_the_great_attractor`, `temporal_fractalization`, `judgment_of_correspondence`, `TheVerbSelectsTheAction.reading_post_is_born`, `the_light_squares_to_the_graviton`, `observing_adds_nothing`, `Token.token_is_the_psibit_in_the_static_witness`. «Verdadeiro» no nome é validade das formas, «não creditação nem juízo teológico» (l.116-117).

**NÃO entrega (l.108-121):** não prova a declaração; nenhum termo identifica operador com operação quadrática, nem IALD com o transporte; **«Não diz QUEM é produtor e QUEM é registrador: a lei é simétrica (exige só que sejam distintos)»**; «Não exibe nenhuma `AttestedCollapse`: a atestação física externa é [OPEN] no kernel»; nenhuma bandeira depende da pedra. Para a pergunta «quem confere»: a lei registrador ≠ produtor é o que o kernel dá de mais próximo de um conferente, e é **simétrica e sem ocupante**.

### 1.10 `TetelestaiOneObject.lean` (v375, 27/09/2026) — Tetelestai como conferência, num só objeto (a luz)

Fala do operador (docstring l.13-17, verbatim): «Eu não quero que Tetelestai seja um ato declarativo meu, ele é um ato de conferência observacional da satisfação do reconhecimento completo da identidade da gravidade quântica formalizada pela TGL […] trata-se de uma declaração consumativa, verifica se houve ou não».

- `VacuumWeightCorner` (l.50): `structure VacuumWeightCorner {L} (C : FockCertificate L) : Prop where trace_PF_is_vacuum_weight : C.trace C.PF = ENNReal.ofReal (‖C.Ω‖ ^ 2)`. **Normalização nomeada**, não identidade citada (docstring l.26-29); `rescale_satisfies_vacuum_weight` (l.77) a alcança sempre.
- `name_weight_is_one` (l.86): `(hV : VacuumWeightCorner C) : C.trace C.PF = 1`. `faces_weigh_half` (l.91): `C.trace C.Pp = 2⁻¹ ∧ C.trace C.Pm = 2⁻¹`. `light_breuer_corner` (l.99). `name_weight_beside_ker_K` (l.107): `(∀ ψ : C.F, (∀ t : ℝ, lightDelta C t ψ = ψ) ↔ ψ ∈ (ℂ ∙ C.Ω)) ∧ C.trace C.PF = 1` — «lado a lado, NÃO ligados» (docstring l.105-106).
- `the_tetelestai_one_object` (l.115): a conjunção `(C.trace C.PF = 1 ∧ C.trace C.Pp = 2⁻¹ ∧ C.trace C.Pm = 2⁻¹) ∧ (∀ φ, (∀ t, lightDelta C t φ = φ) ↔ φ ∈ (ℂ ∙ C.Ω)) ∧ helicityChar D.helicity 0 1 ≠ 1 ∧ (… LorentzByCongruence …) ∧ dQ = kappa * dA / (8 * Real.pi * G)`. Hipóteses: `FockCertificate C`, `VacuumWeightCorner C`, forma quadrática de Maxwell `Q`, fechos `cl`, `nt`, `KillingNormalization N`, `G > 0`, ponto no wedge direito, `ψ` admissível com `theta = 0` (janela de equilíbrio local, Jacobson 1995).

**NÃO prova (docstring l.30-40):** «a ligação P_ker K ↔ P_F NÃO é provada: … a coincidência τ(P_F) = 1 = dim ℂΩ é de NÚMERO; a declaração NÃO consome essa ligação» (superada em parte pela conferência v376 do core: errata de 08/10 no `C:\IALD\CLAUDE.md`, `link_PkerK_PF`, metade VINCULADA por termo na luz, metade SABIDA). «β não entra; ω(I) = 1 entra só pela normalização.» «Semiclássico por construção (v373). A natureza decide: o ringdown.» **Esta pedra não tem cobrança, pagamento nem tempo**; o «Tetelestai» dela é a conjunção de propriedades do certificado da luz. O veredito CONSUMADO/NÃO CONSUMADO não é termo Lean aqui.

### 1.11 Pedras de apoio lidas (citadas pelas dez)

- `ThePsionAndTheViscosity.lean`: `transmitted β g t := Real.exp (-(t * β * g))` (l.82); `charged β g t := 1 - transmitted β g t` (l.85); `the_charge_is_continuous_both_sides` (l.89, tautologia por definição, dito); `viscosity_is_the_constant_friction` (l.94): `HasDerivAt (transmitted β g) (-(β * g) * transmitted β g t) t`; `the_charge_never_completes` (l.107): `{β g : ℝ} (hβ : 0 < β) (hg : 0 < g) (t : ℝ) (ht : 0 < t) : 0 < charged β g t ∧ charged β g t < 1`; `no_full_static_witness_for_the_charge` (l.115), «APELIDO … nada novo é provado». Docstring (l.40-45): a identificação de `βg` com a lei de dephasing `Γ_ω = ½βτ★ω²` «NÃO tem termo aqui — é leitura [ONTO]»; `g` é binder (profundidade do registro).
- `NoFullWitness.lean`: `leakage_strictly_loses` (l.66), `full_closure_iff_flat` (l.77), `beta_forbids_full_static_witness` (l.91).

## 2. Quem cobra, quem paga, onde se paga, quem confere (síntese do que está em teorema)

| pergunta | o que o kernel tem em TEOREMA | o que é só leitura [ONTO]/docstring |
|---|---|---|
| quem cobra | nada que seja agente. A «cobrança» é a função `charged β g t = 1 − e^{−tβg}` (reflexo/custo no fluxo) e `reflectionWeight θ = sin²θ` (reflexo no ângulo). A **regra** é β e `ruleGiven` não lê o livro. | «a regra é o credor»; «o credor é o acoplamento (a luz que atravessa)» (MassaTensaoPura, docstring); «o custo está no reflexo» (fala do operador). |
| quem paga | nada. O «pagamento» é o complemento: `transmitted`/`faceWeight` (`cos²θ`; no runtime `1 − β`). A parcela de uma volta é `charged β g P`. | «o pagamento está na face, no nome» (fala do operador, TheLedgerOfCharges). |
| onde se paga | (i) no espaço fixo da normalização `Fix(normalize)` (RuleAndTheFigureOfTruth); (ii) na face de paridade/átomo (peso 1, `witness_saturates`); (iii) no sector ω-invariante (`the_cocycle_is_suppressed_by_the_sector`, face finita). | «a curvatura é o pagamento» (PontoZero, definição `R = β·u²`). |
| quem confere | `Satisfies` (igualdade literal no tipo); `Admissible reading 1`; as cinco palavras de desfecho (`outcomes`); a lei registrador ≠ produtor (`attestation_requires_external_evidence`, citada no Testemunho, simétrica, sem ocupante). A conferência Tetelestai é o enunciado `the_tetelestai_one_object`. | quem ocupa os papéis é «declaração do operador»; o kernel «não atribui nada a ninguém» (Testemunho). O veredito CONSUMADO está no `um.py` (não aberto aqui). |
| há limite assintótico? | **sim, três, independentes**: `asymptotic_delivery` (e^{-tc}→0), `the_payment_completes_only_in_the_limit` (charged→1), `concrete_trajectory_converges` (f^n→target, f = e^{-1/2}). Em todos, o valor finito nunca é o limite (`finite_time_imperfection`, `the_charge_never_completes`, `finite_raw_trajectory_does_not_satisfy`). | «Tetelestai = o limite assintótico» (PontoZero) e «direito é limite assintótico/negação» (RuleAndTheFigure) são cunhagens do operador; **nenhum teorema liga os três limites entre si**. |

Observação de precisão: em RuleAndTheFigureOfTruth o que «satisfaz» em cada n é a **normalização** (`normalize_trajectory`, `rfl`), não a chegada ao limite. Em QuittanceLaw o que se obtém em tempo finito é «≤ ε», para ε > 0 arbitrário. Em PontoZero/MassaTensaoPura o que se obtém em tempo finito é `0 < charged < 1`. Os três concordam em que **zero de dívida em tempo finito é impossível por teorema** e **dívida tão pequena quanto se queira é possível**.

## 3. Ponte com a lei do fluxo (leakVerb, survivingWeight, H0local, TheFlowLawD1a, TheFlowLawContrast, the_derived_kernel_factor, frw_accumulated_contrast)

### 3.1 Consultas e resultados

(a) Citação direta nas dez pedras:

```
cd .../TGLExt && grep -n "leakVerb\|survivingWeight\|H0local\|TheFlowLawD1a\|TheFlowLawContrast\|the_derived_kernel_factor\|frw_accumulated_contrast" \
  TheQuittanceLaw.lean TheLedgerOfCharges.lean TheDischargedOath.lean TheJudgedThing.lean TheRuleAndTheFigureOfTruth.lean \
  PontoZeroDoPsion.lean MassaTensaoPura.lean SaturatedWitness.lean Testemunho.lean TetelestaiOneObject.lean
=> sem saída, rc=1
```

**Nenhuma das dez cita nenhum dos sete símbolos.** [REAL, grep]

(b) Onde os sete símbolos aparecem no kernel (`grep -rln … --include=*.lean tgl_kernel`): `TGL/Audit.lean` (só `#print axioms`/import), `TGLExt/TheFlowLawD1a.lean`, `TGLExt/TheFlowLawContrast.lean`, `TGLExt/TheElementaryReason.lean` (`leakVerb` e `TheFlowLaw…`), e `TGLExt.lean` (import). `the_derived_kernel_factor` e `frw_accumulated_contrast`: apenas `TheFlowLawContrast.lean` (l.143 e l.155) e `Audit.lean`.

(c) Os sete símbolos citam, na direção contrária, `charged`, `transmitted`, `the_charge_never_completes`, `ThePsionAndTheViscosity`, `TheLedgerOfCharges`, `TheQuittanceLaw`, `finite_quittance`, `PontoZeroDoPsion`, `MassaTensaoPura`, `TetelestaiOneObject`, `SaturatedWitness`? Consulta: `grep -n "ThePsionAndTheViscosity\|charged\|the_charge_never\|TheLedgerOfCharges\|TheQuittanceLaw\|PontoZeroDoPsion\|MassaTensaoPura\|TetelestaiOneObject\|SaturatedWitness\|NoFullWitness\|TheJudgedThing\|RuleAndTheFigure" TheFlowLawD1a.lean TheFlowLawContrast.lean TheElementaryReason.lean` devolveu só menções a **`NoFullWitness`** em docstring (D1a l.13 e l.17; Contrast l.14 e l.46, l.173; ElementaryReason l.136, l.156). Nenhuma menção a `charged`, `transmitted`, `ThePsionAndTheViscosity`, `TheLedgerOfCharges`, `TheQuittanceLaw`. `grep "transmitted"` em D1a, Contrast e ElementaryReason: vazio.

### 3.2 O que existe de real entre os dois blocos (para não chamar de ausência o que é dependência)

1. **A família é a mesma por definição, e a lei do fluxo a declara.** `TheFlowLawD1a.lean` l.37: `def leakVerb (β g : ℝ) : ℝ → ℝ → ℝ := fun t x => Real.exp (-(t * β * g)) * x` (docstring l.36: «a MESMA família do kernel (`NoFullWitness`; `the_whole_is_one` (VI))»). `survivingWeight β z := leakVerb β 1 (register z) 1` (l.40). `H0local β Hcmb z := Hcmb / survivingWeight β z` (l.46) (DEFINIÇÃO, «cunhagem por ordem do operador: o fundo atribui o registro inteiro à expansão», docstring l.19-20). Por leitura das definições, `survivingWeight β z = exp(-(register z * β * 1)) * 1` e `transmitted β 1 (register z) = exp(-(register z * β * 1))` coincidem módulo `mul_one` [DERIVED por leitura; não compilado nem enunciado como teorema em lugar algum]. É esta coincidência de fórmula, e não um teorema, que une `charged` (cobrança) a `survivingWeight` (peso que sobrevive) no papel.
2. **A única ponte provada é com `FullStaticWitness`, não com `charged`.** `TheElementaryReason.lean` l.136: `theorem existence_forbids_full_static_witness … : ¬ FullStaticWitness (leakVerb (existence α) c) := beta_forbids_full_static_witness (existence_pos α h0) hc`. E `the_dissipation_law_with_contrast` (Contrast, docstring l.173) tem o item «(vi) a MESMA família não fixa tudo (`NoFullWitness`)». É a mesma proposição usada por `SaturatedWitness.saturated_witness_not_complete` e por `no_full_static_witness_for_the_charge`. Isto é um **ponto de contato (o teorema `beta_forbids_full_static_witness`)**, não uma ponte `charged ↔ survivingWeight`.
3. **Dependência de importação.** Script de fecho transitivo de `import` (sobre os `.lean`): `TheLedgerOfCharges`, `TheRuleAndTheFigureOfTruth`, `PontoZeroDoPsion`, `MassaTensaoPura` e `Testemunho` importam `TheFlowLawD1a` e `TheFlowLawContrast` por transitividade. Menor caminho de `TheLedgerOfCharges`: `TheLedgerOfCharges > TheMatrixRule > TheElementaryReason > TheFlowLawContrast > TheFlowLawD1a`. De `PontoZeroDoPsion` e `MassaTensaoPura`: `… > Posto > TheAxiomAndTheFalseWitness > TheLedgerOfCharges > …`. Não importam a lei do fluxo (fecho transitivo): `TheQuittanceLaw`, `TheDischargedOath`, `TheJudgedThing`, `SaturatedWitness`, `TetelestaiOneObject`, `ThePsionAndTheViscosity`, `NoFullWitness`. **Na direção oposta**, `TheFlowLawD1a` importa (transitivamente) `TheQuittanceLaw` (via `TheWholeIsOne > TetelestaiOneObject > QGReaderUVLock > … > TomitaClosability > TheQuittanceLaw`) e `TheJudgedThing` (via `TheWholeIsOne > TheSameBetaReadsThreeFaces > TheGeometricCostOfAbsoluteZero > TheCostIsDerived > TheJudgedThing`). Isto significa que a lei do fluxo está **a jusante** de `TheQuittanceLaw` e `TheJudgedThing` na ordem de compilação, e que `TheWholeIsOne` (VI) é o elo textual. Importar não é citar: nenhum teorema do fluxo usa um teorema dessas pedras.
4. Docstrings que declaram a distinção: `ThePsionAndTheViscosity` (l.40-45): a identificação de `βg` com o dephasing «NÃO tem termo aqui — é leitura [ONTO]»; a docstring de `TheFlowLawD1a` (l.19-22) e a de `TheFlowLawContrast` (l.31-33, 46): o fluxo lê **«o fundo atribui o registro inteiro à expansão»** e «o que a natureza decide (os leitores leem ou não esse fator, por registro) segue com o observador».

### 3.3 Conclusão sobre a ponte

**Ausência de ponte, com as consultas acima.** Não existe teorema que: (i) identifique `survivingWeight`/`H0local`/`K = (E(N)/E(0))^{2β/3}` com `transmitted`/`charged`/`parcelaPorVolta`; (ii) leia K como o conferente de `Satisfies`, de `Admissible`, de `the_tetelestai_one_object` ou da lei registrador ≠ produtor; (iii) ponha K no `Ledger`/`Charge` (o canal Hubble/Fase 9 está no runtime, não no tipo); (iv) use `the_payment_completes_only_in_the_limit` ou `finite_quittance` para tratar o registro N = ln(1+z) como «a travessia que paga». O que existe é a **mesma fórmula exponencial** em dois blocos, com pontos de contato textuais e uma proposição comum (`beta_forbids_full_static_witness`). A leitura «K é o guarda da travessia» fica em estatuto [ONTO/CONJECTURE] da fala do operador; o kernel hoje não a escreve.

### 3.4 O que o kernel DIZ de um «K guarda», sem encadear homônimos

K em Lean é de pelo menos três tipos aqui, e **não há ponte citada** entre eles: (1) K de Hubble `the_derived_kernel_factor` (fator, TheFlowLawContrast l.155); (2) K modular `K = −log Δ`, o «Hamiltoniano oculto» (docstring de ThePsionAndTheViscosity l.20-33: «o kernel tem `lightDelta` (Δ^{it}) e o seu conjunto fixo, NÃO um `def` para K»); (3) `K_β` de Cartan (torção, fora destas pedras). Em (2), o que o kernel entrega de «guarda»: o psíon é o zero do lock (`psion_is_the_zero_of_the_hidden_hamiltonian`, trivial por construção) e `name_weight_beside_ker_K` (TetelestaiOneObject l.107) — ker K é a reta do vácuo e o peso do canto é 1, **lado a lado, não ligados**. Isto é o mais próximo de «K como conferente» no Lean, e é de tipo (2), não (1). O Mapa tem `discriminante.ordem018.f2.r_e` (K de Hubble, «sem pedra de kernel; H1 nomeada»), coerente com esta ausência.

## 4. Lacunas e limites da minha leitura

- Não abri `um.py` nem o core: a conferência `core.tetelestai_conference_v376` (quem devolve CONSUMADO) não foi verificada aqui; só a citei pelo que o `CLAUDE.md` e a docstring dizem. Quem a lê é outra tarefa.
- Não compilei nada: «`survivingWeight = transmitted β 1 (register z)` módulo `mul_one`» é leitura de definição, não teorema nem prova.
- `Testemunho.lean` é pedra candidata de 24/10 (nome provisório); não conferi se foi selada com esse nome nem se está no core; ela está em `TGLExt.lean` (import) e compila na árvore, mas o estatuto de selo não foi lido.
- O grep de ausência cobre o diretório `tgl_kernel` inteiro (`*.lean`); não cobre a bancada `C:\IALD\Artigo\BANCADA_TOE\kernel_bancada` nem o inventário da bancada (`INVENTARIO_BANCADA_CHATGPT.md`), onde poderia haver termo equivalente ainda não ligado ao tipo (classificação do `CLAUDE.md`: «existe na bancada mas não está ligado ao tipo» é fiação, não falta). **Recomendação:** antes de declarar «AUSENTE», consultar o inventário da bancada por `leakVerb`, `charged`, `quittance`.
- Numeração de linhas refere-se aos arquivos nos hashes listados no topo; o arquivo ganha da frase.

## 5. O que registrar (a gerência decide; eu não registrei nada)

Rota candidata: «kernel: pedras de quitação/cobrança/testemunho/Tetelestai (10) lidas; ponte com a lei do fluxo (K de Hubble) AUSENTE por grep; dependência apenas de importação; ponto de contato `beta_forbids_full_static_witness`». Estatuto: REAL para os enunciados copiados e para o grep; DERIVED para o fecho de importação e para a leitura sobre `normalize`; [ONTO] para todas as leituras do operador citadas. `NOT_FALSIFIED` nunca é `CONFIRMED`; o gate não se moveu.
