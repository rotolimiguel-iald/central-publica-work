import TGLExt.F1Fecho394.RegularSpectralAverageR6
import TGLExt.F1Fecho394.RegularSpectralCoreRangeR3
import TGLExt.F1Fecho394.CanonicalFockWeightCompletionR5
import TGLExt.F1Fecho394.RegularIntervalVectorsR2
import TGLExt.F1Fecho394.RegularDualGNSActionR1
import TGLExt.F1Fecho394.LpIntervalTotalVectorsR1
/-! The actual normalized Fourier coefficient map is onto the dual-weight
GNS completion. Surjectivity is proved from interval totality and the concrete
cyclic wedge vacuum, without an abstract Hilbert-space identification. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockGNS
open F1Fecho.RegularNormalizedFourier F1Fecho.RegularSpectralAverage
open F1Fecho.LpIntervalTotality
open F1Fecho.RegularIntervalVectors
open scoped Topology ENNReal

theorem fockFlow_vacuum (t : ℝ) : fockFlow.U t vacuum=vacuum :=
  F1Rede.BosonicFock.gamma_vacuum (B0 (-(2*Real.pi*t)))

def coefficientGNS : Submodule ℂ (RegularHilbert F) :=
  GNSSubspace.comap spectralCode.toLinearMap

theorem coefficientGNS_closed : IsClosed (coefficientGNS : Set (RegularHilbert F)) :=
  (Submodule.isClosed_topologicalClosure _).preimage spectralCode.continuous

theorem coefficientGNS_mem (f : RegularHilbert F) :
    f ∈ coefficientGNS ↔ spectralCode f ∈ GNSSubspace := Iff.rfl

theorem average_coefficient_mem (h : ℝ) (hh : 0<h) :
    (h⁻¹ : ℝ) • coefficient h vacuum ∈ coefficientGNS := by
  let av : finiteLeftIdeal :=
    ⟨⟨F1Fecho.RegularCoreAverage.regularAverage fockFlow h,
        F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h⟩,
      F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh⟩
  have he : spectralCode ((h⁻¹ : ℝ) • coefficient h vacuum)=scalarGNSOrbit av := by
    apply Lp.ext
    exact (spectralCode_average_ae fockFlow vacuum fockFlow_vacuum h hh).trans
      (scalarGNSOrbit_ae av).symm
  change spectralCode ((h⁻¹ : ℝ) • coefficient h vacuum) ∈ closure (Set.range scalarGNSLinear)
  exact subset_closure ⟨av,he.symm⟩

theorem coefficient_mem (h : ℝ) (hh : 0<h) : coefficient h vacuum ∈ coefficientGNS := by
  have hs := coefficientGNS.smul_of_tower_mem h (average_coefficient_mem h hh)
  simpa only [smul_smul,mul_inv_cancel₀ hh.ne',one_smul] using hs

theorem regular_preserves (t : ℝ) (f : RegularHilbert F) (hf : f∈coefficientGNS) :
    regularUnitary t f ∈ coefficientGNS := by
  change spectralCode (regularUnitary t f) ∈ GNSSubspace
  have hm := F1Fecho.RegularDualGNSAction.dual_preserves weightContext
    (regularUnitary t) (regular_mem t) (spectralCode f) hf
  exact Eq.mpr (congrArg (fun v => v∈GNSSubspace)
    (RegularSpectralCoreRange.spectralCode_regular fockFlow t f)) hm

theorem fibre_preserves (A : F →L[ℂ] F) (hA : A∈M)
    (f : RegularHilbert F) (hf : f∈coefficientGNS) : fibre A f ∈ coefficientGNS := by
  change spectralCode (fibre A f) ∈ GNSSubspace
  have hm := F1Fecho.RegularDualGNSAction.dual_preserves weightContext
    (fibre A) (fibre_mem A hA) (spectralCode f) hf
  have he := (spectralCode_fibre A f).trans
    (congrArg (fun T : RegularHilbert (RegularHilbert F)→L[ℂ]RegularHilbert (RegularHilbert F) =>
      T (spectralCode f)) (RegularSpectralCoreRange.dualOrbit_fibre A).symm)
  exact Eq.mpr (congrArg (fun v => v∈GNSSubspace) he) hm

theorem interval_vacuum_mem (a b : ℝ) : intervalVector a b vacuum ∈ coefficientGNS := by
  by_cases hab : a<b
  · rw [←regular_coefficient fockFlow vacuum fockFlow_vacuum a b]
    exact regular_preserves a _ (coefficient_mem (b-a) (sub_pos.mpr hab))
  · rw [intervalVector_of_ge a b vacuum (le_of_not_gt hab)]
    exact coefficientGNS.zero_mem

theorem interval_orbit_mem (a b : ℝ) (A : F →L[ℂ] F) (hA : A∈M) :
    intervalVector a b (A vacuum) ∈ coefficientGNS := by
  rw [←fibre_interval]
  exact fibre_preserves A hA _ (interval_vacuum_mem a b)

theorem coefficientGNS_eq_top : coefficientGNS=⊤ := by
  apply F1Fecho.LpIntervalTotalVectors.closed_submodule_eq_top_of_total
    coefficientGNS coefficientGNS_closed
    (F1Fecho.WedgeCyclic.vacuumOrbit F1Rede.CanonicalWedge.spectralOutput.KWR.toClosedSubmodule.toSubmodule)
  · intro v hv
    apply F1Fecho.WedgeCyclic.orthogonal_vacuumOrbit_zero F1Rede.CanonicalWedge.spectralOutput.KWR v
    intro A hA
    exact hv (A vacuum) ⟨A,hA,rfl⟩
  · intro a b w hw
    obtain ⟨A,hA,rfl⟩ := hw
    exact interval_orbit_mem a b A hA


theorem spectralCode_mem_GNS (f : RegularHilbert F) : spectralCode f ∈ GNSSubspace := by
  apply (coefficientGNS_mem f).mp
  rw [coefficientGNS_eq_top]
  trivial

end F1Fecho.CanonicalFockCoefficientGNS
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientGNS_closed
#print axioms F1Fecho.CanonicalFockCoefficientGNS.average_coefficient_mem
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficient_mem
#print axioms F1Fecho.CanonicalFockCoefficientGNS.regular_preserves
#print axioms F1Fecho.CanonicalFockCoefficientGNS.fibre_preserves
#print axioms F1Fecho.CanonicalFockCoefficientGNS.interval_vacuum_mem
#print axioms F1Fecho.CanonicalFockCoefficientGNS.interval_orbit_mem
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientGNS_eq_top
#print axioms F1Fecho.CanonicalFockCoefficientGNS.spectralCode_mem_GNS
