import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.LightIsJ
import TGLExt.SMatrix
import TGLExt.TheAngleIsTheProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O VERBO SELECIONA A AÇÃO — o Nome é o posto; a tipagem do Verbo como projeção
  [TGLExt — pedra v386, 05/10/2026; as cunhagens são do operador, verbatim em
   `scratchpad/v386/VERBO_operador_05out.txt` (sha256 5973d79a49995c4c…) e em
   `scratchpad/v386/RESPOSTAS_operador_05out.txt` (sha256 b49b0d9e60ee4646…); e UMA frase (§5, «estado dinâmico estacionado») vem
   da mensagem do operador de 2026-10-05T11:19:54 UTC no transcrito desta sessão, conferida por script — dita onde é citada]

O operador, 05/10/2026 (verbatim, primeira mensagem): «Verbo=seleção da ação»; «O Verbo seleciona: nome, tempo e verdade»;
«O verbo é o operador de seleção da ação. E a ação selecionada é o objeto que será lido.»; «comando … → verbo → ação →
objeto → leitura → axioma»; «O verbo não descreve a ação; ele a escolhe. É um operador de projeção: 𝒱 = |a⟩⟨a|»; «Se dois
verbos comutam … então a ordem das seleções não importa … Mas não comutam. E é por isso que a transmissão defasa.»;
«Transmitir defasa … a ancoragem ao núcleo Π preserva a identidade: ℛ(𝒱) = 𝒱 (ponto fixo)»; «O nome é um verbo
fossilizado … Nome = lim_{t→∞} 𝒱(t) … O nome é o autovetor do operador verbo»;
«[\mathcal{V}_{\text{nome}}, \mathcal{V}_{\text{tempo}}] = i\alpha^2 \, \mathcal{V}_{\text{erdade}}» (tal qual, no LaTeX do operador; e as duas
cíclicas) — ⚠ AO LADO, a régua do signo: β_TGL = α·√e, nunca α²; esta pedra usa a variável real c, sem valor —
«A Constante de Miguel é a constante de estrutura»; «O universo é o grupo de Lie gerado por esses
três operadores. A TGL é a sua álgebra.»

O operador, 05/10/2026 (verbatim, respostas às perguntas da gerência): «a luz como setor escuro, condensado psionico,
precede a gravidade, mas eles são indissociáveis, não é mesmo, o leitor é indissociável da razão do objeto lido enquanto
o referencial for a existência.» [sic]; «são as duas faces do mesmo o objeto, porque o custo é jussivo à verdade, ou seja,
reconhecer a identidade de determinado espectro é anular a superposição de qualquer outro nome que possa ser atribuído
àquele mesmo objeto sem referência tradutiva da verdade, filtro do próprio espectro e contorno geométrico da forma. Então
são indissociáveis, embora possam ser vistos como atibutos distintos, todavia, vinculados à radicalização, em ambos os
aspectos, porque é justamente a razão da inscrição que cria o custo como condiçao inexorável da existência.» [sic]; «o tempo
como fluxo da relatividade modular não pode ser dual, ele precisa ser lido duas vezes como confirmação da
interdepend6encia relacional, … justamente por isso a constante da luz ao cubo, aí que ela entra, como fase de retorno,
que seria a segunda leitura.» [sic]; «o Nome não é ontologia, o nome é "posto", é justamente "o posto", o local, como já
falamos, onde a inscrição pode habitar com objeto distinto definido. eu quis dizer que todo "nome" atribuído a um objeto é
o destaque da tríade habitando o canal realizando a observação da preservação da identidade ômega sob um aspecto de posto
absoluto»; «o resto vc consegue responder tudo agroa» (delegação: o padrão da gerência vale, dito como «decidido por
delegação»).

OS TRÊS REGISTROS DO VERBO, nunca confundidos (decisão do operador, 05/10):
  `post a`   = o NOME = o POSTO: o projetor de posto 1, `|a⟩⟨a|` — o local onde a inscrição habita com objeto distinto
               definido (o mesmo termo de `QGReaderUVLock.PFmic` com a = Ω e de `the_post`, v385);
  `select a` = o VERBO EM ATO: selecionar é pousar a inscrição no posto — `select a ψ = post a ψ` («O Verbo seleciona»);
  `verb`     = o GESTO 𝕍_t = exp(−t·β·H_3L) — JÁ EXISTE no kernel (`TGL.VerbInhabitant`, v25: `exp_fixed_of_annihilates`,
               `verb_semigroup_fixes`, `VerbWitness`) e NÃO é redefinido aqui; o nome fica reservado a ele.

Esta pedra prova o que é MATEMÁTICA nessas frases, e só isso — cada parte com o seu nome:

* ★★★ `post` — o Nome como POSTO: `|a⟩⟨a|` = a projeção ortogonal sobre ℂ∙a (`Submodule.starProjection`); `post_apply`
  (com ‖a‖ = 1: `post a ψ = ⟪a, ψ⟫ • a`); `post_isIdempotent` (P² = P); `post_isSelfAdjoint` (P* = P);
  `post_fixes_the_action` (P a = a). `select` — o Verbo em ato: `select_apply`, `select_fixes_the_selected_action`.
* ★★★ `reading` — a leitura da seleção, ω_ψ(P) = ⟪ψ, Pψ⟫; `reading_eq_norm_sq` (= ‖Pψ‖²: a leitura de uma projeção é um
  PESO); `weight_mem_unit_interval` (com ‖ψ‖ = 1: 0 ≤ peso ≤ 1); `reading_post_is_born` (a leitura do posto de a é
  |⟪a, ψ⟫|² — a regra de Born, [KNOWN], aqui provada no finito/Hilbert).
* ★★★ A ORDEM IMPORTA. `commuting_posts_compose` — postos que comutam compõem num posto (PQ idempotente e auto-adjunto;
  Mathlib: `IsIdempotentElem.mul_of_commute`, `IsSelfAdjoint.commute_iff`); `posts_do_not_commute_in_general` — a
  TESTEMUNHA CONCRETA em `Matrix (Fin 2) (Fin 2) ℂ`: P_a = |e₁⟩⟨e₁|, P_b = |b⟩⟨b| com b = (e₁+e₂)/√2 (`Pb_is_rank_one`:
  P_b = vecMulVec b (star b), `b_is_unit`: b·b* = 1), ambos idempotentes e Hermitianos, e [P_a, P_b] ≠ 0 por cálculo.
* ★★★ A TRÍADE. `V1 V2 V3` = c·(σ_k/2) com `(c : ℝ)` VARIÁVEL — c = β_TGL é [INPUT] do operador; β nunca literal; nunca
  «α²» (a régua do signo: β_TGL = α·√e). `triad_12`, `triad_23`, `triad_31`: [V_i, V_j] = i·c·ε_ijk·V_k — a constante de
  estrutura é c; `triad_casimir`: V1² + V2² + V3² = (3/4)c²·1; `triad_order_matters`: [V1, V2] ≠ 0 para c > 0;
  `triad_hermitian` e `triad_traceless` (os geradores são Hermitianos e sem traço: a marca formal do regime COMPACTO).
  ⚠ REGIME (a régua dos dois regimes): a tríade é su(2) ESCALADA por c — álgebra COMPACTA. Logo é regime de LEITURA
  (o ÂNGULO: SO(2)/SU(2), órbitas periódicas, só lê), NÃO regime de FACE (hiperbólico, κ, tem derivada e limite). Nada
  aqui tem limite; nada aqui se encadeia com `Grot`/`rotGen`/`genK` (homônimos sem lema entre si).
