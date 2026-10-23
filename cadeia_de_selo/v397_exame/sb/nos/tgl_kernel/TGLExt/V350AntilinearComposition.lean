import TGLExt.V350AntilinearAdjointGraph

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
variable (D E : Submodule ℂ H) (S : D →ₛₗ[starRingEnd ℂ] H)

def antilinearPreimageDomain : Submodule ℂ H where
  carrier := {x | ∃ hx : x ∈ D, S ⟨x,hx⟩ ∈ E}
  zero_mem' := by
    refine ⟨D.zero_mem,?_⟩
    change S 0 ∈ E
    rw [map_zero]
    exact E.zero_mem
  add_mem' := by
    rintro x y ⟨hx,hSx⟩ ⟨hy,hSy⟩
    refine ⟨D.add_mem hx hy,?_⟩
    change S (⟨x,hx⟩+⟨y,hy⟩) ∈ E
    rw [map_add]
    exact E.add_mem hSx hSy
  smul_mem' := by
    rintro c x ⟨hx,hSx⟩
    refine ⟨D.smul_mem c hx,?_⟩
    change S (c • ⟨x,hx⟩) ∈ E
    rw [map_smulₛₗ]
    exact E.smul_mem _ hSx

def antilinearPreimageInput : antilinearPreimageDomain D E S →ₗ[ℂ] D :=
  Submodule.inclusion (fun _ hx => hx.choose)

theorem antilinearPreimageInput_coe (x : antilinearPreimageDomain D E S) :
    (antilinearPreimageInput D E S x : H) = x := rfl

theorem antilinearPreimageInput_mem (x : antilinearPreimageDomain D E S) :
    S (antilinearPreimageInput D E S x) ∈ E := x.property.choose_spec

def antilinearPreimageMap : antilinearPreimageDomain D E S →ₛₗ[starRingEnd ℂ] E :=
  (S.comp (antilinearPreimageInput D E S)).codRestrict E (antilinearPreimageInput_mem D E S)

/-- Composition on the full preimage domain; both antilinearities cancel. -/
def antilinearComposite (A : E →ₛₗ[starRingEnd ℂ] H) : H →ₗ.[ℂ] H where
  domain := antilinearPreimageDomain D E S
  toFun := A.comp (antilinearPreimageMap D E S)

#print axioms antilinearPreimageDomain
#print axioms antilinearPreimageInput
#print axioms antilinearPreimageInput_coe
#print axioms antilinearPreimageInput_mem
#print axioms antilinearPreimageMap
#print axioms antilinearComposite
end
end TGLV350.Regular
