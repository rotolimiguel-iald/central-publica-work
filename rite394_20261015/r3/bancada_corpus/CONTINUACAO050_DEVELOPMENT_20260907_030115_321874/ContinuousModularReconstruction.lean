import GenericAntilinearAdjoint
import ContinuousModularSquare
import ContinuousModularStandardSubspace

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Continuous050
open ChatgptAudit.Continuous049
noncomputable section

/-- The generic construction is the already constructed concrete Tomita operator. -/
theorem continuous_tomita_eq_generic (c : ℝ) (x : (continuousModularOperator c).domain) :
    continuousModularTomita c x =
      genericTomita (continuousModularOperator c) spectralJ x := rfl

def continuousTomitaAdjoint (c : ℝ) : SpectralHilbert →ₛₗ.[starRingEnd ℂ] SpectralHilbert :=
  genericTomitaAdjoint (continuousModularOperator c) spectralJ

theorem continuous_tomita_adjoint_pairing (c : ℝ)
    (x : (continuousModularOperator c).domain) (y : (continuousTomitaAdjoint c).domain) :
    inner ℂ (continuousModularTomita c x) (y : SpectralHilbert) =
      inner ℂ (continuousTomitaAdjoint c y) (x : SpectralHilbert) :=
  generic_adjoint_pairing (continuousModularOperator c) (continuous_modular_selfadjoint c)
    spectralJ spectralJ_involutive x y

theorem continuous_tomita_adjoint_maximal (c : ℝ) {y z : SpectralHilbert}
    (h : ∀ x : (continuousModularOperator c).domain,
      inner ℂ (continuousModularTomita c x) y = inner ℂ z (x : SpectralHilbert)) :
    ∃ hy : y ∈ (continuousTomitaAdjoint c).domain,
      continuousTomitaAdjoint c ⟨y, hy⟩ = z :=
  generic_adjoint_maximal (continuousModularOperator c) (continuous_modular_selfadjoint c)
    spectralJ spectralJ_involutive h

theorem continuous_tomita_adjoint_domain_iff (c : ℝ) (y : SpectralHilbert) :
    y ∈ (continuousTomitaAdjoint c).domain ↔
      ∃ z : SpectralHilbert, ∀ x : (continuousModularOperator c).domain,
        inner ℂ (continuousModularTomita c x) y = inner ℂ z (x : SpectralHilbert) :=
  generic_adjoint_domain_iff (continuousModularOperator c) (continuous_modular_selfadjoint c)
    spectralJ spectralJ_involutive y

theorem continuous_tomita_composition_domain (c : ℝ)
    (x : (continuousModularOperator c).domain) :
    continuousModularTomita c x ∈ (continuousTomitaAdjoint c).domain ↔
      continuousModularOperator c x ∈ (continuousModularOperator c).domain :=
  generic_composition_domain (continuousModularOperator c) spectralJ spectralJ_involutive x

theorem continuous_tomita_adjoint_comp (c : ℝ)
    (x : (continuousModularOperator c).domain)
    (hx : continuousModularOperator c x ∈ (continuousModularOperator c).domain) :
    continuousTomitaAdjoint c
      ⟨continuousModularTomita c x, (continuous_tomita_composition_domain c x).mpr hx⟩ =
        continuousModularOperator c ⟨continuousModularOperator c x, hx⟩ :=
  generic_adjoint_comp (continuousModularOperator c) spectralJ spectralJ_involutive x hx

/-- The full graph characterization below identifies this operator as S†S. -/
def continuousModularDelta (c : ℝ) : SpectralHilbert →ₗ.[ℂ] SpectralHilbert :=
  continuousModularSquare c

