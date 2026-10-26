import TGLExt.LinearizedSpin2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A SEMENTE SEMIFINITA: o primeiro tijolo da biblioteca do fecho
  [TGLExt — v76, o incremento 1 do programa SemifiniteAnalysis]

O caminho ao selo TGL_QG_MATHEMATICAL_MODEL_CONSTRUCTED começa pela
biblioteca que a mathlib não tem: FaithfulNormalSemifiniteTrace →
AffiliatedOperator → TauCompactIdeal → BreuerFredholm. Esta pedra deposita
o PRIMEIRO TIJOLO honesto: os axiomas do peso tracial fiel verificados no
primeiro habitante concreto (o traço matricial no cone psd) — em
particular o axioma central de FIDELIDADE, que não estava na mathlib.

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `psd_offdiag_zero_of_diag_zero` — o argumento do menor 2×2: se A ⪰ 0
  e TODA a diagonal é nula, então A = 0 (para i ≠ j, o vetor
  x = s·eᵢ + eⱼ dá 0 ≤ xᵀAx = 2s·Aᵢⱼ para todo s ⟹ Aᵢⱼ = 0);
* ★★ `psd_trace_eq_zero_iff` — **A FIDELIDADE DO TRAÇO NO CONE PSD**
  (o axioma central de FaithfulNormalSemifiniteTrace, provado em
  concreto): A ⪰ 0 ⟹ (tr A = 0 ⟺ A = 0);
* ★ `trace_monotone_of_psd_sub` — MONOTONIA: B − A ⪰ 0 ⟹ tr A ≤ tr B —
  a face concreta do campo `mono` da camada abstrata v64;
* ★ `matrix_trace_is_faithful_weight` — O PRIMEIRO HABITANTE: positividade
  + fidelidade + monotonia empacotadas — os axiomas do peso tracial no
  primeiro modelo concreto (normalidade é trivial em dimensão finita;
  a semifinitude é a finitude).

HONESTIDADE: dimensão FINITA — o tijolo 1 de um programa nomeado
plurianual (o contínuo II_∞/III₁ exige operadores afiliados e
normalidade genuína); NENHUMA flag concreta do fecho se move com isto
(os probes v75 garantem). β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [KERNEL] ★ o argumento do menor 2×2: A ⪰ 0 com diagonal toda nula ⟹
    A = 0 (o vetor x = s·eᵢ + eⱼ força cada entrada fora da diagonal). -/
theorem psd_offdiag_zero_of_diag_zero (A : Matrix n n ℝ) (hA : A.PosSemidef)
    (hdiag : ∀ i, A i i = 0) : A = 0 := by
  ext i j
  by_cases hij : i = j
  · subst hij
    simpa using hdiag i
  · have hji : A j i = A i j := by
      conv_lhs => rw [← hA.1]
      simp [Matrix.conjTranspose_apply]
    have key : ∀ s : ℝ, 0 ≤ 2 * s * A i j := by
      intro s
      have hp := hA.dotProduct_mulVec_nonneg
        ((Pi.single i s : n → ℝ) + (Pi.single j 1 : n → ℝ))
      have hstar : star ((Pi.single i s : n → ℝ) + (Pi.single j 1 : n → ℝ))
          = (Pi.single i s : n → ℝ) + (Pi.single j 1 : n → ℝ) := by
        funext k
        simp [Pi.star_apply]
      rw [hstar] at hp
      have hmv : ∀ k, (A *ᵥ ((Pi.single i s : n → ℝ) + (Pi.single j 1 : n → ℝ))) k
          = A k i * s + A k j * 1 := by
        intro k
        simp only [Matrix.mulVec, dotProduct, Pi.add_apply, Pi.single_apply,
          mul_add, mul_ite, mul_one, mul_zero]
        rw [Finset.sum_add_distrib]
        simp [Finset.sum_ite_eq', Finset.mem_univ]
      have hval : ((Pi.single i s : n → ℝ) + (Pi.single j 1 : n → ℝ)) ⬝ᵥ
          (A *ᵥ ((Pi.single i s : n → ℝ) + (Pi.single j 1 : n → ℝ)))
          = s * (A i i * s + A i j * 1) + 1 * (A j i * s + A j j * 1) := by
        rw [add_dotProduct, single_dotProduct, single_dotProduct, hmv i, hmv j]
      rw [hval, hdiag i, hdiag j, hji] at hp
      nlinarith [hp]
    have h2 := key (-(A i j))
    have h3 := key (A i j)
    have hz : A i j = 0 := by nlinarith [sq_nonneg (A i j)]
    simpa using hz

/-- [KERNEL] ★★ A FIDELIDADE DO TRAÇO NO CONE PSD — o axioma central de
    `FaithfulNormalSemifiniteTrace`, provado no primeiro habitante
    concreto: A ⪰ 0 ⟹ (tr A = 0 ⟺ A = 0). -/
theorem psd_trace_eq_zero_iff (A : Matrix n n ℝ) (hA : A.PosSemidef) :
    A.trace = 0 ↔ A = 0 := by
  constructor
  · intro htr
    have hdiag : ∀ i, A i i = 0 := by
      have hsum : ∑ k, A k k = 0 := by
        simpa [Matrix.trace, Matrix.diag] using htr
      intro i
      exact (Finset.sum_eq_zero_iff_of_nonneg
        (fun k _ => hA.diag_nonneg)).mp hsum i (Finset.mem_univ i)
    exact psd_offdiag_zero_of_diag_zero A hA hdiag
  · rintro rfl
    simp

/-- [KERNEL] ★ MONOTONIA do traço na ordem de Loewner (a face concreta do
    campo `mono` da camada abstrata v64): B − A ⪰ 0 ⟹ tr A ≤ tr B. -/
theorem trace_monotone_of_psd_sub (A B : Matrix n n ℝ)
    (h : (B - A).PosSemidef) : A.trace ≤ B.trace := by
  have hnn := h.trace_nonneg
  rw [Matrix.trace_sub] at hnn
  linarith

/-- [KERNEL] ★ O PRIMEIRO HABITANTE da biblioteca semifinita: o traço
    matricial satisfaz os três axiomas do peso tracial fiel no cone psd —
    positividade, FIDELIDADE e monotonia (normalidade trivial em dimensão
    finita; a semifinitude é a finitude). O tijolo 1 do caminho
    SemifiniteAnalysis → ... → CanonicalBoundaryWitness. -/
theorem matrix_trace_is_faithful_weight :
    (∀ A : Matrix n n ℝ, A.PosSemidef → 0 ≤ A.trace) ∧
      (∀ A : Matrix n n ℝ, A.PosSemidef → (A.trace = 0 ↔ A = 0)) ∧
      (∀ A B : Matrix n n ℝ, (B - A).PosSemidef → A.trace ≤ B.trace) :=
  ⟨fun _ hA => hA.trace_nonneg, psd_trace_eq_zero_iff, trace_monotone_of_psd_sub⟩

end

end TGLExt
