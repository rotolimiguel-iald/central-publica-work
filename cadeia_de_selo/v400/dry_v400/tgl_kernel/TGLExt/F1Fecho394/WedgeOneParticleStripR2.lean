import TGLExt.F1Fecho394.CanonicalH1StripR3
import TGLExt.F1Fecho394.CanonicalJBoostR3
import TGLExt.F1Fecho394.KMSBoundaryExchangeR1
/-! Standard-wedge vectors already satisfy the genuine half-modular domain
condition and TW f=Jf. Hence the two boundaries of their analytic correlation
are related by the Tomita exchange, using the real boost and its inverse. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.WedgeOneParticleStrip
open TGLExt.ImportedSQ F1Rede.CanonicalWedge
open F1Fecho.CanonicalH1Strip F1Fecho.CanonicalJBoost

def toDomain (f : KWR.toClosedSubmodule) : TW.domain :=
  ⟨f,((KWR_mem f).mp f.property).choose⟩

theorem half_fixed (f : KWR.toClosedSubmodule) : TW (toDomain f)=Jcandidate f := by
  apply Jcandidate.injective
  rw [Jcandidate_involutive]
  exact ((KWR_mem f).mp f.property).choose_spec

theorem boost_symm (s : ℝ) (f : H1) : (B0 s).symm f=B0 (-s) f := by
  apply (B0 s).injective
  rw [LinearIsometryEquiv.apply_symm_apply]
  have h := congrArg (fun u : H1≃ₗᵢ[ℂ]H1 => u f) (B0_add s (-s))
  simpa only [add_neg_cancel,B0_zero,LinearIsometryEquiv.coe_refl,id_eq,
    LinearIsometryEquiv.trans_apply] using h

theorem wedge_strip (f g : KWR.toClosedSubmodule) :
    DiffContOnCl ℂ (coefficient f g) {z : ℂ | 0<z.im ∧ z.im<1} ∧
    (∃ C : ℝ, ∀ z : ℂ, 0≤z.im → z.im≤1 → ‖coefficient f g z‖≤C) ∧
    (∀ t : ℝ, coefficient f g t=inner ℂ (f:H1) (B0 (2*Real.pi*t) g)) ∧
    (∀ t : ℝ, coefficient f g ((t:ℂ)+Complex.I)=
      inner ℂ (g:H1) (B0 (-(2*Real.pi*t)) f)) := by
  refine ⟨coefficient_analytic (toDomain f) (toDomain g),
    coefficient_bounded (toDomain f) (toDomain g),coefficient_real f g,?_⟩
  intro t
  rw [show coefficient f g ((t:ℂ)+Complex.I)=
      inner ℂ (TW (toDomain f)) (B0 (2*Real.pi*t) (TW (toDomain g))) from
      coefficient_top (toDomain f) (toDomain g) t,half_fixed,half_fixed]
  rw [KMSBoundaryExchange.exchange Jcandidate (B0 (2*Real.pi*t))
    (fun x => (Jcandidate_boost _ x).symm),boost_symm]

end F1Fecho.WedgeOneParticleStrip
#print axioms F1Fecho.WedgeOneParticleStrip.half_fixed
#print axioms F1Fecho.WedgeOneParticleStrip.boost_symm
#print axioms F1Fecho.WedgeOneParticleStrip.wedge_strip
