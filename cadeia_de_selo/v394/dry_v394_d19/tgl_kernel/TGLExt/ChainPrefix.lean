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
import TGLExt.ChainLocality

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit
open TGLExt Matrix
open scoped Kronecker
noncomputable section
variable {P : SiteProfile}

def towerPiLinear (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ →ₗ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toFun := towerPi P
  map_add' := towerPi_add
  map_smul' := towerPi_smul

theorem towerPi_sum {ι : Type*} (I : Finset ι) {N : ℕ}
    (a : ι → Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (∑ i ∈ I, a i) = ∑ i ∈ I, towerPi P (a i) :=
  map_sum (towerPiLinear P N) a I

def levelOperatorAlgebra (P : SiteProfile) (N : ℕ) :
    StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) where
  carrier := Set.range (fun a : Matrix (chainIdx N) (chainIdx N) ℂ => towerPi P a)
  zero_mem' := ⟨0,(towerPiLinear P N).map_zero⟩
  one_mem' := ⟨1,towerPi_one N⟩
  add_mem' := by rintro x y ⟨a,rfl⟩ ⟨b,rfl⟩; exact ⟨a+b,towerPi_add a b⟩
  mul_mem' := by rintro x y ⟨a,rfl⟩ ⟨b,rfl⟩; exact ⟨a*b,towerPi_mul N a b⟩
  algebraMap_mem' := by
    intro c
    refine ⟨c • 1, ?_⟩
    change towerPi P (c • (1 : Matrix (chainIdx N) (chainIdx N) ℂ)) = _
    rw [towerPi_smul, towerPi_one, Algebra.algebraMap_eq_smul_one]
  star_mem' := by
    rintro x ⟨a,rfl⟩
    exact ⟨aᴴ, by change towerPi P aᴴ = star (towerPi P a); rw [towerPi_star, ContinuousLinearMap.star_eq_adjoint]⟩

theorem matrix_slice_expansion (N : ℕ)
    (x : Matrix (chainIdx (N+1)) (chainIdx (N+1)) ℂ) :
    x = ∑ s : Fin 2, ∑ t : Fin 2, cSlice s t x ⊗ₖ Matrix.single s t (1 : ℂ) := by
  ext ⟨i,s⟩ ⟨j,t⟩
  fin_cases s <;> fin_cases t <;>
    simp [Matrix.sum_apply, Matrix.kroneckerMap_apply, Matrix.single_apply, cSlice, mul_ite]

theorem towerPi_mem_chain_prefix (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P a ∈ chainLocalAlgebra P (Set.Iic N) := by
  induction N with
  | zero => exact StarAlgebra.subset_adjoin ℂ _ ⟨0,le_refl 0,a,rfl⟩
  | succ N ih =>
    rw [matrix_slice_expansion N a, towerPi_sum]
    apply (chainLocalAlgebra P (Set.Iic (N+1))).sum_mem
    intro s _
    rw [towerPi_sum]
    apply (chainLocalAlgebra P (Set.Iic (N+1))).sum_mem
    intro t _
    have hleft : towerPi P (towerStep (cSlice s t a)) ∈ chainLocalAlgebra P (Set.Iic (N+1)) := by
      rw [towerPi_step]
      apply chain_isotony (Set.Iic_subset_Iic.mpr (Nat.le_succ N))
      exact ih _
    have hright : towerPi P (lastSiteMatrix (N+1) (Matrix.single s t 1)) ∈
        chainLocalAlgebra P (Set.Iic (N+1)) :=
      StarAlgebra.subset_adjoin ℂ (chainGenerators P (Set.Iic (N+1)))
        ⟨N+1,Nat.le_refl (N+1),Matrix.single s t 1,rfl⟩
    have hmul := (chainLocalAlgebra P (Set.Iic (N+1))).mul_mem hleft hright
    rw [← towerPi_mul] at hmul
    simpa only [towerStep,lastSiteMatrix,← Matrix.mul_kronecker_mul,mul_one,one_mul] using hmul

theorem chain_prefix_eq_level (N : ℕ) :
    chainLocalAlgebra P (Set.Iic N) = levelOperatorAlgebra P N := by
  apply le_antisymm
  · apply StarAlgebra.adjoin_le
    rintro x ⟨n,hn,a,rfl⟩
    exact ⟨tPush hn (lastSiteMatrix n a),towerPi_compat hn _⟩
  · rintro x ⟨a,rfl⟩
    exact towerPi_mem_chain_prefix N a

theorem prefix_expectation_into (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N x ∈ chainLocalAlgebra P (Set.Iic N) := by
  rw [chain_prefix_eq_level]
  exact ⟨expectationMatrix P N x,rfl⟩

#print axioms chain_prefix_eq_level
#print axioms prefix_expectation_into
end
end ChatgptAudit
