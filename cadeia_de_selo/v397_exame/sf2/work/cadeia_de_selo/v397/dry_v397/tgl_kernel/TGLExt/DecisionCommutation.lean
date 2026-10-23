import TGLExt.ConjugateAct

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A DECISÃO É COMUTAÇÃO: K é o que ainda não comuta — e K = −∇𝓕 verificado
  [TGLExt — v146, a doutrina do operador (03/08/2026)]

O operador: "K não decide a travessia, porque a decisão é comutação e K não
comuta — K é tudo aquilo que não comuta, o espectro do gradiente negativo.
[K,A]=0 ⟺ decisão realizada; [K,A]≠0 ⟺ contraste, resistência à inscrição.
K não é o veredito; é a inclinação que ainda exige movimento. K=0 ⟹ nenhum
contraste dinâmico interno. J espelha, K inclina, a comutação decide, o
observador lê."

Três seções, SOBRE as pedras 98/100/101:

## I — a comutação como decisão (a face de matrizes)
* ★★ `commutator_entry` — A IDENTIDADE EXATA: [diag d, A]_{ij} =
  (d_i − d_j)·A_{ij} — o comutador é pesado pelos GAPS do espectro: cada
  entrada fora do bloco carrega o seu próprio contraste;
* ★★ `decided_iff_block` — A DECISÃO: [K,A] = 0 ⟺ A não liga níveis
  distintos do gradiente — o setor decidido é o bloco-diagonal (os níveis
  não se falam);
* ★★ `scalar_iff_all_commute` — K SEM CONTRASTE: tudo comuta com K ⟺ o
  espectro é constante (K escalar) — "K=0 ⟹ nenhum contraste interno";
  controle CONSTRUTIVO: havendo gap, a matriz de uma entrada já não comuta;
* `decided_is_subalgebra` — O VEREDITO FECHA: o setor decidido é fechado
  sob produto — o centralizador finito ("o traço emerge no centralizador");

## II — o espelho e a decisão
* ★★ `JKJ_eq_neg_K` — A PARIDADE INVERSA EM ATO: no espaço pareado da
  pedra 101, J K J = −K — o espelho vê a inclinação invertida (a paridade
  óptico-modular; a face finita da pedra do zero modular);
* ★★ `decided_sector_is_J_stable` — A DECISÃO SOBREVIVE AO ESPELHO: o
  setor onde K se anula é levado em si mesmo por J — a travessia não
  desfaz vereditos;

## III — K = −∇𝓕, o estatuto duplo VERIFICADO (a face finita REAL)
* ★★★ `gradient_first_variation` — O GRADIENTE É O GERADOR: a variação
  primeira de 𝓕(x) = ½Σ βd_i x_i² é EXATAMENTE ⟨βd·x, v⟩ — ∇𝓕(x) = βd·x,
  a ação de K; identidade algébrica exata, sem resto além de h²;
* ★★★ `flow_solves_gradient_ode` — O FLUXO RESOLVE ẏ = −∇𝓕(y): a derivada
  do transporte diagonal em todo t é −(βd_i)·(fluxo) — HasDerivAt, cálculo
  real, componente a componente;
* ★★★ `lyapunov_decreases` — SPOHN FINITO: 𝓕 desce ao longo do fluxo
  (monótona não-crescente) — o funcional de contraste é Lyapunov;
* ★★★ `K_equals_neg_gradient_verified` — A SÍNTESE: variação ∧ EDO ∧
  Lyapunov — a identidade K = −∇𝓕 fechada na face finita, nas três provas
  que ela pede.

Honestidades: a identidade K = −∇𝓕 é aqui VERIFICADA na face finita
(quadrática, classe com balanço detalhado); o caso GKLS genuíno é
gradiente-de-fluxo da entropia relativa [KNOWN: Spohn; Carlen–Maas] e
segue EXTERNO; "decisão" = conservação-sob-o-fluxo ([K,A]=0), nenhum
postulado de medição entra; a ressonância com einselection é registrada
no módulo — aqui K é o gerador modular da fronteira, não um ambiente.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## I — a comutação como decisão -/

