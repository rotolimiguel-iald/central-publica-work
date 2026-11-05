import TGLExt.ThirdCone

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1600000

/-!
# O CONE CONTÍNUO: qualquer direção nula TT resolve — o setor TT FECHADO
  [TGLExt — v129, o incremento 52 do programa SemifiniteAnalysis]

As v125–v128 fecharam o setor TT direção a direção (cones 1,2,3). Esta
pedra fecha TODAS as direções de uma vez: para QUALQUER covetor nulo k
(η(k,k)=0) e QUALQUER polarização simétrica transversal-e-η-traço-zero,
a onda plana resolve o vácuo linearizado. As três condições algébricas
matam os três termos do Ricci linearizado:

* `dotCov k` — o funcional linear x ↦ Σ_μ k_μ x_μ (a direção geral);
* `planeWaveG k w` — a onda ao longo de k;
* ★★ `pd_pd_planeWaveG` — ∂_i∂_j(c·w∘k) = c·k_j·k_i·w″ (a redução);
* ★★★ `general_null_tt_ricci_zero` — O TEOREMA GERAL: ε simétrica,
  η-traço zero (mata o termo do traço), k-transversal (Σ_α η^αα k_α
  ε_αν = 0, mata os dois termos ∂_α∂_μ) e k-NULO (Σ_α η^αα k_α² = 0,
  mata o d'Alembertiano) ⟹ Ricci⁽¹⁾ = 0 em toda parte. Isto SUBSUME os
  cones 1,2,3 (v125–v128) E o cone contínuo (direção nula arbitrária).

O QUE ISTO FECHA: o setor de ondas planas TT no contínuo, em TODA
direção nula. O QUE RESTA (nomeado): a decomposição completa de
perturbações GERAIS (superposição de infinitas direções) e as anomalias
— a segunda metade dos flags de física; os 5 flags NÃO se movem por
esta pedra.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped BigOperators

noncomputable section

/-! ## A — o funcional da direção geral -/

/-- o covetor como funcional linear: x ↦ Σ_μ k_μ x_μ. -/
def dotCov (k : Fin 4 → ℝ) : (Fin 4 → ℝ) →L[ℝ] ℝ :=
  ∑ μ : Fin 4, (k μ) • ContinuousLinearMap.proj μ

theorem dotCov_apply (k x : Fin 4 → ℝ) :
    dotCov k x = ∑ μ : Fin 4, k μ * x μ := by
  unfold dotCov
  rw [ContinuousLinearMap.sum_apply]
  simp only [ContinuousLinearMap.smul_apply, ContinuousLinearMap.proj_apply,
    smul_eq_mul]

theorem dotCov_single (k : Fin 4 → ℝ) (j : Fin 4) :
    dotCov k (Pi.single j 1) = k j := by
  rw [dotCov_apply]
  rw [Finset.sum_eq_single j]
  · rw [Pi.single_eq_same, mul_one]
  · intro b _ hb
    rw [Pi.single_eq_of_ne hb, mul_zero]
  · intro h
    exact absurd (Finset.mem_univ j) h

/-- a onda plana ao longo de k. -/
def planeWaveG (k : Fin 4 → ℝ) (w : ℝ → ℝ) (x : Fin 4 → ℝ) : ℝ :=
  w (dotCov k x)

/-! ## B — a redução das derivadas -/

theorem pd_scaled_planeWaveG (k : Fin 4 → ℝ) (c : ℝ) (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (j : Fin 4) :
    pd j (fun y => c * planeWaveG k w y)
      = fun y => c * k j * planeWaveG k w' y := by
  funext y
  unfold pd
  have hf : HasFDerivAt (fun z => c * planeWaveG k w z)
      (c • ((w' (dotCov k y)) • (dotCov k : (Fin 4 → ℝ) →L[ℝ] ℝ))) y := by
    have hbase : HasFDerivAt (planeWaveG k w)
        ((w' (dotCov k y)) • (dotCov k : (Fin 4 → ℝ) →L[ℝ] ℝ)) y :=
      (hw (dotCov k y)).comp_hasFDerivAt y (dotCov k).hasFDerivAt
    exact hbase.const_smul c
  rw [hf.fderiv]
  unfold planeWaveG
  rw [ContinuousLinearMap.smul_apply, ContinuousLinearMap.smul_apply,
    dotCov_single, smul_eq_mul, smul_eq_mul]
  ring

/-- [KERNEL] ★★ a redução: ∂_i∂_j(c·w∘k) = c·k_j·k_i·w″. -/
theorem pd_pd_planeWaveG (k : Fin 4 → ℝ) (c : ℝ) (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u) (i j : Fin 4) (x : Fin 4 → ℝ) :
    pd i (pd j (fun y => c * planeWaveG k w y)) x
      = c * k j * k i * w'' (dotCov k x) := by
  rw [pd_scaled_planeWaveG k c w w' hw j]
  have h2 := pd_scaled_planeWaveG k (c * k j) w' w'' hw' i
  have h3 := congrFun h2 x
  rw [h3]
  unfold planeWaveG
  ring

/-! ## C — O TEOREMA GERAL: qualquer direção nula TT resolve -/

/-- [KERNEL] ★★★ O CONE CONTÍNUO: para QUALQUER covetor NULO k e QUALQUER
    polarização ε simétrica, η-traço zero e k-transversal, a onda plana
    resolve o vácuo linearizado em toda parte. Subsume os cones 1,2,3 E
    a direção nula arbitrária — o setor de ondas planas TT FECHADO.

    As três hipóteses matam os três termos do Ricci linearizado:
    η-traço zero ⟹ termo do traço; k-transversal ⟹ os dois ∂_α∂_μ;
    k-nulo ⟹ o d'Alembertiano. -/
theorem general_null_tt_ricci_zero
    (k : Fin 4 → ℝ) (ε : Fin 4 → Fin 4 → ℝ) (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u)
    (hsymm : ∀ μ ν, ε μ ν = ε ν μ)
    (htraceless : (∑ γ : Fin 4, etaDiag γ * ε γ γ) = 0)
    (htransverse : ∀ ν, (∑ α : Fin 4, etaDiag α * k α * ε α ν) = 0)
    (hnull : (∑ α : Fin 4, etaDiag α * k α * k α) = 0)
    (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (fun μ ν => fun y => ε μ ν * planeWaveG k w y) μ ν x = 0 := by
  unfold linRicci
  have hpp : ∀ (μ' ν' i j : Fin 4),
      pd i (pd j (fun y => ε μ' ν' * planeWaveG k w y)) x
        = ε μ' ν' * k j * k i * w'' (dotCov k x) :=
    fun μ' ν' i j => pd_pd_planeWaveG k (ε μ' ν') w w' w'' hw hw' i j x
  -- o termo do traço: (Σ_γ η^γγ ε_γγ)·w'' = 0
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ * (ε γ γ * planeWaveG k w y))
      = fun y => (∑ γ : Fin 4, etaDiag γ * ε γ γ) * planeWaveG k w y := by
    funext y
    rw [Finset.sum_mul]
    congr 1
    funext γ
    ring
  have hpd_tr : pd μ (pd ν (fun y =>
      (∑ γ : Fin 4, etaDiag γ * ε γ γ) * planeWaveG k w y)) x
      = (∑ γ : Fin 4, etaDiag γ * ε γ γ) * k ν * k μ * w'' (dotCov k x) :=
    pd_pd_planeWaveG k (∑ γ : Fin 4, etaDiag γ * ε γ γ) w w' w'' hw hw' μ ν x
  rw [Fin.sum_univ_four]
  simp only [hpp]
  rw [htr, hpd_tr, htraceless]
  -- as tres condicoes, expandidas
  have hTν := htransverse ν
  have hTμ := htransverse μ
  rw [Fin.sum_univ_four] at hTν hTμ hnull
  norm_num [etaDiag, Fin.ext_iff] at hTν hTμ hnull ⊢
  generalize w'' ((dotCov k) x) = W
  linear_combination (W * k μ) * hTν + (W * k ν) * hTμ - (W * ε μ ν) * hnull

end

end TGLExt
