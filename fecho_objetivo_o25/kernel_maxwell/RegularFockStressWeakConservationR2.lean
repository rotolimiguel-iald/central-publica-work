import RegularFockStressContinuityR4
import CompactTestConservationR3

/-! Weak conservation of the actual point stress form on the regular coherent
Fock domain. Compact smooth tests are integrated with Lebesgue measure on the
existing four-dimensional spacetime; no charge identity is inferred. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory F1Fecho.CompactConservation

 theorem pointStressForm_test_integrable (ψ χ : regularFockDomain) (μ ν : Fin 4)
    (f : Spacetime→ℂ) (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    Integrable (fun x=>metricSignC μ*pointStressForm ψ χ μ ν x*
      (fderiv ℝ f x (spacetimeBasis μ))) :=
  compact_test_integrable volume _ _
    (continuous_const.mul (pointStressForm_continuous ψ χ μ ν)) f hf hc

 theorem pointStressForm_weak_conserved (ψ χ : regularFockDomain) (ν : Fin 4)
    (f : Spacetime→ℂ) (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    (∑μ : Fin 4,∫x,metricSignC μ*pointStressForm ψ χ μ ν x*
      (fderiv ℝ f x (spacetimeBasis μ)))=0 := by
  apply weak_conservation volume
    (fun μ=>pointStressForm ψ χ μ ν)
    (fun μ x=>deriv (fun t : ℝ=>pointStressForm ψ χ μ ν (x+t • spacetimeBasis μ)) 0)
    spacetimeBasis metricSignC
    (fun μ=>pointStressForm_continuous ψ χ μ ν)
    (fun μ=>pointStressForm_partial_continuous ψ χ μ μ ν)
    ?_ (pointStressForm_conserved ψ χ ν) f hf hc
  intro μ x
  exact (pointStressForm_line_hasDerivAt ψ χ μ μ ν x).differentiableAt.hasDerivAt

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_test_integrable
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_weak_conserved
