import TGLExt.F1Fecho394.RegularCovariantCoreR3
import TGLExt.V350ScalarDualWeightFaithfulness
/-! Dual cuts and their canonical resolvent stay in the supplied represented
regular core. The full dual integral and generic variational limit are reused;
no trace or modular-state hypothesis enters this construction. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularCoreResolvent
open Filter TGLExt TGLV350 TGLV350.Regular F1Fecho.RegularCovariantCore
open scoped Topology ENNReal
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B : UnitaryFlow H) (M : VonNeumannAlgebra H)

theorem dualWeightCut_mem (R : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : A ∈ core B M) : dualWeightCut R A ∈ core B M := by
  apply StrongIntegral.operatorIntegral_mem
  intro s
  exact (dualAction B M s ⟨A,hA⟩).property

theorem normalizedDualCut_mem (R : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : A ∈ core B M) : normalizedDualCut R A ∈ core B M := by
  change ((dualHaarFactor : ℂ) • dualWeightCut R A) ∈ core B M
  exact (core B M).toStarSubalgebra.smul_mem (dualWeightCut_mem B M R A hA) _

theorem exists_dualResolvent_limit
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hmem : A ∈ core B M) (hA : 0 ≤ A) :
    ∃ R : RegularHilbert H →L[ℂ] RegularHilbert H,
      R ∈ core B M ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      IsGLB (Set.range (fun n => dualCutResolvent n A)) R := by
  apply vonNeumann_antitone_contraction_limit (core B M) (fun n => dualCutResolvent n A)
  · intro n
    exact positiveResolvent_mem _ _ (normalizedDualCut_mem B M _ A hmem)
      (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)
  · intro n
    exact positiveResolvent_nonneg _ (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)
  · intro n
    exact positiveResolvent_le_one _ (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)
  · exact dualCutResolvent_antitone A hA

theorem exists_dualResolvent_fixed
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hmem : A ∈ core B M) (hA : 0 ≤ A) :
    ∃ R : RegularHilbert H →L[ℂ] RegularHilbert H,
      R ∈ core B M ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      (∀ s : ℝ, dualAmbient s R = R) := by
  obtain ⟨R,hmR,hR,hone,hlim,_⟩ := exists_dualResolvent_limit B M A hmem hA
  exact ⟨R,hmR,hR,hone,hlim,dualResolvent_limit_dual_fixed A R hA hlim⟩

end F1Fecho.RegularCoreResolvent
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.RegularCoreResolvent).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
