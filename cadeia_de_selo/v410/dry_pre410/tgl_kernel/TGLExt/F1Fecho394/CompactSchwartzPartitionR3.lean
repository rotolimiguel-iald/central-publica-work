import Mathlib.Geometry.Manifold.PartitionOfUnity
import Mathlib.Analysis.Distribution.SchwartzSpace.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-! A compact Schwartz test splits into finitely many smooth compact tests
subordinate to an open cover. Each piece keeps the original support as well.
This supplies support decomposition, not causal commutation. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open Function Set SchwartzMap
open scoped Manifold ContDiff
namespace F1Fecho.CompactSchwartzPartition
abbrev E := EuclideanSpace ℝ (Fin 4)
variable {F ι : Type} [NormedAddCommGroup F] [NormedSpace ℝ F] [Fintype ι]

theorem finite_partition (f : SchwartzMap E F) (hf : HasCompactSupport (f : E → F))
    (U : ι → Set E) (ho : ∀ i, IsOpen (U i))
    (hcover : tsupport (f : E → F) ⊆ ⋃ i, U i) :
    ∃ parts : ι → SchwartzMap E F, (∑ i, parts i) = f ∧
      ∀ i, HasCompactSupport (parts i : E → F) ∧
        (support (parts i : E → F) ⊆ U i ∩ support (f : E → F)) ∧
        ∀ x, ∃ r : ℝ, parts i x = r • f x := by
  classical
  obtain ⟨ρ,hρ⟩ := SmoothPartitionOfUnity.exists_isSubordinate 𝓘(ℝ,E)
    isClosed_closure U ho hcover
  let g (i : ι) (x : E) : F := ρ i x • f x
  have hc (i : ι) : HasCompactSupport (g i) := hf.smul_left
  have hd (i : ι) : ContDiff ℝ ∞ (g i) :=
    (contMDiff_iff_contDiff.mp (ρ i).contMDiff).smul f.smooth'
  let parts (i : ι) : SchwartzMap E F := (hc i).toSchwartzMap (hd i)
  have hp (i : ι) (x : E) : parts i x = ρ i x • f x := rfl
  refine ⟨parts,?_,?_⟩
  · ext x
    by_cases hx : f x = 0
    · simp [parts,g,hx]
    · have hsum : (∑ i, ρ i x) = 1 := by
        simpa only [finsum_eq_sum_of_fintype] using
          ρ.sum_eq_one (show x ∈ tsupport (f : E → F) from subset_closure hx)
      change (∑ i, parts i) x = f x
      simp only [SchwartzMap.sum_apply,hp,
        ← Finset.sum_smul,hsum,one_smul]
  · intro i
    refine ⟨hc i,?_,?_⟩
    · intro x hx
      change x ∈ support (g i) at hx
      exact ⟨hρ i (subset_closure (support_smul_subset_left (ρ i) f hx)),
        support_smul_subset_right (ρ i) f hx⟩
    · intro x
      exact ⟨ρ i x,hp i x⟩

end F1Fecho.CompactSchwartzPartition
#print axioms F1Fecho.CompactSchwartzPartition.finite_partition
