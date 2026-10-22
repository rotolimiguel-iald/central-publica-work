import TGLExt.InfiniteWord

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

/-!
# O HABITANTE DE HILBERT: o canto de Breuer dispara CONCRETAMENTE em ℓ²
  [TGLExt — v95, o incremento 12 do programa SemifiniteAnalysis]

O v94 fechou a implicação em ∞-dim com hipóteses estruturais. Esta pedra
constrói O PRIMEIRO HABITANTE: a morada ℓ²(ℕ,ℂ) — Hilbert GENUINAMENTE
∞-dim — e o operador concreto T = 1 − P_{e₀} (apaga tudo MENOS a
primeira inscrição: ker T = ℂ·e₀). Nele o canto de Breuer do v94
DISPARA com todos os dados nomeados: espectro ⊆ {0,1} (gap = 1),
kernel = o átomo da primeira inscrição, e o peso do canto é EXATO:

    τ(ker T) = 1 = ω(I)  —  O CANTO PESA O NOME.

O QUE ESTA PEDRA PROVA [KERNEL]:
* ★ `inscriptions_orthonormal` — as inscrições e_n são ortonormais;
* ★★ `ellTwo_not_finiteDimensional` — ℓ² é GENUINAMENTE ∞-dim
  (a família ortonormal infinita mata qualquer dimensão finita);
* ★ `ker_eraseFirst` — ker(1−P) = o átomo da primeira inscrição;
* ★ `eraseFirst_spectrum_gap` — espectro de T·T ⊆ {0,1}: 0 isolado
  com gap 1 (idempotente auto-adjunto; iff espectral da mathlib);
* ★★★★ `concrete_corner_fires` — O CANTO DISPARA NO HABITANTE:
  P ∈ {T}″ ∧ P ∈ {T}′ ∧ 0 < τ(ker) < ∞ ∧ τ(kerᗮ) = ⊤;
* ★★★ `corner_weighs_the_name` — τ(ker T) = 1 = ω(I).

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-- a morada de Hilbert concreta: ℓ²(ℕ, ℂ). -/
abbrev ellTwo : Type := lp (fun _ : ℕ => ℂ) 2

/-- as inscrições: a base ortonormal canônica e_n. -/
def inscriptions : ℕ → ellTwo := fun n => lp.single 2 n 1

/-- a primeira inscrição: e₀. -/
def firstInscription : ellTwo := inscriptions 0

/-- [KERNEL] ★ as inscrições são ortonormais. -/
theorem inscriptions_orthonormal : Orthonormal ℂ inscriptions := by
  rw [orthonormal_iff_ite]
  intro m n
  unfold inscriptions
  rw [lp.inner_single_left]
  rcases eq_or_ne m n with h | h
  · subst h
    rw [lp.single_apply_self, if_pos rfl]
    simp [RCLike.inner_apply]
  · rw [lp.single_apply_ne 2 n 1 h, if_neg h]
    simp

private theorem firstInscription_ne_zero : firstInscription ≠ 0 :=
  inscriptions_orthonormal.ne_zero 0

/-- [KERNEL] ★★ a morada é GENUINAMENTE ∞-dim: a família ortonormal
    infinita não cabe em dimensão finita. -/
theorem ellTwo_not_finiteDimensional : ¬FiniteDimensional ℂ ellTwo := by
  intro hfd
  set n := Module.finrank ℂ ellTwo with hn
  have hli : LinearIndependent ℂ inscriptions :=
    inscriptions_orthonormal.linearIndependent
  have hli2 : LinearIndependent ℂ
      (inscriptions ∘ (fun i : Fin (n + 1) => (i : ℕ))) :=
    hli.comp _ Fin.val_injective
  have hcard := hli2.fintype_card_le_finrank
  rw [Fintype.card_fin] at hcard
  omega

/-- o átomo: o span da primeira inscrição. -/
def firstAtom : Submodule ℂ ellTwo := ℂ ∙ firstInscription

instance : FiniteDimensional ℂ firstAtom := by
  unfold firstAtom
  infer_instance

instance : (firstAtom).HasOrthogonalProjection := by
  haveI : CompleteSpace firstAtom := FiniteDimensional.complete ℂ firstAtom
  infer_instance

/-- O OPERADOR CONCRETO: T = 1 − P_{e₀} — apaga tudo MENOS a primeira
    inscrição (o kernel é exatamente o átomo). -/
def eraseFirst : ellTwo →L[ℂ] ellTwo := 1 - firstAtom.starProjection

theorem eraseFirst_apply (x : ellTwo) :
    eraseFirst x = x - firstAtom.starProjection x := rfl

/-- [KERNEL] ★ T é auto-adjunto. -/
theorem eraseFirst_selfadjoint :
    ContinuousLinearMap.adjoint eraseFirst = eraseFirst := by
  have h : IsSelfAdjoint eraseFirst := by
    unfold eraseFirst
    exact (IsSelfAdjoint.one (ellTwo →L[ℂ] ellTwo)).sub
      (isSelfAdjoint_starProjection firstAtom)
  rw [← ContinuousLinearMap.star_eq_adjoint]
  exact h

/-- [KERNEL] ★ o kernel é o átomo da primeira inscrição. -/
theorem ker_eraseFirst : eraseFirst.ker = firstAtom := by
  ext x
  constructor
  · intro hx
    have hx0 : eraseFirst x = 0 := LinearMap.mem_ker.mp hx
    have h2 : x - firstAtom.starProjection x = 0 := hx0
    exact Submodule.starProjection_eq_self_iff.mp (sub_eq_zero.mp h2).symm
  · intro hx
    refine LinearMap.mem_ker.mpr ?_
    show eraseFirst x = 0
    calc eraseFirst x = x - firstAtom.starProjection x := rfl
      _ = x - x := by rw [Submodule.starProjection_eq_self_iff.mpr hx]
      _ = 0 := sub_self x

