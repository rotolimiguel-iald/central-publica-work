import TheTimeHasNoRank

set_option autoImplicit false

/-!
# Conferencia do AUDITOR: o enunciado compilado e o PRE-REGISTRADO?

Cada `example` abaixo copia a assinatura-alvo (`lean_alvo`) do PREREGISTRO.json congelado (sha256 64b1c386…)
e a fecha com o termo da pedra. Se o termo da pedra tivesse tipo diferente (hipotese a mais, conclusao mais
fraca, troca por `True`), o `example` NAO compilaria. Convencao do pre-registro: `n` sem binder =
variaveis de secao `{n : Type} [Fintype n] [DecidableEq n]`.
-/

namespace AuditorEnunciados

open TGLExt TGLExt.TheTimeHasNoRank
open Filter Topology
open scoped Matrix ComplexOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

-- T1.a
example {ι : Type} [Fintype ι] [DecidableEq ι] [Nonempty ι] (T H : Matrix ι ι ℂ) {c : ℂ} (hc : c ≠ 0) :
    T * H - H * T ≠ c • (1 : Matrix ι ι ℂ) := no_time_matrix T H hc
example (k : ℕ) (hk : 0 < k) (T H : Matrix (Fin k) (Fin k) ℂ) :
    T * H - H * T ≠ Complex.I • (1 : Matrix (Fin k) (Fin k) ℂ) := no_time_matrix_fin k hk T H
-- T1.b (opcional)
example {ι : Type} [Fintype ι] [DecidableEq ι] (T H : Matrix ι ι ℂ) (c : ℂ) :
    purityR (T * H - H * T - c • (1 : Matrix ι ι ℂ)) = purityR (T * H - H * T) + (Fintype.card ι : ℝ) * Complex.normSq c :=
  commutator_far_from_scalar T H c
-- T1.c
example {ι : Type} [Fintype ι] [DecidableEq ι] [Nonempty ι] (V H : Matrix ι ι ℂ) (hV : IsUnit V) {s : ℂ}
    (hs : s ≠ 0) : V⁻¹ * H * V ≠ H + s • (1 : Matrix ι ι ℂ) := no_finite_spectral_translation V H hV hs
-- T2.b (opcional)
example {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] [CompleteSpace A] [Nontrivial A] (V : Aˣ) (H : A)
    {s : ℂ} (hs : s ≠ 0) : (↑V⁻¹ : A) * H * ↑V ≠ H + algebraMap ℂ A s := no_bounded_spectral_translation V H hs
-- T3.a
example (ρ : Matrix n n ℂ) (hρ : ρ.PosDef) :
    (∀ a, sigma ρ 0 a = a) ∧ (∀ s t a, sigma ρ s (sigma ρ t a) = sigma ρ (s + t) a) ∧
    (∀ t a b, sigma ρ t (a * b) = sigma ρ t a * sigma ρ t b) ∧ (∀ t, sigma ρ t 1 = 1) ∧
    (∀ t a, sigma ρ t aᴴ = (sigma ρ t a)ᴴ) ∧ (∀ t a, gibbs ρ (sigma ρ t a) = gibbs ρ a) ∧
    (∀ a b, gibbs ρ (a * b) = gibbs ρ (b * Delta ρ a)) ∧ (∀ t, modPow ρ t ∈ unitary (Matrix n n ℂ)) :=
  time_is_the_modular_flow ρ hρ
-- T4.a
example (U : (Matrix n n ℂ)ˣ) (hU : (U : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ)) (x : Matrix n n ℂ) :
    ((U : Matrix n n ℂ) * x * ((U⁻¹ : (Matrix n n ℂ)ˣ) : Matrix n n ℂ)).charpoly = x.charpoly ∧
      purity ((U : Matrix n n ℂ) * x * (U : Matrix n n ℂ)ᴴ) = purity x :=
  unitary_keeps_spectrum_and_purity U hU x
-- T4.b
example {X : Type*} [MetricSpace X] {f : X → X} (hf : Isometry f) {x z : X}
    (h : Filter.Tendsto (fun k : ℕ => f^[k] x) Filter.atTop (nhds z)) : x = z ∧ f z = z :=
  isometry_orbit_converges_only_if_fixed hf h
