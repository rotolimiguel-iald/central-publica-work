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
import TGLExt.ExpectationBimodule

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit
open TGLExt Matrix UniformSpace
noncomputable section
variable {P : SiteProfile}

def weightedStepSlice (P : SiteProfile) (N : ℕ)
    (x : Matrix (chainIdx (N+1)) (chainIdx (N+1)) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  fun i j => ∑ r : Fin 2, (siteW (P.w (N+1)) r : ℂ) * x (i,r) (j,r)

theorem weightedStepSlice_pairing (N : ℕ)
    (b : Matrix (chainIdx N) (chainIdx N) ℂ)
    (x : Matrix (chainIdx (N+1)) (chainIdx (N+1)) ℂ) :
    tInner P (N+1) (towerStep b) x = tInner P N b (weightedStepSlice P N x) := by
  rw [tInner_apply, tInner_apply, Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro k _
  simp only [Fintype.sum_prod_type, towerW, towerStep, Matrix.kroneckerMap_apply,
    Matrix.one_apply, apply_ite, map_zero, mul_one, mul_zero,
    ite_mul, zero_mul, Finset.sum_ite_eq', Finset.mem_univ, if_true,
    weightedStepSlice, Complex.ofReal_mul]
  simp only [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro r _
  ring

theorem expectation_step_slice (N : ℕ)
    (x : Matrix (chainIdx (N+1)) (chainIdx (N+1)) ℂ) :
    towerExpectation P N (towerPi P x) = towerPi P (weightedStepSlice P N x) := by
  apply factor_eq_of_omega (expectation_mem_factor _ _) (towerPi_mem_factor _)
  rw [expectation_omega, towerPi_omega, towerPi_omega]
  apply level_inner_ext (levelProject_mem _ _) ⟨_,rfl⟩
  intro v hv
  obtain ⟨b,rfl⟩ := hv
  rw [levelProject_inner ⟨b,rfl⟩]
  change inner ℂ ((tof P N b : TowerPre P) : TowerHilbert P)
      ((tof P (N+1) x : TowerPre P) : TowerHilbert P) =
    inner ℂ ((tof P N b : TowerPre P) : TowerHilbert P)
      ((tof P N (weightedStepSlice P N x) : TowerPre P) : TowerHilbert P)
  rw [← tof_towerStep N b, Completion.inner_coe, Completion.inner_coe]
  change innerPre P (tof P (N+1) (towerStep b)) (tof P (N+1) x) =
    innerPre P (tof P (N+1) (towerStep b)) (tof P N (weightedStepSlice P N x))
  rw [tof_towerStep, innerPre_tof_at (Nat.le_succ N) (le_refl (N+1)),
    tPush_self, innerPre_tof_same]
  rw [tPush_succ (le_refl N), tPush_self]
  exact weightedStepSlice_pairing N b x

#print axioms expectation_step_slice
end
end ChatgptAudit
