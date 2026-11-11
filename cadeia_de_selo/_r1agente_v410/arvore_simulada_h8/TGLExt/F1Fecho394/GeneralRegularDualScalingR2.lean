import TGLExt.F1Fecho394.GeneralRegularSpectralGraphR2
import TGLExt.V351RegularGeneratorDualScaling
/-! Dual graph scaling for the same generic regular positive generator.
This proves the actual graph/domain covariance. It is not by itself a trace
scaling theorem; the inverse-weight construction remains a separate consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit MeasureTheory FourierTransform SchwartzMap Filter
open scoped FourierTransform ENNReal
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
/-- The same spectral coordinates turn the actual dual action into translation. -/
theorem regularSpectralCoordinates_dual (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (s : ℝ)
    (x : RegularHilbert (H)) :
    (regularSpectralCoordinates B).symm (characterMultiplier s x) =
      shift (-s/(2*Real.pi)) ((regularSpectralCoordinates B).symm x) := by
  let F := Lp.fourierTransformₗᵢ ℝ (H)
  let W := CoefficientBoost.unitary B 1
  let V := regularSpectralCoordinates B
  have hv (u : RegularHilbert (H)) :
      V (shift (-s/(2*Real.pi)) u) = characterMultiplier s (V u) := by
    have hf : F.symm (shift (-s/(2*Real.pi)) u) = characterMultiplier s (F.symm u) := by
      apply F.injective
      rw [LinearIsometryEquiv.apply_symm_apply, fourier_characterMultiplier,
        LinearIsometryEquiv.apply_symm_apply]
    change W (F.symm (shift (-s/(2*Real.pi)) u)) =
      characterMultiplier s (W (F.symm u))
    rw [hf]
    exact congrArg (fun A : RegularHilbert (H) →L[ℂ]
      RegularHilbert (H) => A (F.symm u))
      (operatorFieldLift_commutes_character (CoefficientBoost.family B 1) s)
  apply V.injective
  rw [LinearIsometryEquiv.apply_symm_apply, hv, LinearIsometryEquiv.apply_symm_apply]

/-- Domain and graph covariance: h C_s = exp(s) C_s h. This is the graph form
of Ad(C_s) h = exp(-s) h, not a claim based only on imaginary powers. -/
theorem regularPositiveGenerator_dual_graph (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (s : ℝ)
    (x y : RegularHilbert (H))
    (hxy : (x,y) ∈ (regularPositiveGenerator B).graph) :
    (characterMultiplier s x,(Real.exp s : ℂ) • characterMultiplier s y) ∈
      (regularPositiveGenerator B).graph := by
  rw [regularPositiveGenerator_graph_iff] at hxy ⊢
  rw [map_smul, regularSpectralCoordinates_dual, regularSpectralCoordinates_dual]
  let q : ℝ := -s/(2*Real.pi)
  filter_upwards [Lp.coeFn_smul (Real.exp s : ℂ)
      (shift q ((regularSpectralCoordinates B).symm y)),
    shift_ae q ((regularSpectralCoordinates B).symm y),
    shift_ae q ((regularSpectralCoordinates B).symm x),
    (measurePreserving_sub_right volume q).quasiMeasurePreserving.ae hxy]
    with ξ h1 h2 h3 h4
  rw [h1,Pi.smul_apply,h2,h3,h4,smul_smul]
  rw [← Complex.ofReal_mul, ← Real.exp_add]
  have he : s + -(2*Real.pi*(ξ-q)) = -(2*Real.pi*ξ) := by
    dsimp [q]
    field_simp
    ring
  rw [he]

theorem regularPositiveGenerator_dual_scaling (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (s : ℝ)
    (x y : RegularHilbert (H)) :
    (x,y) ∈ (regularPositiveGenerator B).graph ↔
      (characterMultiplier s x,(Real.exp s : ℂ) • characterMultiplier s y) ∈
        (regularPositiveGenerator B).graph := by
  constructor
  · exact regularPositiveGenerator_dual_graph B s x y
  · intro h
    have hh := regularPositiveGenerator_dual_graph B (-s) _ _ h
    have hi (u : RegularHilbert (H)) :
        characterMultiplier (-s) (characterMultiplier s u) = u := by
      simpa only [neg_neg] using characterMultiplier_inverse (-s) u
    have he : (Real.exp (-s) : ℂ) * (Real.exp s : ℂ) = 1 := by
      rw [← Complex.ofReal_mul, ← Real.exp_add, neg_add_cancel, Real.exp_zero,
        Complex.ofReal_one]
    simpa only [map_smul,hi,smul_smul,he,one_smul] using hh


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralCoordinates_dual
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_dual_graph
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_dual_scaling
