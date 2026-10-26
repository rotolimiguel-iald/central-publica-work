import Lean
import TGLExt.O16.LightRayRealFourierUniqueness_v2
import TGLExt.O16.LightRayCoreMembership

set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter Complex FourierTransform
open scoped FourierTransform
open ChatgptAudit.Continuous049

namespace ChatgptAudit.LightRayCore016
local instance instModuleRealSHDensSep : Module ℝ SpectralHilbert := NormedSpace.complexToReal.toModule
local instance instNormedSpaceRealSHDensSep : NormedSpace ℝ SpectralHilbert := NormedSpace.complexToReal

theorem continuous_standard_balance (c : ℝ) (H : SpectralHilbert)
    (hH : H ∈ (continuousStandardSubspace c).toClosedSubmodule) :
    H =ᵐ[volume] fun p => (Real.exp (c*p) : ℂ) * star (H (-p)) := by
  obtain ⟨hdom, hfixed⟩ := (continuous_standard_fixed_iff c H).mp hH
  have h := continuous_tomita_apply_ae c ⟨H,hdom⟩
  rwa [hfixed] at h

theorem reflected_conjugate_integrable (q : ℝ → ℂ) (hq : Integrable q) :
    Integrable (reflectedConjugate q) := by
  exact (memLp_one_iff_integrable.mp (memLp_one_iff_integrable.mpr hq).star).comp_neg

theorem spectral_weighted_product_reflection (c : ℝ) (H : SpectralHilbert) (g : ℝ → ℝ)
    (hH : H ∈ (continuousStandardSubspace c).toClosedSubmodule)
    (hg : ∀ p, g (-p) = Real.exp (-c*p)*g p) :
    reflectedConjugate (fun p => star (H p) * (g p : ℂ)) =ᵐ[volume]
      fun p => (Real.exp (-2*c*p) : ℂ) * (star (H p) * (g p : ℂ)) := by
  have hneg := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (continuous_standard_balance c H hH)
  filter_upwards [hneg] with p hp
  have hp' : H (-p) = (Real.exp (-c*p) : ℂ) * star (H p) := by
    simpa only [neg_neg, mul_neg, neg_mul] using hp
  change star (star (H (-p)) * (g (-p) : ℂ)) = _
  rw [star_mul, star_star]
  have hgr : star (g (-p) : ℂ) = (g (-p) : ℂ) := by simp
  rw [hgr, hp', hg p, ofReal_mul]
  have he : (Real.exp (-c*p) : ℂ) * (Real.exp (-c*p) : ℂ) = (Real.exp (-2*c*p) : ℂ) := by
    rw [← ofReal_mul]
    congr 1
    rw [← Real.exp_add]
    congr 1
    ring
  calc
    _ = ((Real.exp (-c*p) : ℂ) * (Real.exp (-c*p) : ℂ)) *
        (star (H p) * (g p : ℂ)) := by ring
    _ = _ := by rw [he]

/-- The positive weight separates K using only real Fourier data; its hypotheses are explicit. -/
theorem weighted_real_fourier_separates_standard (c : ℝ) (H : SpectralHilbert) (g : ℝ → ℝ)
    (hH : H ∈ (continuousStandardSubspace c).toClosedSubmodule)
    (hg2 : MemLp (fun p => (g p : ℂ)) 2 (volume : Measure ℝ))
    (hgpos : ∀ᵐ p : ℝ ∂volume, 0 < g p)
    (hgref : ∀ p, g (-p) = Real.exp (-c*p)*g p)
    (hreal : ∀ r, (𝓕 (fun p => star (H p) * (g p : ℂ)) r).re = 0) : H = 0 := by
  let q : ℝ → ℂ := fun p => star (H p) * (g p : ℂ)
  have hq : Integrable q := (Lp.memLp H).star.integrable_mul hg2
  have hz := positive_reflection_real_fourier_unique q (fun p => Real.exp (-2*c*p))
    hq (reflected_conjugate_integrable q hq)
    (Eventually.of_forall fun p => (Real.exp_pos _).le)
    (spectral_weighted_product_reflection c H g hH hgref) hreal
  apply Lp.eq_zero_iff_ae_eq_zero.mpr
  filter_upwards [hz, hgpos] with p hp hgp
  change star (H p) * (g p : ℂ) = 0 at hp
  have hn : (g p : ℂ) ≠ 0 := by exact_mod_cast ne_of_gt hgp
  have hs : star (H p) = 0 := (mul_eq_zero.mp hp).resolve_right hn
  change H p = 0
  simpa only [star_star, star_zero] using congrArg star hs

#print axioms continuous_standard_balance
#print axioms reflected_conjugate_integrable
#print axioms spectral_weighted_product_reflection
#print axioms weighted_real_fourier_separates_standard
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
