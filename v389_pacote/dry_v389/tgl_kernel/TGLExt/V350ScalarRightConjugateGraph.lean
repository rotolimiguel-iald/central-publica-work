import TGLExt.V350ScalarTomitaAdjointPolar
import TGLExt.V350ScalarRightGraphCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem involutionImageReverse {X : Type} (f : X → X)
    (hi : Function.Involutive f) (s t : Set X) (h : f '' s = t) : f '' t = s := by
  ext x
  constructor
  · rintro ⟨y, hy, rfl⟩
    obtain ⟨z, hz, rfl⟩ := h.symm ▸ hy
    exact (congrArg (fun w => w ∈ s) (hi z)).mpr hz
  · intro hx
    exact ⟨f x, h ▸ Set.mem_image_of_mem f hx, hi x⟩

private theorem imageRangeComposition {X Y Z : Type} (f : Y → Z) (g : X → Y) :
    Set.range (fun x => f (g x)) = f '' Set.range g := by
  ext z
  constructor
  · rintro ⟨x, rfl⟩
    exact ⟨g x, ⟨x, rfl⟩, rfl⟩
  · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
    exact ⟨x, rfl⟩

private theorem conjugateValueFromGraph {H : Type} (J : H → H)
    (D E : Set H) (S : D → H) (F : E → H)
    (hi : Function.Involutive J)
    (hf : ∀ y : E, ∃ hx : J (y : H) ∈ D, F y = J (S ⟨J y, hx⟩))
    (v w : H) (hv : ∃ hy : v ∈ E, F ⟨v, hy⟩ = w)
    (hd : J v ∈ D) : S ⟨J v, hd⟩ = J w := by
  obtain ⟨hy, he⟩ := hv
  obtain ⟨hx, hxv⟩ := hf ⟨v, hy⟩
  exact ((congrArg J hxv).trans (hi (S ⟨J v, hx⟩))).symm.trans (congrArg J he)

/-- The same original J acts on both coordinates. This is a homeomorphism
of graph spaces, not a linear identification of the two algebras. -/
def scalarTomitaGraphConjugation (P : SiteProfile) :
    (ScalarGNSHilbert P × ScalarGNSHilbert P) ≃ₜ
      (ScalarGNSHilbert P × ScalarGNSHilbert P) where
  toFun p := (scalarTomitaPolarFactor P p.1, scalarTomitaPolarFactor P p.2)
  invFun p := (scalarTomitaPolarFactor P p.1, scalarTomitaPolarFactor P p.2)
  left_inv p := Prod.ext (scalarTomitaPolarFactor_involutive P p.1)
    (scalarTomitaPolarFactor_involutive P p.2)
  right_inv p := Prod.ext (scalarTomitaPolarFactor_involutive P p.1)
    (scalarTomitaPolarFactor_involutive P p.2)
  continuous_toFun := by fun_prop
  continuous_invFun := by fun_prop

theorem scalarTomitaGraphConjugation_involutive (P : SiteProfile) :
    Function.Involutive (scalarTomitaGraphConjugation P) := by
  intro p
  exact Prod.ext (scalarTomitaPolarFactor_involutive P p.1)
    (scalarTomitaPolarFactor_involutive P p.2)

theorem scalarTomitaPolar_conjugates_adjoint_graph (P : SiteProfile) :
    scalarTomitaGraphConjugation P ''
      Set.range (fun y : scalarTomitaAdjointDomain P =>
        ((y : ScalarGNSHilbert P), scalarTomitaAdjoint P y)) =
    Set.range (fun x : scalarClosedTomitaDomain P =>
      ((x : ScalarGNSHilbert P), scalarClosedTomita P x)) := by
  refine involutionImageReverse (scalarTomitaGraphConjugation P)
    (scalarTomitaGraphConjugation_involutive P) _ _ ?_
  exact scalarTomitaPolar_conjugates_closed_graph P

