import TGLExt.F1Fecho394.RegularNormalizedFourierR2
import TGLExt.F1Fecho394.RegularCoreFiniteWeightR3
/-! Exact coefficient formula for finite regular averages. This discharges the
Haar normalization by the existing vector-valued L1/L2 Fourier theorem. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RegularSpectralAverage
open MeasureTheory Filter TGLV350.Regular
open scoped FourierTransform
open F1Fecho.RegularNormalizedFourier F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem normalizedFourier_toLp_ae (f : ℝ → H) (hf1 : Integrable f) (hf2 : MemLp f 2) :
    normalizedFourier (hf2.toLp f) =ᵐ[volume] fun s : ℝ =>
      ((Real.sqrt (2*Real.pi))⁻¹ : ℝ) • (𝓕 f) (s/(2*Real.pi)) := by
  filter_upwards [normalizedFourier_ae (hf2.toLp f),
    (RegularL2Rescale.div_qmp (2*Real.pi) (by positivity)).ae
      (TGLV350.Fourier.fourier_integral_ae_eq_L2 f hf1 hf2)] with s hs ht
  exact hs.trans (congrArg (fun v : H => ((Real.sqrt (2*Real.pi))⁻¹ : ℝ) • v) ht.symm)

def coefficientMemLp (h : ℝ) (Ω : H) :
    MemLp ((Set.Ioc 0 h).indicator (fun _ : ℝ => Ω)) 2 volume :=
  memLp_indicator_const 2 measurableSet_Ioc Ω (Or.inr (by simp [Real.volume_Ioc]))

def coefficient (h : ℝ) (Ω : H) : RegularHilbert H :=
  (coefficientMemLp h Ω).toLp ((Set.Ioc 0 h).indicator (fun _ : ℝ => Ω))

theorem coefficient_ae (h : ℝ) (Ω : H) :
    coefficient h Ω =ᵐ[volume] (Set.Ioc 0 h).indicator (fun _ : ℝ => Ω) :=
  (coefficientMemLp h Ω).coeFn_toLp

theorem regularUnitary_testVector (B : UnitaryFlow H) (Ω : H)
    (hΩ : ∀ t, B.U t Ω=Ω) (t : ℝ) :
    F1Fecho.RegularCovariantCore.regularUnitary B t (testVector Ω) = shift t (testVector Ω) := by
  change fibre (boostCLM B t) (shift t (testVector Ω)) = _
  rw [← ContinuousLinearMap.mul_apply,←shift_commutes_fibre,ContinuousLinearMap.mul_apply,
    fibre_testVector]
  change shift t (testVector (B.U t Ω)) = _
  rw [hΩ]

theorem code_coefficient (B : UnitaryFlow H) (Ω : H)
    (hΩ : ∀ t, B.U t Ω=Ω) (h : ℝ) :
    RegularSpectralCode.code (coefficient h Ω) =
      (RegularCoreFiniteWeight.regularOrbitCut_memLp B h (testVector Ω) 2).toLp
        (RegularCoreFiniteWeight.regularOrbitCut B h (testVector Ω)) := by
  apply Lp.ext
  filter_upwards [RegularSpectralCode.code_ae (coefficient h Ω),coefficient_ae h Ω,
    (RegularCoreFiniteWeight.regularOrbitCut_memLp B h (testVector Ω) 2).coeFn_toLp] with a h1 h2 h3
  rw [h1,h2,h3]
  by_cases ha : a ∈ Set.Ioc 0 h
  · simp only [Set.indicator_of_mem ha,RegularCoreFiniteWeight.regularOrbitCut]
    exact (regularUnitary_testVector B Ω hΩ a).symm
  · simp only [RegularCoreFiniteWeight.regularOrbitCut,Set.indicator_of_notMem ha,Pi.zero_apply]
    have hz : testVector (0 : H) = 0 := by
      apply norm_eq_zero.mp
      rw [testVector_norm,norm_zero]
    rw [hz,map_zero]

theorem spectralCode_average_ae (B : UnitaryFlow H) (Ω : H)
    (hΩ : ∀ t, B.U t Ω=Ω) (h : ℝ) (hh : 0<h) :
    spectralCode ((h⁻¹ : ℝ) • coefficient h Ω) =ᵐ[volume] fun s : ℝ =>
      (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (RegularCoreAverage.regularAverage B h)
        (testVector Ω) := by
  have hs : Real.sqrt dualHaarFactor = (Real.sqrt (2*Real.pi))⁻¹ := by
    unfold dualHaarFactor
    rw [Real.sqrt_inv]
  have hmap : spectralCode ((h⁻¹ : ℝ) • coefficient h Ω) =
      (h⁻¹ : ℝ) • normalizedFourier (RegularSpectralCode.code (coefficient h Ω)) :=
    spectralCode.map_smul_of_tower (h⁻¹ : ℝ) _
  rw [hmap,code_coefficient B Ω hΩ]
  filter_upwards [Lp.coeFn_smul (h⁻¹ : ℝ)
    (normalizedFourier ((RegularCoreFiniteWeight.regularOrbitCut_memLp B h (testVector Ω) 2).toLp
      (RegularCoreFiniteWeight.regularOrbitCut B h (testVector Ω)))),
    normalizedFourier_toLp_ae (RegularCoreFiniteWeight.regularOrbitCut B h (testVector Ω))
      (RegularCoreFiniteWeight.regularOrbitCut_integrable B h (testVector Ω))
      (RegularCoreFiniteWeight.regularOrbitCut_memLp B h (testVector Ω) 2)] with s h1 h2
  simp only [Pi.smul_apply] at h1
  rw [h1,h2,RegularCoreFiniteWeight.regularAverage_dual_fourier B s h hh,hs]
  have hc (a b : ℝ) (v : RegularHilbert H) : a • b • v = b • a • v := by
    rw [smul_smul,smul_smul,mul_comm]
  exact hc h⁻¹ ((Real.sqrt (2*Real.pi))⁻¹) _

end F1Fecho.RegularSpectralAverage
#print axioms F1Fecho.RegularSpectralAverage.normalizedFourier_toLp_ae
#print axioms F1Fecho.RegularSpectralAverage.coefficient_ae
#print axioms F1Fecho.RegularSpectralAverage.regularUnitary_testVector
#print axioms F1Fecho.RegularSpectralAverage.code_coefficient
#print axioms F1Fecho.RegularSpectralAverage.spectralCode_average_ae
