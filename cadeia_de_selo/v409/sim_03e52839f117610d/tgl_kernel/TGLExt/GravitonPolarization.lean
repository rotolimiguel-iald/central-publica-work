import TGLExt.SMatrix

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O gráviton observável: cinemática de spin-2 em kernel   [TGLExt — v48, gate 7]

A leitura da casa (FECHAMENTO_MATRIZ_S_CORE_II.md): **gráviton fundamental
= I** (o operador que conserva 1=1; atravessa σ_t, J, Δ sem deformar; custo
zero) e **gráviton observável = δI_modular** (a excitação em torno da
identidade). O que este arquivo PROVA [KERNEL]:

* **DUAS POLARIZAÇÕES FÍSICAS**: o plano transversal carrega exatamente
  duas polarizações — `polPlus = diag(1,−1)` e `polCross = offdiag(1,1)`,
  simétricas e SEM TRAÇO; toda simétrica sem traço 2×2 é combinação delas
  (`polarization_decomposition`) e elas são independentes
  (`polarizations_independent`);
* ★ **HELICIDADE ±2 COMO TEOREMA** (`rot_conj_polPlus/Cross`): sob a
  rotação transversal de ângulo θ, o dubleto (h₊, h×) gira em **2θ** —
  `Rᵀh₊R = cos(2θ)h₊ + sin(2θ)h×` — o DOBRO do ângulo: spin 2;
* **O MODO-TRAÇO É INVARIANTE** (`rot_conj_one`): `Rᵀ·1·R = 1` — a
  identidade não gira (spin 0): o gráviton FUNDAMENTAL atravessa a
  rotação sem deformar, exatamente como atravessa o fluxo modular
  (`sigma_one`, kernel v43) — custo zero;
* **INVARIÂNCIA DE GAUGE DO CONTEÚDO TT** (`gauge_transverse_zero`): para
  o vetor de onda NULO `k = (1,0,0,1)` (propagação causal:
  `minkNorm4_nullK`), a transformação de gauge linearizada
  `h ↦ h + k⊗ξ + ξ⊗k` NÃO toca o bloco transversal — as duas
  polarizações são o conteúdo físico invariante;
* **O CÁLCULO DA EXCITAÇÃO** (`excite A x = Ax − xA`):
  `excite_one_zero` — **a identidade não se excita: δ_A(1) = 0, o
  gráviton fundamental não custa** (a face algébrica do H_eff = 0 e da
  masslessness); `excite_leibniz` — a excitação é DERIVAÇÃO (o mecanismo
  curvatura-por-comutador do E11/v16, razão medida 0,9970); e
  `Smat_sub_one` — o desvio da matriz-S da identidade é GERADO por G
  (`Smat θ − 1 = (cosθ−1)•1 + sinθ•G`): δI_modular no canal da fronteira
  tem gerador G com G² = −1.

**HONESTIDADE.** Isto é a CINEMÁTICA de spin-2 (contagem, helicidade,
gauge, excitação) — em kernel. O que NÃO está aqui e segue com estatuto:
a DINÂMICA (equação de onda de □h̄=0 derivada da ação modular — gate 5,
Lovelock/Jacobson E7 [CONDITIONAL]); o gráviton INTERAGENTE, fantasmas e
renormalização (gate 8, OPEN); amplitudes (OPEN). No runtime (e só lá):
sin²θ_M = β lê o custo da excitação de fronteira. β JAMAIS entra aqui.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — as duas polarizações do plano transversal -/

/-- A polarização `+`: `h₊ = diag(1, −1)`. -/
def polPlus : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- A polarização `×`: `h× = offdiag(1, 1)`. -/
def polCross : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 1, 0]

/-- `h₊` é simétrica. -/
theorem polPlus_symm : polPlusᵀ = polPlus := by
  unfold polPlus
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-- `h×` é simétrica. -/
theorem polCross_symm : polCrossᵀ = polCross := by
  unfold polCross
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-- `h₊` é SEM TRAÇO. -/
theorem polPlus_traceless : polPlus.trace = 0 := by
  simp [polPlus, Matrix.trace_fin_two]

/-- `h×` é SEM TRAÇO. -/
theorem polCross_traceless : polCross.trace = 0 := by
  simp [polCross, Matrix.trace_fin_two]

