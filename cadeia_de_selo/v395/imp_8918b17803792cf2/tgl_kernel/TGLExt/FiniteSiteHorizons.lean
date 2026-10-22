-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_045 (06/09/2026), transposta em 06/09/2026
-- Lote 044..045 (ORDEM_008 cumprida). 044: BOOST APROXIMADO e orientacao do calor — o peso -kappa t realizado
--   por um campo de boost chi = -kappa u d_u + kappa v d_v e seu fluxo (grupo, inversa, jacobiano); pullback da
--   metrica e defeito de Lie -2kappa(aX^2+cY^2)du^2 (zera com o 1o jato na central); controle negativo: nao e
--   Killing em aberto se kappa != 0 e (a,c) != 0; T(chi,d) = -kappa t T(d,d); Q_boost = opticalHeat041 globalmente,
--   = opticalScreenHeat043 como germe; orientacao do passado certificada (calor e area invertem sinal juntos).
--   045 (resposta a ORDEM_010): swapHorizon P p hp i j — troca de sitios no perfil estacionario e um TowerHorizon
--   por prova (unitario, normaliza M, preserva omega); permutacoes finitas com lei de grupo e covariancia das
--   esperancas estacionaria/tracial (horizontes algebricos; identificacao fisica OPEN); shift unilateral NAO
--   construido; aperiodico OPEN (rota Cesaro nomeada); StateClock: classe cinematica (origem, derivada 1, jato) —
--   DICOTOMIA: para todo relogio comum g alguma tela falha (duas telas sigma = 0, r/4, mesmo estado e Ricci:
--   diferenca dos residuos/t^4 -> +eta r^2/96), cada tela isolada admite relogio que cancela a 4a ordem;
--   area: covariancia por horizontes NAO fixa a normalizacao (h e alpha h ambos invariantes; area x alpha).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia, carta e kappa sao INPUT; kappa/(2pi) e normalizacao
--   herdada (sem Unruh/KMS); H3 fisico, lei finita geral, ponte regiao-algebra, shift e aperiodico OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 8/8; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito). As fontes v329 (gerencia) NAO sao
--   reincorporadas: a bancada as recompilou como dependencia, sem novidade contada.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.FiniteSitePermutations
import TGLExt.ChainPrefix
import TGLExt.AffineClockAndRegion
import TGLExt.ChainSiteFlow
import TGLExt.TheLiftFiresOnThePeriodicTower
import TGLExt.TheModularFlowIsAHorizon

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Horizons045

open TGLExt Matrix
noncomputable section

