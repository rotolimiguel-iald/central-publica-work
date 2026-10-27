import TGLExt.F1Fecho394.CanonicalWedge
/-! Reflection of spectral rapidity and complex conjugation cancel the two
sign changes in the real boost character. This is proved on the unchanged
canonical H1, not assumed from the names of the operators. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.CanonicalJBoost
open TGLExt.ImportedSQ F1Rede.Canonical F1Rede.CanonicalWedge
open F1Rede.SpectralConjugation F1Rede.FiberConjugation TGLV350.Regular

theorem Js_character (s : ℝ) (f : RH) :
    Js (characterMultiplier s f) = characterMultiplier s (Js f) := by
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (characterMultiplier_ae s f)
  filter_upwards [J_ae transverseGeometricJ transverseGeometricJ_involutive (characterMultiplier s f),
    characterMultiplier_ae s (Js f),J_ae transverseGeometricJ transverseGeometricJ_involutive f,hr]
    with ξ h1 h2 h3 h4
  change (Js (characterMultiplier s f) : RH) ξ = _ at h1
  change (Js f : RH) ξ = _ at h3
  rw [h1,h2,h3,h4,map_smulₛₗ]
  congr 1
  simp [characterPhase,Complex.star_def,← Complex.exp_conj]

theorem Jcandidate_boost (s : ℝ) (f : H1) :
    Jcandidate (B0 s f) = B0 s (Jcandidate f) := by
  apply Phi.injective
  calc
    Phi (Jcandidate (B0 s f)) = Js (Phi (B0 s f)) := by
      rw [Jcandidate_apply,LinearIsometryEquiv.apply_symm_apply]
    _ = Js (characterMultiplier (2*Real.pi*s) (Phi f)) := by
      rw [canonicalPartialFourier_boost]
    _ = characterMultiplier (2*Real.pi*s) (Js (Phi f)) := Js_character _ _
    _ = Phi (B0 s (Jcandidate f)) := by
      rw [canonicalPartialFourier_boost,Jcandidate_apply,LinearIsometryEquiv.apply_symm_apply]

end F1Fecho.CanonicalJBoost
#print axioms F1Fecho.CanonicalJBoost.Js_character
#print axioms F1Fecho.CanonicalJBoost.Jcandidate_boost
