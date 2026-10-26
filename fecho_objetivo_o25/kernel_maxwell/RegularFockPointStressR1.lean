import CoherentPointStressR2
import FiniteCoherentKernelCalculusR2
import RegularMaxwellFockDomainR5
import RealProfileMaxwellNonzeroR3

/-! A pointwise sesquilinear stress FORM on the existing regular coherent Fock
 domain, with unique finite coefficients. Its conservation is proved from the
 actual Maxwell wave kernel. No density of this restricted domain, operator
 realization, Wick-smearing identity, boost covariance or null-plane charge is
 postulated. Positivity is asserted only on the explicit coherent witness. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.CoherentKernel

 theorem regularCoefficients_add (ψ χ : regularFockDomain) :
    regularCoefficients (ψ+χ)=regularCoefficients ψ+regularCoefficients χ := by
  apply regularSynthesis_injective
  rw [regularCoefficients_spec,map_add,regularCoefficients_spec,regularCoefficients_spec]
  rfl

 theorem regularCoefficients_smul (z : ℂ) (ψ : regularFockDomain) :
    regularCoefficients (z • ψ)=z • regularCoefficients ψ := by
  apply regularSynthesis_injective
  rw [regularCoefficients_spec,map_smul,regularCoefficients_spec]
  rfl

 def regularExponential (h : RegularLabel) : regularFockDomain :=
  ⟨exponential h.val,exponential_mem_regularFockDomain h.val h.property⟩

 theorem regularCoefficients_exponential (h : RegularLabel) :
    regularCoefficients (regularExponential h)=Finsupp.single h 1 := by
  apply Eq.symm
  apply regularCoefficients_unique
  simp [regularExponential,regularSynthesis]

 def pointStressForm (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  finiteKernel (fun h k : RegularLabel=>coherentProfileStress h.val k.val μ ν x)
    (regularCoefficients ψ) (regularCoefficients χ)

 theorem pointStressForm_exponential (h k : RegularLabel) (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm (regularExponential h) (regularExponential k) μ ν x=
      coherentProfileStress h.val k.val μ ν x := by
  simp only [pointStressForm,regularCoefficients_exponential,finiteKernel_single,
    map_one,one_mul]

 theorem pointStressForm_hermitian (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    (starRingEnd ℂ) (pointStressForm ψ χ μ ν x)=pointStressForm χ ψ μ ν x :=
  finiteKernel_hermitian _ (fun h k=>coherentProfileStress_hermitian h.val k.val μ ν x) _ _

 theorem pointStressForm_diagonal_real (ψ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    (pointStressForm ψ ψ μ ν x).im=0 :=
  finiteKernel_diagonal_real _ (fun h k=>coherentProfileStress_hermitian h.val k.val μ ν x) _

 theorem pointStressForm_add_left (ψ χ ζ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm (ψ+χ) ζ μ ν x=pointStressForm ψ ζ μ ν x+pointStressForm χ ζ μ ν x := by
  unfold pointStressForm
  rw [regularCoefficients_add]
  exact finiteKernel_add_left_of_hermitian _
    (fun h k=>coherentProfileStress_hermitian h.val k.val μ ν x) _ _ _

 theorem pointStressForm_add_right (ψ χ ζ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm ψ (χ+ζ) μ ν x=pointStressForm ψ χ μ ν x+pointStressForm ψ ζ μ ν x := by
  unfold pointStressForm
  rw [regularCoefficients_add,finiteKernel_add_right]

 theorem pointStressForm_smul_left (z : ℂ) (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm (z • ψ) χ μ ν x=(starRingEnd ℂ) z*pointStressForm ψ χ μ ν x := by
  unfold pointStressForm
  rw [regularCoefficients_smul,finiteKernel_smul_left]

 theorem pointStressForm_smul_right (z : ℂ) (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm ψ (z • χ) μ ν x=z*pointStressForm ψ χ μ ν x := by
  unfold pointStressForm
  rw [regularCoefficients_smul,finiteKernel_smul_right]

 theorem pointStressForm_symmetric (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm ψ χ μ ν x=pointStressForm ψ χ ν μ x := by
  simp only [pointStressForm,coherentProfileStress_symmetric (μ:=μ) (ν:=ν)]

 theorem pointStressForm_line_hasDerivAt (ψ χ : regularFockDomain) (ρ μ ν : Fin 4) (x : Spacetime) :
    HasDerivAt (fun t : ℝ=>pointStressForm ψ χ μ ν (x+t • spacetimeBasis ρ))
      (finiteKernel (fun h k : RegularLabel=>
        deriv (fun t : ℝ=>coherentProfileStress h.val k.val μ ν (x+t • spacetimeBasis ρ)) 0)
        (regularCoefficients ψ) (regularCoefficients χ)) 0 := by
  apply finiteKernel_hasDerivAt
  intro h k
  exact (coherentProfileStress_line_hasDerivAt h.val k.val h.property.1 k.property.1 ρ μ ν x).differentiableAt.hasDerivAt

 theorem pointStressForm_conserved (ψ χ : regularFockDomain) (ν : Fin 4) (x : Spacetime) :
    (∑μ : Fin 4,metricSignC μ*
      deriv (fun t : ℝ=>pointStressForm ψ χ μ ν (x+t • spacetimeBasis μ)) 0)=0 := by
  simp only [(pointStressForm_line_hasDerivAt ψ χ _ _ _ x).deriv]
  rw [finiteKernel_weighted_sum]
  have hM (h k : RegularLabel) :
      (∑μ : Fin 4,metricSignC μ*
        deriv (fun t : ℝ=>coherentProfileStress h.val k.val μ ν (x+t • spacetimeBasis μ)) 0)=0 :=
    coherentProfileStress_conserved h.val k.val h.property.1 k.property.1 ν x
  simp_rw [hM]
  exact finiteKernel_zero _ _

 def regularVacuum : regularFockDomain :=⟨vacuum,vacuum_mem_regularFockDomain⟩

 theorem regularVacuum_eq_exponential : regularVacuum=
    regularExponential ⟨0,strongRegularProfile_zero⟩ := by
  apply Subtype.ext
  exact exponential_zero.symm

 theorem pointStressForm_vacuum (μ ν : Fin 4) (x : Spacetime) :
    pointStressForm regularVacuum regularVacuum μ ν x=0 := by
  rw [regularVacuum_eq_exponential,pointStressForm_exponential,
    coherentProfileStress_diagonal,realProfileStress_zero,mul_zero]

 theorem pointStressForm_nontrivial :
    ∃ψ : regularFockDomain,0<(pointStressForm ψ ψ 0 0 0).re := by
  obtain ⟨h,hh,hp⟩:=exists_strongRegular_positive_stress
  refine ⟨regularExponential ⟨h,hh⟩,?_⟩
  rw [pointStressForm_exponential,coherentProfileStress_diagonal]
  have he : Complex.exp (inner ℂ h h)=Complex.ofReal (Real.exp (‖h‖^2)) := by
    rw [inner_self_eq_norm_sq_to_K]
    simp only [← Complex.ofReal_pow,Complex.ofReal_exp]
  rw [he]
  simpa only [Complex.mul_re,Complex.ofReal_re,Complex.ofReal_im,zero_mul,sub_zero] using
    mul_pos (Real.exp_pos (‖h‖^2)) hp

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.regularCoefficients_exponential
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_exponential
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_hermitian
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_diagonal_real
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_add_left
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_add_right
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_smul_left
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_smul_right
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_symmetric
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_conserved
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_vacuum
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_nontrivial
