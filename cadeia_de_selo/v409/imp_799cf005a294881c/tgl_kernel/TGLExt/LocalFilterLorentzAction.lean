-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_039 (06/09/2026), transposta em 06/09/2026
-- Lote 039..041 (ORDEM_008 cumprida: zero instancias anonimas; lote compilado junto em diretorio limpo).
--   039: CONE LOCAL E FILTRO — coordenadas de Herm2, produtos externos positivos singulares, rigidez
--   quadratica condicional, filtro e fase dos logaritmos locais (fatores, sinais, det, nao unitalidade),
--   reducao global ao bloco 0 (igualdade de operadores, compressao GNS). NAO pago: Delta^(it) como boost
--   sobre a tetrade (a obstrucao finita anterior segue). 040 (resposta a ORDEM_009): OBSTRUCAO PRECISA —
--   o fluxo modular do estado fixo nao percorre a curva de estados; o relogio de Fisher (lambda_F = 1/2 - 3k/16)
--   e toda inversa normalizada do relogio entropico (lambda_D = 1/2 - k/8) FALHAM no casamento quartico da
--   familia de um sitio (excedem lambda* = 1/2 - 9B2/(8 log2 B) - eta O/(2 log2 B)) embora preservem o
--   quadratico; o relogio afim da lambda = 0; a rede A(I) <= A(J) sse I <= J com representacao local fiel;
--   NEGATIVO: a area NAO e escalar so da algebra e do estado (dois protocolos de tangentes, duas densidades).
--   H3 (habitante) segue OPEN — o tipo canonico foi usado para PROVAR o negativo. 041: FLUXO DE CALOR efetivo
--   Q(t) = int_0^t -kappa u m A(u) du ligado por teorema a metrica/geodesica/waveMatter/Jacobi; a igualdade
--   FINITA exata Q = kappa eta (A-1)/(2 pi) FALHA (C/t^4 -> kappa eta (a^2+c^2)/(24 pi) > 0); a relacao
--   infinitesimal segue compativel. Estatuto [REAL / DERIVED / INPUT / OPEN]: familia especificada; area
--   fisica, EquilibriumScreenData compativel, materia/geometria/normalizacao e reconstrucao geral OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 16/16, 18/18, 8/8; 3/3 auditores exit 0;
--   recompilacao INDEPENDENTE 11/11, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.HermitianLocalCoordinates
import TGLExt.LikelihoodPreparedState

set_option autoImplicit false
set_option maxHeartbeats 5000000

namespace ChatgptAudit.Cone039
open Matrix TGLExt ChatgptAudit.Cocycle030 ChatgptAudit.Profile026
open scoped Matrix.Norms.Operator
noncomputable section

