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
import TGLExt.LocalCentralizerExpectation
import TGLExt.ExpectationProjection

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit
open TGLExt Matrix Filter Topology
noncomputable section
variable {P : SiteProfile}

theorem omega_product_inner (x y : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (x*y) = inner ℂ (star x (hOmega P)) (y (hOmega P)) := by
  change inner ℂ (hOmega P) (x (y (hOmega P))) =
    inner ℂ (ContinuousLinearMap.adjoint x (hOmega P)) (y (hOmega P))
  rw [ContinuousLinearMap.adjoint_inner_left]

theorem centralizer_from_expectations (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P)
    (hc : ∀ N, towerExpectation P N x ∈ omegaCentralizer P) : x ∈ omegaCentralizer P := by
  refine ⟨hx,?_⟩
  intro b hb
  have hl : Tendsto (fun N => omegaState P (towerExpectation P N x*b)) atTop
      (nhds (omegaState P (x*b))) := by
    simp only [omega_product_inner,← expectation_star _ x hx]
    exact (expectation_omega_limit (star x)).inner tendsto_const_nhds
  have hr : Tendsto (fun N => omegaState P (b*towerExpectation P N x)) atTop
      (nhds (omegaState P (b*x))) := by
    simp only [omega_product_inner]
    exact tendsto_const_nhds.inner (expectation_omega_limit x)
  have he : (fun N => omegaState P (towerExpectation P N x*b)) =
      (fun N => omegaState P (b*towerExpectation P N x)) :=
    funext (fun N => (hc N).2 b hb)
  rw [he] at hl
  exact tendsto_nhds_unique hl hr

theorem half_profile_weights (hp : ∀ n, P.w n = 1/2) (N : ℕ)
    (i j : chainIdx N) : towerW P N i = towerW P N j := by
  have hs : ∀ n (u v : Fin 2), siteW (P.w n) u = siteW (P.w n) v := by
    intro n u v
    fin_cases u <;> fin_cases v <;> norm_num [siteW,hp]
  induction N with
  | zero => exact hs 0 i j
  | succ n ih =>
    rcases i with ⟨i,u⟩
    rcases j with ⟨j,v⟩
    simp only [towerW,ih i j,hs (n+1) u v]

theorem half_profile_local_centralizer (hp : ∀ n, P.w n = 1/2) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : towerPi P a ∈ omegaCentralizer P := by
  apply density_commuting_local_is_global_centralizer N a
  ext i j
  simp only [rhoD,Matrix.diagonal_mul,Matrix.mul_diagonal,half_profile_weights hp N i j]
  exact mul_comm _ _

theorem half_profile_centralizer_is_factor (hp : ∀ n, P.w n = 1/2)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    x ∈ omegaCentralizer P ↔ x ∈ theFactorObject P := by
  constructor
  · exact fun h => h.1
  · intro hx
    exact centralizer_from_expectations x hx (fun N => half_profile_local_centralizer hp N _)

def tracialExpectationInput (P : SiteProfile) (hp : ∀ n, P.w n = 1/2) : ExpectationInput P where
  E := id
  into := fun x hx => (half_profile_centralizer_is_factor hp x).mpr hx
  fixes := fun _ _ => rfl
  ortho := by
    intro a ha b hb
    simp only [id_eq,sub_self,mul_zero]
    simp [omegaState]

theorem tracial_expectation_is_identity (hp : ∀ n, P.w n = 1/2)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) : (tracialExpectationInput P hp).E x = x := rfl

#print axioms omega_product_inner
#print axioms centralizer_from_expectations
#print axioms half_profile_weights
#print axioms half_profile_local_centralizer
#print axioms half_profile_centralizer_is_factor
#print axioms tracialExpectationInput
#print axioms tracial_expectation_is_identity
end
end ChatgptAudit
