import TGLExt.F1Fecho394.OneParticleSymplecticR2
/-! Exact one-particle symplectic duality for the already constructed standard
wedge. The reverse inclusion uses the actual self-adjoint TW and its domain;
no Haag-duality or Fock polar-identification hypothesis is introduced. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.OneParticleDuality
open TGLExt.ImportedSQ F1Rede.CanonicalWedge AuditF13v31
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
open F1Fecho.OneParticleSymplectic

theorem symplectic_tomita_pairing (g : H1)
    (hg : g ∈ KWR.symplComp.toClosedSubmodule) (x : TW.domain) :
    inner ℂ (SW TW Jcandidate x) g = inner ℂ g (x : H1) := by
  obtain ⟨h,k,hh,hk,hx,hs⟩ :=
    domain_fixed_decomposition TW.domain (SW TW Jcandidate) SW_maps SW_involutive x
  have hhK : h ∈ KWR.toClosedSubmodule := hh
  have hkK : k ∈ KWR.toClosedSubmodule := hk
  have hg' := ClosedSubmodule.mem_symplComp_iff.mp hg
  have hreal : star (inner ℂ h g) = inner ℂ h g := by
    apply Complex.ext
    · simp only [Complex.star_def,Complex.conj_re]
    · simp only [Complex.star_def,Complex.conj_im,hg' h hhK,neg_zero]
  have kreal : star (inner ℂ k g) = inner ℂ k g := by
    apply Complex.ext
    · simp only [Complex.star_def,Complex.conj_re]
    · simp only [Complex.star_def,Complex.conj_im,hg' k hkK,neg_zero]
  have hswap : inner ℂ g h = inner ℂ h g := (inner_conj_symm g h).symm.trans hreal
  have kswap : inner ℂ g k = inner ℂ k g := (inner_conj_symm g k).symm.trans kreal
  rw [hs,hx,inner_sub_left,inner_smul_left,inner_add_right,inner_smul_right,hswap,kswap]
  simp only [map_neg,Complex.conj_I,neg_neg]
  ring

theorem Jcandidate_of_symplectic (g : H1)
    (hg : g ∈ KWR.symplComp.toClosedSubmodule) :
    Jcandidate g ∈ KWR.toClosedSubmodule := by
  obtain ⟨hd,heq⟩ := generic_adjoint_maximal TW TW_selfadjoint Jcandidate
    Jcandidate_involutive (fun x => symplectic_tomita_pairing g hg x)
  change Jcandidate g ∈ TW.domain at hd
  have hT : TW ⟨Jcandidate g,hd⟩ = g := heq
  apply (KWR_mem _).mpr
  refine ⟨hd,?_⟩
  change Jcandidate (TW ⟨Jcandidate g,hd⟩) = Jcandidate g
  rw [hT]

theorem Jcandidate_mem_symplectic_iff (g : H1) :
    Jcandidate g ∈ KWR.symplComp.toClosedSubmodule ↔ g ∈ KWR.toClosedSubmodule := by
  constructor
  · intro h
    simpa only [Jcandidate_involutive g] using Jcandidate_of_symplectic (Jcandidate g) h
  · exact Jcandidate_into_symplectic g

theorem Jcandidate_image_equals_symplectic :
    Jcandidate '' (KWR.toClosedSubmodule : Set H1) =
      (KWR.symplComp.toClosedSubmodule : Set H1) := by
  ext g
  constructor
  · rintro ⟨f,hf,rfl⟩
    exact Jcandidate_into_symplectic f hf
  · intro hg
    exact ⟨Jcandidate g,Jcandidate_of_symplectic g hg,Jcandidate_involutive g⟩

end F1Fecho.OneParticleDuality
#print axioms F1Fecho.OneParticleDuality.symplectic_tomita_pairing
#print axioms F1Fecho.OneParticleDuality.Jcandidate_of_symplectic
#print axioms F1Fecho.OneParticleDuality.Jcandidate_mem_symplectic_iff
#print axioms F1Fecho.OneParticleDuality.Jcandidate_image_equals_symplectic
