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

theorem annihilate_exponential (f h : H1) :
    annihilation f (expDomain h)=(inner ℂ f h) • exponential h :=
  annihilation_exponential f h

def doubleAnnihilate (f g : H1) (x : domain) : F :=
  annihilation f (onInvariantDomain g x)

theorem doubleAnnihilate_exponential (f g h : H1) :
    doubleAnnihilate f g (expDomain h)=
      (inner ℂ g h*inner ℂ f h) • exponential h := by
  unfold doubleAnnihilate
  rw [invariant_exponential]
  change onDomain f ((inner ℂ g h) • expDomain h)=_
  rw [map_smul]
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
        (Complex.exp (inner ℂ h k)) := by
  unfold quadratic
  rw [doubleAnnihilate_exponential,doubleAnnihilate_exponential]
  rw [annihilate_exponential,annihilate_exponential,annihilate_exponential,annihilate_exponential]
  simp only [expDomain,inner_smul_left,inner_smul_right,
    exponential_inner,map_mul,inner_conj_symm]
  ring

theorem quadratic_vacuum (f g : H1) :
    quadratic f g ⟨vacuum,vacuum_mem_domain⟩ ⟨vacuum,vacuum_mem_domain⟩=0 := by
  have h:=coherent_kernel f g 0 0
  simpa [expDomain,exponential_zero] using h

theorem quadratic_hermitian_swap (f g : H1) (x y : domain) :
    star (quadratic f g x y)=quadratic g f y x := by
  change (starRingEnd ℂ) (quadratic f g x y)=quadratic g f y x
  simp only [quadratic,map_mul,map_add,map_div₀,map_one,map_ofNat,
    inner_conj_symm]
  ring

theorem diagonal_coherent_positive (f h : H1) :
    0≤(quadratic f f (expDomain h) (expDomain h)).re := by
  rw [coherent_kernel]
  have hc : inner ℂ f h+inner ℂ h f=(2*(inner ℂ f h).re:ℝ) := by
    calc
      _ = inner ℂ f h + (starRingEnd ℂ) (inner ℂ f h) := by rw [inner_conj_symm]
      _ = _ := Complex.add_conj _
  rw [hc]
  have he : inner ℂ h h=((inner ℂ h h).re:ℂ) := by
    apply Complex.ext
    · rfl
    · simpa only [Complex.ofReal_im] using inner_self_im (𝕜:=ℂ) h
  rw [he,←Complex.ofReal_exp]
  norm_cast
  convert mul_nonneg (mul_nonneg (by norm_num : (0:ℝ)≤(1/2:ℝ))
    (sq_nonneg (2*(inner ℂ f h).re))) (Real.exp_pos (inner ℂ h h).re).le using 1 <;> ring

end F1Fecho.WickForm
#print axioms F1Fecho.WickForm.invariant_exponential
#print axioms F1Fecho.WickForm.doubleAnnihilate_exponential
#print axioms F1Fecho.WickForm.coherent_kernel
#print axioms F1Fecho.WickForm.quadratic_vacuum
#print axioms F1Fecho.WickForm.quadratic_hermitian_swap
#print axioms F1Fecho.WickForm.diagonal_coherent_positive
