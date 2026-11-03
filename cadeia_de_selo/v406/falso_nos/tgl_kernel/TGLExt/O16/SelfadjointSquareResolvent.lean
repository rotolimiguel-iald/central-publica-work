import Lean
import TGLExt.O16.ClosedLinearGraphResolvent_v2
import TGLExt.V350PartialPositiveResolvent
import TGLExt.V350PartialSquareGraphCore
import TGLExt.V350PartialSquareEnergy

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem selfadjoint_formal (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    D.IsFormalAdjoint D := by
  have h := LinearPMap.adjoint_isFormalAdjoint hs.dense_domain
  rwa [show D.adjoint=D from hs] at h

theorem selfadjoint_square_positive (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (x : (partialOperatorSquare D).domain) :
    0 ≤ (inner ℂ (x : H) (partialOperatorSquare D x)).re := by
  obtain ⟨u,_,he⟩ := partialSquare_energy D (partialOperatorSquare D)
    (selfadjoint_formal D hs) rfl x
  rw [← he]
  exact sq_nonneg _

theorem selfadjoint_square_formal (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    (partialOperatorSquare D).IsFormalAdjoint (partialOperatorSquare D) := by
  intro x y
  let inc := Submodule.inclusion (partialSquare_domain_le D (partialOperatorSquare D) rfl)
  have hxy := partialSquare_pairing_all D (partialOperatorSquare D) rfl
    (selfadjoint_formal D hs) y (inc x)
  have hyx := partialSquare_pairing_all D (partialOperatorSquare D) rfl
    (selfadjoint_formal D hs) x (inc y)
  change inner ℂ (x : H) (partialOperatorSquare D y) = inner ℂ (D (inc x)) (D (inc y)) at hxy
  change inner ℂ (y : H) (partialOperatorSquare D x) = inner ℂ (D (inc y)) (D (inc x)) at hyx
  calc
    inner ℂ (partialOperatorSquare D x) (y : H) = inner ℂ (D (inc x)) (D (inc y)) := by
      rw [← inner_conj_symm,hyx,inner_conj_symm]
    _ = inner ℂ (x : H) (partialOperatorSquare D y) := hxy.symm

/-- Constructed from the prescribed self-adjoint D, not supplied as an input. -/
def selfadjointSquareResolvent (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) : H →L[ℂ] H :=
  partialPositiveResolvent (partialOperatorSquare D) (selfadjoint_square_positive D hs)
    (selfadjoint_one_add_square_onto D hs)

theorem selfadjoint_square_resolvent_nonneg (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    0 ≤ selfadjointSquareResolvent D hs :=
  partialPositiveResolvent_nonneg _ _ _ (selfadjoint_square_formal D hs)

theorem selfadjoint_square_resolvent_le_one (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    selfadjointSquareResolvent D hs ≤ 1 :=
  partialPositiveResolvent_le_one _ _ _ (selfadjoint_square_formal D hs)

theorem selfadjoint_square_resolvent_injective (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    Function.Injective (selfadjointSquareResolvent D hs) :=
  partialPositiveResolvent_injective _ _ _

theorem selfadjoint_square_resolvent_equation (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (z : H) :
    ∃ u : (partialOperatorSquare D).domain,
      (u : H)=selfadjointSquareResolvent D hs z ∧ (u : H)+partialOperatorSquare D u=z :=
  partialPositiveResolvent_equation _ _ _ z

theorem selfadjoint_square_resolvent_graph (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    resolventGraphOperator (selfadjointSquareResolvent D hs)
      (selfadjoint_square_resolvent_injective D hs) = partialOperatorSquare D :=
  partialPositiveResolvent_graph _ _ _

#print axioms selfadjoint_formal
#print axioms selfadjoint_square_positive
#print axioms selfadjoint_square_formal
#print axioms selfadjoint_square_resolvent_nonneg
#print axioms selfadjoint_square_resolvent_le_one
#print axioms selfadjoint_square_resolvent_injective
#print axioms selfadjoint_square_resolvent_equation
#print axioms selfadjoint_square_resolvent_graph
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
