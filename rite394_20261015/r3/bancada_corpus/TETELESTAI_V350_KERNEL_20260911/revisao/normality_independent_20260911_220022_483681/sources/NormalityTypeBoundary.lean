import TGLV350.RegularNormality
import TGLV350.CoreContractCounterexample
set_option autoImplicit false
set_option maxHeartbeats 1000000
open Filter TGLExt TGLV350.Regular TGL.ModularRealization
open scoped Topology
noncomputable section
universe u
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

-- The order of the algebra subtype is exactly the ambient operator order.
example (N : VonNeumannAlgebra H) (A B : N.toStarSubalgebra) :
    (A ≤ B) ↔ (A.val ≤ B.val) := Iff.rfl
example (N : VonNeumannAlgebra H) (A : N.toStarSubalgebra) :
    (0 ≤ A) ↔ (0 ≤ A.val) := Iff.rfl
example (A B : H →L[ℂ] H) : (A ≤ B) ↔ (B - A).IsPositive :=
  ContinuousLinearMap.le_def A B

-- The space used by fibre remains the actual Lebesgue L2 space.
example (A : H →L[ℂ] H) :
    MeasureTheory.Lp H 2 (MeasureTheory.volume : MeasureTheory.Measure ℝ) →L[ℂ]
      MeasureTheory.Lp H 2 (MeasureTheory.volume : MeasureTheory.Measure ℝ) := fibre A

-- Directedness and nonemptiness produce the nontrivial atTop filter.
example {ι : Type u} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι] :
    (atTop : Filter ι).NeBot := inferInstance

-- This signature uses an internal LUB, without an ambient LUB or SOT premise.
example (N : VonNeumannAlgebra H) {ι : Type u}
    [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → N.toStarSubalgebra) (B : N.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T) (hB : IsLUB (Set.range T) B) :
    IsLUB (Set.range (fun i => (T i).val)) B.val :=
  vonNeumann_isLUB_coe N T B hpos hmono hB

-- The complete codomain algebra, not only the image of the embedding, supplies upper bounds.
example (P : SiteProfile) (S : Set (theFactorObject P).toStarSubalgebra)
    (B : (theFactorObject P).toStarSubalgebra)
    (hne : S.Nonempty) (hdir : DirectedOn (· ≤ ·) S)
    (hpos : ∀ A ∈ S, 0 ≤ A) (hB : IsLUB S B)
    (D : (regularCoreAlgebra P).toStarSubalgebra)
    (hD : ∀ A ∈ S, regularCoreEmbedding P A ≤ D) :
    regularCoreEmbedding P B ≤ D := by
  apply (regularCoreEmbedding_preserves_positive_directed_isLUB P S B hne hdir hpos hB).2
  rintro _ ⟨A, hA, rfl⟩
  exact hD A hA

-- The legacy countermodel cannot provide the third layer for this same core.
example (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (D : WedgeModularData W) :
    IsEmpty (ThreeLocksCoreData W D (TGLV350.ContractAudit.zeroTraceLegacyCore W D)) :=
  ⟨fun T => TGLV350.ContractAudit.zeroTraceLegacyCore_has_no_threeLocks W D ⟨T⟩⟩
end
