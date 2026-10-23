import Lean
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ORDEM016.EquationOfTruth.InfiniteLimitControl
open Filter Topology Set
noncomputable section

def spectralLimit (u : ℝ) : ℝ := if u=0 then 1 else 0

/-- Pointwise scalar convergence is valid, including the zero mode. -/
theorem scalar_pointwise_limit (u : ℝ) (hu : 0 ≤ u) :
    Tendsto (fun s : ℝ => Real.exp (-(s*u))) atTop (𝓝 (spectralLimit u)) := by
  by_cases hz : u=0
  · subst u
    simpa [spectralLimit] using (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1:ℝ)) atTop (𝓝 1))
  · have hp : 0 < u := lt_of_le_of_ne hu (Ne.symm hz)
    rw [spectralLimit, if_neg hz]
    exact Real.tendsto_exp_neg_atTop_nhds_zero.comp (tendsto_id.atTop_mul_const hp)

/-- At every nonnegative time a positive spectral value retains error above exp(-1). -/
theorem uniform_error_lower_bound (s : ℝ) (hs : 0 ≤ s) :
    ∃ u ∈ Ioc (0:ℝ) 1, Real.exp (-1) < |Real.exp (-(s*u))-spectralLimit u| := by
  let u : ℝ := 1/(s+1)
  have hd : 0 < s+1 := by linarith
  have hu : 0 < u := one_div_pos.mpr hd
  have hu1 : u ≤ 1 := by
    apply (div_le_iff₀ hd).mpr
    linarith
  have hsu : s*u < 1 := by
    dsimp [u]
    rw [← mul_div_assoc, mul_one]
    apply (div_lt_iff₀ hd).mpr
    linarith
  refine ⟨u, ⟨hu, hu1⟩, ?_⟩
  rw [spectralLimit, if_neg (ne_of_gt hu), sub_zero, abs_of_pos (Real.exp_pos _)]
  exact Real.exp_lt_exp.mpr (by linarith)

/-- Thus even a fixed positive uniform tolerance cannot be achieved on [0,1]. -/
theorem no_uniform_small_error :
    ¬ ∃ s : ℝ, 0 ≤ s ∧ ∀ u ∈ Icc (0:ℝ) 1,
      |Real.exp (-(s*u))-spectralLimit u| < Real.exp (-1) := by
  rintro ⟨s, hs, hbound⟩
  obtain ⟨u, hu, herr⟩ := uniform_error_lower_bound s hs
  have hb := hbound u ⟨hu.1.le, hu.2⟩
  linarith

#print axioms scalar_pointwise_limit
#print axioms uniform_error_lower_bound
#print axioms no_uniform_small_error
end
end ORDEM016.EquationOfTruth.InfiniteLimitControl


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
