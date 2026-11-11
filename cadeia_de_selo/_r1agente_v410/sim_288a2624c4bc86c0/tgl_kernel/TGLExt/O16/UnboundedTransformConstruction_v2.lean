import Lean
import TGLExt.O16.SelfadjointAbsoluteRoot
import TGLExt.O16.ResolventBoundedTransform_v3

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open ChatgptAudit.Continuous049 TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def normalizedInput (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) : H →ₗ[ℂ] D.domain :=
  (CFC.sqrt (selfadjointSquareResolvent D hs)).toLinearMap.codRestrict D.domain (by
    intro x
    rw [← selfadjoint_normalizer_range D hs]
    exact ⟨x,rfl⟩)

theorem normalizedInput_coe (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (x : H) :
    (normalizedInput D hs x : H)=CFC.sqrt (selfadjointSquareResolvent D hs) x := rfl

theorem normalizedInput_image_norm (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (x : H) :
    ‖D (normalizedInput D hs x)‖=‖CFC.sqrt (1-selfadjointSquareResolvent D hs) x‖ := by
  rw [selfadjoint_absolute_norm D hs]
  have he : Submodule.inclusion (le_of_eq (selfadjoint_absolute_domain D hs).symm)
      (normalizedInput D hs x) =
    boundedGraphLift (CFC.sqrt (selfadjointSquareResolvent D hs))
      (CFC.sqrt (1-selfadjointSquareResolvent D hs))
      (positive_sqrt_injective _ (selfadjoint_square_resolvent_nonneg D hs)
        (selfadjoint_square_resolvent_injective D hs)) x := Subtype.ext rfl
  rw [he]
  change ‖boundedGraphOperator _ _ _ (boundedGraphLift _ _ _ x)‖= _
  rw [bounded_graph_lift_apply]

theorem normalizedInput_image_bound (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (x : H) :
    ‖D (normalizedInput D hs x)‖ ≤ ‖x‖ := by
  rw [normalizedInput_image_norm]
  exact resolvent_bounded_transform_contraction _ (selfadjoint_square_resolvent_nonneg D hs)
    (selfadjoint_square_resolvent_le_one D hs) x

/-- The actual bounded transform of the given unbounded D. -/
def unboundedTransform (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) : H →L[ℂ] H :=
  (D.toFun.comp (normalizedInput D hs)).mkContinuous 1 (by
    intro x
    change ‖D (normalizedInput D hs x)‖ ≤ 1*‖x‖
    rw [one_mul]
    exact normalizedInput_image_bound D hs x)

theorem unboundedTransform_apply (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (x : H) :
    unboundedTransform D hs x=D (normalizedInput D hs x) := rfl

theorem unboundedTransform_norm (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (x : H) :
    ‖unboundedTransform D hs x‖=‖CFC.sqrt (1-selfadjointSquareResolvent D hs) x‖ :=
  normalizedInput_image_norm D hs x

theorem unboundedTransform_contraction (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (x : H) :
    ‖unboundedTransform D hs x‖≤‖x‖ := normalizedInput_image_bound D hs x

#print axioms normalizedInput_coe
#print axioms normalizedInput_image_norm
#print axioms normalizedInput_image_bound
#print axioms unboundedTransform_apply
#print axioms unboundedTransform_norm
#print axioms unboundedTransform_contraction
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
