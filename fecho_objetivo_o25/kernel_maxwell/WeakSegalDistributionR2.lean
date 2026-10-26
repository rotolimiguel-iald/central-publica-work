import PhysicalSchwartzMaxwellR1

/-! Real-linear Segal smearing and continuous matrix elements on the actual
dense exponential domain. This does not assert products preserve that domain
or construct a Wick stress tensor. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential F1Fecho.Annihilation
open scoped Topology

theorem creation_inner_on_domain (h f : H1) (x : domain) :
    inner ℂ (exponential h) (creation f x)=inner ℂ h f*inner ℂ (exponential h) (x:F) := by
  change inner ℂ (exponential h) (creationCombination f (preimage x))=_
  rw [inner_creationCombination,preimage_spec]

theorem annihilation_parameter_continuous (x : domain) :
    Continuous (fun f : H1 => annihilation f x) := by
  change Continuous (fun f : H1 => ∑ g ∈ (preimage x).support,
    (preimage x) g • (inner ℂ f g • exponential g))
  apply continuous_finset_sum
  intro g hg
  exact continuous_const.smul ((continuous_id.inner continuous_const).smul continuous_const)

theorem creation_weak_continuous (x y : domain) :
    Continuous (fun f : H1 => inner ℂ (x:F) (creation f y)) := by
  have he : (fun f : H1 => inner ℂ (x:F) (creation f y))=
      (fun f => inner ℂ (annihilation f x) (y:F)) := by
    funext f
    exact (annihilation_creation_formalAdjoint f x y).symm
  rw [he]
  exact (annihilation_parameter_continuous x).inner continuous_const

theorem segal_weak_continuous (x y : domain) :
    Continuous (fun f : H1 => inner ℂ (x:F) (segal f y)) := by
  change Continuous (fun f : H1 => inner ℂ (x:F)
    (((Real.sqrt 2)⁻¹:ℂ) • (annihilation f y+creation f y)))
  simp only [inner_smul_right,inner_add_right]
  exact continuous_const.mul ((continuous_const.inner (annihilation_parameter_continuous y)).add
    (creation_weak_continuous x y))

theorem annihilation_parameter_add (f g : H1) (x : domain) :
    annihilation (f+g) x=annihilation f x+annihilation g x := by
  change weighted (f+g) (preimage x)=weighted f (preimage x)+weighted g (preimage x)
  simp only [weighted,Finsupp.linearCombination_apply,Finsupp.sum,inner_add_left,
    add_smul,smul_add,Finset.sum_add_distrib]

theorem annihilation_parameter_real_smul (r : ℝ) (f : H1) (x : domain) :
    annihilation ((r:ℂ)•f) x=(r:ℂ)•annihilation f x := by
  change weighted ((r:ℂ)•f) (preimage x)=(r:ℂ)•weighted f (preimage x)
  simp [weighted,Finsupp.linearCombination_apply,Finsupp.sum,inner_smul_left,Complex.conj_ofReal,
    smul_smul,Finset.smul_sum,mul_comm,mul_left_comm,mul_assoc]

theorem creation_parameter_add (f g : H1) (x : domain) :
    creation (f+g) x=creation f x+creation g x := by
  apply sub_eq_zero.mp
  apply exponential_orthogonal_zero
  intro h
  apply inner_eq_zero_symm.mp
  rw [inner_sub_right,inner_add_right]
  simp only [creation_inner_on_domain,inner_add_right]
  ring

theorem creation_parameter_real_smul (r : ℝ) (f : H1) (x : domain) :
    creation ((r:ℂ)•f) x=(r:ℂ)•creation f x := by
  apply sub_eq_zero.mp
  apply exponential_orthogonal_zero
  intro h
  apply inner_eq_zero_symm.mp
  rw [inner_sub_right]
  simp only [creation_inner_on_domain,inner_smul_right]
  ring

theorem segal_parameter_add (f g : H1) (x : domain) :
    segal (f+g) x=segal f x+segal g x := by
  change ((Real.sqrt 2)⁻¹:ℂ) • (annihilation (f+g) x+creation (f+g) x)=_
  rw [annihilation_parameter_add,creation_parameter_add]
  change _=((Real.sqrt 2)⁻¹:ℂ) • (annihilation f x+creation f x)+
    ((Real.sqrt 2)⁻¹:ℂ) • (annihilation g x+creation g x)
  simp only [smul_add]
  abel

theorem segal_parameter_real_smul (r : ℝ) (f : H1) (x : domain) :
    segal ((r:ℂ)•f) x=(r:ℂ)•segal f x := by
  change ((Real.sqrt 2)⁻¹:ℂ) • (annihilation ((r:ℂ)•f) x+creation ((r:ℂ)•f) x)=_
  rw [annihilation_parameter_real_smul,creation_parameter_real_smul,←smul_add]
  exact smul_comm _ _ _

end F1Fecho.Creation
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Fecho.Creation F1Fecho.Annihilation

def weakPhysicalField (x y : domain) : SchwartzTensor →L[ℝ] ℂ where
  toFun f:=inner ℂ (x:F1Rede.BosonicFock.F) (segal (physicalSmearCLM f) y)
  map_add' f g:=by rw [map_add,segal_parameter_add,inner_add_right]
  map_smul' r f:=by
    have hp : physicalSmearCLM (r•f)=(r:ℂ)•physicalSmearCLM f := by
      rw [←Complex.coe_smul,map_smul]
    rw [hp,segal_parameter_real_smul,inner_smul_right]
    exact (Algebra.smul_def r _).symm
  cont:= (segal_weak_continuous x y).comp physicalSmearCLM.continuous

theorem weakPhysicalField_apply (x y : domain) (f : SchwartzTensor) :
    weakPhysicalField x y f=inner ℂ (x:F1Rede.BosonicFock.F)
      (segal (physicalSmearCLM f) y) := rfl

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.Creation.segal_weak_continuous
#print axioms F1Fecho.Creation.segal_parameter_add
#print axioms F1Fecho.Creation.segal_parameter_real_smul
#print axioms F1Fecho.MaxwellGlobal.weakPhysicalField_apply
