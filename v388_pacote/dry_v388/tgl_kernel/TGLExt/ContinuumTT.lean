import TGLExt.MixedLadder

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# O SETOR TT NO CONTÍNUO: ondas de spin-2 sem fantasma, com perfil arbitrário
  [TGLExt — v125, o incremento 45 do programa SemifiniteAnalysis]

O v75 fechou a face FINITA do spin-2 (hélice dupla ±2; TT positivo; duas
polarizações) e nomeou a honestidade: "Fierz–Pauli EL e ghost-freedom
pleno pedem o contínuo". O v114 construiu a onda no contínuo (d'Alembert
para qualquer perfil C²). Esta pedra SOLDA as duas: o setor TT de ondas
planas no CONTÍNUO, sobre o η da casa (diag(1,−1,−1,−1)):

* `epsTT a b` — a polarização TT geral (a·ε₊ + b·ε×, o plano 2-dim);
  ★ `epsTT_traceless` (η-traço zero) + ★ `epsTT_transverse` (suporte
  transversal ao cone x₁−x₀);
* ★★ `pd_pd_scaled` — a segunda derivada da onda escalada: ∂ᵢ∂ⱼ(c·w∘L)
  = c·L(eᵢ)L(eⱼ)·w″ — a REDUÇÃO ALGÉBRICA de todo o cálculo;
* ★★★ `tt_ricci_zero` — A ONDA TT RESOLVE O VÁCUO LINEARIZADO: o Ricci
  linearizado da onda h_{μν} = ε_{μν}·w(x₁−x₀) é ZERO em toda parte,
  para QUALQUER perfil C² — spin-2 SEM MASSA no contínuo (Fierz–Pauli
  no setor de ondas planas);
* ★★ `tt_component_wave` — cada componente satisfaz ∂₀²h = ∂₁²h
  (a onda do v114, componente a componente);
* ★★ `tt_kinetic_nonneg` + ★★★ `tt_kinetic_pos` — SEM FANTASMA: a
  densidade cinética do setor TT é ≥ 0 sempre, e > 0 onde a onda vive
  ((a,b) ≠ 0 e w′ ≠ 0) — a forma cinética é positiva-definida no
  plano das polarizações.

HONESTIDADE (nomeada, sem véu): este é o setor de ONDAS PLANAS; o
ghost-freedom para perturbações GERAIS (decomposição completa) e a
ausência de anomalias relevantes seguem ABERTOS — os flags de física
do gate NÃO se movem por esta pedra. A imobilidade é a credibilidade.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — o η diagonal da casa e a polarização TT -/

/-- a diagonal do η da casa: diag(1,−1,−1,−1). -/
def etaDiag : Fin 4 → ℝ := fun i => if i = 0 then 1 else -1

theorem eta4_eq_diagonal_etaDiag : eta4 = Matrix.diagonal etaDiag := by
  unfold eta4 etaDiag
  congr 1
  funext i
  fin_cases i <;> simp

/-- a polarização TT geral: a·ε₊ + b·ε× no plano (2,3). -/
def epsTT (a b : ℝ) : Fin 4 → Fin 4 → ℝ := fun μ ν =>
  if μ = 2 ∧ ν = 2 then a
  else if μ = 3 ∧ ν = 3 then -a
  else if (μ = 2 ∧ ν = 3) ∨ (μ = 3 ∧ ν = 2) then b
  else 0

theorem epsTT_symm (a b : ℝ) (μ ν : Fin 4) :
    epsTT a b μ ν = epsTT a b ν μ := by
  unfold epsTT
  fin_cases μ <;> fin_cases ν <;> norm_num [Fin.ext_iff]

/-- [KERNEL] ★ η-traço ZERO: Σ η^γγ ε_γγ = 0. -/
theorem epsTT_traceless (a b : ℝ) :
    (∑ γ : Fin 4, etaDiag γ * epsTT a b γ γ) = 0 := by
  unfold etaDiag epsTT
  rw [Fin.sum_univ_four]
  norm_num [Fin.ext_iff]

