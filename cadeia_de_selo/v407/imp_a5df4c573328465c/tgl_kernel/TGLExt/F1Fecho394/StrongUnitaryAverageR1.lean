import TGLExt.F1Fecho394.ClosedGraphRegularizationR3

/-! Bounded operators obtained by strong, real-kernel unitary averaging.
No operator-norm measurability of the unitary group is required. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.StrongUnitaryAverage
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (U:ℝ→H≃ₗᵢ[ℂ]H) (hc:∀x,Continuous (fun t=>U t x))
    (w:ℝ→ℝ) (hw:Integrable w volume)

def averageLinear : H→ₗ[ℂ]H where
  toFun x:=∫t:ℝ,w t • U t x
  map_add' x y:=by
    simp only [map_add,smul_add]
    exact integral_add
      (ClosedGraphRegularization.weighted_orbit_integrable U hc w hw x)
      (ClosedGraphRegularization.weighted_orbit_integrable U hc w hw y)
  map_smul' c x:=by
    simp only [map_smul,smul_comm (w _) c]
    exact integral_smul c (fun t:ℝ=>w t • U t x)

theorem average_bound (x:H) : ‖averageLinear U hc w hw x‖≤(∫t:ℝ,‖w t‖)*‖x‖ := by
  change ‖∫t:ℝ,w t • U t x‖≤_
  calc
    _ ≤ ∫t:ℝ,‖w t • U t x‖ := norm_integral_le_integral_norm _
    _ = (∫t:ℝ,‖w t‖)*‖x‖ := by
      simp only [norm_smul,(U _).norm_map]
      exact integral_mul_const ‖x‖ (fun t:ℝ=>‖w t‖)

def average : H→L[ℂ]H := (averageLinear U hc w hw).mkContinuous (∫t:ℝ,‖w t‖)
  (average_bound U hc w hw)

theorem average_apply (x:H) : average U hc w hw x=∫t:ℝ,w t • U t x := rfl

end F1Fecho.StrongUnitaryAverage
#print axioms F1Fecho.StrongUnitaryAverage.averageLinear
#print axioms F1Fecho.StrongUnitaryAverage.average_bound
#print axioms F1Fecho.StrongUnitaryAverage.average_apply
