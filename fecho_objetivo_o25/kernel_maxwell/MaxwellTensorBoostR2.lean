import MaxwellBoostContractionR1

/-! The same on-shell bivector transforms as an actual rank-two tensor under
the already constructed longitudinal boost, off a measured-null axis. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix MeasureTheory TGLExt F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen
open F1Fecho.MaxwellOnShell
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

theorem realStrength_mulVec (A : Matrix (Fin 4) (Fin 4) ℝ) (p e : Fin 4→ℝ) :
    Matrix.of (realStrength (A.mulVec p) (A.mulVec e))=
      A*Matrix.of (realStrength p e)*A.transpose := by
  have heq (v w : Fin 4 → ℝ) : Matrix.of (realStrength v w)=
      vecMulVec v w-vecMulVec w v := by
    ext μ ν
    simp [realStrength,Matrix.vecMulVec_apply,mul_comm]
  rw [heq,heq]
  rw [Matrix.mul_sub,Matrix.sub_mul]
  simp only [Matrix.mul_vecMulVec,Matrix.vecMulVec_mul,Matrix.vecMul_transpose]

theorem cartesianStrength_boost_ae (s : ℝ) :
    ∀ᵐp ∂orbitalMeasure 0,∀j : Fin 2,
      cartesianStrength (coordinateBoost 0 s p) j=
        (theBoost s).val*cartesianStrength p j*(theBoost s).val.transpose := by
  filter_upwards [regular_orbital_ae,shell_boost_ae s] with p hp hm
  intro j
  have hs : (theBoost s).val.mulVec (screen (inverseRapidityChart 0 p) j)=
      screen (inverseRapidityChart 0 (coordinateBoost 0 s p)) j := by
    rw [inverseChart_coordinateBoost s p hp]
    exact screen_boost s (inverseRapidityChart 0 p) j
  have hq : (coordinateBoost 0 s p).1≠0 := hp
  have h1 : cartesianStrength p j=Matrix.of
      (realStrength (shellMomentum 0 p) (screen (inverseRapidityChart 0 p) j)) := by
    ext μ ν
    exact cartesianStrength_inverse_chart p hp j μ ν
  have h2 : cartesianStrength (coordinateBoost 0 s p) j=Matrix.of
      (realStrength (shellMomentum 0 (coordinateBoost 0 s p))
        (screen (inverseRapidityChart 0 (coordinateBoost 0 s p)) j)) := by
    ext μ ν
    exact cartesianStrength_inverse_chart _ hq j μ ν
  rw [h1,h2,hm,←hs]
  exact realStrength_mulVec _ _ _

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.realStrength_mulVec
#print axioms F1Fecho.MaxwellGlobal.cartesianStrength_boost_ae
