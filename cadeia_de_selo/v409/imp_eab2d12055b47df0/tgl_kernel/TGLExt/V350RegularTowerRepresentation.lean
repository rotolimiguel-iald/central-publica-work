import TGLExt.V350L2Translation
import TGLExt.V350L2StrongContinuity
import TGLExt.TheModularFlowIsAHorizon
import TGLExt.V350WedgeModularData

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- Regular covariant representation in the constant-fibre picture.
This is built from the same tower modular flow as towerWedgeData. -/
def regularUnitary (P : SiteProfile) (t : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) :=
  fibre (modularFlowCLM P t) * shift t

theorem regular_zero (P : SiteProfile) : regularUnitary P 0 = 1 := by
  simp only [regularUnitary, modularFlowCLM_zero, fibre_one, shift_zero, mul_one]

theorem regular_mul (P : SiteProfile) (s t : ℝ) :
    regularUnitary P s * regularUnitary P t = regularUnitary P (s+t) := by
  unfold regularUnitary
  calc
    (fibre (modularFlowCLM P s) * shift s) * (fibre (modularFlowCLM P t) * shift t)
        = fibre (modularFlowCLM P s) * (shift s * fibre (modularFlowCLM P t)) * shift t := by
          simp only [mul_assoc]
    _ = fibre (modularFlowCLM P s) * (fibre (modularFlowCLM P t) * shift s) * shift t := by
          rw [shift_commutes_fibre]
    _ = (fibre (modularFlowCLM P s) * fibre (modularFlowCLM P t)) * (shift s * shift t) := by
          simp only [mul_assoc]
    _ = fibre (modularFlowCLM P (s+t)) * shift (s+t) := by
          rw [← fibre_mul, modularFlowCLM_mul, shift_mul]

theorem regular_star (P : SiteProfile) (t : ℝ) :
    star (regularUnitary P t) = regularUnitary P (-t) := by
  unfold regularUnitary
  rw [star_mul, shift_star, ← fibre_star, modularFlowCLM_star, shift_commutes_fibre]

theorem regular_unitary (P : SiteProfile) (t : ℝ) :
    star (regularUnitary P t) * regularUnitary P t = 1 ∧
      regularUnitary P t * star (regularUnitary P t) = 1 := by
  constructor
  · rw [regular_star, regular_mul, neg_add_cancel, regular_zero]
  · rw [regular_star, regular_mul, add_neg_cancel, regular_zero]

theorem shift_fibre_sandwich {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (t : ℝ) (A : H →L[ℂ] H) :
    shift t * fibre A * shift (-t) = fibre A := by
  rw [shift_commutes_fibre, mul_assoc, shift_mul, add_neg_cancel, shift_zero, mul_one]

theorem regular_covariance (P : SiteProfile) (t : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    regularUnitary P t * fibre A * star (regularUnitary P t) =
      fibre (modularConjugation P t A) := by
  rw [modularConjugation_eq_sandwich, fibre_mul, fibre_mul, fibre_star]
  unfold regularUnitary
  calc
    (fibre (modularFlowCLM P t) * shift t) * fibre A *
        star (fibre (modularFlowCLM P t) * shift t)
      = fibre (modularFlowCLM P t) * (shift t * fibre A * star (shift (H := TowerHilbert P) t)) *
          star (fibre (modularFlowCLM P t)) := by simp only [star_mul, mul_assoc]
    _ = fibre (modularFlowCLM P t) * fibre A * star (fibre (modularFlowCLM P t)) := by
          rw [shift_star, shift_fibre_sandwich]

theorem modularFlowCLM_isometry (P : SiteProfile) (t : ℝ) :
    modularFlowCLM P t = (modularFlowIsometry P t).toContinuousLinearMap := by
  ext v
  rfl

theorem regular_strongly_continuous (P : SiteProfile)
    (f : RegularHilbert (TowerHilbert P)) :
    Continuous (fun t : ℝ => regularUnitary P t f) := by
  have h := fibre_jointly_continuous (H := TowerHilbert P) (Z := ℝ) (modularFlowIsometry P)
    (fun v => modularFlow_strongly_continuous v)
  have hpair : Continuous (fun t : ℝ => (shift (H := TowerHilbert P) t f, t)) :=
    (shift_strongly_continuous (H := TowerHilbert P) f).prodMk continuous_id
  have hc := h.comp hpair
  refine hc.congr ?_
  intro t
  change fibre (modularFlowIsometry P t).toContinuousLinearMap (shift t f) = regularUnitary P t f
  simp only [regularUnitary, mul_apply_eq_comp, modularFlowCLM_isometry]

/-- The covariance above restricts to precisely the factor used by the wedge data. -/
theorem regular_covariance_on_factor (P : SiteProfile) (t : ℝ)
    (A : (theFactorObject P).toStarSubalgebra) :
    regularUnitary P t * fibre (A : TowerHilbert P →L[ℂ] TowerHilbert P) *
        star (regularUnitary P t) =
      fibre ((TGLExt.V350Continuous.factorFlow P t A) : TowerHilbert P →L[ℂ] TowerHilbert P) :=
  regular_covariance P t A

#print axioms regular_mul
#print axioms regular_unitary
#print axioms regular_covariance_on_factor
#print axioms regular_strongly_continuous
end
end TGLV350.Regular
