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
import TGLExt.LocalTowerProjections
import TGLExt.ModularPower

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit
open TGLExt UniformSpace
noncomputable section
variable {P : SiteProfile}

theorem levelEmbedding_injective (P : SiteProfile) (N : ℕ) :
    Function.Injective (levelEmbedding P N) := by
  intro a b h
  have hz : levelEmbedding P N (a-b) = 0 := by rw [map_sub, h, sub_self]
  apply sub_eq_zero.mp
  apply tInner_self_definite P N
  calc
    tInner P N (a-b) (a-b) = inner ℂ
        ((tof P N (a-b) : TowerPre P) : TowerHilbert P)
        ((tof P N (a-b) : TowerPre P) : TowerHilbert P) := by
      rw [Completion.inner_coe]
      exact (innerPre_tof_same N (a-b) (a-b)).symm
    _ = 0 := by change inner ℂ (levelEmbedding P N (a-b)) (levelEmbedding P N (a-b)) = 0; rw [hz, inner_zero_left]

def levelDecode (P : SiteProfile) (N : ℕ) :
    levelSpace P N ≃ₗ[ℂ] Matrix (chainIdx N) (chainIdx N) ℂ :=
  (LinearEquiv.ofInjective (levelEmbedding P N) (levelEmbedding_injective P N)).symm

theorem levelDecode_embedding (N : ℕ) (v : levelSpace P N) :
    levelEmbedding P N (levelDecode P N v) = (v : TowerHilbert P) := by
  exact congrArg Subtype.val
    ((LinearEquiv.ofInjective (levelEmbedding P N) (levelEmbedding_injective P N)).apply_symm_apply v)

def expectationMatrix (P : SiteProfile) (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  levelDecode P N ⟨levelProject P N (x (hOmega P)), levelProject_mem N _⟩

def towerExpectation (P : SiteProfile) (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  towerPi P (expectationMatrix P N x)

theorem expectation_omega (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N x (hOmega P) = levelProject P N (x (hOmega P)) := by
  rw [towerExpectation, towerPi_omega]
  exact levelDecode_embedding N _

theorem expectation_into (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    ∃ a : Matrix (chainIdx N) (chainIdx N) ℂ, towerExpectation P N x = towerPi P a :=
  ⟨expectationMatrix P N x, rfl⟩

theorem expectation_mem_factor (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N x ∈ theFactorObject P := towerPi_mem_factor _

theorem factor_eq_of_omega {x y : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ theFactorObject P) (hy : y ∈ theFactorObject P)
    (h : x (hOmega P) = y (hOmega P)) : x = y := by
  apply sub_eq_zero.mp
  apply factor_omega_separating ((theFactorObject P).sub_mem hx hy)
  change x (hOmega P) - y (hOmega P) = 0
  exact sub_eq_zero.mpr h

theorem expectation_fixes (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerExpectation P N (towerPi P a) = towerPi P a := by
  apply factor_eq_of_omega (expectation_mem_factor _ _) (towerPi_mem_factor _)
  rw [expectation_omega, towerPi_omega]
  exact levelProject_fixed ⟨a,rfl⟩

theorem expectation_idempotent (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N (towerExpectation P N x) = towerExpectation P N x :=
  expectation_fixes N _

theorem omega_mem_level (N : ℕ) : hOmega P ∈ levelSpace P N := by
  refine ⟨1, ?_⟩
  change ((tof P N 1 : TowerPre P) : TowerHilbert P) = _
  rw [← tPush_one (Nat.zero_le N), tof_tPush]
  rfl

theorem expectation_preserves_state (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (towerExpectation P N x) = omegaState P x := by
  unfold omegaState
  rw [expectation_omega]
  exact levelProject_inner (omega_mem_level N) _

theorem expectation_add (N : ℕ) (x y : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N (x+y) = towerExpectation P N x + towerExpectation P N y := by
  apply factor_eq_of_omega (expectation_mem_factor _ _)
    ((theFactorObject P).add_mem (expectation_mem_factor _ _) (expectation_mem_factor _ _))
  simp only [expectation_omega, add_apply, map_add]

theorem expectation_smul (N : ℕ) (c : ℂ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N (c • x) = c • towerExpectation P N x := by
  apply factor_eq_of_omega (expectation_mem_factor _ _)
    ((theFactorObject P).smul_mem (expectation_mem_factor _ _) c)
  simp only [expectation_omega, smul_apply, map_smul]

def expectationLinear (P : SiteProfile) (N : ℕ) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) →ₗ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toFun := towerExpectation P N
  map_add' := expectation_add N
  map_smul' := expectation_smul N

#print axioms expectation_fixes
#print axioms expectation_idempotent
#print axioms expectation_preserves_state
end
end ChatgptAudit
