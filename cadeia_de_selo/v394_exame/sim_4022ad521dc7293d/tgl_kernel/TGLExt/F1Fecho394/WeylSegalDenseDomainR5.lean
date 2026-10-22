import TGLExt.F1Fecho394.WeylSegalGeneratorR3
/-! The constructed exponential domain is invariant under every field Weyl
operator. The actual real derivative there equals i sqrt(2) times Segal.
This identifies a densely defined generator restriction; maximality and
essential self-adjointness are not conclusions of this module. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential F1Fecho.Annihilation

theorem Weyl_preserves_domain (f : H1) (x : domain) :
    FieldWeyl.W f (x:F) ∈ domain := by
  classical
  obtain ⟨c,hc⟩ := x.property
  rw [← hc]
  change FieldWeyl.W f (∑ g ∈ c.support,c g • exponential g) ∈ domain
  rw [map_sum]
  apply Submodule.sum_mem
  intro g hg
  rw [map_smul,FieldWeyl.W,ConcreteWeyl.W_exponential]
  exact domain.smul_mem _ (domain.smul_mem _ (exponential_mem_domain _))

theorem Weyl_domain_hasDerivAt (f : H1) (x : domain) :
    HasDerivAt (fun t : ℝ => FieldWeyl.W ((t:ℂ) • f) (x:F))
      ((Complex.I * (Real.sqrt 2:ℂ)) • segal f x) 0 := by
  classical
  let c := preimage x
  let y : H1 → domain := fun g => ⟨exponential g,exponential_mem_domain g⟩
  have hy : ∑ g ∈ c.support,c g • y g = x := by
    apply Subtype.ext
    simpa [synthesize,Finsupp.linearCombination_apply,Finsupp.sum,y,c] using preimage_spec x
  have hd := HasDerivAt.fun_sum (u := c.support) (fun g hg =>
    (Weyl_exponential_segal f g).const_smul (c g))
  convert! hd using 1
  · funext t
    rw [← hy]
    simp only [Submodule.coe_sum,Submodule.coe_smul_of_tower,map_sum,map_smul,Pi.smul_apply,y]
  · let S : domain →ₗ[ℂ] F := ((Real.sqrt 2)⁻¹:ℂ) • (onDomain f + creationOnDomain f)
    change (Complex.I * (Real.sqrt 2:ℂ)) • S x =
      ∑ g ∈ c.support,c g • (Complex.I * (Real.sqrt 2:ℂ)) • S (y g)
    rw [← hy,map_sum,Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro g hg
    rw [map_smul]
    exact smul_comm _ _ _

end F1Fecho.Creation
#print axioms F1Fecho.Creation.Weyl_preserves_domain
#print axioms F1Fecho.Creation.Weyl_domain_hasDerivAt
