import Lean
import TGLExt.O16.OrbitalRapidityMeasure_v4
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Integral.Lebesgue.Map
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Set Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016

theorem rapidityChart_measurePreserving (m : ℝ) :
    MeasurePreserving (rapidityChart m) momentumMeasure (orbitalMeasure m) := by
  refine ⟨(rapidityChart_continuous m).measurable, ?_⟩
  apply Measure.ext_of_lintegral
  intro g hg
  rw [lintegral_map hg (rapidityChart_continuous m).measurable]
  exact (orbital_lintegral m g hg).symm

def inverseRapidityChart (m : ℝ) (y : MomentumCoordinates) : MomentumCoordinates :=
  (y.1, Real.arsinh (y.2 / transverseMass m y.1))

theorem inverseRapidityChart_measurable (m : ℝ) : Measurable (inverseRapidityChart m) := by
  have ha : Measurable Real.arsinh := Real.continuous_arsinh.measurable
  unfold inverseRapidityChart transverseMass
  exact measurable_fst.prodMk (ha.comp (by fun_prop))

theorem inverse_chart_of_positive (m : ℝ) (y : MomentumCoordinates)
    (h : 0 < transverseMass m y.1) :
    inverseRapidityChart m (rapidityChart m y) = y := by
  apply Prod.ext
  · rfl
  · simp only [inverseRapidityChart, rapidityChart, longitudinal]
    rw [mul_div_cancel_left₀ _ h.ne', Real.arsinh_sinh]

theorem chart_inverse_of_positive (m : ℝ) (y : MomentumCoordinates)
    (h : 0 < transverseMass m y.1) :
    rapidityChart m (inverseRapidityChart m y) = y := by
  apply Prod.ext
  · rfl
  · simp only [inverseRapidityChart, rapidityChart, longitudinal, Real.sinh_arsinh]
    field_simp

theorem inverse_chart_ae (m : ℝ) :
    (fun y => inverseRapidityChart m (rapidityChart m y)) =ᵐ[momentumMeasure] id := by
  have h : ∀ᵐ y ∂momentumMeasure, y.1 ≠ 0 := by
    rw [ae_iff]
    simp only [not_not]
    have hs : (({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ)) =
        {y : MomentumCoordinates | y.1 = 0} := by ext y; simp
    rw [← hs]
    exact exceptional_axis_null
  filter_upwards [h] with y hy
  exact inverse_chart_of_positive m y (transverseMass_pos_of_ne_zero m y.1 hy)

theorem chart_inverse_ae (m : ℝ) :
    (fun y => rapidityChart m (inverseRapidityChart m y)) =ᵐ[orbitalMeasure m] id := by
  have h : ∀ᵐ y ∂orbitalMeasure m, y.1 ≠ 0 := by
    rw [ae_iff]
    simp only [not_not]
    have hs : (({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ)) =
        {y : MomentumCoordinates | y.1 = 0} := by ext y; simp
    rw [← hs]
    exact exceptional_axis_orbital_null m
  filter_upwards [h] with y hy
  exact chart_inverse_of_positive m y (transverseMass_pos_of_ne_zero m y.1 hy)

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

/-- Pullback is a genuine linear isometry of L2 equivalence classes. -/
def orbitalL2Pullback (m : ℝ) :
    Lp E 2 (orbitalMeasure m) →ₗᵢ[ℂ] Lp E 2 momentumMeasure :=
  Lp.compMeasurePreservingₗᵢ ℂ (rapidityChart m) (rapidityChart_measurePreserving m)

theorem orbitalL2Pullback_ae (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalL2Pullback m f =ᵐ[momentumMeasure] fun y => f (rapidityChart m y) :=
  Lp.coeFn_compMeasurePreserving f (rapidityChart_measurePreserving m)

theorem orbitalL2Pullback_norm (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    ‖orbitalL2Pullback m f‖ = ‖f‖ := (orbitalL2Pullback m).norm_map f

def coordinateBoost (m s : ℝ) (y : MomentumCoordinates) : MomentumCoordinates :=
  (y.1, Real.cosh s * y.2 + Real.sinh s * energy (transverseMass m y.1) y.2)

def coordinateShift (s : ℝ) (y : MomentumCoordinates) : MomentumCoordinates :=
  (y.1, y.2+s)

theorem boost_chart_intertwines_of_positive (m s : ℝ) (y : MomentumCoordinates)
    (h : 0 < transverseMass m y.1) :
    coordinateBoost m s (rapidityChart m y) = rapidityChart m (coordinateShift s y) := by
  apply Prod.ext
  · rfl
  · change Real.cosh s * longitudinal (transverseMass m y.1) y.2 +
        Real.sinh s * energy (transverseMass m y.1) (longitudinal (transverseMass m y.1) y.2) =
        longitudinal (transverseMass m y.1) (y.2+s)
    rw [energy_longitudinal _ h]
    simp only [longitudinal, Real.sinh_add]
    ring

theorem boost_chart_intertwines_ae (m s : ℝ) :
    (fun y => coordinateBoost m s (rapidityChart m y)) =ᵐ[momentumMeasure]
      (fun y => rapidityChart m (coordinateShift s y)) := by
  have h : ∀ᵐ y ∂momentumMeasure, y.1 ≠ 0 := by
    rw [ae_iff]
    simp only [not_not]
    have hs : (({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ)) =
        {y : MomentumCoordinates | y.1 = 0} := by ext y; simp
    rw [← hs]
    exact exceptional_axis_null
  filter_upwards [h] with y hy
  exact boost_chart_intertwines_of_positive m s y (transverseMass_pos_of_ne_zero m y.1 hy)

#print axioms rapidityChart_measurePreserving
#print axioms inverseRapidityChart_measurable
#print axioms inverse_chart_of_positive
#print axioms chart_inverse_of_positive
#print axioms inverse_chart_ae
#print axioms chart_inverse_ae
#print axioms orbitalL2Pullback_ae
#print axioms orbitalL2Pullback_norm
#print axioms boost_chart_intertwines_of_positive
#print axioms boost_chart_intertwines_ae
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
