import LowerMaxwellWaveBoostR2
import MaxwellStressTensorCovarianceR2
import CoherentPointStressR2

/-! The actual coherent stress transforms by the inverse boost on both
lower indices. No stress-covariance field is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix TGLExt TGLExt.ImportedSQ F1Fecho.CovariantTensor F1Fecho.MaxwellStress
open F1Fecho.SpacetimeLorentz

theorem complexMetric_eq_map : complexMetric=eta4.map Complex.ofReal := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [complexMetric,eta4,metricSignC,Matrix.diagonal_apply]

theorem complexBoost_metric (s : ℝ) :
    (complexBoost s).transpose*complexMetric*complexBoost s=complexMetric := by
  have h:=congrArg (Complex.ofRealHom.mapMatrix (m:=Fin 4)) (boostMat_isLorentz s)
  change (Complex.ofRealHom.mapMatrix (m:=Fin 4))
    ((boostMat s).transpose*eta4*boostMat s)=
    (Complex.ofRealHom.mapMatrix (m:=Fin 4)) eta4 at h
  simpa only [map_mul,RingHom.mapMatrix_apply,←Matrix.transpose_map,
    complexBoost,complexMetric_eq_map] using h

theorem complexBoost_metric_other (s : ℝ) :
    complexBoost s*complexMetric*(complexBoost s).transpose=complexMetric := by
  simpa only [complexBoost_transpose] using complexBoost_metric s

theorem stress_pull_boost (s : ℝ) (T : TensorValue) :
    (fun μ ν=>stress metricSignC (pull (complexBoost s) T) μ ν)=
      pull (complexBoost s) (fun μ ν=>stress metricSignC T μ ν) := by
  change Matrix.of (stress metricSignC (pull (complexBoost s) T))=
      (complexBoost s).transpose*Matrix.of (stress metricSignC T)*complexBoost s
  rw [stress_as_matrix,stress_as_matrix]
  exact stressMatrix_covariant complexMetric (complexBoost s) (Matrix.of T)
    (complexBoost_metric_other s) (complexBoost_metric s)

theorem coherentProfileStress_boost (s : ℝ) (h k : H1)
    (hh : RegularProfile h) (hk : RegularProfile k) (x : Spacetime) :
    (fun μ ν=>coherentProfileStress (B0 s h) (B0 s k) μ ν x)=
      pull (complexBoost (-s))
        (fun μ ν=>coherentProfileStress h k μ ν ((action (theBoost s)).symm x)) := by
  change Complex.exp (inner ℂ (B0 s h) (B0 s k)) •
      (fun μ ν=>stress metricSignC (fun α β=>coherentProfileWave (B0 s h) (B0 s k) α β x) μ ν)=
    pull (complexBoost (-s)) (Complex.exp (inner ℂ h k) •
      (fun μ ν=>stress metricSignC
        (fun α β=>coherentProfileWave h k α β ((action (theBoost s)).symm x)) μ ν))
  rw [LinearIsometryEquiv.inner_map_map,map_smul,coherentProfileWave_boost s h k hh hk,
    stress_pull_boost]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.complexBoost_metric
#print axioms F1Fecho.MaxwellGlobal.stress_pull_boost
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_boost
