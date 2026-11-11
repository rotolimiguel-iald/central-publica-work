import Mathlib.Topology.Compactness.Compact

/-! Finite rectangular localization for two compact sets. For each member of
the first cover the second compact set has its own finite cover. No single
pair of wedges for arbitrary sets is asserted. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
open Set
namespace F1Fecho.CompactPairCover
variable {X : Type} [TopologicalSpace X]

theorem finite_rectangular_cover (K L : Set X) (hK : IsCompact K) (hL : IsCompact L)
    (R : Set X → Set X → Prop)
    (hmono : ∀ U U' V, U' ⊆ U → R U V → R U' V)
    (hloc : ∀ (x : K) (y : L), ∃ U V : Set X,
      IsOpen U ∧ IsOpen V ∧ x.val ∈ U ∧ y.val ∈ V ∧ R U V) :
    ∃ s : Finset K, ∃ t : K → Finset L, ∃ U : K → Set X, ∃ V : K → L → Set X,
      K ⊆ ⋃ x ∈ s, U x ∧
      ∀ x ∈ s, IsOpen (U x) ∧ L ⊆ ⋃ y ∈ t x, V x y ∧
        ∀ y ∈ t x, IsOpen (V x y) ∧ R (U x) (V x y) := by
  classical
  choose U V hU hV hx hy hR using hloc
  have hc (x : K) : L ⊆ ⋃ y : L, V x y := by
    intro y hyL
    exact mem_iUnion.mpr ⟨⟨y,hyL⟩,hy x ⟨y,hyL⟩⟩
  choose t ht using (fun x : K => hL.elim_finite_subcover (V x) (hV x) (hc x))
  let W (x : K) : Set X := ⋂ y ∈ t x, U x y
  have hw (x : K) : IsOpen (W x) := isOpen_biInter_finset (fun y _ => hU x y)
  have hwx (x : K) : x.val ∈ W x := by
    exact mem_iInter.mpr (fun y => mem_iInter.mpr (fun _ => hx x y))
  have hcover : K ⊆ ⋃ x : K, W x := by
    intro x hxK
    exact mem_iUnion.mpr ⟨⟨x,hxK⟩,hwx ⟨x,hxK⟩⟩
  obtain ⟨s,hs⟩ := hK.elim_finite_subcover W hw hcover
  refine ⟨s,t,W,V,hs,?_⟩
  intro x _
  refine ⟨hw x,ht x,?_⟩
  intro y hyt
  refine ⟨hV x y,hmono (U x y) (W x) (V x y) ?_ (hR x y)⟩
  intro z hz
  exact mem_iInter.mp (mem_iInter.mp hz y) hyt

end F1Fecho.CompactPairCover
#print axioms F1Fecho.CompactPairCover.finite_rectangular_cover
