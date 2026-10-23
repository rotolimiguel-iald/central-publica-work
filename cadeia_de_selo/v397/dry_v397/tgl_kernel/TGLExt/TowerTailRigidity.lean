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
import TGLExt.LevelExpectationFamily
import Mathlib.Data.Matrix.Basis

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt Matrix Filter Topology
noncomputable section
variable {P : SiteProfile}

theorem expectation_commutes_local (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (hc : towerPi P a * x = x * towerPi P a) :
    towerPi P a * towerExpectation P N x = towerExpectation P N x * towerPi P a := by
  have hl := expectation_bimodular N a 1 x hx
  have hr := expectation_bimodular N 1 a x hx
  simp only [towerPi_one, one_mul, mul_one] at hl hr
  rw [← hl, hc, hr]

theorem expectation_central_scalar (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P)
    (hc : ∀ a : Matrix (chainIdx N) (chainIdx N) ℂ, towerPi P a * x = x * towerPi P a) :
    ∃ c : ℂ, towerExpectation P N x = c • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
  have hm : expectationMatrix P N x ∈ Set.range (Matrix.scalar (chainIdx N)) := by
    apply Matrix.mem_range_scalar_of_commute_single
    intro i j _
    change Matrix.single i j 1 * expectationMatrix P N x = expectationMatrix P N x * Matrix.single i j 1
    apply towerPi_injective P N
    change towerPi P (_ * _) = towerPi P (_ * _)
    rw [towerPi_mul, towerPi_mul]
    exact expectation_commutes_local N x hx _ (hc _)
  obtain ⟨c,he⟩ := hm
  refine ⟨c, ?_⟩
  change towerPi P (expectationMatrix P N x) = _
  rw [← he]
  have hs : Matrix.scalar (chainIdx N) c = c • (1 : Matrix (chainIdx N) (chainIdx N) ℂ) := by
    ext i j
    simp [Matrix.scalar_apply, Matrix.one_apply, Matrix.diagonal_apply, smul_eq_mul]
  rw [hs, towerPi_smul, towerPi_one]

theorem omega_scalar (c : ℂ) :
    omegaState P (c • (1 : TowerHilbert P →L[ℂ] TowerHilbert P)) = c := by
  change inner ℂ (hOmega P) (c • hOmega P) = c
  rw [inner_smul_right, hOmega_inner_self, mul_one]

theorem commutes_all_levels_scalar
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P)
    (hc : ∀ N (a : Matrix (chainIdx N) (chainIdx N) ℂ), towerPi P a * x = x * towerPi P a) :
    x = omegaState P x • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
  have he : ∀ N, towerExpectation P N x = omegaState P x • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
    intro N
    obtain ⟨c,hc'⟩ := expectation_central_scalar N x hx (hc N)
    have hw := expectation_preserves_state N x
    rw [hc', omega_scalar] at hw
    simpa only [hw] using hc'
  apply factor_eq_of_omega hx ((theFactorObject P).smul_mem (one_mem _) _)
  have ht := expectation_omega_limit x
  simp only [he] at ht
  exact tendsto_nhds_unique ht tendsto_const_nhds

/-- Interface de cauda: inclusão no comutante de cada prefixo. -/
def prefixCommutingTail (P : SiteProfile) (N : ℕ) : Set (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  {x | x ∈ theFactorObject P ∧ ∀ a : Matrix (chainIdx N) (chainIdx N) ℂ, towerPi P a * x = x * towerPi P a}

theorem tail_intersection_scalar (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : ∀ N, x ∈ prefixCommutingTail P N) :
    x = omegaState P x • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) :=
  commutes_all_levels_scalar x (hx 0).1 (fun N => (hx N).2)

#print axioms commutes_all_levels_scalar
#print axioms tail_intersection_scalar
end
end ChatgptAudit
