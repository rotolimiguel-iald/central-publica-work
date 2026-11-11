import TGLExt.F1Fecho394.ExponentialDirectionalDerivativeR2
import TGLExt.F1Fecho394.CreationAndSegalR2
import TGLExt.F1Fecho394.FieldWeylR3
/-! Generator identity on the same dense exponential domain. The house uses
W(f)=D(i f), with no 1/sqrt(2) in W. Therefore d W(tf)/dt at zero is
sqrt(2) i times the symmetric Segal operator, not just i times Segal.
No essential self-adjointness or spacetime Maxwell realization is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Complex
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.Annihilation

theorem creationVector_smul (z : ℂ) (f g : H1) :
    creationVector (z • f) g = z • creationVector f g := by
  apply sub_eq_zero.mp
  apply exponential_orthogonal_zero
  intro h
  apply inner_eq_zero_symm.mp
  simp only [inner_sub_right,exponential_inner_creationVector,inner_smul_right]
  ring

def amplitudeLine (f g : H1) (z : ℂ) : ℂ :=
  Complex.exp (-(z*z)*inner ℂ f f/2 + I*z*inner ℂ f g)

theorem amplitudeLine_real (f g : H1) (t : ℝ) :
    WeylCoefficients.amplitude (FieldWeyl.rotate ((t:ℂ) • f)) g = amplitudeLine f g t := by
  unfold WeylCoefficients.amplitude FieldWeyl.rotate amplitudeLine
  congr 1
  simp only [inner_smul_left,inner_smul_right,Complex.conj_I,Complex.conj_ofReal]
  ring_nf
  simp only [I_sq]
  ring

theorem amplitudeLine_hasDerivAt (f g : H1) :
    HasDerivAt (amplitudeLine f g) (I * inner ℂ f g) 0 := by
  have hz := hasDerivAt_id (0:ℂ)
  have hq := (((hz.mul hz).neg.mul_const (inner ℂ f f)).div_const 2).add
    ((hz.const_mul I).mul_const (inner ℂ f g))
  change HasDerivAt (fun z : ℂ => Complex.exp (-(z*z)*inner ℂ f f/2 + I*z*inner ℂ f g)) _ _
  simpa only [Pi.add_apply,Pi.mul_apply,Pi.neg_apply,id_eq,mul_zero,zero_mul,
    neg_zero,zero_div,zero_add,add_zero,mul_one,one_mul,Complex.exp_zero] using hq.cexp

theorem Weyl_exponential_line (f g : H1) (t : ℝ) :
    FieldWeyl.W ((t:ℂ) • f) (exponential g) =
      amplitudeLine f g t • exponential (g+(t:ℂ) • (I • f)) := by
  rw [FieldWeyl.W,ConcreteWeyl.W_exponential,amplitudeLine_real]
  congr 2
  simp only [FieldWeyl.rotate,smul_smul,mul_comm I]

theorem Weyl_exponential_hasDerivAt (f g : H1) :
    HasDerivAt (fun t : ℝ => FieldWeyl.W ((t:ℂ) • f) (exponential g))
      (I • (inner ℂ f g • exponential g + creationVector f g)) 0 := by
  have hd := (amplitudeLine_hasDerivAt f g).smul (exponential_line_hasDerivAt (I • f) g)
  have hd' : HasDerivAt (fun z : ℂ => amplitudeLine f g z • exponential (g+z • (I • f)))
      (I • (inner ℂ f g • exponential g + creationVector f g)) 0 := by
    change HasDerivAt (fun z : ℂ => amplitudeLine f g z • exponential (g+z • (I • f)))
      (amplitudeLine f g 0 • creationVector (I • f) g +
        (I * inner ℂ f g) • exponential (g+0 • (I • f))) 0 at hd
    simpa only [amplitudeLine,zero_mul,mul_zero,neg_zero,zero_div,zero_add,
      add_zero,zero_smul,Complex.exp_zero,one_smul,creationVector_smul,
      smul_add,smul_smul,mul_one,one_mul,add_comm] using hd
  have ho : HasDerivAt (fun t : ℝ => (t:ℂ)) 1 0 := by
    simpa only [Complex.ofRealCLM_apply,Complex.ofReal_one] using!
      (Complex.ofRealCLM.hasDerivAt (x := (0:ℝ)))
  have hr := hd'.scomp (h := fun t : ℝ => (t:ℂ)) (0:ℝ) ho
  simpa only [Function.comp_def,Complex.ofRealCLM_apply,one_smul,
    ← Weyl_exponential_line] using hr

theorem Weyl_exponential_segal (f g : H1) :
    HasDerivAt (fun t : ℝ => FieldWeyl.W ((t:ℂ) • f) (exponential g))
      ((I * (Real.sqrt 2:ℂ)) • segal f ⟨exponential g,exponential_mem_domain g⟩) 0 := by
  have hs : (Real.sqrt 2:ℂ) ≠ 0 := by exact_mod_cast (Real.sqrt_ne_zero'.mpr (by norm_num : (0:ℝ)<2))
  convert Weyl_exponential_hasDerivAt f g using 1
  change (I * (Real.sqrt 2:ℂ)) • (((Real.sqrt 2)⁻¹:ℂ) •
    (annihilation f ⟨exponential g,exponential_mem_domain g⟩ +
     creation f ⟨exponential g,exponential_mem_domain g⟩)) = _
  rw [annihilation_exponential,creation_exponential,smul_smul]
  congr 1
  field_simp

end F1Fecho.Creation
#print axioms F1Fecho.Creation.creationVector_smul
#print axioms F1Fecho.Creation.amplitudeLine_real
#print axioms F1Fecho.Creation.Weyl_exponential_hasDerivAt
#print axioms F1Fecho.Creation.Weyl_exponential_segal
