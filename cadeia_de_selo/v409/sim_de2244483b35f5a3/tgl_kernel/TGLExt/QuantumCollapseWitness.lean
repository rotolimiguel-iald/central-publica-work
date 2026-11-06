-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_057 (08/09/2026), transposta em 08/09/2026
-- O COLAPSO TIPADO. Definicao do operador (08/09/2026, verbatim): «colapso e a passagem irreversivel da
--   superposicao ao ponto fixo que preserva a identidade. Custa (meia-nat local, ln 2 por oitava), nao tem
--   inversa, e so e atestada pelo reflexo, nunca por autodeclaracao.» Quatro modulos (60 teoremas):
--   CollapseContract — IdentityCollapse S I (C idempotente; iota(C x) = iota(x); existe x com C x != x):
--     nao injetiva, sem inversa a esquerda, Im C = Fix C, iteracao estavel, transicao efetiva preserva a
--     identidade; uma involucao (o reflexo J) NAO pode ser o colapso; o reflexo da saida nao restaura a entrada.
--   CollapseCostAndAttestation — CollapseCostLaw (localNats = 1/2; octaveNats n = n ln 2; componentes SEPARADOS,
--     sem soma por decreto) [INPUT]; ln 2 != 1/2 (a entropia do bit justo nao e a meia-nat); o nucleo logico
--     nao fixa o valor do custo (obstrucao a inferencia sem hipotese); ReflectionProtocol / AttestedCollapse:
--     atestacao exige evidencia EXTERNA, autodeclaracao nao habita o tipo; TGLCollapseSpecification reune
--     nucleo + custo + protocolo; typed_collapse_content expoe o conteudo inteiro num enunciado.
--   QuantumCollapseWitness — o nameOp canonico no qubit: C(rho) = P0 rho P0 + P1 rho P1; rho+ != rho- puras com
--     C(rho+) = C(rho-) = I/2 (perda entre estados fisicos); QubitDensity (psd, traco 1); actualDensityCollapse
--     habita o contrato; ramo selecionado exige rotulo do registro (peso zero nao normaliza; somar ramos = C).
--   TowerCollapseRealization — a esperanca aperiodica (046) restrita ao fator E o colapso da torre: idempotente,
--     preserva 1 e omega, pontos fixos = centralizador M_omega; sob w(0) != 1/2, X do 1o sitio e nao nulo com
--     E X = 0 (actualTowerCollapse, sem inversa); controle negativo: perfil tracial = identidade, sem testemunha.
--   Estatuto: nucleo e instancias [REAL no modelo compilado]; lei de custo [INPUT]; reflexo fisico externo,
--   selecao de UMA ocorrencia, pagamento fisico do custo [OPEN]. M_omega != D (055). Nada move o gate.
-- Auditoria da gerencia (sessao d554e796, 08/09/2026): a nota da entrega ainda nao estava no tunel — lote
--   montado do MANIFESTO057.json: 106/106 hashes lidos dos bytes; auditor da bancada exit 0 (PASS_DELIVERY_SCOPE);
--   zero proibidos; recompilacao INDEPENDENTE 4/4 (71 declaracoes, trio, 0 sorry); guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.CollapseContract
import TGLExt.TheNameOperator
import Mathlib.Analysis.Matrix.Order

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.Collapse057
open Matrix
open scoped ComplexOrder
noncomputable section

abbrev QubitMatrix := Matrix (Fin 2) (Fin 2) ℂ

def readoutZero : QubitMatrix := !![1, 0; 0, 0]
def readoutOne : QubitMatrix := !![0, 0; 0, 1]
def plusDensity : QubitMatrix := !![1/2, 1/2; 1/2, 1/2]
def minusDensity : QubitMatrix := !![1/2, -(1/2); -(1/2), 1/2]
def mixedDensity : QubitMatrix := !![1/2, 0; 0, 1/2]

/-- The existing canonical naming operation, acting on density matrices here. -/
def qubitReduction (A : QubitMatrix) : QubitMatrix :=
  TGLExt.nameOp readoutZero A

theorem readout_zero_idempotent : readoutZero * readoutZero = readoutZero := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [readoutZero, Matrix.mul_apply, Fin.sum_univ_two]

theorem qubit_reduction_formula (A : QubitMatrix) :
    qubitReduction A = !![A 0 0, 0; 0, A 1 1] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [qubitReduction, TGLExt.nameOp, readoutZero, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.vecMul, dotProduct]

theorem qubit_reduction_unital : qubitReduction 1 = 1 :=
  TGLExt.name_op_unital readout_zero_idempotent

