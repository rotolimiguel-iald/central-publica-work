import Lean
import TGLExt.ContratoQG_v31_Teoremas

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization
namespace ORDEM016.D3prime

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- Reuse the actual spectral theorem of the contract. The contract is a premise,
not a constructed photon witness in this file. -/
theorem contract_fixed_vector_is_vacuum (C : ContratoH2 W R N) (v : W.H)
    (h : ∀ t : ℝ,C.Δit t v=v) : v ∈ (ℂ ∙ W.vac) := by
  apply C.no_point_spectrum v 0
  intro t
  simp [ChatgptAudit.modularPhase,h t]

theorem contract_fixed_vector_has_trivial_translations (C : ContratoH2 W R N) (v : W.H)
    (h : ∀ t : ℝ,C.Δit t v=v) (a : Fin 4 → ℝ) : W.U a v=v := by
  obtain ⟨c,hc⟩ := Submodule.mem_span_singleton.mp (contract_fixed_vector_is_vacuum C v h)
  rw [←hc,map_smul,W.vac_invariant]

/-- A fixed operator applied to the vacuum supplies the fixed vector required
above. This is the exact additional link needed by the stationary-form reading. -/
theorem contract_fixed_operator_readout (C : ContratoH2 W R N) (A : W.H →L[ℂ] W.H)
    (h : ∀ t : ℝ,(C.Δit t).conjStarAlgEquiv A=A) : A W.vac ∈ (ℂ ∙ W.vac) := by
  apply contract_fixed_vector_is_vacuum C (A W.vac)
  intro t
  have he := congrArg (fun B : W.H →L[ℂ] W.H => B W.vac) (h t)
  have hv : (C.Δit t).symm W.vac=W.vac := by
    apply (C.Δit t).injective
    rw [LinearIsometryEquiv.apply_symm_apply]
    rw [C.bw,C.boost.V_vac]
  simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,hv] using he

#print axioms contract_fixed_vector_is_vacuum
#print axioms contract_fixed_vector_has_trivial_translations
#print axioms contract_fixed_operator_readout
end ORDEM016.D3prime


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
