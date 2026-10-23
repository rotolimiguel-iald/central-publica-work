-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_003 (05/09/2026), transposta em 05/09/2026
-- A REDE DA CADEIA: intervalos A(I) fieis (isotonia forte A(I)<=A(J) <-> I<=J),
--   localidade, prefixo=andar, CAUDA ESCALAR (chain_tail_exact), volume q_I aditivo
--   com calibracao omega(q_I)=Sum P(i) e a NECESSIDADE da uniformidade provada.
-- Auditoria da gerencia: hashes 17/17; recompilacao 11/11 exit 0; sonda 55/55 trio.
-- Transposicao MECANICA (cabecalho + prefixo TGLExt. nos imports da bancada).
-- Namespace ChatgptAudit = procedencia. NAO move gate; nao e fisica.
-- [OPEN] declarados pela propria bancada: E_I geral; shift global rho (obstrucao
--   MEDIDA: shift normal nos geradores exige perfil estacionario — contraexemplo
--   alternado 1/3,2/3); inclusao meio-lateral CONTINUA.
-- ---------------------------------------------------------------------
import TGLExt.ChainPrefix

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

def chainTailClosure (P : SiteProfile) (N : ℕ) :
    StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set (TowerHilbert P →L[ℂ] TowerHilbert P))

theorem prefix_mem_tail_commutant (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P a ∈ StarSubalgebra.centralizer ℂ (chainLocalAlgebra P (Set.Ici (N+1)) : Set _) := by
  have hd : Disjoint (Set.Iic N) (Set.Ici (N+1)) := by
    rw [Set.disjoint_left]
    intro k hk hl
    change k ≤ N at hk
    change N+1 ≤ k at hl
    omega
  rw [StarSubalgebra.mem_centralizer_iff]
  intro b hb
  exact ⟨(chain_locality hd (towerPi_mem_chain_prefix N a) hb).symm,
    (chain_locality hd (towerPi_mem_chain_prefix N a) (star_mem hb)).symm⟩

theorem chain_tail_intersection_scalar (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) (ht : ∀ N, x ∈ chainTailClosure P N) :
    x = omegaState P x • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
  apply commutes_all_levels_scalar x hx
  intro N a
  have h := ht (N+1)
  change x ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (chainLocalAlgebra P (Set.Ici (N+1)) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) at h
  rw [StarSubalgebra.mem_centralizer_iff] at h
  exact (h (towerPi P a) (prefix_mem_tail_commutant N a)).1

theorem chain_tail_intersection_iff (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    (x ∈ theFactorObject P ∧ ∀ N, x ∈ chainTailClosure P N) ↔
    ∃ c : ℂ, x = c • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
  constructor
  · rintro ⟨hx,ht⟩
    exact ⟨omegaState P x,chain_tail_intersection_scalar x hx ht⟩
  · rintro ⟨c,rfl⟩
    exact ⟨(theFactorObject P).smul_mem (one_mem _) c,
      fun N => (chainTailClosure P N).smul_mem (one_mem _) c⟩

#print axioms chain_tail_intersection_iff
end
end ChatgptAudit
