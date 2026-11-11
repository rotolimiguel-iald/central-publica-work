import TGLExt.RuleTruthContract
import TGLExt.IALD
import TGLExt.IALDJones
import TGLExt.CondExpect

/-!
# The rule in the existing continuous motor (sandbox candidate)

The operator's instruction, verbatim:
"Agora ligamos tudo no motor contínuo e ele precisa rodar"

[INPUT] A rule has a target fixed independently of its output. Admissibility is
equality of the preserved inscription with that target. The ontology of rule,
right and truth is not asserted as a physical theorem by this implementation.

This module connects RuleTruthContract to the actual IALDJones.orbit and
IALD.motor. The matrix example uses TGLExt.eD (diagonal pinching), with a
proved equality E(X)=PXP+QXQ. It does NOT identify that map with the corner
IALDJones.jonesReading e X=eXe. The vector motor and matrix flow are also not
identified with each other: each gets its own typed satisfaction theorem.

The rate is arbitrary and positive only where convergence is claimed.
The experiment may instantiate it with beta computed at runtime; no physical
beta identification is proved here. The immutable target in the concrete
example is I/2; the off-diagonal initial perturbation is separate.
At every finite time the raw off-diagonal part remains unless initially zero.
Reading satisfaction therefore does not mean finite-time raw convergence.
-/
set_option autoImplicit false

namespace TGLExt.RuleContinuousMotor

open TGLExt.RuleTruthContract TGLExt.IALDJones Filter Topology
noncomputable section

section GeneralFlow
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]

