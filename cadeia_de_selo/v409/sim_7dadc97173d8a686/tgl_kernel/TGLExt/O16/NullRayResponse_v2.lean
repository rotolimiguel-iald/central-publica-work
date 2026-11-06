import Lean
import TGLExt.O16.TeleologicalShift_v3
import TGLExt.O16.TeleologicalBoundary_v2

set_option autoImplicit false
noncomputable section
open MeasureTheory Set Filter
open scoped Topology
namespace ChatgptAudit.NullRay016
open ChatgptAudit.Teleological016
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

def area (n : V) (c : ℝ) (f : V → ℝ) (x : V) : ℝ :=
  -c*(∫ u : ℝ in Ioi 0, u*f (x+u • n))
def expansion (n : V) (c : ℝ) (f : V → ℝ) (x : V) : ℝ :=
  c*(∫ u : ℝ in Ioi 0, f (x+u • n))

theorem area_along (n : V) (c : ℝ) (f : V → ℝ) (x : V) (l : ℝ) :
    area n c f (x+l • n) = -c*weightedTail (fun u => f (x+u • n)) l := by
  unfold area
  simp_rw [add_assoc,← add_smul]
  rw [weighted_tail_shift (fun v => f (x+v • n)) l]

theorem expansion_along (n : V) (c : ℝ) (f : V → ℝ) (x : V) (l : ℝ) :
    expansion n c f (x+l • n) = c*tail (fun u => f (x+u • n)) l := by
  unfold expansion
  simp_rw [add_assoc,← add_smul]
  rw [tail_shift (fun v => f (x+v • n)) l]

theorem area_zero (n : V) (c : ℝ) : area n c (fun _ => 0)=0 := by
  funext x
  simp only [area,mul_zero,integral_zero,Pi.zero_apply]

theorem area_covariant (n : V) (c : ℝ) (f : V → ℝ) (b : V) :
    area n c (fun x => f (x-b))=fun x => area n c f (x-b) := by
  funext x
  have h : ∀ u : ℝ, x+u • n-b=(x-b)+u • n := by intro u; abel
  simp only [area,h]

theorem local_ray_equations (n : V) (c : ℝ) (f : V → ℝ) (x : V)
    (hf : Continuous (fun u : ℝ => f (x+u • n)))
    (hi : ∀ l, IntegrableOn (fun u : ℝ => f (x+u • n)) (Ioi l))
    (hm : ∀ l, IntegrableOn (fun u : ℝ => u*f (x+u • n)) (Ioi l)) (l : ℝ) :
    HasDerivAt (fun u : ℝ => area n c f (x+u • n))
      (expansion n c f (x+l • n)) l ∧
    HasDerivAt (fun u : ℝ => expansion n c f (x+u • n))
      (-c*f (x+l • n)) l := by
  simpa only [area_along,expansion_along] using
    teleological_equations (fun u => f (x+u • n)) hf hi hm c l

theorem ray_boundary_zero (n : V) (c : ℝ) (f : V → ℝ) (x : V)
    (hi : ∀ l, IntegrableOn (fun u : ℝ => f (x+u • n)) (Ioi l))
    (hm : ∀ l, IntegrableOn (fun u : ℝ => u*f (x+u • n)) (Ioi l)) :
    Tendsto (fun l : ℝ => area n c f (x+l • n)) atTop (𝓝 0) ∧
    Tendsto (fun l : ℝ => expansion n c f (x+l • n)) atTop (𝓝 0) := by
  constructor
  · simpa only [area_along,mul_zero] using
      (weighted_tail_tendsto_zero (fun u => f (x+u • n)) hi hm).const_mul (-c)
  · simpa only [expansion_along,mul_zero] using
      (tail_tendsto_zero (fun u => f (x+u • n))).const_mul c

#print axioms area_along
#print axioms expansion_along
#print axioms area_zero
#print axioms area_covariant
#print axioms local_ray_equations
#print axioms ray_boundary_zero
end ChatgptAudit.NullRay016


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
