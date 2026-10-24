import TGLExt.V350FourierUniqueness
import TGLExt.V350L2CharacterMultiplier

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2200000

namespace TGLV350.Regular
open MeasureTheory Filter FourierTransform
open scoped FourierTransform ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The ordinary Fourier transform uses the same characters as the dual action,
with the explicit conversion from frequency to angular frequency. -/
theorem fourier_eq_character_integral (f : ℝ → H) (ξ : ℝ) :
    (𝓕 f) ξ = ∫ x : ℝ, characterPhase (2*Real.pi*ξ) x • f x := by
  rw [Real.fourier_real_eq_integral_exp_smul]
  apply integral_congr_ae
  apply Eventually.of_forall
  intro x
  dsimp only
  unfold characterPhase
  congr 2
  push_cast
  ring

theorem fourier_inner_eq_character_pairing (f g : RegularHilbert H) (ξ : ℝ) :
    (𝓕 (fun x : ℝ => inner ℂ (f x) (g x))) ξ =
      inner ℂ f (characterMultiplier (2*Real.pi*ξ) g) := by
  rw [fourier_eq_character_integral, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [characterMultiplier_ae (2*Real.pi*ξ) g] with x hx
  rw [hx, inner_smul_right]
  rfl

/-- Character commutation forces equality of the pointwise pairings almost
everywhere, for every pair of L2 vectors. No decomposable-operator theorem or
separability hypothesis on the fibre Hilbert space is imported. -/
theorem character_commutation_local_pairing
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (f g : RegularHilbert H) :
    (fun x : ℝ => inner ℂ ((B.adjoint f) x) (g x)) =ᵐ[volume]
      (fun x : ℝ => inner ℂ (f x) ((B g) x)) := by
  apply Fourier.fourier_integral_ae_injective _ _
    (L2.integrable_inner (𝕜 := ℂ) (B.adjoint f) g)
    (L2.integrable_inner (𝕜 := ℂ) f (B g))
  intro ξ
  rw [fourier_inner_eq_character_pairing, fourier_inner_eq_character_pairing,
    ContinuousLinearMap.adjoint_inner_left]
  apply congrArg (fun v => inner ℂ f v)
  exact (congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T g)
    (hB (2*Real.pi*ξ))).symm

#print axioms fourier_eq_character_integral
#print axioms fourier_inner_eq_character_pairing
#print axioms character_commutation_local_pairing
end
end TGLV350.Regular
