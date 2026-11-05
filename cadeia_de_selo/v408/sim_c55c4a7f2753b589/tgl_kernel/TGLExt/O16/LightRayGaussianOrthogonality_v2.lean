import Lean
import TGLExt.O16.LightRayGaussianTransform_v5
import TGLExt.O16.LightRayDensitySeparation_v2
import TGLExt.O16.LightRayCoreExtension_v2

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Complex
open scoped FourierTransform InnerProductSpace
open ChatgptAudit.Continuous049 ChatgptAudit.FourierBridge016

namespace ChatgptAudit.LightRayCore016
local instance instLocalLightRayGaussianOrthogonalityv21 : Module ℝ SpectralHilbert := NormedSpace.complexToReal.toModule
local instance instLocalLightRayGaussianOrthogonalityv22 : NormedSpace ℝ SpectralHilbert := NormedSpace.complexToReal

theorem gaussian_core_fourier_ae (b : ℝ) (hb : 0 < b) (r : ℝ) :
    fourierUnitary (productCore 0 b r le_rfl hb) =ᵐ[volume]
      fun p => (gaussianSpectralWeight b p : ℂ) *
        exp (-2*(Real.pi : ℂ)*I*(r : ℂ)*(p : ℂ)) := by
  have hf1 : Integrable (fun x : ℝ => multiplier 0 (x : ℂ) * twistedGaussian b r (x : ℂ)) := by
    simpa using product_slice_integrable 0 b le_rfl hb r 0 le_rfl Real.pi_pos.le
  have hf2 : MemLp (fun x : ℝ => multiplier 0 (x : ℂ) * twistedGaussian b r (x : ℂ))
      2 (volume : Measure ℝ) := by
    simpa using product_slice_memLp 0 b le_rfl hb r 0 le_rfl Real.pi_pos.le
  have hF := TGLV350.Fourier.fourier_integral_ae_eq_L2 _ hf1 hf2
  filter_upwards [hF] with p hp
  change (𝓕 (hf2.toLp _) : SpectralHilbert) p = _
  rw [← hp]
  have hz : (fun x : ℝ => multiplier 0 (x : ℂ) * twistedGaussian b r (x : ℂ)) =
      (fun x : ℝ => twistedGaussian b r (x : ℂ)) := by
    funext x
    simp [multiplier]
  rw [hz, twisted_gaussian_fourier b hb r p]

theorem gaussian_core_inner_fourier (b : ℝ) (hb : 0 < b) (r : ℝ) (h : SpectralHilbert) :
    inner ℂ h (productCore 0 b r le_rfl hb) =
      𝓕 (fun p => star (fourierUnitary h p) * (gaussianSpectralWeight b p : ℂ)) r := by
  rw [← fourierUnitary.inner_map_map h (productCore 0 b r le_rfl hb), L2.inner_def,
    fourier_explicit]
  apply integral_congr_ae
  filter_upwards [gaussian_core_fourier_ae b hb r] with p hp
  rw [hp]
  simp only [RCLike.inner_apply, Complex.star_def]
  ring

theorem gaussian_core_real_orthogonal_separates (b : ℝ) (hb : 0 < b) (h : SpectralHilbert)
    (hK : h ∈ (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule)
    (horth : ∀ r : ℝ, (inner ℂ h (productCore 0 b r le_rfl hb)).re = 0) : h = 0 := by
  have hz : fourierUnitary h = 0 := weighted_real_fourier_separates_standard
    (2*Real.pi^2) (fourierUnitary h) (gaussianSpectralWeight b)
    ((rapidity_standard_mem _ h).mp hK) (gaussian_spectral_memLp b hb)
    (Eventually.of_forall (gaussian_spectral_positive b hb))
    (gaussian_spectral_reflection b)
    (by intro r; rw [← gaussian_core_inner_fourier b hb r h]; exact horth r)
  apply fourierUnitary.injective
  simpa using hz

#print axioms gaussian_core_fourier_ae
#print axioms gaussian_core_inner_fourier
#print axioms gaussian_core_real_orthogonal_separates
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
