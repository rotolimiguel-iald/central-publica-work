import TGLExt.V351ImaginaryPowerScaling
set_option maxHeartbeats 1500000

open TGLV350.Regular ChatgptAudit

example {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T R : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r)
    (hR : T*R=R*scaledPositiveResolvent T r) (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (R x)=
      modularPhase t (Real.log r) • R (resolventImaginaryPower T hT h1 hi hj t x) := by
  exact resolventImaginaryPower_scaled_intertwining T R hT h1 hi hj r hr hR t x