/-- [KERNEL] ★★ A IDENTIDADE EXATA: o comutador com K = diag d é pesado
    pelos gaps do espectro — [K,A]_{ij} = (d_i − d_j)·A_{ij}. K não
    escolhe: K pesa o contraste. -/
theorem commutator_entry {n : ℕ} (d : Fin n → ℝ)
    (A : Matrix (Fin n) (Fin n) ℝ) (i j : Fin n) :
    (Matrix.diagonal d * A - A * Matrix.diagonal d) i j
      = (d i - d j) * A i j := by
  simp only [Matrix.sub_apply, Matrix.diagonal_mul, Matrix.mul_diagonal]
  ring

/-- [KERNEL] ★★ A DECISÃO É COMUTAÇÃO: [K,A] = 0 ⟺ A não liga níveis
    distintos do gradiente. O setor decidido é o bloco-diagonal — os
    níveis do espectro não se falam. -/
theorem decided_iff_block {n : ℕ} (d : Fin n → ℝ)
    (A : Matrix (Fin n) (Fin n) ℝ) :
    Matrix.diagonal d * A = A * Matrix.diagonal d
      ↔ ∀ i j, d i ≠ d j → A i j = 0 := by
  constructor
  · intro h i j hij
    have he : d i * A i j = A i j * d j := by
      have := (Matrix.ext_iff.mpr h) i j
      simpa [Matrix.diagonal_mul, Matrix.mul_diagonal] using this
    have h2 : (d i - d j) * A i j = 0 := by
      rw [sub_mul, he]
      ring
    rcases mul_eq_zero.mp h2 with h3 | h3
    · exact absurd (sub_eq_zero.mp h3) hij
    · exact h3
  · intro h
    ext i j
    simp only [Matrix.diagonal_mul, Matrix.mul_diagonal]
    by_cases hij : d i = d j
    · rw [hij]
      ring
    · rw [h i j hij]
      ring

/-- [KERNEL] ★★ K SEM CONTRASTE: tudo comuta com K ⟺ o espectro é
    constante. "K = 0 ⟹ nenhum contraste dinâmico interno" — e o controle
    é construtivo: havendo um gap, a matriz de uma entrada já não comuta. -/
theorem scalar_iff_all_commute {n : ℕ} (d : Fin n → ℝ) :
    (∀ A : Matrix (Fin n) (Fin n) ℝ,
        Matrix.diagonal d * A = A * Matrix.diagonal d)
      ↔ ∀ i j, d i = d j := by
  constructor
  · intro h i j
    by_contra hij
    have hA := (decided_iff_block d
      (Matrix.of fun k l => if k = i ∧ l = j then (1 : ℝ) else 0)).mp
      (h _) i j hij
    simp [Matrix.of_apply] at hA
  · intro h A
    ext i j
    simp only [Matrix.diagonal_mul, Matrix.mul_diagonal, h i j]
    ring

/-- [KERNEL] O VEREDITO FECHA: o setor decidido é fechado sob produto —
    o centralizador finito. "O traço emerge no centralizador." -/
theorem decided_is_subalgebra {n : ℕ} (d : Fin n → ℝ)
    (A B : Matrix (Fin n) (Fin n) ℝ)
    (hA : Matrix.diagonal d * A = A * Matrix.diagonal d)
    (hB : Matrix.diagonal d * B = B * Matrix.diagonal d) :
    Matrix.diagonal d * (A * B) = (A * B) * Matrix.diagonal d := by
  calc Matrix.diagonal d * (A * B)
      = (Matrix.diagonal d * A) * B := by rw [Matrix.mul_assoc]
    _ = (A * Matrix.diagonal d) * B := by rw [hA]
    _ = A * (Matrix.diagonal d * B) := by rw [Matrix.mul_assoc]
    _ = A * (B * Matrix.diagonal d) := by rw [hB]
    _ = (A * B) * Matrix.diagonal d := by rw [Matrix.mul_assoc]

/-! ## II — o espelho e a decisão -/

/-- K no espaço pareado da pedra 101: as duas faces veem inclinações
    INVERTIDAS (a paridade óptico-modular). -/
