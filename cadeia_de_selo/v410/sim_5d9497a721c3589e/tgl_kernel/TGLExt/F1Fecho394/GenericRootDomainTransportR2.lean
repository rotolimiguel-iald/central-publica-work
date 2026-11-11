import TGLExt.V350ResolventGraphTransport

/-! Full-domain consequences of the proved square-root graph transport.
Keeping the Hilbert space abstract avoids re-elaborating the concrete Fock
subtype inside existential graph decompositions. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericRootDomainTransport
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (R U : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R) (hc : Commute R U)

include hc

theorem graph_map (x : (resolventSquareRoot R hR hi).domain) :
    (U x,U (resolventSquareRoot R hR hi x)) ∈ (resolventSquareRoot R hR hi).graph :=
  resolvent_sqrt_graph_transport_of_commute R U hR hi hc _ _
    ((LinearPMap.mem_graph_iff _).mpr ⟨x,rfl,rfl⟩)

theorem domain_map (x : (resolventSquareRoot R hR hi).domain) :
    U x ∈ (resolventSquareRoot R hR hi).domain := by
  obtain ⟨y,hy,_⟩ := (LinearPMap.mem_graph_iff _).mp (graph_map R U hR hi hc x)
  change (y:H) = U x at hy
  exact hy ▸ y.property

def mappedInput (x : (resolventSquareRoot R hR hi).domain) :
    (resolventSquareRoot R hR hi).domain := ⟨U x,domain_map R U hR hi hc x⟩

theorem root_map (x : (resolventSquareRoot R hR hi).domain) :
    resolventSquareRoot R hR hi (mappedInput R U hR hi hc x) =
      U (resolventSquareRoot R hR hi x) := by
  obtain ⟨y,hy,he⟩ := (LinearPMap.mem_graph_iff _).mp (graph_map R U hR hi hc x)
  have hy' : mappedInput R U hR hi hc x = y := Subtype.ext hy.symm
  exact (congrArg (resolventSquareRoot R hR hi) hy').trans he

theorem domain_inverse_iff (V : H →L[ℂ] H) (hv : Commute R V)
    (hvu : ∀ x, V (U x) = x) (x : H) :
    U x ∈ (resolventSquareRoot R hR hi).domain ↔ x ∈ (resolventSquareRoot R hR hi).domain := by
  constructor
  · intro hx
    have h := domain_map R V hR hi hv ⟨U x,hx⟩
    change V (U x) ∈ _ at h
    simpa only [hvu] using h
  · intro hx
    exact domain_map R U hR hi hc ⟨x,hx⟩

end F1Fecho.GenericRootDomainTransport
#print axioms F1Fecho.GenericRootDomainTransport.graph_map
#print axioms F1Fecho.GenericRootDomainTransport.domain_map
#print axioms F1Fecho.GenericRootDomainTransport.root_map
#print axioms F1Fecho.GenericRootDomainTransport.domain_inverse_iff