theorem continuous_delta_graph_iff_tomita_comp (c : ℝ) (f g : SpectralHilbert) :
    (f, g) ∈ (continuousModularDelta c).graph ↔
      ∃ hf : f ∈ (continuousModularOperator c).domain,
        ∃ hSf : continuousModularTomita c ⟨f, hf⟩ ∈ (continuousTomitaAdjoint c).domain,
          continuousTomitaAdjoint c ⟨continuousModularTomita c ⟨f, hf⟩, hSf⟩ = g := by
  rw [LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨x, hx, hy⟩
    dsimp only [Prod.fst, Prod.snd] at hx hy
    subst f
    have hSf := (continuous_tomita_composition_domain c
      ⟨(x : SpectralHilbert), x.property.choose⟩).mpr x.property.choose_spec
    refine ⟨x.property.choose, hSf, ?_⟩
    rw [continuous_tomita_adjoint_comp]
    exact hy
  · rintro ⟨hf, hSf, hg⟩
    have hTf := (continuous_tomita_composition_domain c ⟨f, hf⟩).mp hSf
    let x : (continuousModularDelta c).domain := ⟨f, ⟨hf, hTf⟩⟩
    refine ⟨x, rfl, ?_⟩
    change continuousModularOperator c ⟨continuousModularOperator c ⟨f, hf⟩, hTf⟩ = g
    rw [← continuous_tomita_adjoint_comp c ⟨f, hf⟩ hTf]
    exact hg

theorem continuous_delta_eq_double (c : ℝ) :
    continuousModularDelta c = continuousModularOperator (2*c) :=
  continuous_modular_square_eq c

theorem continuous_delta_domain_iff (c : ℝ) (f : SpectralHilbert) :
    f ∈ (continuousModularDelta c).domain ↔
      ∃ hf : f ∈ (continuousModularOperator c).domain,
        continuousModularTomita c ⟨f, hf⟩ ∈ (continuousTomitaAdjoint c).domain := by
  change (∃ hf : f ∈ (continuousModularOperator c).domain,
    continuousModularOperator c ⟨f, hf⟩ ∈ (continuousModularOperator c).domain) ↔ _
  exact exists_congr (fun hf => (continuous_tomita_composition_domain c ⟨f, hf⟩).symm)

theorem continuous_delta_selfadjoint (c : ℝ) : IsSelfAdjoint (continuousModularDelta c) :=
  continuous_modular_square_selfadjoint c

theorem continuous_delta_closed (c : ℝ) : (continuousModularDelta c).IsClosed :=
  continuous_modular_square_closed c

theorem continuous_delta_energy (c : ℝ) (x : (continuousModularDelta c).domain) :
    (inner ℂ (continuousModularDelta c x) (x : SpectralHilbert)).re =
      ‖continuousModularTomita c ⟨(x : SpectralHilbert), x.property.choose⟩‖ ^ 2 := by
  let u : (continuousModularOperator c).domain := ⟨x, x.property.choose⟩
  have hu : continuousModularOperator c u ∈ (continuousModularOperator c).domain :=
    x.property.choose_spec
  have h := continuous_tomita_adjoint_pairing c u
    ⟨continuousModularTomita c u, (continuous_tomita_composition_domain c u).mpr hu⟩
  rw [continuous_tomita_adjoint_comp] at h
  change (inner ℂ (continuousModularOperator c
    ⟨continuousModularOperator c u, hu⟩) (u : SpectralHilbert)).re = _
  rw [← h]
  exact (norm_sq_eq_re_inner (𝕜 := ℂ) (continuousModularTomita c u)).symm

theorem continuous_delta_positive (c : ℝ) (x : (continuousModularDelta c).domain) :
    0 ≤ (inner ℂ (x : SpectralHilbert) (continuousModularDelta c x)).re := by
  have h := continuous_delta_energy c x
  rw [← inner_conj_symm (𝕜 := ℂ) (x : SpectralHilbert) (continuousModularDelta c x)]
  change 0 ≤ (inner ℂ (continuousModularDelta c x) (x : SpectralHilbert)).re
  rw [h]
  exact sq_nonneg _

/-- A positive self-adjoint square root, with its exact composition domain proved above. -/
theorem continuous_modular_positive_square_root (c : ℝ) :
    IsSelfAdjoint (continuousModularOperator c) ∧
      (∀ x : (continuousModularOperator c).domain,
        0 ≤ (inner ℂ (x : SpectralHilbert) (continuousModularOperator c x)).re) ∧
      continuousModularSquare c = continuousModularDelta c :=
  ⟨continuous_modular_selfadjoint c, continuous_modular_positive c, rfl⟩

#print axioms continuous_tomita_eq_generic
#print axioms continuousTomitaAdjoint
#print axioms continuous_tomita_adjoint_pairing
#print axioms continuous_tomita_adjoint_maximal
#print axioms continuous_tomita_adjoint_domain_iff
#print axioms continuous_tomita_composition_domain
#print axioms continuous_tomita_adjoint_comp
#print axioms continuousModularDelta
#print axioms continuous_delta_graph_iff_tomita_comp
#print axioms continuous_delta_eq_double
#print axioms continuous_delta_domain_iff
#print axioms continuous_delta_selfadjoint
#print axioms continuous_delta_closed
#print axioms continuous_delta_energy
#print axioms continuous_delta_positive
#print axioms continuous_modular_positive_square_root

end
end ChatgptAudit.Continuous050
