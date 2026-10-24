import TGLExt.V350L2StrongContinuity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
Strong continuity of uniformly bounded operator families after Lebesgue L²
amplification. The argument uses finite-measure simple functions and uniform
Lipschitz estimates. No operator-norm continuity of the parameter is assumed.
These are continuity statements, not a claim of normality of a star homomorphism.
-/
namespace TGLV350.Regular
open MeasureTheory Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The norm estimate used only for uniform control of the vector variable. -/
theorem fibre_norm_le (T : H →L[ℂ] H) : ‖fibre T‖ ≤ ‖T‖ :=
  ContinuousLinearMap.norm_compLpL_le T

theorem fibre_apply_norm_le (T : H →L[ℂ] H) (f : RegularHilbert H) :
    ‖fibre T f‖ ≤ ‖T‖ * ‖f‖ :=
  ((fibre T).le_opNorm f).trans
    (mul_le_mul_of_nonneg_right (fibre_norm_le T) (norm_nonneg f))

/-- A nonnegative Lipschitz constant is available even when the supplied real
bound C is negative and the indexing type is empty. -/
theorem fibre_lipschitz_of_norm_le (T : H →L[ℂ] H) (C : ℝ) (hT : ‖T‖ ≤ C) :
    LipschitzWith (⟨max C 0, le_max_right C 0⟩ : NNReal) (fibre T) := by
  apply LipschitzWith.of_dist_le_mul
  intro f g
  rw [dist_eq_norm, ← map_sub, dist_eq_norm]
  exact (fibre_apply_norm_le T (f-g)).trans
    (mul_le_mul_of_nonneg_right (hT.trans (le_max_left C 0)) (norm_nonneg (f-g)))

/-- Joint continuity for a strongly continuous, uniformly bounded family.
Z is any topological space; no separability or first-countability is required. -/
theorem fibre_bounded_jointly_continuous {Z : Type*} [TopologicalSpace Z]
    (T : Z → (H →L[ℂ] H)) (C : ℝ) (hbound : ∀ z, ‖T z‖ ≤ C)
    (hT : ∀ v : H, Continuous (fun z => T z v)) :
    Continuous (fun p : RegularHilbert H × Z => fibre (T p.2) p.1) := by
  refine continuous_prod_of_dense_continuous_lipschitzWith _
    (⟨max C 0, le_max_right C 0⟩ : NNReal)
    (Lp.simpleFunc.dense (by norm_num : (2 : ENNReal) ≠ ⊤)) ?_
    (fun z => fibre_lipschitz_of_norm_le (T z) C (hbound z))
  intro f hf
  let g : Lp.simpleFunc H 2 volume := ⟨f, hf⟩
  change Continuous (fun z => fibre (T z) (g : RegularHilbert H))
  induction g using Lp.simpleFunc.induction (p := (2 : ENNReal)) (by norm_num) (by norm_num) with
  | add hfp hgp _ ihf ihg =>
      refine (ihf.add ihg).congr ?_
      intro z
      simp only [AddSubgroup.coe_add, map_add, Pi.add_apply]
  | @indicatorConst v s hs hfinite =>
      simp only [Lp.simpleFunc.coe_indicatorConst, fibre_indicatorConst]
      exact (indicatorConst_continuous hs hfinite.ne).comp (hT v)

theorem fibre_bounded_strongly_continuous {Z : Type*} [TopologicalSpace Z]
    (T : Z → (H →L[ℂ] H)) (C : ℝ) (hbound : ∀ z, ‖T z‖ ≤ C)
    (hT : ∀ v : H, Continuous (fun z => T z v)) (f : RegularHilbert H) :
    Continuous (fun z => fibre (T z) f) :=
  (fibre_bounded_jointly_continuous T C hbound hT).comp
    (continuous_const.prodMk continuous_id)

/-- A uniformly bounded strong operator limit is preserved for an arbitrary
filter, hence also for nets. No topology on the indexing type is needed, and
the limit operator S needs no separately assumed norm bound. -/
theorem fibre_tendsto_of_uniformly_bounded {ι : Type*} {l : Filter ι}
    (T : ι → (H →L[ℂ] H)) (S : H →L[ℂ] H) (C : ℝ)
    (hbound : ∀ i, ‖T i‖ ≤ C)
    (hT : ∀ v : H, Tendsto (fun i => T i v) l (𝓝 (S v)))
    (f : RegularHilbert H) :
    Tendsto (fun i => fibre (T i) f) l (𝓝 (fibre S f)) := by
  have hequi : Equicontinuous (fun i (g : RegularHilbert H) => fibre (T i) g) :=
    (LipschitzWith.uniformEquicontinuous _
      (⟨max C 0, le_max_right C 0⟩ : NNReal)
      (fun i => fibre_lipschitz_of_norm_le (T i) C (hbound i))).equicontinuous
  have hclosed : IsClosed {g : RegularHilbert H |
      Tendsto (fun i => fibre (T i) g) l (𝓝 (fibre S g))} :=
    hequi.isClosed_setOf_tendsto (fibre S).continuous
  refine (Lp.simpleFunc.denseRange (by norm_num : (2 : ENNReal) ≠ ⊤)).induction_on
    f hclosed ?_
  intro g
  induction g using Lp.simpleFunc.induction (p := (2 : ENNReal)) (by norm_num) (by norm_num) with
  | add hfp hgp _ ihf ihg =>
      simpa only [AddSubgroup.coe_add, map_add, Pi.add_apply] using ihf.add ihg
  | @indicatorConst v s hs hfinite =>
      simp only [Lp.simpleFunc.coe_indicatorConst, fibre_indicatorConst]
      exact (indicatorConst_continuous hs hfinite.ne).continuousAt.tendsto.comp (hT v)

#print axioms fibre_norm_le
#print axioms fibre_apply_norm_le
#print axioms fibre_lipschitz_of_norm_le
#print axioms fibre_bounded_jointly_continuous
#print axioms fibre_bounded_strongly_continuous
#print axioms fibre_tendsto_of_uniformly_bounded
end
end TGLV350.Regular
