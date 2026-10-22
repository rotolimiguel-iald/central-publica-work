-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_012 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.CovariantVectorCalculus
import Mathlib.Analysis.SpecialFunctions.Sqrt

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit
open Matrix
noncomputable section

abbrev ScreenMatrix := Matrix (Fin 2) (Fin 2) ℝ
abbrev ScreenVectors := Matrix (Fin 4) (Fin 2) ℝ

def HasMatrixDerivAt {m n : Type} (A : ℝ → Matrix m n ℝ)
    (dA : Matrix m n ℝ) (t : ℝ) : Prop :=
  ∀ i j, HasDerivAt (fun s => A s i j) (dA i j) t

def screenGram (g : Tensor4) (S : ScreenVectors) : ScreenMatrix := Sᵀ*g*S
def screenArea (h : ScreenMatrix) : ℝ := Real.sqrt h.det

def detTangent2 (h dh : ScreenMatrix) : ℝ :=
  dh 0 0*h 1 1+h 0 0*dh 1 1-(dh 0 1*h 1 0+h 0 1*dh 1 0)

theorem matrix_curve_deriv_transpose {m n : Type}
    (A : ℝ → Matrix m n ℝ) (dA : Matrix m n ℝ) (t : ℝ)
    (hA : HasMatrixDerivAt A dA t) :
    HasMatrixDerivAt (fun s => (A s)ᵀ) dAᵀ t := fun i j => hA j i

theorem matrix_curve_deriv_mul {m n l : Type} [Fintype n]
    (A : ℝ → Matrix m n ℝ) (B : ℝ → Matrix n l ℝ)
    (dA : Matrix m n ℝ) (dB : Matrix n l ℝ) (t : ℝ)
    (hA : HasMatrixDerivAt A dA t) (hB : HasMatrixDerivAt B dB t) :
    HasMatrixDerivAt (fun s => A s*B s) (dA*B t+A t*dB) t := by
  intro i j
  have he : (fun s => (A s*B s) i j)=∑ k, (fun s => A s i k)*(fun s => B s k j) := by
    funext s
    simp [Matrix.mul_apply]
  rw [he]
  simpa only [Matrix.mul_apply,Matrix.add_apply,Finset.sum_add_distrib] using
    HasDerivAt.sum (u := Finset.univ) (fun k _ => (hA i k).mul (hB k j))

theorem screen_gram_derivative (g : ℝ → Tensor4) (S : ℝ → ScreenVectors)
    (dg : Tensor4) (dS : ScreenVectors) (t : ℝ)
    (hg : HasMatrixDerivAt g dg t) (hS : HasMatrixDerivAt S dS t) :
    HasMatrixDerivAt (fun s => screenGram (g s) (S s))
      ((dSᵀ*g t+(S t)ᵀ*dg)*S t+((S t)ᵀ*g t)*dS) t := by
  exact matrix_curve_deriv_mul _ S _ dS t
    (matrix_curve_deriv_mul _ g _ dg t (matrix_curve_deriv_transpose S dS t hS) hg) hS

theorem determinant_curve_derivative (h : ℝ → ScreenMatrix) (dh : ScreenMatrix) (t : ℝ)
    (hh : HasMatrixDerivAt h dh t) :
    HasDerivAt (fun s => (h s).det) (detTangent2 (h t) dh) t := by
  have he : (fun s => (h s).det)=
      (fun s => h s 0 0)*(fun s => h s 1 1)-(fun s => h s 0 1)*(fun s => h s 1 0) := by
    funext s
    exact Matrix.det_fin_two (h s)
  rw [he]
  exact ((hh 0 0).mul (hh 1 1)).sub ((hh 0 1).mul (hh 1 0))

theorem determinant_congruence_tangent (h b : ScreenMatrix) :
    detTangent2 h (bᵀ*h+h*b)=2*Matrix.trace b*h.det := by
  simp [detTangent2,Matrix.det_fin_two,Matrix.mul_apply,Fin.sum_univ_two,
    Matrix.trace,Matrix.diag]
  ring

theorem screen_area_positive (h : ScreenMatrix) (hp : 0<h.det) : 0<screenArea h :=
  Real.sqrt_pos.2 hp

theorem screen_area_squared (h : ScreenMatrix) (hp : 0≤h.det) :
    (screenArea h)^2=h.det := Real.sq_sqrt hp

theorem screen_area_derivative (h : ℝ → ScreenMatrix) (b : ScreenMatrix) (t : ℝ)
    (hp : 0<(h t).det)
    (hh : HasMatrixDerivAt h (bᵀ*h t+h t*b) t) :
    HasDerivAt (fun s => screenArea (h s)) (Matrix.trace b*screenArea (h t)) t := by
  have hd := determinant_curve_derivative h _ t hh
  rw [determinant_congruence_tangent] at hd
  have ha := hd.sqrt (ne_of_gt hp)
  have hr : Real.sqrt (h t).det≠0 := ne_of_gt (Real.sqrt_pos.2 hp)
  have he : (2*Matrix.trace b*(h t).det)/(2*Real.sqrt (h t).det)=
      Matrix.trace b*Real.sqrt (h t).det := by
    apply (div_eq_iff (mul_ne_zero (by norm_num) hr)).2
    calc
      _=2*Matrix.trace b*(Real.sqrt (h t).det)^2 := by rw [Real.sq_sqrt hp.le]
      _=_ := by ring
  rw [he] at ha
  exact ha

#print axioms matrix_curve_deriv_transpose
#print axioms matrix_curve_deriv_mul
#print axioms screen_gram_derivative
#print axioms determinant_curve_derivative
#print axioms determinant_congruence_tangent
#print axioms screen_area_positive
#print axioms screen_area_squared
#print axioms screen_area_derivative
end
end ChatgptAudit
