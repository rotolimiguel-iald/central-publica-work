import TGLExt.FLRWGeometry
import TGLExt.TriadMaster

set_option autoImplicit false
set_option maxHeartbeats 2400000

/-! Order 012 B2: components and conservation for the same metric construction. -/
namespace ChatgptAudit.FLRW
open Matrix TGLExt ChatgptAudit.GeneralMetric
open scoped ContDiff
noncomputable section

theorem flrw_einstein_tensor (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x =
      Matrix.diagonal ![3*(flrwHubble a (x 0))^2,
        -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2),
        -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2),
        -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2)] := by
  have hz := (hpos x hx).ne'
  unfold geometricEinsteinTensor coordinateScalarCurvature
  rw [flrw_ricci U hU a ha hpos x hx, flrw_metric_inverse a x hz]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flrwInverse, flrwMetric, flrwHubble, Matrix.diagonal, Fin.sum_univ_four] <;>
    field_simp <;> ring

theorem flrw_einstein_00 (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x 0 0 =
      3*(flrwHubble a (x 0))^2 := by
  simp [flrw_einstein_tensor U hU a ha hpos x hx]

theorem flrw_einstein_spatial (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) (hi : i ≠ 0) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x i i =
      -(2*a (x 0)*deriv (deriv a) (x 0)+(deriv a (x 0))^2) := by
  rw [flrw_einstein_tensor U hU a ha hpos x hx]
  fin_cases i <;> simp_all

theorem flrw_null_ricci (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) (k : SpacetimeVector)
    (hk : tensorQuad (flrwMetric a x) k = 0) :
    tensorQuad (coordinateRicci
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x) k =
      2*((flrwHubble a (x 0))^2-deriv (deriv a) (x 0)/a (x 0))*(k 0)^2 := by
  have hz := (hpos x hx).ne'
  have hn : (k 0)^2 = (a (x 0))^2*((k 1)^2+(k 2)^2+(k 3)^2) := by
    simp [tensorQuad, flrwMetric, dotProduct, Matrix.mulVec, Fin.sum_univ_four,
      Matrix.diagonal] at hk
    nlinarith [hk]
  rw [flrw_ricci U hU a ha hpos x hx]
  simp only [tensorQuad, dotProduct, Matrix.mulVec, Fin.sum_univ_four]
  simp [Matrix.diagonal]
  calc
    _ = (-3*deriv (deriv a) (x 0)/a (x 0))*(k 0)^2 +
        (a (x 0)*deriv (deriv a) (x 0)+2*(deriv a (x 0))^2)*
          ((k 1)^2+(k 2)^2+(k 3)^2) := by ring
    _ = _ := by rw [hn]; unfold flrwHubble; field_simp; ring

def flrwStress (a rho pressure : ℝ → ℝ) : TensorField4 := fun x =>
  Matrix.diagonal ![rho (x 0), pressure (x 0)*(a (x 0))^2,
    pressure (x 0)*(a (x 0))^2, pressure (x 0)*(a (x 0))^2]

theorem flrw_stress_symmetric (a rho pressure : ℝ → ℝ) (x : Coordinate4) :
    (flrwStress a rho pressure x)ᵀ = flrwStress a rho pressure x := by
  simp [flrwStress]

theorem flrw_stress_differentiable (U : Set Coordinate4) (a rho pressure : ℝ → ℝ)
    (ha : ∀ x∈U, DifferentiableAt ℝ a (x 0))
    (hr : ∀ x∈U, DifferentiableAt ℝ rho (x 0))
    (hp : ∀ x∈U, DifferentiableAt ℝ pressure (x 0)) :
    ∀ i j, DifferentiableOn ℝ (fun x => flrwStress a rho pressure x i j) U := by
  intro i j x hx
  have ht : DifferentiableAt ℝ (fun y : Coordinate4 => y 0) x := by fun_prop
  have hd : DifferentiableAt ℝ (fun y : Coordinate4 => pressure (y 0)*(a (y 0))^2) x :=
    ((hp x hx).comp x ht).mul (((ha x hx).comp x ht).pow 2)
  have hdr := (hr x hx).comp x ht
  fin_cases i <;> fin_cases j <;> dsimp [flrwStress, Matrix.diagonal] <;>
    fun_prop

theorem flrw_stress_jet (a rho pressure : ℝ → ℝ) (x : Coordinate4)
    (ha : DifferentiableAt ℝ a (x 0)) (hr : DifferentiableAt ℝ rho (x 0))
    (hp : DifferentiableAt ℝ pressure (x 0)) (i : Fin 4) :
    tensorFieldJet (flrwStress a rho pressure) x i = if i = 0 then
      Matrix.diagonal ![deriv rho (x 0),
        deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0)),
        deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0)),
        deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0))]
      else 0 := by
  have hd : HasDerivAt (fun t => pressure t*(a t)^2)
      (deriv pressure (x 0)*(a (x 0))^2 + pressure (x 0)*(2*a (x 0)*deriv a (x 0)))
      (x 0) := by
    simpa [mul_assoc] using! hp.hasDerivAt.mul (ha.hasDerivAt.pow 2)
  have hs (j : Fin 4) := coordinatePartial_time_function _ _ x hd j
  have hrt (j : Fin 4) := coordinatePartial_time_function _ _ x hr.hasDerivAt j
  have hc (c : ℝ) (j : Fin 4) : coordinatePartial (fun _ => c) x j = 0 := by
    simp [coordinatePartial]
  by_cases hi : i = 0 <;> ext j k <;> fin_cases j <;> fin_cases k <;>
    simp [tensorFieldJet, flrwStress, Matrix.diagonal, hs, hrt, hc, hi]

