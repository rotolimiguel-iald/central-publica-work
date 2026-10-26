import CircularPhysicalFieldTransportR1
import AxisCompactFockTranslationR2

/-! Candidate R50. The fixed circular fiber unitary preserves the SAME
axis-avoiding smooth compact profiles and their unique finite coherent
coefficient domain. No replacement domain, stress invariance or local Wick
identification is assumed. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Set TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016 F1Fecho.OrbitalScreen
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open scoped ContDiff

theorem axisCompactProfile_fiberLift (e : Fiber ≃ₗᵢ[ℂ] Fiber) (h : H1)
    (hh : AxisCompactProfile h) : AxisCompactProfile (fiberLift e h) := by
  obtain ⟨g, he, hc, hg, ε, hε, hgap⟩ := hh
  let g' : MomentumCoordinates → Fiber := fun y => e (g y)
  have htransport : (fiberLift e h : MomentumCoordinates → Fiber) =ᵐ[orbitalMeasure 0] g' := by
    filter_upwards [fiberLiftMap_ae e h, he] with y hy hy'
    change fiberLiftMap e h y = e (g y)
    rw [hy, hy']
  have hcompact : HasCompactSupport g' := hc.comp_left (map_zero e)
  have hsmooth : ContDiff ℝ ∞ g' :=
    (e.toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ).contDiff.comp hg
  have hgap' : ∀ y : MomentumCoordinates, ‖transverseProjection y‖ ≤ ε → g' y = 0 := by
    intro y hy
    change e (g y) = 0
    rw [hgap y hy, map_zero]
  exact ⟨g', htransport, hcompact, hsmooth, ε, hε, hgap'⟩

theorem axisCompactProfile_circular (h : H1) (hh : AxisCompactProfile h) :
    AxisCompactProfile (circularH1 h) :=
  axisCompactProfile_fiberLift circularFiber h hh

theorem axisCompactProfile_circular_symm (h : H1) (hh : AxisCompactProfile h) :
    AxisCompactProfile (circularH1.symm h) :=
  axisCompactProfile_fiberLift circularFiber.symm h hh

theorem axisCompactFock_fiberLift (e : Fiber ≃ₗᵢ[ℂ] Fiber) (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) :
    AxisCompactFock (regularGamma (fiberLift e) (strongRegularProfile_fiberLift e) ψ) := by
  have hv : ∀ h, StrongRegularProfile h → StrongRegularProfile ((fiberLift e).symm h) :=
    strongRegularProfile_fiberLift e.symm
  let eqv : RegularLabel ≃ RegularLabel :=
    regularLabelEquiv (fiberLift e) (strongRegularProfile_fiberLift e) hv
  intro k hk
  rw [regularCoefficients_gamma (fiberLift e) (strongRegularProfile_fiberLift e) hv] at hk
  have hk' : eqv.symm k ∈ (regularCoefficients ψ).support := by
    simpa only [Finsupp.mem_support_iff, Finsupp.equivMapDomain_apply] using hk
  have ht := axisCompactProfile_fiberLift e (eqv.symm k).val (hψ (eqv.symm k) hk')
  have he : fiberLift e (eqv.symm k).val = k.val :=
    congrArg Subtype.val (eqv.apply_symm_apply k)
  exact he ▸ ht

theorem axisCompactFock_circular (ψ : regularFockDomain) (hψ : AxisCompactFock ψ) :
    AxisCompactFock (regularCircular ψ) :=
  axisCompactFock_fiberLift circularFiber ψ hψ

theorem axisCompactFock_circular_iff (ψ : regularFockDomain) :
    AxisCompactFock (regularCircular ψ) ↔ AxisCompactFock ψ := by
  constructor
  · intro hψ
    have hi : AxisCompactFock (regularCircularInverse (regularCircular ψ)) :=
      axisCompactFock_fiberLift circularFiber.symm (regularCircular ψ) hψ
    rwa [regularCircular_left_inverse] at hi
  · exact axisCompactFock_circular ψ

theorem gamma_fiberLift_mem_axisCompactFockDomain (e : Fiber ≃ₗᵢ[ℂ] Fiber) (ψ : F)
    (hψ : ψ ∈ axisCompactFockDomain) : gamma (fiberLift e) ψ ∈ axisCompactFockDomain := by
  obtain ⟨hp, hc⟩ := hψ
  exact ⟨gamma_mem_regularFockDomain (fiberLift e) (strongRegularProfile_fiberLift e) ψ hp,
    axisCompactFock_fiberLift e ⟨ψ, hp⟩ hc⟩

theorem axisCompactFockDomain_circular (ψ : F) :
    gamma circularH1 ψ ∈ axisCompactFockDomain ↔ ψ ∈ axisCompactFockDomain := by
  constructor
  · intro hψ
    have hi := gamma_fiberLift_mem_axisCompactFockDomain circularFiber.symm
      (gamma circularH1 ψ) hψ
    change gamma circularH1.symm (gamma circularH1 ψ) ∈ axisCompactFockDomain at hi
    simpa only [gamma_symm, LinearIsometryEquiv.symm_apply_apply] using hi
  · exact gamma_fiberLift_mem_axisCompactFockDomain circularFiber ψ

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_fiberLift
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_circular
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_circular_symm
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_fiberLift
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_circular
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_circular_iff
#print axioms F1Fecho.MaxwellGlobal.gamma_fiberLift_mem_axisCompactFockDomain
#print axioms F1Fecho.MaxwellGlobal.axisCompactFockDomain_circular

