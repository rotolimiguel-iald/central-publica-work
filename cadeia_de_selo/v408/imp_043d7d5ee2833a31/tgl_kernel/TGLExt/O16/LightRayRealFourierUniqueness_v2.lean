import Lean
import TGLExt.O16.LightRayFourierBoundary_v2
import TGLExt.V350FourierUniqueness

set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter Complex FourierTransform
open scoped FourierTransform

namespace ChatgptAudit.LightRayCore016

def reflectedConjugate (q : ℝ → ℂ) (p : ℝ) : ℂ := star (q (-p))

theorem fourier_reflected_conjugate (q : ℝ → ℂ) (r : ℝ) :
    𝓕 (reflectedConjugate q) r = star (𝓕 q r) := by
  have h := congrFun (Real.fourierInv_eq_fourier_comp_neg (fun x : ℝ => star (q x))) r
  rw [Real.fourierInv_eq_fourier_neg, fourier_star_reverse, neg_neg] at h
  exact h.symm

theorem fourier_sum_apply (q s : ℝ → ℂ) (hq : Integrable q) (hs : Integrable s) (r : ℝ) :
    𝓕 (q+s) r = 𝓕 q r + 𝓕 s r := by
  exact congrFun (VectorFourier.fourierIntegral_add
    (L := innerₗ ℝ) Real.continuous_fourierChar continuous_inner hq hs) r

theorem real_fourier_zero_implies_antisymmetry (q : ℝ → ℂ)
    (hq : Integrable q) (hs : Integrable (reflectedConjugate q))
    (hreal : ∀ r : ℝ, (𝓕 q r).re = 0) :
    (fun p => q p + reflectedConjugate q p) =ᵐ[volume] (0 : ℝ → ℂ) := by
  apply TGLV350.Fourier.fourier_integral_ae_injective _ _ (hq.add hs) (integrable_zero _ _ _)
  intro r
  change 𝓕 (q + reflectedConjugate q) r = 𝓕 (0 : ℝ → ℂ) r
  rw [fourier_sum_apply q _ hq hs, fourier_reflected_conjugate]
  have hz : 𝓕 (0 : ℝ → ℂ) r = 0 := by simp [fourier_explicit]
  rw [hz]
  apply Complex.ext <;> simp [Complex.star_def, hreal r]

theorem positive_reflection_real_fourier_unique (q : ℝ → ℂ) (w : ℝ → ℝ)
    (hq : Integrable q) (hs : Integrable (reflectedConjugate q))
    (hw : ∀ᵐ p : ℝ ∂volume, 0 ≤ w p)
    (hreflection : reflectedConjugate q =ᵐ[volume] fun p => (w p : ℂ) * q p)
    (hreal : ∀ r : ℝ, (𝓕 q r).re = 0) : q =ᵐ[volume] (0 : ℝ → ℂ) := by
  have hz := real_fourier_zero_implies_antisymmetry q hq hs hreal
  filter_upwards [hz, hw, hreflection] with p hp hwp hsp
  change q p + reflectedConjugate q p = 0 at hp
  rw [hsp] at hp
  have hn : ((1+w p : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (ne_of_gt (show 0 < 1+w p by linarith))
  have he : ((1+w p : ℝ) : ℂ) * q p = 0 := by
    simpa only [ofReal_add, ofReal_one, add_mul, one_mul] using hp
  exact (mul_eq_zero.mp he).resolve_left hn

#print axioms fourier_reflected_conjugate
#print axioms fourier_sum_apply
#print axioms real_fourier_zero_implies_antisymmetry
#print axioms positive_reflection_real_fourier_unique

end ChatgptAudit.LightRayCore016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
