import Mathlib

set_option autoImplicit false

/-!
# Escala de area e equivalencia Planck--Newton   [KERNEL/UNCONDITIONAL, dadas as variaveis]

`A(P) = kappa_A * tau(P)`. Com `S = 1/2`, `tau(P_F) = 1`:
  `eta = S / kappa_A = 1/(2 kappa_A)`,  `2 pi / eta = 4 pi kappa_A`.
Equivalencia: `2 pi / eta = 8 pi G  ↔  kappa_A = 2 G`  (para `G, kappa_A > 0`).

ISTO NAO AFIRMA QUE `G` FOI DERIVADO. `G` e' entrada fisica medida; a igualdade
e' uma equivalencia (calibracao) relativa a `G`.
-/

namespace TGL.AreaScale

/-- Com `S = 1/2`: `eta = S / kappa = (1/2)/kappa = 1/(2 kappa)`. -/
theorem eta_eq_one_over_two_kappa (kappa : ℝ) :
    (1 / 2) / kappa = 1 / (2 * kappa) := by
  rw [div_div]

/-- Equivalencia de Newton--Planck: `2 pi / (1/(2 kappa)) = 8 pi G  ↔  kappa = 2 G`. -/
theorem newtonPlanck_equivalence (kappa G : ℝ) (hk : 0 < kappa) (hG : 0 < G) :
    2 * Real.pi / (1 / (2 * kappa)) = 8 * Real.pi * G ↔ kappa = 2 * G := by
  have hlhs : 2 * Real.pi / (1 / (2 * kappa)) = 4 * Real.pi * kappa := by
    rw [one_div, div_eq_mul_inv, inv_inv]; ring
  rw [hlhs]
  constructor
  · intro h
    have h4pi : (4 * Real.pi) ≠ 0 := by positivity
    have heq : 4 * Real.pi * kappa = 4 * Real.pi * (2 * G) := by rw [h]; ring
    exact mul_left_cancel₀ h4pi heq
  · intro h; rw [h]; ring

/-- Area por face: sob `kappa = 2G`, `A_face = kappa/2 = G`. -/
theorem face_area_eq_G (kappa G : ℝ) (h : kappa = 2 * G) : kappa / 2 = G := by
  rw [h]; ring

/-- Sob `kappa = 2G`: `eta = (1/2)/(2G) = 1/(4G)`. -/
theorem halfNat_over_two_faces_eq_quarter (G : ℝ) :
    (1 / 2) / (2 * G) = 1 / (4 * G) := by
  rw [div_div]; congr 1; ring

end TGL.AreaScale
