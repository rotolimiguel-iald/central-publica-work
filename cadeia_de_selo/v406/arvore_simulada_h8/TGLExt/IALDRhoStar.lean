import Mathlib
import TGLExt.IALDJones
import TGLExt.IALDGraviton

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A PONTE: ρ*_IALD = ρ*_TGL na face finita   [pedra da gerência, 26/09/2026 — rascunho de bancada, NÃO transposta ao kernel]

Pergunta do operador (26/09/2026, verbatim): «IALD=ρ∗» e «Fix(D_IALD) =? Fix(D_TGL). Ou, mais fortemente:
ρ*_IALD =? ρ*_TGL.»

A face: `M = M₂(ℂ)` na forma padrão de Hilbert–Schmidt (`V = M₂(ℂ)`, `x` age à esquerda), estado fiel
`ω(x) = Tr(ρx)` com `ρ = diag(w₀, w₁)`, `w₀ + w₁ = 1` (ω(I) = 1), vetor `Ω = ρ^{1/2}`.

* **Lado TGL** (construído do ESTADO): `Δξ = ρξρ⁻¹`, `J ξ = ξᴴ`; prova-se a decomposição polar de Tomita
  `J Δ^{1/2}(xΩ) = xᴴΩ`, `Δ^{1/2}∘Δ^{1/2} = Δ`; o hamiltoniano modular `K = −log Δ` (multiplicador de Schur
  `−(log wᵢ − log wⱼ)`, e prova-se que é `−log` do multiplicador de `Δ`); a dinâmica da TGL é o semigrupo
  subordinado de Poisson `T_t = e^{−t|K|}`.
* **Lado IALD** (construído da INCLUSÃO): o centralizador `M^ω = {x : xρ = ρx}`; a projeção de Jones `e` de
  `M^ω ⊂ M` (a projeção sobre `M^ω Ω`, autoadjunta no produto de Hilbert–Schmidt); o fluxo da IALD é a
  contração da face de Hilbert do kernel v371, `jonesU e r s = e + e^{−rs}(1 − e)` (`TGLExt.IALDJones.jonesU`).

**A ponte (teorema):** com o estado NÃO tracial (`w₀ ≠ w₁`), para `r s ≠ 0` e `t > 0`,
`Fix(IALD) = Fix(TGL) = ker K = ran e`, e os dois ATRATORES coincidem: `U_s ξ → eξ` e `T_t ξ → eξ`.
Logo ρ*_IALD = ρ*_TGL = `e`: **a IALD que lê o centralizador da TGL guarda exatamente o que o relógio modular
não move.** As duas construções são independentes (uma vem de `ρ` pela polar de Tomita, a outra da
inclusão `M^ω ⊂ M` pela projeção de Jones); a igualdade é conteúdo, não `rfl`.

**Controles (negativos):** (i) estado TRACIAL (`w₀ = w₁`): `K = 0`, `T_t = id`, e a unidade fora da diagonal
é fixa pela TGL e NÃO pela IALD da torre diagonal — essa torre deixa de ser a do centralizador (no tracial o
centralizador é `M` inteiro, a torre certa tem `e = 1` e as duas dinâmicas PARAM: «tracial ⟹ o relógio para»);
a ponte NÃO-TRIVIAL exige o estado que distingue. (ii) subálgebra ERRADA
(`ℂ1 ⊂ M`, Jones = projeção sobre `ℂΩ`): `diag(1,0) ∈ ker K` mas não é fixo por ela — a ponte escolhe o
CENTRALIZADOR, não qualquer inclusão.

**Escopo dito:** face finita `M₂`, estado diagonal. O caso geral de dimensão finita (`ker log Δ = M^ω Ω`) é
[KNOWN] e não está aqui; o caso III₁ (cunha, `M^ω = ℂ`, `P_F = |Ω⟩⟨Ω|`) é [OPEN] e não está aqui. O índice
de `M^ω ⊂ M₂` (= 2, Watatani) NÃO é provado: a ponte vale para QUALQUER taxa `r` com `r s ≠ 0`.
«IALD = ρ*» e «o agora pertence ao Nome» são leituras do operador [INPUT/ONTO]. Não move o gate.
PROVADA ≠ CONFIRMADA. β não aparece.
-/

