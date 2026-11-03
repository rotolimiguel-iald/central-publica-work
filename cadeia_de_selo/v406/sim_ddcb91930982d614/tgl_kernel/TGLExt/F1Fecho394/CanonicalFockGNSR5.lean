import TGLExt.F1Fecho394.CanonicalFockFiniteWeightR4
import TGLExt.F1Fecho394.RegularScalarGNSR3
/-! Concrete scalar GNS for the actual Fock core. All properties required by
the generic context are supplied from the original weight proofs; no GNS
result is taken as input. The Hilbert completion is the actual orbit closure. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockFiniteWeight
open scoped ENNReal NNReal Topology

def weightContext : F1Fecho.RegularScalarGNS.Context F where
  algebra := core
  vacuum := regularFockVacuum
  faithful := fun A hm hp => F1Fecho.CanonicalFockFaithfulWeight.weight_faithful ⟨A,hm,hp⟩

theorem scalarOrbit_memLp (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : HasFiniteDualSquare A) : MemLp (fun s : ℝ => dualAmbient s A regularFockVacuum) 2 :=
  F1Fecho.RegularScalarGNS.scalarOrbit_memLp weightContext A hA

abbrev scalarGNSOrbit : finiteLeftIdeal → RegularHilbert (RegularHilbert F) :=
  F1Fecho.RegularScalarGNS.scalarGNSOrbit weightContext

theorem scalarGNSOrbit_norm_sq (A : finiteLeftIdeal) :
    ENNReal.ofReal (‖scalarGNSOrbit A‖^2) = dualQuadraticIntegral (star A.val.val*A.val.val) regularFockVacuum :=
  F1Fecho.RegularScalarGNS.scalarGNSOrbit_norm_sq weightContext A

theorem scalarGNSOrbit_ae (A : finiteLeftIdeal) :
    (scalarGNSOrbit A : ℝ → RegularHilbert F) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val regularFockVacuum :=
  F1Fecho.RegularScalarGNS.scalarGNSOrbit_ae weightContext A

theorem scalarGNSOrbit_add (A B : finiteLeftIdeal) :
    scalarGNSOrbit (A+B) = scalarGNSOrbit A + scalarGNSOrbit B :=
  F1Fecho.RegularScalarGNS.scalarGNSOrbit_add weightContext A B

theorem scalarGNSOrbit_smul (c : ℂ) (A : finiteLeftIdeal) :
    scalarGNSOrbit (c • A) = c • scalarGNSOrbit A :=
  F1Fecho.RegularScalarGNS.scalarGNSOrbit_smul weightContext c A

abbrev scalarGNSLinear : finiteLeftIdeal →ₗ[ℂ] RegularHilbert (RegularHilbert F) :=
  F1Fecho.RegularScalarGNS.scalarGNSLinear weightContext

theorem scalarGNSOrbit_zero_iff (A : finiteLeftIdeal) : scalarGNSOrbit A=0 ↔ A=0 :=
  F1Fecho.RegularScalarGNS.scalarGNSOrbit_zero_iff weightContext A

theorem scalarGNSLinear_injective : Function.Injective scalarGNSLinear :=
  F1Fecho.RegularScalarGNS.scalarGNSLinear_injective weightContext

abbrev GNSSubspace := F1Fecho.RegularScalarGNS.GNSSubspace weightContext
abbrev GNSHilbert := GNSSubspace
instance gnsCompleteSpace : CompleteSpace GNSHilbert := inferInstance
abbrev GNSEmbedding : finiteLeftIdeal →ₗ[ℂ] GNSHilbert :=
  F1Fecho.RegularScalarGNS.GNSEmbedding weightContext

theorem GNSEmbedding_injective : Function.Injective GNSEmbedding :=
  F1Fecho.RegularScalarGNS.GNSEmbedding_injective weightContext

end F1Fecho.CanonicalFockGNS
#print axioms F1Fecho.CanonicalFockGNS.weightContext
#print axioms F1Fecho.CanonicalFockGNS.scalarOrbit_memLp
#print axioms F1Fecho.CanonicalFockGNS.scalarGNSOrbit_norm_sq
#print axioms F1Fecho.CanonicalFockGNS.scalarGNSOrbit_ae
#print axioms F1Fecho.CanonicalFockGNS.scalarGNSOrbit_add
#print axioms F1Fecho.CanonicalFockGNS.scalarGNSOrbit_smul
#print axioms F1Fecho.CanonicalFockGNS.scalarGNSOrbit_zero_iff
#print axioms F1Fecho.CanonicalFockGNS.scalarGNSLinear_injective
#print axioms F1Fecho.CanonicalFockGNS.GNSEmbedding_injective
