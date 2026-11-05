import TGLExt.F1Fecho394.CanonicalTensorResolventEquationR2
import TGLExt.F1Fecho394.TensorResolventScalarsR4
import TGLExt.F1Fecho394.ImaginaryPowerIntertwiningR2
import TGLExt.F1Fecho394.CanonicalFockModularFlowR2
/-! The actual Fock resolvent and modular flow in each non-vacuum sector.
All coordinates refer to the previously constructed Fock space. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.TensorCoordinates
open ChatgptAudit F1Rede.BosonicFock F1Rede.CanonicalWedge F1Fecho.CanonicalFockPolar TGLV350.Regular

theorem Q_resolvent (n:ℕ) (x:F) : Q n (modularR x)=tensorR rootParameter n (Q n x) := by
  apply Lp.ext
  filter_upwards [Q_resolvent_equation_ae n x,tensorR_ae rootParameter n (Q n x)] with p hp hr
  rw [hr]
  apply smul_right_injective (data n).Fiber (scalar_coefficient_nonzero rootParameter n p)
  dsimp only
  rw [smul_smul,scalar_resolvent_identity]
  exact hp

theorem Q_resolvent_intertwine (n:ℕ) :
    (Q n).comp modularR=(tensorR rootParameter n).comp (Q n) := by
  ext1 x
  exact Q_resolvent n x

lemma phase_eq_boost (n:ℕ) (t:ℝ) :
    ScalarL2Spectral.phase (data n).measure (sumEnergy rootParameter n)
      (sumEnergy_measurable rootParameter n) t=spectralBoost n (-(2*Real.pi*t)) := by
  apply ScalarL2.op_eq
  intro p
  change modularPhase t (sumEnergy rootParameter n p)=
    characterPhase (2*Real.pi*(-(2*Real.pi*t))) (rapiditySum n p)
  unfold modularPhase characterPhase sumEnergy rootParameter
  congr 1
  push_cast
  ring

theorem Q_modularFlow (n:ℕ) (t:ℝ) (x:F) :
    Q n (actualModularFlow t x)=spectralBoost n (-(2*Real.pi*t)) (Q n x) := by
  have h:=ContinuousIntertwining.imaginaryPower_intertwine modularR (tensorR rootParameter n)
    (Q n) (Q_resolvent_intertwine n) modularR_nonneg modularR_le_one
    modularR_injective modularR_complement_injective
    (ScalarL2Spectral.R_nonneg _ _ _) (ScalarL2Spectral.R_le_one _ _ _)
    (ScalarL2Spectral.R_injective _ _ _) (ScalarL2Spectral.complement_injective _ _ _) t x
  change Q n (actualModularFlow t x)=_ at h
  calc
    Q n (actualModularFlow t x) = _ := h
    _ = ScalarL2Spectral.phase (data n).measure (sumEnergy rootParameter n)
        (sumEnergy_measurable rootParameter n) t (Q n x) :=
      ScalarL2Spectral.imaginaryPower_eq_phase _ _ _ t (Q n x)
    _ = _ := congrArg (fun L:Space n→L[ℂ]Space n=>L (Q n x)) (phase_eq_boost n t)

theorem positive_component_modularFlow (n:ℕ) (t:ℝ) (x:F) :
    (actualModularFlow t x) (n+1)=
      (F1Rede.BosonicFock.gamma (TGLExt.ImportedSQ.B0 (-(2*Real.pi*t))) x) (n+1) := by
  apply Subtype.ext
  apply (coordinates n).injective
  change Q n (actualModularFlow t x)=
    coordinates n (F1Rede.BosonicSectors.gammaSector (TGLExt.ImportedSQ.B0 (-(2*Real.pi*t)))
      (n+1) (x (n+1)) : F1Rede.BosonicSectors.TensorHilbert (n+1))
  rw [Q_modularFlow,sector_boost]
  rfl

end F1Fecho.TensorCoordinates
#print axioms F1Fecho.TensorCoordinates.Q_resolvent
#print axioms F1Fecho.TensorCoordinates.Q_modularFlow

#print axioms F1Fecho.TensorCoordinates.positive_component_modularFlow
