import Lean
import TGLExt.O16.LightRayVerticalDecay_v4

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter Complex
open scoped Topology

namespace ChatgptAudit.LightRayCore016

theorem spectral_slice_integrable (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b)
    (r p y : ℝ) (hy0 : 0 ≤ y) (hy : y ≤ Real.pi) :
    Integrable (fun x : ℝ => spectralIntegrand a b r p ((x : ℂ) + (y : ℂ)*I)) := by
  have hg := (gaussian_slice_integrable b hb r 0).norm.const_mul
    (Real.exp (2*Real.pi*|p| *Real.pi))
  apply hg.mono'
  · exact ((spectralIntegrand_entire a b r p).continuous.comp (by fun_prop)).aestronglyMeasurable
  · apply Eventually.of_forall
    intro x
    simpa using spectralIntegrand_strip_bound a b ha hb r p x y hy0 hy

theorem spectral_contour_shift (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) (r p : ℝ) :
    (∫ x : ℝ, spectralIntegrand a b r p ((x : ℂ) + (Real.pi : ℂ)*I)) =
      ∫ x : ℝ, spectralIntegrand a b r p (x : ℂ) := by
  apply horizontal_integral_eq_of_vertical_limit _ (spectralIntegrand_entire a b r p) Real.pi
  · simpa using spectral_slice_integrable a b ha hb r p 0 le_rfl Real.pi_pos.le
  · exact spectral_slice_integrable a b ha hb r p Real.pi Real.pi_pos.le le_rfl
  · exact spectral_vertical_limit a b ha hb r p

theorem spectral_top_factor (a b r p x : ℝ) :
    spectralIntegrand a b r p ((x : ℂ) + (Real.pi : ℂ)*I) =
      (Real.exp (2*Real.pi^2*p) : ℂ) *
        (exp (-2*(Real.pi : ℂ)*I*(p : ℂ)*(x : ℂ)) *
          star (multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ))) := by
  have he : -2*(Real.pi : ℂ)*I*(p : ℂ)*((x : ℂ)+(Real.pi : ℂ)*I) =
      ((2*Real.pi^2*p : ℝ) : ℂ) + (-2*(Real.pi : ℂ)*I*(p : ℂ)*(x : ℂ)) := by
    push_cast
    ring_nf
    simp [I_sq]
  unfold spectralIntegrand
  rw [he, exp_add, ← ofReal_exp]
  have ht := product_twist a b r x
  rw [mul_comm I (Real.pi : ℂ)] at ht
  rw [ht]
  ring

theorem spectral_boundary_balance (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) (r p : ℝ) :
    (∫ x : ℝ, exp (-2*(Real.pi : ℂ)*I*(p : ℂ)*(x : ℂ)) *
      (multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ))) =
    (Real.exp (2*Real.pi^2*p) : ℂ) *
      (∫ x : ℝ, exp (-2*(Real.pi : ℂ)*I*(p : ℂ)*(x : ℂ)) *
        star (multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ))) := by
  have h := spectral_contour_shift a b ha hb r p
  simp_rw [spectral_top_factor] at h
  rw [integral_const_mul] at h
  exact h.symm

#print axioms spectral_slice_integrable
#print axioms spectral_contour_shift
#print axioms spectral_top_factor
#print axioms spectral_boundary_balance

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
