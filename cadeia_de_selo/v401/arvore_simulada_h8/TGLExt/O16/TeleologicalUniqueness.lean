import Lean
import TGLExt.O16.TeleologicalBoundary_v2

set_option autoImplicit false
noncomputable section
open Filter
open scoped Topology
namespace ChatgptAudit.Teleological016

theorem vanishing_derivative_unique (f g d : ℝ → ℝ)
    (hf : ∀ x, HasDerivAt f (d x) x) (hg : ∀ x, HasDerivAt g (d x) x)
    (lf : Tendsto f atTop (𝓝 0)) (lg : Tendsto g atTop (𝓝 0)) : f=g := by
  have hd : ∀ x, HasDerivAt (fun y => f y-g y) 0 x := by
    intro x
    exact ((hf x).sub (hg x)).congr_deriv (sub_self _)
  have hc := is_const_of_deriv_eq_zero (fun x => (hd x).differentiableAt)
    (fun x => (hd x).deriv)
  have hlim : Tendsto (fun _ : ℝ => f 0-g 0) atTop (𝓝 0) := by
    have h := lf.sub lg
    simp only [sub_zero] at h
    exact h.congr (fun x => hc x 0)
  have hzero : f 0-g 0=0 := tendsto_nhds_unique tendsto_const_nhds hlim
  funext x
  have h := hc x 0
  linarith

theorem teleological_pair_unique (a b theta eta source : ℝ → ℝ)
    (ha : ∀ x, HasDerivAt a (theta x) x)
    (hb : ∀ x, HasDerivAt b (eta x) x)
    (ht : ∀ x, HasDerivAt theta (source x) x)
    (he : ∀ x, HasDerivAt eta (source x) x)
    (la : Tendsto a atTop (𝓝 0)) (lb : Tendsto b atTop (𝓝 0))
    (lt : Tendsto theta atTop (𝓝 0)) (le : Tendsto eta atTop (𝓝 0)) :
    a=b ∧ theta=eta := by
  have hte := vanishing_derivative_unique theta eta source ht he lt le
  refine ⟨?_,hte⟩
  apply vanishing_derivative_unique a b theta ha
  · simpa only [hte] using hb
  · exact la
  · exact lb

#print axioms vanishing_derivative_unique
#print axioms teleological_pair_unique
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
