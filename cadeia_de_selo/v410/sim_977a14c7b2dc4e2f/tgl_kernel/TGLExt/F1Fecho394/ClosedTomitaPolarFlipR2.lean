import TGLExt.F1Fecho394.ClosedTomitaSquareGraphR1
import TGLExt.V350ResolventGraphTransport
import TGLExt.V350AntiunitaryPositiveConjugation
/-! Generic resolvent flip of a closed dense antilinear involution. The original
v393-embedded proof is applied to Input H, without a SiteProfile surrogate.
The polar consequence below consumes a proved J-root factorization. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.ClosedTomitaOperator
open TGLExt TGLV350.Regular
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (A:Input H)
theorem scalarTomitaAdjoint_swap {y z : H}
    (h : ∀ x : scalarClosedTomitaDomain A,
      inner ℂ (scalarClosedTomita A x) y = inner ℂ z (x : H)) :
    ∀ x : scalarClosedTomitaDomain A,
      inner ℂ (scalarClosedTomita A x) z = inner ℂ y (x : H) := by
  intro x
  have hh := h ⟨scalarClosedTomita A x,scalarClosedTomita_maps_domain A x⟩
  rw [scalarClosedTomita_involutive A] at hh
  have hc := congrArg (starRingEnd ℂ) hh
  calc
    _ = (starRingEnd ℂ) (inner ℂ z (scalarClosedTomita A x)) :=
      (inner_conj_symm (𝕜 := ℂ) (scalarClosedTomita A x) z).symm
    _ = (starRingEnd ℂ) (inner ℂ (x : H) y) := hc.symm
    _ = _ := inner_conj_symm (𝕜 := ℂ) y (x : H)

theorem scalarTomitaAdjoint_maps_domain (y : scalarTomitaAdjointDomain A) :
    scalarTomitaAdjoint A y ∈ scalarTomitaAdjointDomain A :=
  ⟨(y : H),scalarTomitaAdjoint_swap A (scalarTomitaAdjoint_pairing A y)⟩

theorem scalarTomitaAdjoint_involutive (y : scalarTomitaAdjointDomain A) :
    scalarTomitaAdjoint A
        ⟨scalarTomitaAdjoint A y,scalarTomitaAdjoint_maps_domain A y⟩ = y := by
  apply antilinearAdjointRelation_unique (scalarClosedTomitaDomain A) (scalarClosedTomita A)
    (scalarClosedTomita_domain_dense A)
  · exact scalarTomitaAdjoint_pairing A ⟨_,scalarTomitaAdjoint_maps_domain A y⟩
  · exact scalarTomitaAdjoint_swap A (scalarTomitaAdjoint_pairing A y)


theorem scalarTomitaResolvent_memDomain (z : H) :
    scalarTomitaResolvent A z ∈ scalarClosedTomitaDomain A := by
  obtain ⟨u,hu,_⟩ := scalarTomitaResolvent_equation A z
  rw [← hu]
  exact (scalarTomitaSquareInput A u).property

/-- The actual resolvent is exchanged with its complement by S on D(S).
This bounded-resolvent identity does not by itself supply the square-root flip. -/
theorem scalarTomitaResolvent_flip (x : scalarClosedTomitaDomain A) :
    scalarClosedTomita A ⟨scalarTomitaResolvent A (x : H),
      scalarTomitaResolvent_memDomain A (x : H)⟩ =
        scalarClosedTomita A x - scalarTomitaResolvent A (scalarClosedTomita A x) := by
  obtain ⟨u,hu,hueq⟩ := scalarTomitaResolvent_equation A (x : H)
  let uS := scalarTomitaSquareInput A u
  let w : scalarClosedTomitaDomain A := x-uS
  have hw : (w : H)=scalarTomitaSquare A u := by
    change (x : H)-(u : H)=scalarTomitaSquare A u
    rw [← hueq]
    abel
  have hwAdj : (w : H) ∈ scalarTomitaAdjointDomain A := by
    rw [hw]
    exact scalarTomitaAdjoint_maps_domain A (scalarTomitaSquareAdjointInput A u)
  let v : scalarClosedTomitaDomain A :=
    ⟨scalarClosedTomita A w,scalarClosedTomita_maps_domain A w⟩
  have hvS : scalarClosedTomita A v=(w : H) :=
    scalarClosedTomita_involutive A w
  have hvAdj : scalarClosedTomita A v ∈ scalarTomitaAdjointDomain A := by
    rw [hvS]
    exact hwAdj
  let vA : scalarTomitaSquareDomain A := ⟨(v : H),⟨v.property,hvAdj⟩⟩
  have hAv : scalarTomitaSquare A vA=scalarClosedTomita A uS := by
    have he : scalarTomitaSquareAdjointInput A vA =
        ⟨scalarTomitaAdjoint A (scalarTomitaSquareAdjointInput A u),
          scalarTomitaAdjoint_maps_domain A (scalarTomitaSquareAdjointInput A u)⟩ :=
      Subtype.ext (hvS.trans hw)
    change scalarTomitaAdjoint A (scalarTomitaSquareAdjointInput A vA)=_
    rw [he]
    exact scalarTomitaAdjoint_involutive A (scalarTomitaSquareAdjointInput A u)
  have hveq : (vA : H)+scalarTomitaSquare A vA=scalarClosedTomita A x := by
    calc
      _ = scalarClosedTomita A w + scalarClosedTomita A uS :=
        congrArg (fun y => (vA : H)+y) hAv
      _ = scalarClosedTomita A (w+uS) := ((scalarClosedTomita A).map_add w uS).symm
      _ = scalarClosedTomita A x := congrArg (scalarClosedTomita A) (sub_add_cancel x uS)
  have hr : scalarTomitaResolvent A (scalarClosedTomita A x)=scalarClosedTomita A w := by
    calc
      _ = scalarTomitaResolvent A ((vA : H)+scalarTomitaSquare A vA) :=
        congrArg (scalarTomitaResolvent A) hveq.symm
      _ = (vA : H) := scalarTomitaResolvent_inverse A vA
  have he : (⟨scalarTomitaResolvent A (x : H),
      scalarTomitaResolvent_memDomain A (x : H)⟩ : scalarClosedTomitaDomain A)=uS :=
    Subtype.ext hu.symm
  rw [he,hr]
  change scalarClosedTomita A uS=scalarClosedTomita A x-scalarClosedTomita A (x-uS)
  rw [map_sub]
  abel