theorem flrw_stress_divergence (a rho pressure : ℝ → ℝ) (x : Coordinate4)
    (hz : a (x 0) ≠ 0) (ha : DifferentiableAt ℝ a (x 0))
    (hr : DifferentiableAt ℝ rho (x 0)) (hp : DifferentiableAt ℝ pressure (x 0)) :
    tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a rho pressure) x =
      ![deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)),0,0,0] := by
  funext j
  fin_cases j <;>
    simp [tensorFieldDivergence, tensorJetDivergence, covariantTensorJet,
      flrw_metric_inverse a x hz, flrw_connection a x hz ha, flrw_stress_jet a rho pressure x ha hr hp,
      flrwStress, flrwInverse, flrwConnection, flrwConnectionForm, flrwHubble,
      Matrix.mul_apply, Fin.sum_univ_four, Matrix.diagonal]
  field_simp
  ring

theorem flrw_continuity (a rho pressure : ℝ → ℝ) (x : Coordinate4)
    (hz : a (x 0) ≠ 0) (ha : DifferentiableAt ℝ a (x 0))
    (hr : DifferentiableAt ℝ rho (x 0)) (hp : DifferentiableAt ℝ pressure (x 0))
    (hdiv : tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a rho pressure) x 0 = 0) :
    deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)) = 0 := by
  simpa [flrw_stress_divergence a rho pressure x hz ha hr hp] using hdiv

/-- The 00 component of the existing metric equation; its constant stays explicit. -/
theorem flrw_friedmann_first (U : Set Coordinate4) (hU : IsOpen U)
    (a rho pressure : ℝ → ℝ) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
    (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
    (coupling cosmological : ℝ)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x +
      cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
    (flrwHubble a (x 0))^2 = coupling/3*rho (x 0)-cosmological/3 := by
  have h00 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 0) hE
  simp [flrw_einstein_tensor U hU a ha hpos x hx, flrwMetric, flrwStress] at h00
  linarith

theorem flrw_acceleration (U : Set Coordinate4) (hU : IsOpen U)
    (a rho pressure : ℝ → ℝ) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
    (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
    (coupling cosmological : ℝ)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x +
      cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
    deriv (deriv a) (x 0)/a (x 0) =
      -coupling/6*(rho (x 0)+3*pressure (x 0))-cosmological/3 := by
  have hz := (hpos x hx).ne'
  have h11 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 1 1) hE
  simp [flrw_einstein_tensor U hU a ha hpos x hx, flrwMetric, flrwStress] at h11
  have hs : -(2*deriv (deriv a) (x 0)/a (x 0)+(flrwHubble a (x 0))^2)-
      cosmological = coupling*pressure (x 0) := by
    unfold flrwHubble
    field_simp
    nlinarith [h11]
  have h00 := flrw_friedmann_first U hU a rho pressure ha hpos x hx coupling cosmological hE
  linear_combination -(1/2:ℝ)*hs - (1/2:ℝ)*h00

