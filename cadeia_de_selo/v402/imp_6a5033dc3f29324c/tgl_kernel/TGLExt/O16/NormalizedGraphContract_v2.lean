import Lean
import TGLExt.O16.UnboundedGraphTransform_v2
import TGLExt.V350PartialOperatorSquare
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open ChatgptAudit.Continuous049 TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Geometric graph data, without assuming any kernel or gap conclusion. -/
structure NormalizedGraphWitness (D : H →ₗ.[ℂ] H) where
  A : H →L[ℂ] H
  B : H →L[ℂ] H
  positiveA : 0 ≤ A
  selfadjointB : IsSelfAdjoint B
  injectiveA : Function.Injective A
  commute : A*B=B*A
  squares : A*A+B*B=1
  represents : D=boundedGraphOperator A B injectiveA

/-- The named analytic conclusion; existence for an arbitrary prescribed D is not assumed. -/
def BoundedTransformPreservesKernelAndGap
    (D : H →ₗ.[ℂ] H) (b : H →L[ℂ] H) : Prop :=
  ambientKernel D=b.ker ∧ (∀ x, ‖b x‖ ≤ ‖x‖) ∧
  ∀ γ : ℝ, 0 ≤ γ →
    (∀ u : D.domain, (u : H) ∈ (ambientKernel D)ᗮ → γ*‖(u : H)‖ ≤ ‖D u‖) →
    ∀ x ∈ b.kerᗮ, (γ/Real.sqrt (1+γ^2))*‖x‖ ≤ ‖b x‖

theorem normalized_graph_pays_contract (D : H →ₗ.[ℂ] H)
    (w : NormalizedGraphWitness D) : BoundedTransformPreservesKernelAndGap D w.B := by
  rcases w with ⟨A,B,hA,hB,hi,hc,hs,he⟩
  dsimp only at *
  subst D
  exact ⟨graph_ambientKernel A B hi hc hs,
    graph_transform_contraction A B hA.isSelfAdjoint hB hs,
    fun γ hγ hg => graph_transform_gap A B hi hA.isSelfAdjoint hB hc hs γ hγ hg⟩

theorem normalized_graph_inverse_one_add_square (D : H →ₗ.[ℂ] H)
    (w : NormalizedGraphWitness D) (z : H) :
    ∃ u : (partialOperatorSquare D).domain,
      (u : H)=(w.A*w.A) z ∧ (u : H)+partialOperatorSquare D u=z := by
  rcases w with ⟨A,B,hA,hB,hiA,hc,hs,he⟩
  dsimp only at *
  subst D
  have hi : Function.Injective (A*A) := hiA.comp hiA
  have hb : B*B=1-A*A := eq_sub_iff_add_eq.mpr (by simpa only [add_comm] using hs)
  rw [boundedGraph_square_eq_resolvent A B (A*A) hiA hi hc rfl hb]
  exact resolvent_graph_resolvent_equation (A*A) hi z

theorem normalized_graph_normalizer_is_sqrt (D : H →ₗ.[ℂ] H)
    (w : NormalizedGraphWitness D) : CFC.sqrt (w.A*w.A)=w.A :=
  CFC.sqrt_unique rfl w.positiveA

#print axioms normalized_graph_pays_contract
#print axioms normalized_graph_inverse_one_add_square
#print axioms normalized_graph_normalizer_is_sqrt
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
