import Mathlib.Analysis.Fourier.LpSpace
import TGLExt.V350L2OperatorLift
/-! Naturality of the existing vector-valued Fourier L2 equivalence under
bounded complex-linear fibre maps. No Fourier integral is assigned to arbitrary L2 vectors. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 900000
noncomputable section
namespace F1Fecho.RegularFourierFibre
open TGLV350.Regular MeasureTheory FourierTransform SchwartzMap Filter
open scoped FourierTransform ENNReal
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem fourier_integral (C : H →L[ℂ] H) (f : ℝ → H) (hf : Integrable f) (ξ : ℝ) :
    𝓕 (fun r => C (f r)) ξ = C (𝓕 f ξ) := by
  rw [Real.fourier_eq,Real.fourier_eq]
  have hi := (Real.fourierIntegral_convergent_iff ξ).mpr hf
  rw [← C.integral_comp_comm hi]
  apply integral_congr_ae
  filter_upwards [] with r
  simp only [Circle.smul_def,map_smul]

theorem fibre_schwartz (C : H →L[ℂ] H) (f : 𝓢(ℝ,H)) :
    fibre C (f.toLp 2) = (f.postcompCLM (C.restrictScalars ℝ)).toLp 2 := by
  apply Lp.ext
  filter_upwards [fibre_ae C (f.toLp 2),f.coeFn_toLp 2,
    (f.postcompCLM (C.restrictScalars ℝ)).coeFn_toLp 2] with r h1 h2 h3
  rw [h1,h2,h3]
  rfl

theorem fourier_fibre_schwartz (C : H →L[ℂ] H) (f : 𝓢(ℝ,H)) :
    𝓕 (fibre C (f.toLp 2)) = fibre C (𝓕 (f.toLp 2)) := by
  rw [fibre_schwartz,SchwartzMap.toLp_fourier_eq,SchwartzMap.toLp_fourier_eq]
  apply Lp.ext
  filter_upwards [(𝓕 (f.postcompCLM (C.restrictScalars ℝ))).coeFn_toLp 2,
    fibre_ae C ((𝓕 f).toLp 2),(𝓕 f).coeFn_toLp 2] with r h1 h2 h3
  rw [h1,h2,h3]
  change 𝓕 (fun x => C (f x)) r = C (𝓕 (f : ℝ → H) r)
  exact fourier_integral C f f.integrable r

theorem fourier_fibre (C : H →L[ℂ] H) (f : RegularHilbert H) :
    Lp.fourierTransformₗᵢ ℝ H (fibre C f) =
      fibre C (Lp.fourierTransformₗᵢ ℝ H f) := by
  let p : RegularHilbert H → Prop := fun g =>
    Lp.fourierTransformₗᵢ ℝ H (fibre C g) = fibre C (Lp.fourierTransformₗᵢ ℝ H g)
  apply DenseRange.induction_on (p := p)
    (SchwartzMap.denseRange_toLpCLM (E := ℝ) (F := H) (p := 2) ENNReal.ofNat_ne_top) f
  · exact isClosed_eq
      ((Lp.fourierTransformₗᵢ ℝ H).continuous.comp (fibre C).continuous)
      ((fibre C).continuous.comp (Lp.fourierTransformₗᵢ ℝ H).continuous)
  intro g
  exact fourier_fibre_schwartz C g

end F1Fecho.RegularFourierFibre
#print axioms F1Fecho.RegularFourierFibre.fourier_integral
#print axioms F1Fecho.RegularFourierFibre.fibre_schwartz
#print axioms F1Fecho.RegularFourierFibre.fourier_fibre_schwartz
#print axioms F1Fecho.RegularFourierFibre.fourier_fibre
