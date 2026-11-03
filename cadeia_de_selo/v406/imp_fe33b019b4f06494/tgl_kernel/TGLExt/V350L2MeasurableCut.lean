import TGLExt.V350L2OperatorLift

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def measurableCutLp (S : Set ℝ) (hS : MeasurableSet S) (f : RegularHilbert H) :
    RegularHilbert H := ((Lp.memLp f).indicator hS).toLp (S.indicator f)

theorem measurableCutLp_ae (S : Set ℝ) (hS : MeasurableSet S) (f : RegularHilbert H) :
    measurableCutLp S hS f =ᵐ[volume] S.indicator f :=
  ((Lp.memLp f).indicator hS).coeFn_toLp

def measurableCutLinear (S : Set ℝ) (hS : MeasurableSet S) :
    RegularHilbert H →ₗ[ℂ] RegularHilbert H where
  toFun := measurableCutLp S hS
  map_add' f g := by
    apply Lp.ext
    filter_upwards [measurableCutLp_ae S hS (f+g), measurableCutLp_ae S hS f,
      measurableCutLp_ae S hS g, Lp.coeFn_add f g,
      Lp.coeFn_add (measurableCutLp S hS f) (measurableCutLp S hS g)] with x h1 h2 h3 h4 h5
    simp only [Pi.add_apply] at h4 h5
    rw [h1,h5,h2,h3]
    by_cases hx : x ∈ S
    · simp only [Set.indicator_of_mem hx]
      exact h4
    · simp only [Set.indicator_of_notMem hx, add_zero]
  map_smul' c f := by
    apply Lp.ext
    filter_upwards [measurableCutLp_ae S hS (c • f), measurableCutLp_ae S hS f,
      Lp.coeFn_smul c f, Lp.coeFn_smul c (measurableCutLp S hS f)] with x h1 h2 h3 h4
    simp only [Pi.smul_apply] at h3 h4
    simp only [RingHom.id_apply]
    rw [h1,h4,h2]
    by_cases hx : x ∈ S <;> simp [hx,h3]

theorem measurableCutLp_norm_le (S : Set ℝ) (hS : MeasurableSet S) (f : RegularHilbert H) :
    ‖measurableCutLp S hS f‖ ≤ ‖f‖ := by
  apply Lp.norm_le_norm_of_ae_le
  filter_upwards [measurableCutLp_ae S hS f] with x hx
  rw [hx]
  by_cases hxS : x ∈ S <;> simp [hxS]

/-- Multiplication by a measurable indicator on the actual L2 quotient,
constructed as a bounded complex-linear map. The set need not have finite measure. -/
def measurableCut (S : Set ℝ) (hS : MeasurableSet S) :
    RegularHilbert H →L[ℂ] RegularHilbert H :=
  (measurableCutLinear S hS).mkContinuous 1
    (fun f => by simpa [measurableCutLinear] using measurableCutLp_norm_le S hS f)

theorem measurableCut_ae (S : Set ℝ) (hS : MeasurableSet S) (f : RegularHilbert H) :
    measurableCut S hS f =ᵐ[volume] S.indicator f := measurableCutLp_ae S hS f

theorem measurableCut_inner (S : Set ℝ) (hS : MeasurableSet S) (f g : RegularHilbert H) :
    inner ℂ f (measurableCut S hS g) = ∫ x : ℝ in S, inner ℂ (f x) (g x) := by
  rw [L2.inner_def, ← integral_indicator hS]
  apply integral_congr_ae
  filter_upwards [measurableCut_ae S hS g] with x hx
  rw [hx]
  by_cases hxS : x ∈ S <;> simp [hxS]

#print axioms measurableCutLp
#print axioms measurableCutLinear
#print axioms measurableCutLp_norm_le
#print axioms measurableCut
#print axioms measurableCut_ae
#print axioms measurableCut_inner
end
end TGLV350.Regular
