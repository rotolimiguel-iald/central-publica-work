import TGLExt.V350ScalarCutVacuum

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
noncomputable section

def scalarCutLinear (P : SiteProfile) (R : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra →ₗ[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)) where
  toFun A := dualOrbitRepresentation A.val (scalarCutVacuum P R)
  map_add' A B := by
    change dualOrbitRepresentation (A.val+B.val) _ = _
    rw [map_add]
    rfl
  map_smul' c A := by
    change dualOrbitRepresentation (c • A.val) _ = _
    rw [map_smul]
    rfl

def scalarCutSubspace (P : SiteProfile) (R : ℝ) :
    Submodule ℂ (RegularHilbert (RegularHilbert (TowerHilbert P))) :=
  (scalarCutLinear P R).range.topologicalClosure

abbrev ScalarCutHilbert (P : SiteProfile) (R : ℝ) := scalarCutSubspace P R

instance scalarCutCompleteSpace (P : SiteProfile) (R : ℝ) :
    CompleteSpace (ScalarCutHilbert P R) :=
  Submodule.topologicalClosure.completeSpace (scalarCutLinear P R).range

def scalarCutEmbedding (P : SiteProfile) (R : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra →ₗ[ℂ] ScalarCutHilbert P R :=
  (scalarCutLinear P R).codRestrict (scalarCutSubspace P R)
    (fun A => (scalarCutLinear P R).range.le_topologicalClosure ⟨A,rfl⟩)

theorem scalarCutAmbientAction_preserves (P : SiteProfile) (R : ℝ)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    ∀ v ∈ scalarCutSubspace P R,
      dualOrbitRepresentation B.val v ∈ scalarCutSubspace P R := by
  have h : Set.MapsTo (dualOrbitRepresentation B.val)
      ((scalarCutLinear P R).range : Set _) ((scalarCutLinear P R).range : Set _) := by
    rintro v ⟨A,rfl⟩
    refine ⟨B*A,?_⟩
    change dualOrbitRepresentation (B.val*A.val) _ = _
    rw [map_mul]
    rfl
  exact h.closure (dualOrbitRepresentation B.val).continuous

def scalarCutRepresentation (P : SiteProfile) (R : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra →⋆ₐ[ℂ]
      (ScalarCutHilbert P R →L[ℂ] ScalarCutHilbert P R) :=
  reducingStarRepresentation
    (dualOrbitRepresentation.comp (regularCoreAlgebra P).toStarSubalgebra.subtype)
    (scalarCutSubspace P R) (scalarCutAmbientAction_preserves P R)

def scalarCutCyclicVector (P : SiteProfile) (R : ℝ) : ScalarCutHilbert P R :=
  scalarCutEmbedding P R 1

theorem scalarCutCyclicVector_val (P : SiteProfile) (R : ℝ) :
    (scalarCutCyclicVector P R).val = scalarCutVacuum P R := by
  change dualOrbitRepresentation 1 (scalarCutVacuum P R) = _
  rw [map_one,one_apply_eq_self]

theorem scalarCutRepresentation_intertwines (P : SiteProfile) (R : ℝ)
    (B A : (regularCoreAlgebra P).toStarSubalgebra) :
    scalarCutRepresentation P R B (scalarCutEmbedding P R A) =
      scalarCutEmbedding P R (B*A) := by
  apply Subtype.ext
  change dualOrbitRepresentation B.val (dualOrbitRepresentation A.val (scalarCutVacuum P R)) =
    dualOrbitRepresentation (B.val*A.val) (scalarCutVacuum P R)
  rw [map_mul]
  rfl

theorem scalarCutEmbedding_denseRange (P : SiteProfile) (R : ℝ) :
    DenseRange (scalarCutEmbedding P R) := by
  let f := scalarCutLinear P R
  have h : DenseRange (Set.inclusion (s := Set.range f) subset_closure) :=
    (denseRange_inclusion_iff subset_closure).2 subset_rfl
  exact h.comp Set.rangeFactorization_surjective.denseRange (continuous_inclusion subset_closure)

theorem scalarCutCyclicVector_generates (P : SiteProfile) (R : ℝ) :
    DenseRange (fun B : (regularCoreAlgebra P).toStarSubalgebra =>
      scalarCutRepresentation P R B (scalarCutCyclicVector P R)) := by
  have he : (fun B : (regularCoreAlgebra P).toStarSubalgebra =>
      scalarCutRepresentation P R B (scalarCutCyclicVector P R)) =
      (fun B => scalarCutEmbedding P R B) := by
    funext B
    change scalarCutRepresentation P R B (scalarCutEmbedding P R 1) = _
    rw [scalarCutRepresentation_intertwines,mul_one]
  rw [he]
  exact scalarCutEmbedding_denseRange P R

/-- The cut of every vector of H_I lies in this cyclic space, by Hilbert-norm density.
This does not assert that the cut preserves H_I itself. -/
theorem scalarGNSCutMap_mem_cyclicSubspace (P : SiteProfile) (R : ℝ)
    (v : ScalarGNSHilbert P) : scalarGNSCutMap P R v ∈ scalarCutSubspace P R := by
  have hc : IsClosed {v : ScalarGNSHilbert P |
      scalarGNSCutMap P R v ∈ scalarCutSubspace P R} := by
    change IsClosed ((scalarGNSCutMap P R) ⁻¹' closure (Set.range (scalarCutLinear P R)))
    exact isClosed_closure.preimage (scalarGNSCutMap P R).continuous
  refine (scalarGNSEmbedding_denseRange P).induction_on v hc ?_
  intro A
  rw [scalarGNSCutMap_embedding_eq_action]
  exact (scalarCutLinear P R).range.le_topologicalClosure ⟨A.val,rfl⟩

def scalarGNSCutCyclicMap (P : SiteProfile) (R : ℝ) :
    ScalarGNSHilbert P →L[ℂ] ScalarCutHilbert P R :=
  (scalarGNSCutMap P R).codRestrict (scalarCutSubspace P R)
    (scalarGNSCutMap_mem_cyclicSubspace P R)

#print axioms scalarCutLinear
#print axioms scalarCutSubspace
#print axioms scalarCutCompleteSpace
#print axioms scalarCutEmbedding
#print axioms scalarCutAmbientAction_preserves
#print axioms scalarCutRepresentation
#print axioms scalarCutCyclicVector
#print axioms scalarCutCyclicVector_val
#print axioms scalarCutRepresentation_intertwines
#print axioms scalarCutEmbedding_denseRange
#print axioms scalarCutCyclicVector_generates
#print axioms scalarGNSCutMap_mem_cyclicSubspace
#print axioms scalarGNSCutCyclicMap
end
end TGLV350.Regular
