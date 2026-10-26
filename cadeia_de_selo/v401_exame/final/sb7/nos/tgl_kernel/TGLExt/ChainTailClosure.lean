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
import TGLExt.ChainTail

set_option autoImplicit false
namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

theorem chain_tail_mem_factor (N : ℕ) {x : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainTailClosure P N) : x ∈ theFactorObject P := by
  have hsub : (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) ⊆
      (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
    fun _ h => chain_local_mem_factor h
  have hfirst := StarSubalgebra.centralizer_le ℂ _ _ hsub
  have hsecond := StarSubalgebra.centralizer_le ℂ _ _ hfirst
  have h := hsecond hx
  change x ∈ ((StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P))) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) at h
  rw [StarSubalgebra.coe_centralizer_centralizer,StarMemClass.star_coe_eq,
    Set.union_self,VonNeumannAlgebra.centralizer_centralizer] at h
  exact h

theorem chain_tail_antitone : Antitone (chainTailClosure P) := by
  intro m n hmn
  have hsub := chain_isotony (P := P) (Set.Ici_subset_Ici.mpr hmn)
  exact StarSubalgebra.centralizer_le ℂ _ _
    (StarSubalgebra.centralizer_le ℂ _ _ hsub)

theorem chain_tail_exact (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    (∀ N, x ∈ chainTailClosure P N) ↔
    ∃ c : ℂ, x = c • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
  constructor
  · intro ht
    exact chain_tail_intersection_iff x |>.mp ⟨chain_tail_mem_factor 0 (ht 0),ht⟩
  · intro h
    exact (chain_tail_intersection_iff x |>.mpr h).2

#print axioms chain_tail_mem_factor
#print axioms chain_tail_antitone
#print axioms chain_tail_exact
end
end ChatgptAudit
