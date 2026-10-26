import TGLExt.GNSQuotient

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A TERCEIRA DIREÇÃO: o setor TT cobre as TRÊS direções nulas espaciais
  [TGLExt — v128, o incremento 51 do programa SemifiniteAnalysis]

A v127 deu o segundo cone (x₂−x₀). Esta pedra fecha a terceira direção
espacial (x₃−x₀) e a superposição TRIPLA — o setor de ondas planas TT
cobre as três direções nulas geradas pelos eixos espaciais:

* `lightCone3` (x₃−x₀) com o plano de polarizações (1,2) (`epsTT3`:
  η-traço zero; transversal);
* ★★ `tt3_ricci_zero` — a onda TT da terceira direção resolve o vácuo
  linearizado (perfil C² qualquer);
* ★★★ `tt_triple_ricci_zero` — A SUPERPOSIÇÃO DAS TRÊS DIREÇÕES: onda
  no cone 1 (plano 2,3) + cone 2 (plano 1,3) + cone 3 (plano 1,2),
  polarizações e perfis TODOS independentes, resolve o vácuo
  linearizado em toda parte — o espaço-solução cobre as três direções
  nulas espaciais de propagação.

HONESTIDADE (nomeada): três direções por EIXO ≠ todas as direções nulas
(o cone contínuo); a decomposição completa de perturbações gerais e as
anomalias seguem ABERTAS; os 5 flags de física do gate NÃO se movem.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — o terceiro cone -/

/-- o terceiro cone: L₃(x) = x₃ − x₀. -/
def lightCone3 : (Fin 4 → ℝ) →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) (3 : Fin 4))
    - (ContinuousLinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) (0 : Fin 4))

theorem lightCone3_apply (x : Fin 4 → ℝ) : lightCone3 x = x 3 - x 0 := by
  unfold lightCone3
  simp [sub_apply]

def lightWave3 (w : ℝ → ℝ) (x : Fin 4 → ℝ) : ℝ := w (lightCone3 x)

/-- a polarização TT da terceira direção: o plano (1,2). -/
def epsTT3 (a b : ℝ) : Fin 4 → Fin 4 → ℝ := fun μ ν =>
  if μ = 1 ∧ ν = 1 then a
  else if μ = 2 ∧ ν = 2 then -a
  else if (μ = 1 ∧ ν = 2) ∨ (μ = 2 ∧ ν = 1) then b
  else 0

theorem epsTT3_traceless (a b : ℝ) :
    (∑ γ : Fin 4, etaDiag γ * epsTT3 a b γ γ) = 0 := by
  unfold etaDiag epsTT3
  rw [Fin.sum_univ_four]
  norm_num [Fin.ext_iff]

theorem epsTT3_transverse (a b : ℝ) (ν : Fin 4) :
    epsTT3 a b 0 ν = 0 ∧ epsTT3 a b 3 ν = 0 := by
  unfold epsTT3
  fin_cases ν <;> norm_num [Fin.ext_iff]

/-! ## B — as reduções -/