abbrev positiveRoot := resolventSquareRoot (scalarTomitaResolvent A)
  (scalarTomitaResolvent_nonneg A) (scalarTomitaResolvent_injective A)

theorem positiveRoot_resolvent_graph (x:(positiveRoot A).domain) :
    (scalarTomitaResolvent A (x:H),scalarTomitaResolvent A (positiveRoot A x)) ∈
      (positiveRoot A).graph :=
  resolvent_sqrt_graph_transport_of_commute (scalarTomitaResolvent A) (scalarTomitaResolvent A)
    (scalarTomitaResolvent_nonneg A) (scalarTomitaResolvent_injective A) (Commute.refl _) _ _
    ((LinearPMap.mem_graph_iff (positiveRoot A)).mpr ⟨x,rfl,rfl⟩)

theorem polar_resolvent (J:H≃ₛₗᵢ[starRingEnd ℂ]H)
    (hincl:(positiveRoot A).domain ≤ A.domain)
    (hpolar:∀x:(positiveRoot A).domain,
      J (positiveRoot A x)=A.operator (Submodule.inclusion hincl x))
    (hdense:DenseRange (positiveRoot A).toFun) (z:H) :
    J (scalarTomitaResolvent A z)=J z-scalarTomitaResolvent A (J z) := by
  refine hdense.induction ?_ (isClosed_eq (by fun_prop) (by fun_prop)) z
  rintro _ ⟨x,rfl⟩
  obtain ⟨u,hu,hBu⟩ := (LinearPMap.mem_graph_iff (positiveRoot A)).mp
    (positiveRoot_resolvent_graph A x)
  have he : Submodule.inclusion hincl u =
      (⟨scalarTomitaResolvent A (x:H),scalarTomitaResolvent_memDomain A (x:H)⟩ : A.domain) :=
    Subtype.ext hu
  calc
    _ = J (positiveRoot A u) := congrArg J hBu.symm
    _ = A.operator (Submodule.inclusion hincl u) := hpolar u
    _ = A.operator ⟨scalarTomitaResolvent A (x:H),scalarTomitaResolvent_memDomain A (x:H)⟩ :=
      congrArg A.operator he
    _ = A.operator (Submodule.inclusion hincl x)-
        scalarTomitaResolvent A (A.operator (Submodule.inclusion hincl x)) :=
      scalarTomitaResolvent_flip A (Submodule.inclusion hincl x)
    _ = _ := congrArg (fun y:H=>y-scalarTomitaResolvent A y) (hpolar x).symm

theorem polar_conjugate_resolvent (J:H≃ₛₗᵢ[starRingEnd ℂ]H)
    (hincl:(positiveRoot A).domain ≤ A.domain)
    (hpolar:∀x:(positiveRoot A).domain,
      J (positiveRoot A x)=A.operator (Submodule.inclusion hincl x))
    (hdense:DenseRange (positiveRoot A).toFun) :
    antiunitaryConjugate J (scalarTomitaResolvent A)=1-scalarTomitaResolvent A := by
  ext1 x
  have h:=polar_resolvent A J hincl hpolar hdense (J.symm x)
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.apply_symm_apply,
    ContinuousLinearMap.sub_apply,ContinuousLinearMap.one_apply] using h
end F1Fecho.ClosedTomitaOperator
#print axioms F1Fecho.ClosedTomitaOperator.scalarTomitaAdjoint_maps_domain
#print axioms F1Fecho.ClosedTomitaOperator.scalarTomitaAdjoint_involutive
#print axioms F1Fecho.ClosedTomitaOperator.scalarTomitaResolvent_flip
#print axioms F1Fecho.ClosedTomitaOperator.positiveRoot_resolvent_graph
#print axioms F1Fecho.ClosedTomitaOperator.polar_resolvent
#print axioms F1Fecho.ClosedTomitaOperator.polar_conjugate_resolvent
