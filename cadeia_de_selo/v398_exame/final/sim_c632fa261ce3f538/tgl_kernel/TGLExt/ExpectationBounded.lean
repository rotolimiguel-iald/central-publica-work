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
import TGLExt.TowerExpectation

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

def levelRepresent (P : SiteProfile) (N : ℕ) :
    levelSpace P N →ₗ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toFun := fun v => towerPi P (levelDecode P N v)
  map_add' := by
    intro v w
    apply factor_eq_of_omega (towerPi_mem_factor _)
      ((theFactorObject P).add_mem (towerPi_mem_factor _) (towerPi_mem_factor _))
    simp only [add_apply, towerPi_omega]
    change levelEmbedding P N (levelDecode P N (v+w)) =
      levelEmbedding P N (levelDecode P N v) + levelEmbedding P N (levelDecode P N w)
    simp only [levelDecode_embedding, Submodule.coe_add]
  map_smul' := by
    intro c v
    apply factor_eq_of_omega (towerPi_mem_factor _)
      ((theFactorObject P).smul_mem (towerPi_mem_factor _) c)
    simp only [smul_apply, towerPi_omega]
    change levelEmbedding P N (levelDecode P N (c • v)) =
      c • levelEmbedding P N (levelDecode P N v)
    simp only [levelDecode_embedding, Submodule.coe_smul]

def expectationCLM (P : SiteProfile) (N : ℕ) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) →L[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toLinearMap := expectationLinear P N
  cont := by
    have heval : Continuous (fun x : TowerHilbert P →L[ℂ] TowerHilbert P => x (hOmega P)) := by
      fun_prop
    exact (levelRepresent P N).continuous_of_finiteDimensional.comp
      ((levelSpace P N).orthogonalProjectionOnto.continuous.comp heval)

theorem expectation_bounded (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    ‖towerExpectation P N x‖ ≤ ‖expectationCLM P N‖ * ‖x‖ :=
  (expectationCLM P N).le_opNorm x

#print axioms expectation_bounded
end
end ChatgptAudit
