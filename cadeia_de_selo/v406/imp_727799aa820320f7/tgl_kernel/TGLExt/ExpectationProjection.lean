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
import TGLExt.TowerExpectation

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt UniformSpace
noncomputable section
variable {P : SiteProfile}

theorem level_inner_ext {N : ℕ} {x y : TowerHilbert P}
    (hx : x ∈ levelSpace P N) (hy : y ∈ levelSpace P N)
    (h : ∀ b ∈ levelSpace P N, inner ℂ b x = inner ℂ b y) : x = y := by
  have hz := h (x-y) ((levelSpace P N).sub_mem hx hy)
  have hzero : inner ℂ (x-y) (x-y) = 0 := by rw [inner_sub_right, hz, sub_self]
  exact sub_eq_zero.mp (inner_self_eq_zero.mp hzero)

theorem project_nested (M N : ℕ) (x : TowerHilbert P) :
    levelProject P M (levelProject P N x) = levelProject P (min M N) x := by
  rcases le_total M N with h | h
  · rw [min_eq_left h]
    apply level_inner_ext (levelProject_mem _ _) (levelProject_mem _ _)
    intro b hb
    rw [levelProject_inner hb, levelProject_inner (levelSpace_mono h hb), levelProject_inner hb]
  · rw [min_eq_right h]
    exact levelProject_fixed (levelSpace_mono h (levelProject_mem _ _))

theorem expectation_tower (M N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P M (towerExpectation P N x) = towerExpectation P (min M N) x := by
  apply factor_eq_of_omega (expectation_mem_factor _ _) (expectation_mem_factor _ _)
  rw [expectation_omega, expectation_omega, expectation_omega, project_nested]

theorem flow_preserves_level (t : ℝ) {N : ℕ} {v : TowerHilbert P}
    (hv : v ∈ levelSpace P N) : modularFlow P t v ∈ levelSpace P N := by
  obtain ⟨a,rfl⟩ := hv
  refine ⟨flowLevel P t N a, ?_⟩
  change _ = modularFlow P t ((tof P N a : TowerPre P) : TowerHilbert P)
  rw [modularFlow_coe, flowPre_tof]
  rfl

theorem flow_inner_transport (t : ℝ) (b x : TowerHilbert P) :
    inner ℂ b (modularFlow P t x) = inner ℂ (modularFlow P (-t) b) x := by
  have h := (modularFlowIsometry P t).inner_map_map (modularFlow P (-t) b) x
  change inner ℂ (modularFlow P t (modularFlow P (-t) b)) (modularFlow P t x) = _ at h
  rw [modularFlow_group, add_neg_cancel, modularFlow_zero_time] at h
  exact h

theorem project_flow_commutes (t : ℝ) (N : ℕ) (x : TowerHilbert P) :
    levelProject P N (modularFlow P t x) = modularFlow P t (levelProject P N x) := by
  apply level_inner_ext (levelProject_mem _ _) (flow_preserves_level _ (levelProject_mem _ _))
  intro b hb
  rw [levelProject_inner hb, flow_inner_transport, flow_inner_transport,
    levelProject_inner (flow_preserves_level _ hb)]

theorem expectation_flow_commutes (t : ℝ) (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    modularConjugation P t (towerExpectation P N x) =
      towerExpectation P N (modularConjugation P t x) := by
  apply factor_eq_of_omega
    ((modularConjugation_preserves_factor P t _).mp (expectation_mem_factor _ _))
    (expectation_mem_factor _ _)
  rw [expectation_omega]
  change modularFlow P t (towerExpectation P N x (modularFlow P (-t) (hOmega P))) =
    levelProject P N (modularFlow P t (x (modularFlow P (-t) (hOmega P))))
  rw [modularFlow_fixes_omega, expectation_omega, project_flow_commutes]

theorem expectation_omega_limit (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    Filter.Tendsto (fun N => towerExpectation P N x (hOmega P)) Filter.atTop
      (nhds (x (hOmega P))) := by
  simpa only [expectation_omega] using levelProject_tendsto (x (hOmega P))

#print axioms expectation_tower
#print axioms expectation_flow_commutes
#print axioms expectation_omega_limit
end
end ChatgptAudit
