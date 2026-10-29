import Lean
import TGLExt.O16.UnboundedGraphTransform_v2
import TGLExt.ContinuousModularDomain

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open ChatgptAudit.Continuous049

/-- The exact existing continuous operator, not a finite-dimensional replacement. -/
theorem continuous_transform_action (c : ℝ) (x : SpectralHilbert) :
    continuousModularOperator c
      (boundedGraphLift (spectralA c) (spectralB c) (spectralA_injective c) x) =
      spectralB c x :=
  bounded_graph_lift_apply _ _ _ x

theorem continuous_transform_kernel (c : ℝ) :
    ambientKernel (continuousModularOperator c) = (spectralB c).ker :=
  graph_ambientKernel _ _ _ (spectralAB_commute c) (spectralAB_square_sum c)

/-- This transports a supplied lower bound; it does not assert a positive gap. -/
theorem continuous_transform_gap (c γ : ℝ) (hγ : 0 ≤ γ)
    (hgap : ∀ u : (continuousModularOperator c).domain,
      (u : SpectralHilbert) ∈ (ambientKernel (continuousModularOperator c))ᗮ →
        γ*‖(u : SpectralHilbert)‖ ≤ ‖continuousModularOperator c u‖) :
    ∀ x ∈ (spectralB c).kerᗮ,
      (γ/Real.sqrt (1+γ^2))*‖x‖ ≤ ‖spectralB c x‖ :=
  graph_transform_gap _ _ _ (spectralA_selfadjoint c) (spectralB_selfadjoint c)
    (spectralAB_commute c) (spectralAB_square_sum c) γ hγ hgap

#print axioms continuous_transform_action
#print axioms continuous_transform_kernel
#print axioms continuous_transform_gap
end ChatgptAudit.UnboundedTransform016


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
