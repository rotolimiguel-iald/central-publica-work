import TGLExt.F1Fecho394.RegularScalarGNSStrongContinuityR1
import TGLExt.V350DualOrbitStrongLimits
/-! Normality of the actual scalar GNS representation for a general regular
core context, porting the existing V350 order proof. No modular identity or
trace is inserted as an assumption. -/


set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.RegularScalarGNSNormality
open TGLExt TGLV350.Regular Filter F1Fecho.RegularScalarGNS F1Fecho.RegularScalarGNSRepresentation
open F1Fecho.RegularScalarGNSStrongContinuity
open scoped Topology
noncomputable section

theorem operator_le_of_sub_nonneg {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (A B : H →L[ℂ] H) (h : 0 ≤ B-A) : A ≤ B := sub_nonneg.mp h

theorem dualOrbitRepresentation_nonneg {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    0 ≤ dualOrbitRepresentation A := by
  have h := OrderHomClass.monotone (dualOrbitRepresentation (H := H)) hA
  simpa only [map_zero] using h

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem scalarGNSRepresentation_nonneg (D : Context H)
    (B : D.algebra.toStarSubalgebra) (hB : 0 ≤ B) :
    0 ≤ scalarGNSRepresentation D B := by
  have ha := dualOrbitRepresentation_nonneg B.val hB
  rw [ContinuousLinearMap.nonneg_iff_isPositive,
    ContinuousLinearMap.isPositive_iff_complex] at ha ⊢
  intro v
  exact ha v.val

theorem scalarGNSRepresentation_monotone (D : Context H) :
    Monotone (scalarGNSRepresentation D) := by
  intro A B h
  have hp := scalarGNSRepresentation_nonneg D (B-A) (sub_nonneg.mpr h)
  rw [map_sub] at hp
  exact operator_le_of_sub_nonneg _ _ hp

/-- Normality in order of the actual representation on H_I. The strong limit
is constructed from the internal supremum, rather than supplied as a premise. -/
theorem scalarGNSRepresentation_preserves_positive_isLUB (D : Context H)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → D.algebra.toStarSubalgebra)
    (B : D.algebra.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T)
    (hB : IsLUB (Set.range T) B) :
    IsLUB (Set.range (fun i => scalarGNSRepresentation D (T i)))
      (scalarGNSRepresentation D B) := by
  have hbound : ∀ i, ‖(T i).val‖ ≤ ‖B.val‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hB.1 (Set.mem_range_self i))
  obtain ⟨Blim, _, _, hlim, _, hD⟩ := vonNeumann_exists_positive_isLUB
    D.algebra T hpos hmono ‖B.val‖ (norm_nonneg _) hbound
  have hDB : Blim = B := hD.unique hB
  subst Blim
  apply ChatgptAudit.Expectation047.monotone_strong_limit_isLUB
    (fun i => scalarGNSRepresentation D (T i))
  · intro i j hij
    exact scalarGNSRepresentation_monotone D (hmono hij)
  · exact scalarGNSRepresentation_tendsto_of_uniformly_bounded D T B ‖B.val‖ hbound hlim

/-- The same statement for all nonempty directed positive subsets of N.
This theorem does not identify the maximal scalar GNS domain or prove KMS. -/
theorem scalarGNSRepresentation_preserves_positive_directed_isLUB (D : Context H)
    (S : Set D.algebra.toStarSubalgebra)
    (B : D.algebra.toStarSubalgebra)
    (hne : S.Nonempty) (hdir : DirectedOn (· ≤ ·) S)
    (hpos : ∀ A ∈ S, 0 ≤ A) (hB : IsLUB S B) :
    IsLUB (scalarGNSRepresentation D '' S) (scalarGNSRepresentation D B) := by
  letI : Nonempty S := hne.to_subtype
  letI : IsDirectedOrder S := hdir.isDirectedOrder
  have hrange : Set.range (fun A : S => (A : D.algebra.toStarSubalgebra)) = S := by
    ext A
    simp only [Set.mem_range, Subtype.exists, exists_prop, exists_eq_right]
  have hnet := scalarGNSRepresentation_preserves_positive_isLUB D
    (fun A : S => (A : D.algebra.toStarSubalgebra)) B
    (fun A => hpos A A.property) (fun _ _ h => h) (hrange.symm ▸ hB)
  have himage : Set.range (fun A : S => scalarGNSRepresentation D A.val) =
      scalarGNSRepresentation D '' S := by
    ext A
    simp only [Set.mem_range, Set.mem_image, Subtype.exists, exists_prop]
  rw [himage] at hnet
  exact hnet

#print axioms operator_le_of_sub_nonneg
#print axioms dualOrbitRepresentation_nonneg
#print axioms scalarGNSRepresentation_nonneg
#print axioms scalarGNSRepresentation_monotone
#print axioms scalarGNSRepresentation_preserves_positive_isLUB
#print axioms scalarGNSRepresentation_preserves_positive_directed_isLUB
end
end F1Fecho.RegularScalarGNSNormality
