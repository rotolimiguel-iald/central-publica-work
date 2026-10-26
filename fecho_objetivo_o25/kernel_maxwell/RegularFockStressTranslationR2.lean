import RegularFockPointStressR3
import RegularCoherentTransportR1

/-! Exact covariance under canonical translations of the point stress form,
using the unique transported coefficients. No Lorentz tensor covariance is
inferred from this translation result. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Fecho.CoherentKernel

 theorem strongRegularProfile_U1_symm (a : Fin 4→ℝ) (h : H1) (hh : StrongRegularProfile h) :
    StrongRegularProfile ((U1 a).symm h) := by
  rw [← U1_neg]
  exact strongRegularProfile_U1 (-a) h hh

 theorem pointStressForm_translate (a : Fin 4→ℝ) (ψ χ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm (regularGamma (U1 a) (strongRegularProfile_U1 a) ψ)
        (regularGamma (U1 a) (strongRegularProfile_U1 a) χ) μ ν x=
      pointStressForm ψ χ μ ν (x-WithLp.toLp 2 a) := by
  unfold pointStressForm
  rw [regularCoefficients_gamma (U1 a) (strongRegularProfile_U1 a) (strongRegularProfile_U1_symm a),
    regularCoefficients_gamma (U1 a) (strongRegularProfile_U1 a) (strongRegularProfile_U1_symm a),
    finiteKernel_reindex]
  have hM (h k : RegularLabel) :
      coherentProfileStress (regularLabelEquiv (U1 a) (strongRegularProfile_U1 a)
        (strongRegularProfile_U1_symm a) h).val
        (regularLabelEquiv (U1 a) (strongRegularProfile_U1 a)
        (strongRegularProfile_U1_symm a) k).val μ ν x=
      coherentProfileStress h.val k.val μ ν (x-WithLp.toLp 2 a) :=
    coherentProfileStress_translate a h.val k.val μ ν x
  simp_rw [hM]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_translate
