import TGLExt.F1Fecho394.FourierFubiniR3
import TGLExt.V350FourierL1L2

/-! Pointwise representatives of the actual partialTransform L2 Fourier transform.
The section L1 hypothesis is explicit. L2 and the interchanging of Fubini and
Fourier are consequences of the already constructed unitary maps. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped FourierTransform
namespace F1Fecho.PartialFourierRepresentative
open FubiniTranspose FourierFubini
variable {X E : Type} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [TopologicalSpace.SeparableSpace E]
variable (μ : Measure X) [SFinite μ] [IsSeparable μ]
local instance : InnerProductSpace ℝ E := InnerProductSpace.complexToReal

def partialTransform (f : Lp E 2 (μ.prod (volume : Measure ℝ))) :
    Lp E 2 (μ.prod (volume : Measure ℝ)) :=
  (F1Rede.fubiniL2Equiv (𝕜:=ℂ)).symm
    (outerFourier μ (F1Rede.fubiniL2Equiv (𝕜:=ℂ) f))

theorem partial_section_fourier_ae (f : Lp E 2 (μ.prod (volume : Measure ℝ)))
    (hf : ∀ᵐ x ∂μ, Integrable (fun r : ℝ => f (x,r))) :
    ∀ᵐ x ∂μ, (fun p : ℝ => partialTransform μ f (x,p)) =ᵐ[volume]
      𝓕 (fun r : ℝ => f (x,r)) := by
  let t := transpose μ volume (F1Rede.fubiniL2Equiv (𝕜:=ℂ) f)
  have he : transpose μ volume (F1Rede.fubiniL2Equiv (𝕜:=ℂ) (partialTransform μ f))=
      fiberFourier μ t := by
    simp only [partialTransform,LinearIsometryEquiv.apply_symm_apply]
    exact transpose_fourier μ _
  have hout := transpose_fubini_ae μ volume (partialTransform μ f)
  rw [he] at hout
  filter_upwards [hout,transpose_fubini_ae μ volume f,
    (Lp.fourierTransformₗᵢ ℝ E).toLinearIsometry.toContinuousLinearMap.coeFn_compLpL t,
    hf] with x ho hi hm hL1
  have hi' : (t x : ℝ → E) =ᵐ[volume] fun r => f (x,r) := hi
  have hL2 : MemLp (fun r => f (x,r)) 2 := (memLp_congr_ae hi').mp (Lp.memLp (t x))
  have ht : hL2.toLp (fun r => f (x,r))=t x := Lp.ext (hL2.coeFn_toLp.trans hi'.symm)
  have hF := TGLV350.Fourier.fourier_integral_ae_eq_L2 _ hL1 hL2
  rw [ht] at hF
  have hm' : fiberFourier μ t x=Lp.fourierTransformₗᵢ ℝ E (t x) := hm
  rw [hm'] at ho
  exact ho.symm.trans hF.symm

end F1Fecho.PartialFourierRepresentative
#print axioms F1Fecho.PartialFourierRepresentative.partial_section_fourier_ae
