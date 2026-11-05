import TGLExt.F1Fecho394.RegularSpectralAverageR6
import TGLExt.F1Fecho394.RegularSpectralCoreRangeR3
import TGLExt.F1Fecho394.CanonicalFockWeightCompletionR5
import TGLExt.F1Fecho394.RegularOrbitMultiplicationR1
/-! Inclusion of the entire actual dual-weight GNS completion into the
concrete normalized-Fourier coefficient image. No surjectivity or modular
identification is assumed. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 600000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockSpectralGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockRightAverage
open F1Fecho.RegularNormalizedFourier F1Fecho.RegularSpectralAverage
open scoped Topology ENNReal

theorem fockFlow_vacuum (t : ℝ) : fockFlow.U t vacuum=vacuum :=
  F1Rede.BosonicFock.gamma_vacuum (B0 (-(2*Real.pi*t)))

theorem rightRegularization_orbit (A : scalarWeightLeftIdeal) (h : ℝ) (hh : 0<h) :
    dualOrbitRepresentation A.val.val
      (spectralCode ((h⁻¹ : ℝ) • coefficient h vacuum)) =
      scalarWeightOrbit (scalarWeightRightRegularization A h) :=
  RegularOrbitMultiplication.apply_orbit
    (F1Fecho.RegularCoreAverage.regularAverage fockFlow h) A.val.val regularFockVacuum
    (Real.sqrt dualHaarFactor) _ _
    (spectralCode_average_ae fockFlow vacuum fockFlow_vacuum h hh)
    (scalarWeightOrbit_ae (scalarWeightRightRegularization A h))

theorem rightRegularization_in_range (A : scalarWeightLeftIdeal) (h : ℝ) (hh : 0<h) :
    scalarWeightOrbit (scalarWeightRightRegularization A h) ∈
      Set.range (spectralCode (H:=F)) := by
  have hi := RegularSpectralCoreRange.spectralCode_range_preserved fockFlow M
    A.val.val A.val.property ⟨(h⁻¹ : ℝ) • coefficient h vacuum,rfl⟩
  exact Eq.mpr (congrArg (fun v => v∈Set.range (spectralCode (H:=F)))
    (rightRegularization_orbit A h hh).symm) hi

theorem weightOrbit_in_range (A : scalarWeightLeftIdeal) :
    scalarWeightOrbit A ∈ Set.range (spectralCode (H:=F)) := by
  have ht : Tendsto (fun h : ℝ => scalarWeightOrbit (scalarWeightRightRegularization A h))
      (𝓝[>] (0 : ℝ)) (𝓝 (scalarWeightOrbit A)) :=
    (scalarWeightOrbit_rightRegularization_tendsto A).mono_left
      (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  apply spectralCode_closedRange.mem_of_tendsto ht
  filter_upwards [self_mem_nhdsWithin] with h hh
  exact rightRegularization_in_range A h hh

theorem GNS_subset_spectralCode :
    (GNSSubspace : Set (RegularHilbert (RegularHilbert F))) ⊆ Set.range (spectralCode (H:=F)) := by
  change closure (Set.range scalarGNSLinear) ⊆ _
  apply closure_minimal ?_ spectralCode_closedRange
  rintro _ ⟨A,rfl⟩
  have h := weightOrbit_in_range (Submodule.inclusion finiteDualLeftIdeal_le_scalarWeight A)
  exact Eq.mp (congrArg (fun v => v∈Set.range (spectralCode (H:=F)))
    (scalarWeightOrbit_uniform A)) h

end F1Fecho.CanonicalFockSpectralGNS
#print axioms F1Fecho.CanonicalFockSpectralGNS.fockFlow_vacuum
#print axioms F1Fecho.CanonicalFockSpectralGNS.rightRegularization_orbit
#print axioms F1Fecho.CanonicalFockSpectralGNS.rightRegularization_in_range
#print axioms F1Fecho.CanonicalFockSpectralGNS.weightOrbit_in_range
#print axioms F1Fecho.CanonicalFockSpectralGNS.GNS_subset_spectralCode
