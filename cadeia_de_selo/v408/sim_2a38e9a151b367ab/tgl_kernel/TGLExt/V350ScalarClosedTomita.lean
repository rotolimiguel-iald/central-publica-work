import TGLExt.V350ScalarGaussianClosureTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {P : SiteProfile}

local instance scalarStarCoreAdd : AddCommGroup (finiteDualStarCore P) :=
  (NonUnitalStarSubalgebra.toNonUnitalRing (finiteDualStarCore P)).toAddCommGroup

local instance scalarStarCoreSMul : SMul ℂ (finiteDualStarCore P) where
  smul c A := ⟨c • A.val, (finiteDualStarCore P).smul_mem c A.property⟩

theorem scalarGNSStarEmbedding_add (A B : finiteDualStarCore P) :
    scalarGNSStarEmbedding P (A+B) = scalarGNSStarEmbedding P A + scalarGNSStarEmbedding P B :=
  (scalarGNSEmbedding P).map_add ⟨A.val,A.property.1⟩ ⟨B.val,B.property.1⟩

theorem scalarGNSStarEmbedding_smul (c : ℂ) (A : finiteDualStarCore P) :
    scalarGNSStarEmbedding P (c • A : finiteDualStarCore P) = c • scalarGNSStarEmbedding P A :=
  (scalarGNSEmbedding P).map_smul c ⟨A.val,A.property.1⟩

theorem scalarTomitaGraph_zero : (0,0) ∈ scalarTomitaGraph P := by
  refine ⟨0,?_⟩
  change (scalarGNSStarEmbedding P 0,scalarGNSStarEmbedding P (star 0)) = (0,0)
  have hz : star (0 : finiteDualStarCore P) = 0 := by
    apply Subtype.ext
    exact star_zero _
  rw [hz]
  change (scalarGNSEmbedding P 0,scalarGNSEmbedding P 0) = (0,0)
  simp only [map_zero]

theorem scalarTomitaGraph_add {p q : ScalarGNSHilbert P × ScalarGNSHilbert P}
    (hp : p ∈ scalarTomitaGraph P) (hq : q ∈ scalarTomitaGraph P) :
    p+q ∈ scalarTomitaGraph P := by
  obtain ⟨A,rfl⟩ := hp
  obtain ⟨B,rfl⟩ := hq
  refine ⟨A+B,?_⟩
  have hs : star (A+B) = star A + star B := by
    apply Subtype.ext
    exact star_add A.val B.val
  simp only [hs,scalarGNSStarEmbedding_add,Prod.mk_add_mk]

theorem scalarTomitaGraph_conj_smul (c : ℂ)
    {p : ScalarGNSHilbert P × ScalarGNSHilbert P} (hp : p ∈ scalarTomitaGraph P) :
    (c • p.1,(starRingEnd ℂ c) • p.2) ∈ scalarTomitaGraph P := by
  obtain ⟨A,rfl⟩ := hp
  refine ⟨(c • A : finiteDualStarCore P),?_⟩
  have hs : star (c • A : finiteDualStarCore P) = star c • star A := by
    apply Subtype.ext
    exact star_smul c A.val
  simp only [hs,scalarGNSStarEmbedding_smul,starRingEnd_apply]

theorem scalarClosedGraph_add {p q : ScalarGNSHilbert P × ScalarGNSHilbert P}
    (hp : p ∈ closure (scalarTomitaGraph P)) (hq : q ∈ closure (scalarTomitaGraph P)) :
    p+q ∈ closure (scalarTomitaGraph P) := by
  have hleft : ∀ a ∈ scalarTomitaGraph P, ∀ b ∈ closure (scalarTomitaGraph P),
      a+b ∈ closure (scalarTomitaGraph P) := by
    intro a ha
    exact closure_minimal (fun b hb => subset_closure (scalarTomitaGraph_add ha hb))
      (isClosed_closure.preimage (continuous_const.add continuous_id))
  exact closure_minimal (fun a ha => hleft a ha q hq)
    (isClosed_closure.preimage (continuous_id.add continuous_const)) hp