/-- Conjugate-linear inscription of the existing right algebra in H_I. -/
def scalarRightConjugateVector (P : SiteProfile) :
    scalarPairedRightAlgebra P →ₛₗ[starRingEnd ℂ] ScalarGNSHilbert P :=
  (scalarTomitaPolarFactor P).toLinearEquiv.toLinearMap.comp (scalarRightPairVector P)

theorem scalarRightConjugateVector_mem_original (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) :
    scalarRightConjugateVector P a ∈ scalarClosedTomitaDomain P :=
  (scalarTomitaAdjoint_conjugate_domain_iff P _).mp
    (scalarRightPairVector_original_adjoint P a).choose

/-- S acts by the original star on the conjugated right inscriptions. -/
theorem scalarRightConjugateVector_star (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) :
    scalarClosedTomita P ⟨scalarRightConjugateVector P a,
      scalarRightConjugateVector_mem_original P a⟩ =
        scalarRightConjugateVector P (star a) := by
  refine conjugateValueFromGraph (scalarTomitaPolarFactor P)
    (scalarClosedTomitaDomain P : Set (ScalarGNSHilbert P))
    (scalarTomitaAdjointDomain P : Set (ScalarGNSHilbert P))
    (fun x => scalarClosedTomita P x) (fun y => scalarTomitaAdjoint P y)
    ?_ ?_ (scalarRightPairVector P a) (scalarRightPairVector P (star a))
    ?_ (scalarRightConjugateVector_mem_original P a)
  · exact scalarTomitaPolarFactor_involutive P
  · intro y
    exact ⟨(scalarTomitaAdjoint_conjugate_domain_iff P y).mp y.property,
      scalarTomitaAdjoint_conjugate_value P y⟩
  · exact scalarRightPairVector_original_adjoint P a

/-- Graph density for the original S, transported from the already proved
graph core of the original F. This asserts no commutant reconstruction. -/
theorem scalarRightConjugateGraph_closure_eq_original (P : SiteProfile) :
    closure (Set.range (fun a : scalarPairedRightAlgebra P =>
      (scalarRightConjugateVector P a, scalarRightConjugateVector P (star a)))) =
    Set.range (fun x : scalarClosedTomitaDomain P =>
      ((x : ScalarGNSHilbert P), scalarClosedTomita P x)) := by
  have he : Set.range (fun a : scalarPairedRightAlgebra P =>
      (scalarRightConjugateVector P a, scalarRightConjugateVector P (star a))) =
      scalarTomitaGraphConjugation P '' scalarRightPairGraph P :=
    imageRangeComposition (scalarTomitaGraphConjugation P)
      (fun a : scalarPairedRightAlgebra P =>
        (scalarRightPairVector P a, scalarRightPairVector P (star a)))
  calc
    _ = closure (scalarTomitaGraphConjugation P '' scalarRightPairGraph P) :=
      congrArg closure he
    _ = scalarTomitaGraphConjugation P '' closure (scalarRightPairGraph P) :=
      ((scalarTomitaGraphConjugation P).image_closure _).symm
    _ = scalarTomitaGraphConjugation P '' Set.range (fun y : scalarTomitaAdjointDomain P =>
        ((y : ScalarGNSHilbert P), scalarTomitaAdjoint P y)) :=
      congrArg (fun s => scalarTomitaGraphConjugation P '' s)
        (scalarRightPairGraph_closure_eq_original P)
    _ = _ := scalarTomitaPolar_conjugates_adjoint_graph P

#print axioms scalarTomitaGraphConjugation
#print axioms scalarTomitaGraphConjugation_involutive
#print axioms scalarTomitaPolar_conjugates_adjoint_graph
#print axioms scalarRightConjugateVector
#print axioms scalarRightConjugateVector_mem_original
#print axioms scalarRightConjugateVector_star
#print axioms scalarRightConjugateGraph_closure_eq_original
end
end TGLV350.Regular
