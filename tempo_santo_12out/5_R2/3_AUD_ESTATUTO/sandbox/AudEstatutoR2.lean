import TheTimeIsNotAPost

/-! # Sonda do AUDITOR DE ESTATUTO (R2 da F1.TEMPO) sobre a pedra `TheTimeIsNotAPost` (fonte sha256 4d8a8259…)

Objetivo: conferir em Lean, importando SÓ o `.olean` recompilado neste sandbox, que
(a) os reforços E5.11 e E5.12 valem SEM as hipóteses retiradas (`_hd`, `κ ≠ 0`);
(b) os nomes renomeados por E5.06/E5.07/E5.08 têm o tipo que a docstring diz (nenhum tipo menciona
    «tempo», «rank» ou o canal ótico: são conjunções/igualdades sobre `sigma`, `axiomFlow`, `absoluteRho`);
(c) a versão de face finita obrigatória de T3.b(iii) (E5.13) existe e a sua forma negada segue dela;
(d) os seis controles AUD estão presentes com os tipos da auditoria R1;
(e) `probe_bounded_spectral_translation` já não é `True` (E5.09).
Nada aqui é teorema novo: só `example`/`#check`/`#print axioms` sobre a pedra. [INPUT do auditor] -/

set_option autoImplicit false

open TGLExt TGLExt.TheTimeIsNotAPost
open scoped Matrix ComplexOrder

noncomputable section

-- (a) E5.12: a leitura módulo o período vale para TODO κ (sem `κ ≠ 0`), inclusive κ = 0.
example (κ t : ℝ) : Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) :=
  clock_reads_modulo_period κ t
example (t : ℝ) : Circle.exp (0 * (t + 2 * Real.pi / 0)) = Circle.exp (0 * t) :=
  clock_reads_modulo_period 0 t

-- (a) E5.11: a invariância da pureza sob o fluxo modular de `rhoD d` vale para TODO `d` (sem positividade).
example {n : Type} [Fintype n] [DecidableEq n] (d : n → ℝ) (t : ℝ) (x : Matrix n n ℂ) :
    purityR (sigma (rhoD d) t x) = purityR x :=
  purityR_modular d t x
example (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    purityR (sigma (rhoD ![(-1 : ℝ), 0]) t x) = purityR x :=
  purityR_modular ![(-1 : ℝ), 0] t x

-- (b) E5.07: a cláusula composta é SÓ a conjunção T1.a ∧ T9.a ∧ T9.b ∧ T9.c ∧ limite; dela se extrai
--     cada membro, e nenhum membro fala de «rank» (o posto pleno é `flow_full_rank`, separado).
example {A : Type} [NormedRing A] [NormedAlgebra ℂ A] {P : A} (hP : IsIdempotentElem P) (hP1 : P ≠ 1) :
    ∀ t : ℝ, IsUnit (TheAxiomAndTheFalseWitness.axiomFlow P t) :=
  (the_time_is_not_a_post hP hP1).2.2.1
example {A : Type} [NormedRing A] [NormedAlgebra ℂ A] {P : A} (hP : IsIdempotentElem P) (hP1 : P ≠ 1) :
    Filter.Tendsto (TheAxiomAndTheFalseWitness.axiomFlow P) Filter.atTop (nhds P) :=
  (the_time_is_not_a_post hP hP1).2.2.2.2
example (n : ℕ) (P : Matrix (Fin n) (Fin n) ℂ) (hP : IsIdempotentElem P) (t : ℝ) :
    (TheAxiomAndTheFalseWitness.axiomFlow P t).rank = n :=
  flow_full_rank n P hP t

-- (b) E5.06: o grupo KMS vale para ρ = 1 (fluxo congelado) — o nome não pode afirmar «tempo».
example : ∀ a, sigma (1 : Matrix (Fin 2) (Fin 2) ℂ) 0 a = a :=
  (modular_flow_is_a_kms_group (1 : Matrix (Fin 2) (Fin 2) ℂ) Matrix.PosDef.one).1
example : ∀ s t a, sigma (1 : Matrix (Fin 2) (Fin 2) ℂ) s (sigma 1 t a) = sigma 1 (s + t) a :=
  (modular_flow_is_a_kms_group (1 : Matrix (Fin 2) (Fin 2) ℂ) Matrix.PosDef.one).2.1

-- (b) E5.08: as duas igualdades de T11 não mencionam canal ótico algum.
example : (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) = absoluteRho (Fin 2) :=
  half_identity_is_absoluteRho_two
example (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    sigma ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) t a = a :=
  half_identity_clock_stops t a
-- …e a versão COM o canal (opcional feita) é sobre populações em ℝ², genérica em θ.
example {θ : ℝ} (hθ : Real.sin θ ≠ 0) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x = x ↔ x 0 = x 1 :=
  optical_channel_fixed_state_is_half_identity hθ x

-- (c) E5.13: face finita obrigatória e forma negada.
example : gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 1; 0, 0] * !![0, 0; 1, 0])
      ≠ gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) :=
  identity_flow_not_kms_finite
