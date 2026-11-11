import TGLExt.F1Fecho394.CompactPairCoverR1
import TGLExt.F1Fecho394.PhysicalCompactPartitionR1

/-! Local vanishing of a real bilinear pairing extends over two compact
Maxwell test supports by finite real smooth partitions. Local vanishing is
an explicit premise here, to be supplied by physical opposite wedges. -/
set_option autoImplicit false
set_option maxHeartbeats 700000
noncomputable section
open Set Function
namespace F1Fecho.MaxwellGlobal

def TestPairZero (B : SchwartzTensor →ₗ[ℝ] SchwartzTensor →ₗ[ℝ] ℝ)
    (U V : Set Spacetime) : Prop :=
  ∀ f g, IsRealTest f → IsRealTest g →
    support (f : Spacetime → TensorValue) ⊆ U →
    support (g : Spacetime → TensorValue) ⊆ V → B f g = 0

theorem compact_pair_zero (B : SchwartzTensor →ₗ[ℝ] SchwartzTensor →ₗ[ℝ] ℝ)
    (f g : SchwartzTensor) (hfr : IsRealTest f) (hgr : IsRealTest g)
    (hfc : HasCompactSupport (f : Spacetime → TensorValue))
    (hgc : HasCompactSupport (g : Spacetime → TensorValue))
    (hloc : ∀ (x : tsupport (f : Spacetime → TensorValue))
      (y : tsupport (g : Spacetime → TensorValue)), ∃ U V : Set Spacetime,
      IsOpen U ∧ IsOpen V ∧ x.val ∈ U ∧ y.val ∈ V ∧ TestPairZero B U V) :
    B f g = 0 := by
  classical
  have hmono : ∀ U U' V, U' ⊆ U → TestPairZero B U V → TestPairZero B U' V := by
    intro U U' V hsub h f' g' hr hs hf hg
    exact h f' g' hr hs (hf.trans hsub) hg
  obtain ⟨s,t,U,V,hs,hh⟩ := CompactPairCover.finite_rectangular_cover
    (tsupport (f : Spacetime → TensorValue)) (tsupport (g : Spacetime → TensorValue))
    hfc hgc (TestPairZero B) hmono hloc
  have hcoverf : tsupport (f : Spacetime → TensorValue) ⊆ ⋃ i : s, U i.val := by
    intro z hz
    obtain ⟨x,hx⟩ := mem_iUnion.mp (hs hz)
    obtain ⟨hxs,hxz⟩ := mem_iUnion.mp hx
    exact mem_iUnion.mpr ⟨⟨x,hxs⟩,hxz⟩
  obtain ⟨fp,hfs,hfp⟩ := real_compact_partition (ι := s) f hfr hfc
    (fun i => U i.val) (fun i => (hh i.val i.property).1) hcoverf
  rw [← hfs,map_sum]
  simp only [LinearMap.sum_apply]
  apply Finset.sum_eq_zero
  intro i _
  have hcoverg : tsupport (g : Spacetime → TensorValue) ⊆ ⋃ j : t i.val, V i.val j.val := by
    intro z hz
    obtain ⟨y,hy⟩ := mem_iUnion.mp ((hh i.val i.property).2.1 hz)
    obtain ⟨hyt,hyz⟩ := mem_iUnion.mp hy
    exact mem_iUnion.mpr ⟨⟨y,hyt⟩,hyz⟩
  obtain ⟨gp,hgs,hgp⟩ := real_compact_partition (ι := t i.val) g hgr hgc
    (fun j => V i.val j.val) (fun j => ((hh i.val i.property).2.2 j.val j.property).1) hcoverg
  rw [← hgs,map_sum]
  apply Finset.sum_eq_zero
  intro j _
  exact ((hh i.val i.property).2.2 j.val j.property).2
    (fp i) (gp j) (hfp i).1 (hgp j).1
    (fun z hz => ((hfp i).2.2 hz).1) (fun z hz => ((hgp j).2.2 hz).1)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.compact_pair_zero
