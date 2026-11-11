import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
import TGLExt.O16.TeleologicalMatrix_v3

set_option autoImplicit false
noncomputable section
open MeasureTheory Matrix Set
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
namespace ChatgptAudit.TeleologicalContract016

theorem null_direction_exact : nullDir=ChatgptAudit.TeleologicalMatrix016.n := rfl

theorem source_density_exact {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H) :
    nullEnergy T ψ=ChatgptAudit.TeleologicalMatrix016.sourceDensity (T.T ψ) := rfl

theorem area_density_exact (G : ℝ) (f : ChatgptAudit.TeleologicalMatrix016.StressSource) :
    areaDensity (ChatgptAudit.TeleologicalMatrix016.response G f)=ChatgptAudit.TeleologicalMatrix016.responseArea G f := rfl

theorem propagated_geometry_in_contract (G : ℝ) (f : ChatgptAudit.TeleologicalMatrix016.StressSource) (x : Fin 4 → ℝ) :
    (ChatgptAudit.TeleologicalMatrix016.response G f x)ᵀ=ChatgptAudit.TeleologicalMatrix016.response G f x ∧
    (ChatgptAudit.TeleologicalMatrix016.response G f x).mulVec nullDir=0 ∧
    areaDensity (ChatgptAudit.TeleologicalMatrix016.response G f) x=ChatgptAudit.NullRay016.area nullDir (8*Real.pi*G) (ChatgptAudit.TeleologicalMatrix016.sourceDensity f) x :=
  ChatgptAudit.TeleologicalMatrix016.response_fields G f x

theorem local_equations_in_contract {W : TGLSpecificAQFTWitness} (T : StressTensorData W)
    (ψ : W.H) (G : ℝ) (x : Fin 4 → ℝ)
    (hc : Continuous (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)))
    (hi : ∀ l, IntegrableOn (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)) (Ioi l))
    (hm : ∀ l, IntegrableOn (fun u : ℝ => u*nullEnergy T ψ (x+u • nullDir)) (Ioi l)) :
    HasDerivAt (fun u : ℝ => areaDensity (ChatgptAudit.TeleologicalMatrix016.response G (T.T ψ)) (x+u • nullDir))
      (ChatgptAudit.NullRay016.expansion nullDir (8*Real.pi*G) (nullEnergy T ψ) x) 0 ∧
    HasDerivAt (fun u : ℝ => ChatgptAudit.NullRay016.expansion nullDir (8*Real.pi*G) (nullEnergy T ψ)
      (x+u • nullDir)) (-(8*Real.pi*G)*nullEnergy T ψ x) 0 :=
  ChatgptAudit.TeleologicalMatrix016.response_ray_equations G (T.T ψ) x hc hi hm

#print axioms null_direction_exact
#print axioms source_density_exact
#print axioms area_density_exact
#print axioms propagated_geometry_in_contract
#print axioms local_equations_in_contract
end ChatgptAudit.TeleologicalContract016


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
