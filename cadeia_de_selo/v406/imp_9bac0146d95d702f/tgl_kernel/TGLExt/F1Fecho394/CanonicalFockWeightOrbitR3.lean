import TGLExt.F1Fecho394.CanonicalFockWeightDomainR1
import TGLExt.F1Fecho394.CanonicalFockGNSR5
import TGLExt.F1Fecho394.RegularScalarWeightOrbitR1
/-! Full n_nu orbit of the concrete Fock weight, extending the uniformly finite
ideal without changing the original weight. No traciality is asserted. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightOrbit
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockGNS
open scoped ENNReal NNReal

theorem scalarWeightOrbit_memLp (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : HasFiniteScalarSquare A) : MemLp (fun s : ℝ => dualAmbient s A regularFockVacuum) 2 :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_memLp weightContext A hA

abbrev scalarWeightOrbit : scalarWeightLeftIdeal → RegularHilbert (RegularHilbert F) :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit weightContext

theorem scalarWeightOrbit_norm_sq (A : scalarWeightLeftIdeal) :
    ENNReal.ofReal (‖scalarWeightOrbit A‖^2) = dualQuadraticIntegral (star A.val.val*A.val.val) regularFockVacuum :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_norm_sq weightContext A

theorem scalarWeightOrbit_norm_sq_real (A : scalarWeightLeftIdeal) :
    ‖scalarWeightOrbit A‖^2 = dualHaarFactor * ∫ s : ℝ, ‖dualAmbient s A.val.val regularFockVacuum‖^2 :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_norm_sq_real weightContext A

theorem scalarWeightOrbit_ae (A : scalarWeightLeftIdeal) :
    (scalarWeightOrbit A : ℝ → RegularHilbert F) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val regularFockVacuum :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_ae weightContext A

abbrev scalarWeightLinear : scalarWeightLeftIdeal →ₗ[ℂ] RegularHilbert (RegularHilbert F) :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightLinear weightContext

theorem scalarWeightOrbit_zero_iff (A : scalarWeightLeftIdeal) : scalarWeightOrbit A=0 ↔ A=0 :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_zero_iff weightContext A

theorem scalarWeightLinear_injective : Function.Injective scalarWeightLinear :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightLinear_injective weightContext

theorem scalarWeightOrbit_uniform (A : finiteLeftIdeal) :
    scalarWeightOrbit (Submodule.inclusion finiteDualLeftIdeal_le_scalarWeight A) = scalarGNSOrbit A :=
  F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_uniform weightContext A

end F1Fecho.CanonicalFockWeightOrbit
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_memLp
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_norm_sq
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_norm_sq_real
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_ae
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_zero_iff
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear_injective
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_uniform
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit
#print axioms F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear
