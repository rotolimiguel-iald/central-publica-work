import TGLExt.V350L2Order
import TGLExt.V350RegularTopology

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular

open Filter TGLExt
open scoped Topology

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Pointwise norm convergence of operators implies weak operator convergence,
along an arbitrary filter. -/
theorem strong_tendsto_wot {ι : Type*} {l : Filter ι}
    (T : ι → (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hstrong : ∀ v, Tendsto (fun i => T i v) l (𝓝 (B v))) :
    Tendsto (fun i => ContinuousLinearMapWOT.ofCLM (T i)) l
      (𝓝 (ContinuousLinearMapWOT.ofCLM B)) := by
  apply ContinuousLinearMapWOT.tendsto_iff_forall_dual_apply_tendsto.mpr
  intro v φ
  exact (φ.continuous.tendsto (B v)).comp (hstrong v)

/-- The bicommutant's WOT closure keeps every existing strong limit in the algebra. -/
theorem vonNeumann_mem_of_strong_limit (N : VonNeumannAlgebra H)
    {ι : Type*} {l : Filter ι} [l.NeBot]
    (T : ι → (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hmem : ∀ᶠ i in l, T i ∈ N)
    (hstrong : ∀ v, Tendsto (fun i => T i v) l (𝓝 (B v))) : B ∈ N := by
  exact (vonNeumann_wot_closed N).mem_of_tendsto
    (strong_tendsto_wot T B hstrong) hmem

/-- An ambient supremum that belongs to the subalgebra is also its internal supremum. -/
theorem vonNeumann_isLUB_of_coe_isLUB (N : VonNeumannAlgebra H) {ι : Type*}
    (T : ι → N.toStarSubalgebra) (B : N.toStarSubalgebra)
    (hB : IsLUB (Set.range (fun i => (T i : H →L[ℂ] H))) (B : H →L[ℂ] H)) :
    IsLUB (Set.range T) B := by
  constructor
  · rintro _ ⟨i, rfl⟩
    exact hB.1 (Set.mem_range_self i)
  · intro D hD
    apply hB.2
    rintro _ ⟨i, rfl⟩
    exact hD (Set.mem_range_self i)

/-- A positive increasing norm-bounded net in a von Neumann algebra has a strong
limit in that algebra, which is both its ambient and its internal supremum. -/
theorem vonNeumann_exists_positive_isLUB (N : VonNeumannAlgebra H)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → N.toStarSubalgebra) (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖(T i : H →L[ℂ] H)‖ ≤ C) :
    ∃ B : N.toStarSubalgebra, 0 ≤ B ∧ ‖(B : H →L[ℂ] H)‖ ≤ C ∧
      (∀ v, Tendsto (fun i => (T i : H →L[ℂ] H) v) atTop
        (𝓝 ((B : H →L[ℂ] H) v))) ∧
      IsLUB (Set.range (fun i => (T i : H →L[ℂ] H))) (B : H →L[ℂ] H) ∧
      IsLUB (Set.range T) B := by
  obtain ⟨B, hBpos, hBnorm, hstrong, hB⟩ :=
    ChatgptAudit.Expectation047.monotone_operator_limit
      (fun i => (T i : H →L[ℂ] H)) hpos hmono C hC hbound
  have hmem : B ∈ N := vonNeumann_mem_of_strong_limit N _ B
    (Eventually.of_forall (fun i => (T i).property)) hstrong
  refine ⟨⟨B, hmem⟩, hBpos, hBnorm, hstrong, hB, ?_⟩
  exact vonNeumann_isLUB_of_coe_isLUB N T ⟨B, hmem⟩ hB

/-- For positive increasing nets, an internal supremum of a von Neumann algebra
is its ambient supremum. The ambient limit is constructed, not assumed. -/
theorem vonNeumann_isLUB_coe (N : VonNeumannAlgebra H)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → N.toStarSubalgebra) (B : N.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T) (hB : IsLUB (Set.range T) B) :
    IsLUB (Set.range (fun i => (T i : H →L[ℂ] H))) (B : H →L[ℂ] H) := by
  have hbound : ∀ i, ‖(T i : H →L[ℂ] H)‖ ≤ ‖(B : H →L[ℂ] H)‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hB.1 (Set.mem_range_self i))
  obtain ⟨D, _, _, _, hDambient, hDinternal⟩ :=
    vonNeumann_exists_positive_isLUB N T hpos hmono
      ‖(B : H →L[ℂ] H)‖ (norm_nonneg _) hbound
  have hDB : D = B := hDinternal.unique hB
  subst D
  exact hDambient

/-- In particular, an internally order-bounded positive increasing net has a
supremum in the von Neumann algebra, also valid against all ambient upper bounds. -/
theorem vonNeumann_exists_positive_isLUB_of_bddAbove (N : VonNeumannAlgebra H)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → N.toStarSubalgebra) (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T)
    (hbounded : BddAbove (Set.range T)) :
    ∃ B : N.toStarSubalgebra, IsLUB (Set.range T) B ∧
      IsLUB (Set.range (fun i => (T i : H →L[ℂ] H))) (B : H →L[ℂ] H) := by
  obtain ⟨D, hD⟩ := hbounded
  have hbound : ∀ i, ‖(T i : H →L[ℂ] H)‖ ≤ ‖(D : H →L[ℂ] H)‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hD (Set.mem_range_self i))
  obtain ⟨B, _, _, _, hBambient, hBinternal⟩ :=
    vonNeumann_exists_positive_isLUB N T hpos hmono
      ‖(D : H →L[ℂ] H)‖ (norm_nonneg _) hbound
  exact ⟨B, hBinternal, hBambient⟩

@[simp]
theorem regularCoreEmbedding_coe (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) :
    (regularCoreEmbedding P A :
      RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) =
      fibre (A : TowerHilbert P →L[ℂ] TowerHilbert P) := rfl

/-- Order normality of the regular core embedding: every positive increasing net
with an internal supremum is sent to a net with the corresponding internal supremum.
There is no strong-convergence, predual, trace, or normality hypothesis. -/
theorem regularCoreEmbedding_preserves_positive_isLUB (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → (theFactorObject P).toStarSubalgebra)
    (B : (theFactorObject P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T) (hB : IsLUB (Set.range T) B) :
    IsLUB (Set.range (fun i => regularCoreEmbedding P (T i)))
      (regularCoreEmbedding P B) := by
  have hBambient := vonNeumann_isLUB_coe (theFactorObject P) T B hpos hmono hB
  have hfibre := fibre_preserves_positive_isLUB
    (fun i => (T i : TowerHilbert P →L[ℂ] TowerHilbert P))
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) hpos hmono hBambient
  apply vonNeumann_isLUB_of_coe_isLUB (regularCoreAlgebra P)
  simpa only [regularCoreEmbedding_coe] using hfibre

/-- The same normality contract stated for all nonempty directed sets of positive
elements, with the least-upper-bound relation internal on both sides. -/
theorem regularCoreEmbedding_preserves_positive_directed_isLUB (P : SiteProfile)
    (S : Set (theFactorObject P).toStarSubalgebra)
    (B : (theFactorObject P).toStarSubalgebra)
    (hne : S.Nonempty) (hdir : DirectedOn (· ≤ ·) S)
    (hpos : ∀ A ∈ S, 0 ≤ A) (hB : IsLUB S B) :
    IsLUB (regularCoreEmbedding P '' S) (regularCoreEmbedding P B) := by
  letI : Nonempty S := hne.to_subtype
  letI : IsDirectedOrder S := hdir.isDirectedOrder
  have hrange : Set.range (fun A : S => (A : (theFactorObject P).toStarSubalgebra)) = S := by
    ext A
    simp only [Set.mem_range, Subtype.exists, exists_prop, exists_eq_right]
  have hnet := regularCoreEmbedding_preserves_positive_isLUB P
    (fun A : S => (A : (theFactorObject P).toStarSubalgebra)) B
    (fun A => hpos A A.property) (fun _ _ h => h) (hrange.symm ▸ hB)
  have himage : Set.range (fun A : S => regularCoreEmbedding P A.val) =
      regularCoreEmbedding P '' S := by
    ext A
    simp only [Set.mem_range, Set.mem_image, Subtype.exists, exists_prop]
  rw [himage] at hnet
  exact hnet

#print axioms strong_tendsto_wot
#print axioms vonNeumann_mem_of_strong_limit
#print axioms vonNeumann_isLUB_of_coe_isLUB
#print axioms vonNeumann_exists_positive_isLUB
#print axioms vonNeumann_isLUB_coe
#print axioms vonNeumann_exists_positive_isLUB_of_bddAbove
#print axioms regularCoreEmbedding_coe
#print axioms regularCoreEmbedding_preserves_positive_isLUB
#print axioms regularCoreEmbedding_preserves_positive_directed_isLUB

end
end TGLV350.Regular
