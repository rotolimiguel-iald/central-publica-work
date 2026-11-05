import TGLExt.F1Fecho394.GaussianResolventRegularizerR4
import TGLExt.F1Fecho394.GroupAverageApproximationR2
import Mathlib.Analysis.SpecificLimits.Basic

/-! The real Gaussian average is the spectral regularizer of the actual
resolvent group. Equality is proved on the dense damped range, then on H.
This is an operator theorem, not a new assumption about the weight GNS. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.GaussianResolventAverage
open TGLV350.Regular F1Fecho.GaussianLogScalar F1Fecho.GaussianResolventRegularizer
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : Module ℝ (H→L[ℂ]H) := Module.restrictScalars ℝ ℂ _
variable (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
  (hi:Function.Injective R) (hj:Function.Injective (1-R:H→L[ℂ]H))

def average (c:ℝ) : H→L[ℂ]H := StrongUnitaryAverage.average
  (fun t=>resolventImaginaryPower R hR h1 hi hj (c*t))
  (fun x=>(resolventImaginaryPower_strongly_continuous R hR h1 hi hj x).comp
    (continuous_const.mul continuous_id)) gaussianWeight gaussianWeight_integrable

theorem average_apply (c:ℝ) (x:H) : average R hR h1 hi hj c x=
    ∫t:ℝ,gaussianWeight t • resolventImaginaryPower R hR h1 hi hj (c*t) x := rfl

include hR h1 in
theorem weighted_phase_operator (c:ℝ) (hc:c≠0) :
    (∫t:ℝ,(gaussianWeight t:ℂ) • resolventPhaseOperator R (c*t))=
      spectral R (c^2/4) * resolventDampingOperator R := by
  have hb:0<c^2/4:=div_pos (sq_pos_of_ne_zero hc) (by norm_num)
  have hs:=IsSelfAdjoint.of_nonneg hR
  rw [←ResolventScaledPhaseIntegral.weighted_phase_integral R hR h1 c gaussianWeight
    gaussianWeight_continuous gaussianWeight_integrable]
  simp only [gaussian_phase_integral]
  rw [spectral,cfc_real_eq_complex _ hs,←resolventDampingOperator_cfc R hs]
  have hg:Continuous (fun z:ℂ=>(gaussianSymbol (c^2/4) z.re:ℂ)) :=
    Complex.continuous_ofReal.comp ((gaussianSymbol_continuous _ hb).comp Complex.continuous_re)
  have hd:Continuous (fun z:ℂ=>(resolventDamping z.re:ℂ)) := by
    unfold resolventDamping
    fun_prop
  rw [←cfc_mul _ _ R hg.continuousOn hd.continuousOn]
  apply cfc_congr
  intro z hz
  exact mul_comm _ _

theorem average_damping (c:ℝ) (hc:c≠0) (x:H) :
    average R hR h1 hi hj c (resolventDampingOperator R x)=
      spectral R (c^2/4) (resolventDampingOperator R x) := by
  rw [average_apply]
  simp only [resolventImaginaryPower_damping]
  have hint:=ResolventScaledPhaseIntegral.weighted_phase_integrable R hR h1 c gaussianWeight
    gaussianWeight_continuous gaussianWeight_integrable
  have he:=ContinuousLinearMap.integral_apply hint x
  have hv:=congrArg (fun A:H→L[ℂ]H=>A x) (weighted_phase_operator R hR h1 c hc)
  rw [he] at hv
  have hsmul (r : ℝ) (v : H) : (r : ℂ) • v = r • v := by
    exact (RCLike.real_smul_eq_coe_smul (K := ℂ) r v).symm
  simpa only [ContinuousLinearMap.smul_apply, hsmul, ContinuousLinearMap.mul_apply] using hv

theorem average_eq_spectral (c:ℝ) (hc:c≠0) :
    average R hR h1 hi hj c=spectral R (c^2/4) := by
  ext1 x
  refine (resolventDampingOperator_denseRange R hR h1 hi hj).induction ?_
    (isClosed_eq (average R hR h1 hi hj c).continuous (spectral R (c^2/4)).continuous) x
  rintro _ ⟨y,rfl⟩
  exact average_damping R hR h1 hi hj c hc y

theorem average_root_domain (c:ℝ) (hc:c≠0) (x:H) :
    ∃y,(average R hR h1 hi hj c x,y)∈(resolventSquareRoot R hR hi).graph := by
  rw [average_eq_spectral R hR h1 hi hj c hc]
  exact spectral_root_domain R hR h1 hi _ (div_pos (sq_pos_of_ne_zero hc) (by norm_num)) x

def scale (n:ℕ):ℝ:=1/((n:ℝ)+1)

theorem scale_ne_zero (n:ℕ) : scale n≠0 := by unfold scale; positivity

theorem average_tendsto (x:H) :
    Tendsto (fun n:ℕ=>average R hR h1 hi hj (scale n) x) atTop (𝓝 x) := by
  exact GroupAverageApproximation.averages_tendsto_identity
    (resolventImaginaryPower R hR h1 hi hj)
    (resolventImaginaryPower_strongly_continuous R hR h1 hi hj)
    (resolventImaginaryPower_zero R hR h1 hi hj)
    gaussianWeight gaussianWeight_integrable gaussianWeight_integral scale
    tendsto_one_div_add_atTop_nhds_zero_nat x

end F1Fecho.GaussianResolventAverage
#print axioms F1Fecho.GaussianResolventAverage.weighted_phase_operator
#print axioms F1Fecho.GaussianResolventAverage.average_eq_spectral
#print axioms F1Fecho.GaussianResolventAverage.average_root_domain
#print axioms F1Fecho.GaussianResolventAverage.average_tendsto
