import Lean
import TGLExt.O16.ProductOrbitalSpectrum_v3
import Mathlib.MeasureTheory.Function.LpSpace.ContinuousCompMeasurePreserving

set_option autoImplicit false
noncomputable section
open MeasureTheory
namespace ChatgptAudit.WignerRapidityMeasure016

def productShiftMap (s : ℝ) : C(MomentumCoordinates, MomentumCoordinates) :=
  ⟨coordinateShift (-s), by unfold coordinateShift; fun_prop⟩

theorem productShiftMap_continuous : Continuous productShiftMap := by
  apply ContinuousMap.continuous_of_continuous_uncurry
  change Continuous (fun p : ℝ × MomentumCoordinates => (p.2.1, p.2.2 + -p.1))
  fun_prop

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

theorem productRapidityShift_strongly_continuous (f : Lp E 2 momentumMeasure) :
    Continuous (fun s : ℝ => productRapidityShift s f) := by
  letI : momentumMeasure.InnerRegularCompactLTTop := by unfold momentumMeasure; infer_instance
  letI : IsLocallyFiniteMeasure momentumMeasure := by unfold momentumMeasure; infer_instance
  exact (continuous_const : Continuous (fun _ : ℝ => f)).compMeasurePreservingLp
    productShiftMap_continuous (fun s => coordinateShift_measurePreserving (-s)) (by norm_num)

theorem orbitalScalarBoost_strongly_continuous (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    Continuous (fun s : ℝ => orbitalScalarBoost m s f) := by
  have h := (orbitalL2Inverse m).continuous.comp
    (productRapidityShift_strongly_continuous (orbitalL2Pullback m f))
  apply h.congr
  intro s
  dsimp only [Function.comp_apply]
  rw [← orbitalScalarBoost_intertwines, orbitalL2Inverse_pullback]

/-- One-particle states invariant under every wedge boost vanish. A Fock vacuum
therefore cannot be silently supplied as a normalized one-particle vector. -/
theorem orbitalScalarBoost_invariant_zero (m : ℝ) (f : Lp E 2 (orbitalMeasure m))
    (h : ∀ s, orbitalScalarBoost m s f = f) : f = 0 := by
  apply orbitalScalarBoost_no_eigen m f
  intro s
  exact ⟨1, norm_one, by simpa using h s⟩

theorem orbitalScalarBoost_no_normalized_vacuum (m : ℝ) :
    ¬ ∃ f : Lp E 2 (orbitalMeasure m), ‖f‖ = 1 ∧ ∀ s, orbitalScalarBoost m s f = f := by
  rintro ⟨f, hn, hi⟩
  have hf := orbitalScalarBoost_invariant_zero m f hi
  simpa [hf] using hn

#print axioms productShiftMap_continuous
#print axioms productRapidityShift_strongly_continuous
#print axioms orbitalScalarBoost_strongly_continuous
#print axioms orbitalScalarBoost_invariant_zero
#print axioms orbitalScalarBoost_no_normalized_vacuum
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
