import TGLExt.V350L2MeasurableCut
import TGLExt.V350L2Translation
import TGLExt.V350StrongOperatorIntegral

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 500000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Isometric embedding of the fibre as constant vectors on the unit interval.
No nonzero constant function on the entire real line is put into L2. -/
def testEmbedding : H →ₗᵢ[ℂ] RegularHilbert H where
  toFun := testVector
  map_add' := fun v w => indicatorConstLp_add.symm
  map_smul' := by
    intro c v
    have he := fibre_testVector (c • (1 : H →L[ℂ] H)) v
    simpa only [fibre_smul, fibre_one, smul_apply, one_apply_eq_self, RingHom.id_apply] using he.symm
  norm_map' := testVector_norm

def testEmbeddingCLM : H →L[ℂ] RegularHilbert H :=
  (testEmbedding (H := H)).toContinuousLinearMap

theorem inner_testVector (v : H) (f : RegularHilbert H) :
    inner ℂ (testVector v) f = inner ℂ v (∫ x in Set.Ioc (0 : ℝ) 1, f x) := by
  rw [L2.inner_def]
  have hi : IntegrableOn f (Set.Ioc (0 : ℝ) 1) volume :=
    integrableOn_Lp_of_measure_ne_top f (by norm_num) (by simp)
  change (∫ x : ℝ, inner ℂ (testVector v x) (f x)) =
    (innerSL ℂ v) (∫ x in Set.Ioc (0 : ℝ) 1, f x)
  rw [← (innerSL ℂ v).integral_comp_comm hi]
  rw [← integral_indicator measurableSet_Ioc]
  apply integral_congr_ae
  filter_upwards [indicatorConstLp_coeFn (p := (2 : ENNReal))
    (hs := measurableSet_Ioc (a := (0 : ℝ)) (b := 1)) (hμs := by simp) (c := v)] with x hx
  change inner ℂ (testVector v x) (f x) = _
  rw [show testVector v x = _ from hx]
  by_cases h : x ∈ Set.Ioc (0 : ℝ) 1
  · simp only [Set.indicator_of_mem h]
    rfl
  · simp only [Set.indicator_of_notMem h, inner_zero_left]

theorem testEmbedding_adjoint (f : RegularHilbert H) :
    testEmbeddingCLM.adjoint f = ∫ x in Set.Ioc (0 : ℝ) 1, f x := by
  apply ext_inner_left ℂ
  intro v
  rw [ContinuousLinearMap.adjoint_inner_right]
  exact inner_testVector v f

/-- Projection onto the constant fibre on (0,1]. -/
def unitIntervalProjection : RegularHilbert H →L[ℂ] RegularHilbert H :=
  testEmbeddingCLM.comp testEmbeddingCLM.adjoint

theorem unitIntervalProjection_apply (f : RegularHilbert H) :
    unitIntervalProjection f = testVector (∫ x in Set.Ioc (0 : ℝ) 1, f x) := by
  change testVector (testEmbeddingCLM.adjoint f) = _
  rw [testEmbedding_adjoint]

theorem testEmbedding_adjoint_embedding :
    testEmbeddingCLM.adjoint.comp (testEmbeddingCLM (H := H)) = 1 := by
  ext v
  apply ext_inner_left ℂ
  intro w
  rw [ContinuousLinearMap.comp_apply, ContinuousLinearMap.adjoint_inner_right]
  exact (testEmbedding (H := H)).inner_map_map w v

theorem unitIntervalProjection_idempotent :
    unitIntervalProjection (H := H) * unitIntervalProjection = unitIntervalProjection := by
  ext1 f
  change testEmbeddingCLM (testEmbeddingCLM.adjoint
    (testEmbeddingCLM (testEmbeddingCLM.adjoint f))) = _
  have he := congrArg (fun T : H →L[ℂ] H => T (testEmbeddingCLM.adjoint f))
    (testEmbedding_adjoint_embedding (H := H))
  change testEmbeddingCLM.adjoint (testEmbeddingCLM (testEmbeddingCLM.adjoint f)) =
    testEmbeddingCLM.adjoint f at he
  rw [he]
  rfl

theorem unitIntervalProjection_selfAdjoint :
    IsSelfAdjoint (unitIntervalProjection (H := H)) := by
  change (unitIntervalProjection (H := H)).adjoint = unitIntervalProjection
  rw [unitIntervalProjection, ContinuousLinearMap.adjoint_comp,
    ContinuousLinearMap.adjoint_adjoint]

#print axioms testEmbedding
#print axioms testEmbedding_adjoint
#print axioms unitIntervalProjection_apply
#print axioms unitIntervalProjection_idempotent
#print axioms unitIntervalProjection_selfAdjoint
end
end TGLV350.Regular
