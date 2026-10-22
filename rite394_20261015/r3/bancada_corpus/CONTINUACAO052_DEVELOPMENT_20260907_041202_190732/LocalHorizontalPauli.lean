import AperiodicCentralizerExpectation
import CentralizerContractBridge
import ExpectationAlgebra
import SitePauliObservables
import UnitaryStateDerivative

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Orbit052

open TGLExt Matrix ChatgptAudit.Cocycle030 ChatgptAudit.Observable035
  ChatgptAudit.Density033 ChatgptAudit.Aperiodic046 ChatgptAudit.Expectation047

noncomputable section

/-- Real generators in the first-site Pauli plane, inside the existing tower. -/
def pauliHorizontal (P : SiteProfile) (v : Fin 2 → ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  (v 0 : ℂ) • sitePauliX P 0 + (v 1 : ℂ) • sitePauliY P 0

theorem pauli_horizontal_add (P : SiteProfile) (u v : Fin 2 → ℝ) :
    pauliHorizontal P (u + v) = pauliHorizontal P u + pauliHorizontal P v := by
  simp only [pauliHorizontal, Pi.add_apply, Complex.ofReal_add, add_smul]
  abel

theorem pauli_horizontal_smul (P : SiteProfile) (a : ℝ) (v : Fin 2 → ℝ) :
    pauliHorizontal P (a • v) = (a : ℂ) • pauliHorizontal P v := by
  simp only [pauliHorizontal, Pi.smul_apply, smul_eq_mul, Complex.ofReal_mul,
    smul_add, smul_smul]

theorem pauli_horizontal_basis_x (P : SiteProfile) :
    pauliHorizontal P ![1, 0] = sitePauliX P 0 := by
  simp [pauliHorizontal]

theorem pauli_horizontal_basis_y (P : SiteProfile) :
    pauliHorizontal P ![0, 1] = sitePauliY P 0 := by
  simp [pauliHorizontal]

theorem pauli_horizontal_mem_factor (P : SiteProfile) (v : Fin 2 → ℝ) :
    pauliHorizontal P v ∈ theFactorObject P :=
  add_mem
    ((theFactorObject P).toStarSubalgebra.smul_mem (site_pauli_x_mem_factor P 0) _)
    ((theFactorObject P).toStarSubalgebra.smul_mem (site_pauli_y_mem_factor P 0) _)

theorem pauli_horizontal_selfadjoint (P : SiteProfile) (v : Fin 2 → ℝ) :
    IsSelfAdjoint (pauliHorizontal P v) := by
  change star (pauliHorizontal P v) = pauliHorizontal P v
  simp only [pauliHorizontal, star_add, star_smul, Complex.star_def, Complex.conj_ofReal,
    (site_pauli_x_selfadjoint P 0).star_eq, (site_pauli_y_selfadjoint P 0).star_eq]

theorem pauli_horizontal_state (P : SiteProfile) (v : Fin 2 → ℝ) :
    omegaState P (pauliHorizontal P v) = 0 := by
  simp only [pauliHorizontal, omega_state_add, omega_state_smul,
    site_pauli_x_state, site_pauli_y_state, mul_zero, add_zero]

/-- Pinching is the restriction of the constructed aperiodic expectation. -/
theorem aperiodic_pauli_x_zero (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    (aperiodicExpectationInput P).E (sitePauliX P 0) = 0 := by
  have h01 : P.w 0 ≠ 1 - P.w 0 := by intro h; apply hp; linarith
  have h10 : 1 - P.w 0 ≠ P.w 0 := Ne.symm h01
  change (aperiodicExpectationInput P).E (towerPi P (N := 0) pauliXMatrix) = 0
  rw [global_expectation_restricts_to_pinching]
  have hpin : specExpect (towerW P 0) pauliXMatrix = 0 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [specExpect, towerW, siteW, pauliXMatrix, h01, h10]
  rw [hpin]
  exact (towerPiLinear P 0).map_zero

theorem aperiodic_pauli_y_zero (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    (aperiodicExpectationInput P).E (sitePauliY P 0) = 0 := by
  have h01 : P.w 0 ≠ 1 - P.w 0 := by intro h; apply hp; linarith
  have h10 : 1 - P.w 0 ≠ P.w 0 := Ne.symm h01
  change (aperiodicExpectationInput P).E (towerPi P (N := 0) pauliYMatrix) = 0
  rw [global_expectation_restricts_to_pinching]
  have hpin : specExpect (towerW P 0) pauliYMatrix = 0 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [specExpect, towerW, siteW, pauliYMatrix, h01, h10]
  rw [hpin]
  exact (towerPiLinear P 0).map_zero

theorem pauli_horizontal_expectation (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (v : Fin 2 → ℝ) :
    (aperiodicExpectationInput P).E (pauliHorizontal P v) = 0 := by
  rw [pauliHorizontal, expectation_add P (aperiodicExpectationInput P) _ _
    ((theFactorObject P).toStarSubalgebra.smul_mem (site_pauli_x_mem_factor P 0) _)
    ((theFactorObject P).toStarSubalgebra.smul_mem (site_pauli_y_mem_factor P 0) _),
    expectation_smul P (aperiodicExpectationInput P) _ _ (site_pauli_x_mem_factor P 0),
    expectation_smul P (aperiodicExpectationInput P) _ _ (site_pauli_y_mem_factor P 0),
    aperiodic_pauli_x_zero P hp, aperiodic_pauli_y_zero P hp, smul_zero, smul_zero,
    add_zero]

/-- The full complex pairing retains its alternating imaginary component. -/
theorem pauli_horizontal_pairing (P : SiteProfile) (u v : Fin 2 → ℝ) :
    omegaState P (star (pauliHorizontal P u) * pauliHorizontal P v) =
      ((u 0 * v 0 + u 1 * v 1 : ℝ) : ℂ) +
        Complex.I * (((2 * P.w 0 - 1) * (u 0 * v 1 - u 1 * v 0) : ℝ) : ℂ) := by
  have h1 : omegaState P (1 : TowerHilbert P →L[ℂ] TowerHilbert P) = 1 := by
    exact hOmega_inner_self
  rw [(pauli_horizontal_selfadjoint P u).star_eq]
  simp only [pauliHorizontal, add_mul, mul_add, smul_mul_assoc, mul_smul_comm,
    smul_smul, omega_state_add, omega_state_smul, site_pauli_x_square,
    site_pauli_y_square, site_pauli_xy, site_pauli_yx, h1, site_pauli_z_state]
  push_cast
  ring

theorem pauli_horizontal_re_pairing (P : SiteProfile) (u v : Fin 2 → ℝ) :
    (omegaState P (star (pauliHorizontal P u) * pauliHorizontal P v)).re =
      u 0 * v 0 + u 1 * v 1 := by
  rw [pauli_horizontal_pairing]
  simp

theorem pauli_horizontal_im_pairing (P : SiteProfile) (u v : Fin 2 → ℝ) :
    (omegaState P (star (pauliHorizontal P u) * pauliHorizontal P v)).im =
      (2 * P.w 0 - 1) * (u 0 * v 1 - u 1 * v 0) := by
  rw [pauli_horizontal_pairing]
  simp

theorem pauli_horizontal_gns_norm_sq (P : SiteProfile) (v : Fin 2 → ℝ) :
    ‖pauliHorizontal P v (hOmega P)‖ ^ 2 = (v 0)^2 + (v 1)^2 := by
  rw [norm_sq_eq_re_inner (𝕜 := ℂ)]
  have h := pauli_horizontal_re_pairing P v v
  rw [omega_product_inner, star_star] at h
  simpa only [pow_two] using h

theorem pauli_x_gns_norm (P : SiteProfile) :
    ‖sitePauliX P 0 (hOmega P)‖ = 1 := by
  have h := pauli_horizontal_gns_norm_sq P ![1, 0]
  rw [pauli_horizontal_basis_x] at h
  norm_num at h
  nlinarith [norm_nonneg (sitePauliX P 0 (hOmega P))]

theorem pauli_y_gns_norm (P : SiteProfile) :
    ‖sitePauliY P 0 (hOmega P)‖ = 1 := by
  have h := pauli_horizontal_gns_norm_sq P ![0, 1]
  rw [pauli_horizontal_basis_y] at h
  norm_num at h
  nlinarith [norm_nonneg (sitePauliY P 0 (hOmega P))]

theorem pauli_xy_gns_pairing (P : SiteProfile) :
    inner ℂ (sitePauliX P 0 (hOmega P)) (sitePauliY P 0 (hOmega P)) =
      Complex.I * ((2 * P.w 0 - 1 : ℝ) : ℂ) := by
  have h := pauli_horizontal_pairing P ![1, 0] ![0, 1]
  rw [pauli_horizontal_basis_x, pauli_horizontal_basis_y,
    omega_product_inner, star_star] at h
  simpa using h

/-- The real reading of an existing035 unitary state curve. -/
def horizontalReading (P : SiteProfile) (v : Fin 2 → ℝ)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (t : ℝ) : ℝ :=
  (orbitExpectation P (pauliHorizontal P v) 0 B t 0).re

theorem horizontal_x_commutator (P : SiteProfile) (v : Fin 2 → ℝ) :
    Complex.I * omegaState P
      (sitePauliX P 0 * pauliHorizontal P v - pauliHorizontal P v * sitePauliX P 0) =
      ((-2 * (2 * P.w 0 - 1) * v 1 : ℝ) : ℂ) := by
  simp only [pauliHorizontal, mul_add, add_mul, mul_smul_comm, smul_mul_assoc,
    omegaState_sub, omega_state_add, omega_state_smul,
    site_pauli_xy, site_pauli_yx, site_pauli_z_state]
  push_cast
  ring_nf
  simp only [Complex.I_sq]
  ring

theorem horizontal_y_commutator (P : SiteProfile) (v : Fin 2 → ℝ) :
    Complex.I * omegaState P
      (sitePauliY P 0 * pauliHorizontal P v - pauliHorizontal P v * sitePauliY P 0) =
      ((2 * (2 * P.w 0 - 1) * v 0 : ℝ) : ℂ) := by
  simp only [pauliHorizontal, mul_add, add_mul, mul_smul_comm, smul_mul_assoc,
    omegaState_sub, omega_state_add, omega_state_smul,
    site_pauli_xy, site_pauli_yx, site_pauli_z_state]
  push_cast
  ring_nf
  simp only [Complex.I_sq]
  ring

theorem horizontal_x_reading_derivative (P : SiteProfile) (v : Fin 2 → ℝ) :
    HasDerivAt (horizontalReading P v (sitePauliX P 0))
      (-2 * (2 * P.w 0 - 1) * v 1) 0 := by
  have hd := orbit_expectation_first_derivative P (pauliHorizontal P v) 0
    (sitePauliX P 0) (pauli_horizontal_selfadjoint P v)
  rw [horizontal_x_commutator] at hd
  simpa only [horizontalReading, Function.comp_def, Complex.reCLM_apply,
    Complex.ofReal_re] using (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd)

theorem horizontal_y_reading_derivative (P : SiteProfile) (v : Fin 2 → ℝ) :
    HasDerivAt (horizontalReading P v (sitePauliY P 0))
      (2 * (2 * P.w 0 - 1) * v 0) 0 := by
  have hd := orbit_expectation_first_derivative P (pauliHorizontal P v) 0
    (sitePauliY P 0) (pauli_horizontal_selfadjoint P v)
  rw [horizontal_y_commutator] at hd
  simpa only [horizontalReading, Function.comp_def, Complex.reCLM_apply,
    Complex.ofReal_re] using (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd)

/-- Both components are actual derivatives, not an assigned response matrix. -/
def horizontalResponse (P : SiteProfile) (v : Fin 2 → ℝ) : Fin 2 → ℝ :=
  ![deriv (horizontalReading P v (sitePauliX P 0)) 0,
    deriv (horizontalReading P v (sitePauliY P 0)) 0]

theorem horizontal_response_formula (P : SiteProfile) (v : Fin 2 → ℝ) :
    horizontalResponse P v =
      ![-2 * (2 * P.w 0 - 1) * v 1, 2 * (2 * P.w 0 - 1) * v 0] := by
  rw [horizontalResponse, (horizontal_x_reading_derivative P v).deriv,
    (horizontal_y_reading_derivative P v).deriv]

def horizontalResponseMatrix (P : SiteProfile) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![horizontalResponse P ![1, 0] 0, horizontalResponse P ![0, 1] 0;
     horizontalResponse P ![1, 0] 1, horizontalResponse P ![0, 1] 1]

theorem horizontal_response_matrix (P : SiteProfile) :
    horizontalResponseMatrix P =
      !![0, -2 * (2 * P.w 0 - 1); 2 * (2 * P.w 0 - 1), 0] := by
  simp [horizontalResponseMatrix, horizontal_response_formula]

theorem horizontal_response_determinant (P : SiteProfile) :
    (horizontalResponseMatrix P).det = 4 * (2 * P.w 0 - 1)^2 := by
  rw [horizontal_response_matrix, Matrix.det_fin_two]
  simp
  ring

theorem horizontal_response_injective (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    Function.Injective (horizontalResponse P) := by
  intro u v huv
  have h0 := congrFun huv 0
  have h1 := congrFun huv 1
  rw [horizontal_response_formula, horizontal_response_formula] at h0 h1
  norm_num at h0 h1
  have hr : 2 * P.w 0 - 1 ≠ 0 := by intro h; apply hp; linarith
  have hu : u 0 = v 0 := by
    apply (mul_left_cancel₀ (mul_ne_zero (by norm_num : (2 : ℝ) ≠ 0) hr))
    exact h1
  have hv : u 1 = v 1 := by
    apply (mul_left_cancel₀ (mul_ne_zero (by norm_num : (-2 : ℝ) ≠ 0) hr))
    exact h0
  funext i
  fin_cases i
  · exact hu
  · exact hv

/-- Equality of all global state readings forces equality of these local orbit tangents. -/
theorem horizontal_state_tangent_separates (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (u v : Fin 2 → ℝ)
    (h : ∀ B ∈ theFactorObject P,
      deriv (horizontalReading P u B) 0 = deriv (horizontalReading P v B) 0) :
    u = v := by
  apply horizontal_response_injective P hp
  simp only [horizontalResponse,
    h (sitePauliX P 0) (site_pauli_x_mem_factor P 0),
    h (sitePauliY P 0) (site_pauli_y_mem_factor P 0)]

theorem horizontal_response_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2)
    (v : Fin 2 → ℝ) : horizontalResponse P v = 0 := by
  rw [horizontal_response_formula, hp]
  ext i
  fin_cases i <;> norm_num

theorem aperiodic_pauli_x_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2) :
    (aperiodicExpectationInput P).E (sitePauliX P 0) = sitePauliX P 0 := by
  change (aperiodicExpectationInput P).E (towerPi P (N := 0) pauliXMatrix) = _
  rw [global_expectation_restricts_to_pinching]
  congr 1
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [specExpect, towerW, siteW, hp]

theorem aperiodic_pauli_y_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2) :
    (aperiodicExpectationInput P).E (sitePauliY P 0) = sitePauliY P 0 := by
  change (aperiodicExpectationInput P).E (towerPi P (N := 0) pauliYMatrix) = _
  rw [global_expectation_restricts_to_pinching]
  congr 1
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [specExpect, towerW, siteW, hp]

#print axioms pauliHorizontal
#print axioms pauli_horizontal_add
#print axioms pauli_horizontal_smul
#print axioms pauli_horizontal_basis_x
#print axioms pauli_horizontal_basis_y
#print axioms pauli_horizontal_mem_factor
#print axioms pauli_horizontal_selfadjoint
#print axioms pauli_horizontal_state
#print axioms aperiodic_pauli_x_zero
#print axioms aperiodic_pauli_y_zero
#print axioms pauli_horizontal_expectation
#print axioms pauli_horizontal_pairing
#print axioms pauli_horizontal_re_pairing
#print axioms pauli_horizontal_im_pairing
#print axioms pauli_horizontal_gns_norm_sq
#print axioms pauli_x_gns_norm
#print axioms pauli_y_gns_norm
#print axioms pauli_xy_gns_pairing
#print axioms horizontalReading
#print axioms horizontal_x_commutator
#print axioms horizontal_y_commutator
#print axioms horizontal_x_reading_derivative
#print axioms horizontal_y_reading_derivative
#print axioms horizontalResponse
#print axioms horizontal_response_formula
#print axioms horizontalResponseMatrix
#print axioms horizontal_response_matrix
#print axioms horizontal_response_determinant
#print axioms horizontal_response_injective
#print axioms horizontal_state_tangent_separates
#print axioms horizontal_response_tracial
#print axioms aperiodic_pauli_x_tracial
#print axioms aperiodic_pauli_y_tracial

end
end ChatgptAudit.Orbit052
