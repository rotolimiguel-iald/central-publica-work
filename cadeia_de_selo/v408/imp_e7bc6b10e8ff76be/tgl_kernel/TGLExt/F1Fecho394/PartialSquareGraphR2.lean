import TGLExt.ContinuousModularSquare
import TGLExt.GenericAntilinearAdjoint
/-! The exact composition domain and graph of a partial operator square,
reusing the canonical partialSquareDomain. No selfadjointness of the square
or imaginary power identification is asserted by this algebraic lemma. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.PartialSquare
open ChatgptAudit.Continuous050
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

def input (T : H →ₗ.[ℂ] H) : partialSquareDomain T →ₗ[ℂ] T.domain :=
  Submodule.inclusion (fun _ h => h.choose)

def square (T : H →ₗ.[ℂ] H) : H →ₗ.[ℂ] H where
  domain := partialSquareDomain T
  toFun := T.toFun.comp ((T.toFun.comp (input T)).codRestrict
    T.domain (fun x => x.property.choose_spec))

theorem square_graph_iff (T : H →ₗ.[ℂ] H) (x y : H) :
    (x,y) ∈ (square T).graph ↔
      ∃ hx : x ∈ T.domain, ∃ hTx : T ⟨x,hx⟩ ∈ T.domain, T ⟨T ⟨x,hx⟩,hTx⟩ = y := by
  rw [LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨v,hv,hy⟩
    dsimp only [Prod.fst,Prod.snd] at hv hy
    subst x
    exact ⟨v.property.choose,v.property.choose_spec,hy⟩
  · rintro ⟨hx,hTx,hxy⟩
    exact ⟨⟨x,⟨hx,hTx⟩⟩,rfl,hxy⟩

theorem square_graph_iff_tomita_comp (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J) (x y : H) :
    (x,y) ∈ (square T).graph ↔
      ∃ hx : x ∈ T.domain,
        ∃ hSx : genericTomita T J ⟨x,hx⟩ ∈ (genericTomitaAdjoint T J).domain,
          genericTomitaAdjoint T J ⟨genericTomita T J ⟨x,hx⟩,hSx⟩ = y := by
  rw [square_graph_iff]
  constructor
  · rintro ⟨hx,hTx,hxy⟩
    refine ⟨hx,(generic_composition_domain T J hJ ⟨x,hx⟩).mpr hTx,?_⟩
    rw [generic_adjoint_comp T J hJ]
    exact hxy
  · rintro ⟨hx,hSx,hxy⟩
    have hTx := (generic_composition_domain T J hJ ⟨x,hx⟩).mp hSx
    refine ⟨hx,hTx,?_⟩
    rw [← generic_adjoint_comp T J hJ ⟨x,hx⟩ hTx]
    exact hxy

theorem square_energy (T : H →ₗ.[ℂ] H) (hs : T.IsFormalAdjoint T)
    (x : (square T).domain) :
    (inner ℂ (x:H) (square T x)).re = ‖T ⟨x,x.property.choose⟩‖^2 := by
  let u : T.domain := ⟨x,x.property.choose⟩
  let v : T.domain := ⟨T u,x.property.choose_spec⟩
  change (inner ℂ (u:H) (T v)).re = _
  rw [← hs u v]
  exact (norm_sq_eq_re_inner (𝕜 := ℂ) (T u)).symm

end F1Fecho.PartialSquare
#print axioms F1Fecho.PartialSquare.square_graph_iff
#print axioms F1Fecho.PartialSquare.square_graph_iff_tomita_comp
#print axioms F1Fecho.PartialSquare.square_energy
