import TGL.ModularRealization
import TGLExt.V350GateContract
import TGLExt.ModularPower

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace TGLExt.V350Continuous
open ChatgptAudit TGL.ModularRealization TGL.SpecificAQFT
noncomputable section

def towerAntiunitary (P : SiteProfile) : Antiunitary (TowerHilbert P) where
  toFun := towerJ P
  invFun := towerJ P
  left_inv := towerJ_involutive P
  right_inv := towerJ_involutive P
  map_add' := towerJ_add P
  map_smul' := towerJ_conj_smul P
  norm_map' := towerJ_norm P

theorem conjugation_zero (P : SiteProfile) (a : TowerHilbert P →L[ℂ] TowerHilbert P) :
    modularConjugation P 0 a = a := by
  ext v
  change modularFlow P 0 (a (modularFlow P (-0) v)) = a v
  simp only [neg_zero, modularFlow_zero_time]

theorem conjugation_add (P : SiteProfile) (s t : ℝ)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P) :
    modularConjugation P (s+t) a = modularConjugation P t (modularConjugation P s a) := by
  ext v
  change modularFlow P (s+t) (a (modularFlow P (-(s+t)) v)) =
    modularFlow P t (modularFlow P s (a (modularFlow P (-s) (modularFlow P (-t) v))))
  rw [modularFlow_group, modularFlow_group]
  simp only [neg_add_rev, add_comm]

def factorFlow (P : SiteProfile) (t : ℝ) :
    (theFactorObject P).toStarSubalgebra ≃⋆ₐ[ℂ] (theFactorObject P).toStarSubalgebra where
  toFun a := ⟨modularConjugation P t a, (modularConjugation_preserves_factor P t a).mp a.property⟩
  invFun a := ⟨modularConjugation P (-t) a, (modularConjugation_preserves_factor P (-t) a).mp a.property⟩
  left_inv a := by
    apply Subtype.ext
    change modularConjugation P (-t) (modularConjugation P t a) = a
    rw [← conjugation_add, add_neg_cancel, conjugation_zero]
  right_inv a := by
    apply Subtype.ext
    change modularConjugation P t (modularConjugation P (-t) a) = a
    rw [← conjugation_add, neg_add_cancel, conjugation_zero]
  map_mul' a b := Subtype.ext (map_mul (modularConjugation P t)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P) (b : TowerHilbert P →L[ℂ] TowerHilbert P))
  map_add' a b := Subtype.ext (map_add (modularConjugation P t)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P) (b : TowerHilbert P →L[ℂ] TowerHilbert P))
  map_smul' c a := Subtype.ext (map_smul (modularConjugation P t) c
    (a : TowerHilbert P →L[ℂ] TowerHilbert P))
  map_star' a := Subtype.ext (map_star (modularConjugation P t)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P))

theorem factorFlow_zero (P : SiteProfile) : factorFlow P 0 = StarAlgEquiv.refl := by
  apply StarAlgEquiv.ext
  intro a
  exact Subtype.ext (conjugation_zero P a)

theorem factorFlow_add (P : SiteProfile) (s t : ℝ) :
    factorFlow P (s+t) = (factorFlow P s).trans (factorFlow P t) := by
  apply StarAlgEquiv.ext
  intro a
  exact Subtype.ext (conjugation_add P s t a)

/-- The minimal wedge modular data use the actual tower flow and its proven conjugation.
This supplies layer 1A only; it is not a crossed product, a trace, or a BW geometry theorem. -/
def towerWedgeData : WedgeModularData theSpecificAQFTWitness where
  wedgeAlgebra := theFactorObject mixProfile
  wedgeAlgebra_eq := (wedgeNet_M hasRW_rightWedge not_hasLW_rightWedge).symm
  modularFlow := factorFlow mixProfile
  modularFlow_zero := factorFlow_zero mixProfile
  modularFlow_add := factorFlow_add mixProfile
  modularConjugation := towerAntiunitary mixProfile
  modularConjugation_involutive := towerJ_involutive mixProfile
  modularConjugation_vac := towerJ_fixes_hOmega mixProfile

theorem same_conjugation (v : WH) :
    towerWedgeData.modularConjugation v = qgFrontier_modularRealization.J v := rfl

#print axioms towerAntiunitary
#print axioms factorFlow
#print axioms towerWedgeData
#print axioms same_conjugation
end
end TGLExt.V350Continuous
