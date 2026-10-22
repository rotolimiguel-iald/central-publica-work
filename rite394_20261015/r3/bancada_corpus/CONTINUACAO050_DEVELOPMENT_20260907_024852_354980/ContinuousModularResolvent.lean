import ContinuousModularDomain
import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace ChatgptAudit.Continuous050
open ChatgptAudit.Continuous049 MeasureTheory Filter
open scoped ENNReal
noncomputable section

/-- Nonnegative scalar weights produce positive bounded operators in the Loewner order. -/
theorem bounded_spectral_multiplier_nonneg (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) (hn : ∀ x, 0 ≤ w x) :
    0 ≤ boundedSpectralMultiplier w hw hb := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ContinuousLinearMap.isPositive_def'.mpr
  refine ⟨bounded_spectral_multiplier_selfadjoint w hw hb, ?_⟩
  intro f
  change 0 ≤ (inner ℂ (boundedSpectralMultiplier w hw hb f) f).re
  rw [L2.inner_def]
  change 0 ≤ RCLike.re (∫ x : ℝ,
    inner ℂ ((boundedSpectralMultiplier w hw hb f) x) (f x))
  rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) (boundedSpectralMultiplier w hw hb f) f)]
  apply integral_nonneg_of_ae
  filter_upwards [bounded_spectral_multiplier_ae w hw hb f] with x hx
  rw [hx]
  change 0 ≤ (inner ℂ ((w x : ℂ) * f x) (f x)).re
  have he : (inner ℂ ((w x : ℂ) * f x) (f x)).re = w x * ‖f x‖ ^ 2 := by
    simp [RCLike.inner_apply, Complex.mul_re, Complex.normSq_apply, Complex.sq_norm, mul_add]
    ring
  rw [he]
  exact mul_nonneg (hn x) (sq_nonneg _)

theorem spectralA_nonneg (c : ℝ) : 0 ≤ spectralA c :=
  bounded_spectral_multiplier_nonneg _ _ _ (fun x => le_of_lt (spectral_weightA_pos c x))

theorem spectralB_nonneg (c : ℝ) : 0 ≤ spectralB c :=
  bounded_spectral_multiplier_nonneg _ _ _ (fun x => le_of_lt (spectral_weightB_pos c x))

/-- Its resolvent meaning is proved by the two domain identities below. -/
def continuousResolvent (c : ℝ) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  spectralA c * spectralA c

theorem continuous_resolvent_complement (c : ℝ) :
    1 - continuousResolvent c = spectralB c * spectralB c := by
  have h := spectralAB_square_sum c
  unfold continuousResolvent
  exact sub_eq_iff_eq_add.mpr (by simpa only [add_comm] using h.symm)

theorem continuous_resolvent_sqrt (c : ℝ) :
    CFC.sqrt (continuousResolvent c) = spectralA c :=
  CFC.sqrt_unique rfl (spectralA_nonneg c)

theorem continuous_resolvent_complement_sqrt (c : ℝ) :
    CFC.sqrt (1 - continuousResolvent c) = spectralB c :=
  CFC.sqrt_unique (continuous_resolvent_complement c).symm (spectralB_nonneg c)

/-- The graph coordinates are genuine bounded CFC roots. -/
theorem continuous_modular_graph_from_cfc (c : ℝ) (f g : SpectralHilbert) :
    (f,g) ∈ (continuousModularOperator c).graph ↔
      ∃ h : SpectralHilbert,
        CFC.sqrt (continuousResolvent c) h = f ∧
        CFC.sqrt (1 - continuousResolvent c) h = g := by
  rw [continuous_resolvent_sqrt, continuous_resolvent_complement_sqrt]
  exact bounded_graph_param_iff (spectralA c) (spectralB c) (spectralA_injective c) f g

theorem continuous_modular_domain_from_cfc (c : ℝ) :
    (continuousModularOperator c).domain =
      (CFC.sqrt (continuousResolvent c)).range := by
  rw [continuous_resolvent_sqrt]
  rfl

#print axioms bounded_spectral_multiplier_nonneg
#print axioms spectralA_nonneg
#print axioms spectralB_nonneg
#print axioms continuousResolvent
#print axioms continuous_resolvent_complement
#print axioms continuous_resolvent_sqrt
#print axioms continuous_resolvent_complement_sqrt
#print axioms continuous_modular_graph_from_cfc
#print axioms continuous_modular_domain_from_cfc

end
end ChatgptAudit.Continuous050
