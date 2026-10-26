import TGLExt.V351FourierTranslation
import TGLExt.V351RegularGeneratorAffiliation

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory FourierTransform SchwartzMap Filter
open scoped FourierTransform ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem fourierInv_shift_schwartz (t : ℝ) (f : 𝓢(ℝ,H)) :
    𝓕⁻ (shift t (f.toLp 2)) =
      characterMultiplier (-(2*Real.pi*t)) (𝓕⁻ (f.toLp 2)) := by
  rw [shift_schwartz_toLp, SchwartzMap.toLp_fourierInv_eq,
    SchwartzMap.toLp_fourierInv_eq]
  apply Lp.ext
  filter_upwards [(𝓕⁻ (f.compSubConstCLM ℂ t)).coeFn_toLp 2,
    characterMultiplier_ae (-(2*Real.pi*t)) ((𝓕⁻ f).toLp 2),
    (𝓕⁻ f).coeFn_toLp 2] with x h1 h2 h3
  rw [h1,h2,h3]
  simp only [SchwartzMap.fourierInv_coe]
  change (𝓕⁻ (fun y : ℝ => f (y-t))) x =
    characterPhase (-(2*Real.pi*t)) x • (𝓕⁻ (f : ℝ → H)) x
  rw [Real.fourierInv_eq_fourier_neg, Real.fourierInv_eq_fourier_neg]
  have h := congrFun (VectorFourier.fourierIntegral_comp_add_right
    Real.fourierChar volume (innerₗ ℝ) (f : ℝ → H) (-t)) (-x)
  change (𝓕 (fun y : ℝ => f (y + -t))) (-x) =
    Real.fourierChar (inner ℝ (-t) (-x)) • (𝓕 (f : ℝ → H)) (-x) at h
  rw [show (fun y : ℝ => f (y-t)) = (fun y : ℝ => f (y + -t)) by rfl,h]
  rw [Circle.smul_def, Real.fourierChar_apply]
  congr 2
  simp only [Real.inner_apply, Complex.ofReal_mul, Complex.ofReal_neg]
  ring

theorem fourierInv_shift (t : ℝ) (f : RegularHilbert H) :
    (Lp.fourierTransformₗᵢ ℝ H).symm (shift t f) =
      characterMultiplier (-(2*Real.pi*t)) ((Lp.fourierTransformₗᵢ ℝ H).symm f) := by
  let p : RegularHilbert H → Prop := fun g =>
    (Lp.fourierTransformₗᵢ ℝ H).symm (shift t g) =
      characterMultiplier (-(2*Real.pi*t)) ((Lp.fourierTransformₗᵢ ℝ H).symm g)
  apply DenseRange.induction_on (p := p)
    (SchwartzMap.denseRange_toLpCLM (E := ℝ) (F := H) (p := 2) ENNReal.ofNat_ne_top) f
  · exact isClosed_eq
      ((Lp.fourierTransformₗᵢ ℝ H).symm.continuous.comp (shift t).continuous)
      ((characterMultiplier (-(2*Real.pi*t))).continuous.comp
        (Lp.fourierTransformₗᵢ ℝ H).symm.continuous)
  intro g
  exact fourierInv_shift_schwartz t g

theorem fourier_characterMultiplier (s : ℝ) (f : RegularHilbert H) :
    Lp.fourierTransformₗᵢ ℝ H (characterMultiplier s f) =
      shift (-s/(2*Real.pi)) (Lp.fourierTransformₗᵢ ℝ H f) := by
  let F := Lp.fourierTransformₗᵢ ℝ H
  have h := fourierInv_shift (-s/(2*Real.pi)) (F f)
  have hs : -(2*Real.pi*(-s/(2*Real.pi))) = s := by
    field_simp
  rw [hs, LinearIsometryEquiv.symm_apply_apply] at h
  have hh := congrArg F h
  change F (F.symm (shift (-s/(2*Real.pi)) (F f))) = F (characterMultiplier s f) at hh
  simpa only [LinearIsometryEquiv.apply_symm_apply] using hh.symm

/-- Scalar characters commute with the existing pointwise operator-field lift. -/
theorem operatorFieldLift_commutes_character (F : StrongIntegral.Family (H := H)) (s : ℝ) :
    operatorFieldLift F * characterMultiplier s = characterMultiplier s * operatorFieldLift F := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae F (characterMultiplier s f),
    characterMultiplier_ae s f, characterMultiplier_ae s (operatorFieldLift F f),
    operatorFieldLift_ae F f] with x h1 h2 h3 h4
  change operatorFieldLift F (characterMultiplier s f) x =
    characterMultiplier s (operatorFieldLift F f) x
  rw [h1,h2,h3,h4]
  exact map_smul (F.op x) _ _

