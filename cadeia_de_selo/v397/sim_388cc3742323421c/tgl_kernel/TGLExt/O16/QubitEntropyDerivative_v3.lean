import Lean
import TGLExt.O16.QubitScalarEntropy
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.Deriv.Add

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ORDEM016.EquationOfTruth.QubitScalar
open Real
noncomputable section

theorem hasDerivAt_radius (p k s : ℝ) (hr : 0 < radius p k s) :
    HasDerivAt (radius p k) (-4*k*Real.exp (-2*s)/radius p k s) s := by
  have hz : (2*p-1)^2+4*k*Real.exp (-2*s) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mp hr)
  have hd : HasDerivAt (fun t : ℝ => (2*p-1)^2+4*k*Real.exp (-2*t))
      (-8*k*Real.exp (-2*s)) s := by
    have hraw := (((hasDerivAt_id s).const_mul (-2)).exp.const_mul (4*k)).const_add ((2*p-1)^2)
    apply hraw.congr_deriv
    simp only [id_eq]
    ring
  apply (hd.sqrt hz).congr_deriv
  change -8*k*Real.exp (-2*s)/(2*radius p k s) = -4*k*Real.exp (-2*s)/radius p k s
  field_simp [ne_of_gt hr]
  <;> ring

theorem entropy_log_ratio (r : ℝ) (hr0 : 0 ≤ r) (hr1 : r < 1) :
    Real.log (1-(1+r)/2) - Real.log ((1+r)/2) =
      -Real.log ((1+r)/(1-r)) := by
  have hp : 1+r ≠ 0 := by linarith
  have hm : 1-r ≠ 0 := by linarith
  rw [show 1-(1+r)/2 = (1-r)/2 by ring]
  rw [Real.log_div hm (by norm_num), Real.log_div hp (by norm_num), Real.log_div hp hm]
  ring

theorem hasDerivAt_entropy (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) (hr : 0 < radius p k s) :
    HasDerivAt (entropy p k)
      (2*k*Real.exp (-2*s)/radius p k s *
        Real.log ((1+radius p k s)/(1-radius p k s))) s := by
  have hr1 := radius_lt_one p k s hk hkp hs
  have h0 : (1+radius p k s)/2 ≠ 0 := by linarith
  have h1 : (1+radius p k s)/2 ≠ 1 := by linarith
  have hd := ((hasDerivAt_radius p k s hr).const_add 1).div_const 2
  have he := (Real.hasDerivAt_binEntropy h0 h1).comp s hd
  apply he.congr_deriv
  rw [entropy_log_ratio (radius p k s) hr.le hr1]
  ring

theorem deriv_entropy (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) (hr : 0 < radius p k s) :
    deriv (entropy p k) s = 2*k*Real.exp (-2*s)/radius p k s *
      Real.log ((1+radius p k s)/(1-radius p k s)) :=
  (hasDerivAt_entropy p k s hk hkp hs hr).deriv

#print axioms hasDerivAt_radius
#print axioms entropy_log_ratio
#print axioms hasDerivAt_entropy
#print axioms deriv_entropy
end
end ORDEM016.EquationOfTruth.QubitScalar


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
