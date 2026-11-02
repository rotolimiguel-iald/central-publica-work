import TGLExt.LightNetStandardWedgeDataBGL
import Mathlib.MeasureTheory.Function.LpSpace.Basic
/-! Coordinatewise conjugation on the existing two-component fiber, then pointwise
conjugation on its transverse L2 space. No arbitrary Hilbert-space equivalence,
new physical hypothesis, or choice of basis beyond the existing Fib coordinates. -/

set_option autoImplicit false
set_option maxHeartbeats 800000

noncomputable section
namespace F1Rede.FiberConjugation
open MeasureTheory TGLExt.ImportedSQ AuditF13v31
open ChatgptAudit.WignerRapidityMeasure016

def fiberConj (v : Fib) : Fib := WithLp.toLp 2 (fun i => star (v i))

@[simp] theorem fiberConj_apply (v : Fib) (i : Fin 2) :
    fiberConj v i = star (v i) := rfl

theorem fiberConj_involutive : Function.Involutive fiberConj := by
  intro v
  ext i
  simp

def fiberJ : Fib ≃ₛₗᵢ[starRingEnd ℂ] Fib where
  toFun := fiberConj
  invFun := fiberConj
  left_inv := fiberConj_involutive
  right_inv := fiberConj_involutive
  map_add' := by intro x y; ext i; simp [fiberConj]
  map_smul' := by intro c x; ext i; simp [fiberConj]
  norm_map' := by
    intro v
    change ‖fiberConj v‖ = ‖v‖
    simp only [PiLp.norm_eq_of_L2, fiberConj_apply, norm_star]

@[simp] theorem fiberJ_apply (v : Fib) (i : Fin 2) :
    fiberJ v i = star (v i) := rfl

theorem fiberJ_involutive : Function.Involutive fiberJ := fiberConj_involutive

def transverseConj : TransverseFiber →ₛₗ[starRingEnd ℂ] TransverseFiber :=
  fiberJ.toContinuousLinearEquiv.toContinuousLinearMap.compLpₗ 2 volume

theorem transverseConj_ae (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse), transverseConj f q = fiberJ (f q) :=
  fiberJ.toContinuousLinearEquiv.toContinuousLinearMap.coeFn_compLp f

theorem transverseConj_involutive : Function.Involutive transverseConj := by
  intro f
  apply Lp.ext
  filter_upwards [transverseConj_ae (transverseConj f), transverseConj_ae f] with q h1 h2
  rw [h1, h2, fiberJ_involutive]

theorem transverseConj_norm (f : TransverseFiber) : ‖transverseConj f‖ = ‖f‖ := by
  simp only [Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [transverseConj_ae f] with q hq
  rw [hq, fiberJ.norm_map]

def transverseJ : TransverseFiber ≃ₛₗᵢ[starRingEnd ℂ] TransverseFiber where
  toFun := transverseConj
  invFun := transverseConj
  left_inv := transverseConj_involutive
  right_inv := transverseConj_involutive
  map_add' := transverseConj.map_add
  map_smul' := transverseConj.map_smulₛₗ
  norm_map' := transverseConj_norm

theorem transverseJ_involutive : Function.Involutive transverseJ :=
  transverseConj_involutive

theorem transverseJ_ae (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse), transverseJ f q = fiberJ (f q) :=
  transverseConj_ae f

theorem transverseJ_coordinates (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse), ∀ i : Fin 2,
      transverseJ f q i = star (f q i) := by
  filter_upwards [transverseJ_ae f] with q hq
  intro i
  rw [hq, fiberJ_apply]

#print axioms fiberJ
#print axioms fiberJ_involutive
#print axioms transverseJ
#print axioms transverseJ_involutive
#print axioms transverseJ_coordinates

end F1Rede.FiberConjugation

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    match ci with
    | .axiomInfo _ => throwError "NEW_AXIOM_REFUSED: {n}"
    | _ => pure ()
