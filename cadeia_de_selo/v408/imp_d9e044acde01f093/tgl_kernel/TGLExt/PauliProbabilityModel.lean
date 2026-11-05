-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_035 (06/09/2026), transposta em 06/09/2026
-- Lote 035..037 (processo da ORDEM_008 cumprido pela bancada: zero instancias anonimas, lote compilado junto
--   num diretorio limpo). 035: DEFORMACOES OBSERVAVEIS e AREA DE FISHER — derivadas da conjugacao unitaria e
--   do estado, observaveis de Pauli por sitio na torre real, duas leituras independentes (jacobiano nao
--   degenerado), medicao conjunta efetiva (sitios distintos), probabilidades normalizadas e suas derivadas,
--   matriz de Fisher na origem, densidade de area de Fisher (4/9 como area de coordenadas). 036: AREA OPTICA e
--   LIBERDADE RADIATIVA — a area induzida dos campos de Jacobi da metrica 029 ligada a curvatura real
--   (A2(0) = -Ric(d,d); A4(0) = 2(tr K)^2 - 2 tr(K_TF^T K_TF)); germes de area distintos para shears
--   distintos. 037: QUARTA ORDEM, AREA e RELOGIO — limites entropicos e de area em 4a ordem; NEGATIVO
--   MEDIDO: o casamento adicional em 4a ordem com parametro comum fixo FALHA (delta4 >= (7/48) B > 0);
--   a reparametrizacao do relogio t + lambda t^3 cancela o defeito ate 4a ordem (controle do relogio relativo).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: X, Y, sitios e normalizacao sao INPUT; a familia optica
--   lorentziana e INPUT; identificacao da inscricao angular com area fisica, retorno estabilizador, ponte
--   regiao-algebra, escala, assinatura, dinamica gravitacional e H3 geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 14/14, 8/8 (via manifesto), 10/10; manifestos
--   1051/977; 3/3 auditores exit 0; recompilacao INDEPENDENTE 15/15, axiomas no trio; guarda de colisao;
--   enunciados lidos. Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.UnitaryStateDerivative
import TGLExt.SitePauliObservables

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Observable035
open Matrix TGLExt ChatgptAudit ChatgptAudit.Density033
noncomputable section

def signOutcome (a : Fin 2) : ℝ := if a = 0 then 1 else -1

@[simp]
theorem sign_outcome_zero : signOutcome 0 = 1 := by norm_num [signOutcome]

@[simp]
theorem sign_outcome_one : signOutcome 1 = -1 := by norm_num [signOutcome]

theorem sign_outcome_square (a : Fin 2) : signOutcome a ^ 2 = 1 := by
  fin_cases a <;> norm_num [signOutcome]

theorem sign_outcome_sum : ∑ a : Fin 2, signOutcome a = 0 := by
  norm_num [Fin.sum_univ_two, signOutcome]

def pauliYProjectionMatrix (a : Fin 2) : Matrix (Fin 2) (Fin 2) ℂ :=
  (1 / 2 : ℂ) • (1 + (signOutcome a : ℂ) • pauliYMatrix)

def pauliYProjection (P : SiteProfile) (n : ℕ) (a : Fin 2) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  siteOperator P n (pauliYProjectionMatrix a)

def pauliJointEffect (P : SiteProfile) (n m : ℕ) (z : Fin 2 × Fin 2) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  pauliYProjection P n z.1 * pauliYProjection P m z.2

def pauliProbability (P : SiteProfile) (n m : ℕ) (z : Fin 2 × Fin 2) (s t : ℝ) : ℝ :=
  (orbitExpectation P (sitePauliX P n) (sitePauliX P m)
    (pauliJointEffect P n m z) s t).re

theorem pauli_y_matrix_square (a : Fin 2) :
    pauliYProjectionMatrix a * pauliYProjectionMatrix a = pauliYProjectionMatrix a := by
  fin_cases a <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [pauliYProjectionMatrix, signOutcome, pauliYMatrix,
      Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.add_apply, Matrix.one_apply, smul_eq_mul]
  all_goals ring_nf
  all_goals norm_num [Complex.I_sq]

