import TheTimeHasNoRank

set_option autoImplicit false
set_option maxHeartbeats 1000000

/-!
# Auditoria do construtor (rodada 2) da pedra candidata `TheTimeHasNoRank` (F1.TEMPO, sandbox)

Importa o `.olean` COMPILADO da pedra (não o fonte) e:
1. enumera TODA constante do espaço `TGLExt.TheTimeHasNoRank` (inclusive auxiliares geradas pelo Lean), com o
   tipo de declaração e os axiomas de que depende; RECUSA (erro) axioma fora do trio
   {propext, Classical.choice, Quot.sound} ou declaração `axiom` nova;
2. mede, no TERMO de prova, se cada teorema usa cada hipótese (binder de tipo Prop da assinatura): é a medida
   direta de «nome sem peso» no sentido de «a prova não usa a hipótese»;
3. confere cada ASSINATURA PRÉ-REGISTRADA (PREREGISTRO.json → afirmacoes → subitens → lean_alvo) por `example`
   provado pela declaração da rodada 2 (inclusive as renomeadas e as que perderam hipóteses sem peso): se o
   `example` compila, a declaração prova o enunciado pré-registrado (ou um mais forte).
Este arquivo não declara nada.
-/

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut count := 0
  let mut aux := 0
  for (n, ci) in env.constants.map₁.toList do
    if (`TGLExt.TheTimeHasNoRank).isPrefixOf n then
      let axs ← Elab.Command.liftCoreM (collectAxioms n)
      let kind := match ci with
        | .axiomInfo _ => "axiom"
        | .thmInfo _ => "theorem"
        | .defnInfo _ => "definition"
        | _ => "other"
      IO.println ("AUDIT_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
        String.intercalate "," (axs.toList.map Name.toString))
      count := count + 1
      if n.isInternal then aux := aux + 1
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
  IO.println ("AUDIT_TOTAL\t" ++ toString count ++ "\tAUXILIARES\t" ++ toString aux)

open Lean Meta Elab Command in
run_cmd do
  let env ← getEnv
  let mut nThm := 0
  for (n, ci) in env.constants.map₁.toList do
    if (`TGLExt.TheTimeHasNoRank).isPrefixOf n && !n.isInternal then
      if let .thmInfo ti := ci then
        nThm := nThm + 1
        let res ← liftTermElabM do
          forallTelescope ti.type fun xs _ => do
            let body ← instantiateLambda ti.value xs
            let mut nhyp := 0
            let mut acc : Array String := #[]
            for x in xs do
              let ty ← inferType x
              if (← isProp ty) then
                nhyp := nhyp + 1
                unless body.containsFVar x.fvarId! do
                  acc := acc.push (toString (← x.fvarId!.getUserName))
            return (nhyp, acc)
        let (nhyp, unused) := res
        IO.println ("HYP_USE\t" ++ n.toString ++ "\t" ++ toString nhyp ++ "\t" ++
          (if unused.isEmpty then "todas_usadas" else "NAO_USADAS:" ++ String.intercalate "," unused.toList))
  IO.println ("HYP_USE_TOTAL\t" ++ toString nThm)

open TGLExt
open scoped Matrix ComplexOrder

section PreReg

variable {n : Type} [Fintype n] [DecidableEq n]

-- T1.a
example {ι : Type} [Fintype ι] [DecidableEq ι] [Nonempty ι] (T H : Matrix ι ι ℂ) {c : ℂ} (hc : c ≠ 0) :
    T * H - H * T ≠ c • (1 : Matrix ι ι ℂ) :=
  TGLExt.TheTimeHasNoRank.no_time_matrix T H hc
example (m : ℕ) (hm : 0 < m) (T H : Matrix (Fin m) (Fin m) ℂ) :
    T * H - H * T ≠ Complex.I • (1 : Matrix (Fin m) (Fin m) ℂ) :=
  TGLExt.TheTimeHasNoRank.no_time_matrix_fin m hm T H
