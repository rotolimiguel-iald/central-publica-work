import Lean
import TGLExt.O16.TeleologicalTail_v3
import Mathlib.MeasureTheory.Integral.IntegralEqImproper
import Mathlib.Analysis.Calculus.MeanValue

set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory Set Filter
open scoped Topology
namespace ChatgptAudit.Teleological016

theorem tail_tendsto_zero (f : ℝ → ℝ) : Tendsto (tail f) atTop (𝓝 0) :=
  MeasureTheory.tendsto_integral_Ioi_zero tendsto_id

theorem moment_bounds_scaled_tail (f : ℝ → ℝ) (x : ℝ) (hx : 0 ≤ x)
    (hmoment : IntegrableOn (fun u => u*f u) (Ioi x)) :
    ‖x*tail f x‖ ≤ tail (fun u => ‖u*f u‖) x := by
  unfold tail
  rw [← integral_const_mul]
  apply norm_integral_le_of_norm_le hmoment.norm
  filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
  have hu0 : 0 ≤ u := hx.trans (le_of_lt hu)
  simp only [norm_mul,Real.norm_eq_abs,abs_of_nonneg hx,abs_of_nonneg hu0]
  exact mul_le_mul_of_nonneg_right (le_of_lt hu) (abs_nonneg _)

theorem scaled_tail_tendsto_zero (f : ℝ → ℝ)
    (hmoment : ∀ x, IntegrableOn (fun u => u*f u) (Ioi x)) :
    Tendsto (fun x => x*tail f x) atTop (𝓝 0) := by
  apply squeeze_zero_norm'
    (Filter.eventually_atTop.2 ⟨0,fun x hx => moment_bounds_scaled_tail f x hx (hmoment x)⟩)
  exact tail_tendsto_zero (fun u => ‖u*f u‖)

theorem weighted_tail_tendsto_zero (f : ℝ → ℝ)
    (hint : ∀ x, IntegrableOn f (Ioi x))
    (hmoment : ∀ x, IntegrableOn (fun u => u*f u) (Ioi x)) :
    Tendsto (weightedTail f) atTop (𝓝 0) := by
  have h := (tail_tendsto_zero (fun u => u*f u)).sub (scaled_tail_tendsto_zero f hmoment)
  simpa only [sub_zero,← weightedTail_split f hint hmoment] using h

theorem same_source_homogeneous (a b theta eta source : ℝ → ℝ)
    (ha : ∀ x, HasDerivAt a (theta x) x)
    (hb : ∀ x, HasDerivAt b (eta x) x)
    (ht : ∀ x, HasDerivAt theta (source x) x)
    (he : ∀ x, HasDerivAt eta (source x) x) :
    ∃ A B : ℝ, ∀ x, a x-b x=A+B*x := by
  have hdt : ∀ x, HasDerivAt (fun y => theta y-eta y) 0 x := by
    intro x
    exact ((ht x).sub (he x)).congr_deriv (sub_self _)
  have hconst := is_const_of_deriv_eq_zero (fun x => (hdt x).differentiableAt)
    (fun x => (hdt x).deriv)
  let B := theta 0-eta 0
  have hd : ∀ x, HasDerivAt (fun y => a y-b y-B*y) 0 x := by
    intro x
    have hh := ((ha x).sub (hb x)).sub ((hasDerivAt_id x).const_mul B)
    exact hh.congr_deriv (by have h := hconst x 0; dsimp [B] at *; linarith)
  have hc := is_const_of_deriv_eq_zero (fun x => (hd x).differentiableAt)
    (fun x => (hd x).deriv)
  refine ⟨a 0-b 0,B,?_⟩
  intro x
  have h := hc x 0
  linarith

#print axioms tail_tendsto_zero
#print axioms moment_bounds_scaled_tail
#print axioms scaled_tail_tendsto_zero
#print axioms weighted_tail_tendsto_zero
#print axioms same_source_homogeneous
end ChatgptAudit.Teleological016


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
