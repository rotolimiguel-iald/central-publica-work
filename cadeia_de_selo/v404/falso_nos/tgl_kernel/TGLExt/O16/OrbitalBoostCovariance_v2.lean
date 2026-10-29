import Lean
import TGLExt.O16.OrbitalTranslationOperators_v2
import TGLExt.O16.OrbitalBoostTransport
import TGLExt.O16.ContratoQG_v31_Minimal

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31 Matrix

theorem shellMomentum_chart (m : ℝ) (y : MomentumCoordinates)
    (h : 0 < transverseMass m y.1) :
    shellMomentum m (rapidityChart m y) =
      ![transverseMass m y.1 * Real.cosh y.2,
        transverseMass m y.1 * Real.sinh y.2, y.1 0, y.1 1] := by
  change ![energy (transverseMass m y.1) (longitudinal (transverseMass m y.1) y.2),
    longitudinal (transverseMass m y.1) y.2, y.1 0, y.1 1] = _
  rw [energy_longitudinal _ h]
  rfl

/-- Exact identification with the existing kernel matrix, not a homonymous boost. -/
theorem shellMomentum_chart_shift (m s : ℝ) (y : MomentumCoordinates)
    (h : 0 < transverseMass m y.1) :
    shellMomentum m (rapidityChart m (coordinateShift s y)) =
      wedgeBoostMap s (shellMomentum m (rapidityChart m y)) := by
  rw [shellMomentum_chart m (coordinateShift s y) h, shellMomentum_chart m y h]
  ext i
  fin_cases i <;>
    simp [coordinateShift, wedgeBoostMap, boostMat, Matrix.mulVec,
      dotProduct, Fin.sum_univ_four, Real.cosh_add, Real.sinh_add] <;> ring

theorem orbitPairing_boost_inverse (s : ℝ) (a p : Fin 4 → ℝ) :
    orbitPairing a (wedgeBoostMap (-s) p) = orbitPairing (wedgeBoostMap s a) p := by
  simp [orbitPairing, wedgeBoostMap, boostMat, Matrix.mulVec,
    dotProduct, Fin.sum_univ_four, Real.cosh_neg, Real.sinh_neg]
  ring

theorem orbitalPhase_boost_ae (m s : ℝ) (a : Fin 4 → ℝ) :
    (fun y => orbitalPhase m a (coordinateBoost m (-s) y)) =ᵐ[orbitalMeasure m]
      orbitalPhase m (wedgeBoostMap s a) := by
  have hchart : (fun y => orbitalPhase m a (coordinateBoost m (-s) (rapidityChart m y)))
      =ᵐ[momentumMeasure] fun y => orbitalPhase m (wedgeBoostMap s a) (rapidityChart m y) := by
    have hq : ∀ᵐ y ∂momentumMeasure, y.1 ≠ (0 : Transverse) := by
      rw [ae_iff]
      have hs : {y : MomentumCoordinates | ¬ y.1 ≠ (0 : Transverse)} =
          ({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ) := by ext y; simp
      rw [hs]
      exact exceptional_axis_null
    filter_upwards [hq] with y hy
    have hr := transverseMass_pos_of_ne_zero m y.1 hy
    rw [boost_chart_intertwines_of_positive m (-s) y hr]
    unfold orbitalPhase
    rw [shellMomentum_chart_shift m (-s) y hr, orbitPairing_boost_inverse]
  have hinv := (inverseRapidityChart_measurePreserving m).quasiMeasurePreserving.ae hchart
  filter_upwards [hinv, chart_inverse_ae m] with y hy hc
  simpa only [hc, id_eq] using hy

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

theorem orbitalScalarBoost_translations (m s : ℝ) (a : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    orbitalScalarBoost m s (orbitalTranslation m a f) =
      orbitalTranslation m (wedgeBoostMap s a) (orbitalScalarBoost m s f) := by
  have htr := (coordinateBoost_measurePreserving m (-s)).quasiMeasurePreserving.ae
    (orbitalTranslation_ae m a f)
  apply Lp.ext
  filter_upwards [orbitalScalarBoost_ae m s (orbitalTranslation m a f), htr,
    orbitalTranslation_ae m (wedgeBoostMap s a) (orbitalScalarBoost m s f),
    orbitalScalarBoost_ae m s f, orbitalPhase_boost_ae m s a] with y h1 h2 h3 h4 h5
  rw [h1, h2, h3, h4, h5]

theorem orbitalScalarBoost_zero (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalScalarBoost m 0 f = f := by
  apply Lp.ext
  filter_upwards [orbitalScalarBoost_ae m 0 f] with y hy
  simpa [coordinateBoost] using hy

theorem orbitalScalarBoost_inverse (m s : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalScalarBoost m s (orbitalScalarBoost m (-s) f) = f := by
  rw [← orbitalScalarBoost_add, add_neg_cancel, orbitalScalarBoost_zero]

theorem orbitalScalarBoost_conjugates_translations (m s : ℝ) (a : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    orbitalScalarBoost m s (orbitalTranslation m a (orbitalScalarBoost m (-s) f)) =
      orbitalTranslation m (wedgeBoostMap s a) f := by
  rw [orbitalScalarBoost_translations, orbitalScalarBoost_inverse]

/-- Null-ray dilation follows from the same boostMat eigen-direction as the contract. -/
theorem orbitalScalarBoost_null_dilation (m s r : ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    orbitalScalarBoost m s (orbitalTranslation m (r • nullDir)
      (orbitalScalarBoost m (-s) f)) =
        orbitalTranslation m ((r * Real.exp s) • nullDir) f := by
  rw [orbitalScalarBoost_conjugates_translations, wedgeBoostMap_smul,
    wedgeBoostMap_nullDir, smul_smul]

#print axioms shellMomentum_chart
#print axioms shellMomentum_chart_shift
#print axioms orbitPairing_boost_inverse
#print axioms orbitalPhase_boost_ae
#print axioms orbitalScalarBoost_translations
#print axioms orbitalScalarBoost_zero
#print axioms orbitalScalarBoost_inverse
#print axioms orbitalScalarBoost_conjugates_translations
#print axioms orbitalScalarBoost_null_dilation
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