/-- A finite permutation is implemented inside the actual tower factor. -/
def finiteSiteUnitary (P : SiteProfile) (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    TowerHilbert P →L[ℂ] TowerHilbert P := towerPi P (finiteSiteMatrix N σ)

theorem finite_site_unitary_mem (P : SiteProfile) (N : ℕ)
    (σ : Equiv.Perm (Fin (N+1))) :
    finiteSiteUnitary P N σ ∈ theFactorObject P :=
  towerPi_mem_factor _

theorem finite_site_unitary_left (P : SiteProfile) (N : ℕ)
    (σ : Equiv.Perm (Fin (N+1))) :
    star (finiteSiteUnitary P N σ) * finiteSiteUnitary P N σ = 1 := by
  unfold finiteSiteUnitary
  rw [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, ← towerPi_mul,
    finite_site_matrix_unitary_left, towerPi_one]

theorem finite_site_unitary_right (P : SiteProfile) (N : ℕ)
    (σ : Equiv.Perm (Fin (N+1))) :
    finiteSiteUnitary P N σ * star (finiteSiteUnitary P N σ) = 1 := by
  unfold finiteSiteUnitary
  rw [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, ← towerPi_mul,
    finite_site_matrix_unitary_right, towerPi_one]

theorem finite_site_unitary_one (P : SiteProfile) (N : ℕ) :
    finiteSiteUnitary P N 1 = 1 := by
  rw [finiteSiteUnitary, finite_site_matrix_one, towerPi_one]

theorem finite_site_unitary_mul (P : SiteProfile) (N : ℕ)
    (σ τ : Equiv.Perm (Fin (N+1))) :
    finiteSiteUnitary P N (σ * τ) = finiteSiteUnitary P N σ * finiteSiteUnitary P N τ := by
  simp only [finiteSiteUnitary, finite_site_matrix_mul, towerPi_mul]

theorem finite_site_unitary_inverse (P : SiteProfile) (N : ℕ)
    (σ : Equiv.Perm (Fin (N+1))) :
    finiteSiteUnitary P N σ⁻¹ = star (finiteSiteUnitary P N σ) := by
  rw [finiteSiteUnitary, finite_site_matrix_inverse, towerPi_star]
  rfl

theorem finite_site_unitary_centralizer (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    finiteSiteUnitary P N σ ∈ omegaCentralizer P :=
  density_commuting_local_is_global_centralizer N _
    (stationary_density_commutes P p hp N σ)

theorem finite_site_unitary_preserves_state (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    omegaState P (finiteSiteUnitary P N σ * A * star (finiteSiteUnitary P N σ)) =
      omegaState P A := by
  have hc := finite_site_unitary_centralizer P p hp N σ
  have hs : star (finiteSiteUnitary P N σ) ∈ theFactorObject P := star_mem hc.1
  rw [mul_assoc, hc.2 (A * star (finiteSiteUnitary P N σ)) (mul_mem hA hs),
    mul_assoc, finite_site_unitary_left, mul_one]

/-- Stationarity is the proved density invariance, rather than an assumed horizon. -/
def finiteSiteHorizon (P : SiteProfile) (p : ℝ) (hp : ∀ n, P.w n = p)
    (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) : TowerHorizon P where
  U := finiteSiteUnitary P N σ
  unitary_left := finite_site_unitary_left P N σ
  unitary_right := finite_site_unitary_right P N σ
  normalizes _ hA := mul_mem (mul_mem (finite_site_unitary_mem P N σ) hA)
    (star_mem (finite_site_unitary_mem P N σ))
  normalizes_inv _ hA := mul_mem (mul_mem
    (star_mem (finite_site_unitary_mem P N σ)) hA) (finite_site_unitary_mem P N σ)
  preserves A hA := finite_site_unitary_preserves_state P p hp N σ A hA

theorem finite_site_unitary_site_action (P : SiteProfile) (N : ℕ)
    (σ : Equiv.Perm (Fin (N+1))) (n : Fin (N+1))
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    finiteSiteUnitary P N σ * siteOperator P n.val a * star (finiteSiteUnitary P N σ) =
      siteOperator P (σ n).val a := by
  have h := congrArg (fun A : Matrix (chainIdx N) (chainIdx N) ℂ => towerPi P A)
    (finite_site_matrix_site_action N σ n a)
  rw [towerPi_mul, towerPi_mul, towerPi_star] at h
  simpa only [single_site_tensor_pi, finiteSiteUnitary,
    ContinuousLinearMap.star_eq_adjoint] using h

theorem finite_site_horizon_site_action (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (n : Fin (N+1)) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    adT (finiteSiteHorizon P p hp N σ) (siteOperator P n.val a) =
      siteOperator P (σ n).val a :=
  finite_site_unitary_site_action P N σ n a

theorem finite_site_unitary_tail_commutes (P : SiteProfile) (N m : ℕ)
    (hm : N < m) (σ : Equiv.Perm (Fin (N+1))) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    finiteSiteUnitary P N σ * siteOperator P m a =
      siteOperator P m a * finiteSiteUnitary P N σ := by
  have hd : Disjoint (Set.Iic N) ({m} : Set ℕ) := by
    apply Set.disjoint_left.mpr
    intro k hk hkm
    have he : k = m := Set.mem_singleton_iff.mp hkm
    subst k
    exact (not_le_of_gt hm) hk
  have hU : finiteSiteUnitary P N σ ∈ chainLocalAlgebra P (Set.Iic N) :=
    towerPi_mem_chain_prefix N _
  have ha : siteOperator P m a ∈ chainLocalAlgebra P {m} :=
    StarAlgebra.subset_adjoin ℂ (chainGenerators P {m}) ⟨m,rfl,a,rfl⟩
  exact chain_locality hd hU ha

theorem finite_site_horizon_tail_fixed (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N m : ℕ) (hm : N < m)
    (σ : Equiv.Perm (Fin (N+1))) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    adT (finiteSiteHorizon P p hp N σ) (siteOperator P m a) = siteOperator P m a := by
  change finiteSiteUnitary P N σ * siteOperator P m a * star (finiteSiteUnitary P N σ) = _
  rw [finite_site_unitary_tail_commutes P N m hm σ a, mul_assoc,
    finite_site_unitary_right, mul_one]

theorem finite_site_horizon_swap_left (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (i j : Fin (N+1))
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    adT (finiteSiteHorizon P p hp N (Equiv.swap i j)) (siteOperator P i.val a) =
      siteOperator P j.val a := by
  rw [finite_site_horizon_site_action, Equiv.swap_apply_left]

theorem finite_site_horizon_swap_right (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (i j : Fin (N+1))
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    adT (finiteSiteHorizon P p hp N (Equiv.swap i j)) (siteOperator P j.val a) =
      siteOperator P i.val a := by
  rw [finite_site_horizon_site_action, Equiv.swap_apply_right]

theorem finite_site_horizon_stationary_covariance (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (hne : p ≠ 1/2) (N : ℕ)
    (σ : Equiv.Perm (Fin (N+1))) :
    ∀ A ∈ theFactorObject P,
      adT (finiteSiteHorizon P p hp N σ) ((stationaryExpectationInput P p hp hne).E A) =
        (stationaryExpectationInput P p hp hne).E (adT (finiteSiteHorizon P p hp N σ) A) :=
  the_lift_fires_on_the_stationary_tower p hp hne (finiteSiteHorizon P p hp N σ)

theorem finite_site_horizon_tracial_covariance (P : SiteProfile)
    (hp : ∀ n, P.w n = 1/2) (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    ∀ A ∈ theFactorObject P,
      adT (finiteSiteHorizon P (1/2) hp N σ) ((tracialExpectationInput P hp).E A) =
        (tracialExpectationInput P hp).E (adT (finiteSiteHorizon P (1/2) hp N σ) A) :=
  the_lift_fires_on_the_tracial_tower hp (finiteSiteHorizon P (1/2) hp N σ)

theorem finite_site_horizon_covariance (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (I : ExpectationInput P) :
    ∀ A ∈ theFactorObject P,
      adT (finiteSiteHorizon P p hp N σ) (I.E A) =
        I.E (adT (finiteSiteHorizon P p hp N σ) A) :=
  the_lift_on_the_tower I (finiteSiteHorizon P p hp N σ)

/-- Modular conjugation fixes each local diagonal projection individually. -/
theorem modular_site_projection_fixed (P : SiteProfile) (s : ℝ) (n : ℕ) :
    modularConjugation P s (siteOperator P n (Matrix.single 0 0 1)) =
      siteOperator P n (Matrix.single 0 0 1) := by
  rw [modularConjugation_site]
  congr 1
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [siteFlow, modularPhase]

theorem different_site_projections (P : SiteProfile) (n m : ℕ) (hnm : n ≠ m) :
    siteOperator P n (Matrix.single 0 0 1) ≠ siteOperator P m (Matrix.single 0 0 1) := by
  intro he
  have hc := siteOperators_commute (P := P) hnm.symm
    (Matrix.single 0 0 1) (Matrix.single 0 1 1)
  rw [← he] at hc
  exact ChatgptAudit.Clock040.region_site_noncommutation n hc

/-- A moved site provides an explicit observable separating this action from every modular time. -/
theorem finite_site_horizon_nonmodular (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (n : Fin (N+1)) (hn : σ n ≠ n) (s : ℝ) :
    ∃ A ∈ theFactorObject P,
      adT (finiteSiteHorizon P p hp N σ) A ≠ modularConjugation P s A := by
  refine ⟨siteOperator P n.val (Matrix.single 0 0 1), siteOperator_mem_factor _ _, ?_⟩
  rw [finite_site_horizon_site_action, modular_site_projection_fixed]
  apply different_site_projections P
  intro he
  exact hn (Fin.ext he)

theorem finite_site_horizon_ne_modular_horizon (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (n : Fin (N+1)) (hn : σ n ≠ n) (s : ℝ) :
    finiteSiteHorizon P p hp N σ ≠ modularHorizon P s := by
  intro he
  obtain ⟨A, _, hA⟩ := finite_site_horizon_nonmodular P p hp N σ n hn s
  apply hA
  rw [he, adT_modularHorizon]


/-- Natural-site interface: the finite containing prefix is chosen explicitly as max i j. -/
def swapHorizon (P : SiteProfile) (p : ℝ) (hp : ∀ n, P.w n = p) (i j : ℕ) :
    TowerHorizon P :=
  finiteSiteHorizon P p hp (max i j)
    (Equiv.swap ⟨i, Nat.lt_succ_of_le (Nat.le_max_left i j)⟩
      ⟨j, Nat.lt_succ_of_le (Nat.le_max_right i j)⟩)

theorem swap_horizon_left (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (i j : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    adT (swapHorizon P p hp i j) (siteOperator P i a) = siteOperator P j a :=
  finite_site_horizon_swap_left P p hp (max i j)
    ⟨i, Nat.lt_succ_of_le (Nat.le_max_left i j)⟩
    ⟨j, Nat.lt_succ_of_le (Nat.le_max_right i j)⟩ a

theorem swap_horizon_right (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (i j : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    adT (swapHorizon P p hp i j) (siteOperator P j a) = siteOperator P i a :=
  finite_site_horizon_swap_right P p hp (max i j)
    ⟨i, Nat.lt_succ_of_le (Nat.le_max_left i j)⟩
    ⟨j, Nat.lt_succ_of_le (Nat.le_max_right i j)⟩ a

theorem expectation_commutes_with_site_swap (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (i j : ℕ) (I : ExpectationInput P) :
    ∀ A ∈ theFactorObject P,
      adT (swapHorizon P p hp i j) (I.E A) =
        I.E (adT (swapHorizon P p hp i j) A) :=
  the_lift_on_the_tower I (swapHorizon P p hp i j)

theorem swap_horizon_nonmodular (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (i j : ℕ) (hij : i ≠ j) (s : ℝ) :
    ∃ A ∈ theFactorObject P,
      adT (swapHorizon P p hp i j) A ≠ modularConjugation P s A := by
  refine ⟨siteOperator P i (Matrix.single 0 0 1), siteOperator_mem_factor _ _, ?_⟩
  rw [swap_horizon_left, modular_site_projection_fixed]
  exact different_site_projections P j i hij.symm

#print axioms finiteSiteUnitary
#print axioms finite_site_unitary_mem
#print axioms finite_site_unitary_left
#print axioms finite_site_unitary_right
#print axioms finite_site_unitary_one
#print axioms finite_site_unitary_mul
#print axioms finite_site_unitary_inverse
#print axioms finite_site_unitary_centralizer
#print axioms finite_site_unitary_preserves_state
#print axioms finiteSiteHorizon
#print axioms finite_site_unitary_site_action
#print axioms finite_site_horizon_site_action
#print axioms finite_site_unitary_tail_commutes
#print axioms finite_site_horizon_tail_fixed
#print axioms finite_site_horizon_swap_left
#print axioms finite_site_horizon_swap_right
#print axioms finite_site_horizon_stationary_covariance
#print axioms finite_site_horizon_tracial_covariance
#print axioms finite_site_horizon_covariance
#print axioms modular_site_projection_fixed
#print axioms different_site_projections
#print axioms finite_site_horizon_nonmodular
#print axioms finite_site_horizon_ne_modular_horizon
#print axioms swapHorizon
#print axioms swap_horizon_left
#print axioms swap_horizon_right
#print axioms expectation_commutes_with_site_swap
#print axioms swap_horizon_nonmodular

end
end ChatgptAudit.Horizons045
