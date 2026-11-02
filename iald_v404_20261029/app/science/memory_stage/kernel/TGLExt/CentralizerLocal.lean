-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_006 (05/09/2026), transposta em 05/09/2026
-- A ESPERANCA DO CENTRALIZADOR: habitante LOCAL (pinching espectral de cada
--   andar entra no centralizador GLOBAL de omega; into/fixes/ortho; unico) e
--   habitante TRACIAL do contrato original (w=1/2: M_omega = M, E = id);
--   invariancia de sitios sob sigma_t para TODO t (caudas nunca comprimem
--   estritamente); ponte: todo habitante global RESTRINGE-SE ao pinching.
-- Auditoria da gerencia (sessao d554e796): hashes 14/14 + manifesto 408/408;
--   recompilacao independente 5/5 exit 0; 34/34 no trio
--   [propext, Classical.choice, Quot.sound]; zero sorry/warning.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports da
--   bancada; nada mais. Namespace ChatgptAudit = procedencia.
-- [OPEN] declarados pela bancada: habitante global NAO tracial (parede exata:
--   operador medio do periodo + comutacao da media com E_N); nao-ciclicidade
--   da cauda em Lean; translacao de energia positiva nao trivial.
-- NAO move gate; nao e fisica. NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ExpectationPositive
import TGLExt.EquivariantSection
import TGLExt.TheOathOnTheTower
import TGLExt.TheProfileIsometry

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem state_local_left (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P) :
    omegaState P (towerPi P a * x) = tState P N (a * expectationMatrix P N x) := by
  have he := expectation_bimodular N a 1 x hx
  simp only [towerPi_one,mul_one] at he
  rw [← expectation_preserves_state N (towerPi P a*x),he]
  exact omegaState_pi_mul a _

theorem state_local_right (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P) :
    omegaState P (x * towerPi P a) = tState P N (expectationMatrix P N x * a) := by
  have he := expectation_bimodular N 1 a x hx
  simp only [towerPi_one,one_mul] at he
  rw [← expectation_preserves_state N (x*towerPi P a),he]
  exact omegaState_pi_mul _ a

theorem density_commuting_local_is_global_centralizer (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (ha : Commute (rhoD (towerW P N)) a) : towerPi P a ∈ omegaCentralizer P := by
  refine ⟨towerPi_mem_factor _,?_⟩
  intro x hx
  rw [state_local_left N a x hx,state_local_right N a x hx]
  simpa only [gibbs,rhoD,← tState_eq_trace] using
    gibbs_tracial_on_centralizer (rhoD (towerW P N)) a (expectationMatrix P N x) ha

theorem pinching_into_global_centralizer (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (specExpect (towerW P N) a) ∈ omegaCentralizer P :=
  density_commuting_local_is_global_centralizer N _ (rhoD_commute_specExpect _ _)

theorem state_mul_single (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
    tState P N (a * Matrix.single j i 1) = (towerW P N i : ℂ) * a i j := by
  simp [tState,Matrix.mul_apply,Matrix.single_apply,ite_and]

theorem state_single_mul (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
    tState P N (Matrix.single j i 1 * a) = (towerW P N j : ℂ) * a i j := by
  simp [tState,Matrix.mul_apply,Matrix.single_apply,ite_and]

theorem centralizer_local_blocks (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (ha : towerPi P a ∈ omegaCentralizer P) (i j : chainIdx N)
    (hd : towerW P N i ≠ towerW P N j) : a i j = 0 := by
  have he := ha.2 (towerPi P (Matrix.single j i 1)) (towerPi_mem_factor _)
  rw [omegaState_pi_mul,omegaState_pi_mul,state_mul_single,state_single_mul] at he
  have hz : ((towerW P N i : ℂ) - (towerW P N j : ℂ))*a i j = 0 := by
    rw [sub_mul,he,sub_self]
  exact (mul_eq_zero.mp hz).resolve_left (sub_ne_zero.mpr (fun h => hd (Complex.ofReal_injective h)))

theorem pinching_fixes_global_local (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (ha : towerPi P a ∈ omegaCentralizer P) : specExpect (towerW P N) a = a := by
  ext i j
  by_cases h : towerW P N i = towerW P N j
  · simp [h]
  · simp [h,centralizer_local_blocks N a ha i j h]

theorem expectation_of_centralizer_is_centralizer (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ omegaCentralizer P) :
    towerExpectation P N x ∈ omegaCentralizer P := by
  apply density_commuting_local_is_global_centralizer
  ext i j
  have he := hx.2 (towerPi P (Matrix.single j i 1)) (towerPi_mem_factor _)
  rw [state_local_right N _ x hx.1,state_local_left N _ x hx.1,
    state_mul_single,state_single_mul] at he
  simpa only [rhoD,Matrix.diagonal_mul,Matrix.mul_diagonal,mul_comm] using he

theorem pinching_state_ortho (N : ℕ) (a b : Matrix (chainIdx N) (chainIdx N) ℂ)
    (hb : towerPi P b ∈ omegaCentralizer P) :
    tState P N (bᴴ * (a-specExpect (towerW P N) a)) = 0 := by
  unfold tState
  apply Finset.sum_eq_zero
  intro i _
  have hz : (bᴴ * (a-specExpect (towerW P N) a)) i i = 0 := by
    rw [Matrix.mul_apply]
    apply Finset.sum_eq_zero
    intro j _
    by_cases h : towerW P N j = towerW P N i
    · simp [Matrix.sub_apply,h]
    · simp [Matrix.conjTranspose_apply,centralizer_local_blocks N b hb j i h]
  rw [hz,mul_zero]

#print axioms state_local_left
#print axioms state_local_right
#print axioms density_commuting_local_is_global_centralizer
#print axioms pinching_into_global_centralizer
#print axioms state_mul_single
#print axioms state_single_mul
#print axioms centralizer_local_blocks
#print axioms pinching_fixes_global_local
#print axioms expectation_of_centralizer_is_centralizer
#print axioms pinching_state_ortho
end
end ChatgptAudit
