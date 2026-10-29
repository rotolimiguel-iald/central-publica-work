import TGLExt.F1Fecho394.RegularScalarTomitaClosureR2
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.RegularScalarClosedTomita
open TGLExt TGLV350.Regular F1Fecho.RegularScalarGNS
open F1Fecho.RegularScalarTomitaGraph F1Fecho.RegularScalarTomitaClosure
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable {D : Context H}

local instance scalarStarCoreAdd : AddCommGroup (finiteStarCore D) :=
  (NonUnitalStarSubalgebra.toNonUnitalRing (finiteStarCore D)).toAddCommGroup

local instance scalarStarCoreSMul : SMul ℂ (finiteStarCore D) where
  smul c A := ⟨c • A.val, (finiteStarCore D).smul_mem c A.property⟩

theorem scalarGNSStarEmbedding_add (A B : finiteStarCore D) :
    scalarGNSStarEmbedding D (A+B) = scalarGNSStarEmbedding D A + scalarGNSStarEmbedding D B :=
  (GNSEmbedding D).map_add ⟨A.val,A.property.1⟩ ⟨B.val,B.property.1⟩

theorem scalarGNSStarEmbedding_smul (c : ℂ) (A : finiteStarCore D) :
    scalarGNSStarEmbedding D (c • A : finiteStarCore D) = c • scalarGNSStarEmbedding D A :=
  (GNSEmbedding D).map_smul c ⟨A.val,A.property.1⟩

theorem scalarTomitaGraph_zero : (0,0) ∈ scalarTomitaGraph D := by
  refine ⟨0,?_⟩
  change (scalarGNSStarEmbedding D 0,scalarGNSStarEmbedding D (star 0)) = (0,0)
  have hz : star (0 : finiteStarCore D) = 0 := by
    apply Subtype.ext
    exact star_zero _
  rw [hz]
  change (GNSEmbedding D 0,GNSEmbedding D 0) = (0,0)
  simp only [map_zero]

theorem scalarTomitaGraph_add {p q : GNSHilbert D × GNSHilbert D}
    (hp : p ∈ scalarTomitaGraph D) (hq : q ∈ scalarTomitaGraph D) :
    p+q ∈ scalarTomitaGraph D := by
  obtain ⟨A,rfl⟩ := hp
  obtain ⟨B,rfl⟩ := hq
  refine ⟨A+B,?_⟩
  have hs : star (A+B) = star A + star B := by
    apply Subtype.ext
    exact star_add A.val B.val
  simp only [hs,scalarGNSStarEmbedding_add,Prod.mk_add_mk]

theorem scalarTomitaGraph_conj_smul (c : ℂ)
    {p : GNSHilbert D × GNSHilbert D} (hp : p ∈ scalarTomitaGraph D) :
    (c • p.1,(starRingEnd ℂ c) • p.2) ∈ scalarTomitaGraph D := by
  obtain ⟨A,rfl⟩ := hp
  refine ⟨(c • A : finiteStarCore D),?_⟩
  have hs : star (c • A : finiteStarCore D) = star c • star A := by
    apply Subtype.ext
    exact star_smul c A.val
  simp only [hs,scalarGNSStarEmbedding_smul,starRingEnd_apply]

theorem scalarClosedGraph_add {p q : GNSHilbert D × GNSHilbert D}
    (hp : p ∈ closure (scalarTomitaGraph D)) (hq : q ∈ closure (scalarTomitaGraph D)) :
    p+q ∈ closure (scalarTomitaGraph D) := by
  have hleft : ∀ a ∈ scalarTomitaGraph D, ∀ b ∈ closure (scalarTomitaGraph D),
      a+b ∈ closure (scalarTomitaGraph D) := by
    intro a ha
    exact closure_minimal (fun b hb => subset_closure (scalarTomitaGraph_add ha hb))
      (isClosed_closure.preimage (continuous_const.add continuous_id))
  exact closure_minimal (fun a ha => hleft a ha q hq)
    (isClosed_closure.preimage (continuous_id.add continuous_const)) hp

theorem scalarClosedGraph_conj_smul (c : ℂ)
    {p : GNSHilbert D × GNSHilbert D} (hp : p ∈ closure (scalarTomitaGraph D)) :
    (c • p.1,(starRingEnd ℂ c) • p.2) ∈ closure (scalarTomitaGraph D) := by
  apply closure_minimal (t := {q : GNSHilbert D × GNSHilbert D |
    (c • q.1,(starRingEnd ℂ c) • q.2) ∈ closure (scalarTomitaGraph D)}) ?_ ?_ hp
  · intro q hq
    exact subset_closure (scalarTomitaGraph_conj_smul c hq)
  · apply isClosed_closure.preimage
    exact (continuous_fst.const_smul c).prodMk
      (continuous_snd.const_smul (starRingEnd ℂ c))

theorem scalarClosedGraph_swap {p : GNSHilbert D × GNSHilbert D}
    (hp : p ∈ closure (scalarTomitaGraph D)) : p.swap ∈ closure (scalarTomitaGraph D) := by
  apply closure_minimal (t := {q : GNSHilbert D × GNSHilbert D |
    q.swap ∈ closure (scalarTomitaGraph D)}) ?_ ?_ hp
  · intro q hq
    exact subset_closure (scalarTomitaGraph_swap D q hq)
  · exact isClosed_closure.preimage continuous_swap

