import Lean
import TGLExt.O16.InscriptionBridge_Integration_v2
import TGLExt.TheContourOfTruth
set_option autoImplicit false
open scoped InnerProductSpace
noncomputable section
namespace ORDEM016.EquationOfTruth
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E] [FiniteDimensional 𝕜 E]

/-- Operator face, compatible with but not identical to the integer-valued contour. -/
theorem equation_of_truth_is_not_static (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜) (hne : H ≠ 0) :
    ∃ s : ℝ, 0 < s ∧ (∃ x, T H s x ≠ x) ∧ ∀ y, reading H (T H s y) = reading H y := by
  classical
  have hx : ∃ x, H x ≠ 0 := by
    by_contra hn
    push_neg at hn
    apply hne
    ext x
    exact hn x
  obtain ⟨x,hx⟩ := hx
  obtain ⟨s,hs,hchange⟩ := positive_time_changes_nonfixed_content H hH hpos x
    (fun hk => hx (LinearMap.mem_ker.mp hk))
  exact ⟨s,hs,⟨x,hchange⟩,reading_T H hH s⟩

theorem zero_operator_reading_real (x : ℝ) : reading (0 : ℝ →L[ℝ] ℝ) x = x := by
  apply Submodule.starProjection_eq_self_iff.mpr
  simp

theorem unit_operator_flow_real (s x : ℝ) :
    T (1 : ℝ →L[ℝ] ℝ) s x = Real.exp (-s) * x := by
  simpa using T_apply_eigen (1 : ℝ →L[ℝ] ℝ) 1 x (by simp) s

theorem equation_criterion_can_fail (s x : ℝ) (hs : 0 < s) (hx : x ≠ 0) :
    reading (0 : ℝ →L[ℝ] ℝ) (T (1 : ℝ →L[ℝ] ℝ) s x) ≠ reading (0 : ℝ →L[ℝ] ℝ) x := by
  rw [zero_operator_reading_real,zero_operator_reading_real,unit_operator_flow_real]
  intro he
  have he1 : Real.exp (-s) = 1 := mul_right_cancel₀ hx (by simpa using he)
  have : -s = 0 := Real.exp_injective (by simpa using he1)
  linarith

#print axioms equation_of_truth_is_not_static
#print axioms zero_operator_reading_real
#print axioms unit_operator_flow_real
#print axioms equation_criterion_can_fail
#print axioms TGLExt.truth_is_not_static_equality
#print axioms TGLExt.the_criterion_can_fail
end ORDEM016.EquationOfTruth


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
