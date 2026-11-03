import Lean
import TGLExt.O16.BoundedTransformGap
import Mathlib.Analysis.CStarAlgebra.Matrix

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.BoundedTransform016

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem graphInverseRoot_eq_rpow (D : H →L[ℂ] H) :
    graphInverseRoot D = CFC.rpow (1 + star D*D) (-1/2) := by
  unfold graphInverseRoot graphRoot
  rw [CFC.sqrt_eq_rpow, CFC.inverse_rpow _ _ (by norm_num) (graphPositive D)]
  norm_num

theorem boundedTransform_formula (D : H →L[ℂ] H) :
    boundedTransform D = D * CFC.rpow (1 + star D*D) (-1/2) := by
  rw [boundedTransform, graphInverseRoot_eq_rpow]

theorem graphRoot_preserves_kernel_orthogonal (D : H →L[ℂ] H) (x : H)
    (hx : x ∈ D.kerᗮ) : graphRoot D x ∈ D.kerᗮ := by
  apply (D.ker.mem_orthogonal _).mpr
  intro z hz
  have hi := (graphRoot D).adjoint_inner_left x z
  change inner ℂ (star (graphRoot D) z) x = inner ℂ z (graphRoot D x) at hi
  rw [graphRoot_selfadjoint, graphRoot_fixes_kernel D z hz] at hi
  rw [← hi]
  exact (D.ker.mem_orthogonal x).mp hx z hz

theorem gap_attainment_transports (D : H →L[ℂ] H) (γ : ℝ) (hγ : 0 ≤ γ)
    (x : H) (hx : ‖D x‖ = γ*‖x‖) :
    ‖boundedTransform D (graphRoot D x)‖ =
      (γ/Real.sqrt (1+γ^2))*‖graphRoot D x‖ := by
  have hs : (Real.sqrt (1+γ^2))^2 = 1+γ^2 := Real.sq_sqrt (by positivity)
  have hsp : 0 < Real.sqrt (1+γ^2) := Real.sqrt_pos.mpr (by positivity)
  have he := graphRoot_norm_sq D x
  rw [hx] at he
  have hs' := congrArg (fun t : ℝ => t * ‖x‖^2) hs
  have hn : ‖graphRoot D x‖ = Real.sqrt (1+γ^2)*‖x‖ := by
    apply (sq_eq_sq₀ (norm_nonneg _) (by positivity)).mp
    nlinarith
  rw [boundedTransform_graphRoot, hx, hn]
  field_simp

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The bounded transform represented as an actual finite matrix via the canonical star equivalence. -/
def finiteTransform (D : Matrix n n ℂ) : Matrix n n ℂ :=
  (Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)).symm (boundedTransform ((Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) D))

theorem finiteTransform_operator (D : Matrix n n ℂ) :
    (Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) (finiteTransform D) =
      (Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) D *
        CFC.rpow (1 + star ((Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) D)*(Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) D) (-1/2) := by
  simp only [finiteTransform, StarAlgEquiv.apply_symm_apply]
  exact boundedTransform_formula _

theorem finiteTransform_kernel (D : Matrix n n ℂ) :
    ((Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) (finiteTransform D)).ker = ((Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) D).ker := by
  simp only [finiteTransform, StarAlgEquiv.apply_symm_apply]
  exact boundedTransform_kernel _

theorem finiteTransform_gap (D : Matrix n n ℂ) (γ : ℝ) (hγ : 0 ≤ γ)
    (hgap : ∀ x ∈ ((Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) D).kerᗮ, γ*‖x‖ ≤ ‖(Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) D x‖) :
    ∀ x ∈ ((Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) (finiteTransform D)).kerᗮ,
      (γ/Real.sqrt (1+γ^2))*‖x‖ ≤ ‖(Matrix.toEuclideanCLM (n := n) (𝕜 := ℂ)) (finiteTransform D) x‖ := by
  simp only [finiteTransform, StarAlgEquiv.apply_symm_apply]
  exact boundedTransform_gap _ γ hγ hgap

#print axioms graphInverseRoot_eq_rpow
#print axioms boundedTransform_formula
#print axioms graphRoot_preserves_kernel_orthogonal
#print axioms gap_attainment_transports
#print axioms finiteTransform_operator
#print axioms finiteTransform_kernel
#print axioms finiteTransform_gap
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
