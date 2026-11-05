import TGLExt.F1Fecho394.RegularRightActionR2
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.RegularRightAction
open TGLV350.Regular MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem ambient_ae (t : ℝ) (f : RegularHilbert (RegularHilbert H)) :
    ambient t f =ᵐ[volume] fun s => characterPhase t s • shift t (f s) := by
  filter_upwards [characterMultiplier_ae t (fibre (shift t) f),fibre_ae (shift t) f]
    with s h1 h2
  change characterMultiplier t (fibre (shift t) f) s = _
  exact h1.trans (congrArg (fun v => characterPhase t s • v) h2)

theorem phase_symmetric (s t : ℝ) : characterPhase s t=characterPhase t s := by
  unfold characterPhase
  congr 1
  ring

theorem ambient_orbit_pointwise (t s : ℝ) (c : ℝ) (x y : RegularHilbert H)
    (h : y = characterPhase s t • shift t x) :
    characterPhase t s • shift t (c • x) = c • y := by
  rw [h,phase_symmetric s t,(shift t).map_smul_of_tower c x,smul_comm]
end F1Fecho.RegularRightAction
#print axioms F1Fecho.RegularRightAction.ambient_ae
#print axioms F1Fecho.RegularRightAction.ambient_orbit_pointwise
