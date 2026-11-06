import TGLExt.V351PerturbedWeightOrder
import TGLExt.V351WeightAverageRecovery
import TGLExt.V351CutoffAverageCommutation
import TGLExt.V350LevelExpectationUniformBound

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem hilbertPositiveSqrt_core_square {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (X : N.toStarSubalgebra) (hX : 0 ≤ X.val) :
    ∃ _ : hilbertPositiveSqrt X.val ∈ N,
      star (hilbertPositiveSqrt X.val) * hilbertPositiveSqrt X.val = X.val := by
  letI : IsClosed (N.toStarSubalgebra : Set (H →L[ℂ] H)) := vonNeumann_norm_closed N
  have hm : hilbertPositiveSqrt X.val ∈ N := by
    rw [hilbertPositiveSqrt,CFC.sqrt_eq_real_sqrt X.val hX]
    exact cfcₙ_mem (𝕜' := ℂ) (s := N.toStarSubalgebra) Real.sqrt X.property
  refine ⟨hm,?_⟩
  change star (CFC.sqrt X.val) * CFC.sqrt X.val = X.val
  rw [(CFC.sqrt_nonneg X.val).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self X.val hX]

/-- Extend the established finite-domain comparison by the original averages.
Both values may be infinite. Commutation with these averages is explicit. -/
theorem scalarWeight_right_perturbed_mono_all_squares (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c)
    (hbe : ∀ δ : ℝ, Commute b.val (regularAverage P δ))
    (hce : ∀ δ : ℝ, Commute c.val (regularAverage P δ))
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    dualQuadraticIntegral (star b.val * (star A.val*A.val) * b.val) (regularVacuum P) ≤
      dualQuadraticIntegral (star c.val * (star A.val*A.val) * c.val) (regularVacuum P) := by
  let d : ℕ → ℝ := fun n => 1/((n : ℝ)+1)
  have hd (n : ℕ) : 0 < d n := by dsimp [d]; positivity
  obtain ⟨hf,hm,_⟩ := scalarDualWeight_square_finite_strong_density P A
  let T (n : ℕ) : scalarWeightLeftIdeal P :=
    ⟨⟨A.val * regularAverage P (d n),hm (d n)⟩,hf (d n) (hd n)⟩
  have he (b' : (regularCoreAlgebra P).toStarSubalgebra)
      (hb' : ∀ δ : ℝ, Commute b'.val (regularAverage P δ)) (n : ℕ) :
      (A.val*b'.val)*regularAverage P (d n) = (A.val*regularAverage P (d n))*b'.val := by
    rw [mul_assoc,(hb' (d n)).eq,← mul_assoc]
  have hab := scalarWeight_square_eq_iSup_averages P (A*b)
  have hac := scalarWeight_square_eq_iSup_averages P (A*c)
  have hsup :
      (⨆ n : ℕ, dualQuadraticIntegral
        (star ((A.val*b.val)*regularAverage P (d n)) *
          ((A.val*b.val)*regularAverage P (d n))) (regularVacuum P)) ≤
      ⨆ n : ℕ, dualQuadraticIntegral
        (star ((A.val*c.val)*regularAverage P (d n)) *
          ((A.val*c.val)*regularAverage P (d n))) (regularVacuum P) := by
    apply iSup_le
    intro n
    apply le_iSup_of_le n
    rw [he b hbe n,he c hce n]
    have hh := scalarWeight_right_perturbed_mono P b c hb hc hbc (T n)
    simpa only [T,star_mul,mul_assoc] using hh
  change dualQuadraticIntegral (star (A.val*b.val)*(A.val*b.val)) (regularVacuum P) =
    (⨆ n : ℕ, dualQuadraticIntegral (star ((A.val*b.val)*regularAverage P (d n)) *
      ((A.val*b.val)*regularAverage P (d n))) (regularVacuum P)) at hab
  change dualQuadraticIntegral (star (A.val*c.val)*(A.val*c.val)) (regularVacuum P) =
    (⨆ n : ℕ, dualQuadraticIntegral (star ((A.val*c.val)*regularAverage P (d n)) *
      ((A.val*c.val)*regularAverage P (d n))) (regularVacuum P)) at hac
  dsimp only [d] at hsup
  rw [← hab,← hac] at hsup
  simpa only [star_mul,mul_assoc] using hsup

/-- The comparison holds on the entire positive cone of the same core,
using its actual positive square root, without a finite-weight premise. -/
theorem scalarWeight_right_perturbed_mono_all_positive (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c)
    (hbe : ∀ δ : ℝ, Commute b.val (regularAverage P δ))
    (hce : ∀ δ : ℝ, Commute c.val (regularAverage P δ))
    (X : PositiveCoreInput P) :
    dualQuadraticIntegral (star b.val * X.val * b.val) (regularVacuum P) ≤
      dualQuadraticIntegral (star c.val * X.val * c.val) (regularVacuum P) := by
  obtain ⟨hm,he⟩ := hilbertPositiveSqrt_core_square (regularCoreAlgebra P)
    ⟨X.val,X.property.1⟩ X.property.2
  have hh := scalarWeight_right_perturbed_mono_all_squares P b c hb hc hbc hbe hce
    ⟨hilbertPositiveSqrt X.val,hm⟩
  simpa only [he] using hh

end
end TGLV350.Regular
