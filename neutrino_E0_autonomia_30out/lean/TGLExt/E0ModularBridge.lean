import Mathlib

namespace TGLExt.E0ModularBridge

/-- A point is stationary when the real-valued flow vanishes there. -/
def IsStationary {Point : Type*} (flow : Point → ℝ) (point : Point) : Prop :=
  flow point = 0

/-- Conditional inputs for the modular E0 bridge. -/
structure Inputs where
  Point : Type
  tail : ℝ
  magnitude : ℝ
  flow : Point → ℝ
  stationaryPoint : Point
  stationary : IsStationary flow stationaryPoint
  density : Point → ℝ
  readout : ℝ → ℝ
  E0 : ℝ
  E0_eq_magnitude_tail : E0 = magnitude * tail
  density_condenses_at_stationary :
    readout (density stationaryPoint) = magnitude * tail

/-- The modular density is defined directly by the stationary readout. -/
def rhoModular (inputs : Inputs) : ℝ :=
  inputs.readout (inputs.density inputs.stationaryPoint)

/-- The conditional bridge follows by transitivity through magnitude × tail. -/
theorem E0_eq_rhoModular (inputs : Inputs) : inputs.E0 = rhoModular inputs := by
  calc
    inputs.E0 = inputs.magnitude * inputs.tail := inputs.E0_eq_magnitude_tail
    _ = rhoModular inputs := inputs.density_condenses_at_stationary.symm

/-- A separate certificate evaluating the stationary readout at a real target. -/
structure ScaleEvaluation (inputs : Inputs) (target : ℝ) where
  readout_eq_target : inputs.readout (inputs.density inputs.stationaryPoint) = target

/-- No numeric scale is obtained without a separate scale evaluation. -/
theorem E0_eq_target_of_scaleEvaluation (inputs : Inputs) (target : ℝ)
    (evaluation : ScaleEvaluation inputs target) : inputs.E0 = target := by
  calc
    inputs.E0 = rhoModular inputs := E0_eq_rhoModular inputs
    _ = inputs.readout (inputs.density inputs.stationaryPoint) := rfl
    _ = target := evaluation.readout_eq_target

end TGLExt.E0ModularBridge
