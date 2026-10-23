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
import TGLExt.SitePhaseCovariance
import TGLExt.LikelihoodPreparedState

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace ChatgptAudit.Observable035
open Matrix TGLExt ChatgptAudit ChatgptAudit.Cocycle030 ChatgptAudit.Angular034
open scoped Kronecker
noncomputable section

def pauliXMatrix : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

def pauliYMatrix : Matrix (Fin 2) (Fin 2) ℂ := !![0, -Complex.I; Complex.I, 0]

def pauliZMatrix : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

def sitePauliX (P : SiteProfile) (n : ℕ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  siteOperator P n pauliXMatrix

def sitePauliY (P : SiteProfile) (n : ℕ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  siteOperator P n pauliYMatrix

def sitePauliZ (P : SiteProfile) (n : ℕ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  siteOperator P n pauliZMatrix

def siteOperatorLinear (P : SiteProfile) (n : ℕ) :
    Matrix (Fin 2) (Fin 2) ℂ →ₗ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  (towerPiLinear P n).comp (lastSiteLinear n)

theorem site_operator_one (P : SiteProfile) (n : ℕ) :
    siteOperator P n (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 := by
  unfold siteOperator
  rw [last_site_one, towerPi_one]

theorem site_operator_add (P : SiteProfile) (n : ℕ)
    (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n (a + b) = siteOperator P n a + siteOperator P n b :=
  (siteOperatorLinear P n).map_add a b

theorem site_operator_sub (P : SiteProfile) (n : ℕ)
    (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n (a - b) = siteOperator P n a - siteOperator P n b :=
  (siteOperatorLinear P n).map_sub a b

theorem site_operator_smul (P : SiteProfile) (n : ℕ) (c : ℂ)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n (c • a) = c • siteOperator P n a :=
  (siteOperatorLinear P n).map_smul c a

theorem site_operator_state (P : SiteProfile) (n : ℕ)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    omegaState P (siteOperator P n a) =
      ∑ i : Fin 2, (siteW (P.w n) i : ℂ) * a i i := by
  cases n with
  | zero =>
    change omegaState P (towerPi P (N := 0) a) = _
    rw [omegaState_pi]
    rfl
  | succ n =>
    change omegaState P (towerPi P (N := n + 1)
      ((1 : Matrix (chainIdx n) (chainIdx n) ℂ) ⊗ₖ a)) = _
    rw [omegaState_pi (P := P) (N := n + 1)
      ((1 : Matrix (chainIdx n) (chainIdx n) ℂ) ⊗ₖ a),
      tState_kron_split P (N := n) (1 : Matrix (chainIdx n) (chainIdx n) ℂ) a,
      tState_one P n, one_mul]

theorem site_operator_state_diagonal (P : SiteProfile) (n : ℕ)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    omegaState P (siteOperator P n a) =
      (P.w n : ℂ) * a 0 0 + ((1 - P.w n : ℝ) : ℂ) * a 1 1 := by
  rw [site_operator_state, Fin.sum_univ_two]
  simp only [siteW, ite_true, show (1 : Fin 2) ≠ 0 by decide, ite_false]

theorem site_operator_mem_tail (P : SiteProfile) (N m : ℕ) (h : N ≤ m)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P m a ∈ chainTailClosure P N := by
  have hlocal : siteOperator P m a ∈ chainLocalAlgebra P (Set.Ici N) := by
    apply StarAlgebra.subset_adjoin
    exact ⟨m, h, a, rfl⟩
  change siteOperator P m a ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ
      (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P))
  rw [StarSubalgebra.mem_centralizer_iff]
  intro A hA
  have hstarA : star A ∈ StarSubalgebra.centralizer ℂ
      (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
    star_mem hA
  change A ∈ StarSubalgebra.centralizer ℂ
    (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) at hA
  rw [StarSubalgebra.mem_centralizer_iff] at hA hstarA
  exact ⟨(hA _ hlocal).1.symm, (hstarA _ hlocal).1.symm⟩

theorem site_operator_tail_factorization (P : SiteProfile) (n : ℕ)
    (a : Matrix (Fin 2) (Fin 2) ℂ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ chainTailClosure P (n + 1)) :
    omegaState P (siteOperator P n a * A) =
      omegaState P (siteOperator P n a) * omegaState P A := by
  have he := expectation_bimodular n (lastSiteMatrix n a) 1 A
    (chain_tail_mem_factor _ hA)
  simp only [towerPi_one, mul_one] at he
  change towerExpectation P n (siteOperator P n a * A) =
    siteOperator P n a * towerExpectation P n A at he
  rw [← expectation_preserves_state n (siteOperator P n a * A), he,
    tail_prefix_expectation_scalar n A hA, mul_smul_comm, mul_one]
  change inner ℂ (hOmega P) (omegaState P A • siteOperator P n a (hOmega P)) = _
  rw [inner_smul_right]
  change omegaState P A * omegaState P (siteOperator P n a) = _
  exact mul_comm _ _

theorem site_operator_product_state_lt (P : SiteProfile) {n m : ℕ} (h : n < m)
    (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    omegaState P (siteOperator P n a * siteOperator P m b) =
      omegaState P (siteOperator P n a) * omegaState P (siteOperator P m b) :=
  site_operator_tail_factorization P n a (siteOperator P m b)
    (site_operator_mem_tail P (n + 1) m (Nat.succ_le_of_lt h) b)

theorem site_operator_product_state (P : SiteProfile) {n m : ℕ} (h : n ≠ m)
    (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    omegaState P (siteOperator P n a * siteOperator P m b) =
      omegaState P (siteOperator P n a) * omegaState P (siteOperator P m b) := by
  rcases lt_or_gt_of_ne h with hlt | hgt
  · exact site_operator_product_state_lt P hlt a b
  · rw [siteOperators_commute h a b, site_operator_product_state_lt P hgt b a, mul_comm]

theorem pauli_x_conjTranspose : pauliXMatrixᴴ = pauliXMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix, Matrix.conjTranspose_apply]

theorem pauli_y_conjTranspose : pauliYMatrixᴴ = pauliYMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliYMatrix, Matrix.conjTranspose_apply]

theorem pauli_z_conjTranspose : pauliZMatrixᴴ = pauliZMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliZMatrix, Matrix.conjTranspose_apply]

theorem pauli_x_square : pauliXMatrix * pauliXMatrix = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]

theorem pauli_y_square : pauliYMatrix * pauliYMatrix = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliYMatrix, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]

theorem pauli_z_square : pauliZMatrix * pauliZMatrix = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliZMatrix, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]

theorem pauli_xy : pauliXMatrix * pauliYMatrix = Complex.I • pauliZMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix, pauliYMatrix, pauliZMatrix,
      Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply, smul_eq_mul]

theorem pauli_yx : pauliYMatrix * pauliXMatrix = (-Complex.I) • pauliZMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix, pauliYMatrix, pauliZMatrix,
      Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply, smul_eq_mul]

