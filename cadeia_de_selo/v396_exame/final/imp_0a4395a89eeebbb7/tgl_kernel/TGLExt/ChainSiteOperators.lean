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
import TGLExt.TowerTailRigidity

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt Matrix
open scoped Kronecker
noncomputable section
variable {P : SiteProfile}

def lastSiteMatrix : (n : ℕ) → Matrix (Fin 2) (Fin 2) ℂ → Matrix (chainIdx n) (chainIdx n) ℂ
  | 0,a => a
  | n+1,a => (1 : Matrix (chainIdx n) (chainIdx n) ℂ) ⊗ₖ a

def siteOperator (P : SiteProfile) (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :=
  towerPi P (lastSiteMatrix n a)

theorem siteOperator_mem_factor (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n a ∈ theFactorObject P := towerPi_mem_factor _

theorem lastSiteMatrix_star (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    lastSiteMatrix n aᴴ = (lastSiteMatrix n a)ᴴ := by
  cases n with
  | zero => rfl
  | succ n => simp only [lastSiteMatrix, conjTranspose_kronecker, conjTranspose_one]

theorem siteOperator_star (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n aᴴ = star (siteOperator P n a) := by
  unfold siteOperator
  rw [lastSiteMatrix_star, towerPi_star, ContinuousLinearMap.star_eq_adjoint]

theorem towerPi_step {n : ℕ} (a : Matrix (chainIdx n) (chainIdx n) ℂ) :
    towerPi P (towerStep a) = towerPi P a := by
  have h := towerPi_compat (P := P) (Nat.le_succ n) a
  rw [tPush_succ (le_refl n), tPush_self] at h
  exact h

theorem step_commutes_last {n : ℕ} (b : Matrix (chainIdx n) (chainIdx n) ℂ)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    towerStep b * lastSiteMatrix (n+1) a = lastSiteMatrix (n+1) a * towerStep b := by
  simp only [towerStep, lastSiteMatrix, ← Matrix.mul_kronecker_mul, one_mul, mul_one]

theorem siteOperators_commute_lt {n m : ℕ} (h : n < m)
    (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n a * siteOperator P m b = siteOperator P m b * siteOperator P n a := by
  cases m with
  | zero => omega
  | succ m =>
    have hnm : n ≤ m := Nat.le_of_lt_succ h
    change towerPi P (lastSiteMatrix n a) * towerPi P (lastSiteMatrix (m+1) b) =
      towerPi P (lastSiteMatrix (m+1) b) * towerPi P (lastSiteMatrix n a)
    rw [← towerPi_compat hnm (lastSiteMatrix n a), ← towerPi_step]
    rw [← towerPi_mul, ← towerPi_mul, step_commutes_last]

theorem siteOperators_commute {n m : ℕ} (h : n ≠ m)
    (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n a * siteOperator P m b = siteOperator P m b * siteOperator P n a := by
  rcases lt_or_gt_of_ne h with hlt | hgt
  · exact siteOperators_commute_lt hlt a b
  · exact (siteOperators_commute_lt hgt b a).symm

def chainGenerators (P : SiteProfile) (I : Set ℕ) : Set (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  {x | ∃ n ∈ I, ∃ a : Matrix (Fin 2) (Fin 2) ℂ, x = siteOperator P n a}

def chainLocalAlgebra (P : SiteProfile) (I : Set ℕ) :
    StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  StarAlgebra.adjoin ℂ (chainGenerators P I)

theorem chain_isotony {I J : Set ℕ} (h : I ⊆ J) : chainLocalAlgebra P I ≤ chainLocalAlgebra P J := by
  apply StarAlgebra.adjoin_mono
  rintro x ⟨n,hn,a,rfl⟩
  exact ⟨n,h hn,a,rfl⟩

theorem chain_generators_star {I : Set ℕ} {x : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainGenerators P I) : star x ∈ chainGenerators P I := by
  obtain ⟨n,hn,a,rfl⟩ := hx
  exact ⟨n,hn,aᴴ,(siteOperator_star n a).symm⟩

#print axioms siteOperators_commute
#print axioms chain_isotony
end
end ChatgptAudit
