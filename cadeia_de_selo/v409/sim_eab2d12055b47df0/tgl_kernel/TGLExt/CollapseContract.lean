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
import TGLExt.TheCostIsDerived
import TGLExt.TheAtomOfIdentity

set_option autoImplicit false
namespace ChatgptAudit.Collapse057

/-- Logical core. The identity reading is specified, not inferred from a name. -/
structure IdentityCollapse (State Identity : Type) where
  step : State → State
  identity : State → Identity
  stable : ∀ x, step (step x) = step x
  preserves : ∀ x, identity (step x) = identity x
  effective : ∃ x, step x ≠ x

theorem collapse_reuses_canonical_preservation {S I : Type}
    (C : IdentityCollapse S I) (x : S) :
    TGLExt.Preserves C.identity C.step x := C.preserves x

theorem collapse_is_not_identity {S I : Type} (C : IdentityCollapse S I) :
    C.step ≠ id := by
  intro h
  obtain ⟨x, hx⟩ := C.effective
  exact hx (congrFun h x)

theorem collapse_is_not_injective {S I : Type} (C : IdentityCollapse S I) :
    ¬ Function.Injective C.step :=
  TGLExt.the_dispositive_is_not_injective C.step C.stable
    (collapse_is_not_identity C)

theorem collapse_has_no_left_inverse {S I : Type} (C : IdentityCollapse S I) :
    ¬ ∃ R : S → S, Function.LeftInverse R C.step := by
  rintro ⟨R, hR⟩
  exact collapse_is_not_injective C hR.injective

theorem collapse_fixed_iff_in_range {S I : Type} (C : IdentityCollapse S I) (y : S) :
    C.step y = y ↔ y ∈ Set.range C.step := by
  constructor
  · intro h; exact ⟨y, h⟩
  · rintro ⟨x, rfl⟩; exact C.stable x

theorem collapse_iteration_is_stable {S I : Type}
    (C : IdentityCollapse S I) (x : S) (n : ℕ) :
    C.step^[n + 1] x = C.step x :=
  TGLExt.res_judicata_is_terminal C.step C.stable x n

/-- The image admits its inclusion section; this does not recover pre-collapse inputs. -/
def fixedRetraction {S I : Type} (C : IdentityCollapse S I)
    (x : S) : {y : S // C.step y = y} := ⟨C.step x, C.stable x⟩

theorem inclusion_is_right_inverse_on_fixed_sector {S I : Type}
    (C : IdentityCollapse S I) :
    Function.RightInverse (fun y : {y : S // C.step y = y} => y.val)
      (fixedRetraction C) := by
  intro y
  exact Subtype.ext y.property

/-- Actual changed event, not merely application to an already fixed point. -/
def CollapseTransition {S I : Type} (C : IdentityCollapse S I) (before after : S) : Prop :=
  C.step before = after ∧ before ≠ after

theorem transition_preserves_identity_and_is_fixed {S I : Type}
    (C : IdentityCollapse S I) {before after : S}
    (h : CollapseTransition C before after) :
    C.identity after = C.identity before ∧ C.step after = after := by
  rw [← h.1]
  exact ⟨C.preserves before, C.stable before⟩

theorem no_changed_transition_at_fixed_point {S I : Type}
    (C : IdentityCollapse S I) {x : S} (hx : C.step x = x) :
    ¬ CollapseTransition C x (C.step x) := by
  intro h
  exact h.2 hx.symm

theorem involution_cannot_be_collapse {S I : Type}
    (C : IdentityCollapse S I) (J : S → S) (hJ : Function.Involutive J) :
    C.step ≠ J := by
  intro h
  exact collapse_is_not_injective C (h ▸ hJ.injective)

theorem reflection_of_output_cannot_restore_input {S I R : Type}
    (C : IdentityCollapse S I) (reflect : S → R) :
    ¬ ∃ recover : R → S, ∀ x, recover (reflect (C.step x)) = x := by
  rintro ⟨recover, h⟩
  exact collapse_has_no_left_inverse C ⟨recover ∘ reflect, h⟩

#print axioms IdentityCollapse
#print axioms collapse_reuses_canonical_preservation
#print axioms collapse_is_not_identity
#print axioms collapse_is_not_injective
#print axioms collapse_has_no_left_inverse
#print axioms collapse_fixed_iff_in_range
#print axioms collapse_iteration_is_stable
#print axioms fixedRetraction
#print axioms inclusion_is_right_inverse_on_fixed_sector
#print axioms CollapseTransition
#print axioms transition_preserves_identity_and_is_fixed
#print axioms no_changed_transition_at_fixed_point
#print axioms involution_cannot_be_collapse
#print axioms reflection_of_output_cannot_restore_input
end ChatgptAudit.Collapse057
