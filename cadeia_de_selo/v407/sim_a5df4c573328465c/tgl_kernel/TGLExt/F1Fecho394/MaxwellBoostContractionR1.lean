import TGLExt.F1Fecho394.CovariantTensorPullbackR3
import TGLExt.F1Fecho394.CartesianMaxwellChartR3
import TGLExt.F1Fecho394.ScreenPoincareCovarianceR2

/-! The global Cartesian Maxwell bivector and the real O16 screens give the
same boosted tensor contraction off the null axis. This is a coefficient
identity, including the covariant tensor indices and the inverse boost. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Matrix
namespace F1Fecho.MaxwellBoostContraction
open TGLExt F1Fecho.MaxwellGlobal F1Fecho.MaxwellOnShell
open F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen F1Fecho.CovariantTensor
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

theorem realLift_mulVec (A:Matrix (Fin 4) (Fin 4) ℝ) (p:Fin 4→ℝ) :
    (A.map Complex.ofReal).mulVec (realLift p)=realLift (A.mulVec p) := by
  funext μ
  simp [Matrix.mulVec,dotProduct,realLift,Complex.ofReal_sum,Complex.ofReal_mul]

theorem contraction_transport (A:Matrix (Fin 4) (Fin 4) ℝ)
    (p q:MomentumCoordinates) (hp:p.1≠0) (hq:q.1≠0) (j:Fin 2)
    (hm:A.mulVec (shellMomentum 0 p)=shellMomentum 0 q)
    (hs:A.mulVec (screen (inverseRapidityChart 0 p) j)=screen (inverseRapidityChart 0 q) j)
    (T:TensorValue) :
    (∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*pull (A.map Complex.ofReal) T μ ν)=
      ∑μ,∑ν,(cartesianStrength q j μ ν:ℂ)*T μ ν := by
  simp_rw [cartesianStrength_inverse_chart p hp,cartesianStrength_inverse_chart q hq]
  rw [←real_contraction_eq_sum,contraction_pull,realLift_mulVec,realLift_mulVec,hm,hs,
    real_contraction_eq_sum]

theorem boost_contraction_ae (s:ℝ) :
    ∀ᵐ p ∂orbitalMeasure 0,∀j:Fin 2,∀T:TensorValue,
      (∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*
        pull ((theBoost s)⁻¹.val.map Complex.ofReal) T μ ν)=
      ∑μ,∑ν,(cartesianStrength (coordinateBoost 0 (-s) p) j μ ν:ℂ)*T μ ν := by
  filter_upwards [regular_orbital_ae,shell_boost_ae (-s)] with p hp hm
  intro j T
  rw [theBoost_inv_eq]
  apply contraction_transport (theBoost (-s)).val p (coordinateBoost 0 (-s) p) hp hp j hm.symm
  rw [inverseChart_coordinateBoost (-s) p hp]
  exact screen_boost (-s) (inverseRapidityChart 0 p) j

end F1Fecho.MaxwellBoostContraction
#print axioms F1Fecho.MaxwellBoostContraction.realLift_mulVec
#print axioms F1Fecho.MaxwellBoostContraction.contraction_transport
#print axioms F1Fecho.MaxwellBoostContraction.boost_contraction_ae
