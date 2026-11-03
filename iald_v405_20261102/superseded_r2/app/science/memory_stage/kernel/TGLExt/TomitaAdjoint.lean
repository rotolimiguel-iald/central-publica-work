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
import TGLExt.ModularSquareAdjoint

set_option autoImplicit false
set_option maxHeartbeats 3000000

namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

/-- Domínio do adjunto antilinear: Jy pertence ao domínio da parte positiva. -/
def tomitaAdjointDomain (P : SiteProfile) : Submodule ℂ (TowerHilbert P) :=
  (closedModulatorCandidate P).domain.comap (towerJequiv P).toLinearEquiv.toLinearMap

def adjointJInput (P : SiteProfile) :
    tomitaAdjointDomain P →ₛₗ[starRingEnd ℂ] (closedModulatorCandidate P).domain :=
  ((towerJequiv P).toLinearEquiv.toLinearMap.domRestrict (tomitaAdjointDomain P)).codRestrict
    (closedModulatorCandidate P).domain (fun y => y.property)

def closedTomitaAdjoint (P : SiteProfile) :
    TowerHilbert P →ₛₗ.[starRingEnd ℂ] TowerHilbert P where
  domain := tomitaAdjointDomain P
  toFun := (closedModulatorCandidate P).toFun.comp (adjointJInput P)

theorem adjointJInput_coe (y : tomitaAdjointDomain P) :
    (adjointJInput P y : TowerHilbert P) = towerJ P (y : TowerHilbert P) := rfl

theorem tomita_pairing_with_J (x : closedTomitaDomain P) (y : TowerHilbert P) :
    inner ℂ (closedTomita P x) y =
      inner ℂ (towerJ P y) (closedModulatorCandidate P x) := by
  rw [← candidate_factorization x]
  have h := towerJ_inner_flip (towerJ P (closedModulatorCandidate P x)) (towerJ P y)
  simpa only [towerJ_involutive] using h

/-- Convenção do adjunto antilinear: <Sx,y> = <S†y,x>. -/
theorem tomita_adjoint_pairing (x : closedTomitaDomain P) (y : tomitaAdjointDomain P) :
    inner ℂ (closedTomita P x) (y : TowerHilbert P) =
      inner ℂ (closedTomitaAdjoint P y) (x : TowerHilbert P) := by
  rw [tomita_pairing_with_J]
  exact (modulator_is_symmetric (adjointJInput P y) x).symm

/-- Maximalidade: todo par que satisfaz a identidade do adjunto entra no domínio definido. -/
theorem tomita_adjoint_maximal {y z : TowerHilbert P}
    (h : ∀ x : closedTomitaDomain P,
      inner ℂ (closedTomita P x) y = inner ℂ z (x : TowerHilbert P)) :
    ∃ hy : y ∈ tomitaAdjointDomain P, closedTomitaAdjoint P ⟨y, hy⟩ = z := by
  have hadj : towerJ P y ∈ (LinearPMap.adjoint (closedModulatorCandidate P)).domain := by
    apply LinearPMap.mem_adjoint_domain_of_exists
    refine ⟨z, fun x => ?_⟩
    rw [← h x, tomita_pairing_with_J]
  have hy : y ∈ tomitaAdjointDomain P := by
    change towerJ P y ∈ (closedModulatorCandidate P).domain
    rwa [LinearPMap.isSelfAdjoint_def.mp (modulatorCandidate_selfadjoint (P := P))] at hadj
  refine ⟨hy, ?_⟩
  apply (closedTomita_domain_dense (P := P)).eq_of_inner_left ℂ
  intro x hx
  exact (tomita_adjoint_pairing ⟨x, hx⟩ ⟨y, hy⟩).symm.trans (h ⟨x, hx⟩)

theorem tomita_adjoint_domain_iff (y : TowerHilbert P) :
    y ∈ tomitaAdjointDomain P ↔ ∃ z : TowerHilbert P,
      ∀ x : closedTomitaDomain P,
        inner ℂ (closedTomita P x) y = inner ℂ z (x : TowerHilbert P) := by
  constructor
  · intro hy
    exact ⟨closedTomitaAdjoint P ⟨y, hy⟩, fun x => tomita_adjoint_pairing x ⟨y, hy⟩⟩
  · rintro ⟨z, hz⟩
    exact (tomita_adjoint_maximal hz).choose

theorem tomita_composition_domain (x : closedTomitaDomain P) :
    closedTomita P x ∈ tomitaAdjointDomain P ↔
      closedModulatorCandidate P x ∈ (closedModulatorCandidate P).domain := by
  change towerJ P (closedTomita P x) ∈ (closedModulatorCandidate P).domain ↔ _
  rfl

theorem square_tomita_mem_adjoint (x : modularSquareDomain P) :
    closedTomita P (squareInput P x) ∈ tomitaAdjointDomain P :=
  (tomita_composition_domain (squareInput P x)).mpr (squareInput_image_mem x)

/-- S†S=Δ como valores, no domínio da composição provado acima. -/
theorem tomita_adjoint_comp_is_delta (x : modularSquareDomain P) :
    closedTomitaAdjoint P ⟨closedTomita P (squareInput P x), square_tomita_mem_adjoint x⟩ =
      towerDeltaClosed P x := rfl

theorem delta_quadratic_is_tomita_norm (x : modularSquareDomain P) :
    (inner ℂ (x : TowerHilbert P) (towerDeltaClosed P x)).re =
      ‖closedTomita P (squareInput P x)‖ ^ 2 := by
  rw [delta_quadratic]
  calc
    _ = ‖closedModulatorCandidate P (squareInput P x)‖ ^ 2 :=
      (norm_sq_eq_re_inner (𝕜 := ℂ) _).symm
    _ = _ := congrArg (fun t : ℝ => t ^ 2)
      (towerJ_norm P (closedTomita P (squareInput P x)))

#print axioms tomita_adjoint_pairing
#print axioms tomita_adjoint_maximal
#print axioms tomita_composition_domain
#print axioms tomita_adjoint_comp_is_delta
end
end ChatgptAudit
