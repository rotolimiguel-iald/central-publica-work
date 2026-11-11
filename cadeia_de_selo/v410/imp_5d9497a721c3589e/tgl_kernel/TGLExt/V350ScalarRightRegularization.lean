import TGLExt.V350ScalarWeightAction
import Mathlib.Analysis.Normed.Operator.Extend

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

def scalarRightRegularizationLinear (P : SiteProfile) (h : ℝ) :
    scalarWeightLeftIdeal P →ₗ[ℂ] scalarWeightLeftIdeal P where
  toFun := fun a => scalarWeightRightRegularization P a h
  map_add' := by
    intro a b
    apply Subtype.ext
    apply Subtype.ext
    exact add_mul _ _ _
  map_smul' := by
    intro c a
    apply Subtype.ext
    apply Subtype.ext
    exact smul_mul_assoc _ _ _

theorem scalarWeightRightRegularization_norm_le (P : SiteProfile)
    (a : scalarWeightLeftIdeal P) (h : ℝ) :
    ‖scalarWeightGNSEmbedding P (scalarWeightRightRegularization P a h)‖ ≤
      ‖scalarWeightGNSEmbedding P a‖ := by
  have he := scalarWeight_right_average_le P a.val h
  change dualQuadraticIntegral
      (star (scalarWeightRightRegularization P a h).val.val *
        (scalarWeightRightRegularization P a h).val.val) (regularVacuum P) ≤ _ at he
  rw [← scalarWeightGNSEmbedding_norm_sq,← scalarWeightGNSEmbedding_norm_sq] at he
  have hs := ENNReal.toReal_mono ENNReal.ofReal_ne_top he
  simp only [ENNReal.toReal_ofReal (sq_nonneg _)] at hs
  exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mp hs

/-- The right average is constructed on the original full weight ideal,
then extended by its measured GNS norm bound. No inverse Gaussian map. -/
def scalarRightRegularization (P : SiteProfile) (h : ℝ) :
    ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
  ((scalarWeightGNSEmbedding P).comp (scalarRightRegularizationLinear P h)).extendOfNorm
    (scalarWeightGNSEmbedding P)

theorem scalarRightRegularization_embedding (P : SiteProfile) (h : ℝ)
    (a : scalarWeightLeftIdeal P) :
    scalarRightRegularization P h (scalarWeightGNSEmbedding P a) =
      scalarWeightGNSEmbedding P (scalarWeightRightRegularization P a h) := by
  apply LinearMap.extendOfNorm_eq (scalarWeightGNSEmbedding_denseRange P)
  refine ⟨1,fun a => ?_⟩
  change ‖scalarWeightGNSEmbedding P (scalarWeightRightRegularization P a h)‖ ≤
    1 * ‖scalarWeightGNSEmbedding P a‖
  simpa only [one_mul] using scalarWeightRightRegularization_norm_le P a h

theorem scalarRightRegularization_norm_le (P : SiteProfile) (h : ℝ) :
    ‖scalarRightRegularization P h‖ ≤ 1 := by
  apply LinearMap.opNorm_extendOfNorm_le (scalarWeightGNSEmbedding_denseRange P) (by norm_num)
  intro a
  change ‖scalarWeightGNSEmbedding P (scalarWeightRightRegularization P a h)‖ ≤
    1 * ‖scalarWeightGNSEmbedding P a‖
  simpa only [one_mul] using scalarWeightRightRegularization_norm_le P a h

theorem scalarRightRegularization_commutes (P : SiteProfile) (h : ℝ)
    (b : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (scalarRightRegularization P h) (scalarGNSRepresentation P b) := by
  ext1 x
  refine (scalarWeightGNSEmbedding_denseRange P).induction_on x
    (isClosed_eq (by fun_prop) (by fun_prop)) ?_
  intro a
  change scalarRightRegularization P h
      (scalarGNSRepresentation P b (scalarWeightGNSEmbedding P a)) =
    scalarGNSRepresentation P b
      (scalarRightRegularization P h (scalarWeightGNSEmbedding P a))
  conv_lhs => rw [scalarWeightGNSAction_intertwines P b a]
  conv_lhs => rw [scalarRightRegularization_embedding P h (scalarWeightLeftProduct P b a)]
  conv_rhs => rw [scalarRightRegularization_embedding P h a]
  conv_rhs => rw [scalarWeightGNSAction_intertwines P b (scalarWeightRightRegularization P a h)]
  congr 1

theorem scalarRightRegularization_tendsto (P : SiteProfile) (x : ScalarGNSHilbert P) :
    Tendsto (fun h : ℝ => scalarRightRegularization P h x) (𝓝[≠] 0) (𝓝 x) := by
  have hlip (h : ℝ) : LipschitzWith 1 (scalarRightRegularization P h) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    rw [dist_eq_norm,← map_sub,dist_eq_norm]
    exact ((scalarRightRegularization P h).le_opNorm (x-y)).trans
      (mul_le_mul_of_nonneg_right (scalarRightRegularization_norm_le P h) (norm_nonneg _))
  have hequi : Equicontinuous (fun h : ℝ => scalarRightRegularization P h) :=
    (LipschitzWith.uniformEquicontinuous _ 1 hlip).equicontinuous
  have hc : IsClosed {x : ScalarGNSHilbert P |
      Tendsto (fun h : ℝ => scalarRightRegularization P h x) (𝓝[≠] 0) (𝓝 x)} :=
    hequi.isClosed_setOf_tendsto continuous_id
  refine (scalarWeightGNSEmbedding_denseRange P).induction_on x hc ?_
  intro a
  simp only [scalarRightRegularization_embedding]
  exact tendsto_subtype_rng.mpr (scalarWeightOrbit_rightRegularization_tendsto P a)

def scalarRegularizationVector (P : SiteProfile) (h : ℝ) (hh : 0 < h) :
    ScalarGNSHilbert P :=
  scalarGNSEmbedding P ⟨⟨regularAverage P h,regularAverage_mem P h⟩,
    regularAverage_hasFiniteDualSquare P h hh⟩

theorem scalarRightRegularization_vector (P : SiteProfile) (h : ℝ) (hh : 0 < h)
    (a : scalarWeightLeftIdeal P) :
    scalarRightRegularization P h (scalarWeightGNSEmbedding P a) =
      scalarGNSRepresentation P a.val (scalarRegularizationVector P h hh) := by
  rw [scalarRightRegularization_embedding]
  unfold scalarRegularizationVector
  rw [← scalarWeightGNSEmbedding_uniform,scalarWeightGNSAction_intertwines]
  rfl

#print axioms scalarRightRegularizationLinear
#print axioms scalarWeightRightRegularization_norm_le
#print axioms scalarRightRegularization
#print axioms scalarRightRegularization_embedding
#print axioms scalarRightRegularization_norm_le
#print axioms scalarRightRegularization_commutes
#print axioms scalarRightRegularization_tendsto
#print axioms scalarRegularizationVector
#print axioms scalarRightRegularization_vector
end
end TGLV350.Regular
