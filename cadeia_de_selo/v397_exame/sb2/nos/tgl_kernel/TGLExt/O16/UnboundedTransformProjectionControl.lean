import Lean
import TGLExt.O16.UnboundedTransformEnergy

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Strict on each nonzero vector; no uniform operator-norm gap below one is asserted. -/
theorem unboundedTransform_strict_contraction (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (x : H) (hx : x ≠ 0) : ‖unboundedTransform D hs x‖ < ‖x‖ := by
  have hi := positive_sqrt_injective (selfadjointSquareResolvent D hs)
    (selfadjoint_square_resolvent_nonneg D hs) (selfadjoint_square_resolvent_injective D hs)
  have ha : CFC.sqrt (selfadjointSquareResolvent D hs) x ≠ 0 := by
    intro hz
    apply hx
    apply hi
    simpa only [map_zero] using hz
  have hp := norm_pos_iff.mpr ha
  have he := unboundedTransform_energy D hs x
  nlinarith [norm_nonneg (unboundedTransform D hs x),norm_nonneg x]

theorem unboundedTransform_idempotent_only_zero (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (hi : unboundedTransform D hs * unboundedTransform D hs=unboundedTransform D hs) :
    unboundedTransform D hs=0 := by
  apply ContinuousLinearMap.ext
  intro x
  change unboundedTransform D hs x=0
  by_contra hx
  have hlt := unboundedTransform_strict_contraction D hs (unboundedTransform D hs x) hx
  have he := congrArg (fun T : H →L[ℂ] H => T x) hi
  change unboundedTransform D hs (unboundedTransform D hs x)=unboundedTransform D hs x at he
  rw [he] at hlt
  exact (lt_irrefl _ hlt)

/-- Equal kernels do not identify the transform with a nonzero projection. -/
theorem unboundedTransform_ne_nonzero_idempotent (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)
    (P : H →L[ℂ] H) (hp : P*P=P) (hne : P ≠ 0) : unboundedTransform D hs ≠ P := by
  intro he
  have hi : unboundedTransform D hs*unboundedTransform D hs=unboundedTransform D hs := by
    rw [he,hp]
  have hz := unboundedTransform_idempotent_only_zero D hs hi
  exact hne (he.symm.trans hz)

#print axioms unboundedTransform_strict_contraction
#print axioms unboundedTransform_idempotent_only_zero
#print axioms unboundedTransform_ne_nonzero_idempotent
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
