import ScreenCircularBasisR2
import RegularCoherentTransportR1

/-! Explicit unitary transport of the actual regular domain from canonical
helicity coordinates to real transverse screen coordinates. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter TGLExt.ImportedSQ F1Fecho.OrbitalScreen
open ChatgptAudit.WignerRapidityMeasure016 F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

theorem strongRegularProfile_fiberLift (e : Fiber ≃ₗᵢ[ℂ] Fiber) (h : H1)
    (hh : StrongRegularProfile h) : StrongRegularProfile (fiberLift e h) := by
  have he : ∀ᵐy ∂orbitalMeasure 0, ‖fiberLift e h y‖=‖h y‖ := by
    filter_upwards [fiberLiftMap_ae e h] with y hy
    change ‖fiberLiftMap e h y‖=‖h y‖
    rw [hy,e.norm_map]
  constructor
  · intro m
    apply (hh.1 m).congr
    filter_upwards [he] with y hy
    rw [hy]
  · intro m
    apply (hh.2 m).congr
    filter_upwards [he] with y hy
    rw [hy]

theorem strongRegularProfile_circular (h : H1) (hh : StrongRegularProfile h) :
    StrongRegularProfile (circularH1 h) := strongRegularProfile_fiberLift circularFiber h hh

theorem strongRegularProfile_circular_symm (h : H1) (hh : StrongRegularProfile h) :
    StrongRegularProfile (circularH1.symm h) := by
  exact strongRegularProfile_fiberLift circularFiber.symm h hh

def regularCircular (ψ : regularFockDomain) : regularFockDomain :=
  regularGamma circularH1 strongRegularProfile_circular ψ

theorem regularCircular_value (ψ : regularFockDomain) :
    (regularCircular ψ).val=gamma circularH1 ψ.val := rfl

theorem regularCircular_exponential (h : RegularLabel) :
    (regularCircular ⟨F1Fecho.Exponential.exponential h.val,
      exponential_mem_regularFockDomain h.val h.property⟩).val=
      F1Fecho.Exponential.exponential (circularH1 h.val) := by
  exact F1Fecho.Exponential.gamma_exponential circularH1 h.val

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.strongRegularProfile_fiberLift
#print axioms F1Fecho.MaxwellGlobal.strongRegularProfile_circular_symm
#print axioms F1Fecho.MaxwellGlobal.regularCircular_value
#print axioms F1Fecho.MaxwellGlobal.regularCircular_exponential
