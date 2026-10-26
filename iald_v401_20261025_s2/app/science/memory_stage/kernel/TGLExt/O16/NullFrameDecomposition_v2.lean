import Lean
import TGLExt.O16.NullScreenFrame_v2

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Matrix
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31
namespace ChatgptAudit.WignerRapidityMeasure016

def nullCompanion (y : MomentumCoordinates) : Fin 4 → ℝ :=
  ![Real.cosh y.2 / (2 * transverseMass 0 y.1),
    Real.sinh y.2 / (2 * transverseMass 0 y.1),
    -y.1 0 / (2 * transverseMass 0 y.1 ^ 2),
    -y.1 1 / (2 * transverseMass 0 y.1 ^ 2)]

theorem orbitPairing_symm (v w : Fin 4 → ℝ) :
    orbitPairing v w = orbitPairing w v := by
  simp only [orbitPairing]
  ring

theorem null_frame_decomposition (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (v : Fin 4 → ℝ) :
    v = orbitPairing v (nullCompanion y) • shellMomentum 0 (rapidityChart 0 y) +
      orbitPairing v (shellMomentum 0 (rapidityChart 0 y)) • nullCompanion y -
      orbitPairing v (screenOne y) • screenOne y -
      orbitPairing v (screenTwo y) • screenTwo y := by
  have hr := (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  have hsq := transverseMass_sq 0 y.1
  simp only [zero_pow (by decide : 2 ≠ 0), zero_add] at hsq
  have htr := Real.cosh_sq_sub_sinh_sq y.2
  rw [shellMomentum_chart 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)]
  ext i
  fin_cases i <;>
    simp [orbitPairing, nullCompanion, screenOne, screenTwo] <;>
    field_simp <;> first | linear_combination -2 * v 0 * transverseMass 0 y.1 * htr | linear_combination -2 * v 1 * transverseMass 0 y.1 * htr | linear_combination 2 * v 2 * hsq | linear_combination 2 * v 3 * hsq

theorem transverse_decomposition (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (v : Fin 4 → ℝ)
    (hv : orbitPairing v (shellMomentum 0 (rapidityChart 0 y)) = 0) :
    v = orbitPairing v (nullCompanion y) • shellMomentum 0 (rapidityChart 0 y) -
      orbitPairing v (screenOne y) • screenOne y -
      orbitPairing v (screenTwo y) • screenTwo y := by
  simpa [hv] using null_frame_decomposition y hy v

#print axioms orbitPairing_symm
#print axioms null_frame_decomposition
#print axioms transverse_decomposition
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
