import PhysicalSchwartzMaxwellR1
import AnnihilationDomainR1

/-! Normally ordered bilocal quadratic form on the existing dense exponential
domain. No product of unbounded creation operators is postulated. Coincident
point restriction, local Wick stress, and its integrated charge remain distinct. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.WickForm
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential F1Fecho.Annihilation

def expDomain (h : H1) : domain := ⟨exponential h,exponential_mem_domain h⟩

theorem invariant_exponential (f h : H1) :
    onInvariantDomain f (expDomain h)=(inner ℂ f h) • expDomain h := by
  apply Subtype.ext
  exact annihilation_exponential f h

def doubleAnnihilate (f g : H1) (x : domain) : F :=
  annihilation f (onInvariantDomain g x)

theorem doubleAnnihilate_exponential (f g h : H1) :
    doubleAnnihilate f g (expDomain h)=
      (inner ℂ g h*inner ℂ f h) • exponential h := by
  unfold doubleAnnihilate
  rw [invariant_exponential,map_smul]
  change (inner ℂ g h) • annihilation f ⟨exponential h,exponential_mem_domain h⟩=_
  rw [annihilation_exponential,smul_smul]

def quadratic (f g : H1) (x y : domain) : ℂ :=
  (1/2:ℂ)*(inner ℂ (x:F) (doubleAnnihilate f g y)+
    inner ℂ (annihilation g x) (annihilation f y)+
    inner ℂ (annihilation f x) (annihilation g y)+
    inner ℂ (doubleAnnihilate g f x) (y:F))

theorem coherent_kernel (f g h k : H1) :
    quadratic f g (expDomain h) (expDomain k)=
      (1/2:ℂ)*(inner ℂ f k+inner ℂ h f)*(inner ℂ g k+inner ℂ h g)*
        Complex.exp(inner ℂ h k) := by
  unfold quadratic
  rw [doubleAnnihilate_exponential,doubleAnnihilate_exponential]
  simp only [expDomain,annihilation_exponential,inner_smul_left,inner_smul_right,
    exponential_inner,map_mul,inner_conj_symm]
  ring

theorem quadratic_vacuum (f g : H1) :
    quadratic f g ⟨vacuum,vacuum_mem_domain⟩ ⟨vacuum,vacuum_mem_domain⟩=0 := by
  have h:=coherent_kernel f g 0 0
  simpa [expDomain,exponential_zero] using h

theorem quadratic_hermitian_swap (f g : H1) (x y : domain) :
    star (quadratic f g x y)=quadratic g f y x := by
  simp only [quadratic,map_mul,map_add,map_div₀,map_one,star_ofNat,
    inner_conj_symm,starRingEnd_apply]
  ring

theorem diagonal_coherent_positive (f h : H1) :
    0≤(quadratic f f (expDomain h) (expDomain h)).re := by
  rw [coherent_kernel]
  have hc : inner ℂ f h+inner ℂ h f=(2*(inner ℂ f h).re:ℝ) := by
    rw [←inner_conj_symm f h]
    exact Complex.add_conj _
  rw [hc]
  have he : inner ℂ h h=(‖h‖^2:ℝ) := inner_self_eq_norm_sq_to_K h
  rw [he,←Complex.ofReal_exp]
  norm_cast
  positivity

end F1Fecho.WickForm
#print axioms F1Fecho.WickForm.invariant_exponential
#print axioms F1Fecho.WickForm.doubleAnnihilate_exponential
#print axioms F1Fecho.WickForm.coherent_kernel
#print axioms F1Fecho.WickForm.quadratic_vacuum
#print axioms F1Fecho.WickForm.quadratic_hermitian_swap
#print axioms F1Fecho.WickForm.diagonal_coherent_positive
