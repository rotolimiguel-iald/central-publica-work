import Lean
import TGLExt.O16.NullScreenFrame_v2

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Matrix Complex
open TGLExt TGLExt.ContratoQGv31
namespace ChatgptAudit.WignerRapidityMeasure016

def complexWedgeBoost (s : ℝ) (v : Fin 4 → ℂ) : Fin 4 → ℂ :=
  (boostMat s).map (fun x : ℝ => (x : ℂ)) *ᵥ v

/-- Two conjugate circular screen vectors, without assuming an induced representation. -/
def circularScreen (h : ℝ) (y : MomentumCoordinates) : Fin 4 → ℂ :=
  fun i => (screenOne y i : ℂ) + (h : ℂ) * I * (screenTwo y i : ℂ)

theorem complex_boost_of_real (s : ℝ) (v : Fin 4 → ℝ) :
    complexWedgeBoost s (fun i => (v i : ℂ)) = fun i => (wedgeBoostMap s v i : ℂ) := by
  ext i
  simp [complexWedgeBoost,wedgeBoostMap,Matrix.mulVec,dotProduct]

theorem complex_boost_circular (s h : ℝ) (y : MomentumCoordinates) :
    complexWedgeBoost s (circularScreen h y) = circularScreen h (coordinateShift s y) := by
  ext i
  have h1 := congrFun (complex_boost_of_real s (screenOne y)) i
  have h2 := congrFun (complex_boost_of_real s (screenTwo y)) i
  rw [screenOne_boost] at h1
  rw [screenTwo_boost] at h2
  simp only [complexWedgeBoost,Matrix.mulVec,dotProduct,Matrix.map_apply] at *
  simp only [circularScreen,mul_add,Finset.sum_add_distrib]
  rw [h1]
  have he : (∑ j, (boostMat s i j : ℂ) * ((h : ℂ) * I * (screenTwo y j : ℂ))) =
      (h : ℂ) * I * ∑ j, (boostMat s i j : ℂ) * (screenTwo y j : ℂ) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [he,h2]

theorem circularScreen_conjugate (h : ℝ) (y : MomentumCoordinates) :
    (fun i => star (circularScreen h y i)) = circularScreen (-h) y := by
  ext i
  simp [circularScreen]

/-- The two circular vectors are distinct on the regular chart. -/
theorem circularScreen_plus_ne_minus (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    circularScreen 1 y ≠ circularScreen (-1) y := by
  intro he
  have hzero : screenTwo y = 0 := by
    ext i
    have hz := congrArg Complex.im (congrFun he i)
    simp [circularScreen] at hz
    change screenTwo y i = 0
    linarith
  have hn := screenTwo_unit y hy
  rw [hzero] at hn
  norm_num [ChatgptAudit.WignerOrbit016.orbitPairing] at hn

#print axioms complex_boost_of_real
#print axioms complex_boost_circular
#print axioms circularScreen_conjugate
#print axioms circularScreen_plus_ne_minus
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