example : ¬ ∀ x y : Matrix (Fin 2) (Fin 2) ℂ,
      gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (x * y) = gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (y * x) :=
  identity_flow_not_kms_finite'
-- a ligação com a forma KMS de Gibbs da pedra: para o fluxo identidade (Delta = id) a cláusula (vii) de
-- `modular_flow_is_a_kms_group` reduz-se a ω(ab) = ω(ba); com Delta ρ ≠ id a cláusula vale (T3.a).
example (ρ : Matrix (Fin 2) (Fin 2) ℂ) (hρ : ρ.PosDef) (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    gibbs ρ (a * b) = gibbs ρ (b * Delta ρ a) :=
  (modular_flow_is_a_kms_group ρ hρ).2.2.2.2.2.2.1 a b

-- (d) os controles AUD, com os tipos da auditoria R1.
example (x : Matrix (Fin 2) (Fin 2) ℂ) (hx : x 0 1 ≠ 0) : ∀ s : ℝ, 0 < scalarScaling.tau (scalarScaling.theta s x) :=
  (aud_scalar_obeys_agape x hx).2.2.2.1
example : (scalarScaling.theta 1 (1 : Matrix (Fin 2) (Fin 2) ℂ)).trace ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ).trace :=
  aud_scalar_erases_the_record
example (s : ℝ) : ¬ ∀ v : Fin 2 → ℝ,
    Filter.Tendsto (fun k : ℕ => ((TGLExt.boost s) ^ k).mulVec v) Filter.atTop (nhds 0) :=
  aud_boost_has_no_global_attractor s
example : IsIdempotentElem (!![1 / 2, 1 / 2; 1 / 2, 1 / 2] : Matrix (Fin 2) (Fin 2) ℝ) :=
  aud_discrete_step_can_be_a_post
example : ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).rank = 2 := aud_attractor_state_has_full_rank
example : purityR ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 1 / 2 := aud_attractor_state_purity_half
example (a b : ℝ) (ha : 0 < a) (hb : 0 < b) (hab : a ≠ b) :
    ¬ ∀ t : ℝ, sigma (rhoD ![a, b]) t (!![0, 1; 0, 0] : Matrix (Fin 2) (Fin 2) ℂ) = !![0, 1; 0, 0] :=
  aud_clock_runs_unless_equal_populations a b ha hb hab
example (a t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) : sigma (rhoD ![a, a]) t x = x :=
  aud_clock_stops_when_equal_populations a t x
example (s : ℝ) : (TGLExt.boost s)ᵀ * !![0, 1; -1, 0] * TGLExt.boost s = !![0, 1; -1, 0] :=
  aud_boost_is_symplectic s

-- (e) E5.09: a sonda tem enunciado (se fosse `True`, este `example` não tiparia).
example : (((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ)⁻¹ : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ) * 0
        * ((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ)
      ≠ 0 + algebraMap ℂ (Matrix (Fin 2) (Fin 2) ℂ) 1 :=
  probe_bounded_spectral_translation

-- Tipos impressos para a leitura nome × termo (registro).
#check @the_time_is_not_a_post
#check @modular_flow_is_a_kms_group
#check @half_identity_is_absoluteRho_two
#check @half_identity_clock_stops
#check @identity_flow_not_kms_finite
#check @nontracial_state_rejects_the_identity_flow
#check @light_flow_group
#check @light_modular_orbit_converges_iff_post
#check @probe_identity_flow_not_kms_inhabited
#check @the_two_regimes_of_time

#print axioms TGLExt.TheTimeIsNotAPost.the_time_is_not_a_post
#print axioms TGLExt.TheTimeIsNotAPost.modular_flow_is_a_kms_group
#print axioms TGLExt.TheTimeIsNotAPost.identity_flow_not_kms_finite
#print axioms TGLExt.TheTimeIsNotAPost.probe_identity_flow_not_kms_inhabited
#print axioms TGLExt.TheTimeIsNotAPost.clock_reads_modulo_period
#print axioms TGLExt.TheTimeIsNotAPost.purityR_modular
#print axioms TGLExt.TheTimeIsNotAPost.half_identity_clock_stops
#print axioms TGLExt.TheTimeIsNotAPost.aud_boost_is_symplectic

end
