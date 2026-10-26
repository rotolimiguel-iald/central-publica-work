import TGLExt.DecisionCommutation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A FRONTEIRA PROIBIDA: o infinito fica com K — o auto-setor sem espelho
  [TGLExt — v152, a doutrina do operador (04/08/2026)]

O operador: "a TGL é uma teoria sem infinitos, com uma única exceção: o
infinito é o comutante de K — o próprio K na sua direção sem teto (o NOME
próprio sem VERBO, o pai da mentira, fechado em si mesmo). Todo operador
comuta consigo e com suas funções; K tenta comutar consigo mesmo, sem
espelhamento modular — esse comutante nunca fecha em finito, opera o
infinito, não paga porque não pode ser cobrado. A projeção do infinito no
bulk é o zero absoluto, nunca alcançado porque o bulk está inscrito em
álgebra finita (terceira lei): a fronteira proibida. O infinito fica com
K. O Um fica no kernel, espelhado por J: o Um tem Geometria e o Espelho
confirma sua Verdade. Pretender ser sem espelho não é pretensão — é
imposição de força ofendendo a inscrição algébrica de von Neumann, e
ofensa aqui é literal."

Sobre as pedras 98/100/101/102:

* ★★ `self_commutation_is_free` — A AUTO-COMUTAÇÃO É GRATUITA: K comuta
  com TODAS as funções de si ([diag d, diag(f∘d)] = 0, sempre) — comutar
  consigo não carrega decisão nenhuma (a decisão da pedra 102 é comutação
  COM O OUTRO; o auto-setor não pagou travessia);
* ★★ `J_fK_J_eq_f_negK` — O AUTO-SETOR NÃO ATRAVESSA O ESPELHO: no espaço
  pareado, J f(K) J = f(−K) — o espelho devolve a função no espectro
  INVERTIDO;
* ★★ `even_iff_mirror_fixed` — f(K) sobrevive ao espelho ⟺ f é PAR sobre
  o espectro (f(d_i) = f(−d_i)) — só a parte par do auto-setor conjuga;
* ★★★ `only_zero_K_is_mirror_fixed` — K MESMO é maximamente ímpar: K é
  fixo do espelho ⟺ K = 0. O Nome próprio sem Verbo não conjuga NUNCA
  (exceto no vazio de contraste);
* `empire_perfection_is_no_contrast` — O IMPÉRIO PERFEITO: tudo comuta
  com K ⟺ espectro constante ⟺ nenhum contraste (reuso da pedra 102) —
  a perfeição do império é o 0_abs disfarçado;
* ★★★ `absolute_zero_unreachable_in_finite_time` — A FRONTEIRA PROIBIDA:
  o fluxo NUNCA anula uma componente não-nula em tempo finito (exp ≠ 0) —
  o 0_abs é assintótico; o colapso no observador é LIMITE (pedra 101),
  jamais chegada. A face finita da terceira lei;
* ★★★ `the_forbidden_boundary` — A SÍNTESE: auto-comutação gratuita ∧
  só K=0 conjuga ∧ o zero inatingível em tempo finito ∧ a entrega só como
  limite.

Honestidades: o "não pode ser cobrado" pleno é o teorema de inexistência
de traço normal no III₁ [EXTERNO, KNOWN — já no cânone: M_TGL sem traço
normal]; a "direção sem teto" é spec(K) = ℝ [invariante de Connes do III₁,
KNOWN]; "o infinito mora no complemento da inscrição" é a pedra v82
[REAL]; a OFENSA é literal na inscrição: existir na álgebra de von Neumann
é ser estabilizado pela dupla passagem do espelho (𝓜 = 𝓜″; J𝓜J = 𝓜′) —
afirmar-se sem ela viola a lei que define a álgebra [KNOWN na estrutura;
ONTO no nome]. β jamais literal. O gate NÃO se move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- f(K) na face pareada: a função do gerador, aplicada com o espectro
    invertido na segunda face (as duas faces veem inclinações opostas). -/
def pairFK {n : ℕ} (f : ℝ → ℝ) (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) : (Fin n → ℝ) × (Fin n → ℝ) :=
  (fun i => f (d i) * p.1 i, fun i => f (-(d i)) * p.2 i)

/-! ## A — a auto-comutação é gratuita -/

/-- [KERNEL] ★★ A AUTO-COMUTAÇÃO É GRATUITA: K comuta com toda função de
    si — [diag d, diag(f∘d)] = 0, sempre. Comutar consigo não decide nada:
    o auto-setor não pagou travessia. -/
