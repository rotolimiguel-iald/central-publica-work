import TGLExt.F1Fecho394.InvariantUnitaryEssentialR2
import TGLExt.F1Fecho394.WeylSegalDenseDomainR5
/-! Essential self-adjointness of the actual Segal field on the original
canonical bosonic Fock. The proof consumes the constructed Weyl group,
its exact derivative, and its invariant dense exponential domain.
This is not a Maxwell stress-tensor or spacetime-smearing construction. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential F1Fecho.Annihilation
open F1Fecho.DeficiencyCriterion

def segalFlow (f : H1) (t : ℝ) : F →L[ℂ] F := FieldWeyl.W ((t:ℂ) • f)

theorem segalFlow_zero (f : H1) (x : F) : segalFlow f 0 x=x := by
  simp [segalFlow,FieldWeyl.W_zero]

theorem segalFlow_add (f : H1) (s t : ℝ) (x : F) :
    segalFlow f (s+t) x=segalFlow f s (segalFlow f t x) := by
  have hp : WeylCoefficients.phase ((s:ℂ) • f) ((t:ℂ) • f)=1 := by
    have hz : (inner ℂ f f).im=0 := inner_self_im (𝕜:=ℂ) f
    rw [WeylCoefficients.phase, inner_smul_left, inner_smul_right]
    simp only [Complex.conj_ofReal,Complex.mul_im,Complex.ofReal_re,Complex.ofReal_im,
      hz,mul_zero,zero_mul,add_zero,Complex.ofReal_zero,neg_zero,Complex.exp_zero]
  change FieldWeyl.W (((s+t:ℝ):ℂ) • f) x=
    (FieldWeyl.W ((s:ℂ) • f)*FieldWeyl.W ((t:ℂ) • f)) x
  rw [FieldWeyl.W_ccr,hp,one_smul,← add_smul,← Complex.ofReal_add]

theorem segalFlow_norm (f : H1) (t : ℝ) (x : F) : ‖segalFlow f t x‖=‖x‖ := by
  change ‖ConcreteWeyl.D (FieldWeyl.rotate ((t:ℂ) • f)) x‖=‖x‖
  exact (ConcreteWeyl.D _).norm_map x

theorem segal_essentially_selfadjoint (f : H1) : IsSelfAdjoint (segal f).closure := by
  apply invariant_unitary_essentialSelfAdjoint (segal f) (segalFlow f) (Real.sqrt 2)
    (segalFlow_zero f) (segalFlow_add f) (segalFlow_norm f)
  · exact fun t x => Weyl_preserves_domain ((t:ℂ) • f) x
  · exact Weyl_domain_hasDerivAt f
  · exact segal_dense f
  · exact segal_formal_selfadjoint f
  · exact Real.sqrt_ne_zero'.mpr (by norm_num)

theorem segal_closure_has_exponential_core (f : H1) :
    (segal f).closure.HasCore domain := (segal f).closureHasCore

theorem segal_closure_isClosed (f : H1) : (segal f).closure.IsClosed :=
  (segal_essentially_selfadjoint f).isClosed

end F1Fecho.Creation
#print axioms F1Fecho.Creation.segalFlow_add
#print axioms F1Fecho.Creation.segalFlow_norm
#print axioms F1Fecho.Creation.segal_essentially_selfadjoint
#print axioms F1Fecho.Creation.segal_closure_has_exponential_core
#print axioms F1Fecho.Creation.segal_closure_isClosed
