import TGLExt.F1Fecho394.GeneralRegularCutoffCFCR1
import TGLExt.F1Fecho394.RegularCoreAverageR2
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace F1Fecho.RegularPositiveFlow
open TGLExt TGLV350.Regular MeasureTheory
noncomputable section
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

private theorem hilbertPositiveSqrt_commutes {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A B : H →L[ℂ] H) (h : Commute A B) :
    Commute (hilbertPositiveSqrt A) B :=
  h.cfcₙ_nnreal NNReal.sqrt

/-- The resolvent and regular group commute in their original realization. -/
theorem regularSpectralResolvent_commutes_regular (Q : F1Fecho.RegularCovariantCore.UnitaryFlow H) (t : ℝ) :
    Commute (regularSpectralResolvent Q) (RegularCovariantCore.regularUnitary Q t) := by
  let V := regularSpectralCoordinates Q
  let C := characterMultiplier (H := H) (2*Real.pi*t)
  let M := realScalarMultiplier (H := H) (fun x => Real.sigmoid (2*Real.pi*x))
    (by fun_prop) (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _)
  have hchar (s : ℝ) : characterMultiplier s*C = C*characterMultiplier s := by
    dsimp only [C]
    rw [characterMultiplier_mul,characterMultiplier_mul,add_comm]
  have hm : Commute M C :=
    character_commutation_realScalarMultiplier C hchar _ _ _ _
  have hv : V.conjStarAlgEquiv C = RegularCovariantCore.regularUnitary Q t := by
    ext1 x
    change V (C (V.symm x)) = RegularCovariantCore.regularUnitary Q t x
    dsimp only [C]
    rw [regularSpectralCoordinates_character,V.apply_symm_apply]
  have hc := hm.map V.conjStarAlgEquiv
  change Commute (regularSpectralResolvent Q) (V.conjStarAlgEquiv C) at hc
  rwa [hv] at hc

/-- The SAME positive square root of the existing cut commutes with the group. -/
theorem regularInverseCutoffSqrt_commutes_regular (Q : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (ε : ℝ) (hε : 0 < ε) (t : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff Q ε))
      (RegularCovariantCore.regularUnitary Q t) := by
  have hr := (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg Q)).commute_cfc
    (regularSpectralResolvent_commutes_regular Q t) (inverseCutoffFunction ε)
  rw [← regularInverseGeneratorCutoff_cfc Q ε hε] at hr
  exact hilbertPositiveSqrt_commutes _ _ hr

/-- Integration preserves this proved commutation for every averaging interval. -/
theorem regularInverseCutoffSqrt_commutes_average (Q : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff Q ε))
      (RegularCoreAverage.regularAverage Q δ) := by
  let B := hilbertPositiveSqrt (regularInverseGeneratorCutoff Q ε)
  ext1 v
  change B (RegularCoreAverage.regularAverage Q δ v) = RegularCoreAverage.regularAverage Q δ (B v)
  rw [RegularCoreAverage.regularAverage_apply,RegularCoreAverage.regularAverage_apply]
  change B (((δ⁻¹ : ℝ) : ℂ) • ∫ t in 0..δ, RegularCovariantCore.regularUnitary Q t v) =
    ((δ⁻¹ : ℝ) : ℂ) • ∫ t in 0..δ, RegularCovariantCore.regularUnitary Q t (B v)
  rw [map_smul]
  congr 1
  rw [← B.intervalIntegral_comp_comm ((RegularCovariantCore.regular_strongly_continuous Q v).intervalIntegrable 0 δ)]
  apply intervalIntegral.integral_congr
  intro t _
  exact congrArg (fun T : RegularHilbert (H) →L[ℂ] _ => T v)
    (regularInverseCutoffSqrt_commutes_regular Q ε hε t).eq

end
end F1Fecho.RegularPositiveFlow

#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent_commutes_regular
#print axioms F1Fecho.RegularPositiveFlow.regularInverseCutoffSqrt_commutes_regular
#print axioms F1Fecho.RegularPositiveFlow.regularInverseCutoffSqrt_commutes_average
