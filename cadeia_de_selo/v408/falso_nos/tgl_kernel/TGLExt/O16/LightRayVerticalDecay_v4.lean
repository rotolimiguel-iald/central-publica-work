import Lean
import TGLExt.O16.LightRayContourTransport_v2

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter Complex
open scoped Topology

namespace ChatgptAudit.LightRayCore016

def spectralIntegrand (a b r p : ℝ) (z : ℂ) : ℂ :=
  exp (-2 * (Real.pi : ℂ) * I * (p : ℂ) * z) *
    (multiplier a z * twistedGaussian b r z)

theorem spectralIntegrand_entire (a b r p : ℝ) :
    Differentiable ℂ (spectralIntegrand a b r p) := by
  unfold spectralIntegrand multiplier twistedGaussian
  fun_prop

theorem spectralIntegrand_strip_bound (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b)
    (r p x y : ℝ) (hy0 : 0 ≤ y) (hy : y ≤ Real.pi) :
    ‖spectralIntegrand a b r p ((x : ℂ) + (y : ℂ) * I)‖ ≤
      Real.exp (2 * Real.pi * |p| * Real.pi) * ‖twistedGaussian b r (x : ℂ)‖ := by
  have he : ‖exp (-2 * (Real.pi : ℂ) * I * (p : ℂ) *
      ((x : ℂ) + (y : ℂ) * I))‖ = Real.exp (2 * Real.pi * p * y) := by
    rw [norm_exp]
    congr 1
    simp [mul_re, mul_im]
  have hpy : p*y ≤ |p| *Real.pi :=
    (mul_le_mul_of_nonneg_right (le_abs_self p) hy0).trans
      (mul_le_mul_of_nonneg_left hy (abs_nonneg p))
  have hp : Real.exp (2 * Real.pi * p * y) ≤ Real.exp (2 * Real.pi * |p| * Real.pi) := by
    apply Real.exp_le_exp.mpr
    nlinarith [Real.pi_pos]
  unfold spectralIntegrand
  rw [norm_mul, he]
  apply mul_le_mul hp _ (norm_nonneg _) (Real.exp_pos _).le
  simpa only [mul_comm I] using product_uniform_strip_bound a b ha hb r x y hy0 hy

theorem gaussian_norm_atTop (b : ℝ) (hb : 0 < b) (r : ℝ) :
    Tendsto (fun x : ℝ => ‖twistedGaussian b r (x : ℂ)‖) atTop (𝓝 0) := by
  simp_rw [gaussian_real_norm]
  apply Real.tendsto_exp_atBot.comp
  have hx : Tendsto (fun x : ℝ => x-r) atTop atTop := by
    simpa [sub_eq_add_neg] using tendsto_atTop_add_const_right atTop (-r) tendsto_id
  have h : Tendsto (fun x : ℝ => b * (x-r)^2) atTop atTop := by
    apply (tendsto_const_mul_atTop_of_pos hb).mpr
    simpa only [pow_two] using
      Tendsto.atTop_mul_atTop₀ hx hx
  simpa [neg_mul] using tendsto_atBot_add_const_right atTop
    (b * (Real.pi/2)^2) (tendsto_neg_atTop_atBot.comp h)

theorem gaussian_norm_neg_atTop (b : ℝ) (hb : 0 < b) (r : ℝ) :
    Tendsto (fun x : ℝ => ‖twistedGaussian b r ((-x : ℝ) : ℂ)‖) atTop (𝓝 0) := by
  have he : (fun x : ℝ => ‖twistedGaussian b r ((-x : ℝ) : ℂ)‖) =
      (fun x : ℝ => ‖twistedGaussian b (-r) (x : ℂ)‖) := by
    funext x
    rw [gaussian_real_norm, gaussian_real_norm]
    congr 1
    ring
  rw [he]
  exact gaussian_norm_atTop b hb (-r)

theorem spectral_vertical_integral_bound (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b)
    (r p x : ℝ) :
    ‖∫ y : ℝ in (0:ℝ)..Real.pi,
      spectralIntegrand a b r p ((x : ℂ) + (y : ℂ) * I)‖ ≤
      (Real.exp (2*Real.pi*|p| *Real.pi) * ‖twistedGaussian b r (x : ℂ)‖) * Real.pi := by
  have h := intervalIntegral.norm_integral_le_of_norm_le_const
    (fun y hy => spectralIntegrand_strip_bound a b ha hb r p x y
      (by have := (Set.uIoc_of_le Real.pi_pos.le ▸ hy).1; linarith)
      (Set.uIoc_of_le Real.pi_pos.le ▸ hy).2)
  simpa [abs_of_nonneg Real.pi_pos.le] using h

theorem spectral_vertical_limit (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) (r p : ℝ) :
    Tendsto (verticalDifference (spectralIntegrand a b r p) Real.pi) atTop (𝓝 0) := by
  have hpos : Tendsto (fun T : ℝ => ∫ y : ℝ in (0:ℝ)..Real.pi,
      spectralIntegrand a b r p ((T : ℂ) + (y : ℂ)*I)) atTop (𝓝 0) := by
    rw [tendsto_zero_iff_norm_tendsto_zero]
    apply tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds
      (by simpa using ((gaussian_norm_atTop b hb r).const_mul
        (Real.exp (2*Real.pi*|p| *Real.pi))).mul_const Real.pi)
      (Eventually.of_forall fun _ => norm_nonneg _)
    exact Eventually.of_forall (spectral_vertical_integral_bound a b ha hb r p)
  have hneg : Tendsto (fun T : ℝ => ∫ y : ℝ in (0:ℝ)..Real.pi,
      spectralIntegrand a b r p ((-T : ℝ) + (y : ℂ)*I)) atTop (𝓝 0) := by
    rw [tendsto_zero_iff_norm_tendsto_zero]
    apply tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds
      (by simpa using ((gaussian_norm_neg_atTop b hb r).const_mul
        (Real.exp (2*Real.pi*|p| *Real.pi))).mul_const Real.pi)
      (Eventually.of_forall fun _ => norm_nonneg _)
    exact Eventually.of_forall fun T => by
      simpa only [ofReal_neg] using spectral_vertical_integral_bound a b ha hb r p (-T)
  have h := (hpos.const_mul I).sub (hneg.const_mul I)
  convert h using 1 <;> try { funext T; simp only [verticalDifference, ofReal_neg] }
  all_goals simp only [mul_zero, sub_zero]

#print axioms spectralIntegrand_entire
#print axioms spectralIntegrand_strip_bound
#print axioms gaussian_norm_atTop
#print axioms gaussian_norm_neg_atTop
#print axioms spectral_vertical_integral_bound
#print axioms spectral_vertical_limit

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
