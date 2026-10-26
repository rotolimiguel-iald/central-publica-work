import TGLExt.V351ResolventImaginaryPowers
import Mathlib.Topology.EMetricSpace.Lipschitz

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The damped family is norm continuous; the undamped group need not be. -/
theorem resolventPhaseOperator_continuous (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) :
    Continuous (resolventPhaseOperator T) := by
  let f : ℝ → C(spectrum ℂ T,ℂ) := fun t =>
    ⟨fun z => resolventPhaseFunction t (z.val.re),
      (resolventPhaseFunction_continuous t).comp
        (Complex.continuous_re.comp continuous_subtype_val)⟩
  have hf : Continuous f := by
    apply ContinuousMap.continuous_of_continuous_uncurry
    exact resolventPhaseFunction_joint_continuous.comp
      (continuous_fst.prodMk (Complex.continuous_re.comp
        (continuous_subtype_val.comp continuous_snd)))
  have hc := (cfcHom_continuous hT.isStarNormal).comp hf
  apply hc.congr
  intro t
  exact (cfc_apply (fun z : ℂ => resolventPhaseFunction t z.re) T hT.isStarNormal
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn).symm

theorem resolventImaginaryPower_joint_continuous (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) :
    Continuous (fun p : H × ℝ => resolventImaginaryPower T hT h1 hi hj p.2 p.1) := by
  refine continuous_prod_of_dense_continuous_lipschitzWith _ 1
    (resolventDampingOperator_denseRange T hT h1 hi hj) ?_
    (fun t => (resolventImaginaryPower T hT h1 hi hj t).isometry.lipschitz)
  rintro _ ⟨y,rfl⟩
  simp only [resolventImaginaryPower_damping]
  exact (resolventPhaseOperator_continuous T (IsSelfAdjoint.of_nonneg hT)).clm_apply continuous_const

theorem resolventImaginaryPower_strongly_continuous (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (x : H) :
    Continuous (fun t : ℝ => resolventImaginaryPower T hT h1 hi hj t x) := by
  have hf : Continuous (fun t : ℝ => (x,t)) := continuous_const.prodMk continuous_id
  have hc := (resolventImaginaryPower_joint_continuous T hT h1 hi hj).comp hf
  simpa only [Function.comp_def] using hc

#print axioms resolventPhaseOperator_continuous
#print axioms resolventImaginaryPower_joint_continuous
#print axioms resolventImaginaryPower_strongly_continuous
end
end TGLV350.Regular
