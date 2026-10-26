import CartesianMaxwellBivectorR6

/-! The global Cartesian representative is the same O16 p-wedge-screen
bivector on the regular chart. Its axis convention changes only a null set. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix MeasureTheory
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016
open F1Fecho.MaxwellOnShell

theorem cartesianStrength_chart (y : MomentumCoordinates) (hy : y.1≠0)
    (j : Fin 2) (μ ν : Fin 4) :
    cartesianStrength (rapidityChart 0 y) j μ ν=
      realStrength (shellMomentum 0 (rapidityChart 0 y)) (screen y j) μ ν := by
  have hr:=transverseMass_pos_of_ne_zero 0 y.1 hy
  have hc:=Real.cosh_sq_sub_sinh_sq y.2
  have he : shellEnergy (rapidityChart 0 y)=transverseMass 0 y.1*Real.cosh y.2 :=
    energy_longitudinal _ hr _
  rw [shellMomentum_chart 0 y hr]
  fin_cases j <;> fin_cases μ <;> fin_cases ν <;>
    simp [cartesianStrength,Matrix.cons_val_zero',Matrix.cons_val_succ',transverseRatio,he,rapidityChart,longitudinal,
      realStrength,screen,screenOne,screenTwo] <;>
    field_simp [hr.ne'] <;> nlinarith [hc]

theorem cartesianStrength_inverse_chart (y : MomentumCoordinates) (hy : y.1≠0)
    (j : Fin 2) (μ ν : Fin 4) :
    cartesianStrength y j μ ν=
      realStrength (shellMomentum 0 y) (screen (inverseRapidityChart 0 y) j) μ ν := by
  have hreg : (inverseRapidityChart 0 y).1≠0 := hy
  have h := cartesianStrength_chart (inverseRapidityChart 0 y) hreg j μ ν
  rw [chart_inverse_of_positive 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)] at h
  exact h

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.cartesianStrength_chart
#print axioms F1Fecho.MaxwellGlobal.cartesianStrength_inverse_chart