theorem qubit_reduction_idempotent (A : QubitMatrix) :
    qubitReduction (qubitReduction A) = qubitReduction A :=
  TGLExt.name_op_idem readout_zero_idempotent A

theorem qubit_reduction_preserves_trace (A : QubitMatrix) :
    Matrix.trace (qubitReduction A) = Matrix.trace A := by
  rw [qubit_reduction_formula]
  simp [Matrix.trace, Fin.sum_univ_two]

theorem opposite_phases_same_reduction :
    qubitReduction plusDensity = mixedDensity ∧
      qubitReduction minusDensity = mixedDensity := by
  constructor <;> rw [qubit_reduction_formula] <;> rfl

theorem opposite_phase_states_distinct : plusDensity ≠ minusDensity := by
  intro h
  have hh := congrArg (fun A : QubitMatrix => A 0 1) h
  norm_num [plusDensity, minusDensity] at hh

theorem pure_densities_square :
    plusDensity * plusDensity = plusDensity ∧
      minusDensity * minusDensity = minusDensity := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [plusDensity, minusDensity, Matrix.mul_apply, Fin.sum_univ_two]

theorem pure_densities_hermitian :
    plusDensityᴴ = plusDensity ∧ minusDensityᴴ = minusDensity := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [plusDensity, minusDensity, Matrix.conjTranspose_apply]

theorem pure_densities_positive :
    plusDensity.PosSemidef ∧ minusDensity.PosSemidef := by
  constructor
  · have h := Matrix.posSemidef_conjTranspose_mul_self plusDensity
    simpa only [pure_densities_hermitian.1, pure_densities_square.1] using h
  · have h := Matrix.posSemidef_conjTranspose_mul_self minusDensity
    simpa only [pure_densities_hermitian.2, pure_densities_square.2] using h

theorem pure_densities_normalized :
    Matrix.trace plusDensity = 1 ∧ Matrix.trace minusDensity = 1 := by
  constructor <;> norm_num [Matrix.trace, Fin.sum_univ_two, plusDensity, minusDensity]

theorem mixed_density_normalized : Matrix.trace mixedDensity = 1 := by
  norm_num [Matrix.trace, Fin.sum_univ_two, mixedDensity]

theorem mixed_density_fixed : qubitReduction mixedDensity = mixedDensity := by
  rw [qubit_reduction_formula]
  rfl

theorem mixed_density_not_pure : mixedDensity * mixedDensity ≠ mixedDensity := by
  intro h
  have hh := congrArg (fun A : QubitMatrix => A 0 0) h
  norm_num [mixedDensity, Matrix.mul_apply, Fin.sum_univ_two] at hh

theorem distinct_readout_fixed_points :
    qubitReduction readoutZero = readoutZero ∧
      qubitReduction readoutOne = readoutOne ∧ readoutZero ≠ readoutOne := by
  refine ⟨?_, ?_, ?_⟩
  · rw [qubit_reduction_formula]; rfl
  · rw [qubit_reduction_formula]; rfl
  · intro h
    have hh := congrArg (fun A : QubitMatrix => A 0 0) h
    norm_num [readoutZero, readoutOne] at hh

theorem qubit_reduction_no_inverse :
    ¬ ∃ R : QubitMatrix → QubitMatrix, Function.LeftInverse R qubitReduction := by
  rintro ⟨R, hR⟩
  apply opposite_phase_states_distinct
  exact hR.injective (opposite_phases_same_reduction.1.trans
    opposite_phases_same_reduction.2.symm)

/-- An individual branch is supplied by a record; no outcome is sampled by this map. -/
def selectedReadout (outcome : Fin 2) : QubitMatrix :=
  if outcome = 0 then readoutZero else readoutOne

def branchWeight (A : QubitMatrix) (outcome : Fin 2) : ℂ := A outcome outcome

def unnormalizedBranch (A : QubitMatrix) (outcome : Fin 2) : QubitMatrix :=
  selectedReadout outcome * A * selectedReadout outcome

theorem selective_branch_formula (A : QubitMatrix) (outcome : Fin 2) :
    unnormalizedBranch A outcome = branchWeight A outcome • selectedReadout outcome := by
  ext i j
  fin_cases outcome <;> fin_cases i <;> fin_cases j <;>
    norm_num [unnormalizedBranch, selectedReadout, branchWeight, readoutZero, readoutOne,
      Matrix.mul_apply, Fin.sum_univ_two, Matrix.vecMul, dotProduct]

