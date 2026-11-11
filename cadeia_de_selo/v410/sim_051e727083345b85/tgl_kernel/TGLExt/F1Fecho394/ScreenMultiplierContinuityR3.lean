import TGLExt.F1Fecho394.ScreenMatrixMultiplierR4
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Dominated convergence for the constructed unitary screen multipliers. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

theorem H1_integral_norm_sq (f : H1) :
    (∫ p, ‖f p‖^2 ∂orbitalMeasure 0)=‖f‖^2 := by
  have h := congrArg (RCLike.re : ℂ → ℝ) (L2.inner_def (𝕜:=ℂ) f f)
  rw [←integral_re (L2.integrable_inner (𝕜:=ℂ) f f)] at h
  simpa only [inner_self_eq_norm_sq] using h.symm

theorem matrixMultiplier_continuousAt {X : Type*} [TopologicalSpace X] [FirstCountableTopology X]
    (A : X → MomentumCoordinates → Matrix (Fin 2) (Fin 2) ℂ)
    (hm : ∀ x, Measurable (A x))
    (hu : ∀ x, ∀ᵐ p ∂orbitalMeasure 0, A x p ∈ Matrix.unitaryGroup (Fin 2) ℂ)
    (x : X) (hc : ∀ᵐ p ∂orbitalMeasure 0, ContinuousAt (fun y => A y p) x) (f : H1) :
    ContinuousAt (fun y => matrixMultiplier (A y) (hm y) (hu y) f) x := by
  let g := fun y p => matrixFiberOperator (A y p) (f p)
  have hgm (y : X) : AEStronglyMeasurable (g y) (orbitalMeasure 0) := by
    exact (ContinuousLinearMap.id ℂ FiberOperator).aestronglyMeasurable_comp₂
      ((matrixFiberOperator_continuous.measurable.comp (hm y)).aestronglyMeasurable)
      (Lp.aestronglyMeasurable f)
  have hb (y : X) : ∀ᵐ p ∂orbitalMeasure 0, ‖g y p-g x p‖^2 ≤ 4*‖f p‖^2 := by
    filter_upwards [hu y,hu x] with p hy hx
    have hy' := matrixFiberOperator_norm (A y p) hy (f p)
    have hx' := matrixFiberOperator_norm (A x p) hx (f p)
    have hn : ‖g y p-g x p‖≤2*‖f p‖ := (norm_sub_le _ _).trans (by dsimp [g]; rw [hy',hx']; ring_nf; rfl)
    calc
      _ ≤ (2*‖f p‖)^2 := pow_le_pow_left₀ (norm_nonneg _) hn 2
      _ = _ := by ring
  have hi : Tendsto (fun y => ∫ p, ‖g y p-g x p‖^2 ∂orbitalMeasure 0)
      (𝓝 x) (𝓝 (∫ _p, (0:ℝ) ∂orbitalMeasure 0)) := by
    apply tendsto_integral_filter_of_dominated_convergence (fun p => 4*‖f p‖^2)
    · exact Eventually.of_forall fun y => ((hgm y).sub (hgm x)).norm.pow 2
    · exact Eventually.of_forall fun y => (hb y).mono fun p hp => by
        simpa only [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg (‖g y p-g x p‖))] using hp
    · exact ((memLp_two_iff_integrable_sq_norm (Lp.memLp f).1).mp (Lp.memLp f)).const_mul 4
    · filter_upwards [hc] with p hp
      have hg : ContinuousAt (fun y => g y p) x :=
        (matrixFiberOperator_continuous.continuousAt.comp hp).clm_apply continuousAt_const
      simpa only [sub_self,norm_zero,zero_pow (by decide : (2:ℕ)≠0)] using
        ((hg.tendsto.sub (tendsto_const_nhds (x:=g x p))).norm.pow 2)
  have he (y : X) :
      ‖matrixMultiplier (A y) (hm y) (hu y) f-matrixMultiplier (A x) (hm x) (hu x) f‖^2 =
        ∫ p, ‖g y p-g x p‖^2 ∂orbitalMeasure 0 := by
    rw [←H1_integral_norm_sq]
    apply integral_congr_ae
    filter_upwards [Lp.coeFn_sub (matrixMultiplier (A y) (hm y) (hu y) f)
      (matrixMultiplier (A x) (hm x) (hu x) f),matrixMultiplier_ae (A y) (hm y) (hu y) f,
      matrixMultiplier_ae (A x) (hm x) (hu x) f] with p hp hy hx
    simp only [hp,Pi.sub_apply,hy,hx]
    rfl
  have hn := Real.continuous_sqrt.continuousAt.tendsto.comp hi
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [←he,integral_zero,Function.comp_def,Real.sqrt_sq_eq_abs,abs_norm,
    Real.sqrt_zero,dist_eq_norm] using hn

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.matrixMultiplier_continuousAt
