import Lean
import TGLExt.O16.OrbitalL2Equivalence_v2
import Mathlib.MeasureTheory.Group.Measure
import Mathlib.MeasureTheory.Measure.Haar.Unique

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016

theorem coordinateShift_measurePreserving (s : ℝ) :
    MeasurePreserving (coordinateShift s) momentumMeasure momentumMeasure := by
  exact (MeasurePreserving.id (volume : Measure Transverse)).prod
    (measurePreserving_add_right (volume : Measure ℝ) s)

theorem coordinateBoost_measurable (m s : ℝ) : Measurable (coordinateBoost m s) := by
  unfold coordinateBoost energy transverseMass
  fun_prop

theorem coordinateBoost_measurePreserving (m s : ℝ) :
    MeasurePreserving (coordinateBoost m s) (orbitalMeasure m) (orbitalMeasure m) := by
  refine ⟨coordinateBoost_measurable m s, ?_⟩
  calc
    Measure.map (coordinateBoost m s) (orbitalMeasure m) =
        Measure.map (coordinateBoost m s ∘ rapidityChart m) momentumMeasure := by
          rw [← Measure.map_map (coordinateBoost_measurable m s)
            (rapidityChart_continuous m).measurable, (rapidityChart_measurePreserving m).map_eq]
    _ = Measure.map (rapidityChart m ∘ coordinateShift s) momentumMeasure :=
      Measure.map_congr (boost_chart_intertwines_ae m s)
    _ = Measure.map (rapidityChart m) (Measure.map (coordinateShift s) momentumMeasure) :=
      (Measure.map_map (rapidityChart_continuous m).measurable
        (coordinateShift_measurePreserving s).measurable).symm
    _ = orbitalMeasure m := by
      rw [(coordinateShift_measurePreserving s).map_eq, (rapidityChart_measurePreserving m).map_eq]

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

def productRapidityShift (s : ℝ) :
    Lp E 2 momentumMeasure →ₗᵢ[ℂ] Lp E 2 momentumMeasure :=
  Lp.compMeasurePreservingₗᵢ ℂ (coordinateShift (-s)) (coordinateShift_measurePreserving (-s))

def orbitalScalarBoost (m s : ℝ) :
    Lp E 2 (orbitalMeasure m) →ₗᵢ[ℂ] Lp E 2 (orbitalMeasure m) :=
  Lp.compMeasurePreservingₗᵢ ℂ (coordinateBoost m (-s)) (coordinateBoost_measurePreserving m (-s))

theorem productRapidityShift_ae (s : ℝ) (f : Lp E 2 momentumMeasure) :
    productRapidityShift s f =ᵐ[momentumMeasure] fun y => f (coordinateShift (-s) y) :=
  Lp.coeFn_compMeasurePreserving f (coordinateShift_measurePreserving (-s))

theorem orbitalScalarBoost_ae (m s : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalScalarBoost m s f =ᵐ[orbitalMeasure m] fun y => f (coordinateBoost m (-s) y) :=
  Lp.coeFn_compMeasurePreserving f (coordinateBoost_measurePreserving m (-s))

/-- Actual equality of L2 operators, derived from the coordinate boost and measure. -/
theorem orbitalScalarBoost_intertwines (m s : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalL2Pullback m (orbitalScalarBoost m s f) =
      productRapidityShift s (orbitalL2Pullback m f) := by
  have h1 := orbitalL2Pullback_ae m (orbitalScalarBoost m s f)
  have h2 := (rapidityChart_measurePreserving m).quasiMeasurePreserving.ae
    (orbitalScalarBoost_ae m s f)
  have h3 := productRapidityShift_ae s (orbitalL2Pullback m f)
  have h4 := (coordinateShift_measurePreserving (-s)).quasiMeasurePreserving.ae
    (orbitalL2Pullback_ae m f)
  apply Lp.ext
  filter_upwards [h1, h2, h3, h4, boost_chart_intertwines_ae m (-s)] with y e1 e2 e3 e4 ec
  exact (e1.trans e2).trans ((congrArg f ec).trans (e3.trans e4).symm)

theorem productRapidityShift_add (s t : ℝ) (f : Lp E 2 momentumMeasure) :
    productRapidityShift (s+t) f = productRapidityShift s (productRapidityShift t f) := by
  have h1 := productRapidityShift_ae (s+t) f
  have h2 := productRapidityShift_ae s (productRapidityShift t f)
  have h3 := (coordinateShift_measurePreserving (-s)).quasiMeasurePreserving.ae
    (productRapidityShift_ae t f)
  apply Lp.ext
  filter_upwards [h1,h2,h3] with y e1 e2 e3
  rw [e1,e2,e3]
  congr 1
  apply Prod.ext
  · rfl
  · simp only [coordinateShift]
    ring

theorem orbitalScalarBoost_add (m s t : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalScalarBoost m (s+t) f = orbitalScalarBoost m s (orbitalScalarBoost m t f) := by
  apply (orbitalL2Pullback m).injective
  rw [orbitalScalarBoost_intertwines, orbitalScalarBoost_intertwines,
    orbitalScalarBoost_intertwines, productRapidityShift_add]

#print axioms coordinateShift_measurePreserving
#print axioms coordinateBoost_measurable
#print axioms coordinateBoost_measurePreserving
#print axioms productRapidityShift_ae
#print axioms orbitalScalarBoost_ae
#print axioms orbitalScalarBoost_intertwines
#print axioms productRapidityShift_add
#print axioms orbitalScalarBoost_add
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
