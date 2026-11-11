import TGLExt.F1Fecho394.CanonicalOutput

set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory FourierTransform SchwartzMap Filter
open scoped FourierTransform ENNReal

namespace F1Rede.FourierConjugation
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (jc : H ≃ₛₗᵢ[starRingEnd ℂ] H)
abbrev LH (H : Type) [NormedAddCommGroup H] := Lp H 2 (volume : Measure ℝ)

/-- The same antiunitary, viewed as a real continuous linear map for Schwartz postcomposition. -/
def realMap : H →L[ℝ] H where
  toFun := jc
  map_add' := jc.map_add
  map_smul' := by
    intro r x
    change jc ((r : ℂ) • x) = (r : ℂ) • jc x
    rw [map_smulₛₗ]
    simp
  cont := jc.continuous

def pointwise : LH H →SL[starRingEnd ℂ] LH H :=
  jc.toContinuousLinearEquiv.toContinuousLinearMap.compLpL 2 volume

theorem pointwise_ae (f : LH H) : pointwise jc f =ᵐ[volume] fun r => jc (f r) :=
  jc.toContinuousLinearEquiv.toContinuousLinearMap.coeFn_compLpL f

theorem pointwise_schwartz (f : 𝓢(ℝ,H)) :
    pointwise jc (f.toLp 2) = (f.postcompCLM (realMap jc)).toLp 2 := by
  apply Lp.ext
  filter_upwards [pointwise_ae jc (f.toLp 2), f.coeFn_toLp 2,
    (f.postcompCLM (realMap jc)).coeFn_toLp 2] with r hp hf hg
  rw [hp,hg,hf]
  rfl

/-- Fourier of a value antiunitary is the value antiunitary of Fourier at reflected frequency. -/
theorem fourier_integral (f : ℝ → H) (hf : Integrable f) (ξ : ℝ) :
    𝓕 (fun r => jc (f r)) ξ = jc (𝓕 f (-ξ)) := by
  rw [Real.fourier_eq, Real.fourier_eq]
  have hi := (Real.fourierIntegral_convergent_iff (-ξ)).mpr hf
  have hc := ContinuousLinearMap.integral_comp_commSL RCLike.conj_smul
    jc.toContinuousLinearEquiv.toContinuousLinearMap hi
  change _ = jc.toContinuousLinearEquiv.toContinuousLinearMap _
  rw [← hc]
  apply integral_congr_ae
  filter_upwards [] with r
  simp only [inner_neg_right, neg_neg, Circle.smul_def, map_smulₛₗ]
  congr 1
  simp only [← Circle.coe_inv_eq_conj, AddChar.map_neg_eq_inv]

theorem fourier_pointwise_schwartz (hJ : Function.Involutive jc) (f : 𝓢(ℝ,H)) :
    𝓕 (pointwise jc (f.toLp 2)) = SpectralConjugation.J jc hJ (𝓕 (f.toLp 2)) := by
  rw [pointwise_schwartz, SchwartzMap.toLp_fourier_eq, SchwartzMap.toLp_fourier_eq]
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    ((𝓕 f).coeFn_toLp 2 volume)
  filter_upwards [(𝓕 (f.postcompCLM (realMap jc))).coeFn_toLp 2,
    SpectralConjugation.J_ae jc hJ ((𝓕 f).toLp 2), hr] with ξ h1 h2 h3
  rw [h1,h2,h3]
  change 𝓕 (fun r => jc (f r)) ξ = jc (𝓕 (f : ℝ → H) (-ξ))
  exact fourier_integral jc f f.integrable ξ

/-- Exact L² identity, extended from the dense Schwartz subspace; no pointwise Fourier assumption. -/
theorem fourier_pointwise (hJ : Function.Involutive jc) (f : LH H) :
    Lp.fourierTransformₗᵢ ℝ H (pointwise jc f) =
      SpectralConjugation.J jc hJ (Lp.fourierTransformₗᵢ ℝ H f) := by
  let p : LH H → Prop := fun g => Lp.fourierTransformₗᵢ ℝ H (pointwise jc g) =
    SpectralConjugation.J jc hJ (Lp.fourierTransformₗᵢ ℝ H g)
  apply DenseRange.induction_on (p := p)
    (SchwartzMap.denseRange_toLpCLM (E := ℝ) (F := H) (p := 2) ENNReal.ofNat_ne_top) f
  · exact isClosed_eq
      ((Lp.fourierTransformₗᵢ ℝ H).continuous.comp (pointwise jc).continuous)
      ((SpectralConjugation.J jc hJ).continuous.comp (Lp.fourierTransformₗᵢ ℝ H).continuous)
  intro g
  exact fourier_pointwise_schwartz jc hJ g

#print axioms fourier_integral
#print axioms fourier_pointwise
end F1Rede.FourierConjugation
