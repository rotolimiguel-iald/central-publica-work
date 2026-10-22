import TGLExt.V351ResolventImaginaryIntertwining

set_option autoImplicit false
open TGLV350.Regular TGLExt ChatgptAudit
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
example (T Q R : H →L[ℂ] H)
    (h : T*R=R*Q) : resolventDampingOperator T * R = R * resolventDampingOperator Q + 1 := by
  exact resolventDampingOperator_intertwines T Q R h
end
