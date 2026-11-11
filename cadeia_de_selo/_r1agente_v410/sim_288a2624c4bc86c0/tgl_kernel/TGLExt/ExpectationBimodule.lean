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
import TGLExt.ExpectationProjection

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt UniformSpace
noncomputable section
variable {P : SiteProfile}

theorem left_preserves_level {N : ℕ} (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    {v : TowerHilbert P} (hv : v ∈ levelSpace P N) :
    towerPi P a v ∈ levelSpace P N := by
  obtain ⟨b,rfl⟩ := hv
  refine ⟨a*b, ?_⟩
  change _ = towerPi P a ((tof P N b : TowerPre P) : TowerHilbert P)
  rw [towerPi_coe, lmulPre_tof_at (le_refl N) (le_refl N), tPush_self, tPush_self]
  rfl

theorem right_preserves_level {N : ℕ} (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    {v : TowerHilbert P} (hv : v ∈ levelSpace P N) :
    rTowerPi P a v ∈ levelSpace P N := by
  obtain ⟨b,rfl⟩ := hv
  refine ⟨b*a, ?_⟩
  change _ = rTowerPi P a ((tof P N b : TowerPre P) : TowerHilbert P)
  rw [rTowerPi_coe, rmulPre_tof_at (le_refl N) (le_refl N), tPush_self, tPush_self]
  rfl

theorem project_commutes_reducing (N : ℕ)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hT : ∀ v ∈ levelSpace P N, T v ∈ levelSpace P N)
    (hstar : ∀ v ∈ levelSpace P N, T.adjoint v ∈ levelSpace P N)
    (x : TowerHilbert P) : levelProject P N (T x) = T (levelProject P N x) := by
  apply level_inner_ext (levelProject_mem _ _) (hT _ (levelProject_mem _ _))
  intro b hb
  rw [levelProject_inner hb, ← ContinuousLinearMap.adjoint_inner_left,
    ← ContinuousLinearMap.adjoint_inner_left, levelProject_inner (hstar b hb)]

theorem project_left (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (x : TowerHilbert P) : levelProject P N (towerPi P a x) =
      towerPi P a (levelProject P N x) := by
  apply project_commutes_reducing
  · exact fun v hv => left_preserves_level a hv
  · intro v hv
    rw [← towerPi_star]
    exact left_preserves_level _ hv

theorem project_right (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (x : TowerHilbert P) : levelProject P N (rTowerPi P a x) =
      rTowerPi P a (levelProject P N x) := by
  apply project_commutes_reducing
  · exact fun v hv => right_preserves_level a hv
  · intro v hv
    rw [← rTowerPi_star]
    exact right_preserves_level _ hv

theorem factor_right_apply {x : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ theFactorObject P) {N : ℕ}
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) (v : TowerHilbert P) :
    x (rTowerPi P b v) = rTowerPi P b (x v) :=
  congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T v) (factor_comm_rTowerPi hx b)

theorem expectation_compression (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) {v : TowerHilbert P} (hv : v ∈ levelSpace P N) :
    towerExpectation P N x v = levelProject P N (x v) := by
  obtain ⟨b,rfl⟩ := hv
  change towerExpectation P N x ((tof P N b : TowerPre P) : TowerHilbert P) =
    levelProject P N (x ((tof P N b : TowerPre P) : TowerHilbert P))
  rw [← rTowerPi_omega, factor_right_apply (expectation_mem_factor _ _),
    factor_right_apply hx, project_right, expectation_omega]

theorem expectation_bimodular (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P) :
    towerExpectation P N (towerPi P a * x * towerPi P b) =
      towerPi P a * towerExpectation P N x * towerPi P b := by
  apply factor_eq_of_omega (expectation_mem_factor _ _)
    ((theFactorObject P).mul_mem
      ((theFactorObject P).mul_mem (towerPi_mem_factor _) (expectation_mem_factor _ _))
      (towerPi_mem_factor _))
  rw [expectation_omega]
  change levelProject P N (towerPi P a (x (towerPi P b (hOmega P)))) =
    towerPi P a (towerExpectation P N x (towerPi P b (hOmega P)))
  rw [project_left, expectation_compression N x hx (left_preserves_level b (omega_mem_level N))]

#print axioms expectation_compression
#print axioms expectation_bimodular
end
end ChatgptAudit
