import Lean
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.BoundedTransform016
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def graphRoot (D : H →L[ℂ] H) : H →L[ℂ] H := CFC.sqrt (1 + star D * D)
def graphInverseRoot (D : H →L[ℂ] H) : H →L[ℂ] H := Ring.inverse (graphRoot D)
def boundedTransform (D : H →L[ℂ] H) : H →L[ℂ] H := D * graphInverseRoot D

theorem graphPositive (D : H →L[ℂ] H) : IsStrictlyPositive (1 + star D * D) :=
  isStrictlyPositive_one.add_nonneg (star_mul_self_nonneg D)

theorem graphRoot_unit (D : H →L[ℂ] H) : IsUnit (graphRoot D) :=
  (CFC.isUnit_sqrt_iff _ (graphPositive D).nonneg).mpr (graphPositive D).isUnit

theorem graphRoot_square (D : H →L[ℂ] H) :
    graphRoot D * graphRoot D = 1 + star D * D :=
  CFC.sqrt_mul_sqrt_self _ (graphPositive D).nonneg

theorem graphRoot_selfadjoint (D : H →L[ℂ] H) : star (graphRoot D) = graphRoot D :=
  (CFC.sqrt_nonneg _).isSelfAdjoint.star_eq

theorem graphRoot_inverse_right (D : H →L[ℂ] H) :
    graphRoot D * graphInverseRoot D = 1 :=
  Ring.mul_inverse_cancel _ (graphRoot_unit D)

theorem graphRoot_inverse_left (D : H →L[ℂ] H) :
    graphInverseRoot D * graphRoot D = 1 :=
  Ring.inverse_mul_cancel _ (graphRoot_unit D)

theorem graphRoot_norm_sq (D : H →L[ℂ] H) (x : H) :
    ‖graphRoot D x‖^2 = ‖x‖^2 + ‖D x‖^2 := by
  have hi : inner ℂ (graphRoot D x) (graphRoot D x) =
      inner ℂ x x + inner ℂ (D x) (D x) := by
    calc
      _ = inner ℂ ((star (graphRoot D) * graphRoot D) x) x :=
        ((graphRoot D).adjoint_inner_left x (graphRoot D x)).symm
      _ = inner ℂ ((1 + star D*D) x) x := by
        rw [graphRoot_selfadjoint, graphRoot_square]
      _ = _ := by
        simp only [ContinuousLinearMap.add_apply, ContinuousLinearMap.one_apply,
          ContinuousLinearMap.mul_apply, inner_add_left]
        exact congrArg (fun z : ℂ => inner ℂ x x + z) (D.adjoint_inner_left x (D x))
  have hr := congrArg (RCLike.re : ℂ → ℝ) hi
  simpa only [map_add, inner_self_eq_norm_sq] using hr

theorem transform_energy_identity (D : H →L[ℂ] H) (x : H) :
    ‖x‖^2 = ‖graphInverseRoot D x‖^2 + ‖boundedTransform D x‖^2 := by
  have hx : graphRoot D (graphInverseRoot D x) = x :=
    congrArg (fun T : H →L[ℂ] H => T x) (graphRoot_inverse_right D)
  simpa only [hx, boundedTransform, ContinuousLinearMap.mul_apply] using
    graphRoot_norm_sq D (graphInverseRoot D x)

#print axioms graphPositive
#print axioms graphRoot_unit
#print axioms graphRoot_square
#print axioms graphRoot_selfadjoint
#print axioms graphRoot_inverse_right
#print axioms graphRoot_inverse_left
#print axioms graphRoot_norm_sq
#print axioms transform_energy_identity
end ChatgptAudit.BoundedTransform016


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