/-- [KERNEL] ★ T é idempotente (T·T = T): projetor complementar. -/
theorem eraseFirst_idem : eraseFirst * eraseFirst = eraseFirst := by
  unfold eraseFirst
  have hP : firstAtom.starProjection * firstAtom.starProjection
      = firstAtom.starProjection :=
    firstAtom.isIdempotentElem_starProjection
  rw [mul_sub, mul_one, sub_mul, one_mul, hP, sub_self, sub_zero]

/-- [KERNEL] ★ o espectro de T·T mora em {0,1}: 0 ISOLADO com gap 1. -/
theorem eraseFirst_spectrum_gap :
    ∀ y ∈ spectrum ℝ (eraseFirst * eraseFirst), y = 0 ∨ (1 : ℝ) ≤ y := by
  intro y hy
  rw [eraseFirst_idem] at hy
  -- mapeamento espectral (meia-face, vale sobre qualquer corpo):
  -- y² − y ∈ σ(T·T − T) = σ(0) = {0}
  haveI : Nontrivial (ellTwo →L[ℂ] ellTwo) := by
    refine ⟨⟨1, 0, fun h => firstInscription_ne_zero ?_⟩⟩
    have h1 : (1 : ellTwo →L[ℂ] ellTwo) firstInscription = firstInscription := rfl
    rw [h] at h1
    simpa using h1.symm
  have hmem : (Polynomial.X ^ 2 - Polynomial.X : Polynomial ℝ).eval y
      ∈ spectrum ℝ (Polynomial.aeval eraseFirst
        (Polynomial.X ^ 2 - Polynomial.X : Polynomial ℝ)) :=
    spectrum.subset_polynomial_aeval eraseFirst
      (Polynomial.X ^ 2 - Polynomial.X : Polynomial ℝ) ⟨y, hy, rfl⟩
  have haeval : Polynomial.aeval eraseFirst
      (Polynomial.X ^ 2 - Polynomial.X : Polynomial ℝ) = 0 := by
    rw [map_sub, map_pow, Polynomial.aeval_X, sq, eraseFirst_idem, sub_self]
  rw [haeval, spectrum.zero_eq, Set.mem_singleton_iff] at hmem
  have heval : y ^ 2 - y = 0 := by
    have h2 : (Polynomial.X ^ 2 - Polynomial.X : Polynomial ℝ).eval y
        = y ^ 2 - y := by
      simp
    rw [← h2]
    exact hmem
  have hfac : y * (y - 1) = 0 := by linear_combination heval
  rcases mul_eq_zero.mp hfac with h0 | h1
  · exact Or.inl h0
  · right
    have h2 : y = 1 := by linarith [sub_eq_zero.mp h1]
    rw [h2]

/-- [KERNEL] ★ o kernel não é trivial: e₀ mora nele. -/
theorem ker_eraseFirst_ne_bot : eraseFirst.ker ≠ ⊥ := by
  rw [ker_eraseFirst]
  exact (Submodule.ne_bot_iff _).mpr
    ⟨firstInscription, Submodule.mem_span_singleton_self _,
      firstInscription_ne_zero⟩

/-- [KERNEL] ★★★★ O CANTO DISPARA NO HABITANTE: no operador CONCRETO
    T = 1 − P_{e₀} sobre ℓ²(ℕ,ℂ), o canto de Breuer INTEIRO conclui —
    P_{ker T} ∈ {T}″ ∧ P ∈ {T}′ ∧ 0 < τ(ker) < ∞ ∧ τ(kerᗮ) = ⊤.
    Nenhuma hipótese pendente: tudo foi CONSTRUÍDO acima. -/
theorem concrete_corner_fires :
    ((eraseFirst.ker).starProjection
        ∈ ({eraseFirst} : Set (ellTwo →L[ℂ] ellTwo)).centralizer.centralizer ∧
      (eraseFirst.ker).starProjection
        ∈ ({eraseFirst} : Set (ellTwo →L[ℂ] ellTwo)).centralizer) ∧
      ((0 < (semifiniteDimTrace ℂ ellTwo).tau eraseFirst.ker ∧
          (semifiniteDimTrace ℂ ellTwo).tau eraseFirst.ker < ⊤) ∧
        (semifiniteDimTrace ℂ ellTwo).tau (eraseFirst.ker)ᗮ = ⊤) :=
  concrete_breuer_corner_infinite (T := eraseFirst)
    ellTwo_not_finiteDimensional eraseFirst_selfadjoint one_pos
    eraseFirst_spectrum_gap firstAtom ker_eraseFirst_ne_bot
    (le_of_eq ker_eraseFirst) inferInstance

/-- [KERNEL] ★★★ O CANTO PESA O NOME: τ(ker T) = 1 = ω(I) — o átomo da
    primeira inscrição pesa exatamente a identidade preservada. -/
theorem corner_weighs_the_name :
    (semifiniteDimTrace ℂ ellTwo).tau eraseFirst.ker = 1 := by
  rw [ker_eraseFirst]
  show dimOrTop ℂ firstAtom = 1
  have h : dimOrTop ℂ firstAtom = (Module.finrank ℂ firstAtom : ℝ≥0∞) :=
    dimOrTop_of_finite ℂ inferInstance
  have h2 : Module.finrank ℂ firstAtom = 1 := by
    unfold firstAtom
    exact finrank_span_singleton firstInscription_ne_zero
  rw [h, h2, Nat.cast_one]

end

end TGLExt
