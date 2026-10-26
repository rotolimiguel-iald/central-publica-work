import ProfileWaveBoostR2
import CoherentPointMaxwellR1

/-! Lowered and real coherent Maxwell tensors under the canonical boost.
Both indices and the inverse spacetime action are transported explicitly. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix TGLExt TGLExt.ImportedSQ F1Fecho.CovariantTensor
open F1Fecho.SpacetimeLorentz

def complexMetric : Matrix (Fin 4) (Fin 4) ℂ := Matrix.diagonal metricSignC
def complexBoost (s : ℝ) : Matrix (Fin 4) (Fin 4) ℂ := (boostMat s).map Complex.ofReal

theorem complexBoost_transpose (s : ℝ) : (complexBoost s).transpose=complexBoost s := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [complexBoost,boostMat,Matrix.transpose_apply]

theorem complexMetric_boost (s : ℝ) :
    complexMetric*complexBoost s=complexBoost (-s)*complexMetric := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [complexMetric,complexBoost,boostMat,metricSignC,Matrix.mul_apply,
      Fin.sum_univ_four,Matrix.diagonal_apply,Real.cosh_neg,Real.sinh_neg]

theorem boost_complexMetric (s : ℝ) :
    complexBoost s*complexMetric=complexMetric*complexBoost (-s) := by
  simpa only [neg_neg] using (complexMetric_boost (-s)).symm

theorem lowerProfileWave_as_matrix (h : H1) (x : Spacetime) :
    Matrix.of (fun μ ν=>lowerProfileWave h μ ν x)=
      complexMetric*Matrix.of (fun μ ν=>profileWave h μ ν x)*complexMetric := by
  ext μ ν
  simp [complexMetric,lowerProfileWave,Matrix.mul_apply,Matrix.diagonal_apply,mul_comm,mul_left_comm,mul_assoc]

theorem lowerProfileWave_boost (s : ℝ) (h : H1) (hh : RegularProfile h) (x : Spacetime) :
    (fun μ ν=>lowerProfileWave (B0 s h) μ ν x)=
      pull (complexBoost (-s))
        (fun μ ν=>lowerProfileWave h μ ν ((action (theBoost s)).symm x)) := by
  have hu:=profileWave_boost s h hh x
  change Matrix.of (fun μ ν=>profileWave (B0 s h) μ ν x)=
    complexBoost s*Matrix.of (fun μ ν=>profileWave h μ ν ((action (theBoost s)).symm x))*
      (complexBoost s).transpose at hu
  change Matrix.of (fun μ ν=>lowerProfileWave (B0 s h) μ ν x)=
    (complexBoost (-s)).transpose*
      Matrix.of (fun μ ν=>lowerProfileWave h μ ν ((action (theBoost s)).symm x))*
      complexBoost (-s)
  rw [lowerProfileWave_as_matrix,lowerProfileWave_as_matrix,hu,
    complexBoost_transpose,complexBoost_transpose]
  calc
    _ = (complexMetric*complexBoost s)*
        Matrix.of (fun μ ν=>profileWave h μ ν ((action (theBoost s)).symm x))*
        (complexBoost s*complexMetric) := by noncomm_ring
    _ = _ := by rw [complexMetric_boost s,boost_complexMetric s]; noncomm_ring

theorem pull_real_conjugate (A : Matrix (Fin 4) (Fin 4) ℝ) (T : TensorValue) :
    (fun μ ν=>(starRingEnd ℂ) (pull (A.map Complex.ofReal) T μ ν))=
      pull (A.map Complex.ofReal) (fun μ ν=>(starRingEnd ℂ) (T μ ν)) := by
  ext μ ν
  simp [pull,pullLinear,Matrix.mul_apply,Matrix.transpose_apply,map_sum]

theorem coherentProfileWave_boost (s : ℝ) (h k : H1)
    (hh : RegularProfile h) (hk : RegularProfile k) (x : Spacetime) :
    (fun μ ν=>coherentProfileWave (B0 s h) (B0 s k) μ ν x)=
      pull (complexBoost (-s))
        (fun μ ν=>coherentProfileWave h k μ ν ((action (theBoost s)).symm x)) := by
  change (Real.sqrt 2:ℂ)⁻¹ •
      ((fun μ ν=>(starRingEnd ℂ) (lowerProfileWave (B0 s h) μ ν x))+
        (fun μ ν=>lowerProfileWave (B0 s k) μ ν x)) =
    pull (complexBoost (-s)) ((Real.sqrt 2:ℂ)⁻¹ •
      ((fun μ ν=>(starRingEnd ℂ) (lowerProfileWave h μ ν ((action (theBoost s)).symm x)))+
        (fun μ ν=>lowerProfileWave k μ ν ((action (theBoost s)).symm x))))
  rw [map_smul,map_add]
  congr 1
  rw [lowerProfileWave_boost s k hk]
  congr 1
  have hh' := lowerProfileWave_boost s h hh x
  have hh'' (μ ν : Fin 4) := congrFun (congrFun hh' μ) ν
  simp_rw [hh'']
  simpa only [complexBoost] using
    pull_real_conjugate (boostMat (-s))
      (fun μ ν=>lowerProfileWave h μ ν ((action (theBoost s)).symm x))

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_boost
#print axioms F1Fecho.MaxwellGlobal.coherentProfileWave_boost
