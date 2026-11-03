import TGLExt.F1Fecho394.WeylVacuumCoefficientR2
import TGLExt.F1Fecho394.KMSFiniteSpanR3
/-! An actual one-particle strip produces the field-Weyl KMS pair.  This
generic composition lemma exposes the strip inputs; its concrete consumer
must provide them by proved one-particle terms. The positive boost parameter
is the physical KMS flow, opposite to the modular parameter. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.WeylStripFromCoefficient
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 F1Rede.BosonicFock
open F1Fecho.FieldWeyl F1Fecho.WeylVacuumCoefficient

theorem pair_from_coefficient (u : ℝ → H1 ≃ₗᵢ[ℂ] H1) (f g : H1)
    (C : ℂ → ℂ) (hC : DiffContOnCl ℂ C (kmsStrip 1))
    (hbound : ∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ 1 → ‖C z‖ ≤ M)
    (hlower : ∀ t : ℝ, C t = inner ℂ f (u t g))
    (hupper : ∀ t : ℝ, C ((t:ℂ)+Complex.I) = inner ℂ g (u (-t) f)) :
    KMSFiniteSpan.Pair vacuum (fun t => gamma (u t)) (W f) (W g) := by
  let a : ℂ := -((‖f‖ : ℂ)^2)/2 - ((‖g‖ : ℂ)^2)/2
  let G : ℂ → ℂ := fun z => Complex.exp (a - C z)
  have hG : DiffContOnCl ℂ G (kmsStrip 1) :=
    Complex.differentiable_exp.comp_diffContOnCl (hC.const_sub a)
  obtain ⟨M,hM⟩ := hbound
  refine ⟨G,hG,⟨Real.exp (‖a‖+M),?_⟩,?_,?_⟩
  · intro z h0 h1
    exact (Complex.norm_exp_le_exp_norm (a-C z)).trans
      (Real.exp_le_exp.mpr ((norm_sub_le a (C z)).trans
        (_root_.add_le_add (le_refl ‖a‖) (hM z h0 h1))))
  · intro t
    rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_left,
      vacuum_two_weyl]
    simp only [G,a,hlower]
  · intro t
    rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_left,
      vacuum_two_weyl]
    simp only [G,a,hupper]
    congr 1
    ring

end F1Fecho.WeylStripFromCoefficient

#print axioms F1Fecho.WeylStripFromCoefficient.pair_from_coefficient