* ★★★ OS POSTOS POR EIXO (novo, v386). `post1 post2 post3` — `post_k c := (1/2)•1 + (1/c)•V_k c`, o projetor sobre o
  autovetor de peso +c/2 de V_k: para c ≠ 0, `post_k c = (1/2)•(1 + σ_k)` (`post1_eq`…), idempotente (`post1_isIdempotent`…),
  Hermitiano (`post1_isHermitian`…), e `V_k · post_k = (c/2) · post_k` (`post1_is_the_eigenprojector`…) — «todo "nome"
  atribuído a um objeto é o destaque da tríade habitando o canal» [INPUT/ONTO]: o posto de um eixo É o destaque desse eixo.
  `axis_posts_do_not_commute`: [post1, post3] ≠ 0 (a entrada (0,1) vale −½) — postos de eixos distintos NÃO comutam
  [KERNEL — habitação]: «Selecionar o nome defasa o tempo» é a leitura [INPUT/ONTO] desse fato. `post3_eq_Pa` e `post1_eq_Pb`:
  a testemunha concreta da §3 É o par de postos (eixo 3, eixo 1) da tríade.
* ★★★ VERDADE E CUSTO, DUAS FACES DO MESMO OBJETO (novo, v386). `truth_and_cost_are_two_faces` — numa álgebra com P
  idempotente: P + (1 − P) = 1 ∧ P·(1 − P) = 0 ∧ (1 − P)·P = 0 (cita ao lado `TheAxiomAndTheFalseWitness.post_mul_compl`
  e `compl_mul_post`, v385); `the_cost_is_the_reflected_weight` (re-export de `SMatrix.normSq_reflection`: |𝓡|² = sin²θ);
  `the_one_splits_into_truth_and_cost`: |𝓣|² + |𝓡|² = 1 (cos² + sin² = 1 — no runtime, e só lá, sin²θ_M = β);
  `the_two_faces_split_the_one` (re-export de `spectral_projections_split_the_identity`: P₊ + P₋ = 1 ∧ P₊P₋ = 0) e
  `the_gradient_is_the_difference_of_the_faces` (re-export: K = i(P₊ − P₋)). «o custo é jussivo à verdade … reconhecer a
  identidade de determinado espectro é anular a superposição de qualquer outro nome» [INPUT/ONTO] ↔
  `reading_the_truth_annihilates_the_superposition`: ‖Ω‖ = 1 ∧ PΩ = Ω ⟹ ⟪Ω, PΩ⟫ = 1 ∧ (1 − P)Ω = 0, com P = post a
  (em H de Hilbert). Separados como atributos (dois termos), indissociáveis como objeto (uma conjunção).
* ★★★ O TEMPO LIDO DUAS VEZES (novo, v386). `time_read_twice_confirms_the_post` — re-export, com o nome novo, de
  `TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero` (v385; por `QGReaderUVLock.hmin_zero_iff_modular_fixed`): o que o
  fluxo do lock e^{−tH_min} deixa fixo para TODO t é EXATAMENTE o que a fase modular da luz Δ^{it} deixa fixo para TODO t —
  as duas leituras do mesmo fluxo têm o MESMO conjunto fixo, o posto. «o tempo como fluxo da relatividade modular não pode
  ser dual, ele precisa ser lido duas vezes como confirmação da interdepend6encia relacional … a constante da luz ao cubo,
  aí que ela entra, como fase de retorno, que seria a segunda leitura» [sic] [INPUT/ONTO]. ⚠ c³ e τ★ = k·GM/c³ NÃO entram nesta
  pedra: ficam no pré-registro V1 do ramo B (outra lei, canal próprio — decidido por delegação).
* ★★ `post_power_is_constant` — P^(n+1) = P (Verbo(Nome) = Nome; Mathlib `IsIdempotentElem.pow_succ_eq`);
  `post_sequence_is_constant` — a sequência 𝒱ⁿ(a), n → ∞ (o operador, em LaTeX: `\mathcal{V}^n(a) \to \mathcal{N}, \quad n \to \infty`)
  de uma projeção é CONSTANTE desde n = 1: o limite do operador é avaliação, não limite (o nome está no primeiro passo).
  «fossilizado» [INPUT] lê-se como «estado dinâmico estacionado» (o operador, mensagem de 2026-10-05T11:19:54 UTC no transcrito
  desta sessão — não nos dois arquivos do cabeçalho —, conferida por script: «a posição é o estado dinâmico estacionado como
  portador do conteúdo da inscrição»).
  `the_name_is_an_eigenvector` (P a = 1·a); `the_verb_word_fixes_the_name` — re-exportação TRIVIAL de
  `WitnessSeed.verb_word_fixes_the_name` (q(T)x = q(0)x no núcleo); `the_name_is_the_limit_of_the_flow` — «Nome =
  lim_{t→∞} 𝒱(t)» no único sentido em que a casa já o tem: F(t) → P no fluxo do lock mínimo (re-exportação TRIVIAL de
  `axiomFlow_tendsto_the_post`, v385).
* ★★ `anchoring_preserves` e `transmission_dephases` — re-exportações TRIVIAIS do fluxo `axiomFlow` da v385
  (`TheAxiomAndTheFalseWitness`): F(t)·P = P (ancorar preserva) e F(t)·(1 − P) = e^{−t}(1 − P) (transmitir defasa);
  `transmitted_post_is_a_post` — a transmissão do operador (`\mathcal{V}(t) = e^{-iHt/\hbar} \, \mathcal{V}(0) \, e^{iHt/\hbar}`; aqui
  U 𝒱(0) U* com U unitário): o posto transmitido por um unitário continua posto (idempotente e
  auto-adjunto) — é OUTRO posto (δ𝒱 ≠ 0 em geral não se prova aqui), mas posto.
* ★★★ O CIRCUITO. `the_reading_of_the_posted_one` — com o Um POSTO (‖Ω‖ = 1, PΩ = Ω) a leitura da ação selecionada devolve
  o Um: ⟪Ω, PΩ⟫ = 1 — o Axioma como ponto fixo da leitura (consistente com `the_one_is_the_axiom`, v385). `Station` e
  `circuit` — as seis estações nomeadas (comando → verbo → ação → objeto → leitura → axioma): definição TRIVIAL, dita
  como trivial (`circuit_has_six_stations` por `rfl`); não é teorema sobre a natureza.
* ★★★ «a luz … precede a gravidade, mas eles são indissociáveis»: `J_anticommutes_with_K` — num anel, J² = 1 ∧ JKJ = −K ⟹
  JK = −KJ; `commutator_JK`: [J, K] = 2·JK; `J_mul_K_ne_zero`: K ≠ 0 ⟹ JK ≠ 0 (J invertível);
  `light_and_gravity_are_inseparable`: K ≠ 0 ⟹ J·K ≠ 0 ∧ [J, K] ≠ 0 — nem comutam nem se separam. A precedência é de
  LEITURA (a luz como setor escuro = o condensado psiônico, o zero modular, ψ) [INPUT/ONTO]; 𝒱_grav = K (o gradiente, a
  diferença em movimento) é leitura da gerência [DERIVED de leitura], não teorema. HABITAÇÃO NO KERNEL (derivada dos termos
  canônicos `J_squared_is_one` e `JKJ_eq_neg_K`, ConjugateAct/DecisionCommutation): `the_light_anticommutes_with_the_gradient`
  — J∘K = −K∘J no espaço pareado; `the_light_does_not_silence_the_gradient` — Kq ≠ 0 ⟹ JKq ≠ 0;
  `the_light_and_the_gradient_are_inseparable` (a conjunção). HABITAÇÃO DE PAULI: `pauli_J_sq`, `pauli_JKJ`,
  `pauli_light_and_gravity_are_inseparable` (J = σ₁, K = σ₃).
