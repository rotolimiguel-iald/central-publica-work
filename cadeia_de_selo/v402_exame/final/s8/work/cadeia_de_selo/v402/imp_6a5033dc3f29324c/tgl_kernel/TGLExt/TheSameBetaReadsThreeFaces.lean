import TGLExt.TheVerbalCoupling
import TGLExt.TheFiveHalves
import TGLExt.TheGeometricCostOfAbsoluteZero
import TGLExt.RhoPlusPClosure
import TGLExt.NoFullWitness

set_option autoImplicit false

/-!
# One coupling in the angular, cost and background readings (Order 012, B1)

The sole scalar datum is beta in (0,1). Alpha is its cost-normalized reading,
not another input or a numerically derived fine-structure constant. The result
specializes existing theorems. It is not yet a Friedmann equation or a physical
selection claim. Consumer: ext_same_beta_reads_three_faces_kernel_proved;
the background hypothesis of D1 is reached only after B2--B5.
-/

namespace TGLExt

/-- A single coupling datum, with the domain required by all three readings. -/
structure TGLCoupling where
  beta : ℝ
  beta_pos : 0 < beta
  beta_lt_one : beta < 1

namespace TGLCoupling

noncomputable section

/-- The cost-normalized reading; no independent alpha parameter is introduced. -/
def alpha (c : TGLCoupling) : ℝ := c.beta / Real.exp (1 / 2)

theorem alpha_pos (c : TGLCoupling) : 0 < c.alpha :=
  div_pos c.beta_pos (Real.exp_pos _)

theorem alpha_lt_one (c : TGLCoupling) : c.alpha < 1 := by
  unfold alpha
  apply (div_lt_one (Real.exp_pos _)).mpr
  exact c.beta_lt_one.trans the_minimal_volume_exceeds_one

theorem beta_eq_alpha_exp (c : TGLCoupling) :
    c.beta = c.alpha * Real.exp (1 / 2) := by
  exact (div_mul_cancel₀ c.beta (Real.exp_ne_zero _)).symm

theorem beta_eq_alpha_radical (c : TGLCoupling) :
    c.beta = c.alpha * Real.sqrt (Real.exp 1) := by
  rw [boundary_extracts_the_radical.1]
  exact c.beta_eq_alpha_exp

/-- The existing reflected amplitude, squared, reads precisely the same beta. -/
theorem reflection_weight (c : TGLCoupling) :
    Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta := by
  have h := (the_pruning_threshold_is_the_reflection_amplitude
    c.beta_pos.le c.beta_lt_one.le).1
  rwa [Real.sq_sqrt c.beta_pos.le] at h

/-- The same cost variable appears in the reflected weight without a new axiom. -/
theorem reflection_cost (c : TGLCoupling) :
    Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) =
      c.alpha * Real.sqrt (Real.exp 1) :=
  c.reflection_weight.trans c.beta_eq_alpha_radical

/-- Negative control: dropping the geometric cost changes the reflected weight. -/
theorem reflection_rejects_bare_alpha (c : TGLCoupling) :
    Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) ≠ c.alpha := by
  rw [c.reflection_weight, c.beta_eq_alpha_exp]
  have h := mul_lt_mul_of_pos_left the_minimal_volume_exceeds_one c.alpha_pos
  simpa only [mul_one] using ne_of_gt h

end
end TGLCoupling

/-- All clauses use the same projection c.beta. The background clauses are
    algebraic identities, not an imported or assumed Friedmann equation. -/
theorem the_same_beta_reads_three_faces (c : TGLCoupling) (ρr ρm ρΛ : ℝ) :
    Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta
    ∧ (0 < c.alpha ∧ c.alpha < 1
      ∧ c.beta = c.alpha * Real.exp (1 / 2)
      ∧ c.beta = c.alpha * Real.sqrt (Real.exp 1))
    ∧ (c.beta * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
        = c.beta * ((4 / 3) * ρr + ρm))
    ∧ ((ρr + ρm + ρΛ) + c.beta * ((4 / 3) * ρr + ρm)
        = (1 + 4 * c.beta / 3) * ρr + (1 + c.beta) * ρm + ρΛ)
    ∧ (∀ t g : ℝ, 0 < t → 0 < g → Real.exp (-(t * c.beta * g)) < 1)
    ∧ (∀ b : ℝ, (∀ t : ℝ, Real.exp (-(t * b)) = Real.exp (-(t * c.beta)))
        → b = c.beta) := by
  exact ⟨c.reflection_weight,
    ⟨c.alpha_pos, c.alpha_lt_one, c.beta_eq_alpha_exp, c.beta_eq_alpha_radical⟩,
    closure_identity c.beta ρr ρm ρΛ,
    hubble_form c.beta ρr ρm ρΛ,
    fun _ _ ht hg => leakage_strictly_loses ht c.beta_pos hg,
    fun _ h => leakage_rate_unique h⟩

end TGLExt
