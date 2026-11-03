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
import TGLExt.ModulatorPolar

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit
open TGLExt Filter Topology
noncomputable section
variable {P : SiteProfile}

/-- Domínio do quadrado: x pertence ao domínio de A e Ax também. -/
def modularSquareDomain (P : SiteProfile) : Submodule ℂ (TowerHilbert P) :=
  ((closedModulatorCandidate P).domain.comap (closedModulatorCandidate P).toFun).map
    (closedModulatorCandidate P).domain.subtype

theorem squareDomain_le : modularSquareDomain P ≤ (closedModulatorCandidate P).domain := by
  rintro x ⟨z, hz, rfl⟩
  exact z.property

def squareInput (P : SiteProfile) : modularSquareDomain P →ₗ[ℂ] (closedModulatorCandidate P).domain :=
  Submodule.inclusion squareDomain_le

theorem squareInput_image_mem (x : modularSquareDomain P) :
    closedModulatorCandidate P (squareInput P x) ∈ (closedModulatorCandidate P).domain := by
  obtain ⟨z, hz, heq⟩ := x.property
  have h : z = squareInput P x := Subtype.ext heq
  exact h ▸ hz

def squareMid (P : SiteProfile) : modularSquareDomain P →ₗ[ℂ] (closedModulatorCandidate P).domain :=
  ((closedModulatorCandidate P).toFun.comp (squareInput P)).codRestrict
    (closedModulatorCandidate P).domain squareInput_image_mem

def towerDeltaClosed (P : SiteProfile) : TowerHilbert P →ₗ.[ℂ] TowerHilbert P where
  domain := modularSquareDomain P
  toFun := (closedModulatorCandidate P).toFun.comp (squareMid P)

theorem squareInput_coe (x : modularSquareDomain P) :
    (squareInput P x : TowerHilbert P) = (x : TowerHilbert P) := rfl

theorem squareMid_coe (x : modularSquareDomain P) :
    (squareMid P x : TowerHilbert P) = closedModulatorCandidate P (squareInput P x) := rfl

theorem delta_apply (x : modularSquareDomain P) :
    towerDeltaClosed P x = closedModulatorCandidate P (squareMid P x) := rfl

theorem squareDomain_iff (x : TowerHilbert P) :
    x ∈ modularSquareDomain P ↔
      ∃ hx : x ∈ (closedModulatorCandidate P).domain,
        closedModulatorCandidate P ⟨x, hx⟩ ∈ (closedModulatorCandidate P).domain := by
  constructor
  · intro hx
    exact ⟨squareDomain_le hx, squareInput_image_mem ⟨x, hx⟩⟩
  · rintro ⟨hx, hax⟩
    exact ⟨⟨x, hx⟩, hax, rfl⟩

theorem delta_is_symmetric : (towerDeltaClosed P).IsFormalAdjoint (towerDeltaClosed P) := by
  intro x y
  calc
    _ = inner ℂ (squareMid P x : TowerHilbert P)
        (closedModulatorCandidate P (squareInput P y)) :=
      modulator_is_symmetric (squareMid P x) (squareInput P y)
    _ = inner ℂ (squareInput P x : TowerHilbert P)
        (closedModulatorCandidate P (squareMid P y)) :=
      modulator_is_symmetric (squareInput P x) (squareMid P y)
    _ = _ := rfl

theorem delta_quadratic (x : modularSquareDomain P) :
    inner ℂ (x : TowerHilbert P) (towerDeltaClosed P x) =
      inner ℂ (closedModulatorCandidate P (squareInput P x))
        (closedModulatorCandidate P (squareInput P x)) :=
  (modulator_is_symmetric (squareInput P x) (squareMid P x)).symm

theorem delta_positive (x : modularSquareDomain P) :
    0 ≤ (inner ℂ (x : TowerHilbert P) (towerDeltaClosed P x)).re := by
  rw [delta_quadratic]
  exact inner_self_nonneg (𝕜 := ℂ) (x := closedModulatorCandidate P (squareInput P x))

theorem levelSpace_mem_squareDomain {N : ℕ} {x : TowerHilbert P}
    (hx : x ∈ levelSpace P N) : x ∈ modularSquareDomain P := by
  rw [squareDomain_iff]
  refine ⟨levelSpace_mem_domain hx, ?_⟩
  exact levelSpace_mem_domain (modulator_preserves_level ⟨x, levelSpace_mem_domain hx⟩ hx)

theorem squareDomain_dense : Dense (modularSquareDomain P : Set (TowerHilbert P)) := by
  apply Dense.mono ?_ (towerPre_denseRange (P := P))
  rintro _ ⟨v, rfl⟩
  obtain ⟨N, a, rfl⟩ := exists_tof v
  exact levelSpace_mem_squareDomain (N := N) ⟨a, rfl⟩

theorem square_local (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerDeltaClosed P ⟨((tof P N a : TowerPre P) : TowerHilbert P),
      levelSpace_mem_squareDomain (N := N) ⟨a, rfl⟩⟩ =
        ((tof P N (towerDeltaLevel P N a) : TowerPre P) : TowerHilbert P) := by
  let x : modularSquareDomain P := ⟨((tof P N a : TowerPre P) : TowerHilbert P),
    levelSpace_mem_squareDomain (N := N) ⟨a, rfl⟩⟩
  have hm : squareMid P x =
      ⟨((tof P N (towerDeltaHalfLevel P N a) : TowerPre P) : TowerHilbert P),
        local_vector_mem_domain _⟩ := by
    apply Subtype.ext
    exact modulatorCandidate_local a
  change closedModulatorCandidate P (squareMid P x) = _
  rw [hm, modulatorCandidate_local, delta_is_the_square_of_its_half]

#print axioms squareDomain_iff
#print axioms delta_positive
#print axioms squareDomain_dense
#print axioms square_local
end
end ChatgptAudit
