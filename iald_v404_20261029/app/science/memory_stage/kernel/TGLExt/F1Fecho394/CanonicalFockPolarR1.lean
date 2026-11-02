import TGLExt.F1Fecho394.GammaGraphParametersR3
import TGLExt.F1Fecho394.BoundedGraphSelfAdjointR4
import TGLExt.F1Fecho394.ExponentialTomitaEqualityR4
import TGLExt.F1Fecho394.ExponentialLiftPositiveR2
import TGLExt.F1Fecho394.PartialSquareGraphR2
/-! Concrete positive selfadjoint factor of the ACTUAL Weyl/vacuum Tomita
operator, on the unchanged Fock. The bounded graph parameters are constructed,
not fields. The maximal antilinear adjoint and exact S†S graph are identified.
No spectral imaginary-power identity or new KMS analytic-strip theorem is
asserted in this module. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.CanonicalFockPolar
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.ExponentialLift F1Fecho.ExponentialTomita F1Fecho.Antilinear
open F1Fecho.ExponentialTomitaEquality F1Fecho.ExponentialTomitaInclusion
open F1Fecho.GammaGraph F1Fecho.WedgePairTomita
open ChatgptAudit.Continuous050

theorem canonicalLift_selfadjoint : IsSelfAdjoint canonicalLift :=
  BoundedGraphSelfAdjoint.selfAdjoint_of_bounded_pair canonicalLift
    canonicalLift_closed (closedLift_isFormalAdjoint TW TW_selfadjoint)
    canonicalLift_dense GA GB GA_selfadjoint GB_selfadjoint GAB_commute GA_injective graph_parameters

theorem actual_tomita_polar (x : domain KWR) :
    S KWR x = JF (canonicalLift ⟨(x:F),tomita_domain_eq ▸ x.property⟩) :=
  tomita_action_eq x

theorem positive_polar_factor :
    IsSelfAdjoint canonicalLift ∧
      (∀ x : canonicalLift.domain, 0 ≤ (inner ℂ (x:F) (canonicalLift x)).re) ∧
      (∀ x : domain KWR,
        S KWR x = JF (canonicalLift ⟨(x:F),tomita_domain_eq ▸ x.property⟩)) :=
  ⟨canonicalLift_selfadjoint,ExponentialLiftPositive.canonicalLift_positive,actual_tomita_polar⟩

def Sdagger : F →ₛₗ.[starRingEnd ℂ] F := genericTomitaAdjoint canonicalLift JF

theorem actual_adjoint_pairing (x : domain KWR) (y : Sdagger.domain) :
    inner ℂ (S KWR x) (y:F) = inner ℂ (Sdagger y) (x:F) := by
  rw [tomita_action_eq]
  exact generic_adjoint_pairing canonicalLift canonicalLift_selfadjoint JF
    canonicalFockJ_involutive ⟨(x:F),tomita_domain_eq ▸ x.property⟩ y

theorem actual_adjoint_maximal {y z : F}
    (h : ∀ x : domain KWR, inner ℂ (S KWR x) y = inner ℂ z (x:F)) :
    ∃ hy : y ∈ Sdagger.domain, Sdagger ⟨y,hy⟩ = z := by
  apply generic_adjoint_maximal canonicalLift canonicalLift_selfadjoint JF canonicalFockJ_involutive
  intro x
  have hx := h ⟨(x:F),Sexp_domain_inclusion x⟩
  rw [Sexp_eq_pair_on_domain] at hx
  exact hx

theorem actual_adjoint_domain_iff (y : F) :
    y ∈ Sdagger.domain ↔ ∃ z : F,
      ∀ x : domain KWR, inner ℂ (S KWR x) y = inner ℂ z (x:F) := by
  constructor
  · intro hy
    exact ⟨Sdagger ⟨y,hy⟩,fun x => actual_adjoint_pairing x ⟨y,hy⟩⟩
  · rintro ⟨z,hz⟩
    exact (actual_adjoint_maximal hz).choose

/-- S†S, with the exact two-application domain, defined as G squared. -/
def Delta : F →ₗ.[ℂ] F := PartialSquare.square canonicalLift

theorem delta_graph_iff_tomita_comp (x y : F) :
    (x,y) ∈ Delta.graph ↔
      ∃ hx : x ∈ canonicalLift.domain,
        ∃ hSx : Sexp ⟨x,hx⟩ ∈ Sdagger.domain,
          Sdagger ⟨Sexp ⟨x,hx⟩,hSx⟩ = y :=
  PartialSquare.square_graph_iff_tomita_comp canonicalLift JF canonicalFockJ_involutive x y

theorem delta_energy (x : Delta.domain) :
    (inner ℂ (x:F) (Delta x)).re = ‖canonicalLift ⟨x,x.property.choose⟩‖^2 :=
  PartialSquare.square_energy canonicalLift (closedLift_isFormalAdjoint TW TW_selfadjoint) x

theorem delta_positive (x : Delta.domain) : 0 ≤ (inner ℂ (x:F) (Delta x)).re := by
  rw [delta_energy]
  exact sq_nonneg _

end F1Fecho.CanonicalFockPolar
#print axioms F1Fecho.CanonicalFockPolar.canonicalLift_selfadjoint
#print axioms F1Fecho.CanonicalFockPolar.actual_tomita_polar
#print axioms F1Fecho.CanonicalFockPolar.positive_polar_factor
#print axioms F1Fecho.CanonicalFockPolar.actual_adjoint_pairing
#print axioms F1Fecho.CanonicalFockPolar.actual_adjoint_maximal
#print axioms F1Fecho.CanonicalFockPolar.actual_adjoint_domain_iff
#print axioms F1Fecho.CanonicalFockPolar.delta_graph_iff_tomita_comp
#print axioms F1Fecho.CanonicalFockPolar.delta_energy
#print axioms F1Fecho.CanonicalFockPolar.delta_positive
