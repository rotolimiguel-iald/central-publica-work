import TGLExt.F1Fecho394.ScreenLorentzTransportR7
import Mathlib.MeasureTheory.Function.Holder

/-! An a.e.-unitary matrix multiplier on the unchanged canonical H1.
No operator or isometry is assumed as a field: Holder multiplication constructs it. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace F1Fecho.OrbitalScreen
open ChatgptAudit.WignerRapidityMeasure016

abbrev FiberOperator := Fiber →L[ℂ] Fiber

def matrixFiberOperator (A : Matrix (Fin 2) (Fin 2) ℂ) : FiberOperator :=
  (Matrix.toEuclideanCLM (𝕜:=ℂ) (n:=Fin 2)) A

theorem matrixFiberOperator_continuous : Continuous matrixFiberOperator :=
  (Matrix.toEuclideanCLM (𝕜:=ℂ) (n:=Fin 2)).toAlgEquiv.toLinearEquiv.toLinearMap.continuous_of_finiteDimensional

theorem matrixFiberOperator_norm (A : Matrix (Fin 2) (Fin 2) ℂ)
    (hA : A ∈ Matrix.unitaryGroup (Fin 2) ℂ) (v : Fiber) :
    ‖matrixFiberOperator A v‖=‖v‖ := by
  let u : Fiber ≃ₗᵢ[ℂ] Fiber := Unitary.linearIsometryEquiv
    ⟨matrixFiberOperator A,Unitary.map_mem (Matrix.toEuclideanCLM (𝕜:=ℂ) (n:=Fin 2)) hA⟩
  exact u.norm_map v

theorem matrixFiberOperator_bound (A : Matrix (Fin 2) (Fin 2) ℂ)
    (hA : A ∈ Matrix.unitaryGroup (Fin 2) ℂ) : ‖matrixFiberOperator A‖≤1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro v
  rw [matrixFiberOperator_norm A hA,one_mul]

def matrixWeight (A : MomentumCoordinates → Matrix (Fin 2) (Fin 2) ℂ)
    (hA : Measurable A) (hu : ∀ᵐ p ∂orbitalMeasure 0, A p ∈ Matrix.unitaryGroup (Fin 2) ℂ) :
    Lp FiberOperator ∞ (orbitalMeasure 0) :=
  (memLp_top_of_bound (matrixFiberOperator_continuous.measurable.comp hA).aestronglyMeasurable 1
    (hu.mono fun p hp => matrixFiberOperator_bound (A p) hp)).toLp (matrixFiberOperator ∘ A)

theorem matrixWeight_ae (A : MomentumCoordinates → Matrix (Fin 2) (Fin 2) ℂ)
    (hA : Measurable A) (hu : ∀ᵐ p ∂orbitalMeasure 0, A p ∈ Matrix.unitaryGroup (Fin 2) ℂ) :
    matrixWeight A hA hu=ᵐ[orbitalMeasure 0] matrixFiberOperator ∘ A := MemLp.coeFn_toLp _

def matrixMultiplier (A : MomentumCoordinates → Matrix (Fin 2) (Fin 2) ℂ)
    (hA : Measurable A) (hu : ∀ᵐ p ∂orbitalMeasure 0, A p ∈ Matrix.unitaryGroup (Fin 2) ℂ) :
    TGLExt.ImportedSQ.H1 →L[ℂ] TGLExt.ImportedSQ.H1 :=
  (ContinuousLinearMap.id ℂ FiberOperator).holderL (orbitalMeasure 0) ∞ 2 2 (matrixWeight A hA hu)

theorem matrixMultiplier_ae (A : MomentumCoordinates → Matrix (Fin 2) (Fin 2) ℂ)
    (hA : Measurable A) (hu : ∀ᵐ p ∂orbitalMeasure 0, A p ∈ Matrix.unitaryGroup (Fin 2) ℂ)
    (f : TGLExt.ImportedSQ.H1) :
    matrixMultiplier A hA hu f=ᵐ[orbitalMeasure 0] fun p => matrixFiberOperator (A p) (f p) := by
  have h := (ContinuousLinearMap.id ℂ FiberOperator).coeFn_holder (r:=2) (matrixWeight A hA hu) f
  filter_upwards [h,matrixWeight_ae A hA hu] with p hp hwp
  simpa only [matrixMultiplier,ContinuousLinearMap.holderL_apply_apply,
    ContinuousLinearMap.id_apply,hwp,Function.comp_apply] using hp

theorem matrixMultiplier_norm (A : MomentumCoordinates → Matrix (Fin 2) (Fin 2) ℂ)
    (hA : Measurable A) (hu : ∀ᵐ p ∂orbitalMeasure 0, A p ∈ Matrix.unitaryGroup (Fin 2) ℂ)
    (f : TGLExt.ImportedSQ.H1) : ‖matrixMultiplier A hA hu f‖=‖f‖ := by
  apply le_antisymm
  · apply Lp.norm_le_norm_of_ae_le
    filter_upwards [matrixMultiplier_ae A hA hu f,hu] with p hp hup
    rw [hp,matrixFiberOperator_norm (A p) hup]
  · apply Lp.norm_le_norm_of_ae_le
    filter_upwards [matrixMultiplier_ae A hA hu f,hu] with p hp hup
    rw [hp,matrixFiberOperator_norm (A p) hup]

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.matrixFiberOperator_norm
#print axioms F1Fecho.OrbitalScreen.matrixMultiplier_ae
#print axioms F1Fecho.OrbitalScreen.matrixMultiplier_norm