theorem flrw_friedmann_second (U : Set Coordinate4) (hU : IsOpen U)
    (a rho pressure : ℝ → ℝ) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
    (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
    (coupling cosmological : ℝ)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x +
      cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
    deriv (flrwHubble a) (x 0) = -coupling/2*(rho (x 0)+pressure (x 0)) := by
  have hz := (hpos x hx).ne'
  have hda : DifferentiableAt ℝ a (x 0) := (ha x hx).differentiableAt (by simp)
  have hdda : DifferentiableAt ℝ (deriv a) (x 0) :=
    ((ha x hx).derivWithin (m := ∞) (by simp)).differentiableAt (by simp)
  have hh : HasDerivAt (flrwHubble a)
      ((deriv (deriv a) (x 0)*a (x 0)-(deriv a (x 0))^2)/(a (x 0))^2) (x 0) := by
    simpa [flrwHubble, pow_two] using! hdda.hasDerivAt.div hda.hasDerivAt hz
  have h00 := flrw_friedmann_first U hU a rho pressure ha hpos x hx coupling cosmological hE
  have hacc := flrw_acceleration U hU a rho pressure ha hpos x hx coupling cosmological hE
  rw [hh.deriv]
  calc
    _ = deriv (deriv a) (x 0)/a (x 0)-(flrwHubble a (x 0))^2 := by
      unfold flrwHubble; field_simp
    _ = _ := by linarith

/-- Instantiates the existing general Einstein theorem, then reads the FLRW equations.
The null balance and covariant conservation remain explicit hypotheses. -/
theorem flrw_friedmann_from_general_metric
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (a rho pressure : ℝ → ℝ) (eta : ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (hr : ∀ y∈U, DifferentiableAt ℝ rho (y 0))
    (hp : ∀ y∈U, DifferentiableAt ℝ pressure (y 0))
    (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
        (2*Real.pi/eta) • flrwStress a rho pressure x) v = 0)
    (H_conservation : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a rho pressure) x j = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      (flrwHubble a (x 0))^2 = (2*Real.pi/eta)/3*rho (x 0)-cosmological/3 ∧
      deriv (flrwHubble a) (x 0) = -(2*Real.pi/eta)/2*(rho (x 0)+pressure (x 0)) ∧
      deriv rho (x 0)+3*flrwHubble a (x 0)*(rho (x 0)+pressure (x 0)) = 0 := by
  have hda : ∀ y∈U, DifferentiableAt ℝ a (y 0) :=
    fun y hy => (ha y hy).differentiableAt (by simp)
  obtain ⟨cosmological,hE⟩ := metric_only_einstein_equation U hU hconn
    (flrwMetric a) (flrwStress a rho pressure) (2*Real.pi/eta)
    (fun y hy => flrw_metric_lorentz a y (hpos y hy).ne') (flrw_metric_smooth U a ha)
    (flrw_stress_differentiable U a rho pressure hda hr hp)
    (fun x _ => flrw_stress_symmetric a rho pressure x) H_null H_conservation
  refine ⟨cosmological, fun x hx => ⟨?_,?_,?_⟩⟩
  · exact flrw_friedmann_first U hU a rho pressure ha hpos x hx _ _ (hE x hx)
  · exact flrw_friedmann_second U hU a rho pressure ha hpos x hx _ _ (hE x hx)
  · exact flrw_continuity a rho pressure x (hpos x hx).ne' (hda x hx)
      (hr x hx) (hp x hx) (H_conservation x hx 0)

/-- The Newton coefficient uses the imported area calibration; G is not derived. -/
theorem flrw_newton_coefficient (G : ℝ) (hG : 0 < G) :
    (2*Real.pi/(1/(4*G)))/3 = 8*Real.pi*G/3 := by
  have he := congrArg (fun q : ℝ => q⁻¹)
    (einstein_coefficient_from_clausius 1 1 G hG.ne')
  have hc : 2*Real.pi/(1/(4*G)) = 8*Real.pi*G := by
    simpa [one_div, div_eq_mul_inv, mul_assoc, mul_left_comm, mul_comm] using he
  exact congrArg (fun q : ℝ => q/3) hc

end
end ChatgptAudit.FLRW
