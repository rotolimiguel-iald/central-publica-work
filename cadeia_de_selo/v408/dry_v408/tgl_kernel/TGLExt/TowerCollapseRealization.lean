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
import TGLExt.LocalHorizontalPauli

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.Collapse057
open TGLExt ChatgptAudit ChatgptAudit.Aperiodic046 ChatgptAudit.Expectation047
  ChatgptAudit.Observable035 ChatgptAudit.Orbit052

noncomputable section

/-- Restrict the domain to the actual factor; no arbitrary values outside M. -/
abbrev FactorCarrier (P : SiteProfile) :=
  {A : TowerHilbert P →L[ℂ] TowerHilbert P // A ∈ theFactorObject P}

def towerReduction (P : SiteProfile) (A : FactorCarrier P) : FactorCarrier P :=
  ⟨(aperiodicExpectationInput P).E A.val,
    ((aperiodicExpectationInput P).into A.val A.property).1⟩

theorem tower_reduction_idempotent (P : SiteProfile) (A : FactorCarrier P) :
    towerReduction P (towerReduction P A) = towerReduction P A := by
  apply Subtype.ext
  exact aperiodic_expectation_idempotent P A.val A.property

theorem tower_reduction_preserves_state (P : SiteProfile) (A : FactorCarrier P) :
    omegaState P (towerReduction P A).val = omegaState P A.val :=
  expectation_preserves_omega P (aperiodicExpectationInput P) A.val A.property

theorem tower_reduction_preserves_unit (P : SiteProfile) :
    towerReduction P ⟨1, (theFactorObject P).one_mem⟩ =
      ⟨1, (theFactorObject P).one_mem⟩ := by
  apply Subtype.ext
  exact expectation_one P (aperiodicExpectationInput P)

theorem tower_fixed_points_exactly_centralizer (P : SiteProfile) (A : FactorCarrier P) :
    towerReduction P A = A ↔ A.val ∈ omegaCentralizer P := by
  constructor
  · intro h
    have hi := (aperiodicExpectationInput P).into A.val A.property
    have he := congrArg Subtype.val h
    exact he ▸ hi
  · intro h
    exact Subtype.ext ((aperiodicExpectationInput P).fixes A.val h)

theorem tower_pauli_x_nonzero (P : SiteProfile) : sitePauliX P 0 ≠ 0 := by
  intro h
  have hn := pauli_x_gns_norm P
  rw [h] at hn
  norm_num at hn

theorem tower_reduction_effective (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    ∃ A : FactorCarrier P, towerReduction P A ≠ A := by
  refine ⟨⟨sitePauliX P 0, site_pauli_x_mem_factor P 0⟩, ?_⟩
  intro h
  have he := congrArg Subtype.val h
  change (aperiodicExpectationInput P).E (sitePauliX P 0) = sitePauliX P 0 at he
  rw [aperiodic_pauli_x_zero P hp] at he
  exact tower_pauli_x_nonzero P he.symm

/-- Constructed inhabitant for the nontracial first-site regime. -/
def actualTowerCollapse (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    IdentityCollapse (FactorCarrier P) ℂ where
  step := towerReduction P
  identity := fun A => omegaState P A.val
  stable := tower_reduction_idempotent P
  preserves := tower_reduction_preserves_state P
  effective := tower_reduction_effective P hp

theorem actual_tower_collapse_no_inverse (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    ¬ ∃ R : FactorCarrier P → FactorCarrier P,
      Function.LeftInverse R (towerReduction P) :=
  collapse_has_no_left_inverse (actualTowerCollapse P hp)

/-- Negative control: the fully tracial profile gives no changed collapse event. -/
theorem tracial_tower_reduction_is_identity (P : SiteProfile)
    (hp : ∀ n, P.w n = 1 / 2) : towerReduction P = id := by
  funext A
  apply (tower_fixed_points_exactly_centralizer P A).mpr
  exact (half_profile_centralizer_is_factor hp A.val).mpr A.property

theorem tracial_tower_has_no_effective_witness (P : SiteProfile)
    (hp : ∀ n, P.w n = 1 / 2) :
    ¬ ∃ A : FactorCarrier P, towerReduction P A ≠ A := by
  rw [tracial_tower_reduction_is_identity P hp]
  simp

#print axioms FactorCarrier
#print axioms towerReduction
#print axioms tower_reduction_idempotent
#print axioms tower_reduction_preserves_state
#print axioms tower_reduction_preserves_unit
#print axioms tower_fixed_points_exactly_centralizer
#print axioms tower_pauli_x_nonzero
#print axioms tower_reduction_effective
#print axioms actualTowerCollapse
#print axioms actual_tower_collapse_no_inverse
#print axioms tracial_tower_reduction_is_identity
#print axioms tracial_tower_has_no_effective_witness
end
end ChatgptAudit.Collapse057
