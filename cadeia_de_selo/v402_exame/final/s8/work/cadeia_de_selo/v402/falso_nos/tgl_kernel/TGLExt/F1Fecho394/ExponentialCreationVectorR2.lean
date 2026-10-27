import TGLExt.F1Fecho394.AnnihilationDomainR1
import TGLExt.F1Fecho394.ConcreteWeylContinuityR2
import Mathlib.Analysis.Complex.CauchyIntegral
/-! Creation vectors by a Bochner Cauchy integral of the existing Fock
exponentials. Only their previously proved continuity and Gram kernel are used.
No creation operator or vector differentiability is a premise. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Complex Metric
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential

theorem map_circleIntegral {E G : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]
    [CompleteSpace E] [NormedAddCommGroup G] [NormedSpace ℂ G] [CompleteSpace G]
    (L : E →L[ℂ] G) (v : ℂ → E) (hv : CircleIntegrable v 0 1) :
    L (∮ z in C(0,1), v z) = ∮ z in C(0,1), L (v z) := by
  unfold circleIntegral
  rw [← L.intervalIntegral_comp_comm hv.out]
  congr 1
  funext t
  exact L.map_smul _ _

def integrand (f g : H1) (z : ℂ) : F := (1 / z^2) • exponential (g + z • f)

theorem integrand_integrable (f g : H1) : CircleIntegrable (integrand f g) 0 1 := by
  apply ContinuousOn.circleIntegrable (by norm_num)
  have hn : ∀ z ∈ sphere (0 : ℂ) 1, z^2 ≠ 0 := by
    intro z hz
    apply pow_ne_zero
    intro he
    simpa [he] using hz
  exact (continuousOn_const.div (continuousOn_id.pow 2) hn).smul
    ((ConcreteWeyl.exponential_continuous.comp
      (continuous_const.add (continuous_id.smul continuous_const))).continuousOn)

def creationVector (f g : H1) : F :=
  (2 * Real.pi * I : ℂ)⁻¹ • ∮ z in C(0,1), integrand f g z

theorem exponential_inner_creationVector (h f g : H1) :
    inner ℂ (exponential h) (creationVector f g) =
      inner ℂ h f * Complex.exp (inner ℂ h g) := by
  let L : F →L[ℂ] ℂ := innerSL ℂ (exponential h)
  let v : ℂ → ℂ := fun z => Complex.exp (inner ℂ h g + z * inner ℂ h f)
  have hd (z : ℂ) : HasDerivAt v
      (Complex.exp (inner ℂ h g + z * inner ℂ h f) * inner ℂ h f) z := by
    simpa only [v,id_eq,one_mul] using
      (((hasDerivAt_id z).mul_const (inner ℂ h f)).const_add (inner ℂ h g)).cexp
  have hv : DifferentiableOn ℂ v (closedBall 0 1) :=
    fun z _ => (hd z).differentiableAt.differentiableWithinAt
  have hc := DifferentiableOn.deriv_eq_smul_circleIntegral (c := 0) (R := 1)
    (by norm_num : (0:ℝ)<1) hv
  have hm : (fun z => L (integrand f g z)) = fun z => (1/z^2) • v z := by
    funext z
    simp only [L,integrand,innerSL_apply_apply,inner_smul_right,exponential_inner,
      inner_add_right,inner_smul_right,v,smul_eq_mul]
  change L ((2*Real.pi*I:ℂ)⁻¹ • ∮ z in C(0,1), integrand f g z) = _
  rw [map_smul,map_circleIntegral L _ (integrand_integrable f g),hm]
  simp only [sub_zero] at hc
  rw [hc,(hd 0).deriv]
  simp only [zero_mul,add_zero,smul_smul,inv_mul_cancel₀ two_pi_I_ne_zero,one_smul]
  exact mul_comm _ _

end F1Fecho.Creation
#print axioms F1Fecho.Creation.integrand_integrable
#print axioms F1Fecho.Creation.exponential_inner_creationVector
