import Lean
import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.MeasureTheory.Function.JacobianOneDim
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Set
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016

/-- Longitudinal momentum at fixed positive transverse mass. -/
def longitudinal (r x : ℝ) : ℝ := r * Real.sinh x
def energy (r p : ℝ) : ℝ := Real.sqrt (r^2+p^2)

theorem longitudinal_hasDerivAt (r x : ℝ) :
    HasDerivAt (longitudinal r) (r * Real.cosh x) x := by
  exact (Real.hasDerivAt_sinh x).const_mul r

theorem longitudinal_bijective (r : ℝ) (hr : 0<r) :
    Function.Bijective (longitudinal r) := by
  constructor
  · intro x y h
    apply Real.sinh_injective
    exact mul_left_cancel₀ hr.ne' h
  · intro p
    refine ⟨Real.arsinh (p/r), ?_⟩
    simp only [longitudinal, Real.sinh_arsinh]
    field_simp

theorem energy_longitudinal (r : ℝ) (hr : 0<r) (x : ℝ) :
    energy r (longitudinal r x) = r*Real.cosh x := by
  have he : r^2+(r*Real.sinh x)^2=(r*Real.cosh x)^2 := by
    have h := congrArg (fun z : ℝ => r^2*z) (Real.cosh_sq_sub_sinh_sq x)
    nlinarith [h]
  unfold energy longitudinal
  rw [he, Real.sqrt_sq (le_of_lt (mul_pos hr (Real.cosh_pos x)))]

theorem jacobian_weight_cancels (r : ℝ) (hr : 0<r) (x : ℝ) :
    ENNReal.ofReal (|r*Real.cosh x|) *
      ENNReal.ofReal (1 / energy r (longitudinal r x)) = 1 := by
  have hp := mul_pos hr (Real.cosh_pos x)
  rw [energy_longitudinal r hr x, abs_of_pos hp, ← ENNReal.ofReal_mul hp.le]
  have hc : (r*Real.cosh x) * (1/(r*Real.cosh x)) = 1 := by field_simp
  rw [hc, ENNReal.ofReal_one]

/-- Exact change of measure dp/sqrt(r²+p²)=dx, not just a formal Jacobian. -/
theorem longitudinal_lintegral (r : ℝ) (hr : 0<r) (g : ℝ → ℝ≥0∞) :
    (∫⁻ p, ENNReal.ofReal (1 / energy r p) * g p) =
      ∫⁻ x, g (longitudinal r x) := by
  have hb := longitudinal_bijective r hr
  have hchange := lintegral_image_eq_lintegral_abs_deriv_mul
    (s := (Set.univ : Set ℝ)) MeasurableSet.univ
    (fun x _ => (longitudinal_hasDerivAt r x).hasDerivWithinAt)
    hb.1.injOn (fun p => ENNReal.ofReal (1 / energy r p) * g p)
  have hrange : longitudinal r '' (Set.univ : Set ℝ) = Set.univ :=
    Set.image_univ.trans (Set.range_eq_univ.mpr hb.2)
  rw [hrange] at hchange
  simp only [Measure.restrict_univ] at hchange
  rw [hchange]
  apply lintegral_congr_ae
  filter_upwards [] with x
  rw [← mul_assoc, jacobian_weight_cancels r hr x, one_mul]

#print axioms longitudinal_hasDerivAt
#print axioms longitudinal_bijective
#print axioms energy_longitudinal
#print axioms jacobian_weight_cancels
#print axioms longitudinal_lintegral
end ChatgptAudit.WignerRapidityMeasure016


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
