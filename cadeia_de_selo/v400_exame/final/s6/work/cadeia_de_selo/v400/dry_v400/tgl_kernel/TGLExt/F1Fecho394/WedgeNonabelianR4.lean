import TGLExt.F1Fecho394.WedgeNonisotropicR5
import TGLExt.F1Fecho394.FieldWeylR3
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
/-! Noncommuting concrete Weyl operators in the canonical standard wedge.
The symplectic pairing is normalized by a real rescaling inside KWR; no
nonabelian-algebra premise is imported. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.WedgeNonabelian
open TGLExt.ImportedSQ F1Rede.CanonicalWedge F1Rede.BosonicFock
open F1Fecho.WeylCoefficients F1Fecho.WedgeNonisotropic

theorem W_ne_zero (f : H1) : FieldWeyl.W f ≠ 0 := by
  intro h
  have hw := FieldWeyl.W_ccr f (-f)
  rw [h,zero_mul,phase_self_neg,add_neg_cancel,FieldWeyl.W_zero,one_smul] at hw
  have hv := congrArg (fun a : F →L[ℂ] F => a vacuum) hw
  have hn := congrArg norm hv
  simp only [ContinuousLinearMap.zero_apply,ContinuousLinearMap.one_apply,norm_zero,vacuum_norm] at hn
  norm_num at hn

theorem phase_half_pi (f g : H1) (h : (inner ℂ f g).im = Real.pi / 2) :
    phase f g = -Complex.I ∧ phase g f = Complex.I := by
  have hs : (inner ℂ g f).im = -(Real.pi/2) := by
    rw [← inner_conj_symm g f]
    simpa only [Complex.star_def,Complex.conj_im,h]
  constructor
  · rw [phase,h]
    convert Complex.exp_neg_pi_div_two_mul_I using 1 <;> push_cast <;> ring
  · rw [phase,hs]
    convert Complex.exp_pi_div_two_mul_I using 1 <;> push_cast <;> ring

theorem normalized_pair : ∃ f ∈ KWR.toClosedSubmodule,
    ∃ g ∈ KWR.toClosedSubmodule, (inner ℂ f g).im = Real.pi/2 := by
  obtain ⟨f,hf,g,hg,hd⟩ := KWR_not_isotropic
  let t : ℝ := Real.pi / (2 * (inner ℂ f g).im)
  refine ⟨f,hf,t • g,KWR.toClosedSubmodule.toSubmodule.smul_mem t hg,?_⟩
  rw [inner_smul_right_eq_smul,Complex.smul_im]
  change t * (inner ℂ f g).im = Real.pi/2
  dsimp [t]
  field_simp [hd]

theorem wedge_nonabelian : ∃ a ∈ FieldWeyl.R KWR.toClosedSubmodule.toSubmodule,
    ∃ b ∈ FieldWeyl.R KWR.toClosedSubmodule.toSubmodule, a*b ≠ b*a := by
  obtain ⟨f,hf,g,hg,hfg⟩ := normalized_pair
  refine ⟨FieldWeyl.W f,FieldWeyl.W_mem_R _ f hf,
    FieldWeyl.W g,FieldWeyl.W_mem_R _ g hg,?_⟩
  intro hc
  rw [FieldWeyl.W_ccr,FieldWeyl.W_ccr,add_comm g f] at hc
  have he := (smul_left_injective ℂ (W_ne_zero (f+g))) hc
  obtain ⟨hp,hq⟩ := phase_half_pi f g hfg
  rw [hp,hq] at he
  have hi := congrArg Complex.im he
  norm_num at hi

end F1Fecho.WedgeNonabelian
#print axioms F1Fecho.WedgeNonabelian.W_ne_zero
#print axioms F1Fecho.WedgeNonabelian.phase_half_pi
#print axioms F1Fecho.WedgeNonabelian.normalized_pair
#print axioms F1Fecho.WedgeNonabelian.wedge_nonabelian
