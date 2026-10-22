import ContinuousModularSquare
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace ChatgptAudit.Continuous050
open ChatgptAudit.Continuous049 MeasureTheory Filter
open scoped ENNReal ComplexOrder
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


/-- Pointwise meaning of the bounded resolvent, independent of its inverse identities. -/
theorem continuous_resolvent_ae (c : ℝ) (f : SpectralHilbert) :
    continuousResolvent c f =ᵐ[volume]
      fun x => (spectralWeightA c x : ℂ)^2 * f x := by
  filter_upwards [spectralA_ae c (spectralA c f), spectralA_ae c f] with x haa ha
  change (spectralA c (spectralA c f)) x = _
  rw [haa,ha]
  ring

/-- The two bounded coordinates construct both successive domain witnesses. -/
theorem continuous_resolvent_square_graph (c : ℝ) (f : SpectralHilbert) :
    (continuousResolvent c f, spectralB c (spectralB c f)) ∈
      (continuousModularSquare c).graph := by
  rw [continuous_modular_square_graph_iff]
  refine ⟨spectralA c (spectralB c f), ?_, ?_⟩
  · apply (bounded_graph_param_iff (spectralA c) (spectralB c)
      (spectralA_injective c) _ _).mpr
    refine ⟨spectralA c f,rfl,?_⟩
    exact congrArg (fun F : SpectralHilbert →L[ℂ] SpectralHilbert => F f)
      (spectralAB_commute c).symm
  · apply (bounded_graph_param_iff (spectralA c) (spectralB c)
      (spectralA_injective c) _ _).mpr
    exact ⟨spectralB c f,rfl,rfl⟩

theorem continuous_resolvent_mem_square_domain (c : ℝ) (f : SpectralHilbert) :
    continuousResolvent c f ∈ (continuousModularSquare c).domain :=
  LinearPMap.mem_domain_of_mem_graph (continuous_resolvent_square_graph c f)

theorem continuous_resolvent_square_apply (c : ℝ) (f : SpectralHilbert) :
    continuousModularSquare c
      ⟨continuousResolvent c f, continuous_resolvent_mem_square_domain c f⟩ =
        spectralB c (spectralB c f) :=
  ((LinearPMap.image_iff (continuous_resolvent_mem_square_domain c f)).mpr
    (continuous_resolvent_square_graph c f)).symm

/-- (I+T_c²) C_c f=f, with C_c f proved to lie in the full square domain. -/
theorem continuous_resolvent_right_inverse (c : ℝ) (f : SpectralHilbert) :
    continuousResolvent c f +
      continuousModularSquare c
        ⟨continuousResolvent c f, continuous_resolvent_mem_square_domain c f⟩ = f := by
  rw [continuous_resolvent_square_apply]
  exact congrArg (fun F : SpectralHilbert →L[ℂ] SpectralHilbert => F f)
    (spectralAB_square_sum c)

/-- C_c (x+T_c²x)=x for every x in the actual composition domain. -/
theorem continuous_resolvent_left_inverse (c : ℝ)
    (x : (continuousModularSquare c).domain) :
    continuousResolvent c ((x : SpectralHilbert) + continuousModularSquare c x) =
      (x : SpectralHilbert) := by
  apply Lp.ext
  have hg : ((x : SpectralHilbert), continuousModularSquare c x) ∈
      (continuousModularOperator (2*c)).graph := by
    rw [← continuous_modular_square_eq]
    exact (continuousModularSquare c).mem_graph x
  have hq := (continuous_modular_graph_iff (2*c) _ _).mp hg
  filter_upwards [
      continuous_resolvent_ae c ((x : SpectralHilbert) + continuousModularSquare c x),
      Lp.coeFn_add (x : SpectralHilbert) (continuousModularSquare c x), hq]
    with ξ hC hadd hQ
  rw [hC,hadd,Pi.add_apply,hQ,continuous_weight_double_complex]
  have hs : (spectralWeightA c ξ : ℂ)^2 + (spectralWeightB c ξ : ℂ)^2 = 1 := by
    exact_mod_cast spectral_weight_square_sum c ξ
  have hr : (spectralWeightB c ξ : ℂ) =
      (Real.exp (-c*ξ) : ℂ) * (spectralWeightA c ξ : ℂ) := by
    exact_mod_cast spectral_weight_ratio c ξ
  calc
    _ = ((spectralWeightA c ξ : ℂ)^2 +
        ((Real.exp (-c*ξ) : ℂ) * (spectralWeightA c ξ : ℂ))^2) *
          (x : SpectralHilbert) ξ := by ring
    _ = (x : SpectralHilbert) ξ := by rw [← hr,hs,one_mul]

/-- Uniqueness of the bounded resolvent among maps satisfying the right-inverse domain law. -/
theorem continuous_resolvent_unique (c : ℝ)
    (R : SpectralHilbert →L[ℂ] SpectralHilbert)
    (hdom : ∀ f : SpectralHilbert, R f ∈ (continuousModularSquare c).domain)
    (hinv : ∀ f : SpectralHilbert,
      R f + continuousModularSquare c ⟨R f,hdom f⟩ = f) :
    R = continuousResolvent c := by
  apply ContinuousLinearMap.ext
  intro f
  have h := continuous_resolvent_left_inverse c ⟨R f,hdom f⟩
  rw [hinv f] at h
  exact h.symm

#print axioms bounded_spectral_multiplier_nonneg
#print axioms spectralA_nonneg
#print axioms spectralB_nonneg
#print axioms continuousResolvent
#print axioms continuous_resolvent_complement
#print axioms continuous_resolvent_sqrt
#print axioms continuous_resolvent_complement_sqrt
#print axioms continuous_modular_graph_from_cfc
#print axioms continuous_modular_domain_from_cfc

#print axioms continuous_resolvent_ae
#print axioms continuous_resolvent_square_graph
#print axioms continuous_resolvent_mem_square_domain
#print axioms continuous_resolvent_square_apply
#print axioms continuous_resolvent_right_inverse
#print axioms continuous_resolvent_left_inverse
#print axioms continuous_resolvent_unique

end
end ChatgptAudit.Continuous050
