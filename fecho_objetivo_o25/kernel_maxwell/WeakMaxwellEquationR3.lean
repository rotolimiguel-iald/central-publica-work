import WeakSegalDistributionR3
import SpacetimeMaxwellDivergenceR3

/-! Source-free Maxwell identity as an actual operator identity on the dense
exponential domain, hence also for every constructed weak field distribution. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Creation F1Fecho.Annihilation SchwartzMap

theorem segal_zero_on_core (x : domain) : segal (0:H1) x=0 := by
  have ha : onDomain (0:H1) x=0 := by
    change weighted (0:H1) (preimage x)=0
    simp only [weighted,Finsupp.linearCombination_apply,Finsupp.sum,
      inner_zero_left,zero_smul,smul_zero,Finset.sum_const_zero]
  have hc : creationOnDomain (0:H1) x=0 := by
    apply F1Fecho.Exponential.exponential_orthogonal_zero
    intro h
    apply inner_eq_zero_symm.mp
    change inner ℂ (F1Fecho.Exponential.exponential h) (creation (0:H1) x)=0
    rw [creation_inner_on_domain]
    simp
  change ((Real.sqrt 2)⁻¹:ℂ) • (onDomain (0:H1) x+creationOnDomain (0:H1) x)=0
  rw [ha,hc,zero_add,smul_zero]

theorem segal_spacetimeDivergence_zero (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4) (x : domain) :
    segal (physicalSmearCLM (spacetimeDivergence b ν)) x=0 := by
  rw [physicalSmear_spacetimeDivergence_zero,segal_zero_on_core]

theorem weakPhysicalField_spacetimeDivergence_zero (b : 𝓢(Spacetime,ℂ)) (ν : Fin 4)
    (x y : domain) : weakPhysicalField x y (spacetimeDivergence b ν)=0 := by
  rw [weakPhysicalField_apply,segal_spacetimeDivergence_zero,inner_zero_right]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.segal_zero_on_core
#print axioms F1Fecho.MaxwellGlobal.segal_spacetimeDivergence_zero
#print axioms F1Fecho.MaxwellGlobal.weakPhysicalField_spacetimeDivergence_zero
