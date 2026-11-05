import TGLExt.F1Fecho394.ClosedTomitaOperatorR1
import TGLExt.V350ResolventGraphTransport

/-! A full-domain intertwining transports the actual maximal adjoint and
the resolvent of S-adjoint-S. The Hilbert space stays abstract here so the
concrete Fock specialization does not re-elaborate its internal construction.
All intertwining and adjoint relations are explicit premises. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
noncomputable section
namespace F1Fecho.GenericRightTomitaResolvent
open F1Fecho.ClosedTomitaOperator TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (A : Input H) (U V : ℝ → H →L[ℂ] H)
variable (hU : ∀ t, star (U t) = U (-t)) (hV : ∀ t, star (V t) = V (-t))
variable (hd : ∀ t (x : A.domain), U t (x : H) ∈ A.domain)
variable (hs : ∀ t (x : A.domain), A.operator ⟨U t x,hd t x⟩ = V t (A.operator x))

def domainInput (t : ℝ) (x : A.domain) : A.domain := ⟨U t x,hd t x⟩

include hU hV hd hs

theorem adjoint_pairing (t : ℝ) (z : scalarTomitaAdjointDomain A) (x : A.domain) :
    inner ℂ (A.operator x) (V (-t) z) =
      inner ℂ (U (-t) (scalarTomitaAdjoint A z)) (x : H) := by
  calc
    _ = inner ℂ ((V (-t)).adjoint (A.operator x)) (z : H) :=
      ((V (-t)).adjoint_inner_left _ _).symm
    _ = inner ℂ (V t (A.operator x)) (z : H) := by
      change inner ℂ (star (V (-t)) (A.operator x)) (z : H) = _
      rw [hV,neg_neg]
    _ = inner ℂ (A.operator (domainInput A U hd t x)) (z : H) := by rw [domainInput,hs]
    _ = inner ℂ (scalarTomitaAdjoint A z) (U t (x : H)) :=
      scalarTomitaAdjoint_pairing A z (domainInput A U hd t x)
    _ = inner ℂ (star (U t) (scalarTomitaAdjoint A z)) (x : H) :=
      ((U t).adjoint_inner_left _ _).symm
    _ = _ := by rw [hU]

theorem adjoint_maximal (t : ℝ) (z : scalarTomitaAdjointDomain A) :
    ∃ hz : V (-t) z ∈ scalarTomitaAdjointDomain A,
      scalarTomitaAdjoint A ⟨V (-t) z,hz⟩ = U (-t) (scalarTomitaAdjoint A z) :=
  scalarTomitaAdjoint_maximal A (adjoint_pairing A U V hU hV hd hs t z)

def adjointInput (t : ℝ) (z : scalarTomitaAdjointDomain A) : scalarTomitaAdjointDomain A :=
  ⟨V (-t) z,(adjoint_maximal A U V hU hV hd hs t z).choose⟩

theorem adjoint_intertwines (t : ℝ) (z : scalarTomitaAdjointDomain A) :
    scalarTomitaAdjoint A (adjointInput A U V hU hV hd hs t z) =
      U (-t) (scalarTomitaAdjoint A z) :=
  (adjoint_maximal A U V hU hV hd hs t z).choose_spec

theorem square_mem (t : ℝ) (x : scalarTomitaSquareDomain A) :
    U t (x : H) ∈ scalarTomitaSquareDomain A := by
  refine ⟨hd t (scalarTomitaSquareInput A x),?_⟩
  change A.operator (domainInput A U hd t (scalarTomitaSquareInput A x)) ∈ _
  rw [domainInput,hs]
  have hm := (adjointInput A U V hU hV hd hs (-t) (scalarTomitaSquareAdjointInput A x)).property
  change V (- -t) (A.operator (scalarTomitaSquareInput A x)) ∈ scalarTomitaAdjointDomain A at hm
  simpa only [neg_neg] using hm

def squareInput (t : ℝ) (x : scalarTomitaSquareDomain A) : scalarTomitaSquareDomain A :=
  ⟨U t x,square_mem A U V hU hV hd hs t x⟩

theorem square_commutes (t : ℝ) (x : scalarTomitaSquareDomain A) :
    scalarTomitaSquare A (squareInput A U V hU hV hd hs t x) =
      U t (scalarTomitaSquare A x) := by
  have he : scalarTomitaSquareAdjointInput A (squareInput A U V hU hV hd hs t x) =
      adjointInput A U V hU hV hd hs (-t) (scalarTomitaSquareAdjointInput A x) := by
    apply Subtype.ext
    change A.operator (domainInput A U hd t (scalarTomitaSquareInput A x)) =
      V (- -t) (A.operator (scalarTomitaSquareInput A x))
    simpa only [neg_neg,domainInput] using hs t (scalarTomitaSquareInput A x)
  change scalarTomitaAdjoint A (scalarTomitaSquareAdjointInput A
    (squareInput A U V hU hV hd hs t x)) = _
  rw [he,adjoint_intertwines,neg_neg]
  rfl

theorem resolvent_commutes (t : ℝ) : Commute (scalarTomitaResolvent A) (U t) := by
  apply ContinuousLinearMap.ext
  intro z
  obtain ⟨x,hx,he⟩ := scalarTomitaResolvent_equation A z
  calc
    _ = scalarTomitaResolvent A (U t ((x : H)+scalarTomitaSquare A x)) := by rw [he]; rfl
    _ = scalarTomitaResolvent A ((squareInput A U V hU hV hd hs t x : H)+
        scalarTomitaSquare A (squareInput A U V hU hV hd hs t x)) := by
      rw [map_add,square_commutes]
      rfl
    _ = (squareInput A U V hU hV hd hs t x : H) := scalarTomitaResolvent_inverse A _
    _ = _ := congrArg (U t) hx

end F1Fecho.GenericRightTomitaResolvent
#print axioms F1Fecho.GenericRightTomitaResolvent.adjoint_pairing
#print axioms F1Fecho.GenericRightTomitaResolvent.adjoint_maximal
#print axioms F1Fecho.GenericRightTomitaResolvent.square_mem
#print axioms F1Fecho.GenericRightTomitaResolvent.square_commutes
#print axioms F1Fecho.GenericRightTomitaResolvent.resolvent_commutes