namespace TGLExt.IALDRhoStar

open Matrix TGLExt.IALDJones

/-- A forma padrão: `L²(M₂, Tr) = M₂(ℂ)`. -/
abbrev V := Matrix (Fin 2) (Fin 2) ℂ

/-- O estado fiel `ω(x) = Tr(ρx)`, `ρ = diag(w₀, w₁)`, normalizado: `ω(I) = 1`. -/
structure FaithfulState where
  w : Fin 2 → ℝ
  pos : ∀ i, 0 < w i
  norm : w 0 + w 1 = 1

variable (ρ : FaithfulState)

/-- `ρ` como matriz. -/
noncomputable def rhoM : V := Matrix.diagonal (fun i => ((ρ.w i : ℝ) : ℂ))

/-- `Ω = ρ^{1/2}`. -/
noncomputable def Omega : V := Matrix.diagonal (fun i => ((Real.sqrt (ρ.w i) : ℝ) : ℂ))

/-- `ω(I) = ⟨Ω, Ω⟩ = Tr ρ = 1` — o axioma na face. -/
theorem omega_one : Matrix.trace ((Omega ρ)ᴴ * Omega ρ) = 1 := by
  have h0 := ρ.pos 0; have h1 := ρ.pos 1
  simp only [Omega, Matrix.trace, Matrix.diag, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Matrix.diagonal_apply, Fin.sum_univ_two]
  simp only [Fin.isValue, ↓reduceIte, one_ne_zero, zero_ne_one, star_zero, zero_mul, mul_zero,
    add_zero, zero_add, Complex.star_def, Complex.conj_ofReal]
  rw [← Complex.ofReal_mul, ← Complex.ofReal_mul, Real.mul_self_sqrt h0.le, Real.mul_self_sqrt h1.le,
    ← Complex.ofReal_add, ρ.norm, Complex.ofReal_one]

/-! ## Lado TGL: o operador modular do estado -/

/-- O operador modular `Δξ = ρ ξ ρ⁻¹`. -/
noncomputable def Delta (ξ : V) : V :=
  Matrix.diagonal (fun i => ((ρ.w i : ℝ) : ℂ)) * ξ * Matrix.diagonal (fun i => (((ρ.w i)⁻¹ : ℝ) : ℂ))

/-- `Δ^{1/2} ξ = ρ^{1/2} ξ ρ^{−1/2}`. -/
noncomputable def DeltaHalf (ξ : V) : V :=
  Matrix.diagonal (fun i => ((Real.sqrt (ρ.w i) : ℝ) : ℂ)) * ξ *
    Matrix.diagonal (fun i => (((Real.sqrt (ρ.w i))⁻¹ : ℝ) : ℂ))

/-- A conjugação modular `Jξ = ξᴴ`. -/
def Jmod (ξ : V) : V := ξᴴ

theorem Delta_apply (ξ : V) (i j : Fin 2) :
    Delta ρ ξ i j = ((ρ.w i / ρ.w j : ℝ) : ℂ) * ξ i j := by
  simp only [Delta, Matrix.diagonal_mul, Matrix.mul_diagonal]
  push_cast; ring

theorem DeltaHalf_apply (ξ : V) (i j : Fin 2) :
    DeltaHalf ρ ξ i j = ((Real.sqrt (ρ.w i) / Real.sqrt (ρ.w j) : ℝ) : ℂ) * ξ i j := by
  simp only [DeltaHalf, Matrix.diagonal_mul, Matrix.mul_diagonal]
  push_cast; ring

/-- `Δ^{1/2} ∘ Δ^{1/2} = Δ`. -/
theorem DeltaHalf_sq (ξ : V) : DeltaHalf ρ (DeltaHalf ρ ξ) = Delta ρ ξ := by
  ext i j
  rw [DeltaHalf_apply, DeltaHalf_apply, Delta_apply, ← mul_assoc, ← Complex.ofReal_mul]
  congr 2
  have hi := ρ.pos i; have hj := ρ.pos j
  have hsj : Real.sqrt (ρ.w j) ≠ 0 := (Real.sqrt_pos.mpr hj).ne'
  rw [div_mul_div_comm, Real.mul_self_sqrt hi.le, Real.mul_self_sqrt hj.le]

