import TGLExt.F1Fecho394.MaxwellComplexRapidityR3
import TGLExt.F1Fecho394.WedgePhysicalFourierR2
import TGLExt.F1Fecho394.PhysicalFourierDerivativeR4

/-! The strip coefficient uses the actual tensor entries and p-wedge-screen.
Its real boundary is the existing global coefficient of physicalFourierCLM;
its reflected lower boundary and analyticity are proved from real support. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
open MeasureTheory Matrix
open scoped FourierTransform
namespace F1Fecho.MaxwellStrip
open F1Fecho.MaxwellGlobal F1Fecho.WedgeLaplace SchwartzMap
open ChatgptAudit.WignerRapidityMeasure016 F1Rede.WedgeReflectionTranslations

def componentProjection (μ ν : Fin 4) : TensorValue →L[ℂ] ℂ :=
  (ContinuousLinearMap.proj ν : (Fin 4 → ℂ) →L[ℂ] ℂ).comp
    (ContinuousLinearMap.proj μ : TensorValue →L[ℂ] (Fin 4 → ℂ))

def componentTest (f : SchwartzTensor) (μ ν : Fin 4) : 𝓢(Spacetime,ℂ) :=
  SchwartzMap.postcompCLM (componentProjection μ ν) f

theorem componentTest_apply (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime) :
    componentTest f μ ν x=f x μ ν := rfl

theorem componentTest_real (f : SchwartzTensor) (hf : IsRealTest f) (μ ν : Fin 4) :
    ∀ x,(componentTest f μ ν x).im=0 := fun x => hf x μ ν

def supportedTensorRight (f : SchwartzTensor) : Prop :=
  ∀ x ∈ Function.support (f : Spacetime → TensorValue), |x 0| < x 1

theorem componentTest_supported (f : SchwartzTensor) (hf : supportedTensorRight f)
    (μ ν : Fin 4) : supportedRight (componentTest f μ ν) := by
  intro x hx
  apply hf x
  intro hz
  apply hx
  simp only [componentTest_apply,hz,Pi.zero_apply]

def maxwellLaplace (q : Fin 2 → ℝ) (f : SchwartzTensor) (j : Fin 2) (z : ℂ) : ℂ :=
  (1/2:ℂ)*∑ μ,∑ ν,analyticStrength q j μ ν z *
    scalarLaplace (transverseMass 0 q) (q 0) (q 1) (componentTest f μ ν) z

theorem componentLaplace_real (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (f : SchwartzTensor) (μ ν : Fin 4) :
    scalarLaplace (transverseMass 0 y.1) (y.1 0) (y.1 1) (componentTest f μ ν) y.2 =
      physicalFourierCLM f (shellEmbedding (rapidityChart 0 y)) μ ν := by
  rw [scalarLaplace_real_shell y hy]
  change (𝓕⁻ (SchwartzMap.postcompCLM (componentProjection μ ν) f)) _ = _
  rw [schwartz_fourierInv_postcomp,physicalFourier_apply]
  rfl

theorem maxwellLaplace_real (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (f : SchwartzTensor) (j : Fin 2) :
    maxwellLaplace y.1 f j y.2=globalCoefficient (physicalFourierCLM f) (rapidityChart 0 y) j := by
  change (1/2:ℂ)*(∑ μ,∑ ν,_)=(1/2:ℂ)*(∑ μ,∑ ν,_)
  congr 1
  apply Finset.sum_congr rfl
  intro μ _
  apply Finset.sum_congr rfl
  intro ν _
  rw [analyticStrength_real y hy,componentLaplace_real y hy]

theorem maxwellLaplace_differentiable (q : Fin 2 → ℝ) (f : SchwartzTensor)
    (hf : supportedTensorRight f) (j : Fin 2) :
    DifferentiableOn ℂ (maxwellLaplace q f j) lowerOpenStrip := by
  apply DifferentiableOn.const_mul
  apply DifferentiableOn.fun_sum
  intro μ _
  apply DifferentiableOn.fun_sum
  intro ν _
  exact (analyticStrength_entire q j μ ν).differentiableOn.mul
    (scalarLaplace_diffContOnCl _ _ _ _ (by unfold transverseMass; positivity)
      (componentTest_supported f hf μ ν)).1

theorem maxwellLaplace_continuous (q : Fin 2 → ℝ) (f : SchwartzTensor)
    (hf : supportedTensorRight f) (j : Fin 2) :
    ContinuousOn (maxwellLaplace q f j) lowerClosedStrip := by
  apply ContinuousOn.const_mul
  apply continuousOn_finsetSum
  intro μ _
  apply continuousOn_finsetSum
  intro ν _
  exact (analyticStrength_entire q j μ ν).continuous.continuousOn.mul
    (scalarLaplace_continuous_closed _ _ _ _ (by unfold transverseMass; positivity)
      (componentTest_supported f hf μ ν))

theorem maxwellLaplace_lower_real (q : Fin 2 → ℝ) (hq : q ≠ 0) (f : SchwartzTensor)
    (hf : IsRealTest f) (j : Fin 2) (r : ℝ) :
    maxwellLaplace q f j ((r:ℂ)-Complex.I*Real.pi)=star (maxwellLaplace (-q) f j r) := by
  have hn : -q ≠ 0 := neg_ne_zero.mpr hq
  have hterm (μ ν : Fin 4) :
      analyticStrength q j μ ν ((r:ℂ)-Complex.I*Real.pi) *
        scalarLaplace (transverseMass 0 q) (q 0) (q 1) (componentTest f μ ν) ((r:ℂ)-Complex.I*Real.pi) =
      star (analyticStrength (-q) j μ ν r *
        scalarLaplace (transverseMass 0 (-q)) ((-q) 0) ((-q) 1) (componentTest f μ ν) r) := by
    rw [analyticStrength_lower,scalarLaplace_lower_pi_real _ _ _ _ _ (componentTest_real f hf μ ν)]
    rw [analyticStrength_real (-q,r) hn,transverseMass_neg]
    simp only [Pi.neg_apply,star_mul,Complex.star_def,Complex.conj_ofReal]
    exact mul_comm _ _
  unfold maxwellLaplace
  simp_rw [hterm]
  simp only [Complex.star_def,map_mul,map_sum,map_div₀,map_one,map_ofNat]

end F1Fecho.MaxwellStrip
#print axioms F1Fecho.MaxwellStrip.maxwellLaplace_real
#print axioms F1Fecho.MaxwellStrip.maxwellLaplace_differentiable
#print axioms F1Fecho.MaxwellStrip.maxwellLaplace_continuous
#print axioms F1Fecho.MaxwellStrip.maxwellLaplace_lower_real
