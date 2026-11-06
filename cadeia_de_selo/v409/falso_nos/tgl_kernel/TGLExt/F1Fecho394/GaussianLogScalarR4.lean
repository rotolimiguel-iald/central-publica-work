import Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform
import TGLExt.ModularFlowLevel

/-! Scalar Gaussian averaging and endpoint decay for the log-resolvent
coordinate. The constants are derived from the Fourier integral. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.GaussianLogScalar
open ChatgptAudit

theorem gaussian_fourier (a:ℝ) (ha:0<a) (l:ℝ) :
    (∫t:ℝ,(Real.exp (-a*t^2):ℂ)*modularPhase t l)=
      ((Real.pi:ℂ)/a)^(1/2:ℂ)*Complex.exp (-(l:ℂ)^2/(4*a)) := by
  have he: (fun t:ℝ=>(Real.exp (-a*t^2):ℂ)*modularPhase t l)=
      (fun t:ℝ=>Complex.exp (Complex.I*(l:ℂ)*t)*Complex.exp (-(a:ℂ)*t^2)) := by
    funext t
    unfold modularPhase
    rw [Complex.ofReal_exp]
    push_cast
    rw [mul_comm]
    congr 2 <;> ring
  rw [he]
  exact fourierIntegral_gaussian (by simpa using ha) (l:ℂ)

theorem gaussian_linear_atTop (b:ℝ) (hb:0<b) (c:ℝ) :
    Tendsto (fun l:ℝ=>Real.exp (-b*l^2+c*l)) atTop (𝓝 0) := by
  have hg:Tendsto (fun l:ℝ=>Real.exp (-b*l^2)) atTop (𝓝 0) :=
    Real.tendsto_exp_atBot.comp
      ((tendsto_pow_atTop (by norm_num : (2:ℕ)≠0)).const_mul_atTop_of_neg (neg_lt_zero.mpr hb))
  have hs:Tendsto (fun l:ℝ=>l-c/(2*b)) atTop atTop := tendsto_atTop_add_const_right _ _ tendsto_id
  have ht: Tendsto (fun l:ℝ=>Real.exp (c^2/(4*b))*Real.exp (-b*(l-c/(2*b))^2))
      atTop (𝓝 0) := by simpa using (hg.comp hs).const_mul (Real.exp (c^2/(4*b)))
  convert ht using 1
  funext l
  rw [←Real.exp_add]
  congr 1
  field_simp [ne_of_gt hb]
  <;> ring

theorem gaussian_linear_atBot (b:ℝ) (hb:0<b) (c:ℝ) :
    Tendsto (fun l:ℝ=>Real.exp (-b*l^2+c*l)) atBot (𝓝 0) := by
  have h:=(gaussian_linear_atTop b hb (-c)).comp tendsto_neg_atBot_atTop
  convert h using 1
  funext l
  congr 1
  ring

def logCoordinate (x:ℝ):ℝ:=Real.log ((1-x)/x)
def compactify (f:ℝ→ℝ) (x:ℝ):ℝ:=if x=0 ∨ x=1 then 0 else f (logCoordinate x)

theorem logCoordinate_zero : Tendsto logCoordinate (𝓝[≠] (0:ℝ)) atTop := by
  have h1:Tendsto (fun x:ℝ=>Real.log (1-x)) (𝓝[≠] (0:ℝ)) (𝓝 0) := by
    have h:ContinuousAt (fun x:ℝ=>Real.log (1-x)) 0 :=
      (continuousAt_const.sub continuousAt_id).log (by norm_num)
    simpa using h.tendsto.mono_left nhdsWithin_le_nhds
  have h:=h1.add_atTop (tendsto_neg_atBot_atTop.comp Real.tendsto_log_nhdsNE_zero)
  apply h.congr'
  filter_upwards [self_mem_nhdsWithin,
    (eventually_ne_nhdsWithin (s:={0}ᶜ) (by norm_num : (0:ℝ)≠1))] with x hx hx1
  simp only [Set.mem_compl_iff,Set.mem_singleton_iff] at hx
  dsimp only [logCoordinate]
  rw [Real.log_div (sub_ne_zero.mpr (Ne.symm hx1)) hx,sub_eq_add_neg]
  simp only [Function.comp_apply,sub_eq_add_neg]

