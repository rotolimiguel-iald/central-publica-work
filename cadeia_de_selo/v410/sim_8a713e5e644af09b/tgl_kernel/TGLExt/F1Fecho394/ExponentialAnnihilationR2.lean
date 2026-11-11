import TGLExt.F1Fecho394.ExponentialTotalityR4
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
import Mathlib.LinearAlgebra.LinearPMap
/-! The annihilation map on the actual canonical Fock exponential domain.
Well-definedness is proved by differentiating the already proved exponential
inner kernel. No boundedness, creation operator, physical smearing, stress tensor,
or Maxwell equation is assumed or asserted. The domain is dense and concrete. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.Annihilation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential

def synthesize : (H1 →₀ ℂ) →ₗ[ℂ] F := Finsupp.linearCombination ℂ exponential
def weighted (f : H1) : (H1 →₀ ℂ) →ₗ[ℂ] F :=
  Finsupp.linearCombination ℂ (fun g => inner ℂ f g • exponential g)

theorem weighted_kernel (f : H1) (c : H1 →₀ ℂ) (hc : synthesize c = 0) :
    weighted f c = 0 := by
  classical
  apply exponential_orthogonal_zero
  intro h
  have hz (z : ℂ) :
      (∑ g ∈ c.support, c g * Complex.exp (inner ℂ h g + z * inner ℂ f g)) = 0 := by
    have hv := congrArg (fun v : F => inner ℂ (exponential (h + (star z) • f)) v) hc
    simpa only [synthesize,Finsupp.linearCombination_apply,Finsupp.sum,
      inner_sum,inner_smul_right,exponential_inner,inner_add_left,inner_smul_left,
      starRingEnd_apply,star_star,inner_zero_right] using hv
  have hd : HasDerivAt
      (fun z : ℂ => ∑ g ∈ c.support, c g * Complex.exp (inner ℂ h g + z * inner ℂ f g))
      (∑ g ∈ c.support, c g * (Complex.exp (inner ℂ h g) * inner ℂ f g)) 0 := by
    apply HasDerivAt.fun_sum
    intro g hg
    simpa only [id_eq,zero_mul,add_zero,one_mul] using
      (((hasDerivAt_id (0 : ℂ)).mul_const (inner ℂ f g)).const_add
        (inner ℂ h g)).cexp.const_mul (c g)
  have he : (∑ g ∈ c.support, c g * (Complex.exp (inner ℂ h g) * inner ℂ f g)) = 0 := by
    have hf : (fun z : ℂ => ∑ g ∈ c.support, c g * Complex.exp (inner ℂ h g + z * inner ℂ f g)) =
        (fun _ : ℂ => 0) := funext hz
    rw [hf] at hd
    exact hd.unique (hasDerivAt_const (0 : ℂ) (0 : ℂ))
  have hi : inner ℂ (exponential h) (weighted f c) = 0 := by
    simpa only [weighted,Finsupp.linearCombination_apply,Finsupp.sum,
      inner_sum,inner_smul_right,exponential_inner,mul_comm (inner ℂ f _) ] using he
  exact (inner_eq_zero_symm).mp hi

theorem weighted_eq_of_synthesize_eq (f : H1) (c d : H1 →₀ ℂ)
    (h : synthesize c = synthesize d) : weighted f c = weighted f d := by
  apply sub_eq_zero.mp
  rw [← map_sub]
  apply weighted_kernel
  rw [map_sub,h,sub_self]

def domain : Submodule ℂ F := LinearMap.range synthesize

def preimage (x : domain) : H1 →₀ ℂ := Classical.choose x.property
theorem preimage_spec (x : domain) : synthesize (preimage x) = x := Classical.choose_spec x.property

def onDomain (f : H1) : domain →ₗ[ℂ] F where
  toFun x := weighted f (preimage x)
  map_add' x y := by
    rw [← map_add]
    apply weighted_eq_of_synthesize_eq
    rw [map_add,preimage_spec,preimage_spec,preimage_spec]
    rfl
  map_smul' z x := by
    change weighted f (preimage (z • x)) = z • weighted f (preimage x)
    rw [← map_smul]
    apply weighted_eq_of_synthesize_eq
    rw [map_smul,preimage_spec,preimage_spec]
    rfl

def annihilation (f : H1) : F →ₗ.[ℂ] F where
  domain := domain
  toFun := onDomain f

theorem exponential_mem_domain (g : H1) : exponential g ∈ domain := by
  refine ⟨Finsupp.single g 1, ?_⟩
  simp [synthesize]

theorem annihilation_exponential (f g : H1) :
    annihilation f ⟨exponential g, exponential_mem_domain g⟩ = inner ℂ f g • exponential g := by
  change weighted f (preimage ⟨exponential g,exponential_mem_domain g⟩) = _
  have h := weighted_eq_of_synthesize_eq f
    (preimage ⟨exponential g,exponential_mem_domain g⟩) (Finsupp.single g 1)
    (by rw [preimage_spec]; simp [synthesize])
  simpa [weighted] using h

theorem domain_eq_span : domain = Submodule.span ℂ (Set.range exponential) := by
  exact Finsupp.range_linearCombination ℂ

theorem domain_dense : Dense (domain : Set F) := by
  apply Submodule.dense_iff_topologicalClosure_eq_top.mpr
  rw [domain_eq_span]
  exact exponential_total

theorem vacuum_mem_domain : vacuum ∈ domain := exponential_zero ▸ exponential_mem_domain 0

theorem annihilation_vacuum (f : H1) : annihilation f ⟨vacuum,vacuum_mem_domain⟩ = 0 := by
  have h := annihilation_exponential f 0
  simpa only [exponential_zero,inner_zero_right,zero_smul] using h

theorem exponential_ne_zero (g : H1) : exponential g ≠ 0 := by
  intro h
  have hi := exponential_inner g g
  rw [h,inner_zero_right] at hi
  exact Complex.exp_ne_zero _ hi.symm

theorem annihilation_nonzero (f : H1) (hf : f ≠ 0) :
    annihilation f ⟨exponential f,exponential_mem_domain f⟩ ≠ 0 := by
  rw [annihilation_exponential]
  exact smul_ne_zero (fun h => hf (inner_self_eq_zero.mp h)) (exponential_ne_zero f)

end F1Fecho.Annihilation
#print axioms F1Fecho.Annihilation.weighted_kernel
#print axioms F1Fecho.Annihilation.annihilation_exponential
#print axioms F1Fecho.Annihilation.domain_dense
#print axioms F1Fecho.Annihilation.annihilation_vacuum
#print axioms F1Fecho.Annihilation.annihilation_nonzero
