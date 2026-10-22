import Lean
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 800000

/- Scalar B3a. No identification with matrix entropy is asserted here. -/
namespace ORDEM016.EquationOfTruth.QubitScalar
open Set Real
noncomputable section

def radius (p k s : ℝ) : ℝ := Real.sqrt ((2*p-1)^2 + 4*k*Real.exp (-2*s))
def entropy (p k s : ℝ) : ℝ := Real.binEntropy ((1+radius p k s)/2)
def deficit (p k s : ℝ) : ℝ := Real.binEntropy p - entropy p k s

theorem radius_nonneg (p k s : ℝ) : 0 ≤ radius p k s := Real.sqrt_nonneg _

theorem radicand_nonneg (p k s : ℝ) (hk : 0 ≤ k) :
    0 ≤ (2*p-1)^2+4*k*Real.exp (-2*s) := by positivity

theorem radius_lt_one (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) : radius p k s < 1 := by
  have he : Real.exp (-2*s) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
  have hm : 4*k*Real.exp (-2*s) ≤ 4*k := by
    simpa using mul_le_mul_of_nonneg_left he (show 0 ≤ 4*k by positivity)
  apply (Real.sqrt_lt (radicand_nonneg p k s hk) (by norm_num : (0:ℝ) ≤ 1)).mpr
  nlinarith

theorem radius_antitone (p k : ℝ) (hk : 0 ≤ k) : Antitone (radius p k) := by
  intro s t hst
  apply Real.sqrt_le_sqrt
  have he : Real.exp (-2*t) ≤ Real.exp (-2*s) := Real.exp_le_exp.mpr (by linarith)
  have hm := mul_le_mul_of_nonneg_left he (show 0 ≤ 4*k by positivity)
  linarith

theorem radius_strictAnti (p k : ℝ) (hk : 0 < k) : StrictAnti (radius p k) := by
  intro s t hst
  apply Real.sqrt_lt_sqrt (radicand_nonneg p k t hk.le)
  have he : Real.exp (-2*t) < Real.exp (-2*s) := Real.exp_lt_exp.mpr (by linarith)
  have hm := mul_lt_mul_of_pos_left he (show 0 < 4*k by positivity)
  linarith

theorem entropy_argument_mem (p k s : ℝ) (hk : 0 ≤ k)
    (hkp : k < p*(1-p)) (hs : 0 ≤ s) :
    (1+radius p k s)/2 ∈ Icc (2:ℝ)⁻¹ 1 := by
  have h0 := radius_nonneg p k s
  have h1 := radius_lt_one p k s hk hkp hs
  constructor <;> norm_num <;> linarith

theorem entropy_monotoneOn (p k : ℝ) (hk : 0 ≤ k) (hkp : k < p*(1-p)) :
    MonotoneOn (entropy p k) (Ici 0) := by
  intro s hs t ht hst
  apply Real.binEntropy_strictAntiOn.antitoneOn
    (entropy_argument_mem p k t hk hkp ht)
    (entropy_argument_mem p k s hk hkp hs)
  have hr := radius_antitone p k hk hst
  linarith

theorem entropy_strictMonoOn (p k : ℝ) (hk : 0 < k) (hkp : k < p*(1-p)) :
    StrictMonoOn (entropy p k) (Ici 0) := by
  intro s hs t ht hst
  apply Real.binEntropy_strictAntiOn
    (entropy_argument_mem p k t hk.le hkp ht)
    (entropy_argument_mem p k s hk.le hkp hs)
  have hr := radius_strictAnti p k hk hst
  linarith

theorem entropy_abs_identity (p : ℝ) :
    Real.binEntropy ((1+|2*p-1|)/2) = Real.binEntropy p := by
  by_cases hp : 0 ≤ 2*p-1
  · rw [abs_of_nonneg hp]
    congr 1
    ring
  · rw [abs_of_neg (lt_of_not_ge hp)]
    have he : (1+ -(2*p-1))/2 = 1-p := by ring
    rw [he, Real.binEntropy_one_sub]

theorem radius_lower_bound (p k s : ℝ) (hk : 0 ≤ k) :
    |2*p-1| ≤ radius p k s := by
  rw [← Real.sqrt_sq_eq_abs]
  apply Real.sqrt_le_sqrt
  have hm : 0 ≤ 4*k*Real.exp (-2*s) := by positivity
  linarith

theorem asymptotic_argument_mem (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    (1+|2*p-1|)/2 ∈ Icc (2:ℝ)⁻¹ 1 := by
  have ha : |2*p-1| ≤ 1 := abs_le.mpr ⟨by linarith, by linarith⟩
  have hz := abs_nonneg (2*p-1)
  constructor <;> norm_num <;> linarith

theorem entropy_le_diagonal (p k s : ℝ) (hp0 : 0 < p) (hp1 : p < 1)
    (hk : 0 ≤ k) (hkp : k < p*(1-p)) (hs : 0 ≤ s) :
    entropy p k s ≤ Real.binEntropy p := by
  rw [← entropy_abs_identity p]
  apply Real.binEntropy_strictAntiOn.antitoneOn
    (asymptotic_argument_mem p hp0 hp1)
    (entropy_argument_mem p k s hk hkp hs)
  have hr := radius_lower_bound p k s hk
  linarith

theorem deficit_nonneg (p k s : ℝ) (hp0 : 0 < p) (hp1 : p < 1)
    (hk : 0 ≤ k) (hkp : k < p*(1-p)) (hs : 0 ≤ s) :
    0 ≤ deficit p k s := sub_nonneg.mpr (entropy_le_diagonal p k s hp0 hp1 hk hkp hs)

theorem deficit_antitoneOn (p k : ℝ) (hk : 0 ≤ k) (hkp : k < p*(1-p)) :
    AntitoneOn (deficit p k) (Ici 0) := by
  intro s hs t ht hst
  have he := entropy_monotoneOn p k hk hkp hs ht hst
  exact sub_le_sub_left he _

#print axioms radius_nonneg
#print axioms radicand_nonneg
#print axioms radius_lt_one
#print axioms radius_antitone
#print axioms radius_strictAnti
#print axioms entropy_argument_mem
#print axioms entropy_monotoneOn
#print axioms entropy_strictMonoOn
#print axioms entropy_abs_identity
#print axioms radius_lower_bound
#print axioms asymptotic_argument_mem
#print axioms entropy_le_diagonal
#print axioms deficit_nonneg
#print axioms deficit_antitoneOn
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
