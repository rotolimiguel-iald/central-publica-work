import TGLExt.V350L2OperatorLift

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem fibre_isometry_norm (U : H →ₗᵢ[ℂ] H) (f : RegularHilbert H) :
    ‖fibre U.toContinuousLinearMap f‖ = ‖f‖ := by
  rw [Lp.norm_def, Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [fibre_ae U.toContinuousLinearMap f] with x hx
  rw [hx]
  exact U.norm_map (f x)

def fibreIsometry (U : H →ₗᵢ[ℂ] H) : RegularHilbert H →ₗᵢ[ℂ] RegularHilbert H where
  toLinearMap := (fibre U.toContinuousLinearMap).toLinearMap
  norm_map' := fibre_isometry_norm U

theorem fibre_indicatorConst (T : H →L[ℂ] H) {s : Set ℝ}
    (hs : MeasurableSet s) (hfinite : volume s ≠ ⊤) (v : H) :
    fibre T (indicatorConstLp 2 hs hfinite v) = indicatorConstLp 2 hs hfinite (T v) := by
  apply Lp.ext
  filter_upwards [fibre_ae T (indicatorConstLp 2 hs hfinite v),
    indicatorConstLp_coeFn (p := (2 : ENNReal)) (hs := hs) (hμs := hfinite) (c := v),
    indicatorConstLp_coeFn (p := (2 : ENNReal)) (hs := hs) (hμs := hfinite) (c := T v)]
    with x h1 h2 h3
  rw [h1, h2, h3]
  by_cases hx : x ∈ s
  · simp only [Set.indicator_of_mem hx]
  · simp only [Set.indicator_of_notMem hx, map_zero]

theorem indicatorConst_continuous {s : Set ℝ}
    (hs : MeasurableSet s) (hfinite : volume s ≠ ⊤) :
    Continuous (fun v : H => indicatorConstLp 2 hs hfinite v) := by
  let K : NNReal := ⟨volume.real s ^ (1 / (2 : ENNReal).toReal), by positivity⟩
  have hL : LipschitzWith K (fun v : H => indicatorConstLp 2 hs hfinite v) := by
    apply LipschitzWith.of_dist_le_mul
    intro v w
    rw [dist_eq_norm, indicatorConstLp_sub, norm_indicatorConstLp (by norm_num) (by norm_num),
      dist_eq_norm]
    exact le_of_eq (mul_comm _ _)
  exact hL.continuous

/-- A uniformly isometric strongly continuous family lifts to Lebesgue L².
The proof uses density of finite-measure simple functions; it assumes no operator-norm
continuity and makes no compactness assumption on the time parameter. -/
theorem fibre_jointly_continuous {Z : Type} [TopologicalSpace Z]
    (U : Z → (H →ₗᵢ[ℂ] H)) (hU : ∀ v : H, Continuous (fun z => U z v)) :
    Continuous (fun z : RegularHilbert H × Z => fibre (U z.2).toContinuousLinearMap z.1) := by
  refine continuous_prod_of_dense_continuous_lipschitzWith _ 1
    (Lp.simpleFunc.dense (by norm_num : (2 : ENNReal) ≠ ⊤)) ?_
    (fun z => (fibreIsometry (U z)).isometry.lipschitz)
  intro f hf
  let g : Lp.simpleFunc H 2 volume := ⟨f, hf⟩
  change Continuous (fun z => fibre (U z).toContinuousLinearMap (g : RegularHilbert H))
  induction g using Lp.simpleFunc.induction (p := (2 : ENNReal)) (by norm_num) (by norm_num) with
  | add hfp hgp _ ihf ihg =>
      refine (ihf.add ihg).congr ?_
      intro z
      simp only [AddSubgroup.coe_add, map_add, Pi.add_apply]
  | @indicatorConst v s hs hfinite =>
      simp only [Lp.simpleFunc.coe_indicatorConst, fibre_indicatorConst]
      exact (indicatorConst_continuous hs hfinite.ne).comp (hU v)

theorem fibre_strongly_continuous {Z : Type} [TopologicalSpace Z]
    (U : Z → (H →ₗᵢ[ℂ] H)) (hU : ∀ v : H, Continuous (fun z => U z v))
    (f : RegularHilbert H) : Continuous (fun z => fibre (U z).toContinuousLinearMap f) :=
  (fibre_jointly_continuous U hU).comp (continuous_const.prodMk continuous_id)

#print axioms fibreIsometry
#print axioms fibre_jointly_continuous
#print axioms fibre_strongly_continuous
end
end TGLV350.Regular
