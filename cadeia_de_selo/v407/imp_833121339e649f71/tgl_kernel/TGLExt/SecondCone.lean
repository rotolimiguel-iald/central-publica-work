import TGLExt.GNSTower

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A SEGUNDA DIREÇÃO: cones independentes — e a superposição ENTRE direções
  [TGLExt — v127, o incremento 49 do programa SemifiniteAnalysis]

A v125/v126 fecharam o setor TT de UM cone (x₁−x₀) e seu span. A cara
que os flags de física pedem é o setor GERAL — e o primeiro degrau real
é a SEGUNDA direção de propagação:

* `lightCone2` (x₂−x₀) — o segundo cone nulo, com suas ondas e o plano
  de polarizações (1,3) (`epsTT2`: η-traço zero; transversal);
* ★★ `tt2_ricci_zero` — a onda TT da segunda direção resolve o vácuo
  linearizado (perfil C² qualquer) — a construção NÃO era um acidente
  da direção;
* ★★ `pd_pd_cross` — a redução MISTA: derivadas do par com cones
  DIFERENTES;
* ★★★ `tt_cross_direction_ricci_zero` — A SUPERPOSIÇÃO ENTRE DIREÇÕES:
  onda no cone 1 + onda no cone 2 (polarizações e perfis independentes)
  resolve o vácuo linearizado em toda parte — o espaço-solução cruza
  direções de propagação.

HONESTIDADE (nomeada): duas direções ≠ todas; a decomposição completa
de perturbações gerais e as anomalias seguem ABERTAS; os 5 flags de
física do gate NÃO se movem.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — o segundo cone e suas polarizações -/

/-- o segundo cone: L₂(x) = x₂ − x₀. -/
def lightCone2 : (Fin 4 → ℝ) →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) (2 : Fin 4))
    - (ContinuousLinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) (0 : Fin 4))

theorem lightCone2_apply (x : Fin 4 → ℝ) : lightCone2 x = x 2 - x 0 := by
  unfold lightCone2
  simp [ContinuousLinearMap.sub_apply]

/-- a onda da segunda direção. -/
def lightWave2 (w : ℝ → ℝ) (x : Fin 4 → ℝ) : ℝ := w (lightCone2 x)

/-- a polarização TT da segunda direção: o plano (1,3). -/
def epsTT2 (a b : ℝ) : Fin 4 → Fin 4 → ℝ := fun μ ν =>
  if μ = 1 ∧ ν = 1 then a
  else if μ = 3 ∧ ν = 3 then -a
  else if (μ = 1 ∧ ν = 3) ∨ (μ = 3 ∧ ν = 1) then b
  else 0

/-- [KERNEL] ★ η-traço ZERO no segundo plano. -/
theorem epsTT2_traceless (a b : ℝ) :
    (∑ γ : Fin 4, etaDiag γ * epsTT2 a b γ γ) = 0 := by
  unfold etaDiag epsTT2
  rw [Fin.sum_univ_four]
  norm_num [Fin.ext_iff]

/-- [KERNEL] ★ transversal ao segundo cone: linhas 0 e 2 nulas. -/
theorem epsTT2_transverse (a b : ℝ) (ν : Fin 4) :
    epsTT2 a b 0 ν = 0 ∧ epsTT2 a b 2 ν = 0 := by
  unfold epsTT2
  fin_cases ν <;> norm_num [Fin.ext_iff]

/-! ## B — as reduções da segunda direção e a MISTA -/