/-- [KERNEL] ★ TRANSVERSAL ao cone: as linhas 0 e 1 são nulas. -/
theorem epsTT_transverse (a b : ℝ) (ν : Fin 4) :
    epsTT a b 0 ν = 0 ∧ epsTT a b 1 ν = 0 := by
  unfold epsTT
  fin_cases ν <;> norm_num [Fin.ext_iff]

/-! ## B — a onda TT e a redução algébrica das derivadas -/

/-- a onda TT: h_{μν}(x) = ε_{μν}·w(x₁ − x₀). -/
def ttWave (a b : ℝ) (w : ℝ → ℝ) (μ ν : Fin 4) : (Fin 4 → ℝ) → ℝ :=
  fun x => epsTT a b μ ν * lightWave w x

/-- [KERNEL] ★★ a REDUÇÃO: ∂ⱼ(c·w∘L) = c·L(eⱼ)·w′∘L, como FUNÇÃO. -/
theorem pd_scaled_fun (c : ℝ) (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (j : Fin 4) :
    pd j (fun y => c * lightWave w y)
      = fun y => c * lightCone (Pi.single j 1) * lightWave w' y := by
  funext y
  unfold pd
  have hf : HasFDerivAt (fun z => c * lightWave w z)
      (c • ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ))) y := by
    have hbase : HasFDerivAt (lightWave w)
        ((w' (lightCone y)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ)) y :=
      (hw (lightCone y)).comp_hasFDerivAt y lightCone.hasFDerivAt
    exact hbase.const_smul c
  rw [hf.fderiv]
  unfold lightWave
  simp [smul_eq_mul]
  ring

/-- [KERNEL] ★★ a SEGUNDA REDUÇÃO: ∂ᵢ∂ⱼ(c·w∘L) = c·L(eⱼ)L(eᵢ)·w″∘L. -/
theorem pd_pd_scaled (c : ℝ) (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u) (i j : Fin 4) (x : Fin 4 → ℝ) :
    pd i (pd j (fun y => c * lightWave w y)) x
      = c * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
        * w'' (lightCone x) := by
  rw [pd_scaled_fun c w w' hw j]
  have h2 := pd_scaled_fun (c * lightCone (Pi.single j 1)) w' w'' hw' i
  have h3 := congrFun h2 x
  rw [h3]
  unfold lightWave
  ring

theorem lightCone_single_two :
    lightCone (Pi.single (2 : Fin 4) 1) = 0 := by
  rw [lightCone_apply]
  simp

theorem lightCone_single_three :
    lightCone (Pi.single (3 : Fin 4) 1) = 0 := by
  rw [lightCone_apply]
  simp

/-! ## C — o Ricci linearizado e o VÁCUO -/

/-- o Ricci linearizado sobre o fundo plano (η diagonal da casa):
    R⁽¹⁾_{μν} = ½[Σ_α η^αα(∂_α∂_μ h_{αν} + ∂_α∂_ν h_{αμ} − ∂_α∂_α h_{μν})
    − ∂_μ∂_ν(Σ_γ η^γγ h_{γγ})]. -/
def linRicci (h : Fin 4 → Fin 4 → ((Fin 4 → ℝ) → ℝ)) (μ ν : Fin 4)
    (x : Fin 4 → ℝ) : ℝ :=
  (∑ α : Fin 4, etaDiag α *
    (pd α (pd μ (h α ν)) x + pd α (pd ν (h α μ)) x
      - pd α (pd α (h μ ν)) x)) / 2
  - pd μ (pd ν (fun y => ∑ γ : Fin 4, etaDiag γ * h γ γ y)) x / 2

/-- [KERNEL] ★★★ A ONDA TT RESOLVE O VÁCUO LINEARIZADO: R⁽¹⁾ = 0 em toda
    parte, para QUALQUER perfil C² — spin-2 sem massa no contínuo. -/
theorem tt_ricci_zero (a b : ℝ) (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u) (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    linRicci (ttWave a b w) μ ν x = 0 := by
  unfold linRicci ttWave
  have hpp : ∀ (c : ℝ) (i j : Fin 4),
      pd i (pd j (fun y => c * lightWave w y)) x
        = c * lightCone (Pi.single j 1) * lightCone (Pi.single i 1)
          * w'' (lightCone x) :=
    fun c i j => pd_pd_scaled c w w' w'' hw hw' i j x
  have htr : (fun y => ∑ γ : Fin 4, etaDiag γ * (epsTT a b γ γ * lightWave w y))
      = fun y => (0 : ℝ) * lightWave w y := by
    funext y
    rw [Fin.sum_univ_four]
    unfold etaDiag epsTT
    norm_num [Fin.ext_iff]
  rw [Fin.sum_univ_four]
  rw [hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp, hpp]
  rw [htr, hpp 0 μ ν]
  fin_cases μ <;> fin_cases ν <;>
    · norm_num [epsTT, etaDiag, lightCone_apply, Pi.single_apply, Fin.ext_iff]
      try ring

/-- [KERNEL] ★★ cada componente é ONDA: ∂₀²h_{μν} = ∂₁²h_{μν}. -/
theorem tt_component_wave (a b : ℝ) (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u) (μ ν : Fin 4) (x : Fin 4 → ℝ) :
    pd 0 (pd 0 (ttWave a b w μ ν)) x = pd 1 (pd 1 (ttWave a b w μ ν)) x := by
  unfold ttWave
  rw [pd_pd_scaled (epsTT a b μ ν) w w' w'' hw hw' 0 0 x,
    pd_pd_scaled (epsTT a b μ ν) w w' w'' hw hw' 1 1 x,
    lightCone_single_zero, lightCone_single_one]
  ring

/-! ## D — SEM FANTASMA: a cinética do setor TT -/

/-- a densidade cinética do setor TT: Σ_{μν} (∂₀ h_{μν})². -/
def ttKinetic (a b : ℝ) (w : ℝ → ℝ) (x : Fin 4 → ℝ) : ℝ :=
  ∑ μ : Fin 4, ∑ ν : Fin 4, (pd 0 (ttWave a b w μ ν) x) ^ 2

theorem ttKinetic_eval (a b : ℝ) (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (x : Fin 4 → ℝ) :
    ttKinetic a b w x = 2 * (a ^ 2 + b ^ 2) * (w' (lightCone x)) ^ 2 := by
  unfold ttKinetic ttWave
  have hp : ∀ μ ν : Fin 4, pd 0 (fun y => epsTT a b μ ν * lightWave w y) x
      = epsTT a b μ ν * lightCone (Pi.single (0 : Fin 4) 1)
        * lightWave w' x :=
    fun μ ν => congrFun (pd_scaled_fun (epsTT a b μ ν) w w' hw 0) x
  simp only [hp, lightCone_single_zero]
  rw [Fin.sum_univ_four]
  simp only [Fin.sum_univ_four]
  unfold epsTT lightWave
  norm_num [Fin.ext_iff]
  try ring

/-- [KERNEL] ★★ SEM FANTASMA (≥): a cinética TT nunca é negativa. -/
theorem tt_kinetic_nonneg (a b : ℝ) (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (x : Fin 4 → ℝ) :
    0 ≤ ttKinetic a b w x := by
  rw [ttKinetic_eval a b w w' hw x]
  positivity

/-- [KERNEL] ★★★ SEM FANTASMA (>): onde a onda vive ((a,b) ≠ 0, w′ ≠ 0),
    a cinética é ESTRITAMENTE positiva — nenhum modo de norma negativa
    no plano das polarizações. -/
theorem tt_kinetic_pos (a b : ℝ) (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (x : Fin 4 → ℝ)
    (hab : a ≠ 0 ∨ b ≠ 0) (hwx : w' (lightCone x) ≠ 0) :
    0 < ttKinetic a b w x := by
  rw [ttKinetic_eval a b w w' hw x]
  have hsq : (0 : ℝ) < a ^ 2 + b ^ 2 := by
    rcases hab with ha | hb
    · have h1 : (0 : ℝ) < a ^ 2 := by positivity
      nlinarith [sq_nonneg b]
    · have h1 : (0 : ℝ) < b ^ 2 := by positivity
      nlinarith [sq_nonneg a]
  have hw2 : (0 : ℝ) < (w' (lightCone x)) ^ 2 := by positivity
  positivity

end

end TGLExt
