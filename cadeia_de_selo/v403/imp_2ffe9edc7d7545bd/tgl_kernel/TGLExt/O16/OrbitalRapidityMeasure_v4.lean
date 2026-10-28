import Lean
import TGLExt.O16.RapidityJacobian_v2
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Set Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016

abbrev Transverse := Fin 2 → ℝ
abbrev MomentumCoordinates := Transverse × ℝ

def transverseMass (m : ℝ) (q : Transverse) : ℝ :=
  Real.sqrt (m^2 + q 0^2 + q 1^2)

def momentumMeasure : Measure MomentumCoordinates :=
  (volume : Measure Transverse).prod (volume : Measure ℝ)

def orbitalWeight (m : ℝ) (y : MomentumCoordinates) : ℝ≥0∞ :=
  ENNReal.ofReal (1 / energy (transverseMass m y.1) y.2)

def orbitalMeasure (m : ℝ) : Measure MomentumCoordinates :=
  momentumMeasure.withDensity (orbitalWeight m)

def rapidityChart (m : ℝ) (y : MomentumCoordinates) : MomentumCoordinates :=
  (y.1, longitudinal (transverseMass m y.1) y.2)

theorem transverseMass_sq (m : ℝ) (q : Transverse) :
    transverseMass m q ^ 2 = m^2+q 0^2+q 1^2 := by
  exact Real.sq_sqrt (by positivity)

theorem transverseMass_pos_of_mass (m : ℝ) (hm : 0<m) (q : Transverse) :
    0<transverseMass m q := by
  apply Real.sqrt_pos.mpr
  nlinarith [sq_pos_of_pos hm, sq_nonneg (q 0), sq_nonneg (q 1)]

theorem transverseMass_pos_of_ne_zero (m : ℝ) (q : Transverse) (hq : q≠0) :
    0<transverseMass m q := by
  apply Real.sqrt_pos.mpr
  have hc : q 0 ≠ 0 ∨ q 1 ≠ 0 := by
    by_contra hh
    push_neg at hh
    apply hq
    ext i
    fin_cases i <;> simp [hh.1, hh.2]
  rcases hc with h0 | h1
  · nlinarith [sq_pos_of_ne_zero h0, sq_nonneg m, sq_nonneg (q 1)]
  · nlinarith [sq_pos_of_ne_zero h1, sq_nonneg m, sq_nonneg (q 0)]

theorem transverseMass_pos_ae (m : ℝ) :
    ∀ᵐ q ∂(volume : Measure Transverse), 0<transverseMass m q := by
  have h : ∀ᵐ q ∂(volume : Measure Transverse), q≠0 := by
    simp only [ae_iff, not_not, Set.setOf_eq_eq_singleton, measure_singleton]
  filter_upwards [h] with q hq
  exact transverseMass_pos_of_ne_zero m q hq

theorem orbital_iterated_lintegral (m : ℝ) (g : MomentumCoordinates → ℝ≥0∞) :
    (∫⁻ q : Transverse, ∫⁻ p : ℝ, orbitalWeight m (q,p) * g (q,p)) =
      ∫⁻ q : Transverse, ∫⁻ x : ℝ, g (rapidityChart m (q,x)) := by
  apply lintegral_congr_ae
  filter_upwards [transverseMass_pos_ae m] with q hq
  exact longitudinal_lintegral (transverseMass m q) hq (fun p => g (q,p))

theorem exceptional_axis_null :
    momentumMeasure (({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ))=0 := by
  simp [momentumMeasure, Measure.prod_prod]

theorem exceptional_axis_orbital_null (m : ℝ) :
    orbitalMeasure m (({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ))=0 := by
  exact withDensity_absolutelyContinuous momentumMeasure (orbitalWeight m) exceptional_axis_null

theorem orbitalWeight_measurable (m : ℝ) : Measurable (orbitalWeight m) := by
  unfold orbitalWeight energy transverseMass
  fun_prop

theorem rapidityChart_continuous (m : ℝ) : Continuous (rapidityChart m) := by
  unfold rapidityChart longitudinal transverseMass
  fun_prop

/-- The actual weighted three-dimensional integral equals its rapidity pullback. -/
theorem orbital_lintegral (m : ℝ) (g : MomentumCoordinates → ℝ≥0∞)
    (hg : Measurable g) :
    (∫⁻ p, g p ∂orbitalMeasure m) =
      ∫⁻ x, g (rapidityChart m x) ∂momentumMeasure := by
  rw [orbitalMeasure, lintegral_withDensity_eq_lintegral_mul
    momentumMeasure (orbitalWeight_measurable m) hg]
  simp only [Pi.mul_apply]
  have hwg := (orbitalWeight_measurable m).mul hg
  have hgc : Measurable (fun x => g (rapidityChart m x)) :=
    hg.comp (rapidityChart_continuous m).measurable
  rw [momentumMeasure, lintegral_prod _ hwg.aemeasurable,
    lintegral_prod _ hgc.aemeasurable]
  exact orbital_iterated_lintegral m g

#print axioms transverseMass_sq
#print axioms transverseMass_pos_of_mass
#print axioms transverseMass_pos_of_ne_zero
#print axioms transverseMass_pos_ae
#print axioms orbital_iterated_lintegral
#print axioms exceptional_axis_null
#print axioms exceptional_axis_orbital_null
#print axioms orbitalWeight_measurable
#print axioms rapidityChart_continuous
#print axioms orbital_lintegral
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
