import Lean
import TGLExt.O16.OrbitalRapidityTransport_v3
import Mathlib.Analysis.Normed.Operator.LinearIsometry

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016

theorem inverseRapidityChart_measurePreserving (m : ℝ) :
    MeasurePreserving (inverseRapidityChart m) (orbitalMeasure m) momentumMeasure := by
  refine ⟨inverseRapidityChart_measurable m, ?_⟩
  calc
    Measure.map (inverseRapidityChart m) (orbitalMeasure m) =
        Measure.map (inverseRapidityChart m) (Measure.map (rapidityChart m) momentumMeasure) := by
          rw [(rapidityChart_measurePreserving m).map_eq]
    _ = Measure.map (inverseRapidityChart m ∘ rapidityChart m) momentumMeasure :=
      Measure.map_map (inverseRapidityChart_measurable m) (rapidityChart_continuous m).measurable
    _ = Measure.map id momentumMeasure := Measure.map_congr (inverse_chart_ae m)
    _ = momentumMeasure := Measure.map_id

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

def orbitalL2Inverse (m : ℝ) :
    Lp E 2 momentumMeasure →ₗᵢ[ℂ] Lp E 2 (orbitalMeasure m) :=
  Lp.compMeasurePreservingₗᵢ ℂ (inverseRapidityChart m) (inverseRapidityChart_measurePreserving m)

theorem orbitalL2Inverse_ae (m : ℝ) (f : Lp E 2 momentumMeasure) :
    orbitalL2Inverse m f =ᵐ[orbitalMeasure m] fun y => f (inverseRapidityChart m y) :=
  Lp.coeFn_compMeasurePreserving f (inverseRapidityChart_measurePreserving m)

theorem orbitalL2Pullback_inverse (m : ℝ) (f : Lp E 2 momentumMeasure) :
    orbitalL2Pullback m (orbitalL2Inverse m f) = f := by
  have h1 := orbitalL2Pullback_ae m (orbitalL2Inverse m f)
  have h2 := (rapidityChart_measurePreserving m).quasiMeasurePreserving.ae
    (orbitalL2Inverse_ae m f)
  apply Lp.ext
  filter_upwards [h1, h2, inverse_chart_ae m] with y hy1 hy2 hy3
  exact hy1.trans (hy2.trans (congrArg f hy3))

theorem orbitalL2Inverse_pullback (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalL2Inverse m (orbitalL2Pullback m f) = f := by
  have h1 := orbitalL2Inverse_ae m (orbitalL2Pullback m f)
  have h2 := (inverseRapidityChart_measurePreserving m).quasiMeasurePreserving.ae
    (orbitalL2Pullback_ae m f)
  apply Lp.ext
  filter_upwards [h1, h2, chart_inverse_ae m] with y hy1 hy2 hy3
  exact hy1.trans (hy2.trans (congrArg f hy3))

/-- A two-sided complex linear isometry for the actual weighted orbit coordinates. -/
def orbitalL2Equivalence (m : ℝ) :
    Lp E 2 (orbitalMeasure m) ≃ₗᵢ[ℂ] Lp E 2 momentumMeasure :=
  LinearIsometryEquiv.ofLinearIsometry (orbitalL2Pullback m) (orbitalL2Inverse m).toLinearMap
    (by apply LinearMap.ext; intro f; exact orbitalL2Pullback_inverse m f)
    (by apply LinearMap.ext; intro f; exact orbitalL2Inverse_pullback m f)

theorem orbitalL2Equivalence_apply (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalL2Equivalence m f = orbitalL2Pullback m f := rfl

theorem orbitalL2Equivalence_symm_apply (m : ℝ) (f : Lp E 2 momentumMeasure) :
    (orbitalL2Equivalence m).symm f = orbitalL2Inverse m f := rfl

#print axioms inverseRapidityChart_measurePreserving
#print axioms orbitalL2Inverse_ae
#print axioms orbitalL2Pullback_inverse
#print axioms orbitalL2Inverse_pullback
#print axioms orbitalL2Equivalence_apply
#print axioms orbitalL2Equivalence_symm_apply
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
