-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_051 (06-07/09/2026), transposta em 07/09/2026
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
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Optical051
open Matrix
noncomputable section

/-- A symmetric optical endomorphism in an orthonormal two-dimensional screen. -/
def opticalScreenMatrix (x z y : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![x, z; z, y]

def opticalScreenNormSq (x z y : ℝ) : ℝ := x ^ 2 + 2 * z ^ 2 + y ^ 2

/-- Half the squared norm of the trace-free part, in the convention used here. -/
def opticalShearNormSq (x z y : ℝ) : ℝ := ((x - y) / 2) ^ 2 + z ^ 2

/-- All three independent components of the symmetric matrix Riccati equation. -/
def opticalRiccatiSystem (x z y rxx rxy ryy : ℝ → ℝ) (t : ℝ) : Prop :=
  HasDerivAt x (-(x t ^ 2 + z t ^ 2) - rxx t) t ∧
  HasDerivAt z (-(x t * z t + z t * y t) - rxy t) t ∧
  HasDerivAt y (-(z t ^ 2 + y t ^ 2) - ryy t) t

theorem optical_screen_matrix_symmetric (x z y : ℝ) :
    (opticalScreenMatrix x z y).transpose = opticalScreenMatrix x z y := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem optical_screen_matrix_trace (x z y : ℝ) :
    Matrix.trace (opticalScreenMatrix x z y) = x + y := by
  simp [opticalScreenMatrix, Matrix.trace, Fin.sum_univ_two]

theorem optical_screen_matrix_square_trace (x z y : ℝ) :
    Matrix.trace (opticalScreenMatrix x z y * opticalScreenMatrix x z y) =
      opticalScreenNormSq x z y := by
  simp [opticalScreenMatrix, Matrix.trace, Fin.sum_univ_two,
    opticalScreenNormSq]
  ring

theorem optical_screen_raychaudhuri_decomposition (x z y : ℝ) :
    opticalScreenNormSq x z y = (x + y) ^ 2 / 2 + 2 * opticalShearNormSq x z y := by
  unfold opticalScreenNormSq opticalShearNormSq
  ring

theorem optical_screen_norm_nonneg (x z y : ℝ) : 0 ≤ opticalScreenNormSq x z y := by
  unfold opticalScreenNormSq
  positivity

theorem optical_screen_shear_nonneg (x z y : ℝ) : 0 ≤ opticalShearNormSq x z y := by
  unfold opticalShearNormSq
  positivity

theorem optical_screen_norm_eq_zero (x z y : ℝ) :
    opticalScreenNormSq x z y = 0 ↔ x = 0 ∧ z = 0 ∧ y = 0 := by
  constructor
  · intro h
    unfold opticalScreenNormSq at h
    have hx := sq_nonneg x
    have hz := sq_nonneg z
    have hy := sq_nonneg y
    have hx0 : x ^ 2 = 0 := by nlinarith
    have hz0 : z ^ 2 = 0 := by nlinarith
    have hy0 : y ^ 2 = 0 := by nlinarith
    exact ⟨sq_eq_zero_iff.mp hx0, sq_eq_zero_iff.mp hz0, sq_eq_zero_iff.mp hy0⟩
  · rintro ⟨rfl, rfl, rfl⟩
    norm_num [opticalScreenNormSq]

/-- Trace is unchanged by an orthonormal rotation of screen coordinates. -/
theorem optical_rotated_trace (x z y c s : ℝ) (hcs : c ^ 2 + s ^ 2 = 1) :
    (c ^ 2 * x + 2 * c * s * z + s ^ 2 * y) +
      (s ^ 2 * x - 2 * c * s * z + c ^ 2 * y) = x + y := by
  calc
    _ = (c ^ 2 + s ^ 2) * (x + y) := by ring
    _ = x + y := by rw [hcs, one_mul]

theorem optical_rotated_norm (x z y c s : ℝ) (hcs : c ^ 2 + s ^ 2 = 1) :
    opticalScreenNormSq
      (c ^ 2 * x + 2 * c * s * z + s ^ 2 * y)
      (c * s * (y - x) + (c ^ 2 - s ^ 2) * z)
      (s ^ 2 * x - 2 * c * s * z + c ^ 2 * y) =
      opticalScreenNormSq x z y := by
  calc
    _ = (c ^ 2 + s ^ 2) ^ 2 * opticalScreenNormSq x z y := by
      unfold opticalScreenNormSq
      ring
    _ = opticalScreenNormSq x z y := by rw [hcs]; ring

theorem optical_rotated_shear (x z y c s : ℝ) (hcs : c ^ 2 + s ^ 2 = 1) :
    opticalShearNormSq
      (c ^ 2 * x + 2 * c * s * z + s ^ 2 * y)
      (c * s * (y - x) + (c ^ 2 - s ^ 2) * z)
      (s ^ 2 * x - 2 * c * s * z + c ^ 2 * y) =
      opticalShearNormSq x z y := by
  have hn := optical_rotated_norm x z y c s hcs
  rw [optical_screen_raychaudhuri_decomposition,
    optical_screen_raychaudhuri_decomposition, optical_rotated_trace x z y c s hcs] at hn
  linarith

/-- Taking the trace of the optical Riccati system yields Raychaudhuri's ODE. -/
theorem optical_riccati_trace (x z y rxx rxy ryy : ℝ → ℝ) (t : ℝ)
    (h : opticalRiccatiSystem x z y rxx rxy ryy t) :
    HasDerivAt (fun u => x u + y u)
      (-(rxx t + ryy t) - opticalScreenNormSq (x t) (z t) (y t)) t := by
  convert h.1.add h.2.2 using 1
  all_goals first | rfl | (unfold opticalScreenNormSq; ring)

theorem optical_riccati_raychaudhuri (x z y rxx rxy ryy : ℝ → ℝ) (t : ℝ)
    (h : opticalRiccatiSystem x z y rxx rxy ryy t) :
    HasDerivAt (fun u => x u + y u)
      (-(rxx t + ryy t) - (x t + y t) ^ 2 / 2 -
        2 * opticalShearNormSq (x t) (z t) (y t)) t := by
  convert optical_riccati_trace x z y rxx rxy ryy t h using 1
  all_goals first | rfl | (rw [optical_screen_raychaudhuri_decomposition]; ring)

theorem optical_diagonal_distortion (x y : ℝ) :
    opticalScreenNormSq x 0 y = x ^ 2 + y ^ 2 := by
  simp [opticalScreenNormSq]

#print axioms opticalScreenMatrix
#print axioms opticalScreenNormSq
#print axioms opticalShearNormSq
#print axioms opticalRiccatiSystem
#print axioms optical_screen_matrix_symmetric
#print axioms optical_screen_matrix_trace
#print axioms optical_screen_matrix_square_trace
#print axioms optical_screen_raychaudhuri_decomposition
#print axioms optical_screen_norm_nonneg
#print axioms optical_screen_shear_nonneg
#print axioms optical_screen_norm_eq_zero
#print axioms optical_rotated_trace
#print axioms optical_rotated_norm
#print axioms optical_rotated_shear
#print axioms optical_riccati_trace
#print axioms optical_riccati_raychaudhuri
#print axioms optical_diagonal_distortion

end
end ChatgptAudit.Optical051
