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
import TGLExt.SitePauliObservables
import TGLExt.TheModularFlowIsAHorizon
import Mathlib.Data.Real.Sign
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Orbit052
open TGLExt ChatgptAudit ChatgptAudit.Observable035 Matrix
noncomputable section

def firstSiteModularGap (P : SiteProfile) : ℝ :=
  Real.log (P.w 0) - Real.log (1 - P.w 0)

def modularQuarterTurnTime (P : SiteProfile) : ℝ :=
  -Real.pi / (2 * firstSiteModularGap P)

def modularOrientedQuarterTime (P : SiteProfile) : ℝ :=
  -Real.pi / (2 * |firstSiteModularGap P|)

theorem first_site_modular_gap_ne_zero (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    firstSiteModularGap P ≠ 0 := by
  intro h
  have he := Real.log_injOn_pos (P.pos 0)
    (show 0 < 1 - P.w 0 by linarith [P.lt_one 0])
    (sub_eq_zero.mp h)
  apply hp
  linarith

theorem first_site_modular_gap_pos_iff (P : SiteProfile) :
    0 < firstSiteModularGap P ↔ 0 < 2 * P.w 0 - 1 := by
  rw [firstSiteModularGap, sub_pos,
    Real.log_lt_log_iff (show 0 < 1 - P.w 0 by linarith [P.lt_one 0]) (P.pos 0)]
  constructor <;> intro h <;> linarith

theorem first_site_modular_gap_neg_iff (P : SiteProfile) :
    firstSiteModularGap P < 0 ↔ 2 * P.w 0 - 1 < 0 := by
  rw [firstSiteModularGap, sub_neg,
    Real.log_lt_log_iff (P.pos 0) (show 0 < 1 - P.w 0 by linarith [P.lt_one 0])]
  constructor <;> intro h <;> linarith

theorem first_site_modular_gap_sign (P : SiteProfile) :
    Real.sign (firstSiteModularGap P) = Real.sign (2 * P.w 0 - 1) := by
  rcases lt_trichotomy (firstSiteModularGap P) 0 with h | h | h
  · rw [Real.sign_of_neg h,
      Real.sign_of_neg ((first_site_modular_gap_neg_iff P).mp h)]
  · have hr : 2 * P.w 0 - 1 = 0 := by
      by_contra hr
      rcases lt_or_gt_of_ne hr with hn | hp
      · have hg := (first_site_modular_gap_neg_iff P).mpr hn
        linarith
      · have hg := (first_site_modular_gap_pos_iff P).mpr hp
        linarith
    rw [h, hr]
  · rw [Real.sign_of_pos h,
      Real.sign_of_pos ((first_site_modular_gap_pos_iff P).mp h)]

theorem modular_phase_trigonometric (t r : ℝ) :
    modularPhase t r =
      (Real.cos (t * r) : ℂ) + (Real.sin (t * r) : ℂ) * Complex.I := by
  simp only [modularPhase, Complex.exp_mul_I, Complex.ofReal_cos, Complex.ofReal_sin]

theorem first_site_flow_x (P : SiteProfile) (t : ℝ) :
    flowLevel P t 0 pauliXMatrix =
      (Real.cos (t * firstSiteModularGap P) : ℂ) • pauliXMatrix -
      (Real.sin (t * firstSiteModularGap P) : ℂ) • pauliYMatrix := by
  have hgap : Real.log (P.w 0) - Real.log (1 - P.w 0) =
      firstSiteModularGap P := rfl
  have hneg : Real.log (1 - P.w 0) - Real.log (P.w 0) =
      -(firstSiteModularGap P) := by
    unfold firstSiteModularGap
    ring
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flowLevel, towerW, siteW, pauliXMatrix, pauliYMatrix,
      modular_phase_trigonometric, hgap, hneg, mul_neg]
  ring

theorem first_site_flow_y (P : SiteProfile) (t : ℝ) :
    flowLevel P t 0 pauliYMatrix =
      (Real.sin (t * firstSiteModularGap P) : ℂ) • pauliXMatrix +
      (Real.cos (t * firstSiteModularGap P) : ℂ) • pauliYMatrix := by
  have hgap : Real.log (P.w 0) - Real.log (1 - P.w 0) =
      firstSiteModularGap P := rfl
  have hneg : Real.log (1 - P.w 0) - Real.log (P.w 0) =
      -(firstSiteModularGap P) := by
    unfold firstSiteModularGap
    ring
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [flowLevel, towerW, siteW, pauliXMatrix, pauliYMatrix,
      modular_phase_trigonometric, hgap, hneg, mul_neg] <;>
    ring_nf <;> simp [Complex.I_sq]

theorem modular_horizon_pauli_x (P : SiteProfile) (t : ℝ) :
    adT (modularHorizon P t) (sitePauliX P 0) =
      (Real.cos (t * firstSiteModularGap P) : ℂ) • sitePauliX P 0 -
      (Real.sin (t * firstSiteModularGap P) : ℂ) • sitePauliY P 0 := by
  rw [adT_modularHorizon]
  change modularConjugation P t (towerPi P (N := 0) pauliXMatrix) = _
  rw [modularConjugation_local, first_site_flow_x]
  change (towerPiLinear P 0) (_ - _) = _
  rw [map_sub, map_smul, map_smul]
  rfl

