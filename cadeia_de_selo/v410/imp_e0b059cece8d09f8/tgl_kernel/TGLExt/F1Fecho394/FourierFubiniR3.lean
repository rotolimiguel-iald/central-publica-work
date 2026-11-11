import TGLExt.F1Fecho394.FubiniTransposeR2
import TGLExt.F1Fecho394.FourierLpPostcompR1

/-! The Fourier transform in the real coordinate commutes with the actual
L2 Fubini interchange. Equality is proved first on a total rank-one family
and then by continuity, rather than assumed from a pointwise integral. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory
namespace F1Fecho.FourierFubini
open FubiniTranspose TensorL2 FourierNaturality
variable {X E : Type} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [TopologicalSpace.SeparableSpace E]
variable (μ : Measure X) [SFinite μ] [IsSeparable μ]
local instance : InnerProductSpace ℝ E := InnerProductSpace.complexToReal

def outerFourier : Lp (Lp E 2 μ) 2 (volume : Measure ℝ) →L[ℂ]
    Lp (Lp E 2 μ) 2 (volume : Measure ℝ) :=
  (Lp.fourierTransformₗᵢ ℝ (Lp E 2 μ)).toLinearIsometry.toContinuousLinearMap

def fiberFourier : Lp (Lp E 2 (volume : Measure ℝ)) 2 μ →L[ℂ]
    Lp (Lp E 2 (volume : Measure ℝ)) 2 μ :=
  (Lp.fourierTransformₗᵢ ℝ E).toLinearIsometry.toContinuousLinearMap.compLpL 2 μ

omit [TopologicalSpace.SeparableSpace E] in
theorem fourier_pointwise (a : Lp ℂ 2 (volume : Measure ℝ)) (e : E) :
    Lp.fourierTransformₗᵢ ℝ E (pointwise volume (a,e))=
      pointwise volume (Lp.fourierTransformₗᵢ ℝ ℂ a,e) :=
  fourier_compLp (ContinuousLinearMap.toSpanSingleton ℂ e) a

theorem transpose_fourier_rank_one (a : Lp ℂ 2 (volume : Measure ℝ)) (e : Lp E 2 μ) :
    transpose μ volume (outerFourier μ (pointwise volume (a,e)))=
      fiberFourier μ (transpose μ volume (pointwise volume (a,e))) := by
  change transpose μ volume (Lp.fourierTransformₗᵢ ℝ (Lp E 2 μ)
    (pointwise volume (a,e)))=_
  rw [fourier_pointwise]
  apply Lp.ext
  filter_upwards [transpose_rank_one_ae μ volume (Lp.fourierTransformₗᵢ ℝ ℂ a) e,
    transpose_rank_one_ae μ volume a e,
    (Lp.fourierTransformₗᵢ ℝ E).toLinearIsometry.toContinuousLinearMap.coeFn_compLpL
      (transpose μ volume (pointwise volume (a,e)))] with x hl ht hr
  rw [hl]
  change _=(fiberFourier μ (transpose μ volume (pointwise volume (a,e)))) x
  rw [show (fiberFourier μ (transpose μ volume (pointwise volume (a,e)))) x=
      Lp.fourierTransformₗᵢ ℝ E (transpose μ volume (pointwise volume (a,e)) x) from hr,
    ht,fourier_pointwise]

theorem transpose_fourier (f : Lp (Lp E 2 μ) 2 (volume : Measure ℝ)) :
    transpose μ volume (outerFourier μ f)=fiberFourier μ (transpose μ volume f) := by
  let L := (transpose μ volume).toContinuousLinearMap.comp (outerFourier (E:=E) μ)
  let R := (fiberFourier (E:=E) μ).comp (transpose μ volume).toContinuousLinearMap
  have h : L=R := by
    apply ContinuousLinearMap.ext_on
      (Submodule.dense_iff_topologicalClosure_eq_top.mpr
        (pointwise_total (E:=Lp E 2 μ) (volume : Measure ℝ)))
    rintro _ ⟨⟨a,e⟩,rfl⟩
    exact transpose_fourier_rank_one μ a e
  exact congrArg (fun T => T f) h

end F1Fecho.FourierFubini
#print axioms F1Fecho.FourierFubini.fourier_pointwise
#print axioms F1Fecho.FourierFubini.transpose_fourier_rank_one
#print axioms F1Fecho.FourierFubini.transpose_fourier
