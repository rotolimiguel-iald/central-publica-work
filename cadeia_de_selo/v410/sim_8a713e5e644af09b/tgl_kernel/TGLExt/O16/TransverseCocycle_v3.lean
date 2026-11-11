import Lean
import TGLExt.O16.NullFrameDecomposition_v2

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Matrix
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31
namespace ChatgptAudit.WignerRapidityMeasure016

def screen (y : MomentumCoordinates) (i : Fin 2) : Fin 4 → ℝ :=
  ![screenOne y, screenTwo y] i

theorem screen_transverse (y : MomentumCoordinates) (hy : y.1 ≠ 0) (i : Fin 2) :
    orbitPairing (screen y i) (shellMomentum 0 (rapidityChart 0 y)) = 0 := by
  rw [orbitPairing_symm]
  fin_cases i
  · exact screenOne_transverse y hy
  · exact screenTwo_transverse y hy

theorem pairing_sub_right (a b c : Fin 4 → ℝ) :
    orbitPairing a (b-c) = orbitPairing a b - orbitPairing a c := by
  simp [orbitPairing]
  ring

theorem pairing_smul_right (a b : Fin 4 → ℝ) (r : ℝ) :
    orbitPairing a (r • b) = r * orbitPairing a b := by
  simp [orbitPairing]
  ring

def screenCoefficient (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) (i j : Fin 2) : ℝ :=
  -orbitPairing (screen y i) (g (screen x j))

/-- The null remainder disappears in the next screen reading.  The actual
    momentum transport and metric preservation are explicit, not inferred
    from a name or from an abstract fiber isometry. -/
theorem screenCoefficient_comp
    (g h : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y z : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0) (hz : z.1 ≠ 0)
    (hp : h (shellMomentum 0 (rapidityChart 0 x)) = shellMomentum 0 (rapidityChart 0 y))
    (gp : g (shellMomentum 0 (rapidityChart 0 y)) = shellMomentum 0 (rapidityChart 0 z))
    (hm : ∀ a b, orbitPairing (h a) (h b) = orbitPairing a b) (i j : Fin 2) :
    screenCoefficient (g.comp h) x z i j =
      screenCoefficient g y z i 0 * screenCoefficient h x y 0 j +
      screenCoefficient g y z i 1 * screenCoefficient h x y 1 j := by
  have ht : orbitPairing (h (screen x j)) (shellMomentum 0 (rapidityChart 0 y)) = 0 := by
    rw [← hp, hm]
    exact screen_transverse x hx j
  have hd := transverse_decomposition y hy (h (screen x j)) ht
  have he := congrArg (fun v => -orbitPairing (screen z i) (g v)) hd
  simp only [map_sub, map_smul, pairing_sub_right, pairing_smul_right, gp,
    screen_transverse z hz i, mul_zero, zero_sub] at he
  unfold screenCoefficient
  simp only [LinearMap.comp_apply]
  rw [he]
  simp only [screen, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_fin_one]
  simp only [orbitPairing]
  ring

#print axioms screen_transverse
#print axioms pairing_sub_right
#print axioms pairing_smul_right
#print axioms screenCoefficient_comp
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
