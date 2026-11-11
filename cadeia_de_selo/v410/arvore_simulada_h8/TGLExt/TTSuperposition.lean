import TGLExt.ColimitSeed

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A SUPERPOSIÇÃO TT: o espaço de soluções é um ESPAÇO — não uma onda só
  [TGLExt — v126, o incremento 47 do programa SemifiniteAnalysis]

A v125 provou que UMA onda TT resolve o vácuo linearizado. A física dos
flags pede mais: o SETOR — perturbações gerais. Esta pedra dá o passo
estrutural: a SUPERPOSIÇÃO de ondas TT com polarizações E perfis
INDEPENDENTES também resolve — o conjunto-solução é fechado por soma,
um subespaço vetorial de perturbações:

* ★★ `pd_scaled_fun_add` — a derivada distribui sobre o par de ondas
  (HasFDerivAt.add na redução algébrica);
* ★★★ `tt_superposition_ricci_zero` — a soma de DUAS ondas TT quaisquer
  (polarizações (a,b) e (a′,b′) independentes; perfis C² w e v
  independentes) resolve o vácuo linearizado em toda parte — por
  indução evidente, todo o SPAN das ondas TT resolve.

HONESTIDADE (nomeada): superposições ao longo do MESMO cone; direções
múltiplas de propagação e a decomposição completa de perturbações
gerais seguem ABERTAS; os 5 flags de física do gate NÃO se movem.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a derivada do par -/

/-- [KERNEL] ★★ a derivada distribui sobre o par de ondas escaladas. -/
theorem pd_scaled_fun_add (c₁ c₂ : ℝ) (w w' v v' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hv : ∀ u, HasDerivAt v (v' u) u) (j : Fin 4) :
    pd j (fun y => c₁ * lightWave w y + c₂ * lightWave v y)
      = fun y => c₁ * lightCone (Pi.single j 1) * lightWave w' y
        + c₂ * lightCone (Pi.single j 1) * lightWave v' y := by
  funext y
  unfold pd
  have hf : HasFDerivAt
      (fun z => c₁ * lightWave w z + c₂ * lightWave v z)
      ((c₁ • ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ)))
        + (c₂ • ((v' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ)))) y := by
    have h1 : HasFDerivAt (fun z => c₁ * lightWave w z)
        (c₁ • ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ))) y :=
      (((hw (lightCone y)).comp_hasFDerivAt y lightCone.hasFDerivAt).const_smul c₁)
    have h2 : HasFDerivAt (fun z => c₂ * lightWave v z)
        (c₂ • ((v' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ))) y :=
      (((hv (lightCone y)).comp_hasFDerivAt y lightCone.hasFDerivAt).const_smul c₂)
    exact h1.add h2
  rw [hf.fderiv]
  unfold lightWave
  simp [smul_eq_mul]
  ring

/-- [KERNEL] ★★ a segunda derivada do par: a redução completa. -/
theorem pd_pd_pair (c₁ c₂ : ℝ) (w w' w'' v v' v'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u)
    (hv : ∀ u, HasDerivAt v (v' u) u)
    (hv' : ∀ u, HasDerivAt v' (v'' u) u) (i j : Fin 4) (x : Fin 4 → ℝ) :
    pd i (pd j (fun y => c₁ * lightWave w y + c₂ * lightWave v y)) x
      = c₁ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
          * w'' (lightCone x)
        + c₂ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
          * v'' (lightCone x) := by
  rw [pd_scaled_fun_add c₁ c₂ w w' v v' hw hv j]
  have h2 := pd_scaled_fun_add (c₁ * lightCone (Pi.single j 1))
    (c₂ * lightCone (Pi.single j 1)) w' w'' v' v'' hw' hv' i
  have h3 := congrFun h2 x
  rw [h3]
  unfold lightWave
  ring

/-! ## B — a superposição resolve o vácuo -/

/-- o par de ondas TT: polarizações e perfis INDEPENDENTES. -/
def ttPair (a b a' b' : ℝ) (w v : ℝ → ℝ) (μ ν : Fin 4) :
    (Fin 4 → ℝ) → ℝ :=
  fun y => epsTT a b μ ν * lightWave w y + epsTT a' b' μ ν * lightWave v y

/-- [KERNEL] ★★★ A SUPERPOSIÇÃO RESOLVE: a soma de duas ondas TT
    quaisquer (polarizações e perfis independentes) tem Ricci
    linearizado ZERO em toda parte — o conjunto-solução é um ESPAÇO. -/
theorem tt_superposition_ricci_zero (a b a' b' : ℝ)
    (w w' w'' v v' v'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u)
    (hv : ∀ u, HasDerivAt v (v' u) u)
    (hv' : ∀ u, HasDerivAt v' (v'' u) u) (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (ttPair a b a' b' w v) μ ν x = 0 := by
  unfold linRicci ttPair
  have hpp : ∀ (c₁ c₂ : ℝ) (i j : Fin 4),
      pd i (pd j (fun y => c₁ * lightWave w y + c₂ * lightWave v y)) x
        = c₁ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
            * w'' (lightCone x)
          + c₂ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
            * v'' (lightCone x) :=
    fun c₁ c₂ i j => pd_pd_pair c₁ c₂ w w' w'' v v' v'' hw hw' hv hv' i j x
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ *
      (epsTT a b γ γ * lightWave w y + epsTT a' b' γ γ * lightWave v y))
      = fun y => (0 : ℝ) * lightWave w y + (0 : ℝ) * lightWave v y := by
    funext y
    rw [Fin.sum_univ_four]
    unfold etaDiag epsTT
    norm_num [Fin.ext_iff]
    ring
  rw [Fin.sum_univ_four]
  rw [hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp]
  rw [htr, hpp 0 0 μ ν]
  fin_cases μ <;> fin_cases ν <;>
    · norm_num [epsTT, etaDiag, lightCone_apply, Pi.single_apply, Fin.ext_iff]
      try ring

end

end TGLExt
