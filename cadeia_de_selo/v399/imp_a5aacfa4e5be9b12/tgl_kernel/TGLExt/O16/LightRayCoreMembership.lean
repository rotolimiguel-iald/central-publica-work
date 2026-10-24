import Lean
import TGLExt.O16.LightRayFourierBoundary_v2
import TGLExt.V350FourierL1L2
import TGLExt.O16.FourierStandardTransport_v3

set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter Complex
open scoped FourierTransform
open ChatgptAudit.Continuous049 ChatgptAudit.FourierBridge016

namespace ChatgptAudit.LightRayCore016

local instance instLocalLightRayCoreMembership1 : Module ℝ SpectralHilbert := NormedSpace.complexToReal.toModule
local instance instLocalLightRayCoreMembership2 : NormedSpace ℝ SpectralHilbert := NormedSpace.complexToReal

/-- The pointwise balance pays the actual weighted domain obligation, using Jf as witness. -/
theorem spectral_balance_mem_standard (c : ℝ) (f : SpectralHilbert)
    (h : f =ᵐ[volume] fun x => (Real.exp (c*x) : ℂ) * star (f (-x))) :
    f ∈ (continuousStandardSubspace c).toClosedSubmodule := by
  have hw : spectralJ f =ᵐ[volume] fun x => (Real.exp (-c*x) : ℂ) * f x := by
    filter_upwards [spectralJ_ae f, h] with x hx hfx
    rw [hx, hfx, ← mul_assoc]
    have he : (Real.exp (-c*x) : ℂ) * (Real.exp (c*x) : ℂ) = 1 := by
      norm_cast
      rw [← Real.exp_add]
      ring_nf
      exact Real.exp_zero
    rw [he, one_mul]
  have hf : f ∈ (continuousModularOperator c).domain :=
    (continuous_modular_domain_iff c f).mpr ((Lp.memLp (spectralJ f)).ae_eq hw)
  apply (continuous_standard_fixed_iff c f).mpr
  refine ⟨hf, ?_⟩
  apply Lp.ext
  filter_upwards [continuous_tomita_apply_ae c ⟨f,hf⟩, h] with x hx hy
  exact hx.trans hy.symm

def productCore (a b r : ℝ) (ha : 0 ≤ a) (hb : 0 < b) : SpectralHilbert :=
  (show MemLp (fun x : ℝ => multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ))
    2 (volume : Measure ℝ) from by
      simpa using product_slice_memLp a b ha hb r 0 le_rfl Real.pi_pos.le).toLp _

theorem product_core_fourier_balance (a b r : ℝ) (ha : 0 ≤ a) (hb : 0 < b) :
    fourierUnitary (productCore a b r ha hb) =ᵐ[volume]
      fun x => (Real.exp ((2*Real.pi^2)*x) : ℂ) *
        star (fourierUnitary (productCore a b r ha hb) (-x)) := by
  have hf1 : Integrable (fun x : ℝ => multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ)) := by
    simpa using product_slice_integrable a b ha hb r 0 le_rfl Real.pi_pos.le
  have hf2 : MemLp (fun x : ℝ => multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ))
      2 (volume : Measure ℝ) := by
    simpa using product_slice_memLp a b ha hb r 0 le_rfl Real.pi_pos.le
  have hF := TGLV350.Fourier.fourier_integral_ae_eq_L2 _ hf1 hf2
  have hneg := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae hF
  filter_upwards [hF, hneg] with x hx hy
  change (𝓕 (hf2.toLp _) : SpectralHilbert) x =
    (Real.exp ((2*Real.pi^2)*x) : ℂ) * star ((𝓕 (hf2.toLp _) : SpectralHilbert) (-x))
  rw [← hx, ← hy]
  exact product_fourier_modular_balance a b ha hb r x

theorem product_core_mem_rapidity_standard (a b r : ℝ) (ha : 0 ≤ a) (hb : 0 < b) :
    productCore a b r ha hb ∈ (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule := by
  rw [rapidity_standard_mem]
  exact spectral_balance_mem_standard _ _ (product_core_fourier_balance a b r ha hb)

#print axioms spectral_balance_mem_standard
#print axioms product_core_fourier_balance
#print axioms product_core_mem_rapidity_standard

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