-- T1.b (opcional)
example {ι : Type} [Fintype ι] [DecidableEq ι] (T H : Matrix ι ι ℂ) (c : ℂ) :
    purityR (T * H - H * T - c • (1 : Matrix ι ι ℂ))
      = purityR (T * H - H * T) + (Fintype.card ι : ℝ) * Complex.normSq c :=
  TGLExt.TheTimeHasNoRank.commutator_far_from_scalar T H c
-- T1.c
example {ι : Type} [Fintype ι] [DecidableEq ι] [Nonempty ι] (V H : Matrix ι ι ℂ) (hV : IsUnit V) {s : ℂ}
    (hs : s ≠ 0) : V⁻¹ * H * V ≠ H + s • (1 : Matrix ι ι ℂ) :=
  TGLExt.TheTimeHasNoRank.no_finite_spectral_translation V H hV hs
-- T2.b (opcional)
example {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] [CompleteSpace A] [Nontrivial A] (V : Aˣ) (H : A)
    {s : ℂ} (hs : s ≠ 0) : (↑V⁻¹ : A) * H * ↑V ≠ H + algebraMap ℂ A s :=
  TGLExt.TheTimeHasNoRank.no_bounded_spectral_translation V H hs
-- T3.a (pré-registrado como time_is_the_modular_flow)
example (ρ : Matrix n n ℂ) (hρ : ρ.PosDef) :
    (∀ a, sigma ρ 0 a = a) ∧ (∀ s t a, sigma ρ s (sigma ρ t a) = sigma ρ (s + t) a) ∧
    (∀ t a b, sigma ρ t (a * b) = sigma ρ t a * sigma ρ t b) ∧ (∀ t, sigma ρ t 1 = 1) ∧
    (∀ t a, sigma ρ t aᴴ = (sigma ρ t a)ᴴ) ∧ (∀ t a, gibbs ρ (sigma ρ t a) = gibbs ρ a) ∧
    (∀ a b, gibbs ρ (a * b) = gibbs ρ (b * Delta ρ a)) ∧ (∀ t, modPow ρ t ∈ unitary (Matrix n n ℂ)) :=
  TGLExt.TheTimeHasNoRank.modular_flow_is_a_kms_group ρ hρ
-- T3.b (re-exportações, tipo original)
example : type_of% @TGLExt.sigma_fixed_iff_diag := @TGLExt.TheTimeHasNoRank.fixed_sector_is_the_centralizer
example : type_of% @TGLExt.absoluteOne_flow_trivial := @TGLExt.TheTimeHasNoRank.tracial_state_freezes_the_flow
example : type_of% @ChatgptAudit.NonKMSProbe.identity_flow_not_kms :=
  @TGLExt.TheTimeHasNoRank.nontracial_state_rejects_the_identity_flow
-- T4.a
example (U : (Matrix n n ℂ)ˣ) (hU : (U : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ)) (x : Matrix n n ℂ) :
    ((U : Matrix n n ℂ) * x * ((U⁻¹ : (Matrix n n ℂ)ˣ) : Matrix n n ℂ)).charpoly = x.charpoly ∧
    purity ((U : Matrix n n ℂ) * x * (U : Matrix n n ℂ)ᴴ) = purity x :=
  TGLExt.TheTimeHasNoRank.unitary_keeps_spectrum_and_purity U hU x
-- T4.b (abstrato)
example {X : Type*} [MetricSpace X] {f : X → X} (hf : Isometry f) {x z : X}
    (h : Filter.Tendsto (fun k : ℕ => f^[k] x) Filter.atTop (nhds z)) : x = z ∧ f z = z :=
  TGLExt.TheTimeHasNoRank.isometry_orbit_converges_only_if_fixed hf h
example {X : Type*} [MetricSpace X] (φ : ℝ → X → X) (hgrp : ∀ s t x, φ (s + t) x = φ s (φ t x))
    (hiso : ∀ s, Isometry (φ s)) {x z : X} (h : Filter.Tendsto (fun t => φ t x) Filter.atTop (nhds z)) :
    x = z ∧ ∀ s, φ s z = z :=
  TGLExt.TheTimeHasNoRank.isometric_flow_converges_only_if_fixed φ hgrp hiso h
