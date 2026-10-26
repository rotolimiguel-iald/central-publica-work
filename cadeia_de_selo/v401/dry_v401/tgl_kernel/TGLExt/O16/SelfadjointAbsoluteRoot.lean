import Lean
import TGLExt.O16.SameSquareDomain
import TGLExt.V350ResolventSquareRoot

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def selfadjointAbsoluteRoot (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) : H →ₗ.[ℂ] H :=
  resolventSquareRoot (selfadjointSquareResolvent D hs)
    (selfadjoint_square_resolvent_nonneg D hs) (selfadjoint_square_resolvent_injective D hs)

theorem selfadjoint_absolute_selfadjoint (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    IsSelfAdjoint (selfadjointAbsoluteRoot D hs) :=
  resolventSquareRoot_selfadjoint _ _ _ (selfadjoint_square_resolvent_le_one D hs)

theorem selfadjoint_absolute_square (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    partialOperatorSquare (selfadjointAbsoluteRoot D hs)=partialOperatorSquare D :=
  (resolventSquareRoot_square _ _ _ (selfadjoint_square_resolvent_le_one D hs)).trans
    (selfadjoint_square_resolvent_graph D hs)

theorem selfadjoint_absolute_positive (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (x : (selfadjointAbsoluteRoot D hs).domain) :
    0 ≤ (inner ℂ (x : H) (selfadjointAbsoluteRoot D hs x)).re :=
  resolventSquareRoot_positive _ _ _ x

theorem selfadjoint_absolute_domain (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    (selfadjointAbsoluteRoot D hs).domain=D.domain :=
  sameSquare_domain_eq _ _ _ (selfadjoint_absolute_selfadjoint D hs) hs
    (selfadjoint_absolute_square D hs) rfl

theorem selfadjoint_normalizer_range (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    (CFC.sqrt (selfadjointSquareResolvent D hs)).range=D.domain :=
  selfadjoint_absolute_domain D hs

theorem selfadjoint_absolute_norm (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (x : D.domain) :
    ‖D x‖=‖selfadjointAbsoluteRoot D hs
      (Submodule.inclusion (le_of_eq (selfadjoint_absolute_domain D hs).symm) x)‖ := by
  have h := sameSquare_norm_full D (selfadjointAbsoluteRoot D hs) (partialOperatorSquare D)
    hs (selfadjoint_absolute_selfadjoint D hs) rfl (selfadjoint_absolute_square D hs) x
  exact h

#print axioms selfadjoint_absolute_selfadjoint
#print axioms selfadjoint_absolute_square
#print axioms selfadjoint_absolute_positive
#print axioms selfadjoint_absolute_domain
#print axioms selfadjoint_normalizer_range
#print axioms selfadjoint_absolute_norm
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