theorem scalarClosedGraph_conj_smul (c : ℂ)
    {p : ScalarGNSHilbert P × ScalarGNSHilbert P} (hp : p ∈ closure (scalarTomitaGraph P)) :
    (c • p.1,(starRingEnd ℂ c) • p.2) ∈ closure (scalarTomitaGraph P) := by
  apply closure_minimal (t := {q : ScalarGNSHilbert P × ScalarGNSHilbert P |
    (c • q.1,(starRingEnd ℂ c) • q.2) ∈ closure (scalarTomitaGraph P)}) ?_ ?_ hp
  · intro q hq
    exact subset_closure (scalarTomitaGraph_conj_smul c hq)
  · apply isClosed_closure.preimage
    exact (continuous_fst.const_smul c).prodMk
      (continuous_snd.const_smul (starRingEnd ℂ c))

theorem scalarClosedGraph_swap {p : ScalarGNSHilbert P × ScalarGNSHilbert P}
    (hp : p ∈ closure (scalarTomitaGraph P)) : p.swap ∈ closure (scalarTomitaGraph P) := by
  apply closure_minimal (t := {q : ScalarGNSHilbert P × ScalarGNSHilbert P |
    q.swap ∈ closure (scalarTomitaGraph P)}) ?_ ?_ hp
  · intro q hq
    exact subset_closure (scalarTomitaGraph_swap P q hq)
  · exact isClosed_closure.preimage continuous_swap

/-- The actual domain of the closure, not the whole Hilbert space by declaration. -/
def scalarClosedTomitaDomain (P : SiteProfile) : Submodule ℂ (ScalarGNSHilbert P) where
  carrier := {x | ∃ y, (x,y) ∈ closure (scalarTomitaGraph P)}
  zero_mem' := ⟨0,subset_closure scalarTomitaGraph_zero⟩
  add_mem' := by
    rintro x z ⟨y,hy⟩ ⟨w,hw⟩
    exact ⟨y+w,scalarClosedGraph_add hy hw⟩
  smul_mem' := by
    rintro c x ⟨y,hy⟩
    exact ⟨(starRingEnd ℂ c) • y,scalarClosedGraph_conj_smul c hy⟩

def scalarClosedTomitaValue (x : scalarClosedTomitaDomain P) : ScalarGNSHilbert P :=
  Classical.choose x.property

theorem scalarClosedTomitaValue_graph (x : scalarClosedTomitaDomain P) :
    ((x : ScalarGNSHilbert P),scalarClosedTomitaValue x) ∈ closure (scalarTomitaGraph P) :=
  Classical.choose_spec x.property

/-- The closed antilinear operator associated with the original finite-star-core
graph. No identification with the maximal scalar-weight domain is asserted. -/
def scalarClosedTomita (P : SiteProfile) :
    scalarClosedTomitaDomain P →ₛₗ[starRingEnd ℂ] ScalarGNSHilbert P where
  toFun := scalarClosedTomitaValue
  map_add' x z := by
    apply scalarTomitaGraph_closure_single_valued P ((x+z : scalarClosedTomitaDomain P) : ScalarGNSHilbert P)
    · exact scalarClosedTomitaValue_graph (x+z)
    · exact scalarClosedGraph_add (scalarClosedTomitaValue_graph x) (scalarClosedTomitaValue_graph z)
  map_smul' c x := by
    apply scalarTomitaGraph_closure_single_valued P ((c • x : scalarClosedTomitaDomain P) : ScalarGNSHilbert P)
    · exact scalarClosedTomitaValue_graph (c • x)
    · exact scalarClosedGraph_conj_smul c (scalarClosedTomitaValue_graph x)

theorem scalarClosedTomita_graph (x : scalarClosedTomitaDomain P) :
    ((x : ScalarGNSHilbert P),scalarClosedTomita P x) ∈ closure (scalarTomitaGraph P) :=
  scalarClosedTomitaValue_graph x

