import TGLExt.F1Fecho394.ExponentialAnnihilationR2
/-! Domain invariance and a non-vacuity witness for the actual annihilation map.
The witness uses the already constructed nontrivial H1. These are algebraic
operators on a dense domain, not a Maxwell stress tensor or a spacetime field. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.Annihilation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential

theorem weighted_mem_domain (f : H1) (c : H1 →₀ ℂ) : weighted f c ∈ domain := by
  classical
  change (∑ g ∈ c.support, c g • (inner ℂ f g • exponential g)) ∈ domain
  exact domain.sum_mem (fun g _ => domain.smul_mem _
    (domain.smul_mem _ (exponential_mem_domain g)))

theorem annihilation_preserves_domain (f : H1) (x : domain) : annihilation f x ∈ domain :=
  weighted_mem_domain f (preimage x)

def onInvariantDomain (f : H1) : domain →ₗ[ℂ] domain :=
  (onDomain f).codRestrict domain (annihilation_preserves_domain f)

theorem onInvariantDomain_val (f : H1) (x : domain) :
    (onInvariantDomain f x : F) = annihilation f x := rfl

theorem exists_nonzero_annihilation :
    ∃ (f : H1) (x : domain), annihilation f x ≠ 0 := by
  haveI := AuditF13v31.H1_nontrivial
  obtain ⟨f, hf⟩ := exists_ne (0 : H1)
  exact ⟨f, ⟨exponential f, exponential_mem_domain f⟩, annihilation_nonzero f hf⟩

theorem domain_nontrivial : Nontrivial domain := by
  have hv : vacuum ≠ 0 := exponential_zero ▸ exponential_ne_zero 0
  exact ⟨⟨⟨vacuum,vacuum_mem_domain⟩,0,fun h => hv (congrArg Subtype.val h)⟩⟩

end F1Fecho.Annihilation
#print axioms F1Fecho.Annihilation.annihilation_preserves_domain
#print axioms F1Fecho.Annihilation.exists_nonzero_annihilation
#print axioms F1Fecho.Annihilation.domain_nontrivial
