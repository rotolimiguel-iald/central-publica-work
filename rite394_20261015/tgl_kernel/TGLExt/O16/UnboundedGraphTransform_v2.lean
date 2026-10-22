import Lean
import TGLExt.BoundedGraphOperator
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open ChatgptAudit.Continuous049
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Kernel in the ambient Hilbert space, including actual domain membership. -/
def ambientKernel (D : H →ₗ.[ℂ] H) : Submodule ℂ H :=
  (LinearMap.ker D.toFun).map D.domain.subtype

theorem ambientKernel_mem (D : H →ₗ.[ℂ] H) (x : H) :
    x ∈ ambientKernel D ↔ ∃ u : D.domain, (u : H)=x ∧ D u=0 := by
  constructor
  · rintro ⟨u,hu,hx⟩
    exact ⟨u,hx,hu⟩
  · rintro ⟨u,hx,hu⟩
    exact ⟨u,hu,hx⟩

theorem graph_ambientKernel (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (hc : A*B=B*A) (hs : A*A+B*B=1) :
    ambientKernel (boundedGraphOperator A B hAi) = B.ker := by
  ext x
  rw [ambientKernel_mem]
  change (∃ u : (boundedGraphOperator A B hAi).domain, (u : H)=x ∧
      boundedGraphOperator A B hAi u=0) ↔ B x=0
  have hg : ((x,(0 : H)) ∈ (boundedGraphOperator A B hAi).graph) ↔
      (∃ u : (boundedGraphOperator A B hAi).domain, (u : H)=x ∧ boundedGraphOperator A B hAi u=0) :=
    LinearPMap.mem_graph_iff _
  rw [← hg, bounded_graph_equation_iff A B hAi hc hs x 0, map_zero]

theorem graph_pair_energy (A B : H →L[ℂ] H) (hA : IsSelfAdjoint A)
    (hB : IsSelfAdjoint B) (hs : A*A+B*B=1) (x : H) :
    ‖A x‖^2+‖B x‖^2=‖x‖^2 := by
  have he : inner ℂ (A x) (A x) + inner ℂ (B x) (B x) = inner ℂ x x := by
    calc
      _ = inner ℂ ((star A*A+star B*B) x) x := by
        simp only [ContinuousLinearMap.add_apply, inner_add_left, ContinuousLinearMap.mul_apply]
        exact congrArg₂ (·+·) (A.adjoint_inner_left x (A x)).symm
          (B.adjoint_inner_left x (B x)).symm
      _ = _ := by rw [hA.star_eq,hB.star_eq,hs]; rfl
  have hr := congrArg (RCLike.re : ℂ → ℝ) he
  simpa only [map_add,inner_self_eq_norm_sq] using hr

theorem graph_pair_preserves_orthogonal (A B : H →L[ℂ] H) (hA : IsSelfAdjoint A)
    (hc : A*B=B*A) (x : H) (hx : x ∈ B.kerᗮ) : A x ∈ B.kerᗮ := by
  apply (B.ker.mem_orthogonal _).mpr
  intro z hz
  have hAz : A z ∈ B.ker := by
    have h := congrArg (fun T : H →L[ℂ] H => T z) hc
    change A (B z) = B (A z) at h
    rw [show B z=0 from hz,map_zero] at h
    exact h.symm
  have he := A.adjoint_inner_left x z
  change inner ℂ (star A z) x = inner ℂ z (A x) at he
  rw [hA.star_eq] at he
  rw [← he]
  exact (B.ker.mem_orthogonal x).mp hx (A z) hAz

theorem graph_transform_gap (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hc : A*B=B*A) (hs : A*A+B*B=1) (γ : ℝ) (hγ : 0 ≤ γ)
    (hgap : ∀ u : (boundedGraphOperator A B hAi).domain,
      (u : H) ∈ (ambientKernel (boundedGraphOperator A B hAi))ᗮ →
        γ*‖(u : H)‖ ≤ ‖boundedGraphOperator A B hAi u‖) :
    ∀ x ∈ B.kerᗮ, (γ/Real.sqrt (1+γ^2))*‖x‖ ≤ ‖B x‖ := by
  intro x hx
  have hAx := graph_pair_preserves_orthogonal A B hA hc x hx
  have hu : (boundedGraphLift A B hAi x : H) ∈
      (ambientKernel (boundedGraphOperator A B hAi))ᗮ := by
    rw [graph_ambientKernel A B hAi hc hs]
    exact hAx
  have hg := hgap (boundedGraphLift A B hAi x) hu
  rw [bounded_graph_lift_coe, bounded_graph_lift_apply] at hg
  have hgs : (γ*‖A x‖)^2 ≤ ‖B x‖^2 :=
    (sq_le_sq₀ (by positivity) (norm_nonneg _)).mpr hg
  have he := graph_pair_energy A B hA hB hs x
  have hsq : (Real.sqrt (1+γ^2))^2=1+γ^2 := Real.sq_sqrt (by positivity)
  have hp : 0<Real.sqrt (1+γ^2) := Real.sqrt_pos.mpr (by positivity)
  rw [div_mul_eq_mul_div]
  apply (div_le_iff₀ hp).mpr
  apply (sq_le_sq₀ (by positivity) (by positivity)).mp
  have hsq' := congrArg (fun t : ℝ => t*‖B x‖^2) hsq
  have he' := congrArg (fun t : ℝ => γ^2*t) he
  nlinarith

theorem graph_transform_contraction (A B : H →L[ℂ] H) (hA : IsSelfAdjoint A)
    (hB : IsSelfAdjoint B) (hs : A*A+B*B=1) (x : H) : ‖B x‖ ≤ ‖x‖ := by
  have he := graph_pair_energy A B hA hB hs x
  nlinarith [sq_nonneg ‖A x‖,norm_nonneg (B x),norm_nonneg x]

#print axioms ambientKernel_mem
#print axioms graph_ambientKernel
#print axioms graph_pair_energy
#print axioms graph_pair_preserves_orthogonal
#print axioms graph_transform_gap
#print axioms graph_transform_contraction
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
