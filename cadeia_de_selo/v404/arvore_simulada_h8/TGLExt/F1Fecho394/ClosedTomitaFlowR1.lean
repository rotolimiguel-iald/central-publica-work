import TGLExt.F1Fecho394.ClosedTomitaOperatorR1
/-! Strongly continuous imaginary powers of the actual positive operator
S_nu^* S_nu, on the Hilbert space of a closed dense antilinear involution. The complement of
its bounded resolvent is injective because the square has trivial kernel.
This is not an identification with the regular conjugation group, KMS, or
an exp(-s)-scaled trace. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.ClosedTomitaFlow
open TGLExt TGLV350.Regular
open F1Fecho.ClosedTomitaOperator
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (A : Input H)
local instance : PartialOrder (H →L[ℂ] H) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := H)

theorem scalarTomitaResolvent_complement_injective :
    Function.Injective (1-scalarTomitaResolvent A : H →L[ℂ] H) := by
  intro x y h
  apply sub_eq_zero.mp
  have hz : (1-scalarTomitaResolvent A : H →L[ℂ] H) (x-y)=0 := by
    rw [map_sub,h,sub_self]
  have hfix : scalarTomitaResolvent A (x-y)=x-y := by
    change (x-y)-scalarTomitaResolvent A (x-y)=0 at hz
    exact (sub_eq_zero.mp hz).symm
  obtain ⟨z,hzv,heq⟩ := scalarTomitaResolvent_equation A (x-y)
  have he : (z:H)=x-y := hzv.trans hfix
  have hd : scalarTomitaSquare A z=0 := by
    rw [he] at heq
    exact add_left_cancel (heq.trans (add_zero (x-y)).symm)
  exact he.symm.trans (scalarTomitaSquare_zero_only A z hd)
/-- Imaginary powers of the same S†S, defined by its already identified resolvent.
No identification with the regular modular automorphism is claimed here. -/
def scalarTomitaImaginaryPower (t : ℝ) : H ≃ₗᵢ[ℂ] H :=
  resolventImaginaryPower (H := H) (scalarTomitaResolvent A) (scalarTomitaResolvent_nonneg A)
    (scalarTomitaResolvent_le_one A) (scalarTomitaResolvent_injective A)
    (scalarTomitaResolvent_complement_injective A) t

theorem scalarTomitaImaginaryPower_damping (t : ℝ) (x : H) :
    scalarTomitaImaginaryPower A t (resolventDampingOperator (H := H) (scalarTomitaResolvent A) x)=
      resolventPhaseOperator (H := H) (scalarTomitaResolvent A) t x :=
  resolventImaginaryPower_damping (H := H) _ _ _ _ _ t x

/-- The dense-range identity uniquely specifies this operator among bounded maps. -/
theorem scalarTomitaImaginaryPower_unique (t : ℝ)
    (U : H →L[ℂ] H)
    (hU : ∀ x, U (resolventDampingOperator (H := H) (scalarTomitaResolvent A) x)=
      resolventPhaseOperator (H := H) (scalarTomitaResolvent A) t x) (x : H) :
    U x=scalarTomitaImaginaryPower A t x := by
  refine (resolventDampingOperator_denseRange (H := H) (scalarTomitaResolvent A)
    (scalarTomitaResolvent_nonneg A) (scalarTomitaResolvent_le_one A)
    (scalarTomitaResolvent_injective A) (scalarTomitaResolvent_complement_injective A)).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [hU,scalarTomitaImaginaryPower_damping A]

theorem scalarTomitaImaginaryPower_zero (x : H) :
    scalarTomitaImaginaryPower A 0 x=x :=
  resolventImaginaryPower_zero (H := H) _ _ _ _ _ x

theorem scalarTomitaImaginaryPower_add (s t : ℝ) (x : H) :
    scalarTomitaImaginaryPower A s (scalarTomitaImaginaryPower A t x)=
      scalarTomitaImaginaryPower A (s+t) x :=
  resolventImaginaryPower_add (H := H) _ _ _ _ _ s t x

theorem scalarTomitaImaginaryPower_strongly_continuous (x : H) :
    Continuous (fun t : ℝ => scalarTomitaImaginaryPower A t x) :=
  resolventImaginaryPower_strongly_continuous (H := H) _ _ _ _ _ x

theorem scalarTomitaImaginaryPower_inverse (t : ℝ) (x : H) :
    scalarTomitaImaginaryPower A (-t) (scalarTomitaImaginaryPower A t x)=x := by
  rw [scalarTomitaImaginaryPower_add A,neg_add_cancel,scalarTomitaImaginaryPower_zero A]

#print axioms scalarTomitaResolvent_complement_injective
#print axioms scalarTomitaImaginaryPower
#print axioms scalarTomitaImaginaryPower_damping
#print axioms scalarTomitaImaginaryPower_unique
#print axioms scalarTomitaImaginaryPower_zero
#print axioms scalarTomitaImaginaryPower_add
#print axioms scalarTomitaImaginaryPower_strongly_continuous
#print axioms scalarTomitaImaginaryPower_inverse
end F1Fecho.ClosedTomitaFlow
