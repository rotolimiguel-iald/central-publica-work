import PauliOperationalSurface
import PauliProbabilityModel
import ScreenAreaCalculus

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.Observable035
open Matrix TGLExt ChatgptAudit ChatgptAudit.Thermal025
noncomputable section

/-- Coordinate derivatives of the actual joint measurement probabilities at the origin. -/
def pauliProbabilityGradient (P : SiteProfile) (n m : ℕ) (z : Fin 2 × Fin 2) :
    Fin 2 → ℝ :=
  ![deriv (fun s : ℝ => pauliProbability P n m z s 0) 0,
    deriv (fun t : ℝ => pauliProbability P n m z 0 t) 0]

/-- Classical Fisher matrix of the specified measurement, evaluated at the origin. -/
def pauliMeasurementFisher (P : SiteProfile) (n m : ℕ) : ScreenMatrix :=
  fun i j => ∑ z : Fin 2 × Fin 2,
    pauliProbabilityGradient P n m z i*pauliProbabilityGradient P n m z j /
      pauliProbability P n m z 0 0

/-- Area density in these parameter coordinates; no spacetime identification. -/
def pauliFisherArea (P : SiteProfile) (n m : ℕ) : ℝ :=
  screenArea (pauliMeasurementFisher P n m)

theorem pauli_probability_gradient (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (z : Fin 2 × Fin 2) :
    pauliProbabilityGradient P n m z =
      ![signOutcome z.1*(2*P.w n-1)/2,signOutcome z.2*(2*P.w m-1)/2] := by
  simp only [pauliProbabilityGradient,(pauli_probability_first_derivative P h z).deriv,
    (pauli_probability_second_derivative P h z).deriv]

theorem pauli_measurement_fisher_diagonal (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    pauliMeasurementFisher P n m=!![4*(2*P.w n-1)^2,0;0,4*(2*P.w m-1)^2] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [pauliMeasurementFisher,pauli_probability_gradient P h,
      pauli_probability_origin P h,Fintype.sum_prod_type,Fin.sum_univ_two,signOutcome] <;> ring

theorem pauli_measurement_fisher_determinant (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    (pauliMeasurementFisher P n m).det=16*(2*P.w n-1)^2*(2*P.w m-1)^2 := by
  rw [pauli_measurement_fisher_diagonal P h,Matrix.det_fin_two]
  simp
  ring

theorem pauli_measurement_fisher_determinant_square (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    (pauliMeasurementFisher P n m).det=(4*(2*P.w n-1)*(2*P.w m-1))^2 := by
  rw [pauli_measurement_fisher_determinant P h]
  ring

theorem pauli_measurement_fisher_determinant_nonnegative
    (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    0≤(pauliMeasurementFisher P n m).det := by
  rw [pauli_measurement_fisher_determinant_square P h]
  positivity

theorem pauli_measurement_fisher_determinant_positive
    (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hn : P.w n≠1/2) (hm : P.w m≠1/2) :
    0<(pauliMeasurementFisher P n m).det := by
  rw [pauli_measurement_fisher_determinant_square P h]
  rw [←pauli_observable_jacobian_determinant P h]
  exact pauli_observable_jacobian_squared_determinant_positive P h hn hm

theorem pauli_fisher_area_formula (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    pauliFisherArea P n m=4*|(2*P.w n-1)*(2*P.w m-1)| := by
  rw [pauliFisherArea,screenArea,pauli_measurement_fisher_determinant_square P h,
    Real.sqrt_sq_eq_abs]
  rw [mul_assoc,abs_mul]
  norm_num

/-- Equality is derived from measured probabilities, not imposed as a metric definition. -/
theorem pauli_fisher_area_eq_abs_jacobian (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    pauliFisherArea P n m=|(pauliObservableJacobian P n m).det| := by
  rw [pauliFisherArea,screenArea,pauli_measurement_fisher_determinant_square P h,
    Real.sqrt_sq_eq_abs,pauli_observable_jacobian_determinant P h]

theorem pauli_fisher_area_positive (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hn : P.w n≠1/2) (hm : P.w m≠1/2) :
    0<pauliFisherArea P n m :=
  screen_area_positive _ (pauli_measurement_fisher_determinant_positive P h hn hm)

theorem pauli_measurement_fisher_quadratic (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (v : Fin 2 → ℝ) :
    ∑ i, ∑ j, v i*pauliMeasurementFisher P n m i j*v j =
      4*(2*P.w n-1)^2*(v 0)^2+4*(2*P.w m-1)^2*(v 1)^2 := by
  rw [pauli_measurement_fisher_diagonal P h]
  simp [Fin.sum_univ_two]
  ring

theorem pauli_measurement_fisher_quadratic_nonnegative
    (P : SiteProfile) {n m : ℕ} (h : n≠m) (v : Fin 2 → ℝ) :
    0≤∑ i, ∑ j, v i*pauliMeasurementFisher P n m i j*v j := by
  rw [pauli_measurement_fisher_quadratic P h]
  positivity

theorem pauli_fisher_area_first_tracial (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hn : P.w n=1/2) : pauliFisherArea P n m=0 := by
  rw [pauli_fisher_area_formula P h,hn]
  norm_num

theorem pauli_fisher_area_second_tracial (P : SiteProfile) {n m : ℕ} (h : n≠m)
    (hm : P.w m=1/2) : pauliFisherArea P n m=0 := by
  rw [pauli_fisher_area_formula P h,hm]
  norm_num

theorem reference_pauli_measurement_fisher :
    pauliMeasurementFisher thirdThermalReference 0 1=!![4/9,0;0,4/9] := by
  rw [pauli_measurement_fisher_diagonal thirdThermalReference (by decide)]
  norm_num [thirdThermalReference]

theorem reference_pauli_fisher_area :
    pauliFisherArea thirdThermalReference 0 1=4/9 := by
  rw [pauli_fisher_area_formula thirdThermalReference (by decide)]
  norm_num [thirdThermalReference]

theorem tracial_pauli_measurement_fisher {n m : ℕ} (h : n≠m) :
    pauliMeasurementFisher halfThermalReference n m=0 := by
  rw [pauli_measurement_fisher_diagonal halfThermalReference h]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [halfThermalReference]

theorem tracial_pauli_fisher_area {n m : ℕ} (h : n≠m) :
    pauliFisherArea halfThermalReference n m=0 := by
  apply pauli_fisher_area_first_tracial halfThermalReference h
  norm_num [halfThermalReference]

#print axioms pauliProbabilityGradient
#print axioms pauliMeasurementFisher
#print axioms pauliFisherArea
#print axioms pauli_probability_gradient
#print axioms pauli_measurement_fisher_diagonal
#print axioms pauli_measurement_fisher_determinant
#print axioms pauli_measurement_fisher_determinant_square
#print axioms pauli_measurement_fisher_determinant_nonnegative
#print axioms pauli_measurement_fisher_determinant_positive
#print axioms pauli_fisher_area_formula
#print axioms pauli_fisher_area_eq_abs_jacobian
#print axioms pauli_fisher_area_positive
#print axioms pauli_measurement_fisher_quadratic
#print axioms pauli_measurement_fisher_quadratic_nonnegative
#print axioms pauli_fisher_area_first_tracial
#print axioms pauli_fisher_area_second_tracial
#print axioms reference_pauli_measurement_fisher
#print axioms reference_pauli_fisher_area
#print axioms tracial_pauli_measurement_fisher
#print axioms tracial_pauli_fisher_area

end
end ChatgptAudit.Observable035
