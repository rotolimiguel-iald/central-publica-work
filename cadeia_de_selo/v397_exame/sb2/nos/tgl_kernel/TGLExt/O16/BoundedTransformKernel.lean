import Lean
import TGLExt.O16.BoundedTransformCore_v2

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.BoundedTransform016
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem unit_apply_eq_zero (T : H →L[ℂ] H) (hT : IsUnit T) (x : H)
    (hx : T x = 0) : x = 0 := by
  have hi := congrArg (fun A : H →L[ℂ] H => A x) (Ring.inverse_mul_cancel T hT)
  change Ring.inverse T (T x) = x at hi
  rw [hx, map_zero] at hi
  exact hi.symm

theorem graphRoot_fixes_kernel (D : H →L[ℂ] H) (x : H) (hx : D x = 0) :
    graphRoot D x = x := by
  have hu : IsUnit (graphRoot D + 1) :=
    ((isStrictlyPositive_one : IsStrictlyPositive (1 : H →L[ℂ] H)).nonneg_add
      (CFC.sqrt_nonneg (1 + star D*D))).isUnit
  have hp : (graphRoot D + 1)*(graphRoot D - 1) = star D*D := by
    calc
      _ = graphRoot D*graphRoot D - 1 := by noncomm_ring
      _ = _ := by rw [graphRoot_square]; abel
  have hz : (graphRoot D + 1) ((graphRoot D - 1) x) = 0 := by
    have he := congrArg (fun A : H →L[ℂ] H => A x) hp
    simpa only [ContinuousLinearMap.mul_apply, hx, map_zero] using he
  have h := unit_apply_eq_zero _ hu _ hz
  change graphRoot D x - x = 0 at h
  exact sub_eq_zero.mp h

theorem graphInverseRoot_fixes_kernel (D : H →L[ℂ] H) (x : H) (hx : D x = 0) :
    graphInverseRoot D x = x := by
  have h := congrArg (fun A : H →L[ℂ] H => A x) (graphRoot_inverse_left D)
  change graphInverseRoot D (graphRoot D x) = x at h
  rwa [graphRoot_fixes_kernel D x hx] at h

theorem boundedTransform_zero_iff (D : H →L[ℂ] H) (x : H) :
    boundedTransform D x = 0 ↔ D x = 0 := by
  constructor
  · intro h
    change D (graphInverseRoot D x) = 0 at h
    have hfix := graphRoot_fixes_kernel D (graphInverseRoot D x) h
    have hi := congrArg (fun A : H →L[ℂ] H => A x) (graphRoot_inverse_right D)
    change graphRoot D (graphInverseRoot D x) = x at hi
    rw [hi] at hfix
    rwa [← hfix] at h
  · intro h
    change D (graphInverseRoot D x) = 0
    rwa [graphInverseRoot_fixes_kernel D x h]

theorem boundedTransform_kernel (D : H →L[ℂ] H) : (boundedTransform D).ker = D.ker := by
  ext x
  exact boundedTransform_zero_iff D x

theorem graphInverseRoot_selfadjoint (D : H →L[ℂ] H) :
    star (graphInverseRoot D) = graphInverseRoot D := by
  have hp : IsStrictlyPositive (graphRoot D) :=
    (graphRoot_unit D).isStrictlyPositive (CFC.sqrt_nonneg _)
  exact hp.ringInverse.isSelfAdjoint.star_eq

theorem graphInverseRoot_preserves_kernel_orthogonal (D : H →L[ℂ] H) (x : H)
    (hx : x ∈ D.kerᗮ) : graphInverseRoot D x ∈ D.kerᗮ := by
  apply (D.ker.mem_orthogonal _).mpr
  intro z hz
  have hi := (graphInverseRoot D).adjoint_inner_left x z
  change inner ℂ (star (graphInverseRoot D) z) x = inner ℂ z (graphInverseRoot D x) at hi
  rw [graphInverseRoot_selfadjoint, graphInverseRoot_fixes_kernel D z hz] at hi
  rw [← hi]
  exact (D.ker.mem_orthogonal x).mp hx z hz

#print axioms unit_apply_eq_zero
#print axioms graphRoot_fixes_kernel
#print axioms graphInverseRoot_fixes_kernel
#print axioms boundedTransform_zero_iff
#print axioms boundedTransform_kernel
#print axioms graphInverseRoot_selfadjoint
#print axioms graphInverseRoot_preserves_kernel_orthogonal
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