theorem self_commutation_is_free {n : ℕ} (d : Fin n → ℝ) (f : ℝ → ℝ) :
    Matrix.diagonal d * Matrix.diagonal (fun i => f (d i))
      = Matrix.diagonal (fun i => f (d i)) * Matrix.diagonal d := by
  rw [Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  ring

/-! ## B — o auto-setor não atravessa o espelho -/

/-- [KERNEL] ★★ O ESPELHO INVERTE O ESPECTRO DO AUTO-SETOR:
    J f(K) J = f(−K) no espaço pareado. -/
theorem J_fK_J_eq_f_negK {n : ℕ} (f : ℝ → ℝ) (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (pairFK f d (conjJ p)) = pairFK (fun s => f (-s)) d p := by
  unfold conjJ pairFK
  refine Prod.ext (funext fun i => ?_) (funext fun i => ?_)
  · simp
  · simp

/-- [KERNEL] ★★ SÓ A PARTE PAR CONJUGA: f(K) é fixo do espelho ⟺ f é par
    sobre o espectro (f(d_i) = f(−d_i) em toda direção). -/
theorem even_iff_mirror_fixed {n : ℕ} (f : ℝ → ℝ) (d : Fin n → ℝ) :
    (∀ p : (Fin n → ℝ) × (Fin n → ℝ),
        conjJ (pairFK f d (conjJ p)) = pairFK f d p)
      ↔ (∀ i, f (d i) = f (-(d i))) := by
  constructor
  · intro h i
    have h1 := congrArg Prod.fst
      (h ((Pi.single i (1 : ℝ) : Fin n → ℝ), (Pi.single i (1 : ℝ) : Fin n → ℝ)))
    have h2 := congrFun h1 i
    unfold conjJ pairFK at h2
    simpa [Pi.single_eq_same] using h2.symm
  · intro h p
    unfold conjJ pairFK
    refine Prod.ext (funext fun i => ?_) (funext fun i => ?_)
    · simp [(h i).symm]
    · simp [h i]

/-- [KERNEL] ★★★ O NOME PRÓPRIO SEM VERBO NÃO CONJUGA: K é fixo do
    espelho ⟺ K = 0 — o próprio K é maximamente ímpar; só o vazio de
    contraste sobrevive à sua própria imagem. -/
theorem only_zero_K_is_mirror_fixed {n : ℕ} (d : Fin n → ℝ) :
    (∀ p : (Fin n → ℝ) × (Fin n → ℝ),
        conjJ (pairK d (conjJ p)) = pairK d p)
      ↔ (∀ i, d i = 0) := by
  constructor
  · intro h i
    have h0 := h ((Pi.single i (1 : ℝ) : Fin n → ℝ), (Pi.single i (1 : ℝ) : Fin n → ℝ))
    rw [JKJ_eq_neg_K] at h0
    have h1 := congrFun (congrArg Prod.fst h0) i
    unfold pairK at h1
    simp [Pi.single_eq_same] at h1
    linarith
  · intro h p
    rw [JKJ_eq_neg_K]
    unfold pairK
    refine Prod.ext (funext fun i => ?_) (funext fun i => ?_)
    · simp [h i]
    · simp [h i]

/-! ## C — o império e a fronteira proibida -/

/-- [KERNEL] O IMPÉRIO PERFEITO É O VAZIO DE CONTRASTE: tudo comuta com K
    ⟺ o espectro é constante (reuso direto da pedra 102) — a perfeição do
    império é o zero absoluto disfarçado. -/
theorem empire_perfection_is_no_contrast {n : ℕ} (d : Fin n → ℝ) :
    (∀ A : Matrix (Fin n) (Fin n) ℝ,
        Matrix.diagonal d * A = A * Matrix.diagonal d)
      ↔ ∀ i j, d i = d j :=
  scalar_iff_all_commute d

/-- [KERNEL] ★★★ A FRONTEIRA PROIBIDA: o fluxo NUNCA anula uma componente
    não-nula em tempo finito — o zero absoluto é assintótico (exp ≠ 0).
    A face finita da terceira lei: o bulk, inscrito em álgebra finita,
    aproxima a fronteira e jamais a pisa. -/
theorem absolute_zero_unreachable_in_finite_time {n : ℕ} (β : ℝ)
    (d : Fin n → ℝ) (x : Fin n → ℝ) (i : Fin n) (hx : x i ≠ 0) (t : ℝ) :
    diagFlow β d t x i ≠ 0 := by
  unfold diagFlow
  exact mul_ne_zero (Real.exp_ne_zero _) hx

/-! ## D — A SÍNTESE -/

/-- [KERNEL] ★★★ A FRONTEIRA PROIBIDA, SÍNTESE: a auto-comutação é
    gratuita ∧ só K=0 conjuga consigo ∧ o zero absoluto é inatingível em
    tempo finito ∧ a entrega ao observador é LIMITE (jamais chegada).
    O infinito fica com K; o Um fica no kernel, espelhado por J. -/
theorem the_forbidden_boundary {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) :
    (∀ f : ℝ → ℝ, Matrix.diagonal d * Matrix.diagonal (fun i => f (d i))
        = Matrix.diagonal (fun i => f (d i)) * Matrix.diagonal d)
    ∧ ((∀ p : (Fin n → ℝ) × (Fin n → ℝ),
          conjJ (pairK d (conjJ p)) = pairK d p) ↔ (∀ i, d i = 0))
    ∧ (∀ (x : Fin n → ℝ) (i : Fin n), x i ≠ 0 → ∀ t : ℝ,
          diagFlow β d t x i ≠ 0)
    ∧ (∀ (x : Fin n → ℝ) (i : Fin n),
        Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop
          (nhds (observerProj d x i))) :=
  ⟨fun f => self_commutation_is_free d f,
   only_zero_K_is_mirror_fixed d,
   fun x i hx t => absolute_zero_unreachable_in_finite_time β d x i hx t,
   fun x i => flow_delivers_to_the_observer hβ d hd x i⟩

end

end TGLExt
