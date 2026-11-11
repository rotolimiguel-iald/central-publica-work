import TGLExt.F1Fecho394.ExponentialCreationVectorR2
import Mathlib.Analysis.InnerProductSpace.LinearPMap
/-! Actual creation and symmetric Segal operators on the existing dense
exponential domain. The creation output is not claimed to remain in that
domain. Closed adjoints give closed extensions; essential self-adjointness,
the Weyl-generator identity, spacetime smearing and Maxwell stress are separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicSectors F1Fecho.Exponential
open F1Fecho.Annihilation

def creationCombination (f : H1) : (H1 →₀ ℂ) →ₗ[ℂ] F :=
  Finsupp.linearCombination ℂ (creationVector f)

theorem inner_creationCombination (f h : H1) (c : H1 →₀ ℂ) :
    inner ℂ (exponential h) (creationCombination f c) =
      inner ℂ h f * inner ℂ (exponential h) (synthesize c) := by
  classical
  simp only [creationCombination,synthesize,Finsupp.linearCombination_apply,Finsupp.sum,
    inner_sum,inner_smul_right,exponential_inner_creationVector,exponential_inner,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro g hg
  ring

theorem creationCombination_kernel (f : H1) (c : H1 →₀ ℂ) (hc : synthesize c = 0) :
    creationCombination f c = 0 := by
  apply exponential_orthogonal_zero
  intro h
  apply inner_eq_zero_symm.mp
  rw [inner_creationCombination,hc,inner_zero_right,mul_zero]

theorem creationCombination_eq (f : H1) (c d : H1 →₀ ℂ)
    (h : synthesize c = synthesize d) : creationCombination f c = creationCombination f d := by
  apply sub_eq_zero.mp
  rw [← map_sub]
  apply creationCombination_kernel
  rw [map_sub,h,sub_self]

def creationOnDomain (f : H1) : domain →ₗ[ℂ] F where
  toFun x := creationCombination f (preimage x)
  map_add' x y := by
    rw [← map_add]
    apply creationCombination_eq
    rw [map_add,preimage_spec,preimage_spec,preimage_spec]
    rfl
  map_smul' z x := by
    change creationCombination f (preimage (z • x)) = z • creationCombination f (preimage x)
    rw [← map_smul]
    apply creationCombination_eq
    rw [map_smul,preimage_spec,preimage_spec]
    rfl

def creation (f : H1) : F →ₗ.[ℂ] F where
  domain := domain
  toFun := creationOnDomain f

theorem creation_exponential (f g : H1) :
    creation f ⟨exponential g,exponential_mem_domain g⟩ = creationVector f g := by
  change creationCombination f (preimage ⟨exponential g,exponential_mem_domain g⟩) = _
  have h := creationCombination_eq f (preimage ⟨exponential g,exponential_mem_domain g⟩)
    (Finsupp.single g 1) (by rw [preimage_spec]; simp [synthesize])
  simpa [creationCombination] using h

theorem finite_pairing (f : H1) (c d : H1 →₀ ℂ) :
    inner ℂ (weighted f c) (synthesize d) =
      inner ℂ (synthesize c) (creationCombination f d) := by
  classical
  change inner ℂ (∑ h ∈ c.support,c h • (inner ℂ f h • exponential h)) (synthesize d) =
    inner ℂ (∑ h ∈ c.support,c h • exponential h) (creationCombination f d)
  simp only [sum_inner,inner_smul_left,inner_creationCombination,inner_conj_symm]

theorem annihilation_creation_formalAdjoint (f : H1) :
    (annihilation f).IsFormalAdjoint (creation f) := by
  intro x y
  have h := finite_pairing f (preimage x) (preimage y)
  rw [preimage_spec,preimage_spec] at h
  exact h

theorem creation_dense (f : H1) : Dense ((creation f).domain : Set F) := domain_dense

theorem creation_le_annihilation_adjoint (f : H1) : creation f ≤ (annihilation f).adjoint :=
  (annihilation_creation_formalAdjoint f).le_adjoint domain_dense

theorem annihilation_le_creation_adjoint (f : H1) : annihilation f ≤ (creation f).adjoint :=
  (annihilation_creation_formalAdjoint f).symm.le_adjoint (creation_dense f)

theorem annihilation_has_closed_extension (f : H1) :
    ∃ T : F →ₗ.[ℂ] F, T.IsClosed ∧ annihilation f ≤ T :=
  ⟨(creation f).adjoint,LinearPMap.adjoint_isClosed (creation_dense f),
    annihilation_le_creation_adjoint f⟩

theorem creation_has_closed_extension (f : H1) :
    ∃ T : F →ₗ.[ℂ] F, T.IsClosed ∧ creation f ≤ T :=
  ⟨(annihilation f).adjoint,LinearPMap.adjoint_isClosed domain_dense,
    creation_le_annihilation_adjoint f⟩

theorem exponential_inner_oneParticle (h f : H1) :
    inner ℂ (exponential h) (oneParticle f) = inner ℂ h f := by
  change inner ℂ (exponential h) (lp.single 2 1 (oneParticleEmbedding f)) = _
  rw [lp.inner_single_right]
  change inner ℂ (component h 1) (pureTensor 1 f) = _
  have hw : (weight 1 : ℂ) = 1 := by norm_num [weight]
  rw [component,hw,one_smul]
  exact (pureTensor_inner h f 1).trans (pow_one _)

theorem creationVector_zero (f : H1) : creationVector f 0 = oneParticle f := by
  apply sub_eq_zero.mp
  apply exponential_orthogonal_zero
  intro h
  apply inner_eq_zero_symm.mp
  rw [inner_sub_right,exponential_inner_creationVector,exponential_inner_oneParticle]
  simp

theorem creation_vacuum (f : H1) : creation f ⟨vacuum,vacuum_mem_domain⟩ = oneParticle f := by
  have h := creation_exponential f 0
  simpa only [exponential_zero,creationVector_zero] using h

def segal (f : H1) : F →ₗ.[ℂ] F where
  domain := domain
  toFun := ((Real.sqrt 2)⁻¹ : ℂ) • (onDomain f + creationOnDomain f)

theorem segal_formal_selfadjoint (f : H1) : (segal f).IsFormalAdjoint (segal f) := by
  intro x y
  change inner ℂ (((Real.sqrt 2)⁻¹ : ℂ) • (annihilation f x + creation f x)) (y : F) =
    inner ℂ (x : F) (((Real.sqrt 2)⁻¹ : ℂ) • (annihilation f y + creation f y))
  rw [inner_smul_left,inner_smul_right,inner_add_left,inner_add_right]
  rw [annihilation_creation_formalAdjoint f x y,
    (annihilation_creation_formalAdjoint f).symm x y]
  simp only [map_inv₀,Complex.conj_ofReal]
  ring

theorem segal_dense (f : H1) : Dense ((segal f).domain : Set F) := domain_dense

theorem segal_has_closed_extension (f : H1) :
    ∃ T : F →ₗ.[ℂ] F, T.IsClosed ∧ segal f ≤ T :=
  ⟨(segal f).adjoint,LinearPMap.adjoint_isClosed (segal_dense f),
    (segal_formal_selfadjoint f).le_adjoint (segal_dense f)⟩

theorem segal_vacuum (f : H1) :
    segal f ⟨vacuum,vacuum_mem_domain⟩ = ((Real.sqrt 2)⁻¹ : ℂ) • oneParticle f := by
  change ((Real.sqrt 2)⁻¹ : ℂ) •
    (annihilation f ⟨vacuum,vacuum_mem_domain⟩ + creation f ⟨vacuum,vacuum_mem_domain⟩) = _
  rw [annihilation_vacuum,creation_vacuum,zero_add]

end F1Fecho.Creation
#print axioms F1Fecho.Creation.creationCombination_kernel
#print axioms F1Fecho.Creation.annihilation_creation_formalAdjoint
#print axioms F1Fecho.Creation.creation_has_closed_extension
#print axioms F1Fecho.Creation.creation_vacuum
#print axioms F1Fecho.Creation.segal_formal_selfadjoint
#print axioms F1Fecho.Creation.segal_has_closed_extension
#print axioms F1Fecho.Creation.segal_vacuum