theorem pauli_z_projection :
    pauliZMatrix = (2 : ℂ) • Matrix.single (0 : Fin 2) 0 (1 : ℂ) - 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliZMatrix, Matrix.single_apply, Matrix.smul_apply,
      Matrix.sub_apply, Matrix.one_apply, smul_eq_mul]

theorem site_pauli_x_mem_factor (P : SiteProfile) (n : ℕ) :
    sitePauliX P n ∈ theFactorObject P := siteOperator_mem_factor n pauliXMatrix

theorem site_pauli_y_mem_factor (P : SiteProfile) (n : ℕ) :
    sitePauliY P n ∈ theFactorObject P := siteOperator_mem_factor n pauliYMatrix

theorem site_pauli_z_mem_factor (P : SiteProfile) (n : ℕ) :
    sitePauliZ P n ∈ theFactorObject P := siteOperator_mem_factor n pauliZMatrix

theorem site_pauli_x_selfadjoint (P : SiteProfile) (n : ℕ) :
    IsSelfAdjoint (sitePauliX P n) := by
  change star (siteOperator P n pauliXMatrix) = siteOperator P n pauliXMatrix
  rw [← siteOperator_star, pauli_x_conjTranspose]

theorem site_pauli_y_selfadjoint (P : SiteProfile) (n : ℕ) :
    IsSelfAdjoint (sitePauliY P n) := by
  change star (siteOperator P n pauliYMatrix) = siteOperator P n pauliYMatrix
  rw [← siteOperator_star, pauli_y_conjTranspose]

theorem site_pauli_z_selfadjoint (P : SiteProfile) (n : ℕ) :
    IsSelfAdjoint (sitePauliZ P n) := by
  change star (siteOperator P n pauliZMatrix) = siteOperator P n pauliZMatrix
  rw [← siteOperator_star, pauli_z_conjTranspose]

theorem site_pauli_x_square (P : SiteProfile) (n : ℕ) :
    sitePauliX P n * sitePauliX P n = 1 := by
  change siteOperator P n pauliXMatrix * siteOperator P n pauliXMatrix = 1
  rw [← siteOperator_mul, pauli_x_square, site_operator_one]

theorem site_pauli_y_square (P : SiteProfile) (n : ℕ) :
    sitePauliY P n * sitePauliY P n = 1 := by
  change siteOperator P n pauliYMatrix * siteOperator P n pauliYMatrix = 1
  rw [← siteOperator_mul, pauli_y_square, site_operator_one]

theorem site_pauli_z_square (P : SiteProfile) (n : ℕ) :
    sitePauliZ P n * sitePauliZ P n = 1 := by
  change siteOperator P n pauliZMatrix * siteOperator P n pauliZMatrix = 1
  rw [← siteOperator_mul, pauli_z_square, site_operator_one]

theorem site_pauli_xy (P : SiteProfile) (n : ℕ) :
    sitePauliX P n * sitePauliY P n = Complex.I • sitePauliZ P n := by
  change siteOperator P n pauliXMatrix * siteOperator P n pauliYMatrix =
    Complex.I • siteOperator P n pauliZMatrix
  rw [← siteOperator_mul, pauli_xy, site_operator_smul]

