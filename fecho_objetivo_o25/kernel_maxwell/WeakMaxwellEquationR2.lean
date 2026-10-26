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
  have h:=segal_parameter_add (0:H1) (0:H1) x
  have hz : segal (0:H1) x=segal (0:H1) x+segal (0:H1) x := by
    simpa only [zero_add] using h
  exact add_right_eq_self.mp hz.symm

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