theorem logCoordinate_one : Tendsto logCoordinate (𝓝[≠] (1:ℝ)) atBot := by
  have hn:Tendsto (fun x:ℝ=>1-x) (𝓝[≠] (1:ℝ)) (𝓝[≠] (0:ℝ)) := by
    apply tendsto_nhdsWithin_iff.mpr
    constructor
    · have h:ContinuousAt (fun x:ℝ=>1-x) 1 := by fun_prop
      simpa using h.tendsto.mono_left nhdsWithin_le_nhds
    · filter_upwards [self_mem_nhdsWithin] with x hx
      simp only [Set.mem_compl_iff,Set.mem_singleton_iff] at hx ⊢
      exact sub_ne_zero.mpr (Ne.symm hx)
  have h2:Tendsto (fun x:ℝ=>Real.log x) (𝓝[≠] (1:ℝ)) (𝓝 0) := by
    simpa using (Real.continuousAt_log (by norm_num : (1:ℝ)≠0)).tendsto.mono_left nhdsWithin_le_nhds
  have h:=(Real.tendsto_log_nhdsNE_zero.comp hn).atBot_add h2.neg
  apply h.congr'
  filter_upwards [self_mem_nhdsWithin,
    (eventually_ne_nhdsWithin (s:={1}ᶜ) (by norm_num : (1:ℝ)≠0))] with x hx hx0
  simp only [Set.mem_compl_iff,Set.mem_singleton_iff] at hx
  dsimp only [logCoordinate]
  rw [Real.log_div (sub_ne_zero.mpr (Ne.symm hx)) hx0,sub_eq_add_neg]
  simp only [Function.comp_apply,sub_eq_add_neg]

theorem compactify_continuous (f:ℝ→ℝ) (hf:Continuous f)
    (h0:Tendsto f atTop (𝓝 0)) (h1:Tendsto f atBot (𝓝 0)) : Continuous (compactify f) := by
  rw [continuous_iff_continuousAt]
  intro x
  by_cases hz:x=0
  · subst x
    rw [continuousAt_iff_punctured_nhds]
    simp only [compactify,ite_true,true_or]
    apply (h0.comp logCoordinate_zero).congr'
    filter_upwards [self_mem_nhdsWithin,
      (eventually_ne_nhds (by norm_num : (0:ℝ)≠1)).filter_mono nhdsWithin_le_nhds] with y hy hy1
    simp only [Set.mem_compl_iff,Set.mem_singleton_iff] at hy
    simp [compactify,hy,hy1]
  · by_cases ho:x=1
    · subst x
      rw [continuousAt_iff_punctured_nhds]
      simp only [compactify,ite_true,or_true]
      apply (h1.comp logCoordinate_one).congr'
      filter_upwards [self_mem_nhdsWithin,
        (eventually_ne_nhds (by norm_num : (1:ℝ)≠0)).filter_mono nhdsWithin_le_nhds] with y hy hy0
      simp only [Set.mem_compl_iff,Set.mem_singleton_iff] at hy
      simp [compactify,hy,hy0]
    · have hc:ContinuousAt (fun y:ℝ=>f (logCoordinate y)) x := by
        apply hf.continuousAt.comp
        unfold logCoordinate
        apply ContinuousAt.log
        · fun_prop
        · exact div_ne_zero (sub_ne_zero.mpr (Ne.symm ho)) hz
      apply hc.congr_of_eventuallyEq
      filter_upwards [eventually_ne_nhds hz,eventually_ne_nhds ho] with y hy0 hy1
      simp [compactify,hy0,hy1]

end F1Fecho.GaussianLogScalar
#print axioms F1Fecho.GaussianLogScalar.gaussian_fourier
#print axioms F1Fecho.GaussianLogScalar.gaussian_linear_atTop
#print axioms F1Fecho.GaussianLogScalar.gaussian_linear_atBot
#print axioms F1Fecho.GaussianLogScalar.compactify_continuous
