-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_052 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.AperiodicCentralizerExpectation
import TGLExt.ExpectationAlgebra
import TGLExt.SitePauliObservables
import TGLExt.UnitaryStateDerivative

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

/-- The already constructed expectation agrees with local pinching by orthogonality. -/
theorem aperiodic_expectation_local (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (aperiodicExpectationInput P).E (towerPi P a) =
      towerPi P (specExpect (towerW P N) a) := by
  apply expectation_eq_of_ortho P (aperiodicExpectationInput P) _ _
    (towerPi_mem_factor a) (pinching_into_global_centralizer N a)
  intro B hB
  exact pinching_global_ortho N a B hB

/-- Pinching is the restriction of the constructed aperiodic expectation. -/
theorem aperiodic_pauli_x_zero (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    (aperiodicExpectationInput P).E (sitePauliX P 0) = 0 := by
  have h01 : P.w 0 ≠ 1 - P.w 0 := by intro h; apply hp; linarith
  have h10 : 1 - P.w 0 ≠ P.w 0 := Ne.symm h01
  change (aperiodicExpectationInput P).E (towerPi P (N := 0) pauliXMatrix) = 0
  rw [aperiodic_expectation_local]
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
  rw [aperiodic_expectation_local]
  have hpin : specExpect (towerW P 0) pauliYMatrix = 0 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [specExpect, towerW, siteW, pauliYMatrix, h01, h10]
  rw [hpin]
  exact (towerPiLinear P 0).map_zero

theorem pauli_horizontal_expectation (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2)
    (v : Fin 2 → ℝ) :
    (aperiodicExpectationInput P).E (pauliHorizontal P v) = 0 := by
  rw [pauliHorizontal, ChatgptAudit.Expectation047.expectation_add P (aperiodicExpectationInput P) _ _
    ((theFactorObject P).toStarSubalgebra.smul_mem (site_pauli_x_mem_factor P 0) _)
    ((theFactorObject P).toStarSubalgebra.smul_mem (site_pauli_y_mem_factor P 0) _),
    ChatgptAudit.Expectation047.expectation_smul P (aperiodicExpectationInput P) _ _ (site_pauli_x_mem_factor P 0),
    ChatgptAudit.Expectation047.expectation_smul P (aperiodicExpectationInput P) _ _ (site_pauli_y_mem_factor P 0),
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
  simpa only [RCLike.re_eq_complex_re, pow_two] using h

theorem pauli_x_gns_norm (P : SiteProfile) :
    ‖sitePauliX P 0 (hOmega P)‖ = 1 := by
  have h := pauli_horizontal_gns_norm_sq P ![1, 0]
  rw [pauli_horizontal_basis_x] at h
  norm_num at h
  rcases h with h | h
  · exact h
  · have hn := norm_nonneg (sitePauliX P 0 (hOmega P))
    linarith

theorem pauli_y_gns_norm (P : SiteProfile) :
    ‖sitePauliY P 0 (hOmega P)‖ = 1 := by
  have h := pauli_horizontal_gns_norm_sq P ![0, 1]
  rw [pauli_horizontal_basis_y] at h
  norm_num at h
  rcases h with h | h
  · exact h
  · have hn := norm_nonneg (sitePauliY P 0 (hOmega P))
    linarith

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
  convert (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd) using 1
  all_goals rfl

theorem horizontal_y_reading_derivative (P : SiteProfile) (v : Fin 2 → ℝ) :
    HasDerivAt (horizontalReading P v (sitePauliY P 0))
      (2 * (2 * P.w 0 - 1) * v 0) 0 := by
  have hd := orbit_expectation_first_derivative P (pauliHorizontal P v) 0
    (sitePauliY P 0) (pauli_horizontal_selfadjoint P v)
  rw [horizontal_y_commutator] at hd
  convert (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd) using 1
  all_goals rfl

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
  have hu : u 0 = v 0 := h1.resolve_right hr
  have hv : u 1 = v 1 := h0.resolve_right hr
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
  change (aperiodicExpectationInput P).E (towerPi P (N := 0) pauliXMatrix) =
    towerPi P (N := 0) pauliXMatrix
  rw [aperiodic_expectation_local]
  congr 1
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [specExpect, towerW, siteW, hp]

theorem aperiodic_pauli_y_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2) :
    (aperiodicExpectationInput P).E (sitePauliY P 0) = sitePauliY P 0 := by
  change (aperiodicExpectationInput P).E (towerPi P (N := 0) pauliYMatrix) =
    towerPi P (N := 0) pauliYMatrix
  rw [aperiodic_expectation_local]
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
#print axioms aperiodic_expectation_local
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
