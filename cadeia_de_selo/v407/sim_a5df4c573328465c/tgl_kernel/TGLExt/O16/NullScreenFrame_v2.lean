import Lean
import TGLExt.O16.OrbitalBoostCovariance_v2

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Matrix
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31
namespace ChatgptAudit.WignerRapidityMeasure016

/-- A concrete transverse frame; no global helicity representation is assumed. -/
def screenOne (y : MomentumCoordinates) : Fin 4 → ℝ :=
  ![Real.sinh y.2, Real.cosh y.2, 0, 0]

def screenTwo (y : MomentumCoordinates) : Fin 4 → ℝ :=
  ![0, 0, -y.1 1 / transverseMass 0 y.1, y.1 0 / transverseMass 0 y.1]

theorem screenOne_unit (y : MomentumCoordinates) :
    orbitPairing (screenOne y) (screenOne y) = -1 := by
  simp [orbitPairing, screenOne]
  nlinarith [Real.cosh_sq_sub_sinh_sq y.2]

theorem screenTwo_unit (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    orbitPairing (screenTwo y) (screenTwo y) = -1 := by
  have hr := (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  have hsq := transverseMass_sq 0 y.1
  simp only [zero_pow (by decide : 2 ≠ 0), zero_add] at hsq
  simp [orbitPairing, screenTwo]
  field_simp
  nlinarith [hsq]

theorem screens_orthogonal (y : MomentumCoordinates) :
    orbitPairing (screenOne y) (screenTwo y) = 0 := by
  simp [orbitPairing, screenOne, screenTwo]

theorem screenOne_transverse (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    orbitPairing (shellMomentum 0 (rapidityChart 0 y)) (screenOne y) = 0 := by
  rw [shellMomentum_chart 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)]
  simp [orbitPairing, screenOne]
  ring

theorem screenTwo_transverse (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    orbitPairing (shellMomentum 0 (rapidityChart 0 y)) (screenTwo y) = 0 := by
  rw [shellMomentum_chart 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)]
  simp [orbitPairing, screenTwo]
  ring

/-- Uses the very wedgeBoostMap of the contract, not a homonymous matrix. -/
theorem screenOne_boost (s : ℝ) (y : MomentumCoordinates) :
    wedgeBoostMap s (screenOne y) = screenOne (coordinateShift s y) := by
  ext i
  fin_cases i <;>
    simp [screenOne,coordinateShift,wedgeBoostMap,boostMat,Matrix.mulVec,
      dotProduct,Fin.sum_univ_four,Real.cosh_add,Real.sinh_add] <;> ring

theorem screenTwo_boost (s : ℝ) (y : MomentumCoordinates) :
    wedgeBoostMap s (screenTwo y) = screenTwo (coordinateShift s y) := by
  ext i
  fin_cases i <;>
    simp [screenTwo,coordinateShift,wedgeBoostMap,boostMat,Matrix.mulVec,
      dotProduct,Fin.sum_univ_four]

theorem screenOne_measurable : Measurable screenOne := by
  unfold screenOne
  fun_prop

theorem screenTwo_measurable : Measurable screenTwo := by
  unfold screenTwo transverseMass
  fun_prop

/-- The chosen real basis has identity boost coefficients off the null axis. -/
theorem boost_screen_coefficients (s : ℝ) (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    -orbitPairing (screenOne (coordinateShift s y)) (wedgeBoostMap s (screenOne y)) = 1 ∧
    -orbitPairing (screenTwo (coordinateShift s y)) (wedgeBoostMap s (screenTwo y)) = 1 ∧
    -orbitPairing (screenOne (coordinateShift s y)) (wedgeBoostMap s (screenTwo y)) = 0 := by
  rw [screenOne_boost,screenTwo_boost,screenOne_unit,
    screenTwo_unit (coordinateShift s y) hy,screens_orthogonal]
  norm_num

#print axioms screenOne_unit
#print axioms screenTwo_unit
#print axioms screens_orthogonal
#print axioms screenOne_transverse
#print axioms screenTwo_transverse
#print axioms screenOne_boost
#print axioms screenTwo_boost
#print axioms screenOne_measurable
#print axioms screenTwo_measurable
#print axioms boost_screen_coefficients
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
