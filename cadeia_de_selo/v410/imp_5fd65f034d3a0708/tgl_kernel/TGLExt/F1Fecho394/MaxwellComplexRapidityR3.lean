import TGLExt.F1Fecho394.WedgeLaplaceBoundaryR3
import TGLExt.F1Fecho394.ScreenHalfTurnR3
import TGLExt.F1Fecho394.CartesianMaxwellChartR3
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

/-! Actual analytic continuation of the already constructed p-wedge-screen
bivector. At the lower endpoint both p and the screen reverse sign, leaving
the bivector at reflected transverse momentum. No localization is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix
namespace F1Fecho.MaxwellStrip
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016
open F1Fecho.MaxwellOnShell F1Fecho.MaxwellGlobal F1Rede.GeometricIdentification F1Rede.WedgeReflectionTranslations

def complexMomentum (q : Fin 2 → ℝ) (z : ℂ) : Fin 4 → ℂ :=
  ![(transverseMass 0 q:ℂ)*Complex.cosh z,
    (transverseMass 0 q:ℂ)*Complex.sinh z,(q 0:ℂ),(q 1:ℂ)]

def complexScreen (q : Fin 2 → ℝ) (j : Fin 2) (z : ℂ) : Fin 4 → ℂ :=
  ![![Complex.sinh z,Complex.cosh z,0,0],
    ![0,0,(-q 1/transverseMass 0 q:ℝ),(q 0/transverseMass 0 q:ℝ)]] j

def analyticStrength (q : Fin 2 → ℝ) (j : Fin 2) (μ ν : Fin 4) (z : ℂ) : ℂ :=
  strength (complexMomentum q z) (complexScreen q j z) μ ν

theorem complexMomentum_real (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    complexMomentum y.1 y.2=fun i => (shellMomentum 0 (rapidityChart 0 y) i:ℂ) := by
  rw [shellMomentum_chart 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)]
  funext i
  fin_cases i <;> simp [complexMomentum,Complex.ofReal_mul,Complex.ofReal_cosh,Complex.ofReal_sinh]

theorem complexScreen_real (y : MomentumCoordinates) (j : Fin 2) :
    complexScreen y.1 j y.2=fun i => (screen y j i:ℂ) := by
  funext i
  fin_cases j <;> fin_cases i <;>
    simp [complexScreen,screen,screenOne,screenTwo,Complex.ofReal_cosh,Complex.ofReal_sinh]

theorem analyticStrength_real (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (j : Fin 2) (μ ν : Fin 4) :
    analyticStrength y.1 j μ ν y.2=(cartesianStrength (rapidityChart 0 y) j μ ν:ℂ) := by
  rw [cartesianStrength_chart y hy,analyticStrength,complexMomentum_real y hy,complexScreen_real]
  simp only [strength,realStrength,Complex.ofReal_sub,Complex.ofReal_mul]

theorem complexMomentum_lower (q : Fin 2 → ℝ) (r : ℝ) :
    complexMomentum q ((r:ℂ)-Complex.I*Real.pi) = -complexMomentum (-q) r := by
  funext i
  fin_cases i <;> simp [complexMomentum,mul_comm Complex.I,
    Complex.cosh_sub_pi_mul_I,Complex.sinh_sub_pi_mul_I,transverseMass_neg]

theorem complexScreen_lower (q : Fin 2 → ℝ) (j : Fin 2) (r : ℝ) :
    complexScreen q j ((r:ℂ)-Complex.I*Real.pi) = -complexScreen (-q) j r := by
  funext i
  fin_cases j <;> fin_cases i <;> simp [complexScreen,mul_comm Complex.I,
    Complex.cosh_sub_pi_mul_I,Complex.sinh_sub_pi_mul_I,transverseMass_neg] <;> ring

theorem analyticStrength_lower (q : Fin 2 → ℝ) (j : Fin 2) (μ ν : Fin 4) (r : ℝ) :
    analyticStrength q j μ ν ((r:ℂ)-Complex.I*Real.pi)=analyticStrength (-q) j μ ν r := by
  rw [analyticStrength,complexMomentum_lower,complexScreen_lower]
  simp only [strength,Pi.neg_apply,neg_mul_neg,analyticStrength]

theorem analyticStrength_entire (q : Fin 2 → ℝ) (j : Fin 2) (μ ν : Fin 4) :
    Differentiable ℂ (analyticStrength q j μ ν) := by
  have hp (i : Fin 4) : Differentiable ℂ (fun z => complexMomentum q z i) := by
    fin_cases i <;> simp only [complexMomentum,Matrix.cons_val_zero',Matrix.cons_val_succ'] <;> fun_prop
  have hs (i : Fin 4) : Differentiable ℂ (fun z => complexScreen q j z i) := by
    fin_cases j <;> fin_cases i <;>
      simp only [complexScreen,Matrix.cons_val_zero',Matrix.cons_val_succ'] <;> fun_prop
  exact ((hp μ).mul (hs ν)).sub ((hp ν).mul (hs μ))


end F1Fecho.MaxwellStrip
#print axioms F1Fecho.MaxwellStrip.analyticStrength_real
#print axioms F1Fecho.MaxwellStrip.analyticStrength_lower
#print axioms F1Fecho.MaxwellStrip.analyticStrength_entire
