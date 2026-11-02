import Lean
import TGLExt.O16.NullSolutionConsumerReuse
import TGLExt.O16.ModularChargeLink

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.ConstructedImport016
open TGLExt.ContratoQGv31 TGLExt.ContratoQGv31.ProbeResidual
open TGL.SpecificAQFT TGL.ModularRealization MeasureTheory Set Matrix
open ChatgptAudit.TeleologicalConstruct016 ChatgptAudit.ModularCharge016

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- Conditional construction in the original indexed contract.
The obligations involving a candidate H2 are quantified over EVERY such H2,
as required by produce. No physical H2, stress tensor, or G is manufactured. -/
def construct_import (T : StressTensorData W) (G : ℝ) (hG : 0 < G)
    (A : Set W.H) (h2 : ContratoH2 W R N)
    (hAu : ∀ ψ ∈ A, ‖ψ‖ = 1) (hAv : W.vac ∈ A)
    (hAt : ∀ (b : Fin 4 → ℝ) (ψ : W.H), ψ ∈ A → W.U b ψ ∈ A)
    (hmc : ∀ h : ContratoH2 W R N, ModularChargeLink h T A)
    (hAn : ∀ h : ContratoH2 W R N,
      ∃ ψ ∈ A, ∃ k : ℝ, HasModularEnergy h.Δit ψ k ∧ k ≠ 0)
    (hc : ∀ ψ ∈ A, ∀ x, Continuous (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)))
    (hi : ∀ ψ ∈ A, ∀ x l, IntegrableOn (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)) (Ioi l))
    (hm : ∀ ψ ∈ A, ∀ x l, IntegrableOn (fun u : ℝ => u*nullEnergy T ψ (x+u • nullDir)) (Ioi l))
    (hflat : ∀ h : ContratoH2 W R N,
      ∀ x ∈ rightWedge, screenBlockV31 (TGLExt.solderMetric4 (h.E x)⁻¹) = -1) :
    ContratoImportH3 W R N T h2 where
  produce := fun h => H3_of_null_solution h T G hG A hAu hAv hAt
    (hmc h) (hAn h) hc (hflat h) (construct_null_solution T G A hc hi hm)
  same_horizon := fun _ => rfl

/-- The indexed family cannot be inhabited by a function with empty domain alone. -/
theorem no_import_over_empty_h2 (T : StressTensorData W)
    (he : ¬ Nonempty (ContratoH2 W R N)) :
    ¬ Nonempty (Σ h : ContratoH2 W R N, ContratoImportH3 W R N T h) := by
  rintro ⟨⟨h,_⟩⟩
  exact he ⟨h⟩

#print axioms construct_import
#print axioms no_import_over_empty_h2
end ChatgptAudit.ConstructedImport016


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
