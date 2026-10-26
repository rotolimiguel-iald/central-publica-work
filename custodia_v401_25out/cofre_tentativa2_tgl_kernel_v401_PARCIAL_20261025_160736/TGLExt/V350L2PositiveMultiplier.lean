import TGLExt.V350StrongOperatorField

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open MeasureTheory
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A continuous real scalar contraction, acting in the same L² coordinate. -/
def realScalarField (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) : StrongIntegral.Family (H := H) where
  op s := (g s : ℂ) • ContinuousLinearMap.id ℂ H
  continuous_apply v := (Complex.continuous_ofReal.comp hg).smul continuous_const
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound s := ContinuousLinearMap.opNorm_le_bound _ zero_le_one (fun v => by
    change ‖(g s : ℂ) • v‖ ≤ 1 * ‖v‖
    simp only [norm_smul,
      Complex.norm_real,Real.norm_eq_abs,abs_of_nonneg (h0 s),one_mul]
    exact mul_le_of_le_one_left (norm_nonneg v) (h1 s))

def realScalarMultiplier (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) :
    RegularHilbert H →L[ℂ] RegularHilbert H :=
  operatorFieldLift (realScalarField g hg h0 h1)

theorem realScalarMultiplier_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    realScalarMultiplier g hg h0 h1 f =ᵐ[volume] fun s => (g s : ℂ) • f s :=
  operatorFieldLift_ae (realScalarField g hg h0 h1) f

theorem realScalarMultiplier_norm_le (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    ‖realScalarMultiplier g hg h0 h1 f‖ ≤ ‖f‖ := by
  change ‖operatorFieldLift (realScalarField g hg h0 h1) f‖ ≤ ‖f‖
  have hb : ‖operatorFieldLift (realScalarField (H := H) g hg h0 h1)‖ ≤ 1 :=
    operatorFieldLift_norm_le (realScalarField g hg h0 h1)
  simpa only [one_mul] using
    (operatorFieldLift (realScalarField g hg h0 h1)).le_of_opNorm_le hb f

/-- Strict positivity gives injectivity of L² classes, without a bounded inverse. -/
theorem realScalarMultiplier_injective (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (hpos : ∀ s, 0 < g s) :
    Function.Injective (realScalarMultiplier (H := H) g hg h0 h1) := by
  intro f k hk
  apply Lp.ext
  filter_upwards [realScalarMultiplier_ae g hg h0 h1 f,
    realScalarMultiplier_ae g hg h0 h1 k] with s hf hh
  have he : (g s : ℂ) • (f s - k s) = 0 := by
    rw [smul_sub,← hf,← hh,hk,sub_self]
  have hn : (g s : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr (ne_of_gt (hpos s))
  exact sub_eq_zero.mp ((smul_eq_zero.mp he).resolve_left hn)

theorem realScalarMultiplier_commutes_field (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1)
    (F : StrongIntegral.Family (H := H)) :
    realScalarMultiplier g hg h0 h1 * operatorFieldLift F =
      operatorFieldLift F * realScalarMultiplier g hg h0 h1 := by
  ext1 f
  apply Lp.ext
  filter_upwards [realScalarMultiplier_ae g hg h0 h1 (operatorFieldLift F f),
    operatorFieldLift_ae F f,
    operatorFieldLift_ae F (realScalarMultiplier g hg h0 h1 f),
    realScalarMultiplier_ae g hg h0 h1 f] with s h2 h3 h4 h5
  change realScalarMultiplier g hg h0 h1 (operatorFieldLift F f) s =
    operatorFieldLift F (realScalarMultiplier g hg h0 h1 f) s
  rw [h2,h3,h4,h5,map_smul]

#print axioms realScalarField
#print axioms realScalarMultiplier
#print axioms realScalarMultiplier_ae
#print axioms realScalarMultiplier_norm_le
#print axioms realScalarMultiplier_injective
#print axioms realScalarMultiplier_commutes_field
end
end TGLV350.Regular
