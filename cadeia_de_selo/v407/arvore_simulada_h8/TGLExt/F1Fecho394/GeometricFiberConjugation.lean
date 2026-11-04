import TGLExt.F1Fecho394.FiberConjugation
import Mathlib.MeasureTheory.Group.Measure
/-! A geometric candidate: transverse reflection and exchange of the two existing
fiber components, composed with coordinate conjugation. The pointwise formula and
involution are proved. No identification with global PCT is asserted. -/

set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Rede.FiberConjugation
open MeasureTheory TGLExt.ImportedSQ AuditF13v31
open ChatgptAudit.WignerRapidityMeasure016

def helicitySwap : Fin 2 ≃ Fin 2 := Equiv.swap 0 1

@[simp] theorem helicitySwap_twice (i : Fin 2) : helicitySwap (helicitySwap i) = i := by
  simp [helicitySwap]

def fiberSwap : Fib ≃ₗᵢ[ℂ] Fib :=
  LinearIsometryEquiv.piLpCongrLeft 2 ℂ ℂ helicitySwap

@[simp] theorem fiberSwap_apply (v : Fib) (i : Fin 2) :
    fiberSwap v i = v (helicitySwap i) := by
  rfl

def fiberSwappedJ : Fib ≃ₛₗᵢ[starRingEnd ℂ] Fib := fiberJ.trans fiberSwap

@[simp] theorem fiberSwappedJ_apply (v : Fib) (i : Fin 2) :
    fiberSwappedJ v i = star (v (helicitySwap i)) := rfl

theorem fiberSwappedJ_involutive : Function.Involutive fiberSwappedJ := by
  intro v
  ext i
  simp

def transverseNeg : TransverseFiber →ₗᵢ[ℂ] TransverseFiber :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun q : Transverse => -q)
    (Measure.measurePreserving_neg volume)

theorem transverseNeg_ae (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse), transverseNeg f q = f (-q) :=
  Lp.coeFn_compMeasurePreserving f (Measure.measurePreserving_neg volume)

def swappedPointwise : TransverseFiber →ₛₗ[starRingEnd ℂ] TransverseFiber :=
  fiberSwappedJ.toContinuousLinearEquiv.toContinuousLinearMap.compLpₗ 2 volume

theorem swappedPointwise_ae (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse), swappedPointwise f q = fiberSwappedJ (f q) :=
  fiberSwappedJ.toContinuousLinearEquiv.toContinuousLinearMap.coeFn_compLp f

theorem swappedPointwise_norm (f : TransverseFiber) : ‖swappedPointwise f‖ = ‖f‖ := by
  simp only [Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [swappedPointwise_ae f] with q hq
  rw [hq, fiberSwappedJ.norm_map]

def transverseGeometricConj : TransverseFiber →ₛₗ[starRingEnd ℂ] TransverseFiber :=
  swappedPointwise.comp transverseNeg.toLinearMap

theorem transverseGeometricConj_ae (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse),
      transverseGeometricConj f q = fiberSwappedJ (f (-q)) := by
  filter_upwards [swappedPointwise_ae (transverseNeg f), transverseNeg_ae f] with q h1 h2
  change swappedPointwise (transverseNeg f) q = _
  rw [h1, h2]

theorem transverseGeometricConj_involutive : Function.Involutive transverseGeometricConj := by
  intro f
  apply Lp.ext
  filter_upwards [transverseGeometricConj_ae (transverseGeometricConj f),
    (Measure.measurePreserving_neg (volume : Measure Transverse)).quasiMeasurePreserving.ae
      (transverseGeometricConj_ae f)] with q h1 h2
  rw [h1, h2]
  simp only [neg_neg]
  exact fiberSwappedJ_involutive (f q)

theorem transverseGeometricConj_norm (f : TransverseFiber) :
    ‖transverseGeometricConj f‖ = ‖f‖ := by
  change ‖swappedPointwise (transverseNeg f)‖ = _
  rw [swappedPointwise_norm, transverseNeg.norm_map]

def transverseGeometricJ : TransverseFiber ≃ₛₗᵢ[starRingEnd ℂ] TransverseFiber where
  toFun := transverseGeometricConj
  invFun := transverseGeometricConj
  left_inv := transverseGeometricConj_involutive
  right_inv := transverseGeometricConj_involutive
  map_add' := transverseGeometricConj.map_add
  map_smul' := transverseGeometricConj.map_smulₛₗ
  norm_map' := transverseGeometricConj_norm

theorem transverseGeometricJ_involutive : Function.Involutive transverseGeometricJ :=
  transverseGeometricConj_involutive

theorem transverseGeometricJ_ae (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse), transverseGeometricJ f q = fiberSwappedJ (f (-q)) :=
  transverseGeometricConj_ae f

theorem transverseGeometricJ_coordinates (f : TransverseFiber) :
    ∀ᵐ q ∂(volume : Measure Transverse), ∀ i : Fin 2,
      transverseGeometricJ f q i = star (f (-q) (helicitySwap i)) := by
  filter_upwards [transverseGeometricJ_ae f] with q hq
  intro i
  rw [hq, fiberSwappedJ_apply]

#print axioms fiberSwappedJ
#print axioms fiberSwappedJ_involutive
#print axioms transverseGeometricJ
#print axioms transverseGeometricJ_involutive
#print axioms transverseGeometricJ_coordinates
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
