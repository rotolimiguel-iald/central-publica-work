import BoundedGraphOperator
import ContinuousModularMultipliers
import Mathlib.MeasureTheory.Measure.Typeclasses.NoAtoms

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Continuous049

open MeasureTheory Filter Set
open scoped ENNReal
noncomputable section

/-- The very same partial operator defined by the bounded graph coordinates. -/
def continuousModularOperator (c : ℝ) : SpectralHilbert →ₗ.[ℂ] SpectralHilbert :=
  boundedGraphOperator (spectralA c) (spectralB c) (spectralA_injective c)

theorem continuous_modular_domain_dense (c : ℝ) :
    Dense ((continuousModularOperator c).domain : Set SpectralHilbert) :=
  bounded_graph_domain_dense (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralA_selfadjoint c)

theorem continuous_modular_closed (c : ℝ) : (continuousModularOperator c).IsClosed :=
  bounded_graph_closed (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralAB_commute c) (spectralAB_square_sum c)

theorem continuous_modular_selfadjoint (c : ℝ) : IsSelfAdjoint (continuousModularOperator c) :=
  bounded_graph_selfadjoint (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralA_selfadjoint c) (spectralB_selfadjoint c)
    (spectralAB_commute c) (spectralAB_square_sum c)

theorem continuous_modular_positive (c : ℝ) (f : (continuousModularOperator c).domain) :
    0 ≤ (inner ℂ (f : SpectralHilbert) (continuousModularOperator c f)).re :=
  bounded_graph_positive (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralAB_quadratic_nonneg c) f

/-- Equality of the graph with multiplication by exp(-cξ), in L² equivalence classes. -/
theorem continuous_modular_graph_iff (c : ℝ) (f g : SpectralHilbert) :
    (f,g) ∈ (continuousModularOperator c).graph ↔
      g =ᵐ[volume] fun x => (Real.exp (-c * x) : ℂ) * f x := by
  change (f,g) ∈ (boundedGraphOperator (spectralA c) (spectralB c)
    (spectralA_injective c)).graph ↔ _
  rw [bounded_graph_equation_iff (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralAB_commute c) (spectralAB_square_sum c)]
  constructor
  · intro hfg
    filter_upwards [spectralB_ae c f, spectralA_ae c g] with x hb ha
    have he := congrArg (fun u : SpectralHilbert => u x) hfg
    rw [hb, ha] at he
    have hn : (spectralWeightA c x : ℂ) ≠ 0 := by
      exact_mod_cast ne_of_gt (spectral_weightA_pos c x)
    have hr : (spectralWeightB c x : ℂ) =
        (Real.exp (-c * x) : ℂ) * (spectralWeightA c x : ℂ) := by
      exact_mod_cast spectral_weight_ratio c x
    apply mul_left_cancel₀ hn
    calc
      (spectralWeightA c x : ℂ) * g x = (spectralWeightB c x : ℂ) * f x := he.symm
      _ = (spectralWeightA c x : ℂ) * ((Real.exp (-c * x) : ℂ) * f x) := by
        rw [hr]
        ring
  · intro hfg
    apply Lp.ext
    filter_upwards [spectralB_ae c f, spectralA_ae c g, hfg] with x hb ha hg
    rw [hb, ha, hg]
    have hr : (spectralWeightB c x : ℂ) =
        (Real.exp (-c * x) : ℂ) * (spectralWeightA c x : ℂ) := by
      exact_mod_cast spectral_weight_ratio c x
    rw [hr]
    ring

theorem continuous_modular_apply_ae (c : ℝ) (f : (continuousModularOperator c).domain) :
    continuousModularOperator c f =ᵐ[volume]
      fun x => (Real.exp (-c * x) : ℂ) * (f : SpectralHilbert) x :=
  (continuous_modular_graph_iff c _ _).mp ((continuousModularOperator c).mem_graph f)

