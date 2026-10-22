import TGLExt.V351ScaledResolventCalculus
import TGLExt.V350ScaledRootGraphTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open ChatgptAudit
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem scaledResolventDamping_denseRange (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r) :
    DenseRange (resolventDampingOperator (scaledPositiveResolvent T r)) := by
  have hd := resolventDampingOperator_denseRange T hT h1 hi hj
  apply hd.mono
  rintro _ ⟨x,rfl⟩
  obtain ⟨y,hy⟩ := unit_operator_surjective (scaledResolventDampingOperator T r)
    (scaledResolventDampingOperator_isUnit T hT h1 r hr) x
  refine ⟨y,?_⟩
  rw [scaledPositiveResolvent_damping T hT h1 r hr]
  change resolventDampingOperator T (scaledResolventDampingOperator T r y)=_
  rw [hy]

/-- Scaling of the same imaginary powers, with no inverse assumed for the intertwiner. -/
theorem resolventImaginaryPower_scaled_intertwining (T R : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r)
    (hR : T*R=R*scaledPositiveResolvent T r) (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (R x)=
      modularPhase t (Real.log r) • R (resolventImaginaryPower T hT h1 hi hj t x) := by
  refine (scaledResolventDamping_denseRange T hT h1 hi hj r hr).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  have hb := congrArg (fun A : H →L[ℂ] H => A y)
    (resolventDampingOperator_intertwines T (scaledPositiveResolvent T r) R hR)
  change resolventDampingOperator T (R y)=R (resolventDampingOperator (scaledPositiveResolvent T r) y) at hb
  rw [← hb,resolventImaginaryPower_damping]
  have hc := congrArg (fun A : H →L[ℂ] H => A y)
    (resolventPhaseOperator_intertwines T (scaledPositiveResolvent T r) R
      (IsSelfAdjoint.of_nonneg hT) (IsSelfAdjoint.of_nonneg (scaledPositiveResolvent_nonneg T hT h1 r hr)) hR t)
  change resolventPhaseOperator T t (R y)=R (resolventPhaseOperator (scaledPositiveResolvent T r) t y) at hc
  rw [hc,scaledPositiveResolvent_phase T hT h1 r hr t,
    scaledPositiveResolvent_damping T hT h1 r hr]
  change R (modularPhase t (Real.log r) • resolventPhaseOperator T t (scaledResolventDampingOperator T r y)) =
    modularPhase t (Real.log r) • R
      (resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T (scaledResolventDampingOperator T r y)))
  rw [map_smul,resolventImaginaryPower_damping]

#print axioms scaledResolventDamping_denseRange
#print axioms resolventImaginaryPower_scaled_intertwining
end
end TGLV350.Regular
