-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_001 (05/09/2026), transposta em 05/09/2026
-- A ESPERANCA CONDICIONAL DOS ANDARES: constructedLevelExpectations e o TERMO
--   (todos os campos por prova); expectation_not_imported_contract mede a
--   distancia ao contrato importado (obstrucao morre exatamente em w(0)=1/2).
-- Auditoria da gerencia (sessao d554e796): hashes 11/11; recompilacao
--   independente 8/8 exit 0; axiomas = [propext, Classical.choice, Quot.sound].
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports da
--   bancada; nada mais. Namespace ChatgptAudit = procedencia.
-- NAO move gate; nao e fisica. NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ExpectationBounded
import TGLExt.ExpectationPositive
import TGLExt.ExpectationSlice
import TGLExt.ExpectationContractGap

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt
noncomputable section

/-- Contrato específico dos andares; não é o contrato do centralizador. -/
structure LevelExpectationFamily (P : SiteProfile) where
  E : ℕ → (TowerHilbert P →L[ℂ] TowerHilbert P) →L[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P)
  into : ∀ N x, ∃ a : Matrix (chainIdx N) (chainIdx N) ℂ, E N x = towerPi P a
  fixes : ∀ N (a : Matrix (chainIdx N) (chainIdx N) ℂ), E N (towerPi P a) = towerPi P a
  idempotent : ∀ N x, E N (E N x) = E N x
  preserves : ∀ N x, omegaState P (E N x) = omegaState P x
  bimodular : ∀ N (a b : Matrix (chainIdx N) (chainIdx N) ℂ) x,
    x ∈ theFactorObject P → E N (towerPi P a * x * towerPi P b) = towerPi P a * E N x * towerPi P b
  positive : ∀ N x, x ∈ theFactorObject P → 0 ≤ x → 0 ≤ E N x
  modular : ∀ t N x, modularConjugation P t (E N x) = E N (modularConjugation P t x)
  tower : ∀ M N x, E M (E N x) = E (min M N) x

/-- Todos os campos são preenchidos por provas construídas; nenhum é hipótese importada. -/
def constructedLevelExpectations (P : SiteProfile) : LevelExpectationFamily P where
  E := expectationCLM P
  into := expectation_into
  fixes := expectation_fixes
  idempotent := expectation_idempotent
  preserves := expectation_preserves_state
  bimodular := expectation_bimodular
  positive := expectation_positive
  modular := expectation_flow_commutes
  tower := expectation_tower

theorem level_expectation_family_exists (P : SiteProfile) : Nonempty (LevelExpectationFamily P) :=
  ⟨constructedLevelExpectations P⟩

#print axioms constructedLevelExpectations
#print axioms level_expectation_family_exists
end
end ChatgptAudit
