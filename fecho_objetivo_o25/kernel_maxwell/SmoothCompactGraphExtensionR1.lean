import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension
import Mathlib.Analysis.Normed.Group.Bounded

/-! Constructive compact smooth extension from a graph. The graph function
need only be continuous: a time cutoff is one on the compact energy image. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.SmoothGraphExtension
open Set
open scoped ContDiff
variable {E V : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup V] [NormedSpace ℝ V]

theorem exists_extension (h : E→V) (hh : ContDiff ℝ ∞ h)
    (hc : HasCompactSupport h) (e : E→ℝ) (he : Continuous e) :
    ∃ F : ℝ×E→V, ContDiff ℝ ∞ F ∧ HasCompactSupport F ∧
      ∀y,F (e y,y)=h y := by
  obtain ⟨R,hR,hB⟩ := (hc.isCompact.image he).isBounded.exists_pos_norm_le
  let b : ContDiffBump (0:ℝ) := ⟨R,R+1,hR,by linarith⟩
  let F : ℝ×E→V := fun z=>b z.1 • h z.2
  refine ⟨F,?_,?_,?_⟩
  · exact (b.contDiff.comp contDiff_fst).smul (hh.comp contDiff_snd)
  · apply HasCompactSupport.intro (b.hasCompactSupport.isCompact.prod hc.isCompact)
    intro z hz
    by_cases ht : z.1∈tsupport b
    · have hp : z.2∉tsupport h := fun hp=>hz ⟨ht,hp⟩
      simp [F,image_eq_zero_of_notMem_tsupport hp]
    · simp [F,image_eq_zero_of_notMem_tsupport ht]
  · intro y
    by_cases hy : h y=0
    · simp [F,hy]
    · have hb : b (e y)=1 := by
        apply b.one_of_mem_closedBall
        change dist (e y) 0≤R
        simpa only [dist_zero_right] using hB (e y) ⟨y,subset_tsupport h hy,rfl⟩
      simp [F,hb]

end F1Fecho.SmoothGraphExtension
#print axioms F1Fecho.SmoothGraphExtension.exists_extension
