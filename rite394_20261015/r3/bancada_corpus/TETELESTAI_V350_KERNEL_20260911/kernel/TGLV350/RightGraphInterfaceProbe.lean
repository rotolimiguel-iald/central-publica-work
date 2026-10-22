import TGLV350.FixedVectorGraphCore
import TGLV350.ScalarRightProjectionPair
set_option autoImplicit false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000
namespace TGLV350.Regular
open TGLExt ClosedSubmodule
noncomputable section
variable (P : SiteProfile)
#synth Star (scalarPairedRightAlgebra P)
#synth StarAddMonoid (scalarPairedRightAlgebra P)
#synth StarModule ℂ (scalarPairedRightAlgebra P)
example (a : scalarPairedRightAlgebra P) :
    @star (scalarPairedRightAlgebra P) (inferInstance : StarAddMonoid (scalarPairedRightAlgebra P)).toStar a = star a := rfl
example (a : scalarPairedRightAlgebra P) :
    ∃ hv : scalarRightPairVector P a ∈ scalarTomitaAdjointDomain P,
      (scalarTomitaAdjoint P).toFun ⟨scalarRightPairVector P a,hv⟩ = scalarRightPairVector P (star a) :=
  scalarRightPairVector_original_adjoint P a
end
end TGLV350.Regular
