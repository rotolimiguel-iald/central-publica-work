import Lean
import TGLExt.O16.BoundedTransformKernel
import Mathlib.Analysis.Matrix.Normed

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.BoundedTransform016
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem boundedTransform_contraction (D : H →L[ℂ] H) (x : H) :
    ‖boundedTransform D x‖ ≤ ‖x‖ := by
  have he := transform_energy_identity D x
  nlinarith [sq_nonneg (‖graphInverseRoot D x‖), norm_nonneg x,
    norm_nonneg (boundedTransform D x)]

theorem boundedTransform_gap (D : H →L[ℂ] H) (γ : ℝ) (hγ : 0 ≤ γ)
    (hgap : ∀ x ∈ D.kerᗮ, γ * ‖x‖ ≤ ‖D x‖) :
    ∀ x ∈ (boundedTransform D).kerᗮ,
      (γ / Real.sqrt (1+γ^2)) * ‖x‖ ≤ ‖boundedTransform D x‖ := by
  intro x hx
  rw [boundedTransform_kernel] at hx
  have hy := graphInverseRoot_preserves_kernel_orthogonal D x hx
  have hg := hgap (graphInverseRoot D x) hy
  change γ * ‖graphInverseRoot D x‖ ≤ ‖boundedTransform D x‖ at hg
  have hgs : (γ * ‖graphInverseRoot D x‖)^2 ≤ ‖boundedTransform D x‖^2 :=
    (sq_le_sq₀ (by positivity) (norm_nonneg _)).mpr hg
  have he := transform_energy_identity D x
  have hs : (Real.sqrt (1+γ^2))^2 = 1+γ^2 := Real.sq_sqrt (by positivity)
  have hsp : 0 < Real.sqrt (1+γ^2) := Real.sqrt_pos.mpr (by positivity)
  rw [div_mul_eq_mul_div]
  apply (div_le_iff₀ hsp).mpr
  apply (sq_le_sq₀ (by positivity) (by positivity)).mp
  have hs' := congrArg (fun t : ℝ => t * ‖boundedTransform D x‖^2) hs
  have he' := congrArg (fun t : ℝ => γ^2 * t) he
  nlinarith

theorem boundedTransform_graphRoot (D : H →L[ℂ] H) (x : H) :
    boundedTransform D (graphRoot D x) = D x := by
  have hi := congrArg (fun A : H →L[ℂ] H => A x) (graphRoot_inverse_left D)
  change graphInverseRoot D (graphRoot D x) = x at hi
  change D (graphInverseRoot D (graphRoot D x)) = D x
  rw [hi]

#print axioms boundedTransform_contraction
#print axioms boundedTransform_gap
#print axioms boundedTransform_graphRoot
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
