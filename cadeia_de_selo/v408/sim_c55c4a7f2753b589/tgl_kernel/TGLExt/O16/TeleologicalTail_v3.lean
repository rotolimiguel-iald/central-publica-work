import Lean
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory Set
namespace ChatgptAudit.Teleological016

def tail (f : ℝ → ℝ) (x : ℝ) : ℝ := ∫ u in Ioi x, f u
def weightedTail (f : ℝ → ℝ) (x : ℝ) : ℝ := ∫ u in Ioi x, (u-x)*f u

theorem tail_hasDerivAt (f : ℝ → ℝ) (hf : Continuous f)
    (hint : ∀ x, IntegrableOn f (Ioi x)) (x : ℝ) :
    HasDerivAt (tail f) (-f x) x := by
  have hd := intervalIntegral.integral_hasDerivAt_right (hf.intervalIntegrable x x)
    hf.aestronglyMeasurable.stronglyMeasurableAtFilter hf.continuousAt
  have heq : tail f = fun y => tail f x - ∫ u in x..y, f u := by
    funext y
    have h := intervalIntegral.integral_Ioi_sub_Ioi' (hint x) (hint y)
    change tail f x - tail f y = _ at h
    linarith
  rw [heq]
  simpa using hd.const_sub (tail f x)

theorem weightedTail_split (f : ℝ → ℝ)
    (hint : ∀ x, IntegrableOn f (Ioi x))
    (hmoment : ∀ x, IntegrableOn (fun u => u*f u) (Ioi x)) (x : ℝ) :
    weightedTail f x = tail (fun u => u*f u) x - x*tail f x := by
  unfold weightedTail tail
  simp_rw [sub_mul]
  rw [integral_sub (hmoment x) ((hint x).const_mul x), integral_const_mul]

theorem weightedTail_hasDerivAt (f : ℝ → ℝ) (hf : Continuous f)
    (hint : ∀ x, IntegrableOn f (Ioi x))
    (hmoment : ∀ x, IntegrableOn (fun u => u*f u) (Ioi x)) (x : ℝ) :
    HasDerivAt (weightedTail f) (-tail f x) x := by
  have hd1 := tail_hasDerivAt (fun u => u*f u) (continuous_id.mul hf) hmoment x
  have hd2 := (hasDerivAt_id x).mul (tail_hasDerivAt f hf hint x)
  have hd := hd1.sub hd2
  have heq : weightedTail f = fun y => tail (fun u => u*f u) y-y*tail f y := by
    funext y; exact weightedTail_split f hint hmoment y
  rw [heq]
  exact hd.congr_deriv (by simp only [id]; ring)

theorem teleological_equations (f : ℝ → ℝ) (hf : Continuous f)
    (hint : ∀ x, IntegrableOn f (Ioi x))
    (hmoment : ∀ x, IntegrableOn (fun u => u*f u) (Ioi x)) (c x : ℝ) :
    HasDerivAt (fun y => -c*weightedTail f y) (c*tail f x) x ∧
    HasDerivAt (fun y => c*tail f y) (-c*f x) x := by
  constructor
  · exact ((weightedTail_hasDerivAt f hf hint hmoment x).const_mul (-c)).congr_deriv (by ring)
  · exact ((tail_hasDerivAt f hf hint x).const_mul c).congr_deriv (by ring)

#print axioms tail_hasDerivAt
#print axioms weightedTail_split
#print axioms weightedTail_hasDerivAt
#print axioms teleological_equations
end ChatgptAudit.Teleological016


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