theorem pd_scaled_fun2 (c : ℝ) (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (j : Fin 4) :
    pd j (fun y => c * lightWave2 w y)
      = fun y => c * lightCone2 (Pi.single j 1) * lightWave2 w' y := by
  funext y
  unfold pd
  have hf : HasFDerivAt (fun z => c * lightWave2 w z)
      (c • ((w' (lightCone2 y)) • (lightCone2 : (Fin 4 → ℝ) →L[ℝ] ℝ))) y := by
    have hbase : HasFDerivAt (lightWave2 w)
        ((w' (lightCone2 y)) • (lightCone2 : (Fin 4 → ℝ) →L[ℝ] ℝ)) y :=
      (hw (lightCone2 y)).comp_hasFDerivAt y lightCone2.hasFDerivAt
    exact hbase.const_smul c
  rw [hf.fderiv]
  unfold lightWave2
  simp [smul_eq_mul]
  ring

/-- [KERNEL] ★★ a redução MISTA: o par com cones DIFERENTES. -/
theorem pd_scaled_fun_cross (c₁ c₂ : ℝ) (w w' v v' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hv : ∀ u, HasDerivAt v (v' u) u) (j : Fin 4) :
    pd j (fun y => c₁ * lightWave w y + c₂ * lightWave2 v y)
      = fun y => c₁ * lightCone (Pi.single j 1) * lightWave w' y
        + c₂ * lightCone2 (Pi.single j 1) * lightWave2 v' y := by
  funext y
  unfold pd
  have hf : HasFDerivAt
      (fun z => c₁ * lightWave w z + c₂ * lightWave2 v z)
      ((c₁ • ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ)))
        + (c₂ • ((v' (lightCone2 y)) • (lightCone2 : (Fin 4 → ℝ) →L[ℝ] ℝ)))) y := by
    have h1 : HasFDerivAt (fun z => c₁ * lightWave w z)
        (c₁ • ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ))) y :=
      (((hw (lightCone y)).comp_hasFDerivAt y lightCone.hasFDerivAt).const_smul c₁)
    have h2 : HasFDerivAt (fun z => c₂ * lightWave2 v z)
        (c₂ • ((v' (lightCone2 y)) • (lightCone2 : (Fin 4 → ℝ) →L[ℝ] ℝ))) y :=
      (((hv (lightCone2 y)).comp_hasFDerivAt y lightCone2.hasFDerivAt).const_smul c₂)
    exact h1.add h2
  rw [hf.fderiv]
  unfold lightWave lightWave2
  simp [smul_eq_mul]
  ring

/-- [KERNEL] ★★ a segunda derivada MISTA. -/
theorem pd_pd_cross (c₁ c₂ : ℝ) (w w' w'' v v' v'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u)
    (hv : ∀ u, HasDerivAt v (v' u) u)
    (hv' : ∀ u, HasDerivAt v' (v'' u) u) (i j : Fin 4) (x : Fin 4 → ℝ) :
    pd i (pd j (fun y => c₁ * lightWave w y + c₂ * lightWave2 v y)) x
      = c₁ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
          * w'' (lightCone x)
        + c₂ * lightCone2 (Pi.single j 1) * lightCone2 (Pi.single i 1)
          * v'' (lightCone2 x) := by
  rw [pd_scaled_fun_cross c₁ c₂ w w' v v' hw hv j]
  have h2 := pd_scaled_fun_cross (c₁ * lightCone (Pi.single j 1))
    (c₂ * lightCone2 (Pi.single j 1)) w' w'' v' v'' hw' hv' i
  have h3 := congrFun h2 x
  rw [h3]
  unfold lightWave lightWave2
  ring

theorem lightCone2_single_zero :
    lightCone2 (Pi.single (0 : Fin 4) 1) = -1 := by
  rw [lightCone2_apply]
  simp

theorem lightCone2_single_one :
    lightCone2 (Pi.single (1 : Fin 4) 1) = 0 := by
  rw [lightCone2_apply]
  simp

theorem lightCone2_single_two :
    lightCone2 (Pi.single (2 : Fin 4) 1) = 1 := by
  rw [lightCone2_apply]
  simp

theorem lightCone2_single_three :
    lightCone2 (Pi.single (3 : Fin 4) 1) = 0 := by
  rw [lightCone2_apply]
  simp

/-! ## C — a segunda direção resolve; e a superposição ENTRE direções -/

/-- a onda TT da segunda direção. -/
def ttWave2 (a b : ℝ) (v : ℝ → ℝ) (μ ν : Fin 4) : (Fin 4 → ℝ) → ℝ :=
  fun x => epsTT2 a b μ ν * lightWave2 v x

/-- [KERNEL] ★★ a onda da SEGUNDA direção resolve o vácuo linearizado. -/
theorem tt2_ricci_zero (a b : ℝ) (v v' v'' : ℝ → ℝ)
    (hv : ∀ u, HasDerivAt v (v' u) u)
    (hv' : ∀ u, HasDerivAt v' (v'' u) u) (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (ttWave2 a b v) μ ν x = 0 := by
  unfold linRicci ttWave2
  have hpp : ∀ (c : ℝ) (i j : Fin 4),
      pd i (pd j (fun y => c * lightWave2 v y)) x
        = c * lightCone2 (Pi.single j 1) * lightCone2 (Pi.single i 1)
          * v'' (lightCone2 x) := by
    intro c i j
    rw [pd_scaled_fun2 c v v' hv j]
    have h2 := pd_scaled_fun2 (c * lightCone2 (Pi.single j 1)) v' v'' hv' i
    have h3 := congrFun h2 x
    rw [h3]
    unfold lightWave2
    ring
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ *
      (epsTT2 a b γ γ * lightWave2 v y))
      = fun y => (0 : ℝ) * lightWave2 v y := by
    funext y
    rw [Fin.sum_univ_four]
    unfold etaDiag epsTT2
    norm_num [Fin.ext_iff]
  rw [Fin.sum_univ_four]
  rw [hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp]
  rw [htr, hpp 0 μ ν]
  fin_cases μ <;> fin_cases ν <;>
    · norm_num [epsTT2, etaDiag, lightCone2_apply, Pi.single_apply, Fin.ext_iff]
      try ring

/-- o par ENTRE direções: cone 1 (plano 2,3) + cone 2 (plano 1,3). -/
def ttCross (a b a' b' : ℝ) (w v : ℝ → ℝ) (μ ν : Fin 4) :
    (Fin 4 → ℝ) → ℝ :=
  fun y => epsTT a b μ ν * lightWave w y + epsTT2 a' b' μ ν * lightWave2 v y

/-- [KERNEL] ★★★ A SUPERPOSIÇÃO ENTRE DIREÇÕES: onda no cone 1 + onda no
    cone 2 (polarizações e perfis independentes) resolve o vácuo
    linearizado em toda parte — o espaço-solução CRUZA direções. -/
theorem tt_cross_direction_ricci_zero (a b a' b' : ℝ)
    (w w' w'' v v' v'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u)
    (hv : ∀ u, HasDerivAt v (v' u) u)
    (hv' : ∀ u, HasDerivAt v' (v'' u) u) (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (ttCross a b a' b' w v) μ ν x = 0 := by
  unfold linRicci ttCross
  have hpp : ∀ (c₁ c₂ : ℝ) (i j : Fin 4),
      pd i (pd j (fun y => c₁ * lightWave w y + c₂ * lightWave2 v y)) x
        = c₁ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
            * w'' (lightCone x)
          + c₂ * lightCone2 (Pi.single j 1) * lightCone2 (Pi.single i 1)
            * v'' (lightCone2 x) :=
    fun c₁ c₂ i j => pd_pd_cross c₁ c₂ w w' w'' v v' v'' hw hw' hv hv' i j x
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ *
      (epsTT a b γ γ * lightWave w y + epsTT2 a' b' γ γ * lightWave2 v y))
      = fun y => (0 : ℝ) * lightWave w y + (0 : ℝ) * lightWave2 v y := by
    funext y
    rw [Fin.sum_univ_four]
    unfold etaDiag epsTT epsTT2
    norm_num [Fin.ext_iff]
    ring
  rw [Fin.sum_univ_four]
  rw [hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp]
  rw [htr, hpp 0 0 μ ν]
  fin_cases μ <;> fin_cases ν <;>
    · norm_num [epsTT, epsTT2, etaDiag, lightCone_apply, lightCone2_apply,
        Pi.single_apply, Fin.ext_iff]
      try ring

end

end TGLExt