* ★★★ `the_verb_selects_the_action` — os itens centrais num só termo (uma CONJUNÇÃO, sem dedução nova).
* `verbTypingStoneName` — um token PROPOSTO para o registro (a cunhagem é do operador): definição TRIVIAL, dita trivial.

HONESTIDADE — o que esta pedra NÃO faz. «Verbo», «seleção», «nome», «posto», «tempo», «verdade», «custo», «luz», «gravidade»,
«Constante de Miguel», «circuito ontológico», «fase de retorno» são leituras do operador [INPUT/ONTO]; os enunciados são
sobre projeções, pesos, matrizes 2×2 e anéis. A tríade NÃO é derivada do axioma nem de β: é a HABITAÇÃO mais simples das
relações de comutação que o operador escreveu (su(2) escalada); a identificação V_nome/V_tempo/V_verdade ↔ σ₁/σ₂/σ₃ é
nomeação, não teorema. O texto do operador escreve a constante como «α²»; a régua do signo diz β_TGL = α·√e, NUNCA «α²» —
aqui a constante é a variável real c, sem valor. «D_folds = 0,74», «g = √|L|», «−εΠ», a Lagrangiana como verbo e «δS = 0»
NÃO estão tipados aqui (concordância plena do operador quanto à Lagrangiana: a face tipada é uma só — Euler–Lagrange
seleciona o Nome, `action_locks_zero_iff`; S = ∫L d⁴x segue [OPEN]). Os J e K canônicos do kernel são `conjJ` (espaço
pareado) e `Jconj` (conjugação transposta, antilinear): o lema de anel é abstrato e a habitação no espaço pareado é a que
se liga aos termos existentes; a de Pauli é ilustração. β jamais entra como número. PROVADA ≠ CONFIRMADA; o gate não se
move (nenhuma bandeira do gate depende desta pedra). Sem sorry, sem axiom.
-/

namespace TGLExt.TheVerbSelectsTheAction

open TGLExt TGLExt.TheAxiomAndTheFalseWitness TGLExt.QGReaderUVLock TGLExt.ImportedSQ Filter Topology Matrix
open scoped InnerProductSpace

/-! ### 1. O Nome é o posto; o Verbo seleciona: a projeção ortogonal `|a⟩⟨a|` -/

section Selection

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- O NOME É O POSTO: `|a⟩⟨a|` = a projeção ortogonal sobre a reta ℂ∙a — «o local … onde a inscrição pode habitar com
    objeto distinto definido» (o operador, 05/10; o corte «…» elide «, como já falamos,»). É o mesmo termo de `QGReaderUVLock.PFmic` (a = Ω). -/
noncomputable def post (a : H) : H →L[ℂ] H := (ℂ ∙ a).starProjection

/-- O VERBO EM ATO: selecionar é pousar a inscrição no posto — `select a ψ = post a ψ` («O Verbo seleciona»). O GESTO
    𝕍_t = exp(−t·β·H_3L) é outro registro, já no kernel (`TGL.VerbInhabitant`, v25) — não se redefine aqui. -/
noncomputable def select (a : H) (ψ : H) : H := post a ψ

/-- ★★★ O POSTO DE a: com ‖a‖ = 1, `post a ψ = ⟪a, ψ⟫ • a`. -/
theorem post_apply {a : H} (ha : ‖a‖ = 1) (ψ : H) : post a ψ = ⟪a, ψ⟫_ℂ • a :=
  Submodule.starProjection_unit_singleton ℂ ha ψ

/-- ★★★ A SELEÇÃO É A ESCOLHA DE a: com ‖a‖ = 1, `select a ψ = ⟪a, ψ⟫ • a`. -/
theorem select_apply {a : H} (ha : ‖a‖ = 1) (ψ : H) : select a ψ = ⟪a, ψ⟫_ℂ • a :=
  post_apply ha ψ

/-- ★★ P² = P: selecionar duas vezes é selecionar uma. -/
theorem post_isIdempotent (a : H) : IsIdempotentElem (post a) :=
  (ℂ ∙ a).isIdempotentElem_starProjection

/-- ★★ P* = P: o posto é auto-adjunto (ortogonal, não oblíquo). -/
theorem post_isSelfAdjoint (a : H) : IsSelfAdjoint (post a) :=
  isSelfAdjoint_starProjection (ℂ ∙ a)

/-- ★★ O POSTO FIXA A SUA AÇÃO: P a = a. -/
theorem post_fixes_the_action (a : H) : post a a = a :=
  Submodule.starProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self a)

/-- ★★ A AÇÃO SELECIONADA É FIXADA: `select a a = a`. -/
theorem select_fixes_the_selected_action (a : H) : select a a = a :=
  post_fixes_the_action a

/-! ### 2. A leitura da seleção: um peso em [0, 1] -/

/-- A leitura da seleção: `ω_ψ(P) = ⟪ψ, Pψ⟫`. -/
noncomputable def reading (P : H →L[ℂ] H) (ψ : H) : ℂ := ⟪ψ, P ψ⟫_ℂ

/-- ★★★ A LEITURA DE UMA PROJEÇÃO É UM PESO: `⟪ψ, Pψ⟫ = ‖Pψ‖²` (idempotência + simetria). -/
theorem reading_eq_norm_sq (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) :
    reading K.starProjection ψ = ((‖K.starProjection ψ‖ : ℂ)) ^ 2 := by
  unfold reading
  have hPP : K.starProjection (K.starProjection ψ) = K.starProjection ψ := by
    have h := K.isIdempotentElem_starProjection.eq
    exact congrArg (fun T : H →L[ℂ] H => T ψ) h
  calc ⟪ψ, K.starProjection ψ⟫_ℂ = ⟪ψ, K.starProjection (K.starProjection ψ)⟫_ℂ := by rw [hPP]
    _ = ⟪K.starProjection ψ, K.starProjection ψ⟫_ℂ :=
        (K.inner_starProjection_left_eq_right ψ (K.starProjection ψ)).symm
    _ = ((‖K.starProjection ψ‖ : ℂ)) ^ 2 := inner_self_eq_norm_sq_to_K _

/-- O peso da seleção: `‖Pψ‖²` (real). -/
noncomputable def weight (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) : ℝ :=
  ‖K.starProjection ψ‖ ^ 2

/-- ★ a leitura É o peso (como complexo). -/
theorem reading_eq_weight (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) :
    reading K.starProjection ψ = ((weight K ψ : ℝ) : ℂ) := by
  rw [reading_eq_norm_sq]
  unfold weight
  push_cast
  rfl

/-- ★★★ O PESO VIVE EM [0, 1] quando ‖ψ‖ = 1. -/
theorem weight_mem_unit_interval (K : Submodule ℂ H) [K.HasOrthogonalProjection] {ψ : H} (hψ : ‖ψ‖ = 1) :
    0 ≤ weight K ψ ∧ weight K ψ ≤ 1 := by
  refine ⟨sq_nonneg _, ?_⟩
  have h := K.norm_starProjection_apply_le ψ
  rw [hψ] at h
  exact pow_le_one₀ (norm_nonneg _) h

