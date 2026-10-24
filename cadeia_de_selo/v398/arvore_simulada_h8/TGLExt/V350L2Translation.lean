import TGLExt.V350L2OperatorLift

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Translation on Lebesgue L², with the convention (S_t f)(x)=f(x-t). -/
def shiftIsometry (t : ℝ) : RegularHilbert H →ₗᵢ[ℂ] RegularHilbert H :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun x : ℝ => x-t) (measurePreserving_sub_right volume t)

def shift (t : ℝ) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  (shiftIsometry t).toContinuousLinearMap

theorem shift_ae (t : ℝ) (f : RegularHilbert H) :
    shift t f =ᵐ[volume] fun x : ℝ => f (x-t) :=
  Lp.coeFn_compMeasurePreserving f (measurePreserving_sub_right volume t)

theorem shift_norm (t : ℝ) (f : RegularHilbert H) : ‖shift t f‖ = ‖f‖ :=
  (shiftIsometry t).norm_map f

theorem shift_zero : shift (H := H) 0 = 1 := by
  ext1 f
  apply Lp.ext
  filter_upwards [shift_ae 0 f] with x hx
  change (shift (H := H) 0 f) x = f x
  simpa only [sub_zero] using hx

theorem shift_mul (s t : ℝ) : shift (H := H) s * shift t = shift (s+t) := by
  ext1 f
  apply Lp.ext
  filter_upwards [shift_ae s (shift t f), shift_ae (s+t) f,
    (measurePreserving_sub_right volume s).quasiMeasurePreserving.ae (shift_ae t f)]
    with x h1 h2 h3
  change (shift s (shift t f)) x = (shift (s+t) f) x
  rw [h1, h2, h3]
  congr 1
  ring

theorem shift_inverse (t : ℝ) (f : RegularHilbert H) : shift t (shift (-t) f) = f := by
  change (shift (H := H) t * shift (-t) : RegularHilbert H →L[ℂ] RegularHilbert H) f = f
  rw [shift_mul, add_neg_cancel, shift_zero]
  rfl

theorem shift_star (t : ℝ) : star (shift (H := H) t) = shift (-t) := by
  rw [ContinuousLinearMap.star_eq_adjoint]
  ext1 y
  apply ext_inner_left ℂ
  intro x
  rw [ContinuousLinearMap.adjoint_inner_right]
  have h := (shiftIsometry t).inner_map_map x (shift (-t) y)
  change inner ℂ (shift t x) (shift t (shift (-t) y)) = inner ℂ x (shift (-t) y) at h
  rw [shift_inverse] at h
  exact h

theorem shift_commutes_fibre (t : ℝ) (T : H →L[ℂ] H) :
    shift t * fibre T = fibre T * shift t := by
  ext1 f
  apply Lp.ext
  filter_upwards [shift_ae t (fibre T f), fibre_ae T (shift t f), shift_ae t f,
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae (fibre_ae T f)]
    with x h1 h2 h3 h4
  change (shift t (fibre T f)) x = (fibre T (shift t f)) x
  rw [h1, h2, h3, h4]

def shiftMap (t : ℝ) : ContinuousMap ℝ ℝ :=
  ⟨fun x => x-t, continuous_id.sub continuous_const⟩

theorem shiftMap_continuous : Continuous shiftMap := by
  apply ContinuousMap.continuous_of_continuous_uncurry
  exact continuous_snd.sub continuous_fst

/-- The topology here is the real topology, not a discrete surrogate for ℝ. -/
theorem shift_strongly_continuous (f : RegularHilbert H) :
    Continuous (fun t : ℝ => shift t f) := by
  exact (continuous_const : Continuous (fun _ : ℝ => f)).compMeasurePreservingLp
    shiftMap_continuous (fun t => measurePreserving_sub_right volume t) (by norm_num)

#print axioms shift_mul
#print axioms shift_star
#print axioms shift_commutes_fibre
#print axioms shift_strongly_continuous
end
end TGLV350.Regular