/-- The same spectral coordinates turn the actual dual action into translation. -/
theorem regularSpectralCoordinates_dual (P : SiteProfile) (s : ℝ)
    (x : RegularHilbert (TowerHilbert P)) :
    (regularSpectralCoordinates P).symm (characterMultiplier s x) =
      shift (-s/(2*Real.pi)) ((regularSpectralCoordinates P).symm x) := by
  let F := Lp.fourierTransformₗᵢ ℝ (TowerHilbert P)
  let W := regularFlowAbsorptionUnitary P
  let V := regularSpectralCoordinates P
  have hv (u : RegularHilbert (TowerHilbert P)) :
      V (shift (-s/(2*Real.pi)) u) = characterMultiplier s (V u) := by
    have hf : F.symm (shift (-s/(2*Real.pi)) u) = characterMultiplier s (F.symm u) := by
      apply F.injective
      rw [LinearIsometryEquiv.apply_symm_apply, fourier_characterMultiplier,
        LinearIsometryEquiv.apply_symm_apply]
    change W.val (F.symm (shift (-s/(2*Real.pi)) u)) =
      characterMultiplier s (W.val (F.symm u))
    rw [hf]
    exact congrArg (fun A : RegularHilbert (TowerHilbert P) →L[ℂ]
      RegularHilbert (TowerHilbert P) => A (F.symm u))
      (operatorFieldLift_commutes_character (regularFlowField P 1) s)
  apply V.injective
  rw [LinearIsometryEquiv.apply_symm_apply, hv, LinearIsometryEquiv.apply_symm_apply]

/-- Domain and graph covariance: h C_s = exp(s) C_s h. This is the graph form
of Ad(C_s) h = exp(-s) h, not a claim based only on imaginary powers. -/
theorem regularPositiveGenerator_dual_graph (P : SiteProfile) (s : ℝ)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularPositiveGenerator P).graph) :
    (characterMultiplier s x,(Real.exp s : ℂ) • characterMultiplier s y) ∈
      (regularPositiveGenerator P).graph := by
  rw [regularPositiveGenerator_graph_iff] at hxy ⊢
  rw [map_smul, regularSpectralCoordinates_dual, regularSpectralCoordinates_dual]
  let q : ℝ := -s/(2*Real.pi)
  filter_upwards [Lp.coeFn_smul (Real.exp s : ℂ)
      (shift q ((regularSpectralCoordinates P).symm y)),
    shift_ae q ((regularSpectralCoordinates P).symm y),
    shift_ae q ((regularSpectralCoordinates P).symm x),
    (measurePreserving_sub_right volume q).quasiMeasurePreserving.ae hxy]
    with ξ h1 h2 h3 h4
  rw [h1,Pi.smul_apply,h2,h3,h4,smul_smul]
  rw [← Complex.ofReal_mul, ← Real.exp_add]
  have he : s + -(2*Real.pi*(ξ-q)) = -(2*Real.pi*ξ) := by
    dsimp [q]
    field_simp
    ring
  rw [he]

theorem regularPositiveGenerator_dual_scaling (P : SiteProfile) (s : ℝ)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      (characterMultiplier s x,(Real.exp s : ℂ) • characterMultiplier s y) ∈
        (regularPositiveGenerator P).graph := by
  constructor
  · exact regularPositiveGenerator_dual_graph P s x y
  · intro h
    have hh := regularPositiveGenerator_dual_graph P (-s) _ _ h
    have hi (u : RegularHilbert (TowerHilbert P)) :
        characterMultiplier (-s) (characterMultiplier s u) = u := by
      simpa only [neg_neg] using characterMultiplier_inverse (-s) u
    have he : (Real.exp (-s) : ℂ) * (Real.exp s : ℂ) = 1 := by
      rw [← Complex.ofReal_mul, ← Real.exp_add, neg_add_cancel, Real.exp_zero,
        Complex.ofReal_one]
    simpa only [map_smul,hi,smul_smul,he,one_smul] using hh

#print axioms fourierInv_shift_schwartz
#print axioms fourierInv_shift
#print axioms fourier_characterMultiplier
#print axioms operatorFieldLift_commutes_character
#print axioms regularSpectralCoordinates_dual
#print axioms regularPositiveGenerator_dual_graph
#print axioms regularPositiveGenerator_dual_scaling
end
end TGLV350.Regular
