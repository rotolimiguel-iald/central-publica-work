import TGLExt.V350ClosedAntilinearResolvent
import Mathlib.Topology.Sequences

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open WithLp Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance realGraphHilbert : InnerProductSpace ℝ H := InnerProductSpace.complexToReal
variable (D : Submodule ℂ H) (S : D →ₗ[ℝ] H)

/-- Real restriction of a conjugate-linear map, without making it complex linear. -/
def antilinearRealMap (A : D →ₛₗ[starRingEnd ℂ] H) : D →ₗ[ℝ] H where
  toFun := A
  map_add' := A.map_add
  map_smul' := by
    intro r x
    have h := A.map_smulₛₗ (r : ℂ) x
    simpa using h

def realL2Graph : Submodule ℝ (WithLp 2 (H × H)) where
  carrier := {p | ∃ x : D, ofLp p=((x : H),S x)}
  zero_mem' := ⟨0,by simp; rfl⟩
  add_mem' := by
    rintro p q ⟨x,hx⟩ ⟨y,hy⟩
    refine ⟨x+y,?_⟩
    change ofLp p+ofLp q=_
    rw [hx,hy,map_add]
    rfl
  smul_mem' := by
    rintro r p ⟨x,hx⟩
    refine ⟨r • x,?_⟩
    change r • ofLp p=_
    rw [hx,map_smul]
    rfl

theorem realL2Graph_closed (hc : IsClosed (Set.range (fun x : D => ((x : H),S x)))) :
    IsClosed (realL2Graph D S : Set (WithLp 2 (H × H))) := by
  have he : (realL2Graph D S : Set (WithLp 2 (H × H))) =
      ofLp ⁻¹' Set.range (fun x : D => ((x : H),S x)) := by
    ext p
    constructor <;> rintro ⟨x,hx⟩ <;> exact ⟨x,hx.symm⟩
  rw [he]
  exact hc.preimage (WithLp.prod_continuous_ofLp 2 H H)

def realGraphInclusion (C : Submodule ℂ H) (hCD : C ≤ D) :
    C →ₗ[ℝ] realL2Graph D S where
  toFun x := ⟨toLp 2 ((x : H),S (Submodule.inclusion hCD x)),
    ⟨Submodule.inclusion hCD x,rfl⟩⟩
  map_add' := by
    intro x y
    apply Subtype.ext
    change toLp 2 ((x : H)+(y : H),S (Submodule.inclusion hCD (x+y))) = _
    rw [map_add,map_add]
    rfl
  map_smul' := by
    intro r x
    apply Subtype.ext
    change toLp 2 (r • (x : H),S (Submodule.inclusion hCD (r • x))) = _
    have hi : Submodule.inclusion hCD (r • x)=r • Submodule.inclusion hCD x := rfl
    rw [hi,map_smul]
    rfl

/-- A full weak resolvent family inside C makes C a core in the graph norm.
The real graph may come from either a linear or an antilinear operator. -/
theorem realGraphInclusion_dense (C : Submodule ℂ H) (hCD : C ≤ D)
    (hc : IsClosed (Set.range (fun x : D => ((x : H),S x))))
    (hr : ∀ z : H, ∃ u : C, ∀ x : D,
      inner ℝ (x : H) (u : H)+inner ℝ (S x) (S (Submodule.inclusion hCD u)) =
        inner ℝ (x : H) z) : DenseRange (realGraphInclusion D S C hCD) := by
  let G := realL2Graph D S
  letI : CompleteSpace G := (realL2Graph_closed D S hc).completeSpace_coe
  let F := realGraphInclusion D S C hCD
  have ho : F.range.orthogonal=⊥ := by
    apply le_antisymm ?_ bot_le
    intro w hw
    change w=0
    obtain ⟨x,hx⟩ := w.property
    obtain ⟨u,hu⟩ := hr (x : H)
    have hz : inner ℝ w (F u)=0 :=
      (real_inner_comm (F u) w).trans (hw (F u) ⟨u,rfl⟩)
    change inner ℝ (w.val : WithLp 2 (H × H)) ((F u).val) = 0 at hz
    rw [WithLp.prod_inner_apply] at hz
    change inner ℝ (ofLp w.val).1 (u : H)+
      inner ℝ (ofLp w.val).2 (S (Submodule.inclusion hCD u))=0 at hz
    rw [hx] at hz
    have hi : inner ℝ (x : H) (x : H)=0 := (hu x).symm.trans hz
    have hx0 : (x : H)=0 := (inner_self_eq_zero).mp hi
    have hxs : x=0 := Subtype.ext hx0
    apply Subtype.ext
    apply (WithLp.ofLp_injective 2).eq_iff.mp
    change ofLp w.val=(0,0)
    rw [hx,hxs,map_zero]
    rfl
  change Dense (Set.range F)
  rw [dense_iff_closure_eq]
  exact congrArg (fun V : Submodule ℝ G => (V : Set G))
    (F.range.topologicalClosure_eq_top_iff.mpr ho)

/-- Core density yields sequences converging in both graph coordinates. -/
theorem realGraphCore_sequence (C : Submodule ℂ H) (hCD : C ≤ D)
    (hd : DenseRange (realGraphInclusion D S C hCD)) (x : D) :
    ∃ u : ℕ → C, Tendsto (fun n => (u n : H)) atTop (𝓝 (x : H)) ∧
      Tendsto (fun n => S (Submodule.inclusion hCD (u n))) atTop (𝓝 (S x)) := by
  let G := realL2Graph D S
  let F := realGraphInclusion D S C hCD
  let v : G := ⟨toLp 2 ((x : H),S x),⟨x,rfl⟩⟩
  obtain ⟨p,hp,ht⟩ := mem_closure_iff_seq_limit.mp (hd v)
  choose u hu using hp
  have he : p=(fun n => F (u n)) := funext (fun n => (hu n).symm)
  rw [he] at ht
  have hcont : Continuous (fun w : G => ofLp (w.val : WithLp 2 (H × H))) :=
    (WithLp.prod_continuous_ofLp 2 H H).comp continuous_subtype_val
  have hpair := hcont.continuousAt.tendsto.comp ht
  exact ⟨u,continuous_fst.continuousAt.tendsto.comp hpair,
    continuous_snd.continuousAt.tendsto.comp hpair⟩

#print axioms antilinearRealMap
#print axioms realL2Graph
#print axioms realL2Graph_closed
#print axioms realGraphInclusion
#print axioms realGraphInclusion_dense
#print axioms realGraphCore_sequence
end
end TGLV350.Regular
