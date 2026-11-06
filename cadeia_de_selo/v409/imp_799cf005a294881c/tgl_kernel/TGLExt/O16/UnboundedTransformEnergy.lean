import Lean
import TGLExt.O16.UnboundedTransformConstruction_v2

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem unboundedTransform_energy (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) (x : H) :
    ‖CFC.sqrt (selfadjointSquareResolvent D hs) x‖^2 + ‖unboundedTransform D hs x‖^2=‖x‖^2 := by
  rw [unboundedTransform_norm]
  exact graph_pair_energy _ _ (CFC.sqrt_nonneg _).isSelfAdjoint
    (CFC.sqrt_nonneg _).isSelfAdjoint
    (resolvent_sqrt_pair_square_sum _ (selfadjoint_square_resolvent_nonneg D hs)
      (selfadjoint_square_resolvent_le_one D hs)) x

theorem unboundedTransform_lift (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (u : D.domain) : ∃ x : H,
      CFC.sqrt (selfadjointSquareResolvent D hs) x=(u : H) ∧
      unboundedTransform D hs x=D u := by
  have hu : (u : H) ∈ (CFC.sqrt (selfadjointSquareResolvent D hs)).range := by
    rw [selfadjoint_normalizer_range]
    exact u.property
  obtain ⟨x,hx⟩ := hu
  refine ⟨x,hx,?_⟩
  rw [unboundedTransform_apply]
  exact congrArg D (Subtype.ext hx)

/-- An attained norm ratio transports through the actual full-domain lift. -/
theorem unboundedTransform_attainment (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (γ : ℝ) (hγ : 0 ≤ γ) (u : D.domain) (hu : ‖D u‖=γ*‖(u : H)‖) :
    ∃ x : H, CFC.sqrt (selfadjointSquareResolvent D hs) x=(u : H) ∧
      unboundedTransform D hs x=D u ∧
      ‖unboundedTransform D hs x‖=(γ/Real.sqrt (1+γ^2))*‖x‖ := by
  obtain ⟨x,hx,hbx⟩ := unboundedTransform_lift D hs u
  refine ⟨x,hx,hbx,?_⟩
  have he := unboundedTransform_energy D hs x
  rw [hx,hbx,hu] at he
  have hsq : (Real.sqrt (1+γ^2))^2=1+γ^2 := Real.sq_sqrt (by positivity)
  have hp : 0<Real.sqrt (1+γ^2) := Real.sqrt_pos.mpr (by positivity)
  have heq := congrArg (fun t : ℝ => t*‖(u : H)‖^2) hsq
  have hn : ‖x‖=Real.sqrt (1+γ^2)*‖(u : H)‖ := by
    apply (sq_eq_sq₀ (norm_nonneg _) (by positivity)).mp
    nlinarith
  rw [hbx,hu,hn]
  field_simp

#print axioms unboundedTransform_energy
#print axioms unboundedTransform_lift
#print axioms unboundedTransform_attainment
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