theorem pd_scaled_fun3 (c : ℝ) (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (j : Fin 4) :
    pd j (fun y => c * lightWave3 w y)
      = fun y => c * lightCone3 (Pi.single j 1) * lightWave3 w' y := by
  funext y
  unfold pd
  have hf : HasFDerivAt (fun z => c * lightWave3 w z)
      (c • ((w' (lightCone3 y)) • (lightCone3 : (Fin 4 → ℝ) →L[ℝ] ℝ))) y := by
    have hbase : HasFDerivAt (lightWave3 w)
        ((w' (lightCone3 y)) • (lightCone3 : (Fin 4 → ℝ) →L[ℝ] ℝ)) y :=
      (hw (lightCone3 y)).comp_hasFDerivAt y lightCone3.hasFDerivAt
    exact hbase.const_smul c
  rw [hf.fderiv]
  unfold lightWave3
  simp [smul_eq_mul]
  ring

theorem lightCone3_single_zero : lightCone3 (Pi.single (0 : Fin 4) 1) = -1 := by
  rw [lightCone3_apply]; simp
theorem lightCone3_single_one : lightCone3 (Pi.single (1 : Fin 4) 1) = 0 := by
  rw [lightCone3_apply]; simp
theorem lightCone3_single_two : lightCone3 (Pi.single (2 : Fin 4) 1) = 0 := by
  rw [lightCone3_apply]; simp
theorem lightCone3_single_three : lightCone3 (Pi.single (3 : Fin 4) 1) = 1 := by
  rw [lightCone3_apply]; simp

/-! ## C — a terceira direção resolve -/

def ttWave3 (a b : ℝ) (v : ℝ → ℝ) (μ ν : Fin 4) : (Fin 4 → ℝ) → ℝ :=
  fun x => epsTT3 a b μ ν * lightWave3 v x

/-- [KERNEL] ★★ a onda da TERCEIRA direção resolve o vácuo linearizado. -/
theorem tt3_ricci_zero (a b : ℝ) (v v' v'' : ℝ → ℝ)
    (hv : ∀ u, HasDerivAt v (v' u) u)
    (hv' : ∀ u, HasDerivAt v' (v'' u) u) (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (ttWave3 a b v) μ ν x = 0 := by
  unfold linRicci ttWave3
  have hpp : ∀ (c : ℝ) (i j : Fin 4),
      pd i (pd j (fun y => c * lightWave3 v y)) x
        = c * lightCone3 (Pi.single j 1) * lightCone3 (Pi.single i 1)
          * v'' (lightCone3 x) := by
    intro c i j
    rw [pd_scaled_fun3 c v v' hv j]
    have h2 := pd_scaled_fun3 (c * lightCone3 (Pi.single j 1)) v' v'' hv' i
    have h3 := congrFun h2 x
    rw [h3]
    unfold lightWave3
    ring
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ *
      (epsTT3 a b γ γ * lightWave3 v y))
      = fun y => (0 : ℝ) * lightWave3 v y := by
    funext y
    rw [Fin.sum_univ_four]
    unfold etaDiag epsTT3
    norm_num [Fin.ext_iff]
  rw [Fin.sum_univ_four]
  rw [hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp]
  rw [htr, hpp 0 μ ν]
  fin_cases μ <;> fin_cases ν <;>
    · norm_num [epsTT3, etaDiag, lightCone3_apply, Pi.single_apply, Fin.ext_iff]
      try ring

/-! ## D — a superposição das TRÊS direções -/

/-- a redução TRIPLA. -/
theorem pd_scaled_fun_triple (c₁ c₂ c₃ : ℝ) (w w' v v' u u' : ℝ → ℝ)
    (hw : ∀ z, HasDerivAt w (w' z) z)
    (hv : ∀ z, HasDerivAt v (v' z) z)
    (hu : ∀ z, HasDerivAt u (u' z) z) (j : Fin 4) :
    pd j (fun y => c₁ * lightWave w y + c₂ * lightWave2 v y
        + c₃ * lightWave3 u y)
      = fun y => c₁ * lightCone (Pi.single j 1) * lightWave w' y
        + c₂ * lightCone2 (Pi.single j 1) * lightWave2 v' y
        + c₃ * lightCone3 (Pi.single j 1) * lightWave3 u' y := by
  funext y
  unfold pd
  have hf : HasFDerivAt
      (fun z => c₁ * lightWave w z + c₂ * lightWave2 v z + c₃ * lightWave3 u z)
      ((c₁ • ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ)))
        + (c₂ • ((v' (lightCone2 y)) • (lightCone2 : (Fin 4 → ℝ) →L[ℝ] ℝ)))
        + (c₃ • ((u' (lightCone3 y)) • (lightCone3 : (Fin 4 → ℝ) →L[ℝ] ℝ)))) y := by
    have h1 : HasFDerivAt (fun z => c₁ * lightWave w z)
        (c₁ • ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ))) y :=
      (((hw (lightCone y)).comp_hasFDerivAt y lightCone.hasFDerivAt).const_smul c₁)
    have h2 : HasFDerivAt (fun z => c₂ * lightWave2 v z)
        (c₂ • ((v' (lightCone2 y)) • (lightCone2 : (Fin 4 → ℝ) →L[ℝ] ℝ))) y :=
      (((hv (lightCone2 y)).comp_hasFDerivAt y lightCone2.hasFDerivAt).const_smul c₂)
    have h3 : HasFDerivAt (fun z => c₃ * lightWave3 u z)
        (c₃ • ((u' (lightCone3 y)) • (lightCone3 : (Fin 4 → ℝ) →L[ℝ] ℝ))) y :=
      (((hu (lightCone3 y)).comp_hasFDerivAt y lightCone3.hasFDerivAt).const_smul c₃)
    exact (h1.add h2).add h3
  rw [hf.fderiv]
  unfold lightWave lightWave2 lightWave3
  simp [smul_eq_mul]
  ring

theorem pd_pd_triple (c₁ c₂ c₃ : ℝ) (w w' w'' v v' v'' u u' u'' : ℝ → ℝ)
    (hw : ∀ z, HasDerivAt w (w' z) z) (hw' : ∀ z, HasDerivAt w' (w'' z) z)
    (hv : ∀ z, HasDerivAt v (v' z) z) (hv' : ∀ z, HasDerivAt v' (v'' z) z)
    (hu : ∀ z, HasDerivAt u (u' z) z) (hu' : ∀ z, HasDerivAt u' (u'' z) z)
    (i j : Fin 4) (x : Fin 4 → ℝ) :
    pd i (pd j (fun y => c₁ * lightWave w y + c₂ * lightWave2 v y
        + c₃ * lightWave3 u y)) x
      = c₁ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
          * w'' (lightCone x)
        + c₂ * lightCone2 (Pi.single j 1) * lightCone2 (Pi.single i 1)
          * v'' (lightCone2 x)
        + c₃ * lightCone3 (Pi.single j 1) * lightCone3 (Pi.single i 1)
          * u'' (lightCone3 x) := by
  rw [pd_scaled_fun_triple c₁ c₂ c₃ w w' v v' u u' hw hv hu j]
  have h2 := pd_scaled_fun_triple (c₁ * lightCone (Pi.single j 1))
    (c₂ * lightCone2 (Pi.single j 1)) (c₃ * lightCone3 (Pi.single j 1))
    w' w'' v' v'' u' u'' hw' hv' hu' i
  have h3 := congrFun h2 x
  rw [h3]
  unfold lightWave lightWave2 lightWave3
  ring

def ttTriple (a b a' b' a'' b'' : ℝ) (w v u : ℝ → ℝ) (μ ν : Fin 4) :
    (Fin 4 → ℝ) → ℝ :=
  fun y => epsTT a b μ ν * lightWave w y + epsTT2 a' b' μ ν * lightWave2 v y
    + epsTT3 a'' b'' μ ν * lightWave3 u y

/-- [KERNEL] ★★★ A SUPERPOSIÇÃO DAS TRÊS DIREÇÕES resolve o vácuo
    linearizado em toda parte — o espaço-solução cobre as três direções
    nulas espaciais de propagação. -/
theorem tt_triple_ricci_zero (a b a' b' a'' b'' : ℝ)
    (w w' w'' v v' v'' u u' u'' : ℝ → ℝ)
    (hw : ∀ z, HasDerivAt w (w' z) z) (hw' : ∀ z, HasDerivAt w' (w'' z) z)
    (hv : ∀ z, HasDerivAt v (v' z) z) (hv' : ∀ z, HasDerivAt v' (v'' z) z)
    (hu : ∀ z, HasDerivAt u (u' z) z) (hu' : ∀ z, HasDerivAt u' (u'' z) z)
    (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (ttTriple a b a' b' a'' b'' w v u) μ ν x = 0 := by
  unfold linRicci ttTriple
  have hpp : ∀ (c₁ c₂ c₃ : ℝ) (i j : Fin 4),
      pd i (pd j (fun y => c₁ * lightWave w y + c₂ * lightWave2 v y
          + c₃ * lightWave3 u y)) x
        = c₁ * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
            * w'' (lightCone x)
          + c₂ * lightCone2 (Pi.single j 1) * lightCone2 (Pi.single i 1)
            * v'' (lightCone2 x)
          + c₃ * lightCone3 (Pi.single j 1) * lightCone3 (Pi.single i 1)
            * u'' (lightCone3 x) :=
    fun c₁ c₂ c₃ i j =>
      pd_pd_triple c₁ c₂ c₃ w w' w'' v v' v'' u u' u'' hw hw' hv hv' hu hu' i j x
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ *
      (epsTT a b γ γ * lightWave w y + epsTT2 a' b' γ γ * lightWave2 v y
        + epsTT3 a'' b'' γ γ * lightWave3 u y))
      = fun y => (0 : ℝ) * lightWave w y + (0 : ℝ) * lightWave2 v y
        + (0 : ℝ) * lightWave3 u y := by
    funext y
    rw [Fin.sum_univ_four]
    unfold etaDiag epsTT epsTT2 epsTT3
    norm_num [Fin.ext_iff]
    ring
  rw [Fin.sum_univ_four]
  rw [hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp]
  rw [htr, hpp 0 0 0 μ ν]
  fin_cases μ <;> fin_cases ν <;>
    · norm_num [epsTT, epsTT2, epsTT3, etaDiag, lightCone_apply, lightCone2_apply,
        lightCone3_apply, Pi.single_apply, Fin.ext_iff]
      try ring

end

end TGLExt