theorem scalarClosedTomita_graph_eq :
    Set.range (fun x : scalarClosedTomitaDomain P =>
      ((x : ScalarGNSHilbert P),scalarClosedTomita P x)) = closure (scalarTomitaGraph P) := by
  ext p
  constructor
  · rintro ⟨x,rfl⟩
    exact scalarClosedTomita_graph x
  · intro hp
    let x : scalarClosedTomitaDomain P := ⟨p.1,p.2,hp⟩
    refine ⟨x,?_⟩
    apply Prod.ext
    · rfl
    · exact scalarTomitaGraph_closure_single_valued P p.1 _ p.2 (scalarClosedTomita_graph x) hp

theorem scalarClosedTomita_is_closed :
    IsClosed (Set.range (fun x : scalarClosedTomitaDomain P =>
      ((x : ScalarGNSHilbert P),scalarClosedTomita P x))) := by
  rw [scalarClosedTomita_graph_eq]
  exact isClosed_closure

theorem scalarClosedTomita_domain_dense :
    Dense (scalarClosedTomitaDomain P : Set (ScalarGNSHilbert P)) := by
  apply Dense.mono ?_ (scalarTomitaGraph_domain_dense P)
  rintro x ⟨p,hp,rfl⟩
  exact ⟨p.2,subset_closure hp⟩

theorem scalarClosedTomita_maps_domain (x : scalarClosedTomitaDomain P) :
    scalarClosedTomita P x ∈ scalarClosedTomitaDomain P :=
  ⟨(x : ScalarGNSHilbert P),scalarClosedGraph_swap (scalarClosedTomita_graph x)⟩

theorem scalarClosedTomita_involutive (x : scalarClosedTomitaDomain P) :
    scalarClosedTomita P ⟨scalarClosedTomita P x,scalarClosedTomita_maps_domain x⟩ = x :=
  scalarTomitaGraph_closure_single_valued P (scalarClosedTomita P x) _ _
    (scalarClosedTomita_graph ⟨scalarClosedTomita P x,scalarClosedTomita_maps_domain x⟩)
    (scalarClosedGraph_swap (scalarClosedTomita_graph x))

theorem scalarStarCore_mem_closedTomitaDomain (A : finiteDualStarCore P) :
    scalarGNSStarEmbedding P A ∈ scalarClosedTomitaDomain P :=
  ⟨scalarGNSStarEmbedding P (star A),subset_closure ⟨A,rfl⟩⟩

theorem scalarClosedTomita_extends_star (A : finiteDualStarCore P) :
    scalarClosedTomita P ⟨scalarGNSStarEmbedding P A,scalarStarCore_mem_closedTomitaDomain A⟩ =
      scalarGNSStarEmbedding P (star A) :=
  scalarTomitaGraph_closure_single_valued P (scalarGNSStarEmbedding P A) _ _
    (scalarClosedTomita_graph ⟨scalarGNSStarEmbedding P A,scalarStarCore_mem_closedTomitaDomain A⟩)
    (subset_closure ⟨A,rfl⟩)

#print axioms scalarGNSStarEmbedding_add
#print axioms scalarGNSStarEmbedding_smul
#print axioms scalarTomitaGraph_zero
#print axioms scalarTomitaGraph_add
#print axioms scalarTomitaGraph_conj_smul
#print axioms scalarClosedGraph_add
#print axioms scalarClosedGraph_conj_smul
#print axioms scalarClosedGraph_swap
#print axioms scalarClosedTomitaDomain
#print axioms scalarClosedTomitaValue
#print axioms scalarClosedTomitaValue_graph
#print axioms scalarClosedTomita
#print axioms scalarClosedTomita_graph
#print axioms scalarClosedTomita_graph_eq
#print axioms scalarClosedTomita_is_closed
#print axioms scalarClosedTomita_domain_dense
#print axioms scalarClosedTomita_maps_domain
#print axioms scalarClosedTomita_involutive
#print axioms scalarStarCore_mem_closedTomitaDomain
#print axioms scalarClosedTomita_extends_star
end
end TGLV350.Regular
