import TGLExt.V350UnitIntervalShiftProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Translation covariance propagates zero on a unit interval to all of L2.
Only a countable family of integer translates is combined almost everywhere. -/
theorem eq_zero_of_shift_commutation_unitCut_zero
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hshift : ∀ t : ℝ, shift t * A = A * shift t)
    (hunit : unitCut * A = 0) : A = 0 := by
  ext1 f
  have hlocal : ∀ n : ℤ, ∀ᵐ x : ℝ ∂volume,
      x+(n : ℝ) ∈ Set.Ioc (0 : ℝ) 1 → A f x = 0 := by
    intro n
    have hz : unitCut (shift (n : ℝ) (A f)) = 0 := by
      have hc := congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T f) (hshift n)
      change shift (n : ℝ) (A f) = A (shift (n : ℝ) f) at hc
      rw [hc]
      exact congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T (shift (n : ℝ) f)) hunit
    have h0 : (unitCut (shift (n : ℝ) (A f)) : ℝ → H) =ᵐ[volume] 0 := by
      rw [hz]
      exact Lp.coeFn_zero H 2 volume
    have hi : ∀ᵐ y : ℝ ∂volume, y ∈ Set.Ioc (0 : ℝ) 1 → A f (y-(n : ℝ)) = 0 := by
      filter_upwards [h0, measurableCut_ae (Set.Ioc (0 : ℝ) 1) measurableSet_Ioc
        (shift (n : ℝ) (A f)), shift_ae (n : ℝ) (A f)] with y hy0 hyc hys
      intro hy
      have hc : unitCut (shift (n : ℝ) (A f)) y = shift (n : ℝ) (A f) y := by
        exact hyc.trans (Set.indicator_of_mem hy _)
      exact hys.symm.trans (hc.symm.trans hy0)
    have ht := (measurePreserving_add_right volume (n : ℝ)).quasiMeasurePreserving.ae hi
    filter_upwards [ht] with x hx
    simpa only [add_sub_cancel_right] using hx
  have hall : ∀ᵐ x : ℝ ∂volume, ∀ n : ℤ,
      x+(n : ℝ) ∈ Set.Ioc (0 : ℝ) 1 → A f x = 0 := ae_all_iff.mpr hlocal
  apply Lp.ext
  filter_upwards [hall, Lp.coeFn_zero H 2 volume] with x hx hzero
  change A f x = (0 : RegularHilbert H) x
  rw [hzero]
  apply hx (1-Int.ceil x)
  have hlo := Int.ceil_lt_add_one x
  have hhi := Int.le_ceil x
  constructor <;> push_cast <;> linarith

#print axioms eq_zero_of_shift_commutation_unitCut_zero
end
end TGLV350.Regular
