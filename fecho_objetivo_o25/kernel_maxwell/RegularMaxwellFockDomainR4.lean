import RegularMaxwellEnergyR2
import MaxwellMomentTransportR3
import ExponentialLinearIndependenceR2
import BosonicFockGroupActions

/-! The finite coherent domain with actual polynomial L1/L2 energy moments.
It belongs to the SAME Fock and is invariant under the existing translations
and wedge boost. Unique coefficients follow from proved exponential independence.
No stress tensor, charge identity or MaxwellCertificate is supplied as input. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open F1Fecho.Exponential ChatgptAudit.WignerRapidityMeasure016

theorem strongRegularProfile_U1 (a : Fin 4→ℝ) (h : H1) (hh : StrongRegularProfile h) :
    StrongRegularProfile (U1 a h) := by
  constructor
  · intro m
    have hi : MeasureTheory.Integrable (fun y=>shellEnergy y^m*‖h y‖^1) (orbitalMeasure 0) := by
      simpa only [pow_one] using hh.1 m
    simpa only [pow_one] using moment_U1_integrable a h m 1 hi
  · exact fun m=>moment_U1_integrable a h m 2 (hh.2 m)

theorem strongRegularProfile_B0 (s : ℝ) (h : H1) (hh : StrongRegularProfile h) :
    StrongRegularProfile (B0 s h) := by
  constructor
  · intro m
    have hi : MeasureTheory.Integrable (fun y=>shellEnergy y^m*‖h y‖^1) (orbitalMeasure 0) := by
      simpa only [pow_one] using hh.1 m
    simpa only [pow_one] using moment_B0_integrable s h m 1 hi
  · exact fun m=>moment_B0_integrable s h m 2 (hh.2 m)

def RegularLabel := {h : H1 // StrongRegularProfile h}
def regularSynthesis : (RegularLabel→₀ℂ)→ₗ[ℂ]F :=
  Finsupp.linearCombination ℂ (fun h : RegularLabel=>exponential h.val)
def regularFockDomain : Submodule ℂ F := LinearMap.range regularSynthesis

theorem regularSynthesis_injective : Function.Injective regularSynthesis :=
  exponential_linearIndependent.comp (fun h : RegularLabel=>h.val) Subtype.val_injective

theorem regularFockDomain_eq_span : regularFockDomain=
    Submodule.span ℂ (Set.range (fun h : RegularLabel=>exponential h.val)) :=
  Finsupp.range_linearCombination ℂ

theorem exponential_mem_regularFockDomain (h : H1) (hh : StrongRegularProfile h) :
    exponential h∈regularFockDomain := by
  refine ⟨Finsupp.single ⟨h,hh⟩ 1,?_⟩
  simp [regularSynthesis]

theorem vacuum_mem_regularFockDomain : vacuum∈regularFockDomain :=
  exponential_zero ▸ exponential_mem_regularFockDomain 0 strongRegularProfile_zero

theorem gamma_mem_regularFockDomain (u : H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀h,StrongRegularProfile h→StrongRegularProfile (u h))
    (ψ : F) (hψ : ψ∈regularFockDomain) : gamma u ψ∈regularFockDomain := by
  have he : regularFockDomain≤regularFockDomain.comap (gamma u).toLinearMap := by
    rw [regularFockDomain_eq_span]
    apply Submodule.span_le.mpr
    rintro v ⟨h,rfl⟩
    change gamma u (exponential h.val)∈regularFockDomain
    rw [gamma_exponential]
    exact exponential_mem_regularFockDomain (u h.val) (hu h.val h.property)
  exact he hψ

theorem gamma_regularFockDomain_iff (u : H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀h,StrongRegularProfile h→StrongRegularProfile (u h))
    (hv : ∀h,StrongRegularProfile h→StrongRegularProfile (u.symm h)) (ψ : F) :
    gamma u ψ∈regularFockDomain ↔ ψ∈regularFockDomain := by
  constructor
  · intro hψ
    have h:=gamma_mem_regularFockDomain u.symm hv (gamma u ψ) hψ
    simpa only [gamma_symm,LinearIsometryEquiv.symm_apply_apply] using h
  · exact gamma_mem_regularFockDomain u hu ψ

theorem regularFockDomain_translate (a : Fin 4→ℝ) (ψ : F) :
    gamma (U1 a) ψ∈regularFockDomain ↔ ψ∈regularFockDomain := by
  apply gamma_regularFockDomain_iff
  · exact strongRegularProfile_U1 a
  · intro h hh
    rw [← U1_neg]
    exact strongRegularProfile_U1 (-a) h hh

theorem regularFockDomain_boost (s : ℝ) (ψ : F) :
    gamma (B0 s) ψ∈regularFockDomain ↔ ψ∈regularFockDomain := by
  apply gamma_regularFockDomain_iff
  · exact strongRegularProfile_B0 s
  · intro h hh
    have he : (B0 s).symm h=B0 (-s) h := orbitalBoostUnitary_symm_apply 0 s h
    rw [he]
    exact strongRegularProfile_B0 (-s) h hh

def regularCoefficients (ψ : regularFockDomain) : RegularLabel→₀ℂ :=
  Classical.choose ψ.property

theorem regularCoefficients_spec (ψ : regularFockDomain) :
    regularSynthesis (regularCoefficients ψ)=ψ.val := Classical.choose_spec ψ.property

theorem regularCoefficients_unique (ψ : regularFockDomain) (c : RegularLabel→₀ℂ)
    (hc : regularSynthesis c=ψ.val) : c=regularCoefficients ψ :=
  regularSynthesis_injective (hc.trans (regularCoefficients_spec ψ).symm)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.strongRegularProfile_U1
#print axioms F1Fecho.MaxwellGlobal.strongRegularProfile_B0
#print axioms F1Fecho.MaxwellGlobal.regularSynthesis_injective
#print axioms F1Fecho.MaxwellGlobal.vacuum_mem_regularFockDomain
#print axioms F1Fecho.MaxwellGlobal.regularFockDomain_translate
#print axioms F1Fecho.MaxwellGlobal.regularFockDomain_boost
#print axioms F1Fecho.MaxwellGlobal.regularCoefficients_unique