/-- Domain membership is proved equivalent to the integrability of the weighted function. -/
theorem continuous_modular_domain_iff (c : ℝ) (f : SpectralHilbert) :
    f ∈ (continuousModularOperator c).domain ↔
      MemLp (fun x => (Real.exp (-c * x) : ℂ) * f x) 2 (volume : Measure ℝ) := by
  constructor
  · intro hf
    exact (Lp.memLp (continuousModularOperator c ⟨f,hf⟩)).ae_eq
      (continuous_modular_apply_ae c ⟨f,hf⟩)
  · intro hf
    have hg : (f, hf.toLp _) ∈ (continuousModularOperator c).graph :=
      (continuous_modular_graph_iff c f (hf.toLp _)).mpr hf.coeFn_toLp
    exact LinearPMap.mem_domain_of_mem_graph hg

theorem continuous_weight_fiber_subsingleton (c : ℝ) (hc : c ≠ 0) (z : ℂ) :
    ({x : ℝ | (Real.exp (-c * x) : ℂ) = z} : Set ℝ).Subsingleton := by
  intro x hx y hy
  have he : Real.exp (-c * x) = Real.exp (-c * y) :=
    Complex.ofReal_injective (hx.trans hy.symm)
  have hm : -c * x = -c * y := Real.exp_injective he
  exact mul_left_cancel₀ (neg_ne_zero.mpr hc) hm

/-- Every eigenvalue fiber is null, including for arbitrary complex candidate eigenvalues. -/
theorem continuous_weight_fiber_null (c : ℝ) (hc : c ≠ 0) (z : ℂ) :
    (volume : Measure ℝ) {x : ℝ | (Real.exp (-c * x) : ℂ) = z} = 0 :=
  (continuous_weight_fiber_subsingleton c hc z).measure_zero volume

theorem continuous_modular_no_eigen (c : ℝ) (hc : c ≠ 0) (z : ℂ)
    (f : (continuousModularOperator c).domain)
    (hf : continuousModularOperator c f = z • (f : SpectralHilbert)) :
    (f : SpectralHilbert) = 0 := by
  apply Lp.eq_zero_iff_ae_eq_zero.mpr
  have hn : ∀ᵐ x : ℝ ∂volume, (Real.exp (-c * x) : ℂ) ≠ z :=
    (continuous_weight_fiber_subsingleton c hc z).countable.ae_notMem volume
  have he := continuous_modular_apply_ae c f
  rw [hf] at he
  filter_upwards [he, Lp.coeFn_smul z (f : SpectralHilbert), hn] with x hx hs hne
  change (f : SpectralHilbert) x = 0
  have hm : ((Real.exp (-c * x) : ℂ) - z) * (f : SpectralHilbert) x = 0 := by
    rw [hs] at hx
    change z * (f : SpectralHilbert) x =
      (Real.exp (-c * x) : ℂ) * (f : SpectralHilbert) x at hx
    rw [sub_mul, ← hx, sub_self]
  exact (mul_eq_zero.mp hm).resolve_left (sub_ne_zero.mpr hne)

/-- At c=0 the construction is the identity, with its full domain. -/
theorem continuous_modular_zero_graph (f : SpectralHilbert) :
    (f,f) ∈ (continuousModularOperator 0).graph := by
  apply (continuous_modular_graph_iff 0 f f).mpr
  filter_upwards [] with x
  simp

theorem continuous_modular_zero_domain : (continuousModularOperator 0).domain = ⊤ := by
  apply top_unique
  intro f _
  exact LinearPMap.mem_domain_of_mem_graph (continuous_modular_zero_graph f)

theorem continuous_modular_zero_apply (f : (continuousModularOperator 0).domain) :
    continuousModularOperator 0 f = (f : SpectralHilbert) := by
  apply Lp.ext
  have h := continuous_modular_apply_ae 0 f
  filter_upwards [h] with x hx
  simpa using hx

#print axioms continuousModularOperator
#print axioms continuous_modular_domain_dense
#print axioms continuous_modular_closed
#print axioms continuous_modular_selfadjoint
#print axioms continuous_modular_positive
#print axioms continuous_modular_graph_iff
#print axioms continuous_modular_apply_ae
#print axioms continuous_modular_domain_iff
#print axioms continuous_weight_fiber_subsingleton
#print axioms continuous_weight_fiber_null
#print axioms continuous_modular_no_eigen
#print axioms continuous_modular_zero_graph
#print axioms continuous_modular_zero_domain
#print axioms continuous_modular_zero_apply

end
end ChatgptAudit.Continuous049
