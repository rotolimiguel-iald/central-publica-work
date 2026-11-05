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
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt Matrix
open scoped Kronecker
noncomputable section
variable {P : SiteProfile}

def siteMark (P : SiteProfile) (n : ℕ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  siteOperator P n (Matrix.single (0 : Fin 2) 0 (1 : ℂ))

theorem siteMark_state (n : ℕ) : omegaState P (siteMark P n) = (P.w n : ℂ) := by
  cases n with
  | zero =>
    change omegaState P (towerPi P (N := 0) (Matrix.single (0 : Fin 2) 0 (1 : ℂ))) = _
    rw [omegaState_pi, tState_single_diag]
    rfl
  | succ n =>
    change omegaState P (towerPi P (N := n+1) ((1 : Matrix (chainIdx n) (chainIdx n) ℂ) ⊗ₖ Matrix.single (0 : Fin 2) 0 (1 : ℂ))) = _
    rw [omegaState_pi (P := P), tState_kron_split P (N := n), tState_one P n, one_mul]
    simp [Matrix.single_apply, siteW]

def chainVolumeObject (P : SiteProfile) (I : Finset ℕ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  ∑ n ∈ I, siteMark P n

theorem chainVolume_local (I : Finset ℕ) : chainVolumeObject P I ∈ chainLocalAlgebra P (I : Set ℕ) := by
  apply (chainLocalAlgebra P (I : Set ℕ)).sum_mem
  intro n hn
  apply StarAlgebra.subset_adjoin
  exact ⟨n,hn,Matrix.single (0 : Fin 2) 0 (1 : ℂ),rfl⟩

theorem chainVolume_additive (I J : Finset ℕ) (h : Disjoint I J) :
    chainVolumeObject P (I ∪ J) = chainVolumeObject P I + chainVolumeObject P J := by
  exact Finset.sum_union h

theorem omega_sum {ι : Type*} (I : Finset ι) (x : ι → TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (∑ i ∈ I, x i) = ∑ i ∈ I, omegaState P (x i) := by
  simp [omegaState, inner_sum]

theorem chainVolume_state (I : Finset ℕ) :
    omegaState P (chainVolumeObject P I) = ((∑ n ∈ I, P.w n : ℝ) : ℂ) := by
  rw [chainVolumeObject, omega_sum]
  simp only [siteMark_state, Complex.ofReal_sum]

theorem chainVolume_uniform (p : ℝ) (hp : ∀ n, P.w n = p) (I : Finset ℕ) :
    omegaState P (chainVolumeObject P I) = (p * I.card : ℝ) := by
  rw [chainVolume_state]
  simp only [hp, Finset.sum_const, nsmul_eq_mul, mul_comm]

theorem constant_calibration_forces_uniform (p : ℝ)
    (h : ∀ I : Finset ℕ, omegaState P (chainVolumeObject P I) = (p * I.card : ℝ)) :
    ∀ n, P.w n = p := by
  intro n
  have hs := h {n}
  rw [chainVolume_state] at hs
  simpa using Complex.ofReal_injective hs

theorem no_bounded_positive_count_calibration (C : ℝ) (hC : 0 < C) :
    ¬ (∀ n : ℕ, C * n ≤ 1) := by
  intro h
  obtain ⟨n,hn⟩ := exists_nat_gt (1/C)
  have hc := (div_lt_iff₀ hC).mp hn
  have hb := h n
  nlinarith

#print axioms chainVolume_state
#print axioms chainVolume_uniform
#print axioms constant_calibration_forces_uniform
#print axioms no_bounded_positive_count_calibration
end
end ChatgptAudit
