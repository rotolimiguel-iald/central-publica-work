import TGLExt.F1Fecho394.SpectralUnitaryTransportR1
import TGLExt.F1Fecho394.UnitaryRootGraphTransportR1

/-! Transport identities with a named target operator. Rewriting occurs before
the concrete Fock representation is substituted, avoiding expansion of its type.
All graph and resolvent equalities remain explicit premises of these helpers. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
noncomputable section
namespace F1Fecho.ModularTransportTarget
open TGLV350.Regular F1Fecho.SpectralTransport
variable {H E : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

theorem graph_image (V : H ≃ₗᵢ[ℂ] E) (S : Set (H × H)) (T : Set (E × E))
    (h : ∀ x y, (V x,V y) ∈ T ↔ (x,y) ∈ S) :
    (V.toHomeomorph.prodCongr V.toHomeomorph) '' S = T := by
  ext p
  constructor
  · rintro ⟨q,hq,rfl⟩
    exact (h q.1 q.2).mpr hq
  · intro hp
    refine ⟨(V.symm p.1,V.symm p.2),?_,?_⟩
    · apply (h _ _).mp
      simpa only [V.apply_symm_apply] using hp
    · exact Prod.ext (V.apply_symm_apply p.1) (V.apply_symm_apply p.2)

theorem transported_eq (V : H ≃ₗᵢ[ℂ] E) (R : H →L[ℂ] H) (T : E →L[ℂ] E)
    (h : ∀ x, V (R x) = T (V x)) : transported V R = T := by
  ext y
  exact (h (V.symm y)).trans (congrArg T (V.apply_symm_apply y))

theorem imaginary_target (V : H ≃ₗᵢ[ℂ] E) (R : H →L[ℂ] H) (T : E →L[ℂ] E)
    (hR : 0 ≤ R) (hR1 : R ≤ 1) (hRi : Function.Injective R)
    (hRj : Function.Injective (1-R : H→L[ℂ]H))
    (hT : 0 ≤ T) (hT1 : T ≤ 1) (hTi : Function.Injective T)
    (hTj : Function.Injective (1-T : E→L[ℂ]E))
    (he : transported V R = T) (t : ℝ) (x : H) :
    V (resolventImaginaryPower R hR hR1 hRi hRj t x) =
      resolventImaginaryPower T hT hT1 hTi hTj t (V x) := by
  subst T
  exact SpectralTransport.imaginaryPower V R hR hR1 hRi hRj t x

theorem root_target (V : H ≃ₗᵢ[ℂ] E) (R : H →L[ℂ] H) (T : E →L[ℂ] E)
    (hR : 0 ≤ R) (hR1 : R ≤ 1) (hRi : Function.Injective R)
    (hT : 0 ≤ T) (hTi : Function.Injective T)
    (he : transported V R = T) (x y : H) :
    (V x,V y) ∈ (resolventSquareRoot T hT hTi).graph ↔
      (x,y) ∈ (resolventSquareRoot R hR hRi).graph := by
  subst T
  exact UnitaryRootGraphTransport.root_graph_iff V R hR hR1 hRi x y

end F1Fecho.ModularTransportTarget
#print axioms F1Fecho.ModularTransportTarget.graph_image
#print axioms F1Fecho.ModularTransportTarget.transported_eq
#print axioms F1Fecho.ModularTransportTarget.imaginary_target
#print axioms F1Fecho.ModularTransportTarget.root_target
