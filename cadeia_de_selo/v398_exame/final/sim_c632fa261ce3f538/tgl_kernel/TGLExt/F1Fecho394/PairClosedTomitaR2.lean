import TGLExt.F1Fecho394.PairTomitaClosabilityR2
/-! Generic reuse of ClosedTomitaOperator.lean on the actual pair graph.
The graph is closed here and its domain is constructed. Functionality is an
explicit argument, supplied by the commuting cyclic algebra theorem. This
does not assert that its polar conjugation or modular group is a given one. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Set Topology
namespace F1Fecho.PairTomita
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable {M : StarSubalgebra ℂ (H →L[ℂ] H)} {Ω : H}

theorem graph_zero : (0,0) ∈ graph M Ω := by
  refine ⟨0,M.zero_mem,?_⟩
  simp

theorem graph_add {p q : H × H} (hp : p ∈ graph M Ω) (hq : q ∈ graph M Ω) :
    p+q ∈ graph M Ω := by
  obtain ⟨a,ha,rfl⟩ := hp
  obtain ⟨b,hb,rfl⟩ := hq
  refine ⟨a+b,M.add_mem ha hb,?_⟩
  simp [star_add]

theorem graph_conj_smul (c : ℂ) {p : H × H} (hp : p ∈ graph M Ω) :
    (c • p.1, (starRingEnd ℂ c) • p.2) ∈ graph M Ω := by
  obtain ⟨a,ha,rfl⟩ := hp
  refine ⟨c • a,M.smul_mem ha c,?_⟩
  simp only [star_smul,ContinuousLinearMap.smul_apply,starRingEnd_apply]

theorem graph_swap {p : H × H} (hp : p ∈ graph M Ω) : p.swap ∈ graph M Ω := by
  obtain ⟨a,ha,rfl⟩ := hp
  refine ⟨star a,star_mem ha,?_⟩
  simp

theorem closed_graph_add {p q : H × H}
    (hp : p ∈ closure (graph M Ω)) (hq : q ∈ closure (graph M Ω)) :
    p+q ∈ closure (graph M Ω) := by
  have hl : ∀ a ∈ graph M Ω, ∀ b ∈ closure (graph M Ω), a+b ∈ closure (graph M Ω) := by
    intro a ha
    exact closure_minimal (fun b hb => subset_closure (graph_add ha hb))
      (isClosed_closure.preimage (continuous_const.add continuous_id))
  exact closure_minimal (fun a ha => hl a ha q hq)
    (isClosed_closure.preimage (continuous_id.add continuous_const)) hp

theorem closed_graph_conj_smul (c : ℂ) {p : H × H}
    (hp : p ∈ closure (graph M Ω)) :
    (c • p.1, (starRingEnd ℂ c) • p.2) ∈ closure (graph M Ω) := by
  apply closure_minimal (t := {p : H × H |
    (c • p.1, (starRingEnd ℂ c) • p.2) ∈ closure (graph M Ω)}) ?_ ?_ hp
  · intro p hp
    exact subset_closure (graph_conj_smul c hp)
  · apply isClosed_closure.preimage
    fun_prop

theorem closed_graph_swap {p : H × H} (hp : p ∈ closure (graph M Ω)) :
    p.swap ∈ closure (graph M Ω) := by
  apply closure_minimal (t := {p : H × H | p.swap ∈ closure (graph M Ω)}) ?_ ?_ hp
  · intro p hp
    exact subset_closure (graph_swap hp)
  · exact isClosed_closure.preimage continuous_swap

def closedDomain (M : StarSubalgebra ℂ (H →L[ℂ] H)) (Ω : H) : Submodule ℂ H where
  carrier := {x | ∃ y, (x,y) ∈ closure (graph M Ω)}
  zero_mem' := ⟨0,subset_closure graph_zero⟩
  add_mem' := by
    rintro x z ⟨y,hy⟩ ⟨w,hw⟩
    exact ⟨y+w,closed_graph_add hy hw⟩
  smul_mem' := by
    rintro c x ⟨y,hy⟩
    exact ⟨(starRingEnd ℂ c) • y,closed_graph_conj_smul c hy⟩

