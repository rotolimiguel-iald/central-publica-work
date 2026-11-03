-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_006 (05/09/2026), transposta em 05/09/2026
-- A ESPERANCA DO CENTRALIZADOR: habitante LOCAL (pinching espectral de cada
--   andar entra no centralizador GLOBAL de omega; into/fixes/ortho; unico) e
--   habitante TRACIAL do contrato original (w=1/2: M_omega = M, E = id);
--   invariancia de sitios sob sigma_t para TODO t (caudas nunca comprimem
--   estritamente); ponte: todo habitante global RESTRINGE-SE ao pinching.
-- Auditoria da gerencia (sessao d554e796): hashes 14/14 + manifesto 408/408;
--   recompilacao independente 5/5 exit 0; 34/34 no trio
--   [propext, Classical.choice, Quot.sound]; zero sorry/warning.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports da
--   bancada; nada mais. Namespace ChatgptAudit = procedencia.
-- [OPEN] declarados pela bancada: habitante global NAO tracial (parede exata:
--   operador medio do periodo + comutacao da media com E_N); nao-ciclicidade
--   da cauda em Lean; translacao de energia positiva nao trivial.
-- NAO move gate; nao e fisica. NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.LocalCentralizerExpectation
import TGLExt.ExpectationContractGap
import TGLExt.SiteModularInvariance

set_option autoImplicit false
namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem global_expectation_restricts_to_pinching (F : ExpectationInput P) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    F.E (towerPi P a) = towerPi P (specExpect (towerW P N) a) := by
  let L : LocalCentralizerInput P N := {
    E := fun a => F.E (towerPi P a)
    into := fun a => F.into _ (towerPi_mem_factor a)
    fixes := fun a ha => F.fixes _ ha
    ortho := fun a b hb => F.ortho _ (towerPi_mem_factor a) b hb }
  exact local_input_unique N L a

theorem global_expectation_differs_from_floor (F : ExpectationInput P)
    (hp : P.w 0 ≠ 1/2) (N : ℕ) :
    ¬ (∀ x ∈ theFactorObject P, F.E x = towerExpectation P N x) := by
  intro h
  exact expectation_not_imported_contract hp N ⟨F,h⟩

theorem shifted_range_invariant
    (theta : (TowerHilbert P →L[ℂ] TowerHilbert P) →
      (TowerHilbert P →L[ℂ] TowerHilbert P))
    (himage : theta '' (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) =
      (chainTailClosure P 1 : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) (t : ℝ) :
    modularConjugation P t ''
      (theta '' (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) =
      theta '' (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := by
  rw [himage]
  exact tail_flow_image t 1

#print axioms global_expectation_restricts_to_pinching
#print axioms global_expectation_differs_from_floor
#print axioms shifted_range_invariant
end
end ChatgptAudit