def pairK {n : ℕ} (d : Fin n → ℝ) (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    (Fin n → ℝ) × (Fin n → ℝ) :=
  (fun i => d i * p.1 i, fun i => -(d i * p.2 i))

/-- [KERNEL] ★★ A PARIDADE INVERSA EM ATO: J K J = −K no espaço pareado —
    o espelho vê a inclinação invertida. -/
theorem JKJ_eq_neg_K {n : ℕ} (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (pairK d (conjJ p)) = -(pairK d p) := by
  unfold conjJ pairK
  refine Prod.ext (funext fun i => rfl) (funext fun i => by simp)

/-- [KERNEL] ★★ A DECISÃO SOBREVIVE AO ESPELHO: onde K se anula, K também
    se anula do outro lado do espelho — a travessia não desfaz vereditos. -/
theorem decided_sector_is_J_stable {n : ℕ} (d : Fin n → ℝ)
    (p : (Fin n → ℝ) × (Fin n → ℝ)) (hp : pairK d p = 0) :
    pairK d (conjJ p) = 0 := by
  have h1 : ∀ i, d i * p.1 i = 0 := fun i =>
    congrFun (congrArg Prod.fst hp) i
  have h2 : ∀ i, d i * p.2 i = 0 := fun i =>
    neg_eq_zero.mp (congrFun (congrArg Prod.snd hp) i)
  unfold pairK conjJ
  refine Prod.ext (funext fun i => ?_) (funext fun i => ?_)
  · exact h2 i
  · exact neg_eq_zero.mpr (h1 i)

/-! ## III — K = −∇𝓕: o estatuto duplo verificado -/

/-- o funcional de contraste da face finita: 𝓕(x) = ½ Σ βd_i x_i². -/
def contrastF {n : ℕ} (β : ℝ) (d : Fin n → ℝ) (x : Fin n → ℝ) : ℝ :=
  (1 / 2) * ∑ i, β * d i * x i ^ 2

/-- [KERNEL] ★★★ O GRADIENTE É O GERADOR: a variação primeira de 𝓕 é
    exatamente ⟨βd·x, v⟩ — ∇𝓕(x) = βd·x, a ação de K. Identidade
    algébrica exata (o resto é h²·𝓕(v), sem termo escondido). -/
theorem gradient_first_variation {n : ℕ} (β : ℝ) (d : Fin n → ℝ)
    (x v : Fin n → ℝ) (h : ℝ) :
    contrastF β d (x + h • v)
      = contrastF β d x + h * (∑ i, (β * d i * x i) * v i)
        + h ^ 2 * contrastF β d v := by
  unfold contrastF
  have hsplit : ∀ i : Fin n, β * d i * (x + h • v) i ^ 2
      = β * d i * x i ^ 2 + (2 * h) * ((β * d i * x i) * v i)
        + h ^ 2 * (β * d i * v i ^ 2) := by
    intro i
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    ring
  calc (1 / 2) * ∑ i, β * d i * (x + h • v) i ^ 2
      = (1 / 2) * ∑ i, (β * d i * x i ^ 2 + (2 * h) * ((β * d i * x i) * v i)
          + h ^ 2 * (β * d i * v i ^ 2)) := by
        congr 1
        exact Finset.sum_congr rfl fun i _ => hsplit i
    _ = (1 / 2) * ((∑ i, β * d i * x i ^ 2)
          + ((2 * h) * ∑ i, (β * d i * x i) * v i)
          + (h ^ 2 * ∑ i, β * d i * v i ^ 2)) := by
        rw [Finset.sum_add_distrib, Finset.sum_add_distrib,
            Finset.mul_sum, Finset.mul_sum]
    _ = (1 / 2) * (∑ i, β * d i * x i ^ 2)
          + h * (∑ i, (β * d i * x i) * v i)
          + h ^ 2 * ((1 / 2) * ∑ i, β * d i * v i ^ 2) := by
        ring

/-- [KERNEL] ★★★ O FLUXO RESOLVE ẏ = −∇𝓕(y): a derivada do transporte
    diagonal em todo t₀ é −(βd_i)·(o próprio fluxo) — a EDO do gradiente
    negativo, em cálculo real, componente a componente. -/
theorem flow_solves_gradient_ode {n : ℕ} (β : ℝ) (d : Fin n → ℝ)
    (x : Fin n → ℝ) (i : Fin n) (t₀ : ℝ) :
    HasDerivAt (fun t : ℝ => diagFlow β d t x i)
      (-(β * d i) * diagFlow β d t₀ x i) t₀ := by
  unfold diagFlow
  simp only [mul_assoc]
  have h1 : HasDerivAt (fun t : ℝ => -(t * (β * d i))) (-(β * d i)) t₀ :=
    (hasDerivAt_mul_const (β * d i)).neg
  have h2 := (h1.exp).mul_const (x i)
  have hval : Real.exp (-(t₀ * (β * d i))) * -(β * d i) * x i
      = -(β * d i) * (Real.exp (-(t₀ * (β * d i))) * x i) := by ring
  exact hval ▸ h2

/-- [KERNEL] ★★★ SPOHN FINITO: o funcional de contraste DESCE ao longo do
    fluxo — 𝓕 é Lyapunov do transporte. A entrega tem direção. -/
theorem lyapunov_decreases {n : ℕ} {β : ℝ} (hβ : 0 < β) (d : Fin n → ℝ)
    (hd : ∀ i, 0 ≤ d i) (x : Fin n → ℝ) {s t : ℝ} (hst : s ≤ t) :
    contrastF β d (diagFlow β d t x) ≤ contrastF β d (diagFlow β d s x) := by
  unfold contrastF diagFlow
  have key : ∀ i : Fin n,
      β * d i * (Real.exp (-(t * β * d i)) * x i) ^ 2
        ≤ β * d i * (Real.exp (-(s * β * d i)) * x i) ^ 2 := by
    intro i
    have hbd : 0 ≤ β * d i := mul_nonneg (le_of_lt hβ) (hd i)
    apply mul_le_mul_of_nonneg_left _ hbd
    rw [mul_pow, mul_pow]
    apply mul_le_mul_of_nonneg_right _ (sq_nonneg (x i))
    have he : Real.exp (-(t * β * d i)) ≤ Real.exp (-(s * β * d i)) := by
      apply Real.exp_le_exp.mpr
      have h0 : s * β * d i ≤ t * β * d i :=
        mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_right hst (le_of_lt hβ)) (hd i)
      linarith
    calc Real.exp (-(t * β * d i)) ^ 2
        ≤ Real.exp (-(s * β * d i)) ^ 2 := by
          apply pow_le_pow_left₀ (le_of_lt (Real.exp_pos _)) he
      _ = Real.exp (-(s * β * d i)) ^ 2 := rfl
  have hsum := Finset.sum_le_sum (fun i (_ : i ∈ Finset.univ) => key i)
  have hhalf : (0 : ℝ) ≤ 1 / 2 := by norm_num
  exact mul_le_mul_of_nonneg_left hsum hhalf

/-- [KERNEL] ★★★ A SÍNTESE — K = −∇𝓕 VERIFICADO na face finita, nas três
    provas que a identidade pede: o gradiente é o gerador (variação
    primeira exata) ∧ o fluxo resolve a EDO do gradiente ∧ o funcional
    desce (Lyapunov). "K não é o veredito; é a inclinação que ainda exige
    movimento — e a inclinação é EXATAMENTE −∇𝓕." -/
theorem K_equals_neg_gradient_verified {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) (x : Fin n → ℝ) :
    (∀ (v : Fin n → ℝ) (h' : ℝ), contrastF β d (x + h' • v)
        = contrastF β d x + h' * (∑ i, (β * d i * x i) * v i)
          + h' ^ 2 * contrastF β d v)
    ∧ (∀ (i : Fin n) (t₀ : ℝ),
        HasDerivAt (fun t : ℝ => diagFlow β d t x i)
          (-(β * d i) * diagFlow β d t₀ x i) t₀)
    ∧ (∀ s t : ℝ, s ≤ t →
        contrastF β d (diagFlow β d t x) ≤ contrastF β d (diagFlow β d s x)) :=
  ⟨fun v h' => gradient_first_variation β d x v h',
   fun i t₀ => flow_solves_gradient_ode β d x i t₀,
   fun _ _ hst => lyapunov_decreases hβ d hd x hst⟩

end

end TGLExt
