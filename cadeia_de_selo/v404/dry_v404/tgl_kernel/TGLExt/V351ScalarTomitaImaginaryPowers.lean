import TGLExt.V351ResolventImaginaryContinuity
import TGLExt.V350ScalarTomitaPolarResolvent

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

/-- The second endpoint has no kernel, by the actual antiunitary resolvent flip. -/
theorem scalarTomitaResolvent_complement_injective :
    Function.Injective (1-scalarTomitaResolvent P : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := by
  intro x y h
  apply (scalarTomitaPolarFactor P).injective
  apply scalarTomitaResolvent_injective P
  change x-scalarTomitaResolvent P x = y-scalarTomitaResolvent P y at h
  have he := congrArg (scalarTomitaPolarFactor P) h
  simpa only [map_sub,scalarTomitaPolarFactor_resolvent,sub_sub_cancel] using he

/-- Imaginary powers of the same S†S, defined by its already identified resolvent.
No identification with the regular modular automorphism is claimed here. -/
def scalarTomitaImaginaryPower (t : ℝ) : ScalarGNSHilbert P ≃ₗᵢ[ℂ] ScalarGNSHilbert P :=
  resolventImaginaryPower (scalarTomitaResolvent P) (scalarTomitaResolvent_nonneg P)
    (scalarTomitaResolvent_le_one P) (scalarTomitaResolvent_injective P)
    (scalarTomitaResolvent_complement_injective P) t

theorem scalarTomitaImaginaryPower_damping (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (resolventDampingOperator (scalarTomitaResolvent P) x)=
      resolventPhaseOperator (scalarTomitaResolvent P) t x :=
  resolventImaginaryPower_damping _ _ _ _ _ t x

/-- The dense-range identity uniquely specifies this operator among bounded maps. -/
theorem scalarTomitaImaginaryPower_unique (t : ℝ)
    (U : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hU : ∀ x, U (resolventDampingOperator (scalarTomitaResolvent P) x)=
      resolventPhaseOperator (scalarTomitaResolvent P) t x) (x : ScalarGNSHilbert P) :
    U x=scalarTomitaImaginaryPower P t x := by
  refine (resolventDampingOperator_denseRange (scalarTomitaResolvent P)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [hU,scalarTomitaImaginaryPower_damping]

theorem scalarTomitaImaginaryPower_zero (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P 0 x=x :=
  resolventImaginaryPower_zero _ _ _ _ _ x

theorem scalarTomitaImaginaryPower_add (s t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P s (scalarTomitaImaginaryPower P t x)=
      scalarTomitaImaginaryPower P (s+t) x :=
  resolventImaginaryPower_add _ _ _ _ _ s t x

theorem scalarTomitaImaginaryPower_strongly_continuous (x : ScalarGNSHilbert P) :
    Continuous (fun t : ℝ => scalarTomitaImaginaryPower P t x) :=
  resolventImaginaryPower_strongly_continuous _ _ _ _ _ x

theorem scalarTomitaImaginaryPower_inverse (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P (-t) (scalarTomitaImaginaryPower P t x)=x := by
  rw [scalarTomitaImaginaryPower_add,neg_add_cancel,scalarTomitaImaginaryPower_zero]

#print axioms scalarTomitaResolvent_complement_injective
#print axioms scalarTomitaImaginaryPower
#print axioms scalarTomitaImaginaryPower_damping
#print axioms scalarTomitaImaginaryPower_unique
#print axioms scalarTomitaImaginaryPower_zero
#print axioms scalarTomitaImaginaryPower_add
#print axioms scalarTomitaImaginaryPower_strongly_continuous
#print axioms scalarTomitaImaginaryPower_inverse
end
end TGLV350.Regular
