import TGLExt.TimeGravitonFlow
import TGLExt.PageInformation
import TGLExt.Bicommutant

/-!
# The rule as a quadratic residual of the existing reading

The reading Eg, its flow, the inscription type and the Frobenius form are
reused. No new network or dynamical hypothesis is introduced. For a target A
fixed before evaluation, residual A X is the squared Frobenius distance from
Eg X to A, not the distance from the raw state X to A. Its invariance is proved
from reading_flow; it is not assumed and is not a decreasing progress score.

An inscription is a realizable fixed target. The zero criterion and invariance
also hold for arbitrary targets, while an impossible target has positive
residual everywhere. Concrete accepted and rejected controls share the same
transported density and differ only in the target. The construction is M2;
its interpretation as a rule is the explicit representation of
RuleTruthContract. No physical confirmation or global spacetime is asserted.
-/
set_option autoImplicit false
set_option maxHeartbeats 1600000
open Matrix Complex
namespace TGLExt.RuleQuadraticResidual
open TimeGravitonMatrix TimeGravitonFlow RuleTruthContract
noncomputable section

theorem purityR_nonnegative {n : Type} [Fintype n] [DecidableEq n]
    (X : Matrix n n ℂ) : 0 ≤ purityR X := by
  exact Finset.sum_nonneg fun i _ => Finset.sum_nonneg fun j _ =>
    Complex.normSq_nonneg (X i j)

theorem purityR_zero_iff {n : Type} [Fintype n] [DecidableEq n]
    (X : Matrix n n ℂ) : purityR X = 0 ↔ X = 0 := by
  have bridge : frob X X = (purityR X : ℂ) := by
    calc
      frob X X = purity X := Matrix.trace_mul_comm _ _
      _ = (purityR X : ℂ) := purityR_eq X
  constructor
  · intro h
    apply (frob_self_eq_zero_iff X).mp
    rw [bridge, h]
    simp
  · rintro rfl
    simp [purityR]

def residual (A X : M2) : ℝ := purityR (Eg X - A)

theorem residual_nonnegative (A X : M2) : 0 ≤ residual A X :=
  purityR_nonnegative _

theorem residual_zero_iff (A X : M2) :
    residual A X = 0 ↔ Admissible Eg A X := by
  unfold residual Admissible
  rw [purityR_zero_iff, sub_eq_zero]

theorem residual_positive_iff (A X : M2) :
    0 < residual A X ↔ ¬ Admissible Eg A X := by
  constructor
  · intro hp ha
    have hz := (residual_zero_iff A X).mpr ha
    linarith
  · intro ha
    have hn := residual_nonnegative A X
    by_contra hp
    have hz : residual A X = 0 := le_antisymm (le_of_not_gt hp) hn
    exact ha ((residual_zero_iff A X).mp hz)

theorem residual_flow (A X : M2) (rate omega time : ℝ) :
    residual A (flow rate omega time X) = residual A X := by
  simp only [residual, reading_flow]

theorem residual_time_continuous (A X : M2) (rate omega : ℝ) :
    Continuous (fun time : ℝ => residual A (flow rate omega time X)) := by
  simpa only [residual_flow] using
    (continuous_const : Continuous (fun _ : ℝ => residual A X))

theorem residual_time_derivative_zero (A X : M2) (rate omega time : ℝ) :
    HasDerivAt (fun s : ℝ => residual A (flow rate omega s X)) 0 time := by
  simpa only [residual_flow] using (hasDerivAt_const time (residual A X))

theorem inscription_has_zero_residual (A : RuleContinuousMotor.Inscription Eg) :
    residual A.val A.val = 0 := by
  exact (residual_zero_iff _ _).mpr A.property

theorem inscription_residual_zero_iff (A X : RuleContinuousMotor.Inscription Eg) :
    residual A.val X.val = 0 ↔ X = A := by
  rw [residual_zero_iff]
  change Eg X.val = A.val ↔ X = A
  rw [X.property]
  exact Subtype.ext_iff.symm

theorem impossible_anchor_positive (A : M2) (ha : Eg A ≠ A) (X : M2) :
    0 < residual A X := by
  apply (residual_positive_iff A X).mpr
  intro h
  have hi := Eg_idem X
  change Eg X = A at h
  rw [h] at hi
  exact ha hi

def anchor : M2 := (1/2 : ℂ) • (1 : M2)

theorem anchor_fixed : Eg anchor = anchor := by
  simp only [anchor, map_smul, Eg_one]

def anchorInscription : RuleContinuousMotor.Inscription Eg := ⟨anchor, anchor_fixed⟩

theorem transported_accepted : residual anchor transportedRho = 0 := by
  apply (residual_zero_iff _ _).mpr
  exact transported_reading

theorem changed_anchor_residual : residual projPlus transportedRho = 1/2 := by
  unfold residual
  rw [transported_reading, IALDGraviton.projPlus_entries]
  norm_num [purityR, Fin.sum_univ_two, Matrix.smul_apply, Matrix.sub_apply,
    Matrix.one_apply, Complex.normSq_apply]

theorem transported_is_not_anchor : transportedRho ≠ anchor := by
  intro h
  have hc := congrArg (fun X : M2 => X 0 1) h
  rw [density_transport] at hc
  norm_num [PxMinus, anchor, hCrossC] at hc

theorem changed_anchor_rejected (rate omega time : ℝ) :
    ¬ Admissible Eg projPlus (flow rate omega time transportedRho) := by
  apply (residual_positive_iff _ _).mp
  rw [residual_flow, changed_anchor_residual]
  norm_num

theorem accepted_along_flow (rate omega time : ℝ) :
    residual anchor (flow rate omega time transportedRho) = 0 := by
  rw [residual_flow, transported_accepted]

theorem inhabited_and_discriminating :
    ∃ A X : M2, Eg A = A ∧ residual A X = 0 ∧ X ≠ A ∧
      residual projPlus X = 1/2 :=
  ⟨anchor, transportedRho, anchor_fixed, transported_accepted,
    transported_is_not_anchor, changed_anchor_residual⟩

end
end TGLExt.RuleQuadraticResidual

#print axioms TGLExt.RuleQuadraticResidual.purityR_nonnegative
#print axioms TGLExt.RuleQuadraticResidual.purityR_zero_iff
#print axioms TGLExt.RuleQuadraticResidual.residual_nonnegative
#print axioms TGLExt.RuleQuadraticResidual.residual_zero_iff
#print axioms TGLExt.RuleQuadraticResidual.residual_positive_iff
#print axioms TGLExt.RuleQuadraticResidual.residual_flow
#print axioms TGLExt.RuleQuadraticResidual.residual_time_continuous
#print axioms TGLExt.RuleQuadraticResidual.residual_time_derivative_zero
#print axioms TGLExt.RuleQuadraticResidual.inscription_has_zero_residual
#print axioms TGLExt.RuleQuadraticResidual.inscription_residual_zero_iff
#print axioms TGLExt.RuleQuadraticResidual.impossible_anchor_positive
#print axioms TGLExt.RuleQuadraticResidual.anchor_fixed
#print axioms TGLExt.RuleQuadraticResidual.transported_accepted
#print axioms TGLExt.RuleQuadraticResidual.changed_anchor_residual
#print axioms TGLExt.RuleQuadraticResidual.transported_is_not_anchor
#print axioms TGLExt.RuleQuadraticResidual.changed_anchor_rejected
#print axioms TGLExt.RuleQuadraticResidual.accepted_along_flow
#print axioms TGLExt.RuleQuadraticResidual.inhabited_and_discriminating
