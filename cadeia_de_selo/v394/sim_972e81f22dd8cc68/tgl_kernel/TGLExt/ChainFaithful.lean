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
import TGLExt.ChainVolumePositive

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt Matrix
open scoped Kronecker
noncomputable section
variable {P : SiteProfile}

theorem lastSiteMatrix_injective (n : ℕ) : Function.Injective (lastSiteMatrix n) := by
  intro a b h
  cases n with
  | zero => exact h
  | succ n =>
    let k : chainIdx n := Classical.choice inferInstance
    ext i j
    have he := congrArg (fun m => m (k,i) (k,j)) h
    simpa [lastSiteMatrix,Matrix.kroneckerMap_apply] using he

theorem siteOperator_injective (n : ℕ) : Function.Injective (siteOperator P n) := by
  intro a b h
  exact lastSiteMatrix_injective n (towerPi_injective P n h)

theorem site_noncommutation (n : ℕ) :
    siteOperator P n (Matrix.single 0 0 1) * siteOperator P n (Matrix.single 0 1 1) ≠
    siteOperator P n (Matrix.single 0 1 1) * siteOperator P n (Matrix.single 0 0 1) := by
  intro h
  rw [← siteOperator_mul,← siteOperator_mul] at h
  have he := siteOperator_injective n h
  have hc := congrArg (fun m => m 0 1) he
  norm_num [Matrix.mul_apply,Fin.sum_univ_two,Matrix.single_apply] at hc

theorem site_offdiagonal_not_local {J : Set ℕ} {n : ℕ} (hn : n ∉ J) :
    siteOperator P n (Matrix.single 0 1 1) ∉ chainLocalAlgebra P J := by
  intro hx
  have hd : Disjoint ({n} : Set ℕ) J := Set.disjoint_singleton_left.mpr hn
  have he : siteOperator P n (Matrix.single 0 0 1) ∈ chainLocalAlgebra P {n} :=
    StarAlgebra.subset_adjoin ℂ (chainGenerators P {n}) ⟨n,rfl,_,rfl⟩
  exact site_noncommutation n (chain_locality hd he hx)

theorem chain_order_faithful {I J : Set ℕ} :
    chainLocalAlgebra P I ≤ chainLocalAlgebra P J ↔ I ⊆ J := by
  constructor
  · intro h n hn
    by_contra hj
    exact site_offdiagonal_not_local hj (h
      (StarAlgebra.subset_adjoin ℂ (chainGenerators P I) ⟨n,hn,Matrix.single 0 1 1,rfl⟩))
  · exact chain_isotony

theorem chain_localization_injective : Function.Injective (chainLocalAlgebra P) := by
  intro I J h
  exact Set.Subset.antisymm (chain_order_faithful.mp h.le) (chain_order_faithful.mp h.ge)

#print axioms site_noncommutation
#print axioms chain_order_faithful
#print axioms chain_localization_injective
end
end ChatgptAudit
