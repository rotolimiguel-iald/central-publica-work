import TGLExt.F1Fecho394.RegularSpectralAverageR6
import TGLExt.F1Fecho394.CoefficientBoostR1
/-! The Fourier coefficient of a regular average on an arbitrary base vector.
The boost is retained pointwise; invariance of that vector is not assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RegularSpectralBoostedAverage
open MeasureTheory TGLV350.Regular
open F1Fecho.RegularCovariantCore F1Fecho.RegularNormalizedFourier
open F1Fecho.RegularSpectralAverage
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def boostedCoefficient (B : UnitaryFlow H) (h : ℝ) (v : H) : RegularHilbert H :=
  CoefficientBoost.unitary B 1 (coefficient h v)

theorem boostedCoefficient_ae (B : UnitaryFlow H) (h : ℝ) (v : H) :
    boostedCoefficient B h v =ᵐ[volume] fun t =>
      (Set.Ioc 0 h).indicator (fun t => B.U t v) t := by
  filter_upwards [CoefficientBoost.unitary_ae B 1 (coefficient h v),
    coefficient_ae h v] with t ht hv
  change CoefficientBoost.unitary B 1 (coefficient h v) t = _
  rw [ht,hv,one_mul]
  by_cases hmem : t∈Set.Ioc 0 h
  · simp only [Set.indicator_of_mem hmem]
  · simp only [Set.indicator_of_notMem hmem,map_zero]

theorem regularUnitary_testVector (B : UnitaryFlow H) (v : H) (t : ℝ) :
    F1Fecho.RegularCovariantCore.regularUnitary B t (testVector v) =
      shift t (testVector (B.U t v)) := by
  change fibre (boostCLM B t) (shift t (testVector v)) = _
  rw [←ContinuousLinearMap.mul_apply,←shift_commutes_fibre,
    ContinuousLinearMap.mul_apply,fibre_testVector]
  rfl

theorem code_boostedCoefficient (B : UnitaryFlow H) (h : ℝ) (v : H) :
    RegularSpectralCode.code (boostedCoefficient B h v) =
      (RegularCoreFiniteWeight.regularOrbitCut_memLp B h (testVector v) 2).toLp
        (RegularCoreFiniteWeight.regularOrbitCut B h (testVector v)) := by
  apply Lp.ext
  filter_upwards [RegularSpectralCode.code_ae (boostedCoefficient B h v),
    boostedCoefficient_ae B h v,
    (RegularCoreFiniteWeight.regularOrbitCut_memLp B h (testVector v) 2).coeFn_toLp]
    with t h1 h2 h3
  rw [h1,h2,h3]
  by_cases ht : t∈Set.Ioc 0 h
  · simp only [Set.indicator_of_mem ht,RegularCoreFiniteWeight.regularOrbitCut]
    exact (regularUnitary_testVector B v t).symm
  · simp only [RegularCoreFiniteWeight.regularOrbitCut,Set.indicator_of_notMem ht,
      Pi.zero_apply]
    have hz : testVector (0 : H)=0 := by
      apply norm_eq_zero.mp
      rw [testVector_norm,norm_zero]
    rw [hz,map_zero]

theorem spectralCode_boostedAverage_ae (B : UnitaryFlow H) (v : H)
    (h : ℝ) (hh : 0<h) :
    spectralCode ((h⁻¹ : ℝ) • boostedCoefficient B h v) =ᵐ[volume] fun s : ℝ =>
      (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s
        (RegularCoreAverage.regularAverage B h) (testVector v) := by
  have hs : Real.sqrt dualHaarFactor = (Real.sqrt (2*Real.pi))⁻¹ := by
    unfold dualHaarFactor
    rw [Real.sqrt_inv]
  have hmap : spectralCode ((h⁻¹ : ℝ) • boostedCoefficient B h v) =
      (h⁻¹ : ℝ) • normalizedFourier
        (RegularSpectralCode.code (boostedCoefficient B h v)) :=
    spectralCode.map_smul_of_tower (h⁻¹ : ℝ) _
  rw [hmap,code_boostedCoefficient]
  filter_upwards [Lp.coeFn_smul (h⁻¹ : ℝ)
    (normalizedFourier ((RegularCoreFiniteWeight.regularOrbitCut_memLp B h
      (testVector v) 2).toLp (RegularCoreFiniteWeight.regularOrbitCut B h (testVector v)))),
    normalizedFourier_toLp_ae (RegularCoreFiniteWeight.regularOrbitCut B h (testVector v))
      (RegularCoreFiniteWeight.regularOrbitCut_integrable B h (testVector v))
      (RegularCoreFiniteWeight.regularOrbitCut_memLp B h (testVector v) 2)] with s h1 h2
  simp only [Pi.smul_apply] at h1
  rw [h1,h2,RegularCoreFiniteWeight.regularAverage_dual_fourier B s h hh,hs]
  have hc (a b : ℝ) (v : RegularHilbert H) : a • b • v = b • a • v := by
    rw [smul_smul,smul_smul,mul_comm]
  exact hc h⁻¹ ((Real.sqrt (2*Real.pi))⁻¹) _
end F1Fecho.RegularSpectralBoostedAverage
#print axioms F1Fecho.RegularSpectralBoostedAverage.boostedCoefficient_ae
#print axioms F1Fecho.RegularSpectralBoostedAverage.regularUnitary_testVector
#print axioms F1Fecho.RegularSpectralBoostedAverage.code_boostedCoefficient
#print axioms F1Fecho.RegularSpectralBoostedAverage.spectralCode_boostedAverage_ae
