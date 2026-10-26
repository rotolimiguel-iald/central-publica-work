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
import TGLExt.ModularProbe
import Mathlib.Analysis.InnerProductSpace.Projection.Basic

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit
open TGLExt Filter Topology
noncomputable section
variable {P : SiteProfile}

def levelEmbedding (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ →ₗ[ℂ] TowerHilbert P where
  toFun := fun a => ((tof P N a : TowerPre P) : TowerHilbert P)
  map_add' := by intro a b; rw [← tof_add_same, UniformSpace.Completion.coe_add]
  map_smul' := by intro c a; rw [← tof_smul, UniformSpace.Completion.coe_smul]; rfl

def levelSpace (P : SiteProfile) (N : ℕ) : Submodule ℂ (TowerHilbert P) :=
  LinearMap.range (levelEmbedding P N)

instance levelSpace_finite (P : SiteProfile) (N : ℕ) :
    FiniteDimensional ℂ (levelSpace P N) := by
  unfold levelSpace
  infer_instance

instance levelSpace_complete (P : SiteProfile) (N : ℕ) :
    CompleteSpace (levelSpace P N) := FiniteDimensional.complete ℂ _

theorem levelSpace_mono : Monotone (levelSpace P) := by
  intro N M h x hx
  obtain ⟨a, rfl⟩ := hx
  refine ⟨tPush h a, ?_⟩
  change ((tof P M (tPush h a) : TowerPre P) : TowerHilbert P) = _
  rw [tof_tPush]
  rfl

def levelProject (P : SiteProfile) (N : ℕ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  (levelSpace P N).starProjection

theorem levelProject_mem (N : ℕ) (x : TowerHilbert P) :
    levelProject P N x ∈ levelSpace P N :=
  ((levelSpace P N).orthogonalProjectionOnto x).property

theorem levelProject_fixed {N : ℕ} {x : TowerHilbert P} (hx : x ∈ levelSpace P N) :
    levelProject P N x = x := Submodule.starProjection_eq_self_iff.mpr hx

theorem levelProject_inner {N : ℕ} {b : TowerHilbert P}
    (hb : b ∈ levelSpace P N) (x : TowerHilbert P) :
    inner ℂ b (levelProject P N x) = inner ℂ b x := by
  change inner ℂ b ((levelSpace P N).starProjection x) = inner ℂ b x
  rw [← Submodule.inner_starProjection_left_eq_right]
  exact congrArg (fun v => inner ℂ v x) (levelProject_fixed hb)

theorem levelProject_tendsto (x : TowerHilbert P) :
    Tendsto (fun N => levelProject P N x) atTop (𝓝 x) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨v, hv⟩ := Metric.denseRange_iff.mp (towerPre_denseRange (P := P)) x
    (ε / 2) (half_pos hε)
  obtain ⟨M, a, rfl⟩ := exists_tof v
  refine ⟨M, fun N hMN => ?_⟩
  let z : TowerHilbert P := ((tof P M a : TowerPre P) : TowerHilbert P)
  have hz : z ∈ levelSpace P N := levelSpace_mono hMN ⟨a, rfl⟩
  have heq : levelProject P N x - x = levelProject P N (x - z) + (z - x) := by
    rw [map_sub, levelProject_fixed hz]
    abel
  rw [dist_eq_norm, heq]
  have hn := (levelSpace P N).norm_starProjection_apply_le (x - z)
  have hv' : ‖x - z‖ < ε / 2 := by simpa only [dist_eq_norm] using hv
  calc
    ‖levelProject P N (x - z) + (z - x)‖ ≤
        ‖levelProject P N (x - z)‖ + ‖z - x‖ := norm_add_le _ _
    _ ≤ ‖x - z‖ + ‖x - z‖ := by rw [norm_sub_rev z x]; exact add_le_add hn le_rfl
    _ < ε := by linarith

theorem levelSpace_mem_domain {N : ℕ} {x : TowerHilbert P} (hx : x ∈ levelSpace P N) :
    x ∈ closedTomitaDomain P := by
  obtain ⟨a, rfl⟩ := hx
  exact local_vector_mem_domain a

theorem modulator_preserves_level {N : ℕ} (x : closedTomitaDomain P)
    (hx : (x : TowerHilbert P) ∈ levelSpace P N) :
    closedModulatorCandidate P x ∈ levelSpace P N := by
  obtain ⟨a, ha⟩ := hx
  have heq : x = ⟨levelEmbedding P N a, local_vector_mem_domain a⟩ :=
    Subtype.ext ha.symm
  rw [heq]
  change closedModulatorCandidate P ⟨((tof P N a : TowerPre P) : TowerHilbert P),
    local_vector_mem_domain a⟩ ∈ levelSpace P N
  rw [modulatorCandidate_local]
  exact ⟨towerDeltaHalfLevel P N a, rfl⟩

theorem modulator_pairing_level (x : closedTomitaDomain P) {N : ℕ}
    (b : levelSpace P N) :
    inner ℂ (b : TowerHilbert P) (closedModulatorCandidate P x) =
      inner ℂ (closedModulatorCandidate P ⟨b, levelSpace_mem_domain b.property⟩)
        (x : TowerHilbert P) := by
  obtain ⟨a, ha⟩ := b.property
  have heq : b = ⟨levelEmbedding P N a, ⟨a, rfl⟩⟩ := Subtype.ext ha.symm
  subst b
  change inner ℂ ((tof P N a : TowerPre P) : TowerHilbert P) (closedModulatorCandidate P x) =
    inner ℂ (closedModulatorCandidate P ⟨((tof P N a : TowerPre P) : TowerHilbert P),
      local_vector_mem_domain a⟩) (x : TowerHilbert P)
  rw [modulatorCandidate_local]
  exact modulator_pairing_local x a

#print axioms levelProject_tendsto
#print axioms modulator_preserves_level
#print axioms modulator_pairing_level
end
end ChatgptAudit
