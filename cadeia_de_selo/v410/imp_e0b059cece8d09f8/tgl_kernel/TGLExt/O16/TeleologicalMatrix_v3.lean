import Lean
import TGLExt.O16.NullRayResponse_v2
import TGLExt.O16.ScreenMetricAlgebra_v3
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

set_option autoImplicit false
noncomputable section
open MeasureTheory Matrix Set Filter
open scoped Topology
namespace ChatgptAudit.TeleologicalMatrix016
open ChatgptAudit.ScreenMetric016 ChatgptAudit.NullRay016

abbrev Spacetime := Fin 4 → ℝ
abbrev StressSource := Spacetime → Matrix (Fin 4) (Fin 4) ℝ
def n : Spacetime := ![1,1,0,0]
def sourceDensity (f : StressSource) (x : Spacetime) : ℝ :=
  dotProduct n ((f x).mulVec n)
def response (G : ℝ) (f : StressSource) (x : Spacetime) : Matrix (Fin 4) (Fin 4) ℝ :=
  screenMetric (area n (8*Real.pi*G) (sourceDensity f) x)
def responseArea (G : ℝ) (f : StressSource) (x : Spacetime) : ℝ :=
  -((response G f x) 2 2+(response G f x) 3 3)/2

theorem sourceDensity_zero : sourceDensity 0=0 := by
  funext x
  simp only [sourceDensity,Pi.zero_apply,Matrix.zero_mulVec,dotProduct_zero]

theorem response_zero (G : ℝ) : response G 0=0 := by
  funext x
  rw [response,sourceDensity_zero]
  exact (congrArg screenMetric (congrFun (area_zero n (8*Real.pi*G)) x)).trans screenMetric_zero

theorem sourceDensity_translation (f : StressSource) (b : Spacetime) :
    sourceDensity (fun x => f (x-b))=fun x => sourceDensity f (x-b) := rfl

theorem response_translation (G : ℝ) (f : StressSource) (b : Spacetime) :
    response G (fun x => f (x-b))=fun x => response G f (x-b) := by
  funext x
  simp only [response,sourceDensity_translation,area_covariant]

theorem response_fields (G : ℝ) (f : StressSource) (x : Spacetime) :
    (response G f x)ᵀ=response G f x ∧
    (response G f x).mulVec n=0 ∧
    responseArea G f x=area n (8*Real.pi*G) (sourceDensity f) x :=
  ⟨screenMetric_symmetric _,screenMetric_gauge _,screenMetric_area _⟩

theorem response_ray_equations (G : ℝ) (f : StressSource) (x : Spacetime)
    (hc : Continuous (fun u : ℝ => sourceDensity f (x+u • n)))
    (hi : ∀ l, IntegrableOn (fun u : ℝ => sourceDensity f (x+u • n)) (Ioi l))
    (hm : ∀ l, IntegrableOn (fun u : ℝ => u*sourceDensity f (x+u • n)) (Ioi l)) :
    HasDerivAt (fun u : ℝ => responseArea G f (x+u • n))
      (expansion n (8*Real.pi*G) (sourceDensity f) x) 0 ∧
    HasDerivAt (fun u : ℝ => expansion n (8*Real.pi*G) (sourceDensity f) (x+u • n))
      (-(8*Real.pi*G)*sourceDensity f x) 0 := by
  have heq : responseArea G f=area n (8*Real.pi*G) (sourceDensity f) := by
    funext y; exact (response_fields G f y).2.2
  rw [heq]
  simpa only [zero_smul,add_zero] using
    local_ray_equations n (8*Real.pi*G) (sourceDensity f) x hc hi hm 0

#print axioms sourceDensity_zero
#print axioms response_zero
#print axioms sourceDensity_translation
#print axioms response_translation
#print axioms response_fields
#print axioms response_ray_equations
end ChatgptAudit.TeleologicalMatrix016


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
