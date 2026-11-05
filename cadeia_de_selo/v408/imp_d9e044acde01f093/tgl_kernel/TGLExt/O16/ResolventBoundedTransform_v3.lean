import Lean
import TGLExt.O16.UnboundedGraphTransform_v2
import TGLExt.V350ResolventSquareRoot

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open ChatgptAudit.Continuous049 TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (R : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R) (hone : R ≤ 1)

/-- This is the actual product D sqrt(R), evaluated on its proven domain. -/
theorem resolvent_bounded_transform_action (x : H) :
    resolventSquareRoot R hR hi
      (boundedGraphLift (CFC.sqrt R) (CFC.sqrt (1-R)) (positive_sqrt_injective R hR hi) x) =
      CFC.sqrt (1-R) x :=
  bounded_graph_lift_apply _ _ _ x

include hR hone in
theorem resolvent_bounded_transform_kernel :
    ambientKernel (resolventSquareRoot R hR hi) = (CFC.sqrt (1-R)).ker :=
  graph_ambientKernel _ _ _ (resolvent_sqrt_pair_commute R)
    (resolvent_sqrt_pair_square_sum R hR hone)

include hR hone in
theorem resolvent_bounded_transform_gap (γ : ℝ) (hγ : 0 ≤ γ)
    (hgap : ∀ u : (resolventSquareRoot R hR hi).domain,
      (u : H) ∈ (ambientKernel (resolventSquareRoot R hR hi))ᗮ →
        γ*‖(u : H)‖ ≤ ‖resolventSquareRoot R hR hi u‖) :
    ∀ x ∈ (CFC.sqrt (1-R)).kerᗮ,
      (γ/Real.sqrt (1+γ^2))*‖x‖ ≤ ‖CFC.sqrt (1-R) x‖ :=
  graph_transform_gap _ _ _ (CFC.sqrt_nonneg _).isSelfAdjoint
    (CFC.sqrt_nonneg _).isSelfAdjoint (resolvent_sqrt_pair_commute R)
    (resolvent_sqrt_pair_square_sum R hR hone) γ hγ hgap

include hR hone in
theorem resolvent_bounded_transform_contraction (x : H) :
    ‖CFC.sqrt (1-R) x‖ ≤ ‖x‖ :=
  graph_transform_contraction _ _ (CFC.sqrt_nonneg _).isSelfAdjoint
    (CFC.sqrt_nonneg _).isSelfAdjoint (resolvent_sqrt_pair_square_sum R hR hone) x

-- R really inverts I+D², with the successive domain explicitly retained.
include hR hone in
theorem resolvent_is_inverse_one_add_square (z : H) :
    ∃ u : (partialOperatorSquare (resolventSquareRoot R hR hi)).domain,
      (u : H)=R z ∧ (u : H)+partialOperatorSquare (resolventSquareRoot R hR hi) u=z := by
  rw [resolventSquareRoot_square R hR hi hone]
  exact resolvent_graph_resolvent_equation R hi z

#print axioms resolvent_bounded_transform_action
#print axioms resolvent_bounded_transform_kernel
#print axioms resolvent_bounded_transform_gap
#print axioms resolvent_bounded_transform_contraction
#print axioms resolvent_is_inverse_one_add_square
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
