import TGLExt.V350ScalarTomitaAdjointPolar

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt ChatgptAudit.Continuous050
noncomputable section

private theorem bidualPairingTransfer {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (s a f y z : H) (hs : s = J f)
    (h : inner ℂ f y = inner ℂ z (J a)) :
    inner ℂ s (J y) = inner ℂ (J z) a := by
  rw [hs]
  have hc := congrArg (starRingEnd ℂ) h
  simp only [inner_conj_symm] at hc
  calc
    _ = inner ℂ y f := by
      have hi := antiunitary_inner_conj J f y
      exact hi.trans (inner_conj_symm (𝕜 := ℂ) y f)
    _ = inner ℂ (J a) z := hc
    _ = _ := antiunitary_pairing_flip J hJ a z

private theorem bidualMaximalFromTransport {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D E : Submodule ℂ H) (S : D → H) (F : E → H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (c : D → E) (hc : ∀ x : D, (c x : H) = J (x : H))
    (hs : ∀ x : D, S x = J (F (c x)))
    (hd : ∀ y : H, J y ∈ E ↔ y ∈ D)
    (hm : ∀ y z : H, (∀ x : D, inner ℂ (S x) y = inner ℂ z (x : H)) →
      ∃ hy : y ∈ E, F ⟨y,hy⟩ = z)
    (y z : H) (hp : ∀ x : E, inner ℂ (F x) y = inner ℂ z (x : H)) :
    ∃ hy : y ∈ D, S ⟨y,hy⟩ = z := by
  have hpair : ∀ x : D, inner ℂ (S x) (J y) = inner ℂ (J z) (x : H) := by
    intro x
    apply bidualPairingTransfer J hJ (S x) (x : H) (F (c x)) y z (hs x)
    exact (hp (c x)).trans (congrArg (inner ℂ z) (hc x))
  obtain ⟨hJy,hF⟩ := hm (J y) (J z) hpair
  have hy : y ∈ D := (hd y).mp hJy
  refine ⟨hy,?_⟩
  have he : c ⟨y,hy⟩ = ⟨J y,hJy⟩ := Subtype.ext (hc ⟨y,hy⟩)
  exact (hs ⟨y,hy⟩).trans ((congrArg J ((congrArg F he).trans hF)).trans (hJ z))

/-- Every adjoint pair for the original F already lies in the original S graph. -/
theorem scalarClosedTomita_bidual_maximal (P : SiteProfile) (y z : ScalarGNSHilbert P)
    (h : ∀ x : scalarTomitaAdjointDomain P,
      inner ℂ (scalarTomitaAdjoint P x) y = inner ℂ z (x : ScalarGNSHilbert P)) :
    ∃ hy : y ∈ scalarClosedTomitaDomain P, scalarClosedTomita P ⟨y,hy⟩ = z := by
  refine bidualMaximalFromTransport (scalarClosedTomitaDomain P) (scalarTomitaAdjointDomain P)
    (fun x => scalarClosedTomita P x) (fun x => scalarTomitaAdjoint P x)
    (scalarTomitaPolarFactor P) (scalarTomitaPolarFactor_involutive P)
    (scalarClosedTomitaConjugateInput P) ?_ ?_ ?_ ?_ y z h
  · intro x; rfl
  · intro x; exact scalarClosedTomita_conjugate_value P x
  · intro x; exact scalarTomitaPolar_closed_domain_iff P x
  · intro v w hp; exact scalarTomitaAdjoint_maximal P hp

/-- Full original-domain characterization of the adjoint of F; no new S is defined. -/
theorem scalarClosedTomita_bidual_graph_iff (P : SiteProfile) (y z : ScalarGNSHilbert P) :
    (∃ hy : y ∈ scalarClosedTomitaDomain P, scalarClosedTomita P ⟨y,hy⟩ = z) ↔
      ∀ x : scalarTomitaAdjointDomain P,
        inner ℂ (scalarTomitaAdjoint P x) y = inner ℂ z (x : ScalarGNSHilbert P) := by
  constructor
  · rintro ⟨hy,he⟩ x
    exact (scalarTomitaAdjoint_pairing P x ⟨y,hy⟩).symm.trans
      (congrArg (fun v : ScalarGNSHilbert P => inner ℂ v (x : ScalarGNSHilbert P)) he)
  · exact scalarClosedTomita_bidual_maximal P y z

#print axioms scalarClosedTomita_bidual_maximal
#print axioms scalarClosedTomita_bidual_graph_iff
end
end TGLV350.Regular
