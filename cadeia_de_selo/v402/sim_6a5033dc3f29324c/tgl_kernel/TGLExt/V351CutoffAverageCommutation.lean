import TGLExt.V351InverseCutoffCFC
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open TGLExt MeasureTheory
noncomputable section

private theorem hilbertPositiveSqrt_commutes {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A B : H →L[ℂ] H) (h : Commute A B) :
    Commute (hilbertPositiveSqrt A) B :=
  h.cfcₙ_nnreal NNReal.sqrt

/-- The resolvent and regular group commute in their original realization. -/
theorem regularSpectralResolvent_commutes_regular (P : SiteProfile) (t : ℝ) :
    Commute (regularSpectralResolvent P) (regularUnitary P t) := by
  let V := regularSpectralCoordinates P
  let C := characterMultiplier (H := TowerHilbert P) (2*Real.pi*t)
  let M := realScalarMultiplier (H := TowerHilbert P) (fun x => Real.sigmoid (2*Real.pi*x))
    (by fun_prop) (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _)
  have hchar (s : ℝ) : characterMultiplier s*C = C*characterMultiplier s := by
    dsimp only [C]
    rw [characterMultiplier_mul,characterMultiplier_mul,add_comm]
  have hm : Commute M C :=
    character_commutation_realScalarMultiplier C hchar _ _ _ _
  have hv : V.conjStarAlgEquiv C = regularUnitary P t := by
    ext1 x
    change V (C (V.symm x)) = regularUnitary P t x
    dsimp only [C]
    rw [regularSpectralCoordinates_character,V.apply_symm_apply]
  have hc := hm.map V.conjStarAlgEquiv
  change Commute (regularSpectralResolvent P) (V.conjStarAlgEquiv C) at hc
  rwa [hv] at hc

/-- The SAME positive square root of the existing cut commutes with the group. -/
theorem regularInverseCutoffSqrt_commutes_regular (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (t : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularUnitary P t) := by
  have hr := (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg P)).commute_cfc
    (regularSpectralResolvent_commutes_regular P t) (inverseCutoffFunction ε)
  rw [← regularInverseGeneratorCutoff_cfc P ε hε] at hr
  exact hilbertPositiveSqrt_commutes _ _ hr

/-- Integration preserves this proved commutation for every averaging interval. -/
theorem regularInverseCutoffSqrt_commutes_average (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularAverage P δ) := by
  let B := hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)
  ext1 v
  change B (regularAverage P δ v) = regularAverage P δ (B v)
  rw [regularAverage_apply,regularAverage_apply]
  change B (((δ⁻¹ : ℝ) : ℂ) • ∫ t in 0..δ, regularUnitary P t v) =
    ((δ⁻¹ : ℝ) : ℂ) • ∫ t in 0..δ, regularUnitary P t (B v)
  rw [map_smul]
  congr 1
  rw [← B.intervalIntegral_comp_comm ((regular_strongly_continuous P v).intervalIntegrable 0 δ)]
  apply intervalIntegral.integral_congr
  intro t _
  exact congrArg (fun T : RegularHilbert (TowerHilbert P) →L[ℂ] _ => T v)
    (regularInverseCutoffSqrt_commutes_regular P ε hε t).eq

end
end TGLV350.Regular
