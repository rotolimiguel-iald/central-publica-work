import TGLExt.F1Fecho394.RegularSpectralAverageR6
import TGLExt.F1Fecho394.LpIntervalTotalityR3
/-! Elementary interval vectors for the already constructed regular
representation. These identities supply concrete coefficient generators. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 600000
noncomputable section
namespace F1Fecho.RegularIntervalVectors
open MeasureTheory Filter TGLV350.Regular
open F1Fecho.RegularSpectralAverage F1Fecho.LpIntervalTotality
open F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem intervalVector_ae (a b : ℝ) (v : H) :
    intervalVector a b v =ᵐ[volume] (Set.Ioc a b).indicator (fun _ : ℝ => v) :=
  indicatorConstLp_coeFn

theorem coefficient_interval (h : ℝ) (v : H) : coefficient h v=intervalVector 0 h v := by
  apply Lp.ext
  exact (coefficient_ae h v).trans (intervalVector_ae 0 h v).symm

theorem fibre_interval (A : H →L[ℂ] H) (a b : ℝ) (v : H) :
    fibre A (intervalVector a b v)=intervalVector a b (A v) := by
  apply Lp.ext
  filter_upwards [fibre_ae A (intervalVector a b v),intervalVector_ae a b v,
    intervalVector_ae a b (A v)] with x h1 h2 h3
  rw [h1,h2,h3]
  by_cases hx : x ∈ Set.Ioc a b
  · simp only [Set.indicator_of_mem hx]
  · simp only [Set.indicator_of_notMem hx,map_zero]

theorem shift_coefficient (a b : ℝ) (v : H) :
    shift a (coefficient (b-a) v)=intervalVector a b v := by
  apply Lp.ext
  filter_upwards [shift_ae a (coefficient (b-a) v),
    (measurePreserving_sub_right volume a).quasiMeasurePreserving.ae (coefficient_ae (b-a) v),
    intervalVector_ae a b v] with x h1 h2 h3
  rw [h1,h2,h3]
  have hx : x-a ∈ Set.Ioc 0 (b-a) ↔ x ∈ Set.Ioc a b := by
    simp only [Set.mem_Ioc]
    constructor <;> intro h <;> constructor <;> linarith [h.1,h.2]
  by_cases hm : x ∈ Set.Ioc a b
  · simp only [Set.indicator_of_mem hm,Set.indicator_of_mem (hx.mpr hm)]
  · simp only [Set.indicator_of_notMem hm,Set.indicator_of_notMem (fun h => hm (hx.mp h))]

theorem regular_coefficient (B : UnitaryFlow H) (v : H) (hv : ∀ t, B.U t v=v)
    (a b : ℝ) : RegularCovariantCore.regularUnitary B a (coefficient (b-a) v)=
      intervalVector a b v := by
  change fibre (boostCLM B a) (shift a (coefficient (b-a) v)) = _
  rw [shift_coefficient,fibre_interval]
  change intervalVector a b (B.U a v)=_
  rw [hv]

theorem intervalVector_of_ge (a b : ℝ) (v : H) (hab : b≤a) : intervalVector a b v=0 := by
  apply Lp.ext
  filter_upwards [intervalVector_ae a b v, Lp.coeFn_zero H 2 (volume : Measure ℝ)] with t h1 h2
  rw [h1,h2]
  simp [Set.Ioc_eq_empty (not_lt_of_ge hab)]

end F1Fecho.RegularIntervalVectors
#print axioms F1Fecho.RegularIntervalVectors.intervalVector_ae
#print axioms F1Fecho.RegularIntervalVectors.coefficient_interval
#print axioms F1Fecho.RegularIntervalVectors.fibre_interval
#print axioms F1Fecho.RegularIntervalVectors.shift_coefficient
#print axioms F1Fecho.RegularIntervalVectors.regular_coefficient
#print axioms F1Fecho.RegularIntervalVectors.intervalVector_of_ge
