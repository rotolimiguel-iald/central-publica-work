import ExponentialAnnihilationR2
import Mathlib.LinearAlgebra.LinearIndependent.Basic

/-! Finite exponential vectors in the SAME Fock are linearly independent.
Dedekind independence of characters is reused. This gives unique finite
coefficients for regular-profile Wick domains, without a new quotient axiom. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.Exponential
open TGLExt.ImportedSQ F1Rede.BosonicFock

def coherentCharacter (h : H1) : Multiplicative H1 →* ℂ where
  toFun x:=Complex.exp (inner ℂ (Multiplicative.toAdd x) h)
  map_one' := by simp
  map_mul' x y:=by
    change Complex.exp (inner ℂ (Multiplicative.toAdd x+Multiplicative.toAdd y) h)=_
    rw [inner_add_left,Complex.exp_add]

theorem coherentCharacter_injective : Function.Injective coherentCharacter := by
  intro h k he
  have hr (x : H1) : (inner ℂ x h).re=(inner ℂ x k).re := by
    have hi:=congrArg (fun χ : Multiplicative H1→*ℂ => ‖χ (Multiplicative.ofAdd x)‖) he
    change ‖Complex.exp (inner ℂ x h)‖=‖Complex.exp (inner ℂ x k)‖ at hi
    rw [Complex.norm_exp,Complex.norm_exp] at hi
    exact Real.exp_injective hi
  have hz : (inner ℂ (h-k) (h-k)).re=0 := by
    rw [inner_sub_right,Complex.sub_re,hr (h-k),sub_self]
  have hn : ‖h-k‖^2=(inner ℂ (h-k) (h-k)).re := norm_sq_eq_re_inner (𝕜:=ℂ) (h-k)
  rw [hz] at hn
  have hn0 : ‖h-k‖=0 := by nlinarith [norm_nonneg (h-k)]
  exact sub_eq_zero.mp (norm_eq_zero.mp hn0)

theorem exponential_linearIndependent : LinearIndependent ℂ (exponential : H1→F) := by
  classical
  have hc : LinearIndependent ℂ (fun h : H1=>(coherentCharacter h : Multiplicative H1→ℂ)) :=
    (linearIndependent_monoidHom (Multiplicative H1) ℂ).comp coherentCharacter coherentCharacter_injective
  apply linearIndependent_iff'.mpr
  intro s c hs i hi
  apply (linearIndependent_iff'.mp hc) s c ?_ i hi
  funext z
  have hp:=congrArg (fun v : F=>inner ℂ (exponential (Multiplicative.toAdd z)) v) hs
  simpa only [inner_sum,inner_smul_right,inner_zero_right,exponential_inner,
    Finset.sum_apply,Pi.smul_apply,Pi.zero_apply,smul_eq_mul,coherentCharacter,MonoidHom.coe_mk,OneHom.coe_mk] using hp

theorem exponential_synthesize_injective : Function.Injective F1Fecho.Annihilation.synthesize :=
  exponential_linearIndependent

end F1Fecho.Exponential
#print axioms F1Fecho.Exponential.coherentCharacter_injective
#print axioms F1Fecho.Exponential.exponential_linearIndependent
#print axioms F1Fecho.Exponential.exponential_synthesize_injective