/-- The actual domain of the closure, not the whole Hilbert space by declaration. -/
def scalarClosedTomitaDomain (D : Context H) : Submodule ℂ (GNSHilbert D) where
  carrier := {x | ∃ y, (x,y) ∈ closure (scalarTomitaGraph D)}
  zero_mem' := ⟨0,subset_closure scalarTomitaGraph_zero⟩
  add_mem' := by
    rintro x z ⟨y,hy⟩ ⟨w,hw⟩
    exact ⟨y+w,scalarClosedGraph_add hy hw⟩
  smul_mem' := by
    rintro c x ⟨y,hy⟩
    exact ⟨(starRingEnd ℂ c) • y,scalarClosedGraph_conj_smul c hy⟩

def scalarClosedTomitaValue (x : scalarClosedTomitaDomain D) : GNSHilbert D :=
  Classical.choose x.property

theorem scalarClosedTomitaValue_graph (x : scalarClosedTomitaDomain D) :
    ((x : GNSHilbert D),scalarClosedTomitaValue x) ∈ closure (scalarTomitaGraph D) :=
  Classical.choose_spec x.property

/-- The closed antilinear operator associated with the original finite-star-core
graph. No identification with the maximal scalar-weight domain is asserted. -/
def scalarClosedTomita (D : Context H) :
    scalarClosedTomitaDomain D →ₛₗ[starRingEnd ℂ] GNSHilbert D where
  toFun := scalarClosedTomitaValue
  map_add' x z := by
    apply scalarTomitaGraph_closure_single_valued D ((x+z : scalarClosedTomitaDomain D) : GNSHilbert D)
    · exact scalarClosedTomitaValue_graph (x+z)
    · exact scalarClosedGraph_add (scalarClosedTomitaValue_graph x) (scalarClosedTomitaValue_graph z)
  map_smul' c x := by
    apply scalarTomitaGraph_closure_single_valued D ((c • x : scalarClosedTomitaDomain D) : GNSHilbert D)
    · exact scalarClosedTomitaValue_graph (c • x)
    · exact scalarClosedGraph_conj_smul c (scalarClosedTomitaValue_graph x)

theorem scalarClosedTomita_graph (x : scalarClosedTomitaDomain D) :
    ((x : GNSHilbert D),scalarClosedTomita D x) ∈ closure (scalarTomitaGraph D) :=
  scalarClosedTomitaValue_graph x

theorem scalarClosedTomita_graph_eq :
    Set.range (fun x : scalarClosedTomitaDomain D =>
      ((x : GNSHilbert D),scalarClosedTomita D x)) = closure (scalarTomitaGraph D) := by
  ext p
  constructor
  · rintro ⟨x,rfl⟩
    exact scalarClosedTomita_graph x
  · intro hp
    let x : scalarClosedTomitaDomain D := ⟨p.1,p.2,hp⟩
    refine ⟨x,?_⟩
    apply Prod.ext
    · rfl
    · exact scalarTomitaGraph_closure_single_valued D p.1 _ p.2 (scalarClosedTomita_graph x) hp

theorem scalarClosedTomita_is_closed :
    IsClosed (Set.range (fun x : scalarClosedTomitaDomain D =>
      ((x : GNSHilbert D),scalarClosedTomita D x))) := by
  rw [scalarClosedTomita_graph_eq]
  exact isClosed_closure

theorem scalarClosedTomita_maps_domain (x : scalarClosedTomitaDomain D) :
    scalarClosedTomita D x ∈ scalarClosedTomitaDomain D :=
  ⟨(x : GNSHilbert D),scalarClosedGraph_swap (scalarClosedTomita_graph x)⟩

theorem scalarClosedTomita_involutive (x : scalarClosedTomitaDomain D) :
    scalarClosedTomita D ⟨scalarClosedTomita D x,scalarClosedTomita_maps_domain x⟩ = x :=
  scalarTomitaGraph_closure_single_valued D (scalarClosedTomita D x) _ _
    (scalarClosedTomita_graph ⟨scalarClosedTomita D x,scalarClosedTomita_maps_domain x⟩)
    (scalarClosedGraph_swap (scalarClosedTomita_graph x))

theorem scalarStarCore_mem_closedTomitaDomain (A : finiteStarCore D) :
    scalarGNSStarEmbedding D A ∈ scalarClosedTomitaDomain D :=
  ⟨scalarGNSStarEmbedding D (star A),subset_closure ⟨A,rfl⟩⟩

theorem scalarClosedTomita_extends_star (A : finiteStarCore D) :
    scalarClosedTomita D ⟨scalarGNSStarEmbedding D A,scalarStarCore_mem_closedTomitaDomain A⟩ =
      scalarGNSStarEmbedding D (star A) :=
  scalarTomitaGraph_closure_single_valued D (scalarGNSStarEmbedding D A) _ _
    (scalarClosedTomita_graph ⟨scalarGNSStarEmbedding D A,scalarStarCore_mem_closedTomitaDomain A⟩)
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
#print axioms scalarClosedTomita_maps_domain
#print axioms scalarClosedTomita_involutive
#print axioms scalarStarCore_mem_closedTomitaDomain
#print axioms scalarClosedTomita_extends_star
end
end F1Fecho.RegularScalarClosedTomita