example {X : Type*} [MetricSpace X] (φ : ℝ → X → X) (hgrp : ∀ s t x, φ (s + t) x = φ s (φ t x))
    (hiso : ∀ s, Isometry (φ s)) {x z : X} (h : Filter.Tendsto (fun t => φ t x) Filter.atTop (nhds z)) :
    x = z ∧ ∀ s, φ s z = z := isometric_flow_converges_only_if_fixed φ hgrp hiso h
example (d : n → ℝ) (hd : ∀ i, 0 < d i) (hinj : Function.Injective d) (x : Matrix n n ℂ) :
    (∃ z, Filter.Tendsto (fun t => sigma (rhoD d) t x) Filter.atTop (nhds z)) ↔ x = diagExpect x :=
  modular_orbit_converges_iff_diagonal d hd hinj x
-- T4.c
example (m : n → n → ℂ) : schurDiag m = Matrix.diagonal (fun p => m p.1 p.2) := rfl
example (m : n → n → ℂ) (x : Matrix n n ℂ) (p : n × n) :
    (schurDiag m).mulVec (fun q => x q.1 q.2) p = m p.1 p.2 * x p.1 p.2 := schurDiag_mulVec m x p
example (g : n → n → ℝ) (t : ℝ) :
    (schurDiag (fun i j => ((Real.exp (-(t * g i j)) : ℝ) : ℂ))).det = ((Real.exp (-(t * ∑ i, ∑ j, g i j)) : ℝ) : ℂ) :=
  dephase_volume g t
example (g : n → n → ℝ) (hg : ∀ i j, 0 ≤ g i j) (hpos : ∃ i j, 0 < g i j) {t : ℝ} (ht : 0 < t) :
    Real.exp (-(t * ∑ i, ∑ j, g i j)) < 1 := dephase_volume_lt_one g hg hpos ht
example (d : n → ℝ) (t : ℝ) :
    (schurDiag (fun i j => Complex.exp ((t : ℂ) * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))))).det = 1 :=
  modular_volume_one d t
-- T4.e
example {s : ℝ} (hs : 0 < s) :
    (boost s).det = 1 ∧ Filter.Tendsto (fun k : ℕ => ((boost s) ^ k).mulVec ![1, -1]) Filter.atTop (nhds 0) :=
  volume_kept_yet_lands hs
-- T4.f (opcional)
example {m : ℕ} (L : Matrix (Fin m) (Fin m) ℝ)
    (h : ∀ v, Filter.Tendsto (fun k : ℕ => (L ^ k).mulVec v) Filter.atTop (nhds 0)) (hm : 0 < m) : |L.det| < 1 :=
  global_attractor_needs_volume_loss L h hm
-- T5.b
example (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) {i₀ j₀ : n} (hij : i₀ ≠ j₀) :
    ∃ ρ σ : Matrix n n ℂ, ρ ≠ σ ∧ ρ.PosSemidef ∧ σ.PosSemidef ∧ ρ.trace = 1 ∧ σ.trace = 1 ∧
      (∀ t, dephase g t ρ = ρ) ∧ (∀ t, dephase g t σ = σ) := dephase_fixed_states_not_unique g hg0 hij
