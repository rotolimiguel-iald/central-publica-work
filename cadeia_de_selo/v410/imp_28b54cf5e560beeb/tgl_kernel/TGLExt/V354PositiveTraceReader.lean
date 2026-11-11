import TGLExt.V354RegularSupport

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt TGLV351 TGL.ContinuousCorner
noncomputable section

/-- Total reader required by ContinuousCornerWitness's old signature.
It agrees with A1 on EVERY positive input. The value zero outside that cone
is a reader convention, NOT a cyclic trace on the whole ring. -/
def positiveTraceReader (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) : ENNReal := by
  classical
  exact if h : 0 ≤ a.val then scalarInverseLimitWeight P ⟨a.val,a.property,h⟩ else 0

theorem positiveTraceReader_positive (P : SiteProfile) (a : PositiveCoreInput P) :
    positiveTraceReader P ⟨a.val,a.property.1⟩ = scalarInverseLimitWeight P a := by
  simp only [positiveTraceReader,dif_pos a.property.2]

/-- The existing corner consumer, with all its positive readings anchored to
A1. This is not ContinuousCoreData: no global cyclicity is asserted for the reader. -/
def regularContinuousCorner (P : SiteProfile) : ContinuousCornerWitness where
  Core := (regularCoreAlgebra P).toStarSubalgebra
  P := ⟨(regularFiniteSupport P).val,(regularFiniteSupport P).property.1⟩
  Pplus := ⟨(regularNormalizedFaces P).val.1.val,(regularNormalizedFaces P).val.1.property.1⟩
  Pminus := ⟨(regularNormalizedFaces P).val.2.val,(regularNormalizedFaces P).val.2.property.1⟩
  trace := positiveTraceReader P
  P_selfAdjoint := Subtype.ext (regularFiniteSupport_projection P).isSelfAdjoint.star_eq
  P_idempotent := Subtype.ext (regularFiniteSupport_projection P).isIdempotentElem
  Pplus_selfAdjoint := Subtype.ext (regularNormalizedFaces P).property.1.isSelfAdjoint.star_eq
  Pplus_idempotent := Subtype.ext (regularNormalizedFaces P).property.1.isIdempotentElem
  Pminus_selfAdjoint := Subtype.ext (regularNormalizedFaces P).property.2.1.isSelfAdjoint.star_eq
  Pminus_idempotent := Subtype.ext (regularNormalizedFaces P).property.2.1.isIdempotentElem
  split := rfl
  orthogonal := Subtype.ext (regularNormalizedFaces P).property.2.2.1
  trace_additive_on_split := by
    rw [positiveTraceReader_positive,positiveTraceReader_positive,positiveTraceReader_positive]
    exact scalarInverseLimitWeight_add P _ _
  trace_P_pos := by
    rw [positiveTraceReader_positive,regularFiniteSupport_trace]
    exact zero_lt_one
  trace_P_finite := by
    rw [positiveTraceReader_positive,regularFiniteSupport_trace]
    exact ENNReal.one_lt_top
  equal_face_trace := by
    rw [positiveTraceReader_positive,positiveTraceReader_positive]
    exact (regularNormalizedFaces P).property.2.2.2.2

/-- An actual term of the old corner interface, without a witness premise.
The already proved corner laws supply the normalized readings. -/
theorem regularContinuousCorner_readings (P : SiteProfile) :
    (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).P = 1 ∧
    (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pplus = 1/2 ∧
    (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pminus = 1/2 :=
  ⟨(regularContinuousCorner P).normalizedTrace_P_eq_one,
    (regularContinuousCorner P).equalFaces_normalizedTrace_half⟩

/-- Genuine A1 trace on the zero spectral projection of the constructed
affiliated minimal representative. No finite Hilbert rank is used. -/
theorem regularMinimalLock_breuer_kernel (P : SiteProfile) :
    ∃ p : PositiveCoreInput P,
      p.val = (regularMinimalLock P).ker.starProjection ∧
      scalarInverseLimitWeight P p = 1 ∧
      0 < scalarInverseLimitWeight P p ∧ scalarInverseLimitWeight P p < ⊤ := by
  refine ⟨regularFiniteSupport P,(regularMinimalLock_spectral_zero P).symm,
    regularFiniteSupport_trace P,?_,?_⟩
  · rw [regularFiniteSupport_trace]; exact zero_lt_one
  · rw [regularFiniteSupport_trace]; exact ENNReal.one_lt_top

#print axioms positiveTraceReader
#print axioms positiveTraceReader_positive
#print axioms regularContinuousCorner
#print axioms regularContinuousCorner_readings
#print axioms regularMinimalLock_breuer_kernel
end
end TGLV350.Regular
