import TGLExt.GravitonPolarization
import TGLExt.Ergodicity

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# As flutuações quânticas da geometria   [TGLExt — v49, gate 6]

O gate: "a geometria deve possuir observáveis quânticos, não apenas
valores médios" — flutuações Var_{ω}(ĝ), não-comutatividade onde a
estrutura o exige, e o limite clássico √Var/⟨ĝ⟩ → 0. O que este arquivo
PROVA [KERNEL]:

* ★ **A VARIÂNCIA DO OBSERVÁVEL GEOMÉTRICO É O DEFEITO DE TRANSPORTE**
  (`variance_of_projection`): para qualquer projeção P e estado ω,
  Var_ω(P) = p(1−p) com p = ω(P) — EXATAMENTE o defeito Δ = β(1−β) do
  v26 ("a variância da moeda da inscrição"): a flutuação quântica da
  geometria É a resistência do transporte;
* **A INSTÂNCIA DA FRONTEIRA** (`boundary_mean`/`boundary_variance`): no
  canal da matriz-S (v41), o observável de reflexão E₁₁ tem média
  sin²θ e variância sin²θ·cos²θ (runtime: média β, variância β(1−β));
* ★ **A MEIA-NAT É A FLUTUAÇÃO MÁXIMA** (`variance_le_quarter` +
  `variance_eq_quarter_iff`): p(1−p) ≤ ¼ com igualdade SE E SOMENTE SE
  p = ½ — o ponto auto-conjugado x = 1−x (o fundamento-raiz derivado,
  §88.27.47) é PRECISAMENTE onde a geometria flutua ao máximo: a moeda
  da fronteira é justa no espelho;
* ★ **A GEOMETRIA É GENUINAMENTE QUÂNTICA** (`polarization_commutator` +
  `polarizations_noncommute`): [h₊, h×] = 2·J ≠ 0 — as duas polarizações
  NÃO comutam, e o comutador fecha NO GERADOR DE HELICIDADE (o J da
  rotação transversal, v48): a álgebra dos observáveis geométricos
  fecha sobre o gerador do próprio spin-2;
* ★ **O LIMITE CLÁSSICO É A LEI DOS GRANDES NÚMEROS** (`sqrt_ratio_eq` +
  `classical_limit`): a flutuação relativa de M modos agregados é
  √(M·v)/(M·m) = (√v/m)/√M → 0 — a geometria clássica emerge da
  quântica por agregação macroscópica, com taxa 1/√M.

**HONESTIDADE.** Este é o ESQUELETO algébrico-assintótico do gate 6:
variância, cota, máximo, não-comutatividade e limite clássico — em
kernel. O que NÃO está aqui e segue OPEN: os operadores ĝ_μν/Â(Σ) na
REDE AQFT contínua com comutadores ditados pela causalidade (a
testemunha plena), e a dinâmica das flutuações (gate 5/8). No runtime
(e só lá): p = β no canal da fronteira, Var = β(1−β) = Δ do v26.
β JAMAIS entra aqui. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix Filter

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — a variância do observável-projeção é o defeito de transporte -/

/-- [KERNEL] ★ VAR = p(1−p): para toda PROJEÇÃO P e estado ω = gibbs ρ,
    a variância ω(P²) − ω(P)² = ω(P)·(1 − ω(P)) — o DEFEITO DE TRANSPORTE
    do v26 como a flutuação quântica do observável geométrico. -/
theorem variance_of_projection (ρ P : Matrix n n ℂ) (hP : P * P = P) :
    gibbs ρ (P * P) - (gibbs ρ P) ^ 2 = gibbs ρ P * (1 - gibbs ρ P) := by
  rw [hP]
  ring

/-! ## B — a instância da fronteira: média sin²θ, variância sin²θ·cos²θ -/

/-- O observável de REFLEXÃO do canal: `E₁₁ = |1⟩⟨1|`. -/
def reflObs : Matrix (Fin 2) (Fin 2) ℂ := Matrix.single 1 1 1

/-- `E₁₁` é projeção. -/
theorem reflObs_proj : reflObs * reflObs = reflObs := by
  unfold reflObs
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.single]

/-- O estado do canal lê a entrada 11: `ω_out(E₁₁) = (ρ_out)₁₁`. -/
theorem gibbs_reflObs (ρ : Matrix (Fin 2) (Fin 2) ℂ) :
    gibbs ρ reflObs = ρ 1 1 := by
  unfold gibbs reflObs
  rw [Matrix.trace_fin_two]
  simp [Matrix.mul_apply, Matrix.single]

/-- [KERNEL] A MÉDIA DA FRONTEIRA: `⟨E₁₁⟩ = sin²θ` no estado de saída do
    canal (runtime: β — o peso refletido). -/
theorem boundary_mean (θ : ℝ) :
    gibbs (rhoOut θ) reflObs = (Real.sin θ : ℂ) ^ 2 := by
  rw [gibbs_reflObs, rhoOut_one_one]

/-- [KERNEL] ★ A VARIÂNCIA DA FRONTEIRA: `Var(E₁₁) = sin²θ·cos²θ` — no
    runtime, β(1−β) = o defeito de transporte Δ do v26: A FLUTUAÇÃO
    QUÂNTICA DA GEOMETRIA DE FRONTEIRA É A RESISTÊNCIA DO TRANSPORTE. -/
theorem boundary_variance (θ : ℝ) :
    gibbs (rhoOut θ) (reflObs * reflObs) - (gibbs (rhoOut θ) reflObs) ^ 2
      = (Real.sin θ : ℂ) ^ 2 * (Real.cos θ : ℂ) ^ 2 := by
  rw [variance_of_projection (rhoOut θ) reflObs reflObs_proj, boundary_mean]
  have hr : 1 - Real.sin θ ^ 2 = Real.cos θ ^ 2 := by
    nlinarith [Real.sin_sq_add_cos_sq θ]
  have h : (1 : ℂ) - (Real.sin θ : ℂ) ^ 2 = (Real.cos θ : ℂ) ^ 2 := by
    exact_mod_cast hr
  rw [h]