def localDiagonalLog (ell0 ell1 : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.diagonal ![(ell0 : ℂ), (ell1 : ℂ)]

def normalizedLocalFilter (ell0 ell1 : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.diagonal ![(Real.exp ((ell0-ell1)/4) : ℂ),
    (Real.exp (-((ell0-ell1)/4)) : ℂ)]

theorem local_diagonal_log_existing (p q : ℝ) :
    localDiagonalLog (Real.log q-Real.log p)
      (Real.log (1-q)-Real.log (1-p)) = matrixLogRatio (siteW p) (siteW q) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [localDiagonalLog, matrixLogRatio, siteW, Matrix.diagonal_apply]

theorem complex_half_real_exp (ell : ℝ) :
    NormedSpace.exp ((1/2 : ℂ)*(ell : ℂ)) = (Real.exp (ell/2) : ℂ) := by
  rw [← Complex.exp_eq_exp_ℂ]
  have he : (1/2 : ℂ)*(ell : ℂ) = ((ell/2 : ℝ) : ℂ) := by
    push_cast
    ring
  rw [he, ← Complex.ofReal_exp]

theorem local_diagonal_half_exp (ell0 ell1 : ℝ) :
    NormedSpace.exp ((1/2 : ℂ) • localDiagonalLog ell0 ell1) =
      Matrix.diagonal ![(Real.exp (ell0/2) : ℂ), (Real.exp (ell1/2) : ℂ)] := by
  unfold localDiagonalLog
  rw [← Matrix.diagonal_smul, Matrix.exp_diagonal]
  congr 1
  funext i
  simp only [Pi.coe_exp]
  fin_cases i
  · change NormedSpace.exp ((1/2 : ℂ)*(ell0 : ℂ)) = (Real.exp (ell0/2) : ℂ)
    exact complex_half_real_exp ell0
  · change NormedSpace.exp ((1/2 : ℂ)*(ell1 : ℂ)) = (Real.exp (ell1/2) : ℂ)
    exact complex_half_real_exp ell1

theorem normalized_local_filter_as_exponential (ell0 ell1 : ℝ) :
    normalizedLocalFilter ell0 ell1 =
      (Real.exp (-(ell0+ell1)/4) : ℂ) •
        NormedSpace.exp ((1/2 : ℂ) • localDiagonalLog ell0 ell1) := by
  have h0 : Real.exp ((ell0-ell1)/4) =
      Real.exp (-(ell0+ell1)/4)*Real.exp (ell0/2) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have h1 : Real.exp (-((ell0-ell1)/4)) =
      Real.exp (-(ell0+ell1)/4)*Real.exp (ell1/2) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [local_diagonal_half_exp]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [normalizedLocalFilter, h0, h1, Complex.ofReal_mul]

/-- The diagonal filter is the determinant normalization of the existing
    likelihood filter, not a replacement state preparation. -/
theorem normalized_local_filter_from_relative (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) :
    normalizedLocalFilter (Real.log q-Real.log p)
      (Real.log (1-q)-Real.log (1-p)) =
      (Real.exp (-((Real.log q-Real.log p)+
        (Real.log (1-q)-Real.log (1-p)))/4) : ℂ) •
          relativeFilter (siteW p) (siteW q) := by
  rw [normalized_local_filter_as_exponential, local_diagonal_log_existing,
    matrix_half_log_filter _ _ (siteW_pos hp0 hp1) (siteW_pos hq0 hq1)]

theorem pair_diagonal_congruence (a b : ℂ) (X : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix.diagonal ![a,b] * X * (Matrix.diagonal ![a,b])ᴴ =
      !![(a*star a)*X 0 0, (a*star b)*X 0 1;
        (b*star a)*X 1 0, (b*star b)*X 1 1] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem local_filter_exponential_products (ell0 ell1 : ℝ) :
    (Real.exp ((ell0-ell1)/4) : ℂ)*(Real.exp ((ell0-ell1)/4) : ℂ) =
        (Real.exp ((ell0-ell1)/2) : ℂ) ∧
    (Real.exp (-((ell0-ell1)/4)) : ℂ)*(Real.exp (-((ell0-ell1)/4)) : ℂ) =
        (Real.exp (-((ell0-ell1)/2)) : ℂ) ∧
    (Real.exp ((ell0-ell1)/4) : ℂ)*(Real.exp (-((ell0-ell1)/4)) : ℂ) = 1 := by
  have hp : Real.exp ((ell0-ell1)/4)*Real.exp ((ell0-ell1)/4) =
      Real.exp ((ell0-ell1)/2) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hm : Real.exp (-((ell0-ell1)/4))*Real.exp (-((ell0-ell1)/4)) =
      Real.exp (-((ell0-ell1)/2)) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hc : Real.exp ((ell0-ell1)/4)*Real.exp (-((ell0-ell1)/4)) = 1 := by
    rw [← Real.exp_add]
    simp
  exact ⟨by exact_mod_cast hp, by exact_mod_cast hm, by exact_mod_cast hc⟩

theorem normalized_local_filter_selfadjoint (ell0 ell1 : ℝ) :
    (normalizedLocalFilter ell0 ell1)ᴴ = normalizedLocalFilter ell0 ell1 := by
  ext i j
  fin_cases i <;> fin_cases j
  · change star (Real.exp ((ell0-ell1)/4) : ℂ) = (Real.exp ((ell0-ell1)/4) : ℂ)
    exact Complex.conj_ofReal _
  · change star (0 : ℂ) = 0
    simp
  · change star (0 : ℂ) = 0
    simp
  · change star (Real.exp (-((ell0-ell1)/4)) : ℂ) =
      (Real.exp (-((ell0-ell1)/4)) : ℂ)
    exact Complex.conj_ofReal _

theorem normalized_local_filter_det (ell0 ell1 : ℝ) :
    (normalizedLocalFilter ell0 ell1).det = 1 := by
  obtain ⟨_,_,hc⟩ := local_filter_exponential_products ell0 ell1
  simpa [normalizedLocalFilter, Matrix.det_fin_two] using hc

theorem normalized_local_filter_preserves_det (ell0 ell1 : ℝ)
    (X : Matrix (Fin 2) (Fin 2) ℂ) :
    (normalizedLocalFilter ell0 ell1 * X * (normalizedLocalFilter ell0 ell1)ᴴ).det =
      X.det := by
  simp only [Matrix.det_mul, Matrix.det_conjTranspose, normalized_local_filter_det,
    star_one, one_mul, mul_one]

/-- A congruence on local Hermitian matrices, with rapidity (ell0-ell1)/2.
    It is not an identification with a unitary modular action on Hilbert vectors. -/
theorem normalized_local_filter_boost (ell0 ell1 t x y z : ℝ) :
    normalizedLocalFilter ell0 ell1 * hermitianMatrix t x y z *
        (normalizedLocalFilter ell0 ell1)ᴴ =
      hermitianMatrix
        (Real.cosh ((ell0-ell1)/2)*t+Real.sinh ((ell0-ell1)/2)*z) x y
        (Real.sinh ((ell0-ell1)/2)*t+Real.cosh ((ell0-ell1)/2)*z) := by
  obtain ⟨hp,hm,hc⟩ := local_filter_exponential_products ell0 ell1
  have hcr : (Real.exp (-((ell0-ell1)/4)) : ℂ)*
      (Real.exp ((ell0-ell1)/4) : ℂ)=1 := by simpa only [mul_comm] using hc
  unfold normalizedLocalFilter
  rw [pair_diagonal_congruence]
  simp only [Complex.star_def, Complex.conj_ofReal, hp, hm, hc, hcr, one_mul]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [hermitianMatrix, Real.cosh_eq, Real.sinh_eq] <;> ring

theorem normalized_local_filter_identity (ell0 ell1 : ℝ) :
    normalizedLocalFilter ell0 ell1 * 1 * (normalizedLocalFilter ell0 ell1)ᴴ =
      Matrix.diagonal ![(Real.exp ((ell0-ell1)/2) : ℂ),
        (Real.exp (-((ell0-ell1)/2)) : ℂ)] := by
  have h := normalized_local_filter_boost ell0 ell1 1 0 0 0
  rw [hermitian_identity] at h
  simp only [mul_one, mul_zero, add_zero] at h
  rw [mul_one]
  rw [h]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [hermitianMatrix, Real.cosh_add_sinh, Real.cosh_sub_sinh]

theorem normalized_local_filter_not_unital (ell0 ell1 : ℝ)
    (hchi : (ell0-ell1)/2≠0) :
    normalizedLocalFilter ell0 ell1 * 1 * (normalizedLocalFilter ell0 ell1)ᴴ ≠ 1 := by
  intro h
  rw [normalized_local_filter_identity] at h
  have he := congrArg (fun X : Matrix (Fin 2) (Fin 2) ℂ => X 0 0) h
  change (Real.exp ((ell0-ell1)/2) : ℂ)=1 at he
  have hr : Real.exp ((ell0-ell1)/2)=1 := by exact_mod_cast he
  exact hchi ((Real.exp_eq_one_iff _).mp hr)

/-- The phase uses the same diagonal logarithm, before removing any scalar part. -/
def localPhase (ell0 ell1 theta : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.diagonal ![Complex.exp (((theta*ell0 : ℝ) : ℂ)*Complex.I),
    Complex.exp (((theta*ell1 : ℝ) : ℂ)*Complex.I)]

theorem complex_phase_real_exp (theta ell : ℝ) :
    NormedSpace.exp (((theta : ℂ)*Complex.I)*(ell : ℂ)) =
      Complex.exp (((theta*ell : ℝ) : ℂ)*Complex.I) := by
  rw [← Complex.exp_eq_exp_ℂ]
  congr 1
  push_cast
  ring

theorem local_phase_as_exponential (ell0 ell1 theta : ℝ) :
    localPhase ell0 ell1 theta =
      NormedSpace.exp (((theta : ℂ)*Complex.I) • localDiagonalLog ell0 ell1) := by
  unfold localDiagonalLog
  rw [← Matrix.diagonal_smul, Matrix.exp_diagonal]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [localPhase, Pi.coe_exp, smul_eq_mul, complex_phase_real_exp]

theorem local_phase_existing (p q theta : ℝ) :
    localPhase (Real.log q-Real.log p) (Real.log (1-q)-Real.log (1-p)) theta =
      NormedSpace.exp (((theta : ℂ)*Complex.I) •
        matrixLogRatio (siteW p) (siteW q)) := by
  rw [local_phase_as_exponential, local_diagonal_log_existing]

theorem complex_phase_product (a b : ℝ) :
    Complex.exp ((a : ℂ)*Complex.I)*star (Complex.exp ((b : ℂ)*Complex.I)) =
      Complex.exp (((a-b : ℝ) : ℂ)*Complex.I) := by
  simp only [Complex.star_def, ← Complex.exp_conj, map_mul,
    Complex.conj_ofReal, Complex.conj_I]
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

/-- Conjugation U X U* rotates (x,y) by minus theta*(ell0-ell1).
    The opposite conjugation has the opposite angle. -/
theorem local_phase_rotation (ell0 ell1 theta t x y z : ℝ) :
    localPhase ell0 ell1 theta * hermitianMatrix t x y z *
        (localPhase ell0 ell1 theta)ᴴ =
      hermitianMatrix t
        (Real.cos (theta*(ell0-ell1))*x+Real.sin (theta*(ell0-ell1))*y)
        (Real.cos (theta*(ell0-ell1))*y-Real.sin (theta*(ell0-ell1))*x) z := by
  have hd : theta*ell0-theta*ell1=theta*(ell0-ell1) := by ring
  have hn : theta*ell1-theta*ell0=-(theta*(ell0-ell1)) := by ring
  unfold localPhase
  rw [pair_diagonal_congruence]
  simp only [complex_phase_product, sub_self, Complex.ofReal_zero, zero_mul,
    Complex.exp_zero, one_mul]
  rw [hd, hn, Complex.exp_ofReal_mul_I, Complex.exp_ofReal_mul_I]
  ext i j
  fin_cases i <;> fin_cases j <;> apply Complex.ext <;>
    norm_num [hermitianMatrix, Real.cos_neg, Real.sin_neg,
      Complex.mul_re, Complex.mul_im] <;> ring

theorem local_phase_mul_adjoint (ell0 ell1 theta : ℝ) :
    localPhase ell0 ell1 theta * (localPhase ell0 ell1 theta)ᴴ = 1 := by
  have h := local_phase_rotation ell0 ell1 theta 1 0 0 0
  simpa only [hermitian_identity, mul_one, mul_zero, add_zero, sub_zero] using h

#print axioms localDiagonalLog
#print axioms normalizedLocalFilter
#print axioms local_diagonal_log_existing
#print axioms complex_half_real_exp
#print axioms local_diagonal_half_exp
#print axioms normalized_local_filter_as_exponential
#print axioms normalized_local_filter_from_relative
#print axioms pair_diagonal_congruence
#print axioms local_filter_exponential_products
#print axioms normalized_local_filter_selfadjoint
#print axioms normalized_local_filter_det
#print axioms normalized_local_filter_preserves_det
#print axioms normalized_local_filter_boost
#print axioms normalized_local_filter_identity
#print axioms normalized_local_filter_not_unital
#print axioms localPhase
#print axioms complex_phase_real_exp
#print axioms local_phase_as_exponential
#print axioms local_phase_existing
#print axioms complex_phase_product
#print axioms local_phase_rotation
#print axioms local_phase_mul_adjoint

end
end ChatgptAudit.Cone039