theorem pauli_y_matrix_star (a : Fin 2) :
    (pauliYProjectionMatrix a)ᴴ = pauliYProjectionMatrix a := by
  fin_cases a <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [pauliYProjectionMatrix, signOutcome, pauliYMatrix,
      Matrix.conjTranspose_apply, Matrix.smul_apply,
      Matrix.add_apply, Matrix.one_apply, smul_eq_mul]

theorem pauli_y_matrix_orthogonal {a b : Fin 2} (h : a ≠ b) :
    pauliYProjectionMatrix a * pauliYProjectionMatrix b = 0 := by
  fin_cases a <;> fin_cases b
  all_goals first
    | exact (h rfl).elim
    | (ext i j; fin_cases i <;> fin_cases j <;>
        norm_num [pauliYProjectionMatrix, signOutcome, pauliYMatrix,
          Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
          Matrix.add_apply, Matrix.one_apply, Matrix.zero_apply, smul_eq_mul])
  all_goals ring_nf
  all_goals norm_num [Complex.I_sq]

theorem pauli_y_matrix_sum :
    ∑ a : Fin 2, pauliYProjectionMatrix a = 1 := by
  rw [Fin.sum_univ_two]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliYProjectionMatrix, signOutcome, pauliYMatrix,
      Matrix.smul_apply, Matrix.add_apply, Matrix.one_apply, smul_eq_mul]

theorem pauli_y_matrix_commutator (a : Fin 2) :
    Complex.I • (pauliYProjectionMatrix a * pauliXMatrix -
      pauliXMatrix * pauliYProjectionMatrix a) =
        (signOutcome a : ℂ) • pauliZMatrix := by
  fin_cases a <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [pauliYProjectionMatrix, signOutcome, pauliXMatrix, pauliYMatrix, pauliZMatrix,
      Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.add_apply, Matrix.sub_apply, Matrix.one_apply, smul_eq_mul]
  all_goals ring_nf
  all_goals norm_num [Complex.I_sq]

theorem pauli_y_projection_formula (P : SiteProfile) (n : ℕ) (a : Fin 2) :
    pauliYProjection P n a =
      (1 / 2 : ℂ) • (1 + (signOutcome a : ℂ) • sitePauliY P n) := by
  unfold pauliYProjection pauliYProjectionMatrix
  rw [site_operator_smul, site_operator_add, site_operator_one, site_operator_smul]
  rfl

theorem pauli_y_projection_isStarProjection (P : SiteProfile) (n : ℕ) (a : Fin 2) :
    IsStarProjection (pauliYProjection P n a) := by
  constructor
  · change siteOperator P n (pauliYProjectionMatrix a) *
      siteOperator P n (pauliYProjectionMatrix a) = siteOperator P n (pauliYProjectionMatrix a)
    rw [← siteOperator_mul, pauli_y_matrix_square]
  · change star (siteOperator P n (pauliYProjectionMatrix a)) =
      siteOperator P n (pauliYProjectionMatrix a)
    rw [← siteOperator_star, pauli_y_matrix_star]

theorem pauli_y_projection_mem_factor (P : SiteProfile) (n : ℕ) (a : Fin 2) :
    pauliYProjection P n a ∈ theFactorObject P :=
  siteOperator_mem_factor n (pauliYProjectionMatrix a)

theorem pauli_y_projection_orthogonal (P : SiteProfile) (n : ℕ)
    {a b : Fin 2} (h : a ≠ b) :
    pauliYProjection P n a * pauliYProjection P n b = 0 := by
  change siteOperator P n (pauliYProjectionMatrix a) *
    siteOperator P n (pauliYProjectionMatrix b) = 0
  rw [← siteOperator_mul, pauli_y_matrix_orthogonal h]
  exact (siteOperatorLinear P n).map_zero

