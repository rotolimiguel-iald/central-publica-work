import TGLExt.F1Fecho394.WeylFiniteAlgebraR4
import TGLExt.F1Fecho394.BicommutantStarGraphR1
/-! Equality of the actual algebra/vacuum Tomita graph with the concrete
exponential Tomita graph on the same canonical Fock space. The reverse inclusion
uses proved two-vector bicommutant density and real graph separation. No graph
core or strong-star density is supplied as an additional hypothesis. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.ExponentialTomitaEquality
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.ExponentialLift F1Fecho.ExponentialTomita F1Fecho.ExponentialTomitaInclusion
open F1Fecho.WeylExponentialCore F1Fecho.WeylFiniteAlgebra F1Fecho.WedgePairTomita

theorem algebra_pair_mem_Sexp (a : F →L[ℂ] F) (ha : a ∈ FieldWeyl.R K) :
    (a vacuum,(star a) vacuum) ∈
      Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) := by
  have h := StarGraphDensity.star_pair_mem_set_closure_of_bicommutant finiteAlgebra a vacuum
    (R_bicommutant_finite a ha)
  apply (closure_minimal (t := Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)))
    ?_ Sexp_closed) h
  rintro p ⟨b,hb,rfl⟩
  exact finite_algebra_graph b hb

theorem pair_graph_subset_Sexp_graph :
    Set.range (fun x : domain KWR => ((x:F),S KWR x)) ⊆
      Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) := by
  rw [graph_eq]
  apply closure_minimal _ Sexp_closed
  rintro p ⟨a,ha,rfl⟩
  exact algebra_pair_mem_Sexp a ha

theorem tomita_graph_eq :
    Set.range (fun x : domain KWR => ((x:F),S KWR x)) =
      Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) :=
  Set.Subset.antisymm pair_graph_subset_Sexp_graph Sexp_graph_subset_pair_graph

theorem tomita_domain_eq : domain KWR = canonicalLift.domain := by
  apply le_antisymm
  · intro x hx
    have h : (x,S KWR ⟨x,hx⟩) ∈
        Set.range (fun z : domain KWR => ((z:F),S KWR z)) := ⟨⟨x,hx⟩,rfl⟩
    rw [tomita_graph_eq] at h
    obtain ⟨z,hz⟩ := h
    have he : (z:F)=x := congrArg Prod.fst hz
    exact he ▸ z.property
  · intro x hx
    exact Sexp_domain_inclusion ⟨x,hx⟩

theorem tomita_action_eq (x : domain KWR) :
    S KWR x = Sexp ⟨(x:F),tomita_domain_eq ▸ x.property⟩ := by
  exact Sexp_eq_pair_on_domain ⟨(x:F),tomita_domain_eq ▸ x.property⟩

end F1Fecho.ExponentialTomitaEquality
#print axioms F1Fecho.ExponentialTomitaEquality.algebra_pair_mem_Sexp
#print axioms F1Fecho.ExponentialTomitaEquality.pair_graph_subset_Sexp_graph
#print axioms F1Fecho.ExponentialTomitaEquality.tomita_graph_eq
#print axioms F1Fecho.ExponentialTomitaEquality.tomita_domain_eq
#print axioms F1Fecho.ExponentialTomitaEquality.tomita_action_eq