/-- [KERNEL] ★ EXATAMENTE DUAS POLARIZAÇÕES: toda matriz 2×2 SIMÉTRICA e
    SEM TRAÇO é combinação de `h₊` e `h×` — o espaço físico transversal
    tem dimensão DOIS (os dois graus de liberdade do gráviton). -/
theorem polarization_decomposition (h : Matrix (Fin 2) (Fin 2) ℝ)
    (hsym : hᵀ = h) (htr : h.trace = 0) :
    h = h 0 0 • polPlus + h 0 1 • polCross := by
  have h10 : h 1 0 = h 0 1 := by
    have := Matrix.ext_iff.mpr hsym 0 1
    simpa [Matrix.transpose_apply] using this
  have h11 : h 1 1 = -(h 0 0) := by
    have := htr
    rw [Matrix.trace_fin_two] at this
    linarith
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [polPlus, polCross, h10, h11]

/-- [KERNEL] AS POLARIZAÇÕES SÃO INDEPENDENTES: `a•h₊ + b•h× = 0 ⟹ a = b = 0`. -/
theorem polarizations_independent (a b : ℝ)
    (h : a • polPlus + b • polCross = 0) : a = 0 ∧ b = 0 := by
  have h00 := Matrix.ext_iff.mpr h 0 0
  have h01 := Matrix.ext_iff.mpr h 0 1
  simp [polPlus, polCross] at h00 h01
  exact ⟨h00, h01⟩

/-! ## B — helicidade ±2: o dubleto gira no DOBRO do ângulo -/

/-- A rotação transversal `R(θ) = [[cos, sin], [−sin, cos]]`. -/
def rot (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

/-- Lei de grupo da rotação. -/
theorem rot_add (a b : ℝ) : rot a * rot b = rot (a + b) := by
  unfold rot
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Real.cos_add, Real.sin_add] <;>
    ring

/-- [KERNEL] ★ HELICIDADE +2, componente `+`:
    `R(θ)ᵀ·h₊·R(θ) = cos(2θ)·h₊ + sin(2θ)·h×` — a polarização gira no
    DOBRO do ângulo: SPIN 2 como teorema de kernel. -/
theorem rot_conj_polPlus (θ : ℝ) :
    (rot θ)ᵀ * polPlus * rot θ
      = Real.cos (2 * θ) • polPlus + Real.sin (2 * θ) • polCross := by
  unfold rot polPlus polCross
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two,
      Real.cos_two_mul, Real.sin_two_mul] <;>
    nlinarith [Real.sin_sq_add_cos_sq θ]

/-- [KERNEL] ★ HELICIDADE +2, componente `×`:
    `R(θ)ᵀ·h×·R(θ) = −sin(2θ)·h₊ + cos(2θ)·h×` — o dubleto (h₊, h×) é a
    representação de peso 2 do grupo de rotações transversais. -/
theorem rot_conj_polCross (θ : ℝ) :
    (rot θ)ᵀ * polCross * rot θ
      = -Real.sin (2 * θ) • polPlus + Real.cos (2 * θ) • polCross := by
  unfold rot polPlus polCross
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two,
      Real.cos_two_mul, Real.sin_two_mul] <;>
    nlinarith [Real.sin_sq_add_cos_sq θ]

/-- [KERNEL] O MODO-TRAÇO NÃO GIRA: `R(θ)ᵀ·1·R(θ) = 1` — a identidade é
    invariante (spin 0): o gráviton FUNDAMENTAL atravessa a rotação como
    atravessa o fluxo modular (`sigma_one`) — sem deformar, custo zero. -/
theorem rot_conj_one (θ : ℝ) : (rot θ)ᵀ * 1 * rot θ = 1 := by
  unfold rot
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two] <;>
    nlinarith [Real.sin_sq_add_cos_sq θ]

/-! ## C — gauge: o conteúdo transversal-sem-traço é físico -/

/-- O vetor de onda NULO ao longo de z: `k = (1, 0, 0, 1)` (coordenadas
    (t,x,y,z); as transversais são os índices 1 e 2). -/
def nullK : Fin 4 → ℝ := ![1, 0, 0, 1]