theorem pauli_y_projection_sum (P : SiteProfile) (n : ℕ) :
    ∑ a : Fin 2, pauliYProjection P n a = 1 := by
  rw [Fin.sum_univ_two]
  change siteOperator P n (pauliYProjectionMatrix 0) +
    siteOperator P n (pauliYProjectionMatrix 1) = 1
  have hs : pauliYProjectionMatrix 0 + pauliYProjectionMatrix 1 = 1 := by
    simpa only [Fin.sum_univ_two] using pauli_y_matrix_sum
  rw [← site_operator_add, hs, site_operator_one]

theorem pauli_y_projection_state (P : SiteProfile) (n : ℕ) (a : Fin 2) :
    omegaState P (pauliYProjection P n a) = (1 / 2 : ℂ) := by
  change omegaState P (siteOperator P n (pauliYProjectionMatrix a)) = _
  rw [site_operator_state_diagonal]
  fin_cases a <;>
    norm_num [pauliYProjectionMatrix, signOutcome, pauliYMatrix,
      Matrix.smul_apply, Matrix.add_apply, Matrix.one_apply, smul_eq_mul] <;> ring

theorem pauli_y_projection_commute (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (a b : Fin 2) :
    Commute (pauliYProjection P n a) (pauliYProjection P m b) :=
  siteOperators_commute h (pauliYProjectionMatrix a) (pauliYProjectionMatrix b)

theorem pauli_y_projection_x_commute (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (a : Fin 2) : Commute (pauliYProjection P n a) (sitePauliX P m) :=
  siteOperators_commute h (pauliYProjectionMatrix a) pauliXMatrix

theorem pauli_y_projection_commutator (P : SiteProfile) (n : ℕ) (a : Fin 2) :
    Complex.I • (pauliYProjection P n a * sitePauliX P n -
      sitePauliX P n * pauliYProjection P n a) =
        (signOutcome a : ℂ) • sitePauliZ P n := by
  change Complex.I • (siteOperator P n (pauliYProjectionMatrix a) *
    siteOperator P n pauliXMatrix -
    siteOperator P n pauliXMatrix * siteOperator P n (pauliYProjectionMatrix a)) =
      (signOutcome a : ℂ) • siteOperator P n pauliZMatrix
  rw [← siteOperator_mul, ← siteOperator_mul, ← site_operator_sub,
    ← site_operator_smul, pauli_y_matrix_commutator, site_operator_smul]

theorem pauli_y_projection_response (P : SiteProfile) (n : ℕ) (a : Fin 2) :
    Complex.I * omegaState P (pauliYProjection P n a * sitePauliX P n -
      sitePauliX P n * pauliYProjection P n a) =
        ((signOutcome a * (2 * P.w n - 1) : ℝ) : ℂ) := by
  rw [← omega_state_smul, pauli_y_projection_commutator,
    omega_state_smul, site_pauli_z_state]
  push_cast; ring

theorem pauli_joint_effect_isStarProjection (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) : IsStarProjection (pauliJointEffect P n m z) :=
  (pauli_y_projection_isStarProjection P n z.1).mul
    (pauli_y_projection_isStarProjection P m z.2) (pauli_y_projection_commute P h z.1 z.2)

theorem pauli_joint_effect_mem_factor (P : SiteProfile) (n m : ℕ)
    (z : Fin 2 × Fin 2) : pauliJointEffect P n m z ∈ theFactorObject P :=
  (theFactorObject P).mul_mem (pauli_y_projection_mem_factor P n z.1)
    (pauli_y_projection_mem_factor P m z.2)

theorem pauli_joint_effect_positive (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) : (pauliJointEffect P n m z).IsPositive :=
  ContinuousLinearMap.IsPositive.of_isStarProjection (pauli_joint_effect_isStarProjection P h z)

theorem pauli_joint_effect_swap (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) : pauliJointEffect P n m z = pauliJointEffect P m n (z.2, z.1) :=
  (pauli_y_projection_commute P h z.1 z.2).eq

theorem pauli_joint_effect_product (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z w : Fin 2 × Fin 2) :
    pauliJointEffect P n m z * pauliJointEffect P n m w =
      (pauliYProjection P n z.1 * pauliYProjection P n w.1) *
        (pauliYProjection P m z.2 * pauliYProjection P m w.2) := by
  unfold pauliJointEffect
  calc
    (pauliYProjection P n z.1 * pauliYProjection P m z.2) *
        (pauliYProjection P n w.1 * pauliYProjection P m w.2) =
      pauliYProjection P n z.1 *
        (pauliYProjection P m z.2 * pauliYProjection P n w.1) *
          pauliYProjection P m w.2 := by simp only [mul_assoc]
    _ = pauliYProjection P n z.1 *
        (pauliYProjection P n w.1 * pauliYProjection P m z.2) *
          pauliYProjection P m w.2 := by
      rw [(pauli_y_projection_commute P h.symm z.2 w.1).eq]
    _ = _ := by simp only [mul_assoc]

theorem pauli_joint_effect_orthogonal (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    {z w : Fin 2 × Fin 2} (hzw : z ≠ w) :
    pauliJointEffect P n m z * pauliJointEffect P n m w = 0 := by
  rw [pauli_joint_effect_product P h]
  by_cases hfirst : z.1 = w.1
  · have hsecond : z.2 ≠ w.2 := fun he => hzw (Prod.ext hfirst he)
    rw [pauli_y_projection_orthogonal P m hsecond, mul_zero]
  · rw [pauli_y_projection_orthogonal P n hfirst, zero_mul]

theorem pauli_joint_effect_sum (P : SiteProfile) (n m : ℕ) :
    ∑ z : Fin 2 × Fin 2, pauliJointEffect P n m z = 1 := by
  calc
    (∑ z : Fin 2 × Fin 2, pauliJointEffect P n m z) =
        ∑ a : Fin 2, ∑ b : Fin 2, pauliYProjection P n a * pauliYProjection P m b := by
      rw [Fintype.sum_prod_type]
      rfl
    _ = ∑ a : Fin 2, pauliYProjection P n a := by
      apply Finset.sum_congr rfl
      intro a _
      rw [← Finset.mul_sum, pauli_y_projection_sum, mul_one]
    _ = 1 := pauli_y_projection_sum P n

theorem pauli_joint_effect_state (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) : omegaState P (pauliJointEffect P n m z) = (1 / 4 : ℂ) := by
  calc
    omegaState P (pauliJointEffect P n m z) =
        omegaState P (pauliYProjection P n z.1) *
          omegaState P (pauliYProjection P m z.2) :=
      site_operator_product_state P h (pauliYProjectionMatrix z.1) (pauliYProjectionMatrix z.2)
    _ = 1 / 4 := by rw [pauli_y_projection_state, pauli_y_projection_state]; norm_num

theorem star_projection_inner_norm_sq (P : SiteProfile)
    (E : TowerHilbert P →L[ℂ] TowerHilbert P) (hE : IsStarProjection E)
    (v : TowerHilbert P) :
    inner ℂ v (E v) = ((‖E v‖ ^ 2 : ℝ) : ℂ) := by
  have hp := ContinuousLinearMap.adjoint_inner_right E v (E v)
  rw [← ContinuousLinearMap.star_eq_adjoint, hE.isSelfAdjoint.star_eq] at hp
  change inner ℂ v ((E * E) v) = inner ℂ (E v) (E v) at hp
  rw [hE.isIdempotentElem] at hp
  rw [hp, inner_self_eq_norm_sq_to_K, Complex.ofReal_pow]
  rfl

theorem pauli_expectation_norm_sq (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) (s t : ℝ) :
    orbitExpectation P (sitePauliX P n) (sitePauliX P m) (pauliJointEffect P n m z) s t =
      ((‖pauliJointEffect P n m z
        (operatorOrbit P (sitePauliX P n) (sitePauliX P m) s t (hOmega P))‖ ^ 2 : ℝ) : ℂ) := by
  rw [orbit_vector_state]
  exact star_projection_inner_norm_sq P _ (pauli_joint_effect_isStarProjection P h z) _

theorem pauli_probability_norm_sq (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) (s t : ℝ) :
    pauliProbability P n m z s t =
      ‖pauliJointEffect P n m z
        (operatorOrbit P (sitePauliX P n) (sitePauliX P m) s t (hOmega P))‖ ^ 2 := by
  unfold pauliProbability
  rw [pauli_expectation_norm_sq P h]
  rfl

theorem pauli_probability_real (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) (s t : ℝ) :
    orbitExpectation P (sitePauliX P n) (sitePauliX P m) (pauliJointEffect P n m z) s t =
      (pauliProbability P n m z s t : ℂ) := by
  rw [pauli_probability_norm_sq P h]
  exact pauli_expectation_norm_sq P h z s t

theorem pauli_probability_nonnegative (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) (s t : ℝ) : 0 ≤ pauliProbability P n m z s t := by
  rw [pauli_probability_norm_sq P h]
  exact sq_nonneg _

theorem pauli_probability_sum (P : SiteProfile) {n m : ℕ} (_h : n ≠ m) (s t : ℝ) :
    ∑ z : Fin 2 × Fin 2, pauliProbability P n m z s t = 1 := by
  have hs := orbit_expectation_sum P (sitePauliX P n) (sitePauliX P m)
    (pauliJointEffect P n m) s t
  rw [pauli_joint_effect_sum,
    orbit_expectation_one P _ _ (site_pauli_x_selfadjoint P n) (site_pauli_x_selfadjoint P m)] at hs
  simpa only [pauliProbability, Fintype.sum_prod_type, Fin.sum_univ_two,
    Complex.add_re, Complex.one_re] using congrArg Complex.re hs.symm

theorem pauli_probability_origin (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) : pauliProbability P n m z 0 0 = 1 / 4 := by
  rw [pauliProbability, orbit_expectation_origin, pauli_joint_effect_state P h]
  norm_num

theorem pauli_probability_origin_pos (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) : 0 < pauliProbability P n m z 0 0 := by
  rw [pauli_probability_origin P h]
  norm_num

theorem pauli_joint_first_commutator (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) :
    pauliJointEffect P n m z * sitePauliX P n -
      sitePauliX P n * pauliJointEffect P n m z =
        (pauliYProjection P n z.1 * sitePauliX P n -
          sitePauliX P n * pauliYProjection P n z.1) * pauliYProjection P m z.2 := by
  unfold pauliJointEffect
  calc
    (pauliYProjection P n z.1 * pauliYProjection P m z.2) * sitePauliX P n -
        sitePauliX P n * (pauliYProjection P n z.1 * pauliYProjection P m z.2) =
      pauliYProjection P n z.1 * (pauliYProjection P m z.2 * sitePauliX P n) -
        (sitePauliX P n * pauliYProjection P n z.1) * pauliYProjection P m z.2 := by
          simp only [mul_assoc]
    _ = pauliYProjection P n z.1 * (sitePauliX P n * pauliYProjection P m z.2) -
        (sitePauliX P n * pauliYProjection P n z.1) * pauliYProjection P m z.2 := by
          rw [(pauli_y_projection_x_commute P h.symm z.2).eq]
    _ = _ := by simp only [sub_mul, mul_assoc]

theorem pauli_joint_first_response (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) :
    Complex.I * omegaState P (pauliJointEffect P n m z * sitePauliX P n -
      sitePauliX P n * pauliJointEffect P n m z) =
        ((signOutcome z.1 * (2 * P.w n - 1) / 2 : ℝ) : ℂ) := by
  rw [pauli_joint_first_commutator P h]
  have hf := site_operator_product_state P h
    (pauliYProjectionMatrix z.1 * pauliXMatrix - pauliXMatrix * pauliYProjectionMatrix z.1)
    (pauliYProjectionMatrix z.2)
  rw [site_operator_sub, siteOperator_mul, siteOperator_mul] at hf
  change omegaState P
      ((pauliYProjection P n z.1 * sitePauliX P n -
        sitePauliX P n * pauliYProjection P n z.1) * pauliYProjection P m z.2) =
    omegaState P (pauliYProjection P n z.1 * sitePauliX P n -
      sitePauliX P n * pauliYProjection P n z.1) * omegaState P (pauliYProjection P m z.2) at hf
  rw [hf, pauli_y_projection_state, ← mul_assoc, pauli_y_projection_response]
  push_cast; ring

theorem pauli_joint_second_response (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) :
    Complex.I * omegaState P (pauliJointEffect P n m z * sitePauliX P m -
      sitePauliX P m * pauliJointEffect P n m z) =
        ((signOutcome z.2 * (2 * P.w m - 1) / 2 : ℝ) : ℂ) := by
  rw [pauli_joint_effect_swap P h z]
  exact pauli_joint_first_response P h.symm (z.2, z.1)

theorem pauli_probability_first_derivative (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) :
    HasDerivAt (fun s : ℝ => pauliProbability P n m z s 0)
      (signOutcome z.1 * (2 * P.w n - 1) / 2) 0 := by
  have hd := orbit_expectation_first_derivative P (sitePauliX P n) (sitePauliX P m)
    (pauliJointEffect P n m z) (site_pauli_x_selfadjoint P n)
  rw [pauli_joint_first_response P h z] at hd
  have hr := Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd
  simpa only [Function.comp_def, Complex.reCLM_apply, Complex.ofReal_re, pauliProbability] using hr

theorem pauli_probability_second_derivative (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (z : Fin 2 × Fin 2) :
    HasDerivAt (fun t : ℝ => pauliProbability P n m z 0 t)
      (signOutcome z.2 * (2 * P.w m - 1) / 2) 0 := by
  have hd := orbit_expectation_second_derivative P (sitePauliX P n) (sitePauliX P m)
    (pauliJointEffect P n m z) (site_pauli_x_selfadjoint P m)
  rw [pauli_joint_second_response P h z] at hd
  have hr := Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd
  simpa only [Function.comp_def, Complex.reCLM_apply, Complex.ofReal_re, pauliProbability] using hr

#print axioms signOutcome
#print axioms sign_outcome_zero
#print axioms sign_outcome_one
#print axioms sign_outcome_square
#print axioms sign_outcome_sum
#print axioms pauliYProjectionMatrix
#print axioms pauliYProjection
#print axioms pauliJointEffect
#print axioms pauliProbability
#print axioms pauli_y_matrix_square
#print axioms pauli_y_matrix_star
#print axioms pauli_y_matrix_orthogonal
#print axioms pauli_y_matrix_sum
#print axioms pauli_y_matrix_commutator
#print axioms pauli_y_projection_formula
#print axioms pauli_y_projection_isStarProjection
#print axioms pauli_y_projection_mem_factor
#print axioms pauli_y_projection_orthogonal
#print axioms pauli_y_projection_sum
#print axioms pauli_y_projection_state
#print axioms pauli_y_projection_commute
#print axioms pauli_y_projection_x_commute
#print axioms pauli_y_projection_commutator
#print axioms pauli_y_projection_response
#print axioms pauli_joint_effect_isStarProjection
#print axioms pauli_joint_effect_mem_factor
#print axioms pauli_joint_effect_positive
#print axioms pauli_joint_effect_swap
#print axioms pauli_joint_effect_product
#print axioms pauli_joint_effect_orthogonal
#print axioms pauli_joint_effect_sum
#print axioms pauli_joint_effect_state
#print axioms star_projection_inner_norm_sq
#print axioms pauli_expectation_norm_sq
#print axioms pauli_probability_norm_sq
#print axioms pauli_probability_real
#print axioms pauli_probability_nonnegative
#print axioms pauli_probability_sum
#print axioms pauli_probability_origin
#print axioms pauli_probability_origin_pos
#print axioms pauli_joint_first_commutator
#print axioms pauli_joint_first_response
#print axioms pauli_joint_second_response
#print axioms pauli_probability_first_derivative
#print axioms pauli_probability_second_derivative
end
end ChatgptAudit.Observable035
