import Lean
import TGLExt.V350PartialOperatorSquare
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open WithLp TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The complex linear graph in the Hilbert direct sum. -/
def linearL2Graph (D : H →ₗ.[ℂ] H) : Submodule ℂ (WithLp 2 (H × H)) where
  carrier := {p | ofLp p ∈ D.graph}
  zero_mem' := D.graph.zero_mem
  add_mem' := fun hp hq => D.graph.add_mem hp hq
  smul_mem' := fun c p hp => D.graph.smul_mem c hp

theorem linearL2Graph_closed (D : H →ₗ.[ℂ] H) (hc : D.IsClosed) :
    IsClosed (linearL2Graph D : Set (WithLp 2 (H × H))) :=
  hc.preimage (WithLp.prod_continuous_ofLp 2 H H)

/-- Projection on the complex graph yields the full complex variational identity. -/
theorem closedLinear_weak_resolvent (D : H →ₗ.[ℂ] H) (hc : D.IsClosed) (z : H) :
    ∃ x : D.domain, ∀ u : D.domain,
      inner ℂ (z-(x : H)) (u : H) = inner ℂ (D x) (D u) := by
  let G := linearL2Graph D
  letI : CompleteSpace G := (linearL2Graph_closed D hc).completeSpace_coe
  let p := Submodule.starProjection (𝕜 := ℂ) G (toLp 2 (z,(0 : H)))
  have hp : ofLp p ∈ D.graph :=
    Submodule.starProjection_apply_mem (𝕜 := ℂ) G (toLp 2 (z,(0 : H)))
  obtain ⟨x,hx,hDx⟩ := (LinearPMap.mem_graph_iff D).mp hp
  have he : ofLp p = ((x : H),D x) := Prod.ext hx.symm hDx.symm
  refine ⟨x,?_⟩
  intro u
  have hu : toLp 2 ((u : H),D u) ∈ G :=
    (LinearPMap.mem_graph_iff D).mpr ⟨u,rfl,rfl⟩
  have ho := Submodule.starProjection_inner_eq_zero (𝕜 := ℂ) (K := G)
    (toLp 2 (z,(0 : H))) (toLp 2 ((u : H),D u)) hu
  rw [WithLp.prod_inner_apply] at ho
  change inner ℂ (z-(ofLp p).1) (u : H) + inner ℂ (0-(ofLp p).2) (D u)=0 at ho
  rw [he] at ho
  simp only [zero_sub,inner_neg_left] at ho
  exact sub_eq_zero.mp ho

/-- Surjectivity of I+D² for the prescribed self-adjoint partial operator. -/
theorem selfadjoint_one_add_square_onto (D : H →ₗ.[ℂ] H)
    (hs : IsSelfAdjoint D) (z : H) :
    ∃ u : (partialOperatorSquare D).domain,
      (u : H)+partialOperatorSquare D u=z := by
  obtain ⟨x,hx⟩ := closedLinear_weak_resolvent D hs.isClosed z
  have hm : D x ∈ D.adjoint.domain :=
    LinearPMap.mem_adjoint_domain_of_exists (D x) ⟨z-(x : H),hx⟩
  have ha : D.adjoint ⟨D x,hm⟩=z-(x : H) :=
    LinearPMap.adjoint_apply_eq hs.dense_domain ⟨D x,hm⟩ hx
  have hg : (D x,z-(x : H)) ∈ D.adjoint.graph :=
    (LinearPMap.mem_graph_iff D.adjoint).mpr ⟨⟨D x,hm⟩,rfl,ha⟩
  rw [show D.adjoint=D from hs] at hg
  have hsq : ((x : H),z-(x : H)) ∈ (partialOperatorSquare D).graph :=
    (partialOperatorSquare_graph_iff D (x : H) (z-(x : H))).mpr
      ⟨D x,(LinearPMap.mem_graph_iff D).mpr ⟨x,rfl,rfl⟩,hg⟩
  obtain ⟨u,hu,hDu⟩ := (LinearPMap.mem_graph_iff (partialOperatorSquare D)).mp hsq
  refine ⟨u,?_⟩
  change (u : H)+partialOperatorSquare D u=z
  rw [hu,hDu]
  change (x : H)+(z-(x : H))=z
  abel

#print axioms linearL2Graph_closed
#print axioms closedLinear_weak_resolvent
#print axioms selfadjoint_one_add_square_onto
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
