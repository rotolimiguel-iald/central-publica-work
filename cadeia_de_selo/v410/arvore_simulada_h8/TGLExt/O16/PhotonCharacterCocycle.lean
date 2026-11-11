import Lean
import TGLExt.O16.PhotonScreenCharacters_v3

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31
open ChatgptAudit.WignerRapidityMeasure016
namespace ORDEM016.D1prime

def ScreenOrientationMeasured (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) : Prop :=
  screenCoefficient g x y 0 0 * screenCoefficient g x y 1 1 -
    screenCoefficient g x y 0 1 * screenCoefficient g x y 1 0 = 1

theorem oriented_screen_entries (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (gp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (gm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b)
    (ho : ScreenOrientationMeasured g x y) :
    screenCoefficient g x y 1 1=screenCoefficient g x y 0 0 ∧
    screenCoefficient g x y 1 0= -screenCoefficient g x y 0 1 ∧
    screenCoefficient g x y 0 0*screenCoefficient g x y 0 0+
      screenCoefficient g x y 0 1*screenCoefficient g x y 0 1=1 := by
  apply oriented_two_frame
  · simpa using screen_columns_orthonormal g x y hx hy gp gm 0 0
  · simpa using screen_columns_orthonormal g x y hx hy gp gm 1 1
  · exact ho

def screenPhase (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) : ℂ :=
  photonPhase (screenCoefficient g x y 0 0) (screenCoefficient g x y 0 1)

theorem oriented_screen_phase_unit (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (gp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (gm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b)
    (ho : ScreenOrientationMeasured g x y) : Complex.normSq (screenPhase g x y)=1 :=
  photon_phase_unit _ _ (oriented_screen_entries g x y hx hy gp gm ho).2.2

/-- The U(1) composition is extracted from the concrete transverse coefficients.
Orientation remains an explicit obligation for physical Lorentz transports. -/
theorem screen_phase_cocycle
    (g h : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y z : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0) (hz : z.1 ≠ 0)
    (hp : h (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (gp : g (shellMomentum 0 (rapidityChart 0 y))=shellMomentum 0 (rapidityChart 0 z))
    (hm : ∀ a b,orbitPairing (h a) (h b)=orbitPairing a b)
    (ho : ScreenOrientationMeasured h x y) :
    screenPhase (g.comp h) x z=screenPhase g y z*screenPhase h x y := by
  obtain ⟨h11,h10,_⟩ := oriented_screen_entries h x y hx hy hp hm ho
  unfold screenPhase
  rw [screenCoefficient_comp g h x y z hx hy hz hp gp hm 0 0,
      screenCoefficient_comp g h x y z hx hy hz hp gp hm 0 1,h10,h11]
  convert photon_phase_composes (screenCoefficient g y z 0 0)
    (screenCoefficient g y z 0 1) (screenCoefficient h x y 0 0)
    (screenCoefficient h x y 0 1) using 1 <;> congr 1 <;> ring

/-- The opposite helicity obeys the same composition law after conjugation. -/
theorem conjugate_phase_cocycle (a b c : ℂ) (h : a=b*c) :
    star a=star b*star c := by rw [h,star_mul,mul_comm]

#print axioms oriented_screen_entries
#print axioms oriented_screen_phase_unit
#print axioms screen_phase_cocycle
#print axioms conjugate_phase_cocycle
end ORDEM016.D1prime


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
