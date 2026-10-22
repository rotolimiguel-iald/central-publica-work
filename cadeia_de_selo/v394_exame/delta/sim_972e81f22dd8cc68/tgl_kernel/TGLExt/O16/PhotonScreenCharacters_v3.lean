-- predecessor_sha256: 1572acae35aa00b3b600946094697f6fce6c6d5e4c2f54207d2552b7904a6c8c
-- predecessor_sha256: 4e098c9d8b47b11c37945bca6963ec479d29181624dd424270fe25d3196a0025
import Lean
import TGLExt.O16.TransverseCocycle_v3
import TGLExt.O16.BoostScreenPolarizations_v2

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31
open ChatgptAudit.WignerRapidityMeasure016
namespace ORDEM016.D1prime

theorem pairing_sub_left (a b c : Fin 4 → ℝ) :
    orbitPairing (a-b) c = orbitPairing a c-orbitPairing b c := by
  simp [orbitPairing]; ring

theorem pairing_smul_left (a b : Fin 4 → ℝ) (r : ℝ) :
    orbitPairing (r • a) b = r*orbitPairing a b := by
  simp [orbitPairing]; ring

/-- The induced positive metric on the transverse quotient, in the existing chart. -/
theorem transverse_pairing (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (v w : Fin 4 → ℝ)
    (hv : orbitPairing v (shellMomentum 0 (rapidityChart 0 y))=0)
    (hw : orbitPairing w (shellMomentum 0 (rapidityChart 0 y))=0) :
    orbitPairing v w = -(orbitPairing v (screenOne y)*orbitPairing w (screenOne y))
      -orbitPairing v (screenTwo y)*orbitPairing w (screenTwo y) := by
  have hd := congrArg (fun u => orbitPairing u w) (transverse_decomposition y hy v hv)
  simp only [pairing_sub_left,pairing_smul_left] at hd
  rw [orbitPairing_symm (shellMomentum 0 (rapidityChart 0 y)) w, hw] at hd
  rw [orbitPairing_symm (screenOne y) w,orbitPairing_symm (screenTwo y) w] at hd
  simpa only [mul_zero,zero_sub] using hd

theorem screen_metric (x : MomentumCoordinates) (hx : x.1 ≠ 0) (i j : Fin 2) :
    orbitPairing (screen x i) (screen x j) = -(if i=j then 1 else 0) := by
  fin_cases i <;> fin_cases j <;>
    simp [screen,screenOne_unit,screenTwo_unit x hx,screens_orthogonal,
      orbitPairing_symm (screenTwo x) (screenOne x)]

/-- Metric preservation yields O(2); orientation is deliberately not assumed here. -/
theorem screen_columns_orthonormal
    (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (gp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (gm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b) (i j : Fin 2) :
    screenCoefficient g x y 0 i*screenCoefficient g x y 0 j+
      screenCoefficient g x y 1 i*screenCoefficient g x y 1 j = if i=j then 1 else 0 := by
  have ht (k : Fin 2) : orbitPairing (g (screen x k))
      (shellMomentum 0 (rapidityChart 0 y))=0 := by
    rw [←gp,gm]; exact screen_transverse x hx k
  have h := transverse_pairing y hy (g (screen x i)) (g (screen x j)) (ht i) (ht j)
  rw [gm,screen_metric x hx i j] at h
  simp only [screenCoefficient,screen,Matrix.cons_val_zero,Matrix.cons_val_one,
    Matrix.cons_val_fin_one,neg_mul_neg,orbitPairing_symm (screenOne y),
    orbitPairing_symm (screenTwo y)]
  simp only [screen] at h
  linarith

/-- Determinant +1 is the exact additional orientation obligation. -/
theorem oriented_two_frame (a b c d : ℝ)
    (h0 : a*a+c*c=1) (h1 : b*b+d*d=1) (hd : a*d-b*c=1) :
    d=a ∧ c = -b ∧ a*a+b*b=1 := by
  have hz : (d-a)^2+(b+c)^2=0 := by nlinarith
  have hda : d=a := by nlinarith [sq_nonneg (d-a),sq_nonneg (b+c)]
  have hcb : c = -b := by nlinarith [sq_nonneg (d-a),sq_nonneg (b+c)]
  exact ⟨hda,hcb,by nlinarith [h0]⟩

def photonPhase (a b : ℝ) : ℂ := (a : ℂ)+(b : ℂ)*Complex.I

theorem photon_phase_unit (a b : ℝ) (h : a*a+b*b=1) :
    Complex.normSq (photonPhase a b)=1 := by
  simpa [photonPhase,Complex.normSq_apply] using h

theorem photon_phase_composes (a b c d : ℝ) :
    photonPhase (a*c-b*d) (a*d+b*c)=photonPhase a b*photonPhase c d := by
  apply Complex.ext <;> simp [photonPhase] <;> ring

theorem conjugation_reverses_character (a b : ℝ) :
    star (photonPhase a b)=photonPhase a (-b) := by simp [photonPhase]

/-- Conjugation exchanges the two existing circular polarizations, on wavefunctions.
No PCT implementation on a photon net is inferred from this pointwise identity. -/
theorem conjugation_exchanges_wave_sections (f : MomentumCoordinates → ℂ) :
    (fun y i => star (f y * circularScreen 1 y i)) =
      fun y i => star (f y)*circularScreen (-1) y i := by
  funext y i
  rw [star_mul,congrFun (circularScreen_conjugate 1 y) i]
  exact mul_comm _ _

#print axioms pairing_sub_left
#print axioms pairing_smul_left
#print axioms transverse_pairing
#print axioms screen_metric
#print axioms screen_columns_orthonormal
#print axioms oriented_two_frame
#print axioms photon_phase_unit
#print axioms photon_phase_composes
#print axioms conjugation_reverses_character
#print axioms conjugation_exchanges_wave_sections
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