-- T4.b (ii)
example (d : n → ℝ) (hd : ∀ i, 0 < d i) (hinj : Function.Injective d) (x : Matrix n n ℂ) :
    (∃ z, Filter.Tendsto (fun t => sigma (rhoD d) t x) Filter.atTop (nhds z)) ↔ x = diagExpect x :=
  TGLExt.TheTimeHasNoRank.modular_orbit_converges_iff_diagonal d hd hinj x
-- T4.b (i), na métrica de Frobenius
section
open scoped Matrix.Norms.Frobenius
example (U : Matrix n n ℂ) (hU : U ∈ unitary (Matrix n n ℂ)) : Isometry (fun x : Matrix n n ℂ => U * x * Uᴴ) :=
  TGLExt.TheTimeHasNoRank.unitary_conj_isometry U hU
end
-- T4.c
example (m : n → n → ℂ) : TGLExt.TheTimeHasNoRank.schurDiag m = Matrix.diagonal (fun p => m p.1 p.2) := rfl
example (m : n → n → ℂ) (x : Matrix n n ℂ) (p : n × n) :
    (TGLExt.TheTimeHasNoRank.schurDiag m).mulVec (fun q => x q.1 q.2) p = m p.1 p.2 * x p.1 p.2 :=
  TGLExt.TheTimeHasNoRank.schurDiag_mulVec m x p
example (g : n → n → ℝ) (t : ℝ) :
    (TGLExt.TheTimeHasNoRank.schurDiag (fun i j => ((Real.exp (-(t * g i j)) : ℝ) : ℂ))).det
      = ((Real.exp (-(t * ∑ i, ∑ j, g i j)) : ℝ) : ℂ) :=
  TGLExt.TheTimeHasNoRank.dephase_volume g t
example (g : n → n → ℝ) (hg : ∀ i j, 0 ≤ g i j) (hpos : ∃ i j, 0 < g i j) {t : ℝ} (ht : 0 < t) :
    Real.exp (-(t * ∑ i, ∑ j, g i j)) < 1 :=
  TGLExt.TheTimeHasNoRank.dephase_volume_lt_one g hg hpos ht
example (d : n → ℝ) (t : ℝ) :
    (TGLExt.TheTimeHasNoRank.schurDiag (fun i j => Complex.exp ((t : ℂ) * Complex.I
      * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))))).det = 1 :=
  TGLExt.TheTimeHasNoRank.modular_volume_one d t
-- T4.d / T5.a (re-exportações, tipo original)
example : type_of% @TGLExt.dephase_tendsto_expectation := @TGLExt.TheTimeHasNoRank.dephasing_lands_on_the_diagonal
example : type_of% @TGLExt.dephase_fixed_iff_diagonal :=
  @TGLExt.TheTimeHasNoRank.fixed_set_of_dephasing_is_the_diagonal
example : type_of% @TGLExt.diag_invariant := @TGLExt.TheTimeHasNoRank.the_record_is_invariant
-- T4.e
example {s : ℝ} (hs : 0 < s) : (boost s).det = 1 ∧
    Filter.Tendsto (fun k : ℕ => ((boost s) ^ k).mulVec ![1, -1]) Filter.atTop (nhds 0) :=
  TGLExt.TheTimeHasNoRank.volume_kept_yet_lands hs
-- T4.f (opcional)
example {m : ℕ} (L : Matrix (Fin m) (Fin m) ℝ)
    (h : ∀ v, Filter.Tendsto (fun k : ℕ => (L ^ k).mulVec v) Filter.atTop (nhds 0)) (hm : 0 < m) :
    |L.det| < 1 :=
  TGLExt.TheTimeHasNoRank.global_attractor_needs_volume_loss L h hm
