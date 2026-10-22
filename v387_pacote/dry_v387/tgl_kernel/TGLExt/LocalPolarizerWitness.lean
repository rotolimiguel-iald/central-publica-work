-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_053 (06-07/09/2026), transposta em 07/09/2026
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
import TGLExt.TowerStatePolarizer
import TGLExt.LocalHorizontalPauli
import TGLExt.HorizontalAreaSelection

set_option autoImplicit false
set_option maxHeartbeats 2400000

namespace ChatgptAudit.Covariant053
open Matrix TGLExt ChatgptAudit ChatgptAudit.Thermal025
  ChatgptAudit.Observable035 ChatgptAudit.Orbit052 ChatgptAudit.Aperiodic046 ChatgptAudit.Density033
noncomputable section

/-- The local representative of the real state polarizer. -/
def localPolarizerMatrix (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  fun i j => Complex.I * (((towerW P N i - towerW P N j) /
    (towerW P N i + towerW P N j) : ℝ) : ℂ) * a i j

theorem local_polarizer_hermitian (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    (localPolarizerMatrix P N a).IsHermitian := by
  ext i j
  have hij : star (a j i) = a i j := congrFun (congrFun ha i) j
  have hr : (towerW P N j - towerW P N i) / (towerW P N j + towerW P N i) =
      -((towerW P N i - towerW P N j) / (towerW P N i + towerW P N j)) := by
    rw [add_comm (towerW P N j) (towerW P N i)]
    ring
  change star (Complex.I * (((towerW P N j - towerW P N i) /
      (towerW P N j + towerW P N i) : ℝ) : ℂ) * a j i) = _
  simp only [star_mul, Complex.star_def, Complex.conj_I, Complex.conj_ofReal]
  change star (a j i) * (_ * -Complex.I) = _
  rw [hij, hr]
  simp only [localPolarizerMatrix, Complex.ofReal_neg]
  ring

theorem local_polarizer_sylvester (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (diagonal fun i => (towerW P N i : ℂ)) * localPolarizerMatrix P N a +
      localPolarizerMatrix P N a * (diagonal fun i => (towerW P N i : ℂ)) =
    Complex.I • ((diagonal fun i => (towerW P N i : ℂ)) * a -
      a * (diagonal fun i => (towerW P N i : ℂ))) := by
  ext i j
  have hd : ((towerW P N i + towerW P N j : ℝ) : ℂ) ≠ 0 :=
    Complex.ofReal_ne_zero.mpr (ne_of_gt (add_pos (towerW_pos P N i) (towerW_pos P N j)))
  simp only [Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply, Matrix.diagonal_mul,
    Matrix.mul_diagonal, localPolarizerMatrix, smul_eq_mul]
  push_cast at hd ⊢
  field_simp [hd]

theorem local_state_star (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    star (tState P N a) = tState P N aᴴ := by
  have hd : (diagonal fun i => (towerW P N i : ℂ))ᴴ =
      diagonal fun i => (towerW P N i : ℂ) := by
    ext i j
    by_cases h : i = j
    · subst j
      simp [Matrix.diagonal]
    · simp [Matrix.diagonal, h, Ne.symm h]
  rw [tState_eq_trace, ← Matrix.trace_conjTranspose]
  rw [Matrix.conjTranspose_mul, hd, Matrix.trace_mul_comm, tState_eq_trace]

theorem local_polarizer_pairing (P : SiteProfile) (N : ℕ)
    (a x : Matrix (chainIdx N) (chainIdx N) ℂ)
    (ha : a.IsHermitian) (hx : x.IsHermitian) :
    (tState P N (x * localPolarizerMatrix P N a)).re = (tState P N (x * a)).im := by
  let rho : Matrix (chainIdx N) (chainIdx N) ℂ := diagonal fun i => (towerW P N i : ℂ)
  have hl (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
      (x * (rho * b)).trace = tState P N (b * x) := by
    rw [Matrix.trace_mul_comm x (rho * b), Matrix.mul_assoc, tState_eq_trace]
  have hr (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
      (x * (b * rho)).trace = tState P N (x * b) := by
    rw [← Matrix.mul_assoc, Matrix.trace_mul_comm (x * b) rho, tState_eq_trace]
  have h := congrArg (fun z : Matrix (chainIdx N) (chainIdx N) ℂ => (x * z).trace)
    (local_polarizer_sylvester P N a)
  change (x * (rho * localPolarizerMatrix P N a + localPolarizerMatrix P N a * rho)).trace =
    (x * (Complex.I • (rho * a - a * rho))).trace at h
  simp only [Matrix.mul_add, Matrix.mul_sub, Matrix.mul_smul, Matrix.trace_add,
    Matrix.trace_sub, Matrix.trace_smul, smul_eq_mul] at h
  rw [hl, hr, hl, hr] at h
  have hc (b : Matrix (chainIdx N) (chainIdx N) ℂ) (hb : b.IsHermitian) :
      tState P N (b * x) = star (tState P N (x * b)) := by
    rw [local_state_star, Matrix.conjTranspose_mul, hb, hx]
  rw [hc _ (local_polarizer_hermitian P N a ha), hc _ ha] at h
  have he := congrArg Complex.re h
  simp only [Complex.add_re, Complex.mul_re, Complex.I_re, Complex.I_im, zero_mul,
    one_mul, zero_sub, Complex.sub_im, Complex.star_def, Complex.conj_re,
    Complex.conj_im] at he
  linarith

theorem tower_local_selfadjoint (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    IsSelfAdjoint (towerPi P a) := by
  change star (towerPi P a) = towerPi P a
  rw [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, ha]

/-- Equality with the global operator is tested against every self-adjoint factor element. -/
theorem state_polarizer_local (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (ha : a.IsHermitian) :
    statePolarizer P (towerPi P a (hOmega P)) =
      towerPi P (localPolarizerMatrix P N a) (hOmega P) := by
  apply tower_polarizer_eq_of_pairing P (towerPi P a)
    (towerPi P (localPolarizerMatrix P N a))
    (towerPi_mem_factor a) (tower_local_selfadjoint P N a ha)
    (towerPi_mem_factor _) (tower_local_selfadjoint P N _ (local_polarizer_hermitian P N a ha))
  intro B hB hBsa
  rw [hBsa.star_eq, state_local_right, state_local_right]
  exact local_polarizer_pairing P N a (expectationMatrix P N B) ha
    (expectationMatrix_hermitian N B hB hBsa)
  all_goals assumption

theorem local_operator_pairing (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ (towerPi P a (hOmega P)) (towerPi P b (hOmega P)) =
      tState P N (aᴴ * b) := by
  have he := omega_product_inner (P := P) (star (towerPi P a)) (towerPi P b)
  rw [star_star] at he
  rw [← he, ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, ← towerPi_mul, omegaState_pi]

/-- The second test is the raw 00-to-11 flip, with GNS square norm 5/9. -/
def doubleFlipXMatrix : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  Matrix.single (0, 0) (1, 1) 1 + Matrix.single (1, 1) (0, 0) 1

def doubleFlipYMatrix : Matrix (chainIdx 1) (chainIdx 1) ℂ :=
  (-Complex.I) • Matrix.single (0, 0) (1, 1) 1 +
    Complex.I • Matrix.single (1, 1) (0, 0) 1

def doubleFlipX : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  towerPi thirdThermalReference doubleFlipXMatrix

def doubleFlipY : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  towerPi thirdThermalReference doubleFlipYMatrix

theorem double_flip_x_hermitian : doubleFlipXMatrix.IsHermitian := by
  ext ⟨i, j⟩ ⟨k, l⟩
  fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
    norm_num [doubleFlipXMatrix, Matrix.single_apply, Matrix.conjTranspose_apply]

theorem double_flip_y_hermitian : doubleFlipYMatrix.IsHermitian := by
  ext ⟨i, j⟩ ⟨k, l⟩
  fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
    norm_num [doubleFlipYMatrix, Matrix.single_apply, Matrix.conjTranspose_apply,
      Complex.star_def]

theorem double_flip_x_mem_factor : doubleFlipX ∈ theFactorObject thirdThermalReference :=
  towerPi_mem_factor doubleFlipXMatrix

theorem double_flip_y_mem_factor : doubleFlipY ∈ theFactorObject thirdThermalReference :=
  towerPi_mem_factor doubleFlipYMatrix

theorem double_flip_x_selfadjoint : IsSelfAdjoint doubleFlipX :=
  tower_local_selfadjoint _ _ _ double_flip_x_hermitian

theorem double_flip_y_selfadjoint : IsSelfAdjoint doubleFlipY :=
  tower_local_selfadjoint _ _ _ double_flip_y_hermitian

theorem local_real_smul_action (P : SiteProfile) (N : ℕ) (c : ℝ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P ((c : ℂ) • a) (hOmega P) = c • towerPi P a (hOmega P) := by
  change ((towerPiLinear P N) ((c : ℂ) • a)) (hOmega P) = _
  rw [map_smul]
  rfl

theorem first_pauli_polarizer_x :
    statePolarizer thirdThermalReference (sitePauliX thirdThermalReference 0 (hOmega _)) =
      (1 / 3 : ℝ) • sitePauliY thirdThermalReference 0 (hOmega _) := by
  change statePolarizer thirdThermalReference
    (towerPi thirdThermalReference (N := 0) pauliXMatrix (hOmega _)) = _
  rw [state_polarizer_local thirdThermalReference 0 pauliXMatrix pauli_x_conjTranspose]
  have hm : localPolarizerMatrix thirdThermalReference 0 pauliXMatrix =
      ((1 / 3 : ℝ) : ℂ) • pauliYMatrix := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [localPolarizerMatrix, towerW, siteW, thirdThermalReference,
        pauliXMatrix, pauliYMatrix, Complex.ext_iff, Complex.mul_re, Complex.mul_im]
  rw [hm]
  exact local_real_smul_action thirdThermalReference 0 (1 / 3) pauliYMatrix

theorem first_pauli_polarizer_y :
    statePolarizer thirdThermalReference (sitePauliY thirdThermalReference 0 (hOmega _)) =
      (-1 / 3 : ℝ) • sitePauliX thirdThermalReference 0 (hOmega _) := by
  change statePolarizer thirdThermalReference
    (towerPi thirdThermalReference (N := 0) pauliYMatrix (hOmega _)) = _
  rw [state_polarizer_local thirdThermalReference 0 pauliYMatrix pauli_y_conjTranspose]
  have hm : localPolarizerMatrix thirdThermalReference 0 pauliYMatrix =
      ((-1 / 3 : ℝ) : ℂ) • pauliXMatrix := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [localPolarizerMatrix, towerW, siteW, thirdThermalReference,
        pauliXMatrix, pauliYMatrix, Complex.ext_iff, Complex.mul_re, Complex.mul_im]
  rw [hm]
  exact local_real_smul_action thirdThermalReference 0 (-1 / 3) pauliXMatrix

theorem double_flip_polarizer_x :
    statePolarizer thirdThermalReference (doubleFlipX (hOmega _)) =
      (3 / 5 : ℝ) • doubleFlipY (hOmega _) := by
  rw [doubleFlipX, state_polarizer_local _ _ _ double_flip_x_hermitian]
  have hm : localPolarizerMatrix thirdThermalReference 1 doubleFlipXMatrix =
      ((3 / 5 : ℝ) : ℂ) • doubleFlipYMatrix := by
    ext ⟨i, j⟩ ⟨k, l⟩
    fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
      norm_num [localPolarizerMatrix, towerW, siteW, thirdThermalReference,
        doubleFlipXMatrix, doubleFlipYMatrix, Matrix.single_apply,
        Complex.ext_iff, Complex.mul_re, Complex.mul_im]
  rw [hm]
  exact local_real_smul_action thirdThermalReference 1 (3 / 5) doubleFlipYMatrix

theorem double_flip_polarizer_y :
    statePolarizer thirdThermalReference (doubleFlipY (hOmega _)) =
      (-3 / 5 : ℝ) • doubleFlipX (hOmega _) := by
  rw [doubleFlipY, state_polarizer_local _ _ _ double_flip_y_hermitian]
  have hm : localPolarizerMatrix thirdThermalReference 1 doubleFlipYMatrix =
      ((-3 / 5 : ℝ) : ℂ) • doubleFlipXMatrix := by
    ext ⟨i, j⟩ ⟨k, l⟩
    fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
      norm_num [localPolarizerMatrix, towerW, siteW, thirdThermalReference,
        doubleFlipXMatrix, doubleFlipYMatrix, Matrix.single_apply,
        Complex.ext_iff, Complex.mul_re, Complex.mul_im]
  rw [hm]
  exact local_real_smul_action thirdThermalReference 1 (-3 / 5) doubleFlipXMatrix

theorem double_flip_x_expectation :
    (aperiodicExpectationInput thirdThermalReference).E doubleFlipX = 0 := by
  rw [doubleFlipX, aperiodic_expectation_local]
  have hm : specExpect (towerW thirdThermalReference 1) doubleFlipXMatrix = 0 := by
    ext ⟨i, j⟩ ⟨k, l⟩
    fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
      norm_num [specExpect, towerW, siteW, thirdThermalReference,
        doubleFlipXMatrix, Matrix.single_apply]
  rw [hm]
  exact (towerPiLinear thirdThermalReference 1).map_zero

theorem double_flip_y_expectation :
    (aperiodicExpectationInput thirdThermalReference).E doubleFlipY = 0 := by
  rw [doubleFlipY, aperiodic_expectation_local]
  have hm : specExpect (towerW thirdThermalReference 1) doubleFlipYMatrix = 0 := by
    ext ⟨i, j⟩ ⟨k, l⟩
    fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l <;>
      norm_num [specExpect, towerW, siteW, thirdThermalReference,
        doubleFlipYMatrix, Matrix.single_apply]
  rw [hm]
  exact (towerPiLinear thirdThermalReference 1).map_zero

theorem double_flip_state_products :
    omegaState thirdThermalReference (doubleFlipX * doubleFlipX) = (5 / 9 : ℂ) ∧
    omegaState thirdThermalReference (doubleFlipY * doubleFlipY) = (5 / 9 : ℂ) ∧
    omegaState thirdThermalReference (doubleFlipX * doubleFlipY) = -Complex.I / 3 ∧
    omegaState thirdThermalReference (doubleFlipY * doubleFlipX) = Complex.I / 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    simp only [doubleFlipX, doubleFlipY, ← towerPi_mul, omegaState_pi] <;>
    norm_num [tState, towerW, siteW, thirdThermalReference, doubleFlipXMatrix,
      doubleFlipYMatrix, Matrix.mul_apply, Matrix.single_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, Complex.ext_iff,
      Complex.mul_re, Complex.mul_im]

theorem double_flip_real_gram :
    (inner ℂ (doubleFlipX (hOmega _)) (doubleFlipX (hOmega _))).re = 5 / 9 ∧
    (inner ℂ (doubleFlipY (hOmega _)) (doubleFlipY (hOmega _))).re = 5 / 9 ∧
    (inner ℂ (doubleFlipX (hOmega _)) (doubleFlipY (hOmega _))).re = 0 ∧
    (inner ℂ (doubleFlipY (hOmega _)) (doubleFlipX (hOmega _))).re = 0 := by
  rcases double_flip_state_products with ⟨hxx, hyy, hxy, hyx⟩
  rw [omega_product_inner, double_flip_x_selfadjoint.star_eq] at hxx hxy
  rw [omega_product_inner, double_flip_y_selfadjoint.star_eq] at hyy hyx
  rw [hxx, hyy, hxy, hyx]
  norm_num

theorem double_flip_norm_squares :
    ‖doubleFlipX (hOmega thirdThermalReference)‖ ^ 2 = 5 / 9 ∧
    ‖doubleFlipY (hOmega thirdThermalReference)‖ ^ 2 = 5 / 9 := by
  simpa only [norm_sq_eq_re_inner (𝕜 := ℂ), RCLike.re_eq_complex_re] using
    And.intro double_flip_real_gram.1 double_flip_real_gram.2.1

/-- Two parameters in actual unitary state curves, with fixed measured observables. -/
def doubleFlipHorizontal (u : Fin 2 → ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  (u 0 : ℂ) • doubleFlipX + (u 1 : ℂ) • doubleFlipY

theorem double_flip_horizontal_mem_factor (u : Fin 2 → ℝ) :
    doubleFlipHorizontal u ∈ theFactorObject thirdThermalReference :=
  add_mem
    ((theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem double_flip_x_mem_factor _)
    ((theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem double_flip_y_mem_factor _)

theorem double_flip_horizontal_selfadjoint (u : Fin 2 → ℝ) :
    IsSelfAdjoint (doubleFlipHorizontal u) := by
  change star (doubleFlipHorizontal u) = doubleFlipHorizontal u
  simp only [doubleFlipHorizontal, star_add, star_smul, Complex.star_def, Complex.conj_ofReal,
    double_flip_x_selfadjoint.star_eq, double_flip_y_selfadjoint.star_eq]

theorem double_flip_horizontal_expectation (u : Fin 2 → ℝ) :
    (aperiodicExpectationInput thirdThermalReference).E (doubleFlipHorizontal u) = 0 := by
  rw [doubleFlipHorizontal,
    ChatgptAudit.Expectation047.expectation_add _ _ _ _
      ((theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem double_flip_x_mem_factor _)
      ((theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem double_flip_y_mem_factor _),
    ChatgptAudit.Expectation047.expectation_smul _ _ _ _ double_flip_x_mem_factor,
    ChatgptAudit.Expectation047.expectation_smul _ _ _ _ double_flip_y_mem_factor,
    double_flip_x_expectation, double_flip_y_expectation, smul_zero, smul_zero, add_zero]

def doubleFlipReading (u : Fin 2 → ℝ)
    (B : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (t : ℝ) : ℝ := (orbitExpectation thirdThermalReference (doubleFlipHorizontal u) 0 B t 0).re

theorem double_flip_x_commutator (u : Fin 2 → ℝ) :
    Complex.I * omegaState thirdThermalReference
      (doubleFlipX * doubleFlipHorizontal u - doubleFlipHorizontal u * doubleFlipX) =
      ((2 * u 1 / 3 : ℝ) : ℂ) := by
  rcases double_flip_state_products with ⟨hxx, _, hxy, hyx⟩
  simp only [doubleFlipHorizontal, mul_add, add_mul, mul_smul_comm, smul_mul_assoc,
    omegaState_sub, omega_state_add, omega_state_smul, hxx, hxy, hyx]
  push_cast
  ring_nf
  simp only [Complex.I_sq]
  ring

theorem double_flip_y_commutator (u : Fin 2 → ℝ) :
    Complex.I * omegaState thirdThermalReference
      (doubleFlipY * doubleFlipHorizontal u - doubleFlipHorizontal u * doubleFlipY) =
      ((-2 * u 0 / 3 : ℝ) : ℂ) := by
  rcases double_flip_state_products with ⟨_, hyy, hxy, hyx⟩
  simp only [doubleFlipHorizontal, mul_add, add_mul, mul_smul_comm, smul_mul_assoc,
    omegaState_sub, omega_state_add, omega_state_smul, hyy, hxy, hyx]
  push_cast
  ring_nf
  simp only [Complex.I_sq]
  ring

theorem double_flip_x_reading_derivative (u : Fin 2 → ℝ) :
    HasDerivAt (doubleFlipReading u doubleFlipX) (2 * u 1 / 3) 0 := by
  have hd := orbit_expectation_first_derivative thirdThermalReference
    (doubleFlipHorizontal u) 0 doubleFlipX (double_flip_horizontal_selfadjoint u)
  rw [double_flip_x_commutator] at hd
  convert (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd) using 1
  all_goals rfl

theorem double_flip_y_reading_derivative (u : Fin 2 → ℝ) :
    HasDerivAt (doubleFlipReading u doubleFlipY) (-2 * u 0 / 3) 0 := by
  have hd := orbit_expectation_first_derivative thirdThermalReference
    (doubleFlipHorizontal u) 0 doubleFlipY (double_flip_horizontal_selfadjoint u)
  rw [double_flip_y_commutator] at hd
  convert (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd) using 1
  all_goals rfl

def doubleFlipResponse (u : Fin 2 → ℝ) : Fin 2 → ℝ :=
  ![deriv (doubleFlipReading u doubleFlipX) 0, deriv (doubleFlipReading u doubleFlipY) 0]

theorem double_flip_response_formula (u : Fin 2 → ℝ) :
    doubleFlipResponse u = ![2 * u 1 / 3, -2 * u 0 / 3] := by
  rw [doubleFlipResponse, (double_flip_x_reading_derivative u).deriv,
    (double_flip_y_reading_derivative u).deriv]

theorem double_flip_response_injective : Function.Injective doubleFlipResponse := by
  intro u v h
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  simp only [double_flip_response_formula, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
  funext i
  fin_cases i
  · change u 0 = v 0
    linarith
  · change u 1 = v 1
    linarith

/-- Zero response in all self-adjoint measurements forces a zero parameter direction. -/
theorem double_flip_effective_directions (u v : Fin 2 → ℝ)
    (h : ∀ B ∈ theFactorObject thirdThermalReference, IsSelfAdjoint B →
      deriv (doubleFlipReading u B) 0 = deriv (doubleFlipReading v B) 0) : u = v := by
  apply double_flip_response_injective
  have hx := h doubleFlipX double_flip_x_mem_factor double_flip_x_selfadjoint
  have hy := h doubleFlipY double_flip_y_mem_factor double_flip_y_selfadjoint
  simp only [doubleFlipResponse, hx, hy]

#print axioms localPolarizerMatrix
#print axioms local_polarizer_hermitian
#print axioms local_polarizer_sylvester
#print axioms local_state_star
#print axioms local_polarizer_pairing
#print axioms tower_local_selfadjoint
#print axioms state_polarizer_local
#print axioms local_operator_pairing
#print axioms doubleFlipXMatrix
#print axioms doubleFlipYMatrix
#print axioms doubleFlipX
#print axioms doubleFlipY
#print axioms double_flip_x_hermitian
#print axioms double_flip_y_hermitian
#print axioms double_flip_x_mem_factor
#print axioms double_flip_y_mem_factor
#print axioms double_flip_x_selfadjoint
#print axioms double_flip_y_selfadjoint
#print axioms local_real_smul_action
#print axioms first_pauli_polarizer_x
#print axioms first_pauli_polarizer_y
#print axioms double_flip_polarizer_x
#print axioms double_flip_polarizer_y
#print axioms double_flip_x_expectation
#print axioms double_flip_y_expectation
#print axioms double_flip_state_products
#print axioms double_flip_real_gram
#print axioms double_flip_norm_squares
#print axioms doubleFlipHorizontal
#print axioms double_flip_horizontal_mem_factor
#print axioms double_flip_horizontal_selfadjoint
#print axioms double_flip_horizontal_expectation
#print axioms doubleFlipReading
#print axioms double_flip_x_commutator
#print axioms double_flip_y_commutator
#print axioms double_flip_x_reading_derivative
#print axioms double_flip_y_reading_derivative
#print axioms doubleFlipResponse
#print axioms double_flip_response_formula
#print axioms double_flip_response_injective
#print axioms double_flip_effective_directions
end
end ChatgptAudit.Covariant053
