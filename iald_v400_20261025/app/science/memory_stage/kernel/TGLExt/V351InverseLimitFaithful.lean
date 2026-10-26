import TGLExt.V351InverseLimitWeight

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem hilbertPositiveSqrt_conjugation_faithful {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R X : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R)
    (hz : star (hilbertPositiveSqrt R) * X * hilbertPositiveSqrt R = 0) : X = 0 := by
  have hsi : Function.Injective (hilbertPositiveSqrt R) := positive_sqrt_injective R hR hi
  have hsd : DenseRange (hilbertPositiveSqrt R) := resolventSquareRoot_dense R hR hi
  have hs : star (hilbertPositiveSqrt R) = hilbertPositiveSqrt R :=
    (CFC.sqrt_nonneg R).isSelfAdjoint.star_eq
  have hzv (v : H) : X (hilbertPositiveSqrt R v) = 0 := by
    apply hsi
    have he := congrArg (fun T : H →L[ℂ] H => T v) hz
    simpa only [hs,mul_apply_eq_comp,zero_apply,map_zero] using he
  ext1 x
  change X x = 0
  refine hsd.induction ?_ (isClosed_eq X.continuous continuous_const) x
  rintro _ ⟨v,rfl⟩
  exact hzv v

/-- The one existing resolvent cutoff is already faithful. -/
theorem scalarInverseCutoffWeight_one_faithful (P : SiteProfile) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P 1 X = 0 ↔ X = PositiveCoreInput.zero P := by
  constructor
  · intro hz
    obtain ⟨hm,_⟩ := regularInverseGeneratorCutoff_sqrt_right P 1 zero_lt_one
    let b := hilbertPositiveSqrt (regularInverseGeneratorCutoff P 1)
    have hmem : star b*X.val*b ∈ regularCoreAlgebra P :=
      (regularCoreAlgebra P).mul_mem
        ((regularCoreAlgebra P).mul_mem
          ((regularCoreAlgebra P).toStarSubalgebra.star_mem' hm) X.property.1) hm
    have he := (dualQuadraticIntegral_vacuum_faithful P (star b*X.val*b)
      hmem (star_left_conjugate_nonneg X.property.2 b)).mp hz
    dsimp only [b] at he
    rw [regularInverseGeneratorCutoff_one] at he
    apply Subtype.ext
    exact hilbertPositiveSqrt_conjugation_faithful (regularSpectralResolvent P) X.val
      (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_injective P) he
  · rintro rfl
    exact scalarInverseCutoffWeight_zero P 1

/-- A zero value of the supremum forces its n=0 cutoff to vanish. -/
theorem scalarInverseLimitWeight_faithful (P : SiteProfile) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X = 0 ↔ X = PositiveCoreInput.zero P := by
  constructor
  · intro hz
    have hh := scalarInverseCutoffWeight_le_limit P 0 X
    simp only [Nat.cast_zero,zero_add,div_one,hz] at hh
    exact (scalarInverseCutoffWeight_one_faithful P X).mp (le_antisymm hh bot_le)
  · rintro rfl
    exact scalarInverseLimitWeight_zero P

end
end TGLV350.Regular
