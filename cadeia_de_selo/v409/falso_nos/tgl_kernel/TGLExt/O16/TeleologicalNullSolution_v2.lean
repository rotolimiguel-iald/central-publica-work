import Lean
import TGLExt.O16.TeleologicalContractBridge_v3
set_option autoImplicit false
noncomputable section
open MeasureTheory Matrix Set
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
namespace TGLExt.ContratoQGv31.ProbeResidual
abbrev Source := (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
structure NullSolution (W : TGLSpecificAQFTWitness) (T : StressTensorData W) (G : ℝ) (A : Set W.H) where
  a : Source → (Fin 4 → ℝ) → ℝ
  θ : W.H → (Fin 4 → ℝ) → ℝ
  a_zero : ∀ x, a 0 x = 0
  a_cov : ∀ (b : Fin 4 → ℝ) (f : Source) (x : Fin 4 → ℝ), a (fun y => f (y - b)) x = a f (x - b)
  a_deriv : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ, HasDerivAt (fun l : ℝ => a (T.T ψ) (x + l • nullDir)) (θ ψ x) 0
  θ_deriv : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ,
    HasDerivAt (fun l : ℝ => θ ψ (x + l • nullDir)) (-(8 * Real.pi * G) * nullEnergy T ψ x) 0

end TGLExt.ContratoQGv31.ProbeResidual
namespace ChatgptAudit.TeleologicalConstruct016
open TGLExt.ContratoQGv31.ProbeResidual
open ChatgptAudit.TeleologicalMatrix016 ChatgptAudit.NullRay016

def construct_null_solution {W : TGLSpecificAQFTWitness}
    (T : StressTensorData W) (G : ℝ) (A : Set W.H)
    (hc : ∀ ψ ∈ A, ∀ x, Continuous (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)))
    (hi : ∀ ψ ∈ A, ∀ x l, IntegrableOn (fun u : ℝ => nullEnergy T ψ (x+u • nullDir)) (Ioi l))
    (hm : ∀ ψ ∈ A, ∀ x l, IntegrableOn (fun u : ℝ => u*nullEnergy T ψ (x+u • nullDir)) (Ioi l)) :
    NullSolution W T G A where
  a := fun f => area n (8*Real.pi*G) (sourceDensity f)
  θ := fun ψ => expansion n (8*Real.pi*G) (sourceDensity (T.T ψ))
  a_zero := by
    intro x
    rw [sourceDensity_zero]
    exact congrFun (area_zero n (8*Real.pi*G)) x
  a_cov := by
    intro b f x
    rw [sourceDensity_translation]
    exact congrFun (area_covariant n (8*Real.pi*G) (sourceDensity f) b) x
  a_deriv := by
    intro ψ hψ x
    have h := local_ray_equations n (8*Real.pi*G) (sourceDensity (T.T ψ)) x
      (hc ψ hψ x) (hi ψ hψ x) (hm ψ hψ x) 0
    simpa only [n,nullDir,sourceDensity,nullEnergy,pairing,zero_smul,add_zero] using h.1
  θ_deriv := by
    intro ψ hψ x
    have h := local_ray_equations n (8*Real.pi*G) (sourceDensity (T.T ψ)) x
      (hc ψ hψ x) (hi ψ hψ x) (hm ψ hψ x) 0
    simpa only [n,nullDir,sourceDensity,nullEnergy,pairing,zero_smul,add_zero] using h.2

#print axioms construct_null_solution
end ChatgptAudit.TeleologicalConstruct016


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