-- T6.a
example (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    purityR (dephase g t x) = ∑ i, ∑ j, Real.exp (-(2 * t * g i j)) * Complex.normSq (x i j) := purityR_dephase g t x
-- T6.c
example (g : n → n → ℝ) (hg : ∀ i j, 0 ≤ g i j) {t : ℝ} (ht : 0 < t) (x : Matrix n n ℂ) {i₀ j₀ : n}
    (hpos : 0 < g i₀ j₀) (hx : x i₀ j₀ ≠ 0) : purityR (dephase g t x) < purityR x :=
  purityR_dephase_lt g hg ht x hpos hx
-- T6.d
example (x : Matrix n n ℂ) (hx : x.IsHermitian) : purity x = (x * x).trace := purity_of_hermitian x hx
example (d : n → ℝ) (hd : ∀ i, 0 < d i) (t : ℝ) (x : Matrix n n ℂ) :
    purityR (sigma (rhoD d) t x) = purityR x := purityR_modular d hd t x
-- T7.a
example (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    dephase g (-t) (dephase g t x) = x ∧ dephase g t (dephase g (-t) x) = x := dephase_inverse g t x
-- T7.b
example {γ t : ℝ} (hγ : 0 < γ) (ht : 0 < t) :
    let g : Fin 2 → Fin 2 → ℝ := fun i j => if i = j then 0 else γ
    let ψ : Matrix (Fin 2) (Fin 2) ℂ := (1 / 2 : ℂ) • !![1, 1; 1, 1]
    ψ.PosSemidef ∧ ψ.trace = 1 ∧ ¬ (dephase g (-t) ψ).PosSemidef := inverse_dephasing_not_positive hγ ht
-- T8.a (os campos sao os pre-registrados)
example (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) :
    (coherenceScaling g i₀ j₀ hg).tau = (fun x => ‖x i₀ j₀‖) := rfl
example (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) :
    (coherenceScaling g i₀ j₀ hg).theta = (fun s x => dephase g s x) := rfl
-- T8.b: a conjuncao e EXATAMENTE a de Fundacao.agape para D := coherenceScaling, m := x
example (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) (x : Matrix n n ℂ) (hx : x i₀ j₀ ≠ 0) :
    let D := coherenceScaling g i₀ j₀ hg
    (∀ s : ℝ, s ≠ 0 → ∀ m' : Matrix n n ℂ, D.theta s m' = m' → D.tau m' = 0) ∧
    (∀ s : ℝ, D.tau (D.theta s x) < D.tau (D.theta (s - 1) x)) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < D.tau (D.theta s x)) ∧
    (∀ s : ℝ, 0 < D.tau (D.theta s x)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s x) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) :=
  TGLExt.Fundacao.agape (coherenceScaling g i₀ j₀ hg) (m := x) (norm_pos_iff.mpr hx)
example (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) (x : Matrix n n ℂ) (hx : x i₀ j₀ ≠ 0) :
    type_of% (the_coherence_obeys_agape g i₀ j₀ hg x hx) =
      type_of% (TGLExt.Fundacao.agape (coherenceScaling g i₀ j₀ hg) (m := x) (norm_pos_iff.mpr hx)) := rfl
-- T8.c
example (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (i₀ : n) (x : Matrix n n ℂ) (hx : x i₀ i₀ ≠ 0) {s : ℝ}
    (hs : s ≠ 0) : ‖dephase g s x i₀ i₀‖ ≠ Real.exp (-s) * ‖x i₀ i₀‖ := the_record_does_not_scale g hg0 i₀ x hx hs
-- T9.a, T9.b, T9.c
example {A : Type*} [Ring A] [Algebra ℂ A] {P : A} (hP : IsIdempotentElem P) (hP1 : (1 : A) - P ≠ 0) (t : ℝ) :
    IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow P t) ↔ t = 0 := flow_isIdempotentElem_iff hP hP1 t
example {A : Type*} [Ring A] [Algebra ℂ A] {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    IsUnit (TheAxiomAndTheFalseWitness.axiomFlow P t) := flow_isUnit hP t
example {A : Type*} [Ring A] {P : A} (hP : IsIdempotentElem P) (hP1 : P ≠ 1) : ¬ IsUnit P := post_not_isUnit hP hP1
-- T9.d (opcional)
example (k : ℕ) (P : Matrix (Fin k) (Fin k) ℂ) (hP : IsIdempotentElem P) (t : ℝ) :
    (TheAxiomAndTheFalseWitness.axiomFlow P t).rank = k := flow_full_rank k P hP t
example (k : ℕ) (P : Matrix (Fin k) (Fin k) ℂ) (hP : IsIdempotentElem P) (hP1 : P ≠ 1) : P.rank < k :=
  post_rank_lt k P hP hP1
-- T10.b
example {κ : ℝ} (hκ : κ ≠ 0) (t : ℝ) : Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) :=
  clock_reads_modulo_period hκ t
example (t u : ℝ) : Circle.exp (0 * t) = Circle.exp (0 * u) := frozen_clock t u
-- T10.d
example (d : n → ℝ) (hd : ∀ i, 0 < d i) (t : ℝ) (x : Matrix n n ℂ) (i j : n) :
    ‖sigma (rhoD d) t x i j‖ = ‖x i j‖ := modular_clock_rotates_without_shrinking d hd t x i j
-- T11.a
example : (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) = absoluteRho (Fin 2) := optical_attractor_is_the_absolute_one

end

end AuditorEnunciados