abbrev Inscription (E : V →ₗ[ℂ] V) := {x : V // E x = x}

def inscribe (E : V →ₗ[ℂ] V) (hE : ∀ x, E (E x) = E x) (x : V) :
    Inscription E := ⟨E x, hE x⟩

theorem inscription_reading_faithful (E : V →ₗ[ℂ] V) :
    Function.Injective (fun x : Inscription E => E x.val) := by
  intro x y h
  apply Subtype.ext
  simpa only [x.property, y.property] using h

theorem rule_on_inscriptions_is_equality (E : V →ₗ[ℂ] V)
    (target : Inscription E) (x : Inscription E) :
    Admissible (fun z : Inscription E => E z.val) target.val x ↔ x = target :=
  admissible_iff_eq_of_injective _ _ (inscription_reading_faithful E)
    target target.property x

theorem unique_sound_complete_rule (E : V →ₗ[ℂ] V)
    (target : Inscription E) (C : Inscription E → Prop)
    (hs : SoundRule (fun z : Inscription E => E z.val) target.val C)
    (hc : CompleteRule (fun z : Inscription E => E z.val) target.val C) :
    C = (fun z => z = target) := by
  funext z
  exact propext ((sound_complete_iff _ _ _ hs hc z).trans
    (rule_on_inscriptions_is_equality E target z))

theorem flow_preserves_rule (E : V →ₗ[ℂ] V) (hE : ∀ x, E (E x) = E x)
    (target x : V) (rate frequency time : ℝ) :
    Admissible E target (orbit E rate frequency time x) ↔ Admissible E target x := by
  unfold Admissible
  rw [orbit_center hE]

theorem flow_inscription_is_stationary (E : V →ₗ[ℂ] V)
    (hE : ∀ x, E (E x) = E x) (x : V) (rate frequency time : ℝ) :
    inscribe E hE (orbit E rate frequency time x) = inscribe E hE x := by
  apply Subtype.ext
  exact orbit_center hE rate frequency time x

theorem flow_satisfies_fixed_target_iff (E : V →ₗ[ℂ] V)
    (hE : ∀ x, E (E x) = E x) (target : Inscription E)
    (x : V) (rate frequency time : ℝ) :
    inscribe E hE (orbit E rate frequency time x) = target ↔ E x = target.val := by
  rw [flow_inscription_is_stationary]
  exact Subtype.ext_iff

theorem flow_semigroup (E : V →ₗ[ℂ] V) (hE : ∀ x, E (E x) = E x)
    (x : V) (rate frequency s t : ℝ) :
    orbit E rate frequency (s+t) x = orbit E rate frequency s (orbit E rate frequency t x) :=
  orbit_add hE rate frequency s t x

theorem flow_starts_at_input (E : V →ₗ[ℂ] V) (x : V) (rate frequency : ℝ) :
    orbit E rate frequency 0 x = x := by
  simp [orbit, spin, coeff]

theorem flow_continuous (E : V →ₗ[ℂ] V) (x : V) (rate frequency : ℝ) :
    Continuous (fun time : ℝ => orbit E rate frequency time x) := by
  unfold orbit spin coeff
  fun_prop

theorem flow_converges_to_inscription (E : V →ₗ[ℂ] V) (x : V)
    {rate : ℝ} (hRate : 0 < rate) (frequency : ℝ) :
    Tendsto (fun time => orbit E rate frequency time x) atTop (nhds (E x)) :=
  orbit_tendsto_center E hRate frequency x

theorem raw_finite_output_not_inscription (E : V →ₗ[ℂ] V) (x : V)
    (hx : x ≠ E x) (rate frequency time : ℝ) :
    orbit E rate frequency time x ≠ E x := by
  intro h
  have hnorm := norm_orbit_sub_center E rate frequency time x
  rw [h, sub_self, norm_zero] at hnorm
  have hpos : 0 < Real.exp (-(rate*time)) * ‖x-E x‖ :=
    mul_pos (Real.exp_pos _) (norm_pos_iff.mpr (sub_ne_zero.mpr hx))
  exact (ne_of_gt hpos) hnorm.symm

theorem wrong_target_stays_rejected (E : V →ₗ[ℂ] V)
    (hE : ∀ x, E (E x) = E x) (x target : V) (hWrong : E x ≠ target)
    (rate frequency time : ℝ) :
    ¬ Admissible E target (orbit E rate frequency time x) := by
  rw [flow_preserves_rule E hE]
  exact hWrong

end GeneralFlow

section VectorMotor
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
open TGLExt.TheVerbSelectsTheAction

/-- Exact satisfaction criterion for the existing vector motor, for an
independently supplied target. No matrix pinching equality is asserted. -/
theorem vector_motor_satisfies_iff (a target ψ : H) (U : H →L[ℂ] H) (rate time : ℝ) :
    IALD.motor a U rate time ψ = target ↔ post a (U ψ) = target := by
  rw [IALD.the_reading_absorbs_the_dephasing]

theorem vector_motor_rule_ignores_rate_and_time (a target ψ : H)
    (U : H →L[ℂ] H) (r t r' t' : ℝ) :
    (IALD.motor a U r t ψ = target) ↔ (IALD.motor a U r' t' ψ = target) := by
  rw [vector_motor_satisfies_iff, vector_motor_satisfies_iff]

end VectorMotor

section MatrixWitness
abbrev Mat := Matrix (Fin 2) (Fin 2) ℂ
def E : Mat →ₗ[ℂ] Mat := TGLExt.eD
def P : Mat := Matrix.diagonal ![1,0]
def Q : Mat := Matrix.diagonal ![0,1]
def target : Mat := !![(1/2 : ℂ),0;0,(1/2 : ℂ)]
def initial : Mat := !![(1/2 : ℂ),(1/4 : ℂ);(1/4 : ℂ),(1/2 : ℂ)]
def wrongInitial : Mat := !![(3/4 : ℂ),(1/4 : ℂ);(1/4 : ℂ),(1/4 : ℂ)]

theorem E_idempotent (x : Mat) : E (E x) = E x := TGLExt.diagExpect_idem x

theorem E_is_two_face_pinching (x : Mat) : E x = P*x*P + Q*x*Q := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [E, TGLExt.eD, TGLExt.diagExpect, P, Q, Matrix.diagonal_mul, Matrix.mul_diagonal]

theorem target_is_fixed : E target = target := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [E,TGLExt.eD,TGLExt.diagExpect,target]

theorem initial_has_target_reading : E initial = target := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [E,TGLExt.eD,TGLExt.diagExpect,initial,target]

theorem target_nonzero : target ≠ 0 := by
  intro h
  have h00 := congrArg (fun x : Mat => x 0 0) h
  norm_num [target] at h00

theorem initial_not_fixed : initial ≠ E initial := by
  rw [initial_has_target_reading]
  intro h
  have h01 := congrArg (fun x : Mat => x 0 1) h
  norm_num [initial,target] at h01

theorem wrong_initial_rejected : E wrongInitial ≠ target := by
  intro h
  have h00 := congrArg (fun x : Mat => x 0 0) h
  norm_num [E,TGLExt.eD,TGLExt.diagExpect,wrongInitial,target] at h00

def due : Inscription E := ⟨target, target_is_fixed⟩

theorem matrix_flow_satisfies_declared_target (rate time : ℝ) :
    inscribe E E_idempotent (orbit E rate 0 time initial) = due := by
  apply (flow_satisfies_fixed_target_iff E E_idempotent due initial rate 0 time).mpr
  exact initial_has_target_reading

theorem matrix_wrong_input_never_satisfies (rate time : ℝ) :
    ¬ Admissible E target (orbit E rate 0 time wrongInitial) :=
  wrong_target_stays_rejected E E_idempotent wrongInitial target wrong_initial_rejected rate 0 time

theorem matrix_raw_finite_output_not_target (rate time : ℝ) :
    orbit E rate 0 time initial ≠ target := by
  rw [← initial_has_target_reading]
  exact raw_finite_output_not_inscription E initial initial_not_fixed rate 0 time

theorem matrix_flow_converges {rate : ℝ} (hRate : 0 < rate) :
    Tendsto (fun time => orbit E rate 0 time initial) atTop (nhds target) := by
  rw [← initial_has_target_reading]
  exact flow_converges_to_inscription E initial hRate 0

theorem inhabited_and_discriminating (rate time : ℝ) :
    target ≠ 0 ∧
    Admissible E target (orbit E rate 0 time initial) ∧
    ¬ Admissible E target (orbit E rate 0 time wrongInitial) := by
  refine ⟨target_nonzero, ?_, matrix_wrong_input_never_satisfies rate time⟩
  rw [flow_preserves_rule E E_idempotent]
  exact initial_has_target_reading

end MatrixWitness

/-! The consumer's actual M4 block pinching and target, pinned in
PREREGISTRO_R1.json before the run. This section, rather than the auxiliary
M2 witness, supplies the direct bridge to that consumer. -/
section ActualConsumerM4
abbrev Mat4 := Matrix (Fin 4) (Fin 4) ℂ

def E4 : Mat4 →ₗ[ℂ] Mat4 where
  toFun x i j := if (i.val < 2 ↔ j.val < 2) then x i j else 0
  map_add' x y := by
    ext i j
    dsimp
    split_ifs <;> simp
  map_smul' c x := by
    ext i j
    dsimp
    split_ifs <;> simp

def P4 : Mat4 := Matrix.diagonal (fun i => if i.val < 2 then 1 else 0)
def Q4 : Mat4 := Matrix.diagonal (fun i => if i.val < 2 then 0 else 1)
def target4 : Mat4 :=
  !![(1/4:ℂ), -Complex.I/4, 0, 0;
     Complex.I/4, (1/4:ℂ), 0, 0;
     0, 0, (1/4:ℂ), Complex.I/4;
     0, 0, -Complex.I/4, (1/4:ℂ)]
def psi4 : Fin 4 → ℂ := ![(1/2:ℂ), Complex.I/2, (1/2:ℂ), -Complex.I/2]
def initial4 : Mat4 := fun i j => psi4 i * star (psi4 j)
def incompatibleTarget4 : Mat4 := (1/4:ℂ) • (1:Mat4)

theorem E4_idempotent (x : Mat4) : E4 (E4 x) = E4 x := by
  ext i j
  simp only [E4, LinearMap.coe_mk, AddHom.coe_mk]
  split_ifs <;> rfl

theorem E4_is_consumer_pinching (x : Mat4) : E4 x = P4*x*P4 + Q4*x*Q4 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [E4,P4,Q4,Matrix.diagonal_mul,Matrix.mul_diagonal]

theorem consumer_faces_sum_identity : P4 + Q4 = (1:Mat4) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [P4,Q4]

theorem target4_fixed : E4 target4 = target4 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [E4,target4]

theorem initial4_has_preregistered_reading : E4 initial4 = target4 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [E4,initial4,psi4,target4,Complex.star_def,Complex.conj_I] <;>
    ring_nf <;> norm_num [pow_two, Complex.I_mul_I]

theorem target4_nonzero : target4 ≠ 0 := by
  intro h
  have h00 := congrArg (fun x : Mat4 => x 0 0) h
  norm_num [target4] at h00

theorem initial4_not_fixed : initial4 ≠ E4 initial4 := by
  rw [initial4_has_preregistered_reading]
  intro h
  have h02 := congrArg (fun x : Mat4 => x 0 2) h
  norm_num [initial4,psi4,target4,Complex.star_def,Matrix.cons_val_two] at h02

theorem incompatible_target4_differs : target4 ≠ incompatibleTarget4 := by
  intro h
  have h01 := congrArg (fun x : Mat4 => x 0 1) h
  have hi := congrArg Complex.im h01
  norm_num [target4,incompatibleTarget4,div_eq_mul_inv] at hi

theorem pinching_is_not_corner : E4 target4 ≠ P4*target4*P4 := by
  rw [target4_fixed]
  intro h
  have h22 := congrArg (fun x : Mat4 => x 2 2) h
  norm_num [P4,target4,Matrix.diagonal_mul,Matrix.mul_diagonal,Matrix.cons_val_two] at h22

theorem actual_flow_formula (x : Mat4) (rate time : ℝ) :
    orbit E4 rate 0 time x = E4 x + coeff rate time • (x-E4 x) := by
  simp [orbit,spin]

theorem actual_flow_rule (rate time : ℝ) :
    Admissible E4 target4 (orbit E4 rate 0 time initial4) := by
  rw [flow_preserves_rule E4 E4_idempotent]
  exact initial4_has_preregistered_reading

theorem actual_flow_rejects_incompatible_target (rate time : ℝ) :
    ¬ Admissible E4 incompatibleTarget4 (orbit E4 rate 0 time initial4) := by
  apply wrong_target_stays_rejected E4 E4_idempotent
  rw [initial4_has_preregistered_reading]
  exact incompatible_target4_differs

theorem actual_flow_continuous (rate : ℝ) :
    Continuous (fun time : ℝ => orbit E4 rate 0 time initial4) :=
  flow_continuous E4 initial4 rate 0

theorem actual_flow_semigroup (rate s t : ℝ) :
    orbit E4 rate 0 (s+t) initial4 = orbit E4 rate 0 s (orbit E4 rate 0 t initial4) :=
  flow_semigroup E4 E4_idempotent initial4 rate 0 s t

theorem actual_flow_converges {rate : ℝ} (hRate : 0 < rate) :
    Tendsto (fun time => orbit E4 rate 0 time initial4) atTop (nhds target4) := by
  rw [← initial4_has_preregistered_reading]
  exact flow_converges_to_inscription E4 initial4 hRate 0

theorem actual_raw_finite_output_not_target (rate time : ℝ) :
    orbit E4 rate 0 time initial4 ≠ target4 := by
  rw [← initial4_has_preregistered_reading]
  exact raw_finite_output_not_inscription E4 initial4 initial4_not_fixed rate 0 time

end ActualConsumerM4
end
end TGLExt.RuleContinuousMotor

#print axioms TGLExt.RuleContinuousMotor.inscription_reading_faithful
#print axioms TGLExt.RuleContinuousMotor.rule_on_inscriptions_is_equality
#print axioms TGLExt.RuleContinuousMotor.unique_sound_complete_rule
#print axioms TGLExt.RuleContinuousMotor.flow_preserves_rule
#print axioms TGLExt.RuleContinuousMotor.flow_inscription_is_stationary
#print axioms TGLExt.RuleContinuousMotor.flow_satisfies_fixed_target_iff
#print axioms TGLExt.RuleContinuousMotor.flow_semigroup
#print axioms TGLExt.RuleContinuousMotor.flow_starts_at_input
#print axioms TGLExt.RuleContinuousMotor.flow_continuous
#print axioms TGLExt.RuleContinuousMotor.flow_converges_to_inscription
#print axioms TGLExt.RuleContinuousMotor.raw_finite_output_not_inscription
#print axioms TGLExt.RuleContinuousMotor.wrong_target_stays_rejected
#print axioms TGLExt.RuleContinuousMotor.vector_motor_satisfies_iff
#print axioms TGLExt.RuleContinuousMotor.vector_motor_rule_ignores_rate_and_time
#print axioms TGLExt.RuleContinuousMotor.E_idempotent
#print axioms TGLExt.RuleContinuousMotor.E_is_two_face_pinching
#print axioms TGLExt.RuleContinuousMotor.target_is_fixed
#print axioms TGLExt.RuleContinuousMotor.initial_has_target_reading
#print axioms TGLExt.RuleContinuousMotor.target_nonzero
#print axioms TGLExt.RuleContinuousMotor.initial_not_fixed
#print axioms TGLExt.RuleContinuousMotor.wrong_initial_rejected
#print axioms TGLExt.RuleContinuousMotor.matrix_flow_satisfies_declared_target
#print axioms TGLExt.RuleContinuousMotor.matrix_wrong_input_never_satisfies
#print axioms TGLExt.RuleContinuousMotor.matrix_raw_finite_output_not_target
#print axioms TGLExt.RuleContinuousMotor.matrix_flow_converges
#print axioms TGLExt.RuleContinuousMotor.inhabited_and_discriminating

#print axioms TGLExt.RuleContinuousMotor.E4_idempotent
#print axioms TGLExt.RuleContinuousMotor.E4_is_consumer_pinching
#print axioms TGLExt.RuleContinuousMotor.consumer_faces_sum_identity
#print axioms TGLExt.RuleContinuousMotor.target4_fixed
#print axioms TGLExt.RuleContinuousMotor.initial4_has_preregistered_reading
#print axioms TGLExt.RuleContinuousMotor.target4_nonzero
#print axioms TGLExt.RuleContinuousMotor.initial4_not_fixed
#print axioms TGLExt.RuleContinuousMotor.incompatible_target4_differs
#print axioms TGLExt.RuleContinuousMotor.pinching_is_not_corner
#print axioms TGLExt.RuleContinuousMotor.actual_flow_formula
#print axioms TGLExt.RuleContinuousMotor.actual_flow_rule
#print axioms TGLExt.RuleContinuousMotor.actual_flow_rejects_incompatible_target
#print axioms TGLExt.RuleContinuousMotor.actual_flow_continuous
#print axioms TGLExt.RuleContinuousMotor.actual_flow_semigroup
#print axioms TGLExt.RuleContinuousMotor.actual_flow_converges
#print axioms TGLExt.RuleContinuousMotor.actual_raw_finite_output_not_target
