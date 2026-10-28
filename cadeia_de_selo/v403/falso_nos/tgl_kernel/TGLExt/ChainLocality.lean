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
import TGLExt.ChainSiteOperators

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

theorem chain_local_mem_factor {I : Set ℕ} {x : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainLocalAlgebra P I) : x ∈ theFactorObject P := by
  have h : chainLocalAlgebra P I ≤ (theFactorObject P).toStarSubalgebra := by
    apply StarAlgebra.adjoin_le
    rintro a ⟨n,hn,b,rfl⟩
    exact siteOperator_mem_factor n b
  exact h hx

theorem chain_generators_commute {I J : Set ℕ} (h : Disjoint I J)
    {x y : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainGenerators P I) (hy : y ∈ chainGenerators P J) : x*y=y*x := by
  obtain ⟨n,hn,a,rfl⟩ := hx
  obtain ⟨m,hm,b,rfl⟩ := hy
  apply siteOperators_commute
  intro he
  subst m
  exact Set.disjoint_left.mp h hn hm

theorem chain_locality {I J : Set ℕ} (h : Disjoint I J)
    {x y : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainLocalAlgebra P I) (hy : y ∈ chainLocalAlgebra P J) : x*y=y*x := by
  have hI : chainLocalAlgebra P I ≤ StarSubalgebra.centralizer ℂ (chainGenerators P J) := by
    apply StarAlgebra.adjoin_le
    intro a ha
    change a ∈ StarSubalgebra.centralizer ℂ (chainGenerators P J)
    rw [StarSubalgebra.mem_centralizer_iff]
    intro b hb
    exact ⟨(chain_generators_commute h ha hb).symm,
      (chain_generators_commute h ha (chain_generators_star hb)).symm⟩
  have hJ : chainLocalAlgebra P J ≤ StarSubalgebra.centralizer ℂ (chainLocalAlgebra P I : Set _) := by
    apply StarAlgebra.adjoin_le
    intro b hb
    change b ∈ StarSubalgebra.centralizer ℂ (chainLocalAlgebra P I : Set _)
    rw [StarSubalgebra.mem_centralizer_iff]
    intro a ha
    have hc := hI ha
    have hs := hI (star_mem ha)
    rw [StarSubalgebra.mem_centralizer_iff] at hc hs
    exact ⟨(hc b hb).1.symm, (hs b hb).1.symm⟩
  have hc := hJ hy
  rw [StarSubalgebra.mem_centralizer_iff] at hc
  exact (hc x hx).1

theorem chain_empty : chainLocalAlgebra P ∅ = ⊥ := by
  unfold chainLocalAlgebra
  have hg : chainGenerators P ∅ = ∅ := by
    ext x
    simp [chainGenerators]
  rw [hg]
  exact le_antisymm (StarAlgebra.adjoin_le (Set.empty_subset _)) bot_le

#print axioms chain_local_mem_factor
#print axioms chain_locality
#print axioms chain_empty
end
end ChatgptAudit
