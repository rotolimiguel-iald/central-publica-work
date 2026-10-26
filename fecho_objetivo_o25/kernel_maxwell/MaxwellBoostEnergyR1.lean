import MaxwellShellGeometryR3
import OrbitalGeneratedMeasureR2

/-! Energy comparability for the EXISTING orbital boost. These estimates
preserve the concrete regular-profile moment domain; no new flow is defined. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Matrix
open TGLExt TGLExt.ImportedSQ F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016

def boostEnergyConstant (s : ℝ) : ℝ := Real.cosh s+|Real.sinh s|

theorem boostEnergyConstant_positive (s : ℝ) : 0<boostEnergyConstant s :=
  add_pos_of_pos_of_nonneg (Real.cosh_pos _) (abs_nonneg _)

theorem shellEnergy_boost_ae (s : ℝ) :
    ∀ᵐ y ∂orbitalMeasure 0,shellEnergy (coordinateBoost 0 s y)=
      Real.cosh s*shellEnergy y+Real.sinh s*y.2 := by
  filter_upwards [shell_boost_ae s] with y hy
  have h:=congrArg (fun v : Fin 4→ℝ=>v 0) hy
  simpa [theBoost,boostMat,Matrix.mulVec,Fin.sum_univ_four,shellMomentum,shellEnergy] using h

theorem shellEnergy_boost_bound_ae (s : ℝ) :
    ∀ᵐ y ∂orbitalMeasure 0,shellEnergy (coordinateBoost 0 s y)≤boostEnergyConstant s*shellEnergy y := by
  filter_upwards [shellEnergy_boost_ae s] with y hy
  rw [hy]
  have hl:Real.sinh s*y.2≤|Real.sinh s|*shellEnergy y := by
    calc
      _ ≤ |Real.sinh s*y.2| := le_abs_self _
      _ = |Real.sinh s|*|y.2| := abs_mul _ _
      _ ≤ _ := mul_le_mul_of_nonneg_left (abs_spatial_le_energy y).2.2 (abs_nonneg _)
  dsimp [boostEnergyConstant]
  nlinarith only [hl]

theorem coordinateBoost_inverse_ae (s : ℝ) :
    (fun y=>coordinateBoost 0 s (coordinateBoost 0 (-s) y))=ᵐ[orbitalMeasure 0] id := by
  have h:=shellLift_mul (shellLift_boost s) (shellLift_boost (-s))
  rw [theBoost_add,add_neg_cancel,theBoost_zero_eq] at h
  exact shellLift_unique h shellLift_one

theorem shellEnergy_boost_reverse_bound_ae (s : ℝ) :
    ∀ᵐ y ∂orbitalMeasure 0,shellEnergy y≤
      boostEnergyConstant s*shellEnergy (coordinateBoost 0 (-s) y) := by
  have hb:=(coordinateBoost_measurePreserving 0 (-s)).quasiMeasurePreserving.ae
    (shellEnergy_boost_bound_ae s)
  filter_upwards [hb,coordinateBoost_inverse_ae s] with y hy hi
  simpa only [hi,id_eq] using hy

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.boostEnergyConstant_positive
#print axioms F1Fecho.MaxwellGlobal.shellEnergy_boost_ae
#print axioms F1Fecho.MaxwellGlobal.shellEnergy_boost_bound_ae
#print axioms F1Fecho.MaxwellGlobal.coordinateBoost_inverse_ae
#print axioms F1Fecho.MaxwellGlobal.shellEnergy_boost_reverse_bound_ae