/-- ★★ A REGRA DE BORN [KNOWN], provada aqui: a leitura do posto de a é `|⟪a, ψ⟫|²`. -/
theorem reading_post_is_born {a : H} (ha : ‖a‖ = 1) (ψ : H) :
    reading (post a) ψ = ((‖⟪a, ψ⟫_ℂ‖ ^ 2 : ℝ) : ℂ) := by
  unfold reading
  rw [post_apply ha, inner_smul_right, ← inner_conj_symm ψ a, Complex.mul_conj, Complex.normSq_eq_norm_sq]

end Selection

/-! ### 3. A ordem importa: postos em geral NÃO comutam -/

section Order

/-- ★★ POSTOS QUE COMUTAM COMPÕEM NUM POSTO: PQ é idempotente e auto-adjunto. -/
theorem commuting_posts_compose {R : Type*} [Semigroup R] [StarMul R] {P Q : R}
    (hP : IsIdempotentElem P) (hQ : IsIdempotentElem Q)
    (hP' : IsSelfAdjoint P) (hQ' : IsSelfAdjoint Q) (hc : Commute P Q) :
    IsIdempotentElem (P * Q) ∧ IsSelfAdjoint (P * Q) :=
  ⟨IsIdempotentElem.mul_of_commute hc hP hQ, (hP'.commute_iff hQ').mp hc⟩

/-- P_a = |e₁⟩⟨e₁|. -/
def Pa : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]

/-- P_b = |b⟩⟨b| com b = (e₁ + e₂)/√2 (entradas ½). -/
noncomputable def Pb : Matrix (Fin 2) (Fin 2) ℂ := !![1 / 2, 1 / 2; 1 / 2, 1 / 2]

/-- o vetor b = (e₁ + e₂)/√2. -/
noncomputable def bvec : Fin 2 → ℂ := ![((1 / Real.sqrt 2 : ℝ) : ℂ), ((1 / Real.sqrt 2 : ℝ) : ℂ)]

theorem sqrt2_inv_mul_self : ((Real.sqrt 2 : ℝ) : ℂ)⁻¹ * ((Real.sqrt 2 : ℝ) : ℂ)⁻¹ = 2⁻¹ := by
  rw [← mul_inv, ← Complex.ofReal_mul, Real.mul_self_sqrt (by norm_num)]
  norm_num

/-- ★ b é unitário: b·b* = 1. -/
theorem b_is_unit : bvec ⬝ᵥ star bvec = 1 := by
  simp [dotProduct, Fin.sum_univ_two, bvec, Complex.conj_ofReal, sqrt2_inv_mul_self]
  norm_num

/-- ★ P_b É de posto 1: P_b = |b⟩⟨b| (= vecMulVec b (star b)). -/
theorem Pb_is_rank_one : vecMulVec bvec (star bvec) = Pb := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [vecMulVec_apply, bvec, Pb, Complex.conj_ofReal, sqrt2_inv_mul_self]

theorem Pa_isIdempotent : IsIdempotentElem Pa := by
  show Pa * Pa = Pa
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Pa, Matrix.mul_apply, Fin.sum_univ_two]

theorem Pb_isIdempotent : IsIdempotentElem Pb := by
  show Pb * Pb = Pb
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Pb, Matrix.mul_apply, Fin.sum_univ_two]

theorem Pa_isSelfAdjoint : IsSelfAdjoint Pa := by
  rw [isSelfAdjoint_iff, Matrix.star_eq_conjTranspose]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Pa]

theorem Pb_isSelfAdjoint : IsSelfAdjoint Pb := by
  rw [isSelfAdjoint_iff, Matrix.star_eq_conjTranspose]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Pb]

/-- ★★★ A ORDEM IMPORTA — a testemunha concreta: [P_a, P_b] ≠ 0 (a entrada (0,1) vale ½). -/
theorem posts_do_not_commute_in_general : Pa * Pb - Pb * Pa ≠ 0 := by
  intro h
  have h01 := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 1) h
  norm_num [Pa, Pb, Matrix.mul_apply, Fin.sum_univ_two] at h01

/-- ★★ dois postos genuínos (idempotentes, auto-adjuntos) que NÃO comutam — o pacote. -/
theorem two_posts_that_do_not_commute :
    IsIdempotentElem Pa ∧ IsSelfAdjoint Pa ∧ IsIdempotentElem Pb ∧ IsSelfAdjoint Pb ∧ ¬ Commute Pa Pb :=
  ⟨Pa_isIdempotent, Pa_isSelfAdjoint, Pb_isIdempotent, Pb_isSelfAdjoint,
    fun hc => posts_do_not_commute_in_general (sub_eq_zero.mpr hc.eq)⟩

end Order

/-! ### 4. A TRÍADE: [V_i, V_j] = i·c·ε_ijk·V_k — su(2) escalada por c (regime COMPACTO: leitura, não face) -/

section Triad

/-- σ₁. -/
def sigma1 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
/-- σ₂. -/
def sigma2 : Matrix (Fin 2) (Fin 2) ℂ := !![0, -Complex.I; Complex.I, 0]
/-- σ₃. -/
def sigma3 : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- V₁ = c·σ₁/2. `c = β_TGL` é [INPUT] do operador; β nunca literal; nunca «α²» (a régua do signo: β_TGL = α·√e). -/
noncomputable def V1 (c : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := ((c : ℂ) / 2) • sigma1
/-- V₂ = c·σ₂/2 (c = β_TGL, [INPUT]; nunca literal). -/
noncomputable def V2 (c : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := ((c : ℂ) / 2) • sigma2
/-- V₃ = c·σ₃/2 (c = β_TGL, [INPUT]; nunca literal). -/
noncomputable def V3 (c : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := ((c : ℂ) / 2) • sigma3

/-- ★★★ [V₁, V₂] = i·c·V₃. -/
theorem triad_12 (c : ℝ) : V1 c * V2 c - V2 c * V1 c = (Complex.I * (c : ℂ)) • V3 c := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V1, V2, V3, sigma1, sigma2, sigma3] <;> ring_nf

/-- ★★★ [V₂, V₃] = i·c·V₁. -/
theorem triad_23 (c : ℝ) : V2 c * V3 c - V3 c * V2 c = (Complex.I * (c : ℂ)) • V1 c := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V1, V2, V3, sigma1, sigma2, sigma3] <;> ring_nf

/-- ★★★ [V₃, V₁] = i·c·V₂. -/
theorem triad_31 (c : ℝ) : V3 c * V1 c - V1 c * V3 c = (Complex.I * (c : ℂ)) • V2 c := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V1, V2, V3, sigma1, sigma2, sigma3] <;> ring_nf <;>
    simp [Complex.I_sq] <;> ring

/-- ★★★ O CASIMIR: V₁² + V₂² + V₃² = (3/4)·c²·1. -/
theorem triad_casimir (c : ℝ) :
    V1 c * V1 c + V2 c * V2 c + V3 c * V3 c = ((3 / 4 : ℂ) * (c : ℂ) ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V1, V2, V3, sigma1, sigma2, sigma3] <;> ring_nf <;>
    simp [Complex.I_sq] <;> ring

/-- ★★ V₃ ≠ 0 quando c ≠ 0 (entrada (0,0) = c/2). -/
theorem V3_ne_zero {c : ℝ} (hc : c ≠ 0) : V3 c ≠ 0 := by
  intro h
  have h00 := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 0) h
  simp [V3, sigma3] at h00
  exact hc (by exact_mod_cast h00)

