import TGLExt.V350ScalarCutCyclicSpace
import TGLExt.V350ScalarCutVectorFunctional

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology
noncomputable section

theorem scalarCutCyclicVector_functional (P : SiteProfile) (R : ℝ) (hR : 0 ≤ R)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    inner ℂ (scalarCutCyclicVector P R)
      (scalarCutRepresentation P R B (scalarCutCyclicVector P R)) =
      dualCutFunctional R (regularVacuum P) B.val := by
  change inner ℂ (scalarCutCyclicVector P R).val
    (dualOrbitRepresentation B.val (scalarCutCyclicVector P R).val) = _
  rw [scalarCutCyclicVector_val]
  exact scalarCutVacuum_inner_action P R hR B.val

theorem scalarCutEmbedding_norm_sq (P : SiteProfile) (R : ℝ) (hR : 0 ≤ R)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    ‖scalarCutEmbedding P R A‖ ^ 2 =
      (dualCutFunctional R (regularVacuum P) (star A.val * A.val)).re :=
  scalarCutLinear_norm_sq P R hR A.val

theorem scalarGNSCutCyclicMap_embedding (P : SiteProfile) (R : ℝ)
    (A : finiteDualLeftIdeal P) :
    scalarGNSCutCyclicMap P R (scalarGNSEmbedding P A) = scalarCutEmbedding P R A.val := by
  apply Subtype.ext
  exact scalarGNSCutMap_embedding_eq_action P R A

theorem scalarGNSCutCyclicMap_intertwines (P : SiteProfile) (R : ℝ)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) :
    scalarGNSCutCyclicMap P R (scalarGNSRepresentation P B v) =
      scalarCutRepresentation P R B (scalarGNSCutCyclicMap P R v) := by
  apply Subtype.ext
  exact scalarGNSCutMap_intertwines P R B v

theorem scalarGNSCutCyclicMap_norm_le (P : SiteProfile) (R : ℝ)
    (v : ScalarGNSHilbert P) : ‖scalarGNSCutCyclicMap P R v‖ ≤ ‖v‖ :=
  scalarGNSCutMap_norm_le P R v

theorem scalarGNSCutCyclicMap_joint_zero (P : SiteProfile) (v : ScalarGNSHilbert P)
    (h : ∀ n : ℕ, scalarGNSCutCyclicMap P (n : ℝ) v = 0) : v = 0 := by
  apply scalarGNSCutMap_joint_zero P v
  intro n
  exact congrArg Subtype.val (h n)

/-- Each contraction has dense range in its concrete cyclic GNS target.
This asserts neither surjectivity nor injectivity of an individual contraction. -/
theorem scalarGNSCutCyclicMap_denseRange (P : SiteProfile) (R : ℝ) :
    DenseRange (scalarGNSCutCyclicMap P R) := by
  have hr : Set.range (scalarCutEmbedding P R) ⊆
      closure (Set.range (scalarGNSCutCyclicMap P R)) := by
    rintro v ⟨B,rfl⟩
    let F (h : ℝ) : (regularCoreAlgebra P).toStarSubalgebra :=
      B * ⟨regularAverage P h,regularAverage_mem P h⟩
    have hb (h : ℝ) : ‖B.val * regularAverage P h‖ ≤ ‖B.val‖ := by
      have hc := mul_le_mul_of_nonneg_left (regularAverage_norm_le_one P h) (norm_nonneg B.val)
      exact (norm_mul_le _ _).trans (by simpa only [mul_one] using hc)
    have ht := dualOrbit_tendsto_of_uniformly_bounded
      (fun h : ℝ => B.val * regularAverage P h) B.val ‖B.val‖ hb
      (regularAverage_mul_tendsto P B.val) (scalarCutVacuum P R)
    have ht' : Tendsto (fun h : ℝ => scalarCutEmbedding P R (F h)) (𝓝[>] 0)
        (𝓝 (scalarCutEmbedding P R B)) :=
      tendsto_subtype_rng.mpr (ht.mono_left (nhdsGT_le_nhdsNE 0))
    apply isClosed_closure.mem_of_tendsto ht'
    filter_upwards [self_mem_nhdsWithin] with h hh
    let A : finiteDualLeftIdeal P := scalarGNSLeftProduct P B
      ⟨⟨regularAverage P h,regularAverage_mem P h⟩,regularAverage_hasFiniteDualSquare P h hh⟩
    apply subset_closure
    exact ⟨scalarGNSEmbedding P A,scalarGNSCutCyclicMap_embedding P R A⟩
  intro v
  exact (closure_minimal hr isClosed_closure) (scalarCutEmbedding_denseRange P R v)

#print axioms scalarCutCyclicVector_functional
#print axioms scalarCutEmbedding_norm_sq
#print axioms scalarGNSCutCyclicMap_embedding
#print axioms scalarGNSCutCyclicMap_intertwines
#print axioms scalarGNSCutCyclicMap_norm_le
#print axioms scalarGNSCutCyclicMap_joint_zero
#print axioms scalarGNSCutCyclicMap_denseRange
end
end TGLV350.Regular