def closedValue (x : closedDomain M Ω) : H := Classical.choose x.property

theorem closedValue_graph (x : closedDomain M Ω) :
    ((x : H), closedValue x) ∈ closure (graph M Ω) := Classical.choose_spec x.property

def closedTomita
    (hf : ∀ x y z : H, (x,y) ∈ closure (graph M Ω) → (x,z) ∈ closure (graph M Ω) → y=z) :
    closedDomain M Ω →ₛₗ[starRingEnd ℂ] H where
  toFun := closedValue
  map_add' x z := by
    apply hf ((x+z : closedDomain M Ω) : H)
    · exact closedValue_graph (x+z)
    · exact closed_graph_add (closedValue_graph x) (closedValue_graph z)
  map_smul' c x := by
    apply hf ((c • x : closedDomain M Ω) : H)
    · exact closedValue_graph (c • x)
    · exact closed_graph_conj_smul c (closedValue_graph x)

variable (hf : ∀ x y z : H, (x,y) ∈ closure (graph M Ω) → (x,z) ∈ closure (graph M Ω) → y=z)

theorem closedTomita_graph (x : closedDomain M Ω) :
    ((x : H),closedTomita hf x) ∈ closure (graph M Ω) := closedValue_graph x

theorem closedTomita_graph_eq :
    Set.range (fun x : closedDomain M Ω => ((x : H),closedTomita hf x)) = closure (graph M Ω) := by
  ext p
  constructor
  · rintro ⟨x,rfl⟩
    exact closedTomita_graph hf x
  · intro hp
    let x : closedDomain M Ω := ⟨p.1,p.2,hp⟩
    refine ⟨x,?_⟩
    apply Prod.ext
    · rfl
    · exact hf p.1 _ p.2 (closedTomita_graph hf x) hp

theorem closedTomita_isClosed :
    IsClosed (Set.range (fun x : closedDomain M Ω => ((x : H),closedTomita hf x))) := by
  rw [closedTomita_graph_eq]
  exact isClosed_closure

theorem closedDomain_dense
    (hM : Dense ((fun a : H →L[ℂ] H => a Ω) '' (M : Set (H →L[ℂ] H)))) :
    Dense (closedDomain M Ω : Set H) := by
  apply Dense.mono ?_ (domain_dense M Ω hM)
  rintro x ⟨p,hp,rfl⟩
  exact ⟨p.2,subset_closure hp⟩

theorem closedTomita_maps_domain (x : closedDomain M Ω) :
    closedTomita hf x ∈ closedDomain M Ω :=
  ⟨(x : H),closed_graph_swap (closedTomita_graph hf x)⟩

theorem closedTomita_involutive (x : closedDomain M Ω) :
    closedTomita hf ⟨closedTomita hf x,closedTomita_maps_domain hf x⟩ = x := by
  exact hf (closedTomita hf x) _ _
    (closedTomita_graph hf ⟨closedTomita hf x,closedTomita_maps_domain hf x⟩)
    (closed_graph_swap (closedTomita_graph hf x))

theorem algebra_vector_mem_domain {a : H →L[ℂ] H} (ha : a ∈ M) :
    a Ω ∈ closedDomain M Ω := ⟨(star a) Ω,subset_closure ⟨a,ha,rfl⟩⟩

theorem closedTomita_extends_adjoint {a : H →L[ℂ] H} (ha : a ∈ M) :
    closedTomita hf ⟨a Ω,algebra_vector_mem_domain ha⟩ = (star a) Ω := by
  exact hf (a Ω) _ _ (closedTomita_graph hf ⟨a Ω,algebra_vector_mem_domain ha⟩)
    (subset_closure ⟨a,ha,rfl⟩)

end F1Fecho.PairTomita
#print axioms F1Fecho.PairTomita.closedTomita
#print axioms F1Fecho.PairTomita.closedTomita_graph_eq
#print axioms F1Fecho.PairTomita.closedTomita_isClosed
#print axioms F1Fecho.PairTomita.closedDomain_dense
#print axioms F1Fecho.PairTomita.closedTomita_involutive
#print axioms F1Fecho.PairTomita.closedTomita_extends_adjoint