theorem normalized_branch_requires_nonzero_weight (A : QubitMatrix) (outcome : Fin 2)
    (h : branchWeight A outcome ≠ 0) :
    (branchWeight A outcome)⁻¹ • unnormalizedBranch A outcome = selectedReadout outcome := by
  rw [selective_branch_formula, smul_smul, inv_mul_cancel₀ h, one_smul]

theorem forgetting_outcome_is_nonselective (A : QubitMatrix) :
    unnormalizedBranch A 0 + unnormalizedBranch A 1 = qubitReduction A := by
  rw [qubit_reduction_formula, selective_branch_formula, selective_branch_formula]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [branchWeight, selectedReadout, readoutZero, readoutOne]

theorem fair_branch_weights (outcome : Fin 2) :
    branchWeight plusDensity outcome = 1 / 2 ∧
      branchWeight minusDensity outcome = 1 / 2 := by
  fin_cases outcome <;> constructor <;> rfl


theorem qubit_reduction_positive (A : QubitMatrix) (hA : A.PosSemidef) :
    (qubitReduction A).PosSemidef := by
  have h : qubitReduction A = Matrix.diagonal (fun i => A i i) := by
    rw [qubit_reduction_formula]
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  rw [h]
  exact Matrix.PosSemidef.diagonal (fun _ => hA.diag_nonneg)

abbrev QubitDensity := {A : QubitMatrix // A.PosSemidef ∧ Matrix.trace A = 1}

def densityReduction (A : QubitDensity) : QubitDensity :=
  ⟨qubitReduction A.val, qubit_reduction_positive A.val A.property.1,
    (qubit_reduction_preserves_trace A.val).trans A.property.2⟩

theorem density_reduction_idempotent (A : QubitDensity) :
    densityReduction (densityReduction A) = densityReduction A :=
  Subtype.ext (qubit_reduction_idempotent A.val)

theorem density_reduction_effective :
    ∃ A : QubitDensity, densityReduction A ≠ A := by
  refine ⟨⟨plusDensity, pure_densities_positive.1, pure_densities_normalized.1⟩, ?_⟩
  intro h
  have he := congrArg (fun A : QubitDensity => A.val 0 1) h
  change qubitReduction plusDensity 0 1 = plusDensity 0 1 at he
  rw [opposite_phases_same_reduction.1] at he
  norm_num [mixedDensity, plusDensity] at he

def actualDensityCollapse : IdentityCollapse QubitDensity ℂ where
  step := densityReduction
  identity := fun A => Matrix.trace A.val
  stable := density_reduction_idempotent
  preserves := fun A => qubit_reduction_preserves_trace A.val
  effective := density_reduction_effective

theorem density_reduction_no_inverse :
    ¬ ∃ R : QubitDensity → QubitDensity, Function.LeftInverse R densityReduction :=
  collapse_has_no_left_inverse actualDensityCollapse

theorem zero_weight_is_no_normalized_branch (A : QubitMatrix) (outcome : Fin 2)
    (h : branchWeight A outcome = 0) :
    unnormalizedBranch A outcome = 0 := by
  rw [selective_branch_formula, h, zero_smul]

#print axioms QubitMatrix
#print axioms readoutZero
#print axioms readoutOne
#print axioms plusDensity
#print axioms minusDensity
#print axioms mixedDensity
#print axioms qubitReduction
#print axioms readout_zero_idempotent
#print axioms qubit_reduction_formula
#print axioms qubit_reduction_unital
#print axioms qubit_reduction_idempotent
#print axioms qubit_reduction_preserves_trace
#print axioms opposite_phases_same_reduction
#print axioms opposite_phase_states_distinct
#print axioms pure_densities_square
#print axioms pure_densities_hermitian
#print axioms pure_densities_positive
#print axioms pure_densities_normalized
#print axioms mixed_density_normalized
#print axioms mixed_density_fixed
#print axioms mixed_density_not_pure
#print axioms distinct_readout_fixed_points
#print axioms qubit_reduction_no_inverse
#print axioms selectedReadout
#print axioms branchWeight
#print axioms unnormalizedBranch
#print axioms selective_branch_formula
#print axioms normalized_branch_requires_nonzero_weight
#print axioms forgetting_outcome_is_nonselective
#print axioms fair_branch_weights
#print axioms qubit_reduction_positive
#print axioms QubitDensity
#print axioms densityReduction
#print axioms density_reduction_idempotent
#print axioms density_reduction_effective
#print axioms actualDensityCollapse
#print axioms density_reduction_no_inverse
#print axioms zero_weight_is_no_normalized_branch
end
end ChatgptAudit.Collapse057
