import BoundedGraphStandardSubspace
import ContinuousModularDomain

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Continuous049
open Complex ClosedSubmodule MeasureTheory Filter
noncomputable section

/-- The concrete densely defined anti-linear Tomita map. -/
def continuousModularTomita (c : ℝ) :
    (continuousModularOperator c).domain →ₛₗ[starRingEnd ℂ] SpectralHilbert :=
  boundedGraphTomita (spectralA c) (spectralB c) (spectralA_injective c) spectralJ

/-- A standard real subspace of Lebesgue L² built from explicit multipliers. -/
def continuousStandardSubspace (c : ℝ) : StandardSubspace SpectralHilbert :=
  boundedGraphStandardSubspace (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralA_selfadjoint c) (spectralAB_commute c) (spectralAB_square_sum c)
    spectralJ spectralJ_involutive (spectralJB_eq_AJ c)

theorem continuous_tomita_domain_dense (c : ℝ) :
    Dense ((continuousModularOperator c).domain : Set SpectralHilbert) :=
  bounded_graph_domain_dense (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralA_selfadjoint c)

theorem continuous_tomita_closed (c : ℝ) :
    IsClosed (Set.range (fun f : (continuousModularOperator c).domain =>
      ((f : SpectralHilbert), continuousModularTomita c f))) :=
  bounded_graph_tomita_closed (spectralA c) (spectralB c) (spectralA_injective c)
    (spectralAB_commute c) (spectralAB_square_sum c) spectralJ spectralJ_involutive

theorem continuous_tomita_maps_domain (c : ℝ) (f : (continuousModularOperator c).domain) :
    continuousModularTomita c f ∈ (continuousModularOperator c).domain :=
  bounded_graph_tomita_maps_domain (spectralA c) (spectralB c) (spectralA_injective c)
    spectralJ (spectralJB_eq_AJ c) f

theorem continuous_tomita_involutive (c : ℝ) (f : (continuousModularOperator c).domain) :
    continuousModularTomita c
      ⟨continuousModularTomita c f, continuous_tomita_maps_domain c f⟩ = (f : SpectralHilbert) :=
  bounded_graph_tomita_involutive (spectralA c) (spectralB c) (spectralA_injective c)
    spectralJ spectralJ_involutive (spectralJB_eq_AJ c) f

theorem continuous_J_tomita_eq_modular (c : ℝ) (f : (continuousModularOperator c).domain) :
    spectralJ (continuousModularTomita c f) = continuousModularOperator c f :=
  bounded_graph_J_tomita (spectralA c) (spectralB c) (spectralA_injective c)
    spectralJ spectralJ_involutive f

theorem continuous_standard_fixed_iff (c : ℝ) (f : SpectralHilbert) :
    f ∈ (continuousStandardSubspace c).toClosedSubmodule ↔
      ∃ hf : f ∈ (continuousModularOperator c).domain,
        continuousModularTomita c ⟨f, hf⟩ = f := Iff.rfl

theorem continuous_domain_iff_standard_sum (c : ℝ) (f : SpectralHilbert) :
    f ∈ (continuousModularOperator c).domain ↔
      ∃ h k : SpectralHilbert,
        h ∈ (continuousStandardSubspace c).toClosedSubmodule ∧
        k ∈ (continuousStandardSubspace c).toClosedSubmodule ∧ f = h + I • k :=
  mem_domain_iff_fixed_sum (continuousModularOperator c).domain (continuousModularTomita c)
    (continuous_tomita_maps_domain c) (continuous_tomita_involutive c) f

theorem continuous_tomita_decomposition (c : ℝ) (f : (continuousModularOperator c).domain) :
    ∃ h k : SpectralHilbert,
      h ∈ (continuousStandardSubspace c).toClosedSubmodule ∧
      k ∈ (continuousStandardSubspace c).toClosedSubmodule ∧
      (f : SpectralHilbert) = h + I • k ∧ continuousModularTomita c f = h - I • k :=
  domain_fixed_decomposition (continuousModularOperator c).domain (continuousModularTomita c)
    (continuous_tomita_maps_domain c) (continuous_tomita_involutive c) f

/-- The Tomita map is explicit almost everywhere on its weighted L² domain. -/
theorem continuous_tomita_apply_ae (c : ℝ) (f : (continuousModularOperator c).domain) :
    continuousModularTomita c f =ᵐ[volume]
      fun x => (Real.exp (c * x) : ℂ) * star ((f : SpectralHilbert) (-x)) := by
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (continuous_modular_apply_ae c f)
  filter_upwards [spectralJ_ae (continuousModularOperator c f), hr] with x hx hy
  change (spectralJ (continuousModularOperator c f)) x =
    (Real.exp (c * x) : ℂ) * star ((f : SpectralHilbert) (-x))
  rw [hx]
  simpa only [star_mul, Complex.star_def, Complex.conj_ofReal, neg_mul_neg]
    using congrArg star hy

theorem continuous_tomita_zero_apply (f : (continuousModularOperator 0).domain) :
    continuousModularTomita 0 f = spectralJ (f : SpectralHilbert) :=
  congrArg spectralJ (continuous_modular_zero_apply f)

#print axioms continuousModularTomita
#print axioms continuousStandardSubspace
#print axioms continuous_tomita_domain_dense
#print axioms continuous_tomita_closed
#print axioms continuous_tomita_maps_domain
#print axioms continuous_tomita_involutive
#print axioms continuous_J_tomita_eq_modular
#print axioms continuous_standard_fixed_iff
#print axioms continuous_domain_iff_standard_sum
#print axioms continuous_tomita_decomposition
#print axioms continuous_tomita_apply_ae
#print axioms continuous_tomita_zero_apply

end
end ChatgptAudit.Continuous049