theorem site_pauli_yx (P : SiteProfile) (n : ℕ) :
    sitePauliY P n * sitePauliX P n = (-Complex.I) • sitePauliZ P n := by
  change siteOperator P n pauliYMatrix * siteOperator P n pauliXMatrix =
    (-Complex.I) • siteOperator P n pauliZMatrix
  rw [← siteOperator_mul, pauli_yx, site_operator_smul]

theorem site_pauli_z_projection (P : SiteProfile) (n : ℕ) :
    sitePauliZ P n = (2 : ℂ) • siteZeroProjection P n - 1 := by
  unfold sitePauliZ
  rw [pauli_z_projection, site_operator_sub, site_operator_smul, site_operator_one]
  rfl

theorem site_pauli_x_state (P : SiteProfile) (n : ℕ) :
    omegaState P (sitePauliX P n) = 0 := by
  rw [sitePauliX, site_operator_state_diagonal]
  simp [pauliXMatrix]

theorem site_pauli_y_state (P : SiteProfile) (n : ℕ) :
    omegaState P (sitePauliY P n) = 0 := by
  rw [sitePauliY, site_operator_state_diagonal]
  simp [pauliYMatrix]

theorem site_pauli_z_state (P : SiteProfile) (n : ℕ) :
    omegaState P (sitePauliZ P n) = ((2 * P.w n - 1 : ℝ) : ℂ) := by
  rw [sitePauliZ, site_operator_state_diagonal]
  simp only [pauliZMatrix, Matrix.of_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one, mul_one, mul_neg]
  push_cast
  ring

theorem site_pauli_yx_commutator (P : SiteProfile) (n : ℕ) :
    Complex.I • (sitePauliY P n * sitePauliX P n -
      sitePauliX P n * sitePauliY P n) = (2 : ℂ) • sitePauliZ P n := by
  rw [site_pauli_yx, site_pauli_xy, ← sub_smul, smul_smul]
  congr 1
  norm_num [mul_sub]

theorem site_pauli_y_response (P : SiteProfile) (n : ℕ) :
    Complex.I * omegaState P (sitePauliY P n * sitePauliX P n -
      sitePauliX P n * sitePauliY P n) = ((2 * (2 * P.w n - 1) : ℝ) : ℂ) := by
  rw [← ChatgptAudit.Density033.omega_state_smul, site_pauli_yx_commutator,
    ChatgptAudit.Density033.omega_state_smul, site_pauli_z_state]
  push_cast; ring

theorem site_pauli_xy_commute (P : SiteProfile) {n m : ℕ} (h : n ≠ m) :
    Commute (sitePauliX P n) (sitePauliY P m) :=
  siteOperators_commute h pauliXMatrix pauliYMatrix

theorem site_pauli_xx_commute (P : SiteProfile) {n m : ℕ} (h : n ≠ m) :
    Commute (sitePauliX P n) (sitePauliX P m) :=
  siteOperators_commute h pauliXMatrix pauliXMatrix

theorem site_pauli_yy_commute (P : SiteProfile) {n m : ℕ} (h : n ≠ m) :
    Commute (sitePauliY P n) (sitePauliY P m) :=
  siteOperators_commute h pauliYMatrix pauliYMatrix

#print axioms pauliXMatrix
#print axioms pauliYMatrix
#print axioms pauliZMatrix
#print axioms sitePauliX
#print axioms sitePauliY
#print axioms sitePauliZ
#print axioms siteOperatorLinear
#print axioms site_operator_one
#print axioms site_operator_add
#print axioms site_operator_sub
#print axioms site_operator_smul
#print axioms site_operator_state
#print axioms site_operator_state_diagonal
#print axioms site_operator_mem_tail
#print axioms site_operator_tail_factorization
#print axioms site_operator_product_state_lt
#print axioms site_operator_product_state
#print axioms pauli_x_conjTranspose
#print axioms pauli_y_conjTranspose
#print axioms pauli_z_conjTranspose
#print axioms pauli_x_square
#print axioms pauli_y_square
#print axioms pauli_z_square
#print axioms pauli_xy
#print axioms pauli_yx
#print axioms pauli_z_projection
#print axioms site_pauli_x_mem_factor
#print axioms site_pauli_y_mem_factor
#print axioms site_pauli_z_mem_factor
#print axioms site_pauli_x_selfadjoint
#print axioms site_pauli_y_selfadjoint
#print axioms site_pauli_z_selfadjoint
#print axioms site_pauli_x_square
#print axioms site_pauli_y_square
#print axioms site_pauli_z_square
#print axioms site_pauli_xy
#print axioms site_pauli_yx
#print axioms site_pauli_z_projection
#print axioms site_pauli_x_state
#print axioms site_pauli_y_state
#print axioms site_pauli_z_state
#print axioms site_pauli_yx_commutator
#print axioms site_pauli_y_response
#print axioms site_pauli_xy_commute
#print axioms site_pauli_xx_commute
#print axioms site_pauli_yy_commute
end
end ChatgptAudit.Observable035