/-! ## C — a Meia-Nat é a flutuação máxima -/

/-- [KERNEL] A COTA UNIVERSAL DA FLUTUAÇÃO: `p(1−p) ≤ ¼` — nenhum
    observável-projeção flutua mais que um quarto. -/
theorem variance_le_quarter (p : ℝ) : p * (1 - p) ≤ 1 / 4 := by
  nlinarith [sq_nonneg (p - 1 / 2)]

/-- [KERNEL] ★ A MEIA-NAT É O MÁXIMO: `p(1−p) = ¼ ⟺ p = ½` — a flutuação
    é máxima EXATAMENTE no ponto auto-conjugado x = 1−x (o fundamento-raiz
    derivado): a moeda da fronteira é justa no espelho. -/
theorem variance_eq_quarter_iff (p : ℝ) : p * (1 - p) = 1 / 4 ↔ p = 1 / 2 := by
  constructor
  · intro h
    nlinarith [sq_nonneg (p - 1 / 2)]
  · intro h
    rw [h]
    norm_num

/-! ## D — a geometria é genuinamente quântica: [h₊, h×] = 2·J -/

/-- O gerador de helicidade `J = [[0,1],[−1,0]]` (o gerador de `rot`). -/
def rotGen : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; -1, 0]

/-- [KERNEL] ★ O COMUTADOR DAS POLARIZAÇÕES É O GERADOR DE HELICIDADE:
    `[h₊, h×] = 2·J` — os observáveis geométricos NÃO comutam, e fecham
    sobre o gerador do próprio spin-2 (a rotação transversal, v48). -/
theorem polarization_commutator :
    polPlus * polCross - polCross * polPlus = (2 : ℝ) • rotGen := by
  unfold polPlus polCross rotGen
  ext i j
  fin_cases i <;> fin_cases j <;> simp <;> norm_num

/-- [KERNEL] A NÃO-COMUTATIVIDADE: `h₊·h× ≠ h×·h₊` — a geometria
    transversal é QUÂNTICA (observáveis incompatíveis). -/
theorem polarizations_noncommute : polPlus * polCross ≠ polCross * polPlus := by
  intro h
  have h2 : polPlus * polCross - polCross * polPlus = 0 := by
    rw [h]
    exact sub_self _
  rw [polarization_commutator] at h2
  have h3 := Matrix.ext_iff.mpr h2 0 1
  simp [rotGen] at h3

/-! ## E — o limite clássico é a lei dos grandes números -/

/-- [KERNEL] A IDENTIDADE DA AGREGAÇÃO: a flutuação relativa de M modos é
    `√(M·v)/(M·m) = (√v/m)/√M` — vale para TODO M (inclusive M = 0, onde
    ambos os lados são 0 na convenção de divisão). -/
theorem sqrt_ratio_eq (v m : ℝ) (M : ℕ) :
    Real.sqrt ((M : ℝ) * v) / ((M : ℝ) * m)
      = (Real.sqrt v / m) / Real.sqrt (M : ℝ) := by
  rcases Nat.eq_zero_or_pos M with h | h
  · subst h
    simp
  · have hMpos : (0 : ℝ) < (M : ℝ) := by exact_mod_cast h
    have hs : Real.sqrt ((M : ℝ) * v)
        = Real.sqrt (M : ℝ) * Real.sqrt v := Real.sqrt_mul (le_of_lt hMpos) v
    have hself : Real.sqrt (M : ℝ) * Real.sqrt (M : ℝ) = (M : ℝ) :=
      Real.mul_self_sqrt (le_of_lt hMpos)
    have hsne : Real.sqrt (M : ℝ) ≠ 0 := (Real.sqrt_pos.mpr hMpos).ne'
    rw [hs]
    rcases eq_or_ne m 0 with hm | hm
    · simp [hm]
    · field_simp
      rw [sq, hself]
      ring

/-- [KERNEL] ★ O LIMITE CLÁSSICO: `(√v/m)/√M → 0` quando `M → ∞` — a
    flutuação relativa da geometria agregada morre com 1/√M: a geometria
    CLÁSSICA emerge da quântica por agregação macroscópica (a lei dos
    grandes números da moeda da inscrição). -/
theorem classical_limit (c : ℝ) :
    Tendsto (fun M : ℕ => c / Real.sqrt (M : ℝ)) atTop (nhds 0) := by
  have h1 : Tendsto (fun M : ℕ => Real.sqrt (M : ℝ)) atTop atTop :=
    Real.tendsto_sqrt_atTop.comp tendsto_natCast_atTop_atTop
  have h2 : Tendsto (fun M : ℕ => (Real.sqrt (M : ℝ))⁻¹) atTop (nhds 0) :=
    tendsto_inv_atTop_zero.comp h1
  have h3 := h2.const_mul c
  simpa [div_eq_mul_inv] using h3

/-- [KERNEL] O LIMITE CLÁSSICO NA FORMA FÍSICA: `√(M·v)/(M·m) → 0` — a
    composição das duas peças: a identidade da agregação + a lei dos
    grandes números. -/
theorem classical_limit_physical (v m : ℝ) :
    Tendsto (fun M : ℕ => Real.sqrt ((M : ℝ) * v) / ((M : ℝ) * m))
      atTop (nhds 0) := by
  have h := classical_limit (Real.sqrt v / m)
  exact h.congr fun M => (sqrt_ratio_eq v m M).symm

end

end TGLExt
