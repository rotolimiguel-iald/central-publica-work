import Lean
import TGLExt.O16.PolarQuotientGeometry_v2
import TGLExt.BoostHeatConstruction

set_option autoImplicit false
noncomputable section
open Filter
open scoped Topology
namespace ChatgptAudit.PolarPeriod016
open TGLExt ChatgptAudit.Boost044 ChatgptAudit.Wave029

theorem boost_defect_with_derived_period (a c rate mass eta t period : ℝ)
    (hr : 0 < rate) (hp : 0 < period)
    (h : AngularQuotientFaithful rate period) :
    boostSegmentDefect a c rate mass eta t =
      boostSegmentHeat a c rate (waveMatter a c mass) t -
        ((1/period)*eta)*boostSegmentArea a c t := by
  rw [reciprocal_temperature hr hp h]
  rfl

theorem polar_period_scale {kappa period c : ℝ} (hk : kappa ≠ 0) (hc : c ≠ 0)
    (h : AngularQuotientFaithful kappa period) :
    AngularQuotientFaithful (c*kappa) (period/c) := by
  apply (faithful_period_iff (mul_ne_zero hc hk)).mpr
  have he : (c*kappa)*(period/c) = kappa*period := by field_simp
  rw [he]
  exact (faithful_period_iff hk).mp h

theorem reciprocal_temperature_scale (period c : ℝ) :
    1/(period/c) = c*(1/period) := by simp [div_eq_mul_inv, mul_comm]

theorem kappa_temperature_ratio {kappa period : ℝ} (hk : 0 < kappa)
    (hp : 0 < period) (h : AngularQuotientFaithful kappa period) :
    kappa/(1/period) = 2*Real.pi := by
  rw [reciprocal_temperature hk hp h]
  field_simp

theorem temperature_ratio_scale (kappa temperature c : ℝ) (hc : c ≠ 0) :
    (c*kappa)/(c*temperature) = kappa/temperature := by
  exact mul_div_mul_left kappa temperature hc

theorem boost_balance_scale_iff (a c rate mass eta scale : ℝ)
    (ha : 0 ≤ a) (hc : 0 ≤ c) (hr : rate ≠ 0) (hs : scale ≠ 0) :
    Tendsto (fun t => boostSegmentDefect a c (scale*rate) mass eta t/t^2)
      (𝓝[<] 0) (𝓝 0) ↔
    Tendsto (fun t => boostSegmentDefect a c rate mass eta t/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  rw [boost_segment_quadratic_balance_iff a c ha hc (scale*rate) mass eta (mul_ne_zero hs hr),
      boost_segment_quadratic_balance_iff a c ha hc rate mass eta hr]

#print axioms boost_defect_with_derived_period
#print axioms polar_period_scale
#print axioms reciprocal_temperature_scale
#print axioms kappa_temperature_ratio
#print axioms temperature_ratio_scale
#print axioms boost_balance_scale_iff
end ChatgptAudit.PolarPeriod016


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