-- T5.b
example (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) {i₀ j₀ : n} (hij : i₀ ≠ j₀) :
    ∃ ρ σ : Matrix n n ℂ, ρ ≠ σ ∧ ρ.PosSemidef ∧ σ.PosSemidef ∧ ρ.trace = 1 ∧ σ.trace = 1 ∧
      (∀ t, dephase g t ρ = ρ) ∧ (∀ t, dephase g t σ = σ) :=
  TGLExt.TheTimeHasNoRank.dephase_fixed_states_not_unique g hg0 hij
-- T6.a
example (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    purityR (dephase g t x) = ∑ i, ∑ j, Real.exp (-(2 * t * g i j)) * Complex.normSq (x i j) :=
  TGLExt.TheTimeHasNoRank.purityR_dephase g t x
-- T6.b (re-exportação)
example : type_of% @TGLExt.dephase_purityR_le := @TGLExt.TheTimeHasNoRank.purity_never_grows_under_dephasing
-- T6.c
example (g : n → n → ℝ) (hg : ∀ i j, 0 ≤ g i j) {t : ℝ} (ht : 0 < t) (x : Matrix n n ℂ) {i₀ j₀ : n}
    (hpos : 0 < g i₀ j₀) (hx : x i₀ j₀ ≠ 0) : purityR (dephase g t x) < purityR x :=
  TGLExt.TheTimeHasNoRank.purityR_dephase_lt g hg ht x hpos hx
-- T6.d
example (x : Matrix n n ℂ) (hx : x.IsHermitian) : purity x = (x * x).trace :=
  TGLExt.TheTimeHasNoRank.purity_of_hermitian x hx
example (d : n → ℝ) (_hd : ∀ i, 0 < d i) (t : ℝ) (x : Matrix n n ℂ) :
    purityR (sigma (rhoD d) t x) = purityR x :=
  TGLExt.TheTimeHasNoRank.purityR_modular d t x
-- T7.a
example (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    dephase g (-t) (dephase g t x) = x ∧ dephase g t (dephase g (-t) x) = x :=
  TGLExt.TheTimeHasNoRank.dephase_inverse g t x
-- T7.b
example {γ t : ℝ} (hγ : 0 < γ) (ht : 0 < t) :
    let g : Fin 2 → Fin 2 → ℝ := fun i j => if i = j then 0 else γ
    let ψ : Matrix (Fin 2) (Fin 2) ℂ := (1 / 2 : ℂ) • !![1, 1; 1, 1]
    ψ.PosSemidef ∧ ψ.trace = 1 ∧ ¬ (dephase g (-t) ψ).PosSemidef :=
  TGLExt.TheTimeHasNoRank.inverse_dephasing_not_positive hγ ht
-- T8.a (os campos da instância, por definição)
example (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) :
    (TGLExt.TheTimeHasNoRank.coherenceScaling g i₀ j₀ hg).tau = fun x => ‖x i₀ j₀‖ := rfl
example (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) :
    (TGLExt.TheTimeHasNoRank.coherenceScaling g i₀ j₀ hg).theta = fun s x => dephase g s x := rfl
-- T8.b (a conjunção literal de Fundacao.agape para D := coherenceScaling, m := x)
example (g : n → n → ℝ) (i₀ j₀ : n) (hg : g i₀ j₀ = 1) (x : Matrix n n ℂ) (hx : x i₀ j₀ ≠ 0) :
    type_of% (TGLExt.Fundacao.agape (TGLExt.TheTimeHasNoRank.coherenceScaling g i₀ j₀ hg) (m := x)
      (norm_pos_iff.mpr hx)) :=
  TGLExt.TheTimeHasNoRank.the_coherence_obeys_agape g i₀ j₀ hg x hx
-- T8.c
example (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (i₀ : n) (x : Matrix n n ℂ) (hx : x i₀ i₀ ≠ 0) {s : ℝ}
    (hs : s ≠ 0) : ‖dephase g s x i₀ i₀‖ ≠ Real.exp (-s) * ‖x i₀ i₀‖ :=
  TGLExt.TheTimeHasNoRank.the_record_does_not_scale g hg0 i₀ x hx hs
-- T8.d (re-exportação)
example : type_of% @TGLExt.boost_null_contract := @TGLExt.TheTimeHasNoRank.past_null_ray_contracts
-- T9.a–d
example {A : Type*} [Ring A] [Algebra ℂ A] {P : A} (hP : IsIdempotentElem P) (hP1 : (1 : A) - P ≠ 0) (t : ℝ) :
    IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow P t) ↔ t = 0 :=
  TGLExt.TheTimeHasNoRank.flow_isIdempotentElem_iff hP hP1 t
example {A : Type*} [Ring A] [Algebra ℂ A] {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    IsUnit (TheAxiomAndTheFalseWitness.axiomFlow P t) :=
  TGLExt.TheTimeHasNoRank.flow_isUnit hP t
example {A : Type*} [Ring A] {P : A} (hP : IsIdempotentElem P) (hP1 : P ≠ 1) : ¬ IsUnit P :=
  TGLExt.TheTimeHasNoRank.post_not_isUnit hP hP1
example (m : ℕ) (P : Matrix (Fin m) (Fin m) ℂ) (hP : IsIdempotentElem P) (t : ℝ) :
    (TheAxiomAndTheFalseWitness.axiomFlow P t).rank = m :=
  TGLExt.TheTimeHasNoRank.flow_full_rank m P hP t
example (m : ℕ) (P : Matrix (Fin m) (Fin m) ℂ) (hP : IsIdempotentElem P) (hP1 : P ≠ 1) : P.rank < m :=
  TGLExt.TheTimeHasNoRank.post_rank_lt m P hP hP1
-- T9.e (pré-registrado como the_time_has_no_rank: a conjunção literal)
example {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] {P : A} (hP : IsIdempotentElem P) (hP1 : P ≠ 1) :
    (∀ (m : ℕ), 0 < m → ∀ T H : Matrix (Fin m) (Fin m) ℂ,
        T * H - H * T ≠ Complex.I • (1 : Matrix (Fin m) (Fin m) ℂ)) ∧
    (∀ t : ℝ, IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow P t) ↔ t = 0) ∧
    (∀ t : ℝ, IsUnit (TheAxiomAndTheFalseWitness.axiomFlow P t)) ∧
    ¬ IsUnit P ∧
    Filter.Tendsto (TheAxiomAndTheFalseWitness.axiomFlow P) Filter.atTop (nhds P) :=
  TGLExt.TheTimeHasNoRank.the_post_is_only_the_limit hP hP1
-- o último conjunto é exatamente o termo do kernel
example {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] (P : A) :
    Filter.Tendsto (TheAxiomAndTheFalseWitness.axiomFlow P) Filter.atTop (nhds P) :=
  TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post P
-- T10.a (re-exportações)
example : type_of% @ChatgptAudit.PolarPeriod016.faithful_period_iff :=
  @TGLExt.TheTimeHasNoRank.clock_faithful_iff_one_turn
example : type_of% @ChatgptAudit.PolarPeriod016.reciprocal_temperature :=
  @TGLExt.TheTimeHasNoRank.clock_reciprocal_temperature
-- T10.b (pré-registrado com κ ≠ 0)
example {κ : ℝ} (_hκ : κ ≠ 0) (t : ℝ) : Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) :=
  TGLExt.TheTimeHasNoRank.clock_reads_modulo_period κ t
example (t u : ℝ) : Circle.exp (0 * t) = Circle.exp (0 * u) := TGLExt.TheTimeHasNoRank.frozen_clock t u
-- T10.c (re-exportações)
example : type_of% @TGLExt.IALDJones.angular_orbit_no_limit := @TGLExt.TheTimeHasNoRank.angle_has_no_limit
example : type_of% @TGLExt.IALDJones.angular_orbit_periodic := @TGLExt.TheTimeHasNoRank.angle_is_periodic
example : type_of% @TGLExt.IALDJones.orbit_tendsto_center := @TGLExt.TheTimeHasNoRank.damped_orbit_has_a_limit
example : type_of% @TGLExt.time_witnesses_noncoincidence := @TGLExt.TheTimeHasNoRank.decay_distinguishes_instants
-- T10.d
example (d : n → ℝ) (_hd : ∀ i, 0 < d i) (t : ℝ) (x : Matrix n n ℂ) (i j : n) :
    ‖sigma (rhoD d) t x i j‖ = ‖x i j‖ :=
  TGLExt.TheTimeHasNoRank.modular_clock_rotates_without_shrinking d t x i j
-- T10.e (re-exportações)
example : type_of% @TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post :=
  @TGLExt.TheTimeHasNoRank.the_post_is_not_moved
example : type_of% @TGLExt.gibbs_sigma := @TGLExt.TheTimeHasNoRank.the_state_is_not_moved
example : type_of% @TGLExt.sigma_omega := @TGLExt.TheTimeHasNoRank.the_vector_is_not_moved
-- T11.a (pré-registrado como optical_attractor_is_the_absolute_one)
example : (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) = absoluteRho (Fin 2) :=
  TGLExt.TheTimeHasNoRank.half_identity_is_absoluteRho_two
-- C-T1-c, C-T6-b (re-citações, tipo original)
example : type_of% @TGLV350.Regular.characterMultiplier_weyl := @TGLExt.TheTimeHasNoRank.weyl_pair_lives_in_L2
example : type_of% @TGLExt.purity_unitary_invariant := @TGLExt.TheTimeHasNoRank.unitary_keeps_purity

end PreReg

-- Controles e sondas: os tipos ficam impressos para o auditor (comparação com o texto pré-registrado)
#check @TGLExt.TheTimeHasNoRank.commutator_can_be_nonzero
#check @TGLExt.TheTimeHasNoRank.empty_dimension_admits_time
#check @TGLExt.TheTimeHasNoRank.probe_identity_flow_not_kms_inhabited
#check @TGLExt.TheTimeHasNoRank.finite_face_identity_flow_not_kms
#check @TGLExt.TheTimeHasNoRank.identity_flow_kms_pair_iff
#check @TGLExt.TheTimeHasNoRank.dephasing_lands_without_being_fixed
#check @TGLExt.TheTimeHasNoRank.no_coherence_no_loss
#check @TGLExt.TheTimeHasNoRank.purity_grows_backwards
#check @TGLExt.TheTimeHasNoRank.control_inverse_at_time_zero
#check @TGLExt.TheTimeHasNoRank.control_inverse_on_diagonal
#check @TGLExt.TheTimeHasNoRank.unitary_inverse_is_a_channel
#check @TGLExt.TheTimeHasNoRank.wrong_rate_breaks_scaling
#check @TGLExt.TheTimeHasNoRank.flow_of_one_is_idempotent
#check @TGLExt.TheTimeHasNoRank.flow_at_zero_is_idempotent
#check @TGLExt.TheTimeHasNoRank.frozen_clock_not_faithful
#check @TGLExt.TheTimeHasNoRank.decay_reading_has_no_period
#check @TGLExt.TheTimeHasNoRank.probe_bounded_spectral_translation
#check @TGLExt.TheTimeHasNoRank.scalar_decay_also_obeys_agape
#check @TGLExt.TheTimeHasNoRank.half_identity_has_full_rank
#check @TGLExt.TheTimeHasNoRank.half_identity_purity
#check @TGLExt.TheTimeHasNoRank.half_identity_freezes_the_clock
#check @TGLExt.TheTimeHasNoRank.no_finite_instant_is_the_post
#check @TGLExt.TheTimeHasNoRank.the_two_regimes_of_time
#check @TGLExt.TheTimeHasNoRank.light_flow_group
#check @TGLExt.TheTimeHasNoRank.light_modular_orbit_converges_iff_post
