import RealSchwartzTestsR1
import SchwartzMaxwellNonzeroR6
import CanonicalSegalEssentialR6

/-! A real spacetime Schwartz test is mapped into the same H1 and then into
an essentially self-adjoint Segal operator on the same Fock. A real test has
nonzero vacuum excitation. Neither wedge localization nor Maxwell stress is
assumed or concluded; the Segal assignment is not complex-linear in its label. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Annihilation F1Fecho.Creation

abbrev RealTest := {f : SchwartzTensor // IsRealTest f}

theorem exists_nonzero_real_spacetimeSmear :
    ∃ f : RealTest,spacetimeSmear f.val≠0 := by
  obtain ⟨f,hf⟩ := exists_nonzero_spacetimeSmear
  by_cases hr : spacetimeSmear (realPart f)=0
  · refine ⟨⟨imagPart f,imagPart_real f⟩,?_⟩
    intro hi
    apply hf
    have hd:=congrArg spacetimeSmearLinear (real_imag_decomposition f)
    change spacetimeSmear f=spacetimeSmearLinear (realPart f+Complex.I•imagPart f) at hd
    rw [map_add,map_smul] at hd
    change spacetimeSmear f=spacetimeSmear (realPart f)+Complex.I•spacetimeSmear (imagPart f) at hd
    simpa only [hr,hi,smul_zero,add_zero] using hd
  · exact ⟨⟨realPart f,realPart_real f⟩,hr⟩

def field (f : RealTest) : F →ₗ.[ℂ] F := segal (spacetimeSmear f.val)

theorem field_essentially_selfadjoint (f : RealTest) :
    IsSelfAdjoint (field f).closure := segal_essentially_selfadjoint _

theorem field_has_exponential_core (f : RealTest) :
    (field f).closure.HasCore domain := segal_closure_has_exponential_core _

theorem field_vacuum (f : RealTest) :
    field f ⟨vacuum,vacuum_mem_domain⟩ =
      ((Real.sqrt 2)⁻¹ : ℂ) • oneParticle (spacetimeSmear f.val) := segal_vacuum _

theorem exists_nonzero_real_field_vacuum : ∃ f : RealTest,
    field f ⟨vacuum,vacuum_mem_domain⟩≠0 := by
  obtain ⟨f,hf⟩ := exists_nonzero_real_spacetimeSmear
  refine ⟨f,?_⟩
  rw [field_vacuum]
  apply smul_ne_zero
  · exact inv_ne_zero (Complex.ofReal_ne_zero.mpr (Real.sqrt_ne_zero'.mpr (by norm_num)))
  · intro hz
    apply hf
    apply oneParticle.injective
    simpa using hz

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_real_spacetimeSmear
#print axioms F1Fecho.MaxwellGlobal.field_essentially_selfadjoint
#print axioms F1Fecho.MaxwellGlobal.field_has_exponential_core
#print axioms F1Fecho.MaxwellGlobal.field_vacuum
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_real_field_vacuum
