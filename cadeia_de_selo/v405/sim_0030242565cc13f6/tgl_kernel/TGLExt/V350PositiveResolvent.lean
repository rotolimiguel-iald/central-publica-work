import TGLExt.V350RegularNormality
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The bounded inverse of one plus a positive operator. Positivity is required
in the theorems, not hidden in the definition. -/
def positiveResolvent (A : H →L[ℂ] H) : H →L[ℂ] H := Ring.inverse (1 + A)

theorem one_add_strictlyPositive (A : H →L[ℂ] H) (hA : 0 ≤ A) :
    IsStrictlyPositive (1 + A) := isStrictlyPositive_one.add_nonneg hA

theorem positiveResolvent_left_inverse (A : H →L[ℂ] H) (hA : 0 ≤ A) :
    positiveResolvent A * (1 + A) = 1 :=
  Ring.inverse_mul_cancel _ (one_add_strictlyPositive A hA).isUnit

theorem positiveResolvent_right_inverse (A : H →L[ℂ] H) (hA : 0 ≤ A) :
    (1 + A) * positiveResolvent A = 1 :=
  Ring.mul_inverse_cancel _ (one_add_strictlyPositive A hA).isUnit

theorem positiveResolvent_nonneg (A : H →L[ℂ] H) (hA : 0 ≤ A) :
    0 ≤ positiveResolvent A := (one_add_strictlyPositive A hA).ringInverse.nonneg

theorem positiveResolvent_le_one (A : H →L[ℂ] H) (hA : 0 ≤ A) :
    positiveResolvent A ≤ 1 := by
  simpa only [positiveResolvent, Ring.inverse_one] using
    CStarAlgebra.ringInverse_le_ringInverse (show (1 : H →L[ℂ] H) ≤ 1 + A by
      exact le_add_of_nonneg_right hA) isStrictlyPositive_one

theorem positiveResolvent_antitone {A B : H →L[ℂ] H} (hA : 0 ≤ A) (hAB : A ≤ B) :
    positiveResolvent B ≤ positiveResolvent A :=
  CStarAlgebra.ringInverse_le_ringInverse (add_le_add le_rfl hAB)
    (one_add_strictlyPositive A hA)

theorem positiveResolvent_injective (A : H →L[ℂ] H) (hA : 0 ≤ A) :
    Function.Injective (positiveResolvent A) := by
  intro v w h
  have h' := congrArg (fun x => (1 + A) x) h
  change ((1+A) * positiveResolvent A) v = ((1+A) * positiveResolvent A) w at h'
  simpa only [positiveResolvent_right_inverse A hA, one_apply_eq_self] using h'

/-- A bicommutant contains the resolvent of each of its positive elements. -/
theorem positiveResolvent_mem (N : VonNeumannAlgebra H) (A : H →L[ℂ] H)
    (hmem : A ∈ N) (hA : 0 ≤ A) : positiveResolvent A ∈ N := by
  rw [← SetLike.mem_coe, ← VonNeumannAlgebra.centralizer_centralizer]
  rw [Set.mem_centralizer_iff]
  intro C hC
  have hBmem : (1 : H →L[ℂ] H) + A ∈ N := N.toStarSubalgebra.add_mem
    N.toStarSubalgebra.one_mem hmem
  have hBC := (Set.mem_centralizer_iff.mp hC) (1 + A) hBmem
  calc
    C * positiveResolvent A =
        (positiveResolvent A * (1+A)) * (C * positiveResolvent A) := by
      rw [positiveResolvent_left_inverse A hA, one_mul]
    _ = positiveResolvent A * ((1+A) * C) * positiveResolvent A := by
      simp only [mul_assoc]
    _ = positiveResolvent A * (C * (1+A)) * positiveResolvent A := by rw [hBC]
    _ = (positiveResolvent A * C) * ((1+A) * positiveResolvent A) := by
      simp only [mul_assoc]
    _ = positiveResolvent A * C := by
      rw [positiveResolvent_right_inverse A hA, mul_one]

/-- A decreasing family of positive contractions has a strong infimum in the same
von Neumann algebra. No uniform positive lower bound is assumed. -/
theorem vonNeumann_antitone_contraction_limit (N : VonNeumannAlgebra H)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (F : ι → (H →L[ℂ] H)) (hmem : ∀ i, F i ∈ N)
    (hpos : ∀ i, 0 ≤ F i) (hone : ∀ i, F i ≤ 1) (hanti : Antitone F) :
    ∃ R : H →L[ℂ] H, R ∈ N ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun i => F i v) atTop (𝓝 (R v))) ∧ IsGLB (Set.range F) R := by
  let T : ι → (H →L[ℂ] H) := fun i => 1 - F i
  have hTpos : ∀ i, 0 ≤ T i := fun i => sub_nonneg.mpr (hone i)
  have hTmono : Monotone T := fun i j hij => sub_le_sub_left (hanti hij) 1
  have hTone : ∀ i, T i ≤ 1 := fun i => sub_le_self 1 (hpos i)
  have hTnorm : ∀ i, ‖T i‖ ≤ ‖(1 : H →L[ℂ] H)‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hTpos i) (hTone i)
  obtain ⟨B, hBpos, _, hstrong, hB⟩ :=
    ChatgptAudit.Expectation047.monotone_operator_limit T hTpos hTmono
      ‖(1 : H →L[ℂ] H)‖ (norm_nonneg _) hTnorm
  have hBone : B ≤ 1 := hB.2 (by rintro _ ⟨i,rfl⟩; exact hTone i)
  have hBmem : B ∈ N := vonNeumann_mem_of_strong_limit N T B
    (Eventually.of_forall (fun i => N.toStarSubalgebra.sub_mem
      N.toStarSubalgebra.one_mem (hmem i))) hstrong
  refine ⟨1-B, N.toStarSubalgebra.sub_mem N.toStarSubalgebra.one_mem hBmem,
    sub_nonneg.mpr hBone, sub_le_self 1 hBpos, ?_, ?_⟩
  · intro v
    have ht : Tendsto (fun i => v - T i v) atTop (𝓝 (v - B v)) :=
      tendsto_const_nhds.sub (hstrong v)
    simpa only [T, sub_apply, one_apply_eq_self, sub_sub_cancel] using ht
  · constructor
    · rintro _ ⟨i,rfl⟩
      have hi := sub_le_sub_left (hB.1 (Set.mem_range_self i)) 1
      simpa only [T, sub_sub_cancel] using hi
    · intro D hD
      have hi : B ≤ 1-D := hB.2 (by
        rintro _ ⟨i,rfl⟩
        exact sub_le_sub_left (hD (Set.mem_range_self i)) 1)
      have hi' := sub_le_sub_left hi 1
      simpa only [sub_sub_cancel] using hi'

#print axioms positiveResolvent_left_inverse
#print axioms positiveResolvent_right_inverse
#print axioms positiveResolvent_nonneg
#print axioms positiveResolvent_le_one
#print axioms positiveResolvent_antitone
#print axioms positiveResolvent_injective
#print axioms positiveResolvent_mem
#print axioms vonNeumann_antitone_contraction_limit
end
end TGLV350.Regular
