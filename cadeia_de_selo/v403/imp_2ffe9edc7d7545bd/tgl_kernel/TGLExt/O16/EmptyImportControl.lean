import Lean
import TGLExt.O16.ConstructedImportH3_v2

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.EmptyImport016
open TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
variable {N : KillingNormalization}

theorem nullDir_ne_zero : nullDir ≠ 0 := by
  intro h0
  have h := congrFun h0 0
  simp [nullDir] at h

/-- Both original negative examples have precisely this failure of fidelity. -/
theorem nonfaithful_null_excludes_h2 (hu : W.U nullDir = 1) :
    ¬ Nonempty (ContratoH2 W R N) := by
  rintro ⟨h⟩
  exact nullDir_ne_zero (h.translations_faithful nullDir hu)

theorem nonfaithful_null_excludes_indexed_import (T : StressTensorData W)
    (hu : W.U nullDir = 1) :
    ¬ Nonempty (Σ h : ContratoH2 W R N, ContratoImportH3 W R N T h) :=
  ConstructedImport016.no_import_over_empty_h2 T (nonfaithful_null_excludes_h2 hu)

/-- A function with an impossible argument is still definable, not an inhabitant. -/
def empty_domain_function (T : StressTensorData W) (hu : W.U nullDir = 1)
    (h2 : ContratoH2 W R N) : ContratoImportH3 W R N T h2 where
  produce := fun h => absurd (h.translations_faithful nullDir hu) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir hu) nullDir_ne_zero

#print axioms nullDir_ne_zero
#print axioms nonfaithful_null_excludes_h2
#print axioms nonfaithful_null_excludes_indexed_import
#print axioms empty_domain_function
end ChatgptAudit.EmptyImport016


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