theorem modular_horizon_pauli_y (P : SiteProfile) (t : ℝ) :
    adT (modularHorizon P t) (sitePauliY P 0) =
      (Real.sin (t * firstSiteModularGap P) : ℂ) • sitePauliX P 0 +
      (Real.cos (t * firstSiteModularGap P) : ℂ) • sitePauliY P 0 := by
  rw [adT_modularHorizon]
  change modularConjugation P t (towerPi P (N := 0) pauliYMatrix) = _
  rw [modularConjugation_local, first_site_flow_y, towerPi_add, towerPi_smul,
    towerPi_smul]
  rfl

theorem modular_quarter_turn_angle (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    modularQuarterTurnTime P * firstSiteModularGap P = -(Real.pi / 2) := by
  unfold modularQuarterTurnTime
  field_simp [first_site_modular_gap_ne_zero P hp]

theorem modular_quarter_horizon_x (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularQuarterTurnTime P)) (sitePauliX P 0) =
      sitePauliY P 0 := by
  rw [modular_horizon_pauli_x, modular_quarter_turn_angle P hp]
  simp

theorem modular_quarter_horizon_y (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularQuarterTurnTime P)) (sitePauliY P 0) =
      -sitePauliX P 0 := by
  rw [modular_horizon_pauli_y, modular_quarter_turn_angle P hp]
  simp

theorem modular_oriented_quarter_time_neg (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    modularOrientedQuarterTime P < 0 := by
  exact div_neg_of_neg_of_pos (neg_lt_zero.mpr Real.pi_pos)
    (mul_pos (by norm_num) (abs_pos.mpr (first_site_modular_gap_ne_zero P hp)))

theorem modular_oriented_angle_of_pos (P : SiteProfile)
    (h : 0 < firstSiteModularGap P) :
    modularOrientedQuarterTime P * firstSiteModularGap P = -(Real.pi / 2) := by
  unfold modularOrientedQuarterTime
  rw [abs_of_pos h]
  field_simp [ne_of_gt h]

theorem modular_oriented_angle_of_neg (P : SiteProfile)
    (h : firstSiteModularGap P < 0) :
    modularOrientedQuarterTime P * firstSiteModularGap P = Real.pi / 2 := by
  unfold modularOrientedQuarterTime
  rw [abs_of_neg h]
  field_simp [ne_of_lt h]

theorem modular_oriented_horizon_x (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularOrientedQuarterTime P)) (sitePauliX P 0) =
      (Real.sign (2 * P.w 0 - 1) : ℂ) • sitePauliY P 0 := by
  rw [modular_horizon_pauli_x]
  rcases lt_or_gt_of_ne (first_site_modular_gap_ne_zero P hp) with hn | hp
  · rw [modular_oriented_angle_of_neg P hn,
      Real.sign_of_neg ((first_site_modular_gap_neg_iff P).mp hn)]
    simp
  · rw [modular_oriented_angle_of_pos P hp,
      Real.sign_of_pos ((first_site_modular_gap_pos_iff P).mp hp)]
    simp

theorem modular_oriented_horizon_y (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    adT (modularHorizon P (modularOrientedQuarterTime P)) (sitePauliY P 0) =
      (-Real.sign (2 * P.w 0 - 1) : ℂ) • sitePauliX P 0 := by
  rw [modular_horizon_pauli_y]
  rcases lt_or_gt_of_ne (first_site_modular_gap_ne_zero P hp) with hn | hp
  · rw [modular_oriented_angle_of_neg P hn,
      Real.sign_of_neg ((first_site_modular_gap_neg_iff P).mp hn)]
    simp
  · rw [modular_oriented_angle_of_pos P hp,
      Real.sign_of_pos ((first_site_modular_gap_pos_iff P).mp hp)]
    simp

theorem first_site_modular_gap_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2) :
    firstSiteModularGap P = 0 := by
  norm_num [firstSiteModularGap, hp]

theorem modular_horizon_pauli_x_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2)
    (t : ℝ) :
    adT (modularHorizon P t) (sitePauliX P 0) = sitePauliX P 0 := by
  rw [modular_horizon_pauli_x, first_site_modular_gap_tracial P hp]
  simp

theorem modular_horizon_pauli_y_tracial (P : SiteProfile) (hp : P.w 0 = 1 / 2)
    (t : ℝ) :
    adT (modularHorizon P t) (sitePauliY P 0) = sitePauliY P 0 := by
  rw [modular_horizon_pauli_y, first_site_modular_gap_tracial P hp]
  simp

#print axioms firstSiteModularGap
#print axioms modularQuarterTurnTime
#print axioms modularOrientedQuarterTime
#print axioms first_site_modular_gap_ne_zero
#print axioms first_site_modular_gap_pos_iff
#print axioms first_site_modular_gap_neg_iff
#print axioms first_site_modular_gap_sign
#print axioms modular_phase_trigonometric
#print axioms first_site_flow_x
#print axioms first_site_flow_y
#print axioms modular_horizon_pauli_x
#print axioms modular_horizon_pauli_y
#print axioms modular_quarter_turn_angle
#print axioms modular_quarter_horizon_x
#print axioms modular_quarter_horizon_y
#print axioms modular_oriented_quarter_time_neg
#print axioms modular_oriented_angle_of_pos
#print axioms modular_oriented_angle_of_neg
#print axioms modular_oriented_horizon_x
#print axioms modular_oriented_horizon_y
#print axioms first_site_modular_gap_tracial
#print axioms modular_horizon_pauli_x_tracial
#print axioms modular_horizon_pauli_y_tracial

end
end ChatgptAudit.Orbit052
