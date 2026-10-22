import TGLExt.F1Fecho394.FubiniL2
import TGLExt.ContinuousModularMultipliers
set_option autoImplicit false
set_option maxHeartbeats 400000
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace F1Rede.SpectralConjugation
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
abbrev LH (H : Type) [NormedAddCommGroup H] := Lp H 2 (volume : Measure ℝ)
variable (jc : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive jc)
def reflection : LH H →ₗᵢ[ℂ] LH H :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun x : ℝ => -x) (Measure.measurePreserving_neg volume)
def JMap : LH H →SL[starRingEnd ℂ] LH H :=
  (jc.toContinuousLinearEquiv.toContinuousLinearMap.compLpL 2 volume).comp reflection.toContinuousLinearMap
theorem JMap_ae (f : LH H) : JMap jc f =ᵐ[volume] fun x => jc (f (-x)) := by
  have hc := jc.toContinuousLinearEquiv.toContinuousLinearMap.coeFn_compLpL (reflection f)
  have hr := Lp.coeFn_compMeasurePreserving f (Measure.measurePreserving_neg volume)
  filter_upwards [hc,hr] with x hx hrx
  change (jc.toContinuousLinearEquiv.toContinuousLinearMap.compLpL 2 volume (reflection f)) x = _
  rw [hx]
  change jc ((reflection f) x) = _
  change (reflection f) x = f (-x) at hrx
  rw [hrx]
include hJ
theorem JMap_involutive : Function.Involutive (JMap jc) := by
  intro f
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae (JMap_ae jc f)
  filter_upwards [JMap_ae jc (JMap jc f),hr] with x hx hy
  rw [hx,hy,neg_neg,hJ]
theorem JMap_norm (f : LH H) : ‖JMap jc f‖ = ‖f‖ := by
  have hbound : ∀ g : LH H, ‖JMap jc g‖ ≤ ‖g‖ := by
    intro g
    calc
      ‖JMap jc g‖ ≤ ‖reflection g‖ := by
        apply Lp.norm_le_norm_of_ae_le
        filter_upwards [jc.toContinuousLinearEquiv.toContinuousLinearMap.coeFn_compLpL (reflection g)] with x hx
        change ‖(jc.toContinuousLinearEquiv.toContinuousLinearMap.compLpL 2 volume (reflection g)) x‖ ≤ _
        rw [hx]
        exact (jc.norm_map ((reflection g) x)).le
      _ = ‖g‖ := reflection.norm_map g
  exact le_antisymm (hbound f) (by simpa only [JMap_involutive jc hJ f] using hbound (JMap jc f))
def J : LH H ≃ₛₗᵢ[starRingEnd ℂ] LH H where
  toLinearEquiv := { (JMap jc).toLinearMap with
    invFun := JMap jc
    left_inv := JMap_involutive jc hJ
    right_inv := JMap_involutive jc hJ }
  norm_map' := JMap_norm jc hJ
theorem J_ae (f : LH H) : J jc hJ f =ᵐ[volume] fun x => jc (f (-x)) := JMap_ae jc f
theorem J_involutive : Function.Involutive (J jc hJ) := JMap_involutive jc hJ
#print axioms J
#print axioms J_ae
#print axioms J_involutive
end F1Rede.SpectralConjugation