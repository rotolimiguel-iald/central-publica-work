import TGLExt.F1Fecho394.ScreenPoincareCovarianceR2

/-! The fixed unitary change from helicity coordinates to the real transverse
screen basis, lifted to the unchanged canonical H1. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix Complex
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

def circularMatrix : Matrix (Fin 2) (Fin 2) ℂ :=
  ((Real.sqrt 2 : ℂ)⁻¹) • !![1,1;I,-I]

theorem circularMatrix_unitary : circularMatrix ∈ Matrix.unitaryGroup (Fin 2) ℂ := by
  have hr : Real.sqrt 2 ≠ 0 := (Real.sqrt_pos.2 (by norm_num : (0:ℝ)<2)).ne'
  have hrc : (Real.sqrt 2 : ℂ) ≠ 0 := by exact_mod_cast hr
  have hs : (Real.sqrt 2 : ℂ)^2=2 := by exact_mod_cast Real.sq_sqrt (by norm_num : (0:ℝ)≤2)
  apply Matrix.mem_unitaryGroup_iff'.mpr
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [circularMatrix,Matrix.mul_apply,Matrix.star_apply,Fin.sum_univ_two,
      Matrix.one_apply,Complex.star_def] <;>
    field_simp <;> ring_nf <;> simp [Complex.I_sq,hs] <;> norm_num

def circularFiber : Fiber ≃ₗᵢ[ℂ] Fiber :=
  Unitary.linearIsometryEquiv
    ⟨matrixFiberOperator circularMatrix,
      Unitary.map_mem (Matrix.toEuclideanCLM (𝕜:=ℂ) (n:=Fin 2)) circularMatrix_unitary⟩

def fiberLiftMap (e : Fiber ≃ₗᵢ[ℂ] Fiber) : H1 →L[ℂ] H1 :=
  e.toLinearIsometry.toContinuousLinearMap.compLpL 2 (orbitalMeasure 0)

theorem fiberLiftMap_ae (e : Fiber ≃ₗᵢ[ℂ] Fiber) (f : H1) :
    fiberLiftMap e f=ᵐ[orbitalMeasure 0] fun p => e (f p) :=
  e.toLinearIsometry.toContinuousLinearMap.coeFn_compLpL f

theorem fiberLiftMap_norm (e : Fiber ≃ₗᵢ[ℂ] Fiber) (f : H1) : ‖fiberLiftMap e f‖=‖f‖ := by
  apply le_antisymm
  · apply Lp.norm_le_norm_of_ae_le
    filter_upwards [fiberLiftMap_ae e f] with p hp
    rw [hp,e.norm_map]
  · apply Lp.norm_le_norm_of_ae_le
    filter_upwards [fiberLiftMap_ae e f] with p hp
    rw [hp,e.norm_map]

theorem fiberLiftMap_inverse (e : Fiber ≃ₗᵢ[ℂ] Fiber) (f : H1) :
    fiberLiftMap e (fiberLiftMap e.symm f)=f := by
  apply Lp.ext
  filter_upwards [fiberLiftMap_ae e (fiberLiftMap e.symm f),fiberLiftMap_ae e.symm f] with p hp hq
  rw [hp,hq,e.apply_symm_apply]

def fiberLiftIsometry (e : Fiber ≃ₗᵢ[ℂ] Fiber) : H1 →ₗᵢ[ℂ] H1 where
  toLinearMap := (fiberLiftMap e).toLinearMap
  norm_map' := fiberLiftMap_norm e

def fiberLift (e : Fiber ≃ₗᵢ[ℂ] Fiber) : H1 ≃ₗᵢ[ℂ] H1 :=
  LinearIsometryEquiv.ofLinearIsometry (fiberLiftIsometry e) (fiberLiftMap e.symm).toLinearMap
    (by apply LinearMap.ext; intro f; exact fiberLiftMap_inverse e f)
    (by
      apply LinearMap.ext
      intro f
      change fiberLiftMap e.symm (fiberLiftMap e f)=f
      simpa only [LinearIsometryEquiv.symm_symm] using fiberLiftMap_inverse e.symm f)

def circularH1 : H1 ≃ₗᵢ[ℂ] H1 := fiberLift circularFiber

theorem fiberLift_U1 (e : Fiber ≃ₗᵢ[ℂ] Fiber) (a : Fin 4 → ℝ) (f : H1) :
    fiberLift e (U1 a f)=U1 a (fiberLift e f) := by
  change fiberLiftMap e (orbitalTranslation 0 a f)=orbitalTranslation 0 a (fiberLiftMap e f)
  apply Lp.ext
  filter_upwards [fiberLiftMap_ae e (orbitalTranslation 0 a f),orbitalTranslation_ae 0 a f,
    orbitalTranslation_ae 0 a (fiberLiftMap e f),fiberLiftMap_ae e f] with p hp hq hr hs
  rw [hp,hq,hr,hs,map_smul]

theorem fiberLift_B0 (e : Fiber ≃ₗᵢ[ℂ] Fiber) (s : ℝ) (f : H1) :
    fiberLift e (B0 s f)=B0 s (fiberLift e f) := by
  change fiberLiftMap e (orbitalScalarBoost 0 s f)=orbitalScalarBoost 0 s (fiberLiftMap e f)
  have he := (coordinateBoost_measurePreserving 0 (-s)).quasiMeasurePreserving.ae (fiberLiftMap_ae e f)
  apply Lp.ext
  filter_upwards [fiberLiftMap_ae e (orbitalScalarBoost 0 s f),orbitalScalarBoost_ae 0 s f,
    orbitalScalarBoost_ae 0 s (fiberLiftMap e f),he] with p hp hq hr hs
  rw [hp,hq,hr,hs]

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.circularMatrix_unitary
#print axioms F1Fecho.OrbitalScreen.fiberLift
#print axioms F1Fecho.OrbitalScreen.fiberLift_U1
#print axioms F1Fecho.OrbitalScreen.fiberLift_B0