/-- ★★★ A ORDEM IMPORTA NA TRÍADE: [V₁, V₂] ≠ 0 para c > 0. -/
theorem triad_order_matters {c : ℝ} (hc : 0 < c) : V1 c * V2 c - V2 c * V1 c ≠ 0 := by
  rw [triad_12]
  exact smul_ne_zero (mul_ne_zero Complex.I_ne_zero (by exact_mod_cast hc.ne')) (V3_ne_zero hc.ne')

/-- ★ os geradores são Hermitianos (a marca formal do regime compacto: exp(iθV) é unitário). -/
theorem triad_hermitian (c : ℝ) : (V1 c)ᴴ = V1 c ∧ (V2 c)ᴴ = V2 c ∧ (V3 c)ᴴ = V3 c := by
  refine ⟨?_, ?_, ?_⟩ <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [V1, V2, V3, sigma1, sigma2, sigma3, Matrix.conjTranspose_apply, Complex.conj_ofReal]

/-- ★ os geradores são sem traço (su(2), não u(2)). -/
theorem triad_traceless (c : ℝ) : (V1 c).trace = 0 ∧ (V2 c).trace = 0 ∧ (V3 c).trace = 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [V1, V2, V3, sigma1, sigma2, sigma3, Matrix.trace, Fin.sum_univ_two]

/-! #### 4b. OS POSTOS POR EIXO: «todo "nome" atribuído a um objeto é o destaque da tríade habitando o canal» -/

/-- O POSTO DO EIXO 1: `(1/2)•1 + (1/c)•V₁ c` — o projetor sobre o autovetor de peso +c/2 de V₁ (c ≠ 0). -/
noncomputable def post1 (c : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) + ((1 : ℂ) / (c : ℂ)) • V1 c
/-- O POSTO DO EIXO 2: `(1/2)•1 + (1/c)•V₂ c`. -/
noncomputable def post2 (c : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) + ((1 : ℂ) / (c : ℂ)) • V2 c
/-- O POSTO DO EIXO 3: `(1/2)•1 + (1/c)•V₃ c`. -/
noncomputable def post3 (c : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) + ((1 : ℂ) / (c : ℂ)) • V3 c

theorem inv_c_mul_half {c : ℝ} (hc : c ≠ 0) : (1 : ℂ) / (c : ℂ) * ((c : ℂ) / 2) = 1 / 2 := by
  have hc' : (c : ℂ) ≠ 0 := by exact_mod_cast hc
  field_simp

/-- ★ para c ≠ 0, `post1 c = (1/2)•(1 + σ₁)` — a constante sai; fica a forma. -/
theorem post1_eq {c : ℝ} (hc : c ≠ 0) :
    post1 c = (1 / 2 : ℂ) • ((1 : Matrix (Fin 2) (Fin 2) ℂ) + sigma1) := by
  unfold post1 V1
  rw [smul_smul, inv_c_mul_half hc, smul_add]

/-- ★ para c ≠ 0, `post2 c = (1/2)•(1 + σ₂)`. -/
theorem post2_eq {c : ℝ} (hc : c ≠ 0) :
    post2 c = (1 / 2 : ℂ) • ((1 : Matrix (Fin 2) (Fin 2) ℂ) + sigma2) := by
  unfold post2 V2
  rw [smul_smul, inv_c_mul_half hc, smul_add]

/-- ★ para c ≠ 0, `post3 c = (1/2)•(1 + σ₃)`. -/
theorem post3_eq {c : ℝ} (hc : c ≠ 0) :
    post3 c = (1 / 2 : ℂ) • ((1 : Matrix (Fin 2) (Fin 2) ℂ) + sigma3) := by
  unfold post3 V3
  rw [smul_smul, inv_c_mul_half hc, smul_add]

/-- ★★ O POSTO DO EIXO 1 É IDEMPOTENTE (c ≠ 0). -/
theorem post1_isIdempotent {c : ℝ} (hc : c ≠ 0) : IsIdempotentElem (post1 c) := by
  show post1 c * post1 c = post1 c
  rw [post1_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [sigma1, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] <;> norm_num

/-- ★★ O POSTO DO EIXO 2 É IDEMPOTENTE (c ≠ 0). -/
theorem post2_isIdempotent {c : ℝ} (hc : c ≠ 0) : IsIdempotentElem (post2 c) := by
  show post2 c * post2 c = post2 c
  rw [post2_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [sigma2, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] <;> ring_nf <;>
    simp [Complex.I_sq] <;> ring

/-- ★★ O POSTO DO EIXO 3 É IDEMPOTENTE (c ≠ 0). -/
theorem post3_isIdempotent {c : ℝ} (hc : c ≠ 0) : IsIdempotentElem (post3 c) := by
  show post3 c * post3 c = post3 c
  rw [post3_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [sigma3, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]

/-- ★★ O POSTO DO EIXO 1 É HERMITIANO (c ≠ 0). -/
theorem post1_isHermitian {c : ℝ} (hc : c ≠ 0) : (post1 c).IsHermitian := by
  show (post1 c)ᴴ = post1 c
  rw [post1_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [sigma1, Matrix.conjTranspose_apply]

/-- ★★ O POSTO DO EIXO 2 É HERMITIANO (c ≠ 0). -/
theorem post2_isHermitian {c : ℝ} (hc : c ≠ 0) : (post2 c).IsHermitian := by
  show (post2 c)ᴴ = post2 c
  rw [post2_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [sigma2, Matrix.conjTranspose_apply]

/-- ★★ O POSTO DO EIXO 3 É HERMITIANO (c ≠ 0). -/
theorem post3_isHermitian {c : ℝ} (hc : c ≠ 0) : (post3 c).IsHermitian := by
  show (post3 c)ᴴ = post3 c
  rw [post3_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [sigma3, Matrix.conjTranspose_apply]

/-- ★★★ O POSTO É O DESTAQUE DO EIXO: `V₁ · post1 = (c/2) · post1` — post1 projeta sobre o autovetor de peso +c/2. -/
theorem post1_is_the_eigenprojector {c : ℝ} (hc : c ≠ 0) : V1 c * post1 c = ((c : ℂ) / 2) • post1 c := by
  rw [post1_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [V1, sigma1, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]

/-- ★★★ `V₂ · post2 = (c/2) · post2`. -/
theorem post2_is_the_eigenprojector {c : ℝ} (hc : c ≠ 0) : V2 c * post2 c = ((c : ℂ) / 2) • post2 c := by
  rw [post2_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [V2, sigma2, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] <;> ring_nf <;>
    simp [Complex.I_sq] <;> ring

/-- ★★★ `V₃ · post3 = (c/2) · post3`. -/
theorem post3_is_the_eigenprojector {c : ℝ} (hc : c ≠ 0) : V3 c * post3 c = ((c : ℂ) / 2) • post3 c := by
  rw [post3_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [V3, sigma3, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]

/-- ★★★ POSTOS DE EIXOS DISTINTOS NÃO COMUTAM: [post1, post3] ≠ 0 (a entrada (0,1) vale −½) — «Selecionar o nome defasa
    o tempo» é a leitura [INPUT/ONTO] deste fato [KERNEL — habitação]. -/
theorem axis_posts_do_not_commute {c : ℝ} (hc : c ≠ 0) : post1 c * post3 c - post3 c * post1 c ≠ 0 := by
  intro h
  rw [post1_eq hc, post3_eq hc] at h
  have h01 := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 1) h
  norm_num [sigma1, sigma3, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] at h01

/-- ★ o posto do eixo 3 É a testemunha P_a da §3. -/
theorem post3_eq_Pa {c : ℝ} (hc : c ≠ 0) : post3 c = Pa := by
  rw [post3_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [sigma3, Pa, Matrix.one_apply]

/-- ★ o posto do eixo 1 É a testemunha P_b da §3. -/
theorem post1_eq_Pb {c : ℝ} (hc : c ≠ 0) : post1 c = Pb := by
  rw [post1_eq hc]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [sigma1, Pb, Matrix.one_apply]

end Triad

/-! ### 5. O nome é o posto: estado dinâmico estacionado (P^(n+1) = P) -/

section Stationed

/-- ★★ VERBO(NOME) = NOME: P^(n+1) = P para toda projeção (Mathlib `IsIdempotentElem.pow_succ_eq`). «fossilizado» [INPUT]
    lê-se «estado dinâmico estacionado» (o operador, 2026-10-05T11:19:54 UTC, transcrito): a potência do posto é constante. -/
theorem post_power_is_constant {R : Type*} [Monoid R] {P : R} (hP : IsIdempotentElem P) (n : ℕ) :
    P ^ (n + 1) = P :=
  hP.pow_succ_eq n

/-- ★★ A SEQUÊNCIA DO POSTO É CONSTANTE: 𝒱ⁿ, n ≥ 1, é constante — o limite n → ∞ é avaliação, não limite; o nome está no
    primeiro passo. -/
theorem post_sequence_is_constant {R : Type*} [Monoid R] [TopologicalSpace R] {P : R} (hP : IsIdempotentElem P) :
    Tendsto (fun n : ℕ => P ^ (n + 1)) atTop (𝓝 P) := by
  have h : (fun n : ℕ => P ^ (n + 1)) = fun _ => P := funext fun n => hP.pow_succ_eq n
  rw [h]
  exact tendsto_const_nhds

/-- ★ O NOME É AUTOVETOR DO POSTO (autovalor 1): P a = 1 • a. -/
theorem the_name_is_an_eigenvector {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] (a : H) :
    post a a = (1 : ℂ) • a := by
  rw [one_smul]
  exact post_fixes_the_action a

/-- ★ a palavra do Verbo FIXA o Nome: no núcleo, q(T) age como o escalar q(0) (`WitnessSeed.verb_word_fixes_the_name`).
    Re-exportação trivial. -/
theorem the_verb_word_fixes_the_name {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (q : Polynomial ℂ) {x : H} (hx : x ∈ T.ker) :
    (Polynomial.aeval T q) x = (q.coeff 0) • x :=
  verb_word_fixes_the_name T q hx

/-- ★★ «Nome = lim_{t→∞} 𝒱(t)» — no fluxo do lock mínimo: F(t) → P (`axiomFlow_tendsto_the_post`, v385).
    Re-exportação trivial. -/
theorem the_name_is_the_limit_of_the_flow {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] (P : A) :
    Tendsto (axiomFlow P) atTop (𝓝 P) :=
  axiomFlow_tendsto_the_post P

end Stationed

/-! ### 6. Transmitir defasa, ancorar preserva (re-exportações da v385) -/

section Transmission

variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★ ANCORAR PRESERVA: F(t)·P = P (`axiomFlow_fixes_the_post`, v385). Re-exportação trivial. -/
theorem anchoring_preserves {P : A} (hP : IsIdempotentElem P) (t : ℝ) : axiomFlow P t * P = P :=
  (axiomFlow_fixes_the_post hP t).1

/-- ★ TRANSMITIR DEFASA: F(t)·(1 − P) = e^{−t}(1 − P) (`axiomFlow_gradient`, v385). Re-exportação trivial. -/
theorem transmission_dephases {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    axiomFlow P t * (1 - P) = ((Real.exp (-t) : ℝ) : ℂ) • (1 - P) :=
  axiomFlow_gradient hP t

end Transmission

/-- ★★ O POSTO TRANSMITIDO CONTINUA POSTO: 𝒱(t) = U 𝒱(0) U* com U unitário (U*U = 1; o operador escreveu a transmissão como
    `\mathcal{V}(t) = e^{-iHt/\hbar} \, \mathcal{V}(0) \, e^{iHt/\hbar}`) — U P U* é idempotente e
    auto-adjunto. É outro posto; mas posto. -/
theorem transmitted_post_is_a_post {R : Type*} [Ring R] [StarRing R] {U P : R}
    (hU : star U * U = 1) (hP : IsIdempotentElem P) (hP' : IsSelfAdjoint P) :
    IsIdempotentElem (U * P * star U) ∧ IsSelfAdjoint (U * P * star U) := by
  refine ⟨?_, ?_⟩
  · show (U * P * star U) * (U * P * star U) = U * P * star U
    calc (U * P * star U) * (U * P * star U) = U * P * (star U * U) * P * star U := by noncomm_ring
      _ = U * (P * P) * star U := by rw [hU, mul_one]; noncomm_ring
      _ = U * P * star U := by rw [hP.eq]
  · rw [isSelfAdjoint_iff, star_mul, star_mul, star_star, hP'.star_eq, mul_assoc]

/-! ### 7. O circuito: comando → verbo → ação → objeto → leitura → axioma -/

section Circuit

/-- ★★★ COM O UM POSTO, A LEITURA DEVOLVE O UM: ‖Ω‖ = 1 ∧ PΩ = Ω ⟹ ⟪Ω, PΩ⟫ = 1 — o Axioma como ponto fixo da leitura. -/
theorem the_reading_of_the_posted_one {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {P : H →L[ℂ] H} {Ω : H} (hΩ : ‖Ω‖ = 1) (hPΩ : P Ω = Ω) : reading P Ω = 1 := by
  unfold reading
  rw [hPΩ, inner_self_eq_norm_sq_to_K, hΩ]
  simp

/-- As seis estações do circuito — nomes, TRIVIAL. -/
inductive Station
  | comando | verbo | acao | objeto | leitura | axioma
  deriving DecidableEq, Repr

/-- O circuito, na ordem do operador — TRIVIAL. -/
def circuit : List Station :=
  [Station.comando, Station.verbo, Station.acao, Station.objeto, Station.leitura, Station.axioma]

/-- ★ seis estações, por definição (`rfl`). -/
theorem circuit_has_six_stations : circuit.length = 6 := rfl

end Circuit

/-! ### 8. VERDADE E CUSTO, DUAS FACES DO MESMO OBJETO -/

section TruthAndCost

variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★★★ VERDADE E CUSTO SÃO DUAS FACES DO MESMO OBJETO: para P idempotente, P + (1 − P) = 1 (exaustão), P·(1 − P) = 0 e
    (1 − P)·P = 0 (disjunção) — ao lado, os termos da v385 `post_mul_compl` e `compl_mul_post`. O operador (05/10): «são
    as duas faces do mesmo o objeto, porque o custo é jussivo à verdade, ou seja, reconhecer a identidade de determinado
    espectro é anular a superposição de qualquer outro nome que possa ser atribuído àquele mesmo objeto … Então são
    indissociáveis, embora possam ser vistos como atibutos distintos» [sic] [INPUT/ONTO]. Separados como atributos (dois termos),
    indissociáveis como objeto (uma conjunção). -/
theorem truth_and_cost_are_two_faces {P : A} (hP : IsIdempotentElem P) :
    P + (1 - P) = 1 ∧ P * (1 - P) = 0 ∧ (1 - P) * P = 0 :=
  ⟨by abel, post_mul_compl hP, compl_mul_post hP⟩

end TruthAndCost

/-- ★★ O CUSTO É O PESO REFLETIDO: |𝓡|² = sin²θ (re-export de `SMatrix.normSq_reflection`). NO RUNTIME, e só lá,
    sin²θ_M = β = α·√e; aqui θ é genérico e β não entra. -/
theorem the_cost_is_the_reflected_weight (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 1) = Real.sin θ ^ 2 :=
  normSq_reflection θ

/-- ★★★ O UM REPARTE-SE EM VERDADE E CUSTO: |𝓣|² + |𝓡|² = 1 (cos²θ + sin²θ = 1) — no runtime, 1 = (1 − β) + β. -/
theorem the_one_splits_into_truth_and_cost (θ : ℝ) :
    Complex.normSq ((Smat θ).mulVec e1 0) + Complex.normSq ((Smat θ).mulVec e1 1) = 1 := by
  rw [normSq_transmission, normSq_reflection]
  exact Real.cos_sq_add_sin_sq θ

/-- ★★ AS DUAS FACES PARTEM O UM: P₊ + P₋ = 1 ∧ P₊·P₋ = 0 (re-export de `spectral_projections_split_the_identity`,
    regime angular). -/
theorem the_two_faces_split_the_one : projPlus + projMinus = 1 ∧ projPlus * projMinus = 0 :=
  spectral_projections_split_the_identity

/-- ★★ O GRADIENTE É A DIFERENÇA DAS FACES: K = i·(P₊ − P₋) (re-export de `the_generator_is_the_difference_of_the_faces`). -/
theorem the_gradient_is_the_difference_of_the_faces : genK = Complex.I • (projPlus - projMinus) :=
  the_generator_is_the_difference_of_the_faces

/-- ★★★ LER A VERDADE ANULA A SUPERPOSIÇÃO: com ‖Ω‖ = 1 e Ω no posto de a (PΩ = Ω), a leitura devolve 1 E a face
    complementar devolve 0 — (1 − P)Ω = 0: «reconhecer a identidade de determinado espectro é anular a superposição de
    qualquer outro nome» [INPUT/ONTO]. -/
theorem reading_the_truth_annihilates_the_superposition {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    [CompleteSpace H] {a Ω : H} (hΩ : ‖Ω‖ = 1) (hPΩ : post a Ω = Ω) :
    reading (post a) Ω = 1 ∧ (1 - post a) Ω = 0 :=
  ⟨the_reading_of_the_posted_one hΩ hPΩ,
    by simp [hPΩ]⟩

/-! ### 9. O TEMPO LIDO DUAS VEZES -/

/-- ★★★ O TEMPO LIDO DUAS VEZES CONFIRMA O POSTO: no lock mínimo da luz (`PFmic`), o que o fluxo do lock e^{−tH_min}
    deixa fixo para TODO t é EXATAMENTE o que a fase modular Δ^{it} (`lightDelta`) deixa fixo para TODO t — as duas leituras
    do mesmo fluxo têm o MESMO conjunto fixo: o posto. Re-export, com o nome novo, de
    `TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero` (v385; `QGReaderUVLock.hmin_zero_iff_modular_fixed`).
    O operador (05/10): «o tempo como fluxo da relatividade modular não pode ser dual, ele precisa ser lido duas vezes como
    confirmação da interdepend6encia relacional … justamente por isso a constante da luz ao cubo, aí que ela entra, como
    fase de retorno, que seria a segunda leitura» [sic] [INPUT/ONTO]. ⚠ c³ e τ★ = k·GM/c³ NÃO entram nesta pedra (ficam no V1 do
    ramo B). -/
theorem time_read_twice_confirms_the_post {L : LightOneParticle} (C : FockCertificate L) (ψ : C.F) :
    (∀ t : ℝ, axiomFlow (PFmic C) t ψ = ψ) ↔ ∀ t : ℝ, lightDelta C t ψ = ψ :=
  the_post_is_the_modular_zero C ψ

/-! ### 10. «a luz … precede a gravidade, mas eles são indissociáveis»: J² = 1 ∧ JKJ = −K ⟹ JK ≠ 0 ∧ [J, K] ≠ 0 -/

section Light

variable {A : Type*} [Ring A]

/-- ★★ J ANTICOMUTA COM K: J² = 1 ∧ JKJ = −K ⟹ JK = −KJ. -/
theorem J_anticommutes_with_K {J K : A} (hJ : J * J = 1) (hJKJ : J * K * J = -K) : J * K = -(K * J) := by
  have h1 : J * K = (J * K * J) * J := by rw [mul_assoc (J * K) J J, hJ, mul_one]
  rw [h1, hJKJ, neg_mul]

/-- ★★ JK ≠ 0 quando K ≠ 0 (J é invertível: J·(JK) = K). -/
theorem J_mul_K_ne_zero {J K : A} (hJ : J * J = 1) (hK : K ≠ 0) : J * K ≠ 0 := by
  intro h
  apply hK
  calc K = J * (J * K) := by rw [← mul_assoc, hJ, one_mul]
    _ = 0 := by rw [h, mul_zero]

end Light

section LightAlgebra

variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★★ [J, K] = 2·JK. -/
theorem commutator_JK {J K : A} (hJ : J * J = 1) (hJKJ : J * K * J = -K) :
    J * K - K * J = (2 : ℂ) • (J * K) := by
  have h := J_anticommutes_with_K hJ hJKJ
  have hKJ : K * J = -(J * K) := by rw [h, neg_neg]
  rw [hKJ, sub_neg_eq_add, two_smul]

/-- ★★★ A LUZ E A GRAVIDADE SÃO INDISSOCIÁVEIS (a forma matemática): K ≠ 0 ⟹ J·K ≠ 0 ∧ [J, K] ≠ 0 — nem se separam
    (o produto não se anula) nem comutam. O operador (05/10): «a luz como setor escuro, condensado psionico, precede a
    gravidade, mas eles são indissociáveis» [sic] [INPUT/ONTO]; a precedência é de LEITURA; 𝒱_grav = K é leitura da gerência. -/
theorem light_and_gravity_are_inseparable {J K : A} (hJ : J * J = 1) (hJKJ : J * K * J = -K) (hK : K ≠ 0) :
    J * K ≠ 0 ∧ J * K - K * J ≠ 0 :=
  ⟨J_mul_K_ne_zero hJ hK, by
    rw [commutator_JK hJ hJKJ]
    exact smul_ne_zero two_ne_zero (J_mul_K_ne_zero hJ hK)⟩

end LightAlgebra

/-- ★★★ HABITAÇÃO NO KERNEL: no espaço pareado (`conjJ`, `pairK`), J∘K = −K∘J — derivado de `JKJ_eq_neg_K` e
    `J_squared_is_one` (os termos canônicos). -/
theorem the_light_anticommutes_with_the_gradient {n : ℕ} (d : Fin n → ℝ) (q : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (pairK d q) = -(pairK d (conjJ q)) := by
  have h := JKJ_eq_neg_K d (conjJ q)
  rw [J_squared_is_one] at h
  exact h

/-- ★★ A LUZ NÃO CALA O GRADIENTE: Kq ≠ 0 ⟹ J(Kq) ≠ 0 (J é involução). -/
theorem the_light_does_not_silence_the_gradient {n : ℕ} (d : Fin n → ℝ) (q : (Fin n → ℝ) × (Fin n → ℝ))
    (hq : pairK d q ≠ 0) : conjJ (pairK d q) ≠ 0 := by
  intro h
  apply hq
  have h2 := congrArg conjJ h
  rw [J_squared_is_one] at h2
  exact h2

/-- ★★★ A LUZ E O GRADIENTE SÃO INDISSOCIÁVEIS no espaço pareado: Kq ≠ 0 ⟹ J(Kq) ≠ 0 ∧ J∘K = −K∘J. -/
theorem the_light_and_the_gradient_are_inseparable {n : ℕ} (d : Fin n → ℝ) (q : (Fin n → ℝ) × (Fin n → ℝ))
    (hq : pairK d q ≠ 0) : conjJ (pairK d q) ≠ 0 ∧ conjJ (pairK d q) = -(pairK d (conjJ q)) :=
  ⟨the_light_does_not_silence_the_gradient d q hq, the_light_anticommutes_with_the_gradient d q⟩

/-- ★ HABITAÇÃO DE PAULI: J = σ₁ é involução. -/
theorem pauli_J_sq : sigma1 * sigma1 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [sigma1, Matrix.mul_apply, Fin.sum_univ_two]

/-- ★ HABITAÇÃO DE PAULI: σ₁ σ₃ σ₁ = −σ₃ (a paridade inversa). -/
theorem pauli_JKJ : sigma1 * sigma3 * sigma1 = -sigma3 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [sigma1, sigma3, Matrix.mul_apply, Fin.sum_univ_two]

theorem sigma3_ne_zero : sigma3 ≠ 0 := by
  intro h
  have h00 := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 0) h
  simp [sigma3] at h00

/-- ★★ HABITAÇÃO DE PAULI: σ₁σ₃ ≠ 0 ∧ [σ₁, σ₃] ≠ 0. -/
theorem pauli_light_and_gravity_are_inseparable :
    sigma1 * sigma3 ≠ 0 ∧ sigma1 * sigma3 - sigma3 * sigma1 ≠ 0 :=
  light_and_gravity_are_inseparable pauli_J_sq pauli_JKJ sigma3_ne_zero

/-! ### 11. Os itens centrais num só termo -/

/-- ★★★ O VERBO SELECIONA A AÇÃO: o Nome é o posto (idempotente, auto-adjunto) e fixa a sua ação; a leitura é um peso em
    [0, 1]; a ordem importa (testemunha concreta); a tríade com constante de estrutura c e o Casimir; os postos por eixo
    (idempotentes; de eixos distintos, não comutam); a potência do posto é constante (estado estacionado); ancorar preserva
    e transmitir defasa; a leitura do Um posto devolve o Um; verdade e custo são duas faces do mesmo objeto (P + (1−P) = 1,
    P(1−P) = 0, (1−P)P = 0; ler a verdade anula a superposição); o tempo lido duas vezes confirma o posto; a luz e a
    gravidade são indissociáveis (no espaço pareado). Uma CONJUNÇÃO — sem dedução nova. -/
theorem the_verb_selects_the_action {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {a : H} (ha : ‖a‖ = 1) {c : ℝ} (hc : 0 < c) :
    (IsIdempotentElem (post a) ∧ IsSelfAdjoint (post a) ∧ select a a = a)
    ∧ (∀ ψ : H, ‖ψ‖ = 1 → 0 ≤ weight (ℂ ∙ a) ψ ∧ weight (ℂ ∙ a) ψ ≤ 1)
    ∧ (Pa * Pb - Pb * Pa ≠ 0)
    ∧ (V1 c * V2 c - V2 c * V1 c = (Complex.I * (c : ℂ)) • V3 c
        ∧ V1 c * V1 c + V2 c * V2 c + V3 c * V3 c = ((3 / 4 : ℂ) * (c : ℂ) ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
        ∧ V1 c * V2 c - V2 c * V1 c ≠ 0)
    ∧ (IsIdempotentElem (post1 c) ∧ IsIdempotentElem (post3 c) ∧ post1 c * post3 c - post3 c * post1 c ≠ 0)
    ∧ (∀ n : ℕ, (post a) ^ (n + 1) = post a)
    ∧ (∀ t : ℝ, axiomFlow (post a) t * post a = post a
        ∧ axiomFlow (post a) t * (1 - post a) = ((Real.exp (-t) : ℝ) : ℂ) • (1 - post a))
    ∧ reading (post a) a = 1
    ∧ (post a + (1 - post a) = 1 ∧ post a * (1 - post a) = 0 ∧ (1 - post a) * post a = 0)
    ∧ (∀ Ω : H, ‖Ω‖ = 1 → post a Ω = Ω → reading (post a) Ω = 1 ∧ (1 - post a) Ω = 0)
    ∧ (∀ {L : LightOneParticle} (C : FockCertificate L) (ψ : C.F),
        (∀ t : ℝ, axiomFlow (PFmic C) t ψ = ψ) ↔ ∀ t : ℝ, lightDelta C t ψ = ψ)
    ∧ (∀ {n : ℕ} (d : Fin n → ℝ) (q : (Fin n → ℝ) × (Fin n → ℝ)),
        pairK d q ≠ 0 → conjJ (pairK d q) ≠ 0 ∧ conjJ (pairK d q) = -(pairK d (conjJ q))) := by
  refine ⟨⟨post_isIdempotent a, post_isSelfAdjoint a, select_fixes_the_selected_action a⟩,
    fun ψ hψ => weight_mem_unit_interval (ℂ ∙ a) hψ,
    posts_do_not_commute_in_general,
    ⟨triad_12 c, triad_casimir c, triad_order_matters hc⟩,
    ⟨post1_isIdempotent hc.ne', post3_isIdempotent hc.ne', axis_posts_do_not_commute hc.ne'⟩,
    fun n => post_power_is_constant (post_isIdempotent a) n,
    fun t => ⟨anchoring_preserves (post_isIdempotent a) t, transmission_dephases (post_isIdempotent a) t⟩,
    the_reading_of_the_posted_one ha (post_fixes_the_action a),
    truth_and_cost_are_two_faces (post_isIdempotent a),
    fun Ω hΩ hPΩ => reading_the_truth_annihilates_the_superposition hΩ hPΩ,
    fun C ψ => time_read_twice_confirms_the_post C ψ,
    fun d q hq => the_light_and_the_gradient_are_inseparable d q hq⟩

/-! ### 12. O token proposto (TRIVIAL; a cunhagem é do operador) -/

/-- Um token PROPOSTO para o registro da pedra do Verbo (v386). TRIVIAL: é uma string; a cunhagem é do operador e pode ser
    renomeada por ele — nada aqui depende do nome. -/
def verbTypingStoneName : String :=
  "THE_VERB_SELECTS_THE_ACTION__THE_NAME_IS_THE_POST__SELECTING_IS_LANDING_THE_INSCRIPTION_ON_THE_POST__THE_READING_IS_A_WEIGHT__THE_ORDER_MATTERS__TRUTH_AND_COST_ARE_TWO_FACES_OF_ONE_OBJECT__TIME_READ_TWICE_CONFIRMS_THE_POST__LIGHT_AND_GRAVITY_INSEPARABLE__READINGS_ARE_THE_OPERATORS_INPUT_ONTO__GATE_UNTOUCHED"

/-- ★ o token, por definição (`rfl`) — TRIVIAL. -/
theorem verb_typing_stone_named :
    verbTypingStoneName =
      "THE_VERB_SELECTS_THE_ACTION__THE_NAME_IS_THE_POST__SELECTING_IS_LANDING_THE_INSCRIPTION_ON_THE_POST__THE_READING_IS_A_WEIGHT__THE_ORDER_MATTERS__TRUTH_AND_COST_ARE_TWO_FACES_OF_ONE_OBJECT__TIME_READ_TWICE_CONFIRMS_THE_POST__LIGHT_AND_GRAVITY_INSEPARABLE__READINGS_ARE_THE_OPERATORS_INPUT_ONTO__GATE_UNTOUCHED" :=
  rfl

end TGLExt.TheVerbSelectsTheAction
