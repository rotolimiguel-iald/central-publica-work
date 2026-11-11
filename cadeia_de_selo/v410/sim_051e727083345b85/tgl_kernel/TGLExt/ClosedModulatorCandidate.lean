-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT (05/09/2026) — transposta em 05/09/2026
-- Procedencia: C:\IALD\Central de Patentes\Chatgpt (bancada da outra sessao,
--   sob direcao do operador; TUNEL\TUNEL_PROTOCOLO.md).
-- Auditoria da gerencia (sessao Claude d554e796, 05/09/2026): recompilacao
--   independente 20/20 exit 0; sonda #print axioms dos teoremas de manchete =
--   [propext, Classical.choice, Quot.sound]; zero sorry; enunciados conferidos.
-- Transposicao MECANICA: apenas (a) este cabecalho, (b) "import TGLExt" (root)
--   expandido no bloco de imports da epoca, (c) imports internos da bancada
--   prefixados com TGLExt. — nada mais foi alterado. Namespace ChatgptAudit
--   PRESERVADO como marca de procedencia.
-- Estatuto: [REAL — Lean] analise modular da torre produto (S, J·S, Delta,
--   Delta^{it}, invariancia do bicomutante). NAO move gate; NAO e fisica;
--   NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ClosedTomitaOperator
import TGLExt.TheAntiunitaryInhabitant
import TGLExt.TheMatrixAndTheModulator

set_option autoImplicit false
set_option maxHeartbeats 2000000

open Filter Topology

namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

/-- S como operador parcialmente definido semilinear da mathlib. -/
def closedTomitaPMap (P : SiteProfile) :
    TowerHilbert P →ₛₗ.[starRingEnd ℂ] TowerHilbert P where
  domain := closedTomitaDomain P
  toFun := closedTomita P

/-- Candidato J S. Ainda não se afirma positividade ou auto-adjunticidade. -/
def closedModulatorCandidate (P : SiteProfile) :
    TowerHilbert P →ₗ.[ℂ] TowerHilbert P :=
  (towerJequiv P).toLinearEquiv.toLinearMap.compPMap (closedTomitaPMap P)

theorem modulatorCandidate_apply (x : closedTomitaDomain P) :
    closedModulatorCandidate P x = towerJ P (closedTomita P x) := rfl

theorem modulatorCandidate_domain :
    (closedModulatorCandidate P).domain = closedTomitaDomain P := rfl

theorem modulatorCandidate_graph_iff (p : TowerHilbert P × TowerHilbert P) :
    p ∈ (closedModulatorCandidate P).graph ↔
      (p.1, towerJ P p.2) ∈ closure (tomitaGraph P) := by
  rw [LinearPMap.mem_graph_iff]
  constructor
  · rintro ⟨x, hx, hy⟩
    rw [← hx, ← hy, modulatorCandidate_apply, towerJ_involutive]
    exact closedTomita_graph x
  · intro hp
    let x : closedTomitaDomain P := ⟨p.1, towerJ P p.2, hp⟩
    refine ⟨x, rfl, ?_⟩
    rw [modulatorCandidate_apply]
    have h := tomita_graph_closure_single_valued p.1 _ _ (closedTomita_graph x) hp
    rw [h, towerJ_involutive]

theorem modulatorCandidate_is_closed : (closedModulatorCandidate P).IsClosed := by
  have heq : ((closedModulatorCandidate P).graph : Set (TowerHilbert P × TowerHilbert P)) =
      (fun p : TowerHilbert P × TowerHilbert P => (p.1, towerJ P p.2)) ⁻¹'
        closure (tomitaGraph P) := by
    ext p
    exact modulatorCandidate_graph_iff p
  unfold LinearPMap.IsClosed
  rw [heq]
  apply isClosed_closure.preimage
  exact continuous_fst.prodMk ((towerJ_continuous P).comp continuous_snd)

theorem modulatorCandidate_domain_dense :
    Dense ((closedModulatorCandidate P).domain : Set (TowerHilbert P)) :=
  closedTomita_domain_dense

/-- Identidade algébrica com os objetos exatos: S = J (J S). -/
theorem candidate_factorization (x : closedTomitaDomain P) :
    towerJ P (closedModulatorCandidate P x) = closedTomita P x :=
  towerJ_involutive P (closedTomita P x)

theorem local_vector_mem_domain {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    ((tof P N a : TowerPre P) : TowerHilbert P) ∈ closedTomitaDomain P :=
  ⟨((tof P N (Matrix.conjTranspose a) : TowerPre P) : TowerHilbert P),
    subset_closure (local_tomita_graph a)⟩

theorem closedTomita_local {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    closedTomita P ⟨((tof P N a : TowerPre P) : TowerHilbert P),
      local_vector_mem_domain a⟩ =
      ((tof P N (Matrix.conjTranspose a) : TowerPre P) : TowerHilbert P) := by
  exact tomita_graph_closure_single_valued _ _ _
    (closedTomita_graph ⟨_, local_vector_mem_domain a⟩)
    (subset_closure (local_tomita_graph a))

/-- O candidato reproduz exatamente o modulador de meia potência no andar. -/
theorem modulatorCandidate_local {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    closedModulatorCandidate P ⟨((tof P N a : TowerPre P) : TowerHilbert P),
      local_vector_mem_domain a⟩ =
      ((tof P N (towerDeltaHalfLevel P N a) : TowerPre P) : TowerHilbert P) := by
  change towerJ P (closedTomita P
    (⟨((tof P N a : TowerPre P) : TowerHilbert P), local_vector_mem_domain a⟩ :
      closedTomitaDomain P)) = _
  rw [closedTomita_local, towerJ_coe, profileJpre_tof]
  congr 2
  rw [profileJlevel_eq, Matrix.conjTranspose_conjTranspose]
  rfl

#print axioms closedModulatorCandidate
#print axioms modulatorCandidate_is_closed
#print axioms modulatorCandidate_domain_dense
#print axioms candidate_factorization
#print axioms modulatorCandidate_local

end
end ChatgptAudit
