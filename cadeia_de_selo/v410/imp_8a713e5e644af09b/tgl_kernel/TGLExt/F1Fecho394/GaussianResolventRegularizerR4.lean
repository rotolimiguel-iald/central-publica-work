import TGLExt.F1Fecho394.GaussianResolventSymbolR2
import TGLExt.F1Fecho394.GaussianProbabilityKernelR4
import TGLExt.F1Fecho394.ResolventScaledPhaseIntegralR1
import TGLExt.F1Fecho394.StrongUnitaryAverageR1
import TGLExt.F1Fecho394.FibreRootGraphR3

/-! Concrete Gaussian averaging of the resolvent modular group, including
its range in the positive root domain. The GNS graph is not an input here. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory
namespace F1Fecho.GaussianResolventRegularizer
open TGLV350.Regular F1Fecho.GaussianLogScalar
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : Module ℝ (H→L[ℂ]H) := Module.restrictScalars ℝ ℂ _

def spectral (R:H→L[ℂ]H) (b:ℝ) : H→L[ℂ]H := cfc (gaussianSymbol b) R

theorem spectral_factor (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1) (b:ℝ) (hb:0<b) :
    spectral R b=R*cfc (gaussianRangeFactor b) R := by
  have hs:=IsSelfAdjoint.of_nonneg hR
  change cfc (gaussianSymbol b) R=_
  have he:cfc (gaussianSymbol b) R=cfc (fun x:ℝ=>x*gaussianRangeFactor b x) R := by
    apply cfc_congr
    intro x hx
    exact gaussianSymbol_factors b x (positive_contraction_spectrum_bounds R hR h1 hx)
  rw [he,cfc_mul (fun x:ℝ=>x) (gaussianRangeFactor b) R (by fun_prop) (gaussianRangeFactor_continuous b hb).continuousOn,
    cfc_id' ℝ R hs]

theorem spectral_root_domain (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (hi:Function.Injective R) (b:ℝ) (hb:0<b) (x:H) :
    ∃y,(spectral R b x,y)∈(resolventSquareRoot R hR hi).graph := by
  rw [spectral_factor R hR h1 b hb]
  exact ⟨_,FibreRootGraph.root_regularized_graph R hR h1 hi (cfc (gaussianRangeFactor b) R x)⟩

theorem gaussian_phase_integral (c x:ℝ) :
    (∫t:ℝ,(gaussianWeight t:ℂ)*resolventPhaseFunction (c*t) x)=
      (resolventDamping x:ℂ)*(gaussianSymbol (c^2/4) x:ℂ) := by
  by_cases hx:x=0 ∨ x=1
  · rcases hx with rfl|rfl <;> simp [resolventPhaseFunction,resolventDamping]
  · have he: (fun t:ℝ=>(gaussianWeight t:ℂ)*resolventPhaseFunction (c*t) x)=
      (fun t:ℝ=>(resolventDamping x:ℂ)*((gaussianWeight t:ℂ)*
        ChatgptAudit.modularPhase (c*t) (logCoordinate x))) := by
      funext t
      unfold resolventPhaseFunction logCoordinate
      ring
    rw [he,integral_const_mul,gaussianWeight_fourier]
    simp only [gaussianSymbol,compactify,if_neg hx]
    congr 2
    ring

end F1Fecho.GaussianResolventRegularizer
#print axioms F1Fecho.GaussianResolventRegularizer.spectral_factor
#print axioms F1Fecho.GaussianResolventRegularizer.spectral_root_domain
#print axioms F1Fecho.GaussianResolventRegularizer.gaussian_phase_integral
