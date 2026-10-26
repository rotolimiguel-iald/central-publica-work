import SmoothLinearMomentumCutoffR3
import SchwartzMaxwellCoefficientR5
import OrbitalLocalFinitenessR2

/-! Smooth compact profiles avoiding the fixed gauge axis form a dense class
in the unchanged orbital H1. This auxiliary chart class is not asserted to be
invariant under every Lorentz transformation. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Set TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016
open scoped ContDiff ENNReal

def transverseProjection : MomentumCoordinates→L[ℝ]Transverse :=
  ContinuousLinearMap.fst ℝ Transverse ℝ

theorem transverseProjection_ne_zero_ae :
    ∀ᵐy ∂orbitalMeasure 0,transverseProjection y≠0 := by
  rw [ae_iff]
  have hs : {y : MomentumCoordinates | ¬transverseProjection y≠0}=
      ({0}:Set Transverse) ×ˢ (Set.univ:Set ℝ) := by
    ext y
    simp [transverseProjection]
  rw [hs]
  exact exceptional_axis_orbital_null 0

def AxisCompactProfile (h : H1) : Prop :=
  F1Fecho.SmoothLinearMomentumCutoff.AwaySmoothCompactProfile
    transverseProjection (orbitalMeasure 0) h

theorem axisCompactProfile_dense : Dense {h : H1 | AxisCompactProfile h} := by
  exact F1Fecho.SmoothLinearMomentumCutoff.awaySmoothCompactProfile_dense
    transverseProjection (orbitalMeasure 0) transverseProjection_ne_zero_ae


end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.transverseProjection_ne_zero_ae
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_dense