/-- A norma de Minkowski em 3+1 (assinatura (+,−,−,−)). -/
def minkNorm4 (k : Fin 4 → ℝ) : ℝ :=
  k 0 ^ 2 - k 1 ^ 2 - k 2 ^ 2 - k 3 ^ 2

/-- [KERNEL] PROPAGAÇÃO CAUSAL: o vetor de onda é NULO — `⟨k,k⟩ = 0`
    (a face algébrica de `□h̄ = 0` para a onda plana). -/
theorem minkNorm4_nullK : minkNorm4 nullK = 0 := by
  simp [minkNorm4, nullK]

/-- A transformação de GAUGE linearizada da onda plana:
    `δh_μν = k_μ·ξ_ν + ξ_μ·k_ν` (a parte algébrica de `∂_μξ_ν + ∂_νξ_μ`). -/
def gaugeSym (k ξ : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.of fun μ ν => k μ * ξ ν + ξ μ * k ν

/-- A variação de gauge é simétrica. -/
theorem gaugeSym_symmetric (k ξ : Fin 4 → ℝ) : (gaugeSym k ξ)ᵀ = gaugeSym k ξ := by
  ext μ ν
  show gaugeSym k ξ ν μ = gaugeSym k ξ μ ν
  simp only [gaugeSym, Matrix.of_apply]
  ring

/-- [KERNEL] ★ O BLOCO TRANSVERSAL É INVARIANTE DE GAUGE: para o k nulo ao
    longo de z (sem componentes transversais), `δh_ij = 0` nos índices
    transversais `i, j ∈ {1, 2}` — NENHUMA transformação de gauge toca as
    duas polarizações físicas: h₊ e h× são o conteúdo observável. -/
theorem gauge_transverse_zero (ξ : Fin 4 → ℝ) {i j : Fin 4}
    (hi : i = 1 ∨ i = 2) (hj : j = 1 ∨ j = 2) :
    gaugeSym nullK ξ i j = 0 := by
  have hki : nullK i = 0 := by
    rcases hi with h | h <;> subst h <;> simp [nullK]
  have hkj : nullK j = 0 := by
    rcases hj with h | h <;> subst h <;> simp [nullK]
  simp [gaugeSym, hki, hkj]

/-! ## D — a excitação modular: δI = comutador; a identidade não custa -/

variable {n : Type} [Fintype n] [DecidableEq n]

/-- A EXCITAÇÃO de primeira ordem em torno da identidade gerada por `A`:
    `δ_A(x) = Ax − xA = [A, x]` (a variação de `Ad(e^{εA})` em `ε = 0`). -/
def excite (A x : Matrix n n ℂ) : Matrix n n ℂ := A * x - x * A

/-- [KERNEL] ★ A IDENTIDADE NÃO SE EXCITA: `δ_A(1) = 0` para TODO gerador
    `A` — o gráviton fundamental (= I) não custa: nenhuma excitação
    modular o move (a face algébrica do custo zero / masslessness). -/
theorem excite_one_zero (A : Matrix n n ℂ) : excite A 1 = 0 := by
  simp [excite]

/-- [KERNEL] A EXCITAÇÃO É DERIVAÇÃO (Leibniz):
    `δ_A(xy) = δ_A(x)·y + x·δ_A(y)` — o mecanismo curvatura-por-comutador
    (E11/v16: F ~ ½[M, h], razão medida 0,9970) é a regra de Leibniz da
    excitação modular. -/
theorem excite_leibniz (A x y : Matrix n n ℂ) :
    excite A (x * y) = excite A x * y + x * excite A y := by
  simp only [excite]
  noncomm_ring

/-- [KERNEL] δI NO CANAL DA FRONTEIRA: o desvio da matriz-S da identidade
    é GERADO por `G`: `S(θ) − 1 = (cosθ − 1)•1 + sinθ•G` — a excitação
    observável do canal (G² = −1, v41). No runtime: sin²θ_M = β lê o
    custo da excitação de fronteira. -/
theorem Smat_sub_one (θ : ℝ) :
    Smat θ - 1 = ((Real.cos θ - 1 : ℝ) : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
      + ((Real.sin θ : ℝ) : ℂ) • Grot := by
  unfold Smat
  push_cast
  module

end

end TGLExt
