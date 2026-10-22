import TGLExt.V351ScaledResolventCalculus

set_option autoImplicit false
open TGLV350.Regular TGLExt ChatgptAudit
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
example (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    resolventDampingOperator (scaledPositiveResolvent T r) =
      (2 : ℝ) • (resolventDampingOperator T * scaledResolventDampingOperator T r) := by
  exact scaledPositiveResolvent_damping T hT h1 r hr
end
