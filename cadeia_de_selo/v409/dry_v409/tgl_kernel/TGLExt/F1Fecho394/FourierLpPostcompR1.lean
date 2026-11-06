import TGLExt.F1Fecho394.FourierConjugation

/-! Naturality of the actual Hilbert-valued L2 Fourier equivalence under a
bounded complex-linear map. Proved on Schwartz functions and extended by
density, without assuming a pointwise Fourier representative for arbitrary L2. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory SchwartzMap Filter
open scoped FourierTransform ENNReal
namespace F1Fecho.FourierNaturality
variable {H G : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup G] [InnerProductSpace ℂ G] [CompleteSpace G]
abbrev LH (H : Type) [NormedAddCommGroup H] := Lp H 2 (volume : Measure ℝ)

theorem postcomp_toLp (L : H →L[ℂ] G) (f : 𝓢(ℝ,H)) :
    L.compLp (f.toLp 2)=(SchwartzMap.postcompCLM L f).toLp 2 := by
  apply Lp.ext
  filter_upwards [L.coeFn_compLp (f.toLp 2),f.coeFn_toLp 2,
    (SchwartzMap.postcompCLM L f).coeFn_toLp 2] with r hL hf hg
  rw [hL,hg,hf]
  rfl

theorem fourier_integral_postcomp (L : H →L[ℂ] G) (f : ℝ → H)
    (hf : Integrable f) (p : ℝ) :
    𝓕 (fun r => L (f r)) p=L (𝓕 f p) := by
  rw [Real.fourier_eq,Real.fourier_eq,
    ←L.integral_comp_comm ((Real.fourierIntegral_convergent_iff p).2 hf)]
  apply integral_congr_ae
  filter_upwards [] with r
  simp only [Circle.smul_def,map_smul]

theorem fourier_schwartz_postcomp (L : H →L[ℂ] G) (f : 𝓢(ℝ,H)) :
    𝓕 (SchwartzMap.postcompCLM L f)=SchwartzMap.postcompCLM L (𝓕 f) := by
  ext p : 1
  exact fourier_integral_postcomp L f f.integrable p

theorem fourier_compLp (L : H →L[ℂ] G) (f : LH H) :
    Lp.fourierTransformₗᵢ ℝ G (L.compLp f)=
      L.compLp (Lp.fourierTransformₗᵢ ℝ H f) := by
  let P : LH H → Prop := fun g => Lp.fourierTransformₗᵢ ℝ G (L.compLp g)=
    L.compLp (Lp.fourierTransformₗᵢ ℝ H g)
  apply DenseRange.induction_on (p:=P)
    (SchwartzMap.denseRange_toLpCLM (E:=ℝ) (F:=H) (p:=2) ENNReal.ofNat_ne_top) f
  · exact isClosed_eq
      ((Lp.fourierTransformₗᵢ ℝ G).continuous.comp (L.compLpL 2 volume).continuous)
      ((L.compLpL 2 volume).continuous.comp (Lp.fourierTransformₗᵢ ℝ H).continuous)
  intro g
  change 𝓕 (L.compLp (g.toLp 2))=L.compLp (𝓕 (g.toLp 2))
  rw [postcomp_toLp,SchwartzMap.toLp_fourier_eq,SchwartzMap.toLp_fourier_eq,
    postcomp_toLp,fourier_schwartz_postcomp]

end F1Fecho.FourierNaturality
#print axioms F1Fecho.FourierNaturality.postcomp_toLp
#print axioms F1Fecho.FourierNaturality.fourier_integral_postcomp
#print axioms F1Fecho.FourierNaturality.fourier_compLp
