import TGLExt.F1Fecho394.OneParticleDualityR2
import Mathlib.MeasureTheory.Measure.Typeclasses.NoAtoms
/-! The canonical half-modular multiplier has no fixed vector, since its
multiplier equals one only at a Lebesgue-null singleton. Consequently its
standard wedge is not symplectically isotropic. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.WedgeNonisotropic
open TGLExt.ImportedSQ F1Rede.CanonicalWedge F1Rede.Canonical AuditF13v31
open F1Fecho.OneParticleSymplectic F1Fecho.OneParticleDuality

theorem TW_fixed_zero (f : TW.domain) (hf : TW f = (f : H1)) : (f : H1) = 0 := by
  have hgraph : ((f : H1),(f : H1)) ∈ TW.graph := by
    simpa only [hf] using TW.mem_graph f
  have hmult := (TW_multiplier (f : H1) (f : H1)).mp hgraph
  have hzero : Phi (f : H1) = 0 := by
    apply Lp.ext
    filter_upwards [hmult,Measure.ae_ne (volume : Measure ℝ) 0,
      Lp.coeFn_zero (TransverseFiber) 2 (volume : Measure ℝ)] with x hx hxn hz
    rw [hz]
    have he : (Real.exp (2 * Real.pi ^ 2 * x) : ℂ) ≠ 1 := by
      intro he
      have hr : Real.exp (2 * Real.pi ^ 2 * x) = 1 := by exact_mod_cast he
      have harg := Real.exp_injective (hr.trans Real.exp_zero.symm)
      have hp : 2 * Real.pi ^ 2 ≠ 0 := mul_ne_zero (by norm_num) (pow_ne_zero _ Real.pi_ne_zero)
      exact hxn ((mul_eq_zero.mp harg).resolve_left hp)
    have hsm : ((Real.exp (2 * Real.pi ^ 2 * x) : ℂ) - 1) • Phi (f : H1) x = 0 := by
      rw [sub_smul,one_smul,← hx,sub_self]
    exact (smul_eq_zero.mp hsm).resolve_left (sub_ne_zero.mpr he)
  apply Phi.injective
  simpa using hzero

theorem KWR_inter_JKWR_zero (f : H1) (hf : f ∈ KWR.toClosedSubmodule)
    (hj : Jcandidate f ∈ KWR.toClosedSubmodule) : f = 0 := by
  obtain ⟨df,tf⟩ := TW_on_KWR f hf
  obtain ⟨dj,tj⟩ := TW_on_KWR (Jcandidate f) hj
  have tj' : TW ⟨Jcandidate f,dj⟩ = f := by simpa only [Jcandidate_involutive f] using tj
  have hsum : f + Jcandidate f = 0 := by
    apply TW_fixed_zero ⟨f + Jcandidate f,TW.domain.add_mem df dj⟩
    have h := TW.map_add ⟨f,df⟩ ⟨Jcandidate f,dj⟩
    change TW ⟨f + Jcandidate f,TW.domain.add_mem df dj⟩ = TW ⟨f,df⟩ + TW ⟨Jcandidate f,dj⟩ at h
    rw [tf,tj'] at h
    exact h.trans (add_comm _ _)
  have hjneg : Jcandidate f = -f := eq_neg_of_add_eq_zero_left (by simpa only [add_comm] using hsum)
  have hp := TW_positive ⟨f,df⟩
  rw [tf,hjneg,inner_neg_right,Complex.neg_re] at hp
  change 0 ≤ -(inner ℂ f f).re at hp
  have he : (inner ℂ f f).re = ‖f‖^2 := (norm_sq_eq_re_inner (𝕜 := ℂ) f).symm
  rw [he] at hp
  have hn : ‖f‖ = 0 := by
    nlinarith [norm_nonneg f]
  exact norm_eq_zero.mp hn

theorem KWR_not_isotropic : ∃ f ∈ KWR.toClosedSubmodule,
    ∃ g ∈ KWR.toClosedSubmodule, (inner ℂ f g).im ≠ 0 := by
  by_contra h
  push_neg at h
  obtain ⟨f,hf,hfn⟩ := spectralOutput_nonzero
  have hf' : f ∈ KWR.toClosedSubmodule := hf
  have hs : f ∈ KWR.symplComp.toClosedSubmodule := by
    apply ClosedSubmodule.mem_symplComp_iff.mpr
    intro g hg
    exact h g hg f hf'
  exact hfn (KWR_inter_JKWR_zero f hf' (Jcandidate_of_symplectic f hs))

end F1Fecho.WedgeNonisotropic
#print axioms F1Fecho.WedgeNonisotropic.TW_fixed_zero
#print axioms F1Fecho.WedgeNonisotropic.KWR_inter_JKWR_zero
#print axioms F1Fecho.WedgeNonisotropic.KWR_not_isotropic