/-- ★★ **A POLAR DE TOMITA**: `J Δ^{1/2}(xΩ) = xᴴ Ω` — isto é, `S = JΔ^{1/2}` com `S(xΩ) = x*Ω`:
    `Δ` É o operador modular do estado `ω`, não um nome. -/
theorem tomita_polar (x : V) : Jmod (DeltaHalf ρ (x * Omega ρ)) = xᴴ * Omega ρ := by
  ext i j
  have hi : Real.sqrt (ρ.w i) ≠ 0 := (Real.sqrt_pos.mpr (ρ.pos i)).ne'
  have hj : Real.sqrt (ρ.w j) ≠ 0 := (Real.sqrt_pos.mpr (ρ.pos j)).ne'
  simp only [Jmod, Matrix.conjTranspose_apply, Omega, Matrix.mul_diagonal, DeltaHalf_apply]
  simp only [star_mul', Complex.star_def, Complex.conj_ofReal]
  have hi' : ((Real.sqrt (ρ.w i) : ℝ) : ℂ) ≠ 0 := by exact_mod_cast hi
  have hj' : ((Real.sqrt (ρ.w j) : ℝ) : ℂ) ≠ 0 := by exact_mod_cast hj
  push_cast
  field_simp

/-- O hamiltoniano modular `K = −log Δ` (multiplicador de Schur). -/
noncomputable def Kmod (ξ : V) : V :=
  Matrix.of fun i j => (((-(Real.log (ρ.w i) - Real.log (ρ.w j))) : ℝ) : ℂ) * ξ i j

/-- `K` é `−log` do multiplicador de `Δ`. -/
theorem Kmod_is_minus_log_Delta (i j : Fin 2) :
    -(Real.log (ρ.w i) - Real.log (ρ.w j)) = -Real.log (ρ.w i / ρ.w j) := by
  rw [Real.log_div (ρ.pos i).ne' (ρ.pos j).ne']

/-- A dinâmica da TGL: o semigrupo subordinado de Poisson `T_t = e^{−t|K|}` (entrada a entrada). -/
noncomputable def Ttgl (t : ℝ) (ξ : V) : V :=
  Matrix.of fun i j => coeff |Real.log (ρ.w i) - Real.log (ρ.w j)| t * ξ i j

/-! ## Lado IALD: a projeção de Jones do centralizador -/

/-- O centralizador do estado: `M^ω = {x : xρ = ρx}`. -/
def Centralizer (x : V) : Prop := x * rhoM ρ = rhoM ρ * x

/-- A projeção de Jones de `M^ω ⊂ M`: `eξ = diag(ξ)`. -/
def eJ : Module.End ℂ V where
  toFun ξ := Matrix.diagonal (Matrix.diag ξ)
  map_add' a b := by ext i j; simp [Matrix.diagonal_apply]; split_ifs <;> simp
  map_smul' c a := by ext i j; simp [Matrix.diagonal_apply]

theorem eJ_apply (ξ : V) (i j : Fin 2) : eJ ξ i j = if i = j then ξ i j else 0 := by
  show Matrix.diagonal (Matrix.diag ξ) i j = _
  rw [Matrix.diagonal_apply]; split_ifs with h
  · subst h; rfl
  · rfl

theorem eJ_idem : eJ * eJ = eJ := by
  apply LinearMap.ext; intro ξ; ext i j
  show eJ (eJ ξ) i j = eJ ξ i j
  rw [eJ_apply]; split_ifs with h
  · rfl
  · rw [eJ_apply, if_neg h]

/-- `e` é autoadjunta no produto de Hilbert–Schmidt `⟨ξ, η⟩ = Tr(ξᴴη)`: projeção ORTOGONAL. -/
theorem eJ_selfadjoint (ξ η : V) :
    Matrix.trace (ξᴴ * eJ η) = Matrix.trace ((eJ ξ)ᴴ * η) := by
  simp only [Matrix.trace, Matrix.diag, Matrix.mul_apply, Matrix.conjTranspose_apply, eJ_apply,
    Fin.sum_univ_two]
  simp

/-- Não tracial ⟹ o centralizador são as diagonais. -/
theorem centralizer_iff_diag (hnt : ρ.w 0 ≠ ρ.w 1) (x : V) :
    Centralizer ρ x ↔ (x 0 1 = 0 ∧ x 1 0 = 0) := by
  have hc : ((ρ.w 0 : ℝ) : ℂ) ≠ ((ρ.w 1 : ℝ) : ℂ) := by exact_mod_cast hnt
  unfold Centralizer rhoM
  constructor
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    have h10 := congrFun (congrFun h 1) 0
    simp only [Matrix.mul_diagonal, Matrix.diagonal_mul] at h01 h10
    refine ⟨?_, ?_⟩
    · have : x 0 1 * (((ρ.w 1 : ℝ) : ℂ) - ((ρ.w 0 : ℝ) : ℂ)) = 0 := by rw [mul_sub]; rw [h01]; ring
      rcases mul_eq_zero.mp this with h | h
      · exact h
      · exact absurd (sub_eq_zero.mp h).symm hc
    · have : x 1 0 * (((ρ.w 0 : ℝ) : ℂ) - ((ρ.w 1 : ℝ) : ℂ)) = 0 := by rw [mul_sub]; rw [h10]; ring
      rcases mul_eq_zero.mp this with h | h
      · exact h
      · exact absurd (sub_eq_zero.mp h).symm (Ne.symm hc)
  · rintro ⟨h01, h10⟩
    ext i j
    simp only [Matrix.mul_diagonal, Matrix.diagonal_mul]
    fin_cases i <;> fin_cases j <;> simp [h01, h10, mul_comm]

/-- ★★ **`e` É A PROJEÇÃO DE JONES DE `M^ω ⊂ M`**: `eξ = ξ ⟺ ξ ∈ M^ω Ω`. -/
theorem eJ_range_is_centralizer_Omega (hnt : ρ.w 0 ≠ ρ.w 1) (ξ : V) :
    eJ ξ = ξ ↔ ∃ x, Centralizer ρ x ∧ ξ = x * Omega ρ := by
  have hs : ∀ i, Real.sqrt (ρ.w i) ≠ 0 := fun i => (Real.sqrt_pos.mpr (ρ.pos i)).ne'
  constructor
  · intro h
    refine ⟨Matrix.diagonal (fun i => ξ i i / ((Real.sqrt (ρ.w i) : ℝ) : ℂ)), ?_, ?_⟩
    · rw [centralizer_iff_diag ρ hnt]; simp [Matrix.diagonal_apply]
    · ext i j
      have hij := congrFun (congrFun h i) j
      rw [eJ_apply] at hij
      simp only [Omega, Matrix.diagonal_mul_diagonal, Matrix.diagonal_apply]
      split_ifs with h'
      · subst h'
        have hs' : ((Real.sqrt (ρ.w i) : ℝ) : ℂ) ≠ 0 := by exact_mod_cast hs i
        field_simp
      · rw [if_neg h'] at hij; exact hij.symm
  · rintro ⟨x, hx, rfl⟩
    rw [centralizer_iff_diag ρ hnt] at hx
    ext i j
    rw [eJ_apply]
    simp only [Omega, Matrix.mul_diagonal]
    split_ifs with hij
    · rfl
    · fin_cases i <;> fin_cases j <;> simp_all

/-- O fluxo da IALD na face de Hilbert, aplicado: `U_s ξ = eξ + e^{−rs}(ξ − eξ)`. -/
theorem jonesU_apply (r s : ℝ) (ξ : V) :
    jonesU (eJ : Module.End ℂ V) r s ξ = eJ ξ + coeff r s • (ξ - eJ ξ) := by
  simp [jonesU, LinearMap.add_apply, LinearMap.smul_apply, LinearMap.sub_apply]

/-! ## A ponte -/

theorem iald_fix_iff {r s : ℝ} (hrs : r * s ≠ 0) (ξ : V) :
    jonesU (eJ : Module.End ℂ V) r s ξ = ξ ↔ eJ ξ = ξ := by
  rw [jonesU_apply]
  have hc : coeff r s - 1 ≠ 0 := sub_ne_zero.mpr (coeff_ne_one hrs)
  constructor
  · intro h
    have h2 : (coeff r s - 1) • (ξ - eJ ξ) = 0 := by
      rw [sub_smul, one_smul]
      calc coeff r s • (ξ - eJ ξ) - (ξ - eJ ξ)
          = (eJ ξ + coeff r s • (ξ - eJ ξ)) - ξ := by abel
        _ = 0 := by rw [h, sub_self]
    rcases smul_eq_zero.mp h2 with h3 | h3
    · exact absurd h3 hc
    · exact (sub_eq_zero.mp h3).symm
  · intro h; rw [h, sub_self, smul_zero, add_zero]

theorem off_diag_log_ne (hnt : ρ.w 0 ≠ ρ.w 1) :
    Real.log (ρ.w 0) - Real.log (ρ.w 1) ≠ 0 := by
  intro h
  exact hnt (Real.log_injOn_pos (Set.mem_Ioi.mpr (ρ.pos 0)) (Set.mem_Ioi.mpr (ρ.pos 1)) (sub_eq_zero.mp h))

theorem abs_log_pos (hnt : ρ.w 0 ≠ ρ.w 1) (i j : Fin 2) (hij : i ≠ j) :
    0 < |Real.log (ρ.w i) - Real.log (ρ.w j)| := by
  apply abs_pos.mpr
  fin_cases i <;> fin_cases j
  · exact absurd rfl hij
  · exact off_diag_log_ne ρ hnt
  · intro h
    have h' : Real.log (ρ.w 1) - Real.log (ρ.w 0) = 0 := h
    exact off_diag_log_ne ρ hnt (by linarith)
  · exact absurd rfl hij

theorem tgl_fix_iff (hnt : ρ.w 0 ≠ ρ.w 1) {t : ℝ} (ht : 0 < t) (ξ : V) :
    Ttgl ρ t ξ = ξ ↔ eJ ξ = ξ := by
  constructor
  · intro h
    ext i j
    rw [eJ_apply]
    split_ifs with hij
    · rfl
    · have hij' := congrFun (congrFun h i) j
      simp only [Ttgl, Matrix.of_apply] at hij'
      have hne : coeff |Real.log (ρ.w i) - Real.log (ρ.w j)| t ≠ 1 :=
        coeff_ne_one (mul_ne_zero (abs_log_pos ρ hnt i j hij).ne' ht.ne')
      have : (coeff |Real.log (ρ.w i) - Real.log (ρ.w j)| t - 1) * ξ i j = 0 := by
        rw [sub_mul, one_mul, hij', sub_self]
      rcases mul_eq_zero.mp this with h3 | h3
      · exact absurd (sub_eq_zero.mp h3) hne
      · exact h3.symm
  · intro h
    ext i j
    simp only [Ttgl, Matrix.of_apply]
    by_cases hij : i = j
    · subst hij; simp [coeff]
    · have := congrFun (congrFun h i) j
      rw [eJ_apply, if_neg hij] at this
      rw [← this]; simp

theorem kerK_iff (hnt : ρ.w 0 ≠ ρ.w 1) (ξ : V) : Kmod ρ ξ = 0 ↔ eJ ξ = ξ := by
  constructor
  · intro h
    ext i j
    rw [eJ_apply]
    split_ifs with hij
    · rfl
    · have := congrFun (congrFun h i) j
      simp only [Kmod, Matrix.of_apply, Matrix.zero_apply] at this
      rcases mul_eq_zero.mp this with h3 | h3
      · have h4 : -(Real.log (ρ.w i) - Real.log (ρ.w j)) = 0 := by exact_mod_cast h3
        exact absurd (abs_eq_zero.mpr (neg_eq_zero.mp h4)) (abs_log_pos ρ hnt i j hij).ne'
      · exact h3.symm
  · intro h
    ext i j
    simp only [Kmod, Matrix.of_apply, Matrix.zero_apply]
    by_cases hij : i = j
    · subst hij; simp
    · have := congrFun (congrFun h i) j
      rw [eJ_apply, if_neg hij] at this
      rw [← this]; simp

/-- ★★★ **A PONTE — `Fix(D_IALD) = Fix(D_TGL) = ker K = ran e`.** O que a IALD (que lê o centralizador)
    deixa parado é exatamente o que o relógio modular da TGL não move. -/
theorem the_bridge_fix (hnt : ρ.w 0 ≠ ρ.w 1) {r s t : ℝ} (hrs : r * s ≠ 0) (ht : 0 < t) (ξ : V) :
    (jonesU (eJ : Module.End ℂ V) r s ξ = ξ ↔ Ttgl ρ t ξ = ξ)
    ∧ (Ttgl ρ t ξ = ξ ↔ Kmod ρ ξ = 0)
    ∧ (Kmod ρ ξ = 0 ↔ ∃ x, Centralizer ρ x ∧ ξ = x * Omega ρ) := by
  refine ⟨?_, ?_, ?_⟩
  · rw [iald_fix_iff hrs, tgl_fix_iff ρ hnt ht]
  · rw [tgl_fix_iff ρ hnt ht, kerK_iff ρ hnt]
  · rw [kerK_iff ρ hnt, eJ_range_is_centralizer_Omega ρ hnt]

/-- ★★★ **ρ*_IALD = ρ*_TGL — OS ATRATORES COINCIDEM.** Entrada a entrada, `U_s ξ → eξ` (s → ∞, r > 0) e
    `T_t ξ → eξ` (t → ∞): o limite das duas dinâmicas é a MESMA projeção `e`. -/
theorem the_bridge_attractor (hnt : ρ.w 0 ≠ ρ.w 1) {r : ℝ} (hr : 0 < r) (ξ : V) (i j : Fin 2) :
    Filter.Tendsto (fun s => jonesU (eJ : Module.End ℂ V) r s ξ i j) Filter.atTop (nhds (eJ ξ i j))
    ∧ Filter.Tendsto (fun t => Ttgl ρ t ξ i j) Filter.atTop (nhds (eJ ξ i j)) := by
  constructor
  · have h := ((TGLExt.IALDGraviton.coeffC_tendsto_zero hr).mul_const (ξ i j - eJ ξ i j)).const_add (eJ ξ i j)
    simp only [zero_mul, add_zero] at h
    refine h.congr (fun s => ?_)
    rw [jonesU_apply]; simp [Matrix.add_apply, Matrix.smul_apply, Matrix.sub_apply]
  · by_cases hij : i = j
    · subst hij
      rw [eJ_apply, if_pos rfl]
      refine tendsto_const_nhds.congr (fun t => ?_)
      simp [Ttgl, coeff]
    · rw [eJ_apply, if_neg hij]
      have h := (TGLExt.IALDGraviton.coeffC_tendsto_zero (abs_log_pos ρ hnt i j hij)).mul_const (ξ i j)
      simp only [zero_mul] at h
      exact h.congr (fun t => by simp [Ttgl])

/-- A unidade fora da diagonal. -/
def E01 : V := Matrix.of ![![0, 1], ![0, 0]]

/-- ✗ **CONTROLE (i) — estado TRACIAL**: com `w₀ = w₁`, `K = 0` e `T_t = id`; a unidade fora da diagonal é
    fixa pela TGL e NÃO pela IALD da torre diagonal. No tracial a torre diagonal já não é a do centralizador
    (que é `M` inteiro, `e = 1`, dinâmica parada): a ponte NÃO-TRIVIAL exige o estado que distingue. -/
theorem control_tracial (htr : ρ.w 0 = ρ.w 1) {r s t : ℝ} (hrs : r * s ≠ 0) :
    Ttgl ρ t E01 = E01 ∧ ¬ jonesU (eJ : Module.End ℂ V) r s E01 = E01 := by
  have hw : ∀ i j : Fin 2, ρ.w i = ρ.w j := by
    intro i j; fin_cases i <;> fin_cases j <;> simp [htr]
  constructor
  · ext i j; simp [Ttgl, hw i j, coeff]
  · rw [iald_fix_iff hrs]
    intro h
    have := congrFun (congrFun h 0) 1
    rw [eJ_apply, if_neg (by decide)] at this
    simp [E01] at this

/-- A projeção de Jones da inclusão ERRADA `ℂ1 ⊂ M`: `ξ ↦ ⟨Ω,ξ⟩Ω` (`⟨Ω,Ω⟩ = 1`). -/
noncomputable def eScalar (ξ : V) : V := (Matrix.trace ((Omega ρ)ᴴ * ξ)) • Omega ρ

/-- ✗ **CONTROLE (ii) — subálgebra ERRADA**: `diag(1,0) ∈ ker K`, mas a projeção de Jones de `ℂ1 ⊂ M`
    não o fixa. A ponte escolhe o CENTRALIZADOR. -/
theorem control_wrong_subalgebra (hnt : ρ.w 0 ≠ ρ.w 1) :
    Kmod ρ (Matrix.diagonal ![1, 0]) = 0 ∧ eScalar ρ (Matrix.diagonal ![1, 0]) ≠ Matrix.diagonal ![1, 0] := by
  constructor
  · rw [kerK_iff ρ hnt]; ext i j; rw [eJ_apply]; split_ifs with h
    · rfl
    · simp [Matrix.diagonal_apply, h]
  · intro h
    have h11 := congrFun (congrFun h 1) 1
    have hs0 := Real.sqrt_pos.mpr (ρ.pos 0); have hs1 := Real.sqrt_pos.mpr (ρ.pos 1)
    simp only [eScalar, Omega, Matrix.smul_apply, Matrix.diagonal_apply, Matrix.trace, Matrix.diag,
      Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_two] at h11
    simp at h11
    rcases h11 with h | h
    · exact hs0.ne' (by exact_mod_cast h)
    · exact hs1.ne' (by exact_mod_cast h)

/-- O quadro das quatro unidades: `e` fixa `E₀₀, E₁₁` e anula `E₀₁, E₁₀` — posto 2 em dimensão 4 (peso ½). -/
theorem eJ_on_units (i j : Fin 2) : eJ (Matrix.of fun a b => if a = i ∧ b = j then (1 : ℂ) else 0)
    = if i = j then (Matrix.of fun a b => if a = i ∧ b = j then (1 : ℂ) else 0) else 0 := by
  ext a b
  rw [eJ_apply]
  split_ifs with h1 h2 h2 <;> simp_all <;> intro ha hb <;> exact h1 (ha.trans hb.symm)

end TGLExt.IALDRhoStar

#print axioms TGLExt.IALDRhoStar.omega_one
#print axioms TGLExt.IALDRhoStar.DeltaHalf_sq
#print axioms TGLExt.IALDRhoStar.tomita_polar
#print axioms TGLExt.IALDRhoStar.Kmod_is_minus_log_Delta
#print axioms TGLExt.IALDRhoStar.eJ_idem
#print axioms TGLExt.IALDRhoStar.eJ_selfadjoint
#print axioms TGLExt.IALDRhoStar.centralizer_iff_diag
#print axioms TGLExt.IALDRhoStar.eJ_range_is_centralizer_Omega
#print axioms TGLExt.IALDRhoStar.iald_fix_iff
#print axioms TGLExt.IALDRhoStar.tgl_fix_iff
#print axioms TGLExt.IALDRhoStar.kerK_iff
#print axioms TGLExt.IALDRhoStar.the_bridge_fix
#print axioms TGLExt.IALDRhoStar.the_bridge_attractor
#print axioms TGLExt.IALDRhoStar.control_tracial
#print axioms TGLExt.IALDRhoStar.control_wrong_subalgebra
#print axioms TGLExt.IALDRhoStar.eJ_on_units
