import MaxwellShellGeometryR1
import MaxwellScreenIntertwinerR2

/-! Globally measurable Cartesian representatives of the same regular-chart
bivectors. At the exceptional transverse axis the representative is zero.
The entire bivector is bounded by the shell energy, despite the 1/rho screen. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix MeasureTheory
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016
open F1Fecho.MaxwellOnShell

def transverseRatio (y : MomentumCoordinates) (i : Fin 2) : ℝ := y.1 i/transverseMass 0 y.1

def cartesianStrength (y : MomentumCoordinates) (j : Fin 2) : Matrix (Fin 4) (Fin 4) ℝ :=
  let r:=transverseMass 0 y.1
  let a:=transverseRatio y 0
  let b:=transverseRatio y 1
  let l:=y.2
  let e:=shellEnergy y
  ![!![0,r,-a*l,-b*l; -r,0,-a*e,-b*e; a*l,a*e,0,0; b*l,b*e,0,0],
    !![0,0,-b*e,a*e; 0,0,-b*l,a*l; b*e,b*l,0,r; -a*e,-a*l,-r,0]] j

theorem transverse_abs_le (y : MomentumCoordinates) (i : Fin 2) :
    |y.1 i|≤transverseMass 0 y.1 := by
  have hs:=transverseMass_sq 0 y.1
  have hn : 0≤transverseMass 0 y.1 := Real.sqrt_nonneg _
  fin_cases i <;> rw [abs_le] <;> constructor <;> nlinarith [sq_nonneg (y.1 0),sq_nonneg (y.1 1)]

theorem transverseRatio_bound (y : MomentumCoordinates) (i : Fin 2) : |transverseRatio y i|≤1 := by
  unfold transverseRatio
  rw [abs_div,abs_of_nonneg (Real.sqrt_nonneg _)]
  by_cases hr : transverseMass 0 y.1=0
  · simp [hr]
  · exact (div_le_one (lt_of_le_of_ne (Real.sqrt_nonneg _) (Ne.symm hr))).mpr (transverse_abs_le y i)

theorem transverse_le_energy (y : MomentumCoordinates) : transverseMass 0 y.1≤shellEnergy y := by
  have ht:=transverseMass_sq 0 y.1
  have hs:=shellEnergy_sq y
  have hn:=shellEnergy_nonneg y
  have hr : 0≤transverseMass 0 y.1 := Real.sqrt_nonneg _
  nlinarith [sq_nonneg y.2]

theorem ratio_mul_energy_bound (y : MomentumCoordinates) (i : Fin 2) :
    |transverseRatio y i*shellEnergy y|≤shellEnergy y := by
  rw [abs_mul,abs_of_nonneg (shellEnergy_nonneg y)]
  simpa using mul_le_mul_of_nonneg_right (transverseRatio_bound y i) (shellEnergy_nonneg y)

theorem ratio_mul_longitudinal_bound (y : MomentumCoordinates) (i : Fin 2) :
    |transverseRatio y i*y.2|≤shellEnergy y := by
  rw [abs_mul]
  exact (by simpa using mul_le_mul_of_nonneg_right (transverseRatio_bound y i) (abs_nonneg y.2)).trans
    (abs_spatial_le_energy y).2.2

theorem cartesianStrength_bound (y : MomentumCoordinates) (j : Fin 2) (μ ν : Fin 4) :
    |cartesianStrength y j μ ν|≤shellEnergy y := by
  have hz:=shellEnergy_nonneg y
  have hr : |transverseMass 0 y.1|≤shellEnergy y := by
    rw [abs_of_nonneg (Real.sqrt_nonneg _)]; exact transverse_le_energy y
  have ha:=ratio_mul_energy_bound y 0
  have hb:=ratio_mul_energy_bound y 1
  have hc:=ratio_mul_longitudinal_bound y 0
  have hd:=ratio_mul_longitudinal_bound y 1
  fin_cases j <;> fin_cases μ <;> fin_cases ν <;>
    simpa [cartesianStrength,neg_mul,abs_neg] using (by first | exact hz | exact hr | exact ha | exact hb | exact hc | exact hd)

theorem cartesianStrength_measurable (j : Fin 2) (μ ν : Fin 4) :
    Measurable (fun y => cartesianStrength y j μ ν) := by
  unfold cartesianStrength transverseRatio shellEnergy energy transverseMass
  fun_prop

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.transverseRatio_bound
#print axioms F1Fecho.MaxwellGlobal.cartesianStrength_bound
#print axioms F1Fecho.MaxwellGlobal.cartesianStrength_measurable
