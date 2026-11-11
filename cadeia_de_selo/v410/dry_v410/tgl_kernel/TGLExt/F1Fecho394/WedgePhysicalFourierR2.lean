import TGLExt.F1Fecho394.WedgeLaplaceAnalyticR3
import TGLExt.F1Fecho394.WedgeLaplaceBoundaryR3

/-! The real boundary of the constructed strip integral is the actual
positive-angular inverse Fourier transform, not an unrelated analytic model. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Matrix
open scoped FourierTransform RealInnerProductSpace
namespace F1Fecho.WedgeLaplace
open F1Fecho.MaxwellGlobal F1Fecho.PhysicalFourier SchwartzMap
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

def rapidityMomentum (m q₂ q₃ r : ℝ) : Spacetime :=
  WithLp.toLp 2 ![m*Real.cosh r,m*Real.sinh r,q₂,q₃]

theorem kernel_real_pairing (m q₂ q₃ r : ℝ) (x : Spacetime) :
    kernel m (x 0) (x 1) (q₂*x 2+q₃*x 3) r =
      phase (orbitPairing (fun i => x i) (fun i => rapidityMomentum m q₂ q₃ r i)) := by
  rw [kernel,longitudinal_real]
  unfold phase orbitPairing rapidityMomentum
  congr 1
  simp only [WithLp.toLp_ofLp,Matrix.cons_val_zero,Matrix.cons_val_one,
    Matrix.cons_val,Matrix.head_cons,Matrix.head_fin_const]
  push_cast
  ring

theorem scalarLaplace_real_fourier (m q₂ q₃ r : ℝ) (f : 𝓢(Spacetime,ℂ)) :
    scalarLaplace m q₂ q₃ f r =
      (𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip (rapidityMomentum m q₂ q₃ r)) := by
  rw [SchwartzMap.fourierInv_coe,Real.fourierInv_eq']
  apply integral_congr_ae
  apply ae_of_all
  intro x
  dsimp only
  rw [angular_pairing]
  change integrand m q₂ q₃ f r x =
    phase (orbitPairing (fun i => x i) (fun i => rapidityMomentum m q₂ q₃ r i)) * f x
  exact congrArg (fun z : ℂ => z*f x) (kernel_real_pairing m q₂ q₃ r x)

theorem rapidityMomentum_eq_shell (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    rapidityMomentum (transverseMass 0 y.1) (y.1 0) (y.1 1) y.2 =
      shellEmbedding (rapidityChart 0 y) := by
  unfold shellEmbedding
  rw [shellMomentum_chart 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)]
  rfl

theorem scalarLaplace_real_shell (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (f : 𝓢(Spacetime,ℂ)) :
    scalarLaplace (transverseMass 0 y.1) (y.1 0) (y.1 1) f y.2 =
      (𝓕⁻ f) ((2*Real.pi)⁻¹ • metricFlip (shellEmbedding (rapidityChart 0 y))) := by
  rw [scalarLaplace_real_fourier,rapidityMomentum_eq_shell y hy]

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.kernel_real_pairing
#print axioms F1Fecho.WedgeLaplace.scalarLaplace_real_fourier
#print axioms F1Fecho.WedgeLaplace.rapidityMomentum_eq_shell
#print axioms F1Fecho.WedgeLaplace.scalarLaplace_real_shell
