import Lean
import TGLExt.O16.UnboundedTransformConstruction_v2
import TGLExt.O16.NormalizedGraphContract_v2

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem sameSquare_ambientKernel (D E Q : H →ₗ.[ℂ] H)
    (hd : IsSelfAdjoint D) (he : IsSelfAdjoint E)
    (hdq : partialOperatorSquare D=Q) (heq : partialOperatorSquare E=Q) :
    ambientKernel D=ambientKernel E := by
  ext x
  rw [ambientKernel_mem,ambientKernel_mem]
  constructor
  · rintro ⟨u,hu,hDu⟩
    let v := Submodule.inclusion (sameSquare_domain_le D E Q hd he hdq heq) u
    refine ⟨v,hu,?_⟩
    have hn := sameSquare_norm_full D E Q hd he hdq heq u
    rw [hDu,norm_zero] at hn
    exact norm_eq_zero.mp hn.symm
  · rintro ⟨u,hu,hEu⟩
    let v := Submodule.inclusion (sameSquare_domain_le E D Q he hd heq hdq) u
    refine ⟨v,hu,?_⟩
    have hn := sameSquare_norm_full E D Q he hd heq hdq u
    rw [hEu,norm_zero] at hn
    exact norm_eq_zero.mp hn.symm

theorem unboundedTransform_kernel (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    (unboundedTransform D hs).ker=ambientKernel D := by
  have he := sameSquare_ambientKernel (selfadjointAbsoluteRoot D hs) D
    (partialOperatorSquare D) (selfadjoint_absolute_selfadjoint D hs) hs
    (selfadjoint_absolute_square D hs) rfl
  have hc : ambientKernel (selfadjointAbsoluteRoot D hs) =
      (CFC.sqrt (1-selfadjointSquareResolvent D hs)).ker :=
    resolvent_bounded_transform_kernel _ (selfadjoint_square_resolvent_nonneg D hs)
      (selfadjoint_square_resolvent_injective D hs) (selfadjoint_square_resolvent_le_one D hs)
  calc
    _ = (CFC.sqrt (1-selfadjointSquareResolvent D hs)).ker := by
      ext x
      change unboundedTransform D hs x=0 ↔ CFC.sqrt (1-selfadjointSquareResolvent D hs) x=0
      rw [← norm_eq_zero,unboundedTransform_norm,norm_eq_zero]
    _ = ambientKernel (selfadjointAbsoluteRoot D hs) := hc.symm
    _ = ambientKernel D := he

theorem unboundedTransform_gap (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (γ : ℝ) (hγ : 0 ≤ γ)
    (hgap : ∀ u : D.domain, (u : H) ∈ (ambientKernel D)ᗮ → γ*‖(u : H)‖ ≤ ‖D u‖) :
    ∀ x ∈ (unboundedTransform D hs).kerᗮ,
      (γ/Real.sqrt (1+γ^2))*‖x‖ ≤ ‖unboundedTransform D hs x‖ := by
  let E := selfadjointAbsoluteRoot D hs
  have he := sameSquare_ambientKernel E D (partialOperatorSquare D)
    (selfadjoint_absolute_selfadjoint D hs) hs (selfadjoint_absolute_square D hs) rfl
  have hc : ambientKernel E = (CFC.sqrt (1-selfadjointSquareResolvent D hs)).ker :=
    resolvent_bounded_transform_kernel _ (selfadjoint_square_resolvent_nonneg D hs)
      (selfadjoint_square_resolvent_injective D hs) (selfadjoint_square_resolvent_le_one D hs)
  have heg : ∀ u : E.domain, (u : H) ∈ (ambientKernel E)ᗮ → γ*‖(u : H)‖ ≤ ‖E u‖ := by
    intro u hu
    rw [he] at hu
    have hn := sameSquare_norm_full E D (partialOperatorSquare D)
      (selfadjoint_absolute_selfadjoint D hs) hs (selfadjoint_absolute_square D hs) rfl u
    rw [hn]
    exact hgap (Submodule.inclusion (sameSquare_domain_le E D (partialOperatorSquare D)
      (selfadjoint_absolute_selfadjoint D hs) hs (selfadjoint_absolute_square D hs) rfl) u) hu
  have hcg := resolvent_bounded_transform_gap _ (selfadjoint_square_resolvent_nonneg D hs)
    (selfadjoint_square_resolvent_injective D hs) (selfadjoint_square_resolvent_le_one D hs)
    γ hγ heg
  have hker : (unboundedTransform D hs).ker=(CFC.sqrt (1-selfadjointSquareResolvent D hs)).ker :=
    (unboundedTransform_kernel D hs).trans (he.symm.trans hc)
  intro x hx
  rw [unboundedTransform_norm]
  apply hcg x
  rwa [← hker]

/-- Existence is now constructed for every given self-adjoint LinearPMap. -/
theorem unboundedTransform_pays_contract (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    BoundedTransformPreservesKernelAndGap D (unboundedTransform D hs) :=
  ⟨(unboundedTransform_kernel D hs).symm, unboundedTransform_contraction D hs,
    fun γ hγ hg => unboundedTransform_gap D hs γ hγ hg⟩

#print axioms sameSquare_ambientKernel
#print axioms unboundedTransform_kernel
#print axioms unboundedTransform_gap
#print axioms unboundedTransform_pays_contract
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
