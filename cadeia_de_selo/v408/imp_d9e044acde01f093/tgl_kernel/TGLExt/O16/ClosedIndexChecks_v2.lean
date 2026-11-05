import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
set_option autoImplicit false
namespace ChatgptAudit.GateProposal016
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31

/- Conditional consumers, not physical inhabitants. Dedicated exact-type
metaprogram tested separately to reduce memory; check below retains every input. -/
def conditionalH2 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (h : ContratoH2 W R N) : ContratoH2 W R N := h
#check (conditionalH2 : (W : TGLSpecificAQFTWitness) →
    (R : TGLModularRealization W) → (N : KillingNormalization) →
    ContratoH2 W R N → ContratoH2 W R N)

def conditionalImport (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (T : StressTensorData W) (h : ContratoH2 W R N)
    (f : ContratoImportH3 W R N T h) : ContratoH3 W R N T := f.produce h

theorem conditionalImport_sameHorizon
    (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (T : StressTensorData W) (h : ContratoH2 W R N)
    (f : ContratoImportH3 W R N T h) : (conditionalImport W R N T h f).H2 = h :=
  f.same_horizon h
#print axioms conditionalH2
#print axioms conditionalImport
#print axioms conditionalImport_sameHorizon
end ChatgptAudit.GateProposal016


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
