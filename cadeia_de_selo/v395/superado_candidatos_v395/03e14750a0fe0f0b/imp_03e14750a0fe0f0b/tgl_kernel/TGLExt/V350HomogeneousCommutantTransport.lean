import TGLExt.V350RegularCoreCommutant
import TGLExt.V350ScalarModularInvariance

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory
noncomputable section

theorem characterPhase_neg_modularPhase (c x : ℝ) :
    characterPhase (-c) x = modularPhase x c := by
  unfold characterPhase modularPhase
  congr 1
  push_cast
  ring

theorem homogeneous_twistedCommutantLift (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (c : ℝ)
    (he : ∀ t : ℝ, modularConjugation P t D = modularPhase t c • D) :
    operatorFieldLift (twistedCommutantField P D) = characterMultiplier (-c) * fibre D := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (twistedCommutantField P D) f,
    characterMultiplier_ae (-c) (fibre D f),fibre_ae D f] with x h1 h2 h3
  change operatorFieldLift (twistedCommutantField P D) f x = characterMultiplier (-c) (fibre D f) x
  rw [h1,h2,h3]
  change modularConjugation P x D (f x) = characterPhase (-c) x • D (f x)
  rw [characterPhase_neg_modularPhase,he]
  rfl

/-- A homogeneous base commutant operator shifts the dual orbit. The sign
follows from the actual character multiplier, not a KMS convention assumed. -/
theorem homogeneous_commutant_dual_intertwines (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (c : ℝ)
    (hD : D ∈ (theFactorObject P).commutant)
    (he : ∀ t : ℝ, modularConjugation P t D = modularPhase t c • D)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s : ℝ) :
    dualAmbient s A.val * fibre D = fibre D * dualAmbient (s-c) A.val := by
  have hm := twistedCommutantLift_mem P D hD
  rw [homogeneous_twistedCommutantLift P D c he] at hm
  have hc := (VonNeumannAlgebra.mem_commutant_iff.mp hm) A.val A.property
  have hb : dualAmbient c A.val * fibre D = fibre D * A.val := by
    calc
      _ = characterMultiplier c * (A.val * (characterMultiplier (-c) * fibre D)) := by
        rw [dualAmbient_apply,characterMultiplier_star]
        simp only [mul_assoc]
      _ = characterMultiplier c * ((characterMultiplier (-c) * fibre D) * A.val) :=
        congrArg (fun T => characterMultiplier c * T) hc
      _ = _ := by rw [← mul_assoc,← mul_assoc,characterMultiplier_mul,add_neg_cancel,
        characterMultiplier_zero,one_mul]
  have ht := congrArg (dualAmbient (s-c)) hb
  simp only [map_mul,dualAmbient_fibre] at ht
  have hs : dualAmbient (s-c) (dualAmbient c A.val) = dualAmbient s A.val := by
    rw [← StarAlgEquiv.trans_apply,← dualAmbient_add]
    congr 1
    ring
  rwa [hs] at ht

#print axioms characterPhase_neg_modularPhase
#print axioms homogeneous_twistedCommutantLift
#print axioms homogeneous_commutant_dual_intertwines
end
end TGLV350.Regular
