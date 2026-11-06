import TGLExt.F1Fecho394.RegularCoreAverageR2
/-! The adjoint of the same regular average is a translated average.
This uses strong vector integrals, never operator-norm integrability. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularAverageAdjoint
open MeasureTheory TGLV350 TGLV350.Regular
open F1Fecho.RegularCovariantCore F1Fecho.RegularCoreAverage
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def reverseFamily (B : UnitaryFlow H) : StrongIntegral.Family (H:=RegularHilbert H) where
  op t := regularUnitary B (-t)
  continuous_apply v := (regular_strongly_continuous B v).comp continuous_neg
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound t := (regularIntegralFamily B).norm_bound (-t)

theorem integral_star (B : UnitaryFlow H) (a b : ℝ) :
    star (StrongIntegral.operatorIntegral (regularIntegralFamily B) a b)=
      StrongIntegral.operatorIntegral (reverseFamily B) a b := by
  apply ContinuousLinearMap.ext
  intro x
  apply ext_inner_left ℂ
  intro y
  rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right,
    StrongIntegral.operatorIntegral_inner,StrongIntegral.inner_operatorIntegral]
  apply intervalIntegral.integral_congr
  intro t _
  change inner ℂ (regularUnitary B t y) x=inner ℂ y (regularUnitary B (-t) x)
  rw [←regular_star B,ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_right]

theorem reverse_integral (B : UnitaryFlow H) (h : ℝ) :
    StrongIntegral.operatorIntegral (reverseFamily B) 0 h=
      regularUnitary B (-h)*StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h := by
  apply ContinuousLinearMap.ext
  intro x
  change (∫ t in 0..h,regularUnitary B (-t) x)=
    regularUnitary B (-h) (∫ t in 0..h,regularUnitary B t x)
  rw [←(regularUnitary B (-h)).intervalIntegral_comp_comm
    ((regular_strongly_continuous B x).intervalIntegrable 0 h)]
  have he : (fun t => regularUnitary B (-h) (regularUnitary B t x))=
      (fun t => regularUnitary B (t-h) x) := by
    funext t
    change (regularUnitary B (-h)*regularUnitary B t) x=_
    rw [F1Fecho.RegularCovariantCore.regular_mul]
    congr 2
    ring
  rw [he,intervalIntegral.integral_comp_neg (fun t : ℝ => regularUnitary B t x),
    intervalIntegral.integral_comp_sub_right (fun t : ℝ => regularUnitary B t x)]
  simp only [neg_zero,zero_sub,sub_self]

theorem regularAverage_star (B : UnitaryFlow H) (h : ℝ) :
    star (F1Fecho.RegularCoreAverage.regularAverage B h)=regularUnitary B (-h)*F1Fecho.RegularCoreAverage.regularAverage B h := by
  unfold F1Fecho.RegularCoreAverage.regularAverage
  change star (((h⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h) =
    regularUnitary B (-h) * (((h⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h)
  rw [star_smul,Complex.star_def,Complex.conj_ofReal,integral_star,reverse_integral,mul_smul_comm]

end F1Fecho.RegularAverageAdjoint
#print axioms F1Fecho.RegularAverageAdjoint.integral_star
#print axioms F1Fecho.RegularAverageAdjoint.reverse_integral
#print axioms F1Fecho.RegularAverageAdjoint.regularAverage_star
