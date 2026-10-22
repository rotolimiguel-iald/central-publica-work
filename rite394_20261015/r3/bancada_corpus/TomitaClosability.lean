import TGL
import TGLExt
import TGLExt.TheImportedExpectation
import TGLExt.RightMult

set_option autoImplicit false
set_option maxHeartbeats 1000000

open Filter Topology

namespace ChatgptAudit

open TGLExt

noncomputable section

variable {P : SiteProfile}

/-- Identidade de dualidade com a direita limitada da torre. -/
theorem tomita_pairing
    {A : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A ∈ theFactorObject P) {N : ℕ}
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ ((star A) (hOmega P)) (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) (A (hOmega P)) := by
  simp only [ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_left]
  have hc := congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P =>
    T (hOmega P)) (factor_comm_rTowerPi hA b)
  simpa only [mul_apply_eq_comp] using congrArg
    (fun z : TowerHilbert P => inner ℂ (hOmega P) z) hc

/-- Critério sequencial de fechabilidade no completamento genuíno.
    Não pressupõe TakesakiInput nem CommutationInput. -/
theorem tomita_sequential_closability
    (A : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : ∀ n, A n ∈ theFactorObject P)
    (y : TowerHilbert P)
    (hzero : Tendsto (fun n => A n (hOmega P)) atTop (𝓝 0))
    (hy : Tendsto (fun n => (star (A n)) (hOmega P)) atTop (𝓝 y)) :
    y = 0 := by
  apply (towerPre_denseRange (P := P)).eq_zero_of_inner_left (𝕜 := ℂ)
  intro v
  obtain ⟨N, b, rfl⟩ := exists_tof v
  rw [← rTowerPi_omega]
  have hleft := hy.inner (𝕜 := ℂ)
    (tendsto_const_nhds (x := rTowerPi P b (hOmega P)))
  have hright := (tendsto_const_nhds
    (x := (star (rTowerPi P b)) (hOmega P))).inner (𝕜 := ℂ) hzero
  have heq : (fun n => inner ℂ ((star (A n)) (hOmega P))
      (rTowerPi P b (hOmega P))) =
      (fun n => inner ℂ ((star (rTowerPi P b)) (hOmega P))
        (A n (hOmega P))) := funext (fun n => tomita_pairing (hA n) b)
  rw [heq] at hleft
  simpa only [inner_zero_right] using tendsto_nhds_unique hleft hright

/-- A regra AΩ ↦ A*Ω é bem definida pela separância já provada. -/
theorem tomita_well_defined
    {A B : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P)
    (h : A (hOmega P) = B (hOmega P)) :
    (star A) (hOmega P) = (star B) (hOmega P) := by
  have hz : A - B = 0 := factor_omega_separating
    ((theFactorObject P).sub_mem hA hB) (by simpa using sub_eq_zero.mpr h)
  have hab : A = B := sub_eq_zero.mp hz
  rw [hab]

/-- Gráfico do operador antilinear AΩ ↦ A*Ω no domínio MΩ. -/
def tomitaGraph (P : SiteProfile) : Set (TowerHilbert P × TowerHilbert P) :=
  {p | ∃ A : TowerHilbert P →L[ℂ] TowerHilbert P,
    A ∈ theFactorObject P ∧ p = (A (hOmega P), (star A) (hOmega P))}

/-- Ponte explícita ao operador S no andar: o adjunto matricial vive neste gráfico. -/
theorem local_tomita_graph {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (((tof P N a : TowerPre P) : TowerHilbert P),
      ((tof P N (Matrix.conjTranspose a) : TowerPre P) : TowerHilbert P)) ∈ tomitaGraph P := by
  refine ⟨towerPi P a, towerPi_mem_factor a, ?_⟩
  simp only [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, towerPi_omega]

/-- A identidade de dualidade sobrevive ao fecho topológico do gráfico. -/
theorem closure_graph_pairing
    {p : TowerHilbert P × TowerHilbert P}
    (hp : p ∈ closure (tomitaGraph P)) {N : ℕ}
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ p.2 (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) p.1 := by
  have hc : IsClosed {p : TowerHilbert P × TowerHilbert P |
      inner ℂ p.2 (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) p.1} := by
    apply isClosed_eq <;> fun_prop
  apply closure_minimal (t := {p : TowerHilbert P × TowerHilbert P |
      inner ℂ p.2 (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) p.1}) ?_ hc hp
  rintro p ⟨A, hA, rfl⟩
  exact tomita_pairing hA b

/-- Fechabilidade em forma topológica: o fecho não adquire fibra vertical não nula. -/
theorem tomita_graph_closure_vertical
    (y : TowerHilbert P) (hy : (0, y) ∈ closure (tomitaGraph P)) : y = 0 := by
  apply (towerPre_denseRange (P := P)).eq_zero_of_inner_left (𝕜 := ℂ)
  intro v
  obtain ⟨N, b, rfl⟩ := exists_tof v
  rw [← rTowerPi_omega]
  simpa only [inner_zero_right] using closure_graph_pairing hy b

/-- O fecho do gráfico é univalente, inclusive fora do domínio inicial MΩ. -/
theorem tomita_graph_closure_single_valued
    (x y z : TowerHilbert P)
    (hy : (x, y) ∈ closure (tomitaGraph P))
    (hz : (x, z) ∈ closure (tomitaGraph P)) : y = z := by
  apply (towerPre_denseRange (P := P)).eq_of_inner_left (𝕜 := ℂ)
  intro v
  obtain ⟨N, b, rfl⟩ := exists_tof v
  rw [← rTowerPi_omega]
  exact (closure_graph_pairing hy b).trans (closure_graph_pairing hz b).symm

/-- Densidade do domínio inicial, com a definição concreta do gráfico. -/
theorem tomita_graph_domain_dense :
    Dense (Prod.fst '' tomitaGraph P) := by
  apply Dense.mono ?_ (factor_omega_cyclic (P := P))
  rintro x ⟨A, hA, rfl⟩
  exact ⟨(A (hOmega P), (star A) (hOmega P)), ⟨A, hA, rfl⟩, rfl⟩

#print axioms tomita_pairing
#print axioms tomita_sequential_closability
#print axioms tomita_well_defined
#print axioms local_tomita_graph
#print axioms closure_graph_pairing
#print axioms tomita_graph_closure_vertical
#print axioms tomita_graph_closure_single_valued
#print axioms tomita_graph_domain_dense

end
end ChatgptAudit
