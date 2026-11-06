import TGLExt.F1Fecho394.MaxwellFourierBalanceR2
import TGLExt.F1Fecho394.FourierLpPostcompR1
import TGLExt.F1Fecho394.GeometricFiberConjugation
import Mathlib.MeasureTheory.SpecificCodomains.WithLp

/-! The scalar component contour result is assembled into the actual two-screen
Hilbert fiber. L1 is proved componentwise, not added as a physical hypothesis. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Complex
open scoped FourierTransform
namespace F1Fecho.MaxwellStrip
open F1Fecho.MaxwellGlobal F1Fecho.WedgeLaplace
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016 F1Rede.FiberConjugation

def regularizedVector (b : ℝ) (q : Fin 2 → ℝ) (f : SchwartzTensor) (r : ℝ) : Fib :=
  WithLp.toLp 2 (fun j => regularizedMaxwell b q f j r)

theorem regularizedVector_real (b : ℝ) (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (f : SchwartzTensor) : regularizedVector b y.1 f y.2=
      lowerGaussian b y.2 • globalCoefficient (physicalFourierCLM f) (rapidityChart 0 y) := by
  apply PiLp.ext
  intro j
  exact regularizedMaxwell_real b y hy f j

theorem regularizedVector_integrable (b : ℝ) (hb : 0 < b)
    (q : Fin 2 → ℝ) (f : SchwartzTensor) (hf : supportedTensorRight f) :
    Integrable (regularizedVector b q f) := by
  apply integrable_piLp_iff.mpr
  intro j
  exact regularizedMaxwell_integrable b hb q f hf j

theorem regularizedVector_fourier_component (b : ℝ) (hb : 0 < b)
    (q : Fin 2 → ℝ) (f : SchwartzTensor) (hf : supportedTensorRight f)
    (j : Fin 2) (p : ℝ) :
    (𝓕 (regularizedVector b q f) p) j=𝓕 (regularizedMaxwell b q f j) p := by
  exact (FourierNaturality.fourier_integral_postcomp
    (PiLp.proj 2 (fun _ : Fin 2 => ℂ) j : Fib →L[ℂ] ℂ)
    (regularizedVector b q f) (regularizedVector_integrable b hb q f hf) p).symm

theorem maxwell_vector_fourier_balance (b : ℝ) (hb : 0 < b) (q : Fin 2 → ℝ)
    (hq : q ≠ 0) (f : SchwartzTensor) (hf : supportedTensorRight f)
    (hr : IsRealTest f) (p : ℝ) :
    (Real.exp (2*Real.pi^2*p):ℂ) • 𝓕 (regularizedVector b q f) p=
      fiberJ (𝓕 (regularizedVector b (-q) f) (-p)) := by
  apply PiLp.ext
  intro j
  change (Real.exp (2*Real.pi^2*p):ℂ)*(𝓕 (regularizedVector b q f) p) j=
    star ((𝓕 (regularizedVector b (-q) f) (-p)) j)
  rw [regularizedVector_fourier_component b hb q f hf,
    regularizedVector_fourier_component b hb (-q) f hf]
  exact maxwell_fourier_balance b hb q hq f hf hr j p

end F1Fecho.MaxwellStrip
#print axioms F1Fecho.MaxwellStrip.regularizedVector_real
#print axioms F1Fecho.MaxwellStrip.regularizedVector_integrable
#print axioms F1Fecho.MaxwellStrip.maxwell_vector_fourier_balance
