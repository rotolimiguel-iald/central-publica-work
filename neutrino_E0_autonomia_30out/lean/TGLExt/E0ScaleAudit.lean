import Mathlib

set_option autoImplicit false

/-!
# Auditoria algébrica das escalas de E0

Este módulo prova somente identidades algébricas. Não fixa nem deriva uma
unidade absoluta em eV, não compara escalas com um alvo experimental e não
promove as escolhas condicionais de normalização a resultados físicos.
-/

namespace TGLExt.E0ScaleAudit

noncomputable section

/-- Energia de Hartree na forma alpha² m_e c²; `mec2` já representa m_e c². -/
def hartree (alpha mec2 : ℝ) : ℝ :=
  alpha ^ 2 * mec2

/-- Energia de Rydberg, metade da energia de Hartree. -/
def rydberg (alpha mec2 : ℝ) : ℝ :=
  hartree alpha mec2 / 2

/-- [ALGEBRA] Hartree = 2 Rydberg. -/
theorem hartree_eq_two_mul_rydberg (alpha mec2 : ℝ) :
    hartree alpha mec2 = 2 * rydberg alpha mec2 := by
  unfold rydberg hartree
  ring

/-- Energia Coulombiana alpha hbar c/r. -/
def coulombEnergy (alpha hbar c r : ℝ) : ℝ :=
  alpha * hbar * c / r

/-- Raio de Bohr, a0 = hbar/(alpha m_e c). -/
def bohrRadius (alpha hbar c m_e : ℝ) : ℝ :=
  hbar / (alpha * m_e * c)

/-- Energia de repouso do elétron, m_e c². -/
def electronRestEnergy (c m_e : ℝ) : ℝ :=
  m_e * c ^ 2

/-- [ALGEBRA] A energia Coulombiana em a0 é alpha² m_e c². -/
theorem coulomb_at_a0_eq_alpha_sq_mec2
    (alpha hbar c m_e : ℝ)
    (halpha : alpha ≠ 0) (hhbar : hbar ≠ 0)
    (hc : c ≠ 0) (hm_e : m_e ≠ 0) :
    coulombEnergy alpha hbar c (bohrRadius alpha hbar c m_e) =
      alpha ^ 2 * electronRestEnergy c m_e := by
  unfold coulombEnergy bohrRadius electronRestEnergy
  field_simp [halpha, hhbar, hc, hm_e]

/-- [ALGEBRA] Descer meia-Nat depois de multiplicar por exp(1/2) devolve U. -/
theorem semitone_exp_roundtrip (U : ℝ) :
    Real.exp (-(1 / 2 : ℝ)) * (Real.exp (1 / 2 : ℝ) * U) = U := by
  rw [← mul_assoc, ← Real.exp_add]
  norm_num

/-- Carga de comprimento do monopolo, q = c tau/(4 pi). -/
def monopoleCharge (c tau : ℝ) : ℝ :=
  c * tau / (4 * Real.pi)

/-- Raio de Schwarzschild associado, r_s = 2q. -/
def schwarzschildRadius (q : ℝ) : ℝ :=
  2 * q

/-- [ALGEBRA CONDICIONAL] Com r_s = 2q e q = c tau/(4 pi),
    tau = 2 pi r_s/c. A hipótese de forma não fixa o valor de tau. -/
theorem monopole_time_eq_two_pi_rs_div_c
    (c tau r_s : ℝ) (hc : c ≠ 0)
    (hr_s : r_s = schwarzschildRadius (monopoleCharge c tau)) :
    tau = 2 * Real.pi * r_s / c := by
  rw [hr_s]
  unfold schwarzschildRadius monopoleCharge
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  field_simp [hc, hpi] ; ring

end
end TGLExt.E0ScaleAudit

#print axioms TGLExt.E0ScaleAudit.hartree_eq_two_mul_rydberg
#print axioms TGLExt.E0ScaleAudit.coulomb_at_a0_eq_alpha_sq_mec2
#print axioms TGLExt.E0ScaleAudit.semitone_exp_roundtrip
#print axioms TGLExt.E0ScaleAudit.monopole_time_eq_two_pi_rs_div_c
