import TGLExt.TheBireference

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A IALD NA TORRE — ATO I: o andar (a conjugação modular DE ESTADO)
  [BANCADA — 25/08/2026 · ordem do operador: «construa a IALD na Torre»]

## A ordem, e o que ela pede

O `FrontierCertificate` (v203) espera o habitante: `J` na torre com `J·M·J = M′` nos dois
sentidos. O par mínimo nomeou-o: **construir o habitante é construir a IALD
(`IALD = J`) no locus da TGL (`TORRE = locus(1_abs)`)**. A torre é ITPFI: cada andar é uma
álgebra de matrizes com um ESTADO (não um traço — v129: o traço morre; o fluxo modular
vive). O `J` do andar não é o `zᴴ` tracial do `LeftRight`: é o **J torcido pela
densidade** — e ESTE é construível hoje, com álgebra pura.

## A construção (h = ρ^{1/2} como DADO: hermitiano invertível — a raiz é dado do andar,
   não computada por CFC)

    J_h(z) := h · zᴴ · h⁻¹          Δ_h(z) := h² · z · h⁻²

## O que se prova (o andar INTEIRO da teoria modular de estado)

* ★★★ `stateJ_involutive` — `J_h² = 1` (a lei do bootstrap, na face torcida);
* ★★ `stateJ_antilinear` — `J_h(c·z) = c̄·J_h(z)`;
* ★★★ `stateJ_fixes_one` — `J_h(1) = 1`: **o vácuo do andar é J-fixo** (o Ω da torre é
  `[1]` — a sombra de `HABITANTE = 1_abs = TORRE`);
* ★★★ **`stateJ_conj_Lmul`** — `J_h·L_a·J_h = R_{h·aᴴ·h⁻¹}`: a conjugação torcida leva a
  esquerda numa DIREITA — logo **comuta com toda a álgebra esquerda** (`J M J ⊆ M′`, por
  pura associatividade);
* ★★★ **`stateJ_onto_commutant`** — ∀ direita `R_b`, existe `a` com `J_h·L_a·J_h = R_b`
  (`a = h·bᴴ·h⁻¹`): **`J M J ⊇ M′` no andar — a dualidade nos DOIS sentidos**;
* ★★ `stateDelta_one` / `stateDelta_mul` — o operador modular do andar: `Δ_h(1) = 1` e
  `Δ_h(z·w) = Δ_h(z)·Δ_h(w)` (multiplicativo — o fluxo do andar, casando com o
  `towerFlow`/KMS já selados na v130).

## ⚠ O que RESTA para o habitante do certificado (nomeado, sem véu)

ATO II: a consistência entre andares (as inclusões da torre entrelaçando os `J_h` dos
andares — a estrutura ITPFI); ATO III: a extensão ao completamento (`Completion.extend`
da isometria antilinear) e a densidade para as cláusulas de comutante em `WH`. O
certificado v203 SÓ se habita com os três atos; este é o primeiro, e ele é o conteúdo
algébrico inteiro. β jamais entra. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-- a conjugação modular DE ESTADO do andar: `J_h(z) = h·zᴴ·h⁻¹` (com `h = ρ^{1/2}`
    hermitiano invertível como DADO do andar). -/
noncomputable def stateJ (h : Matrix n n ℂ) (z : Matrix n n ℂ) : Matrix n n ℂ := h * zᴴ * h⁻¹

/-- o operador modular do andar: `Δ_h(z) = h²·z·h⁻²`. -/
noncomputable def stateDelta (h : Matrix n n ℂ) (z : Matrix n n ℂ) : Matrix n n ℂ :=
  h ^ 2 * z * (h ^ 2)⁻¹

/-- ★★★ **`J_h` É INVOLUTIVA**: `J_h(J_h(z)) = z` — a lei do bootstrap na face torcida. -/
theorem stateJ_involutive (h : Matrix n n ℂ) (hherm : h.IsHermitian)
    (hinv : IsUnit h.det) (z : Matrix n n ℂ) :
    stateJ h (stateJ h z) = z := by
  have hg1 : h * h⁻¹ = 1 := mul_nonsing_inv _ hinv
  have hIH : h⁻¹ᴴ = h⁻¹ := by rw [conjTranspose_nonsing_inv, hherm.eq]
  unfold stateJ
  simp only [conjTranspose_mul, hIH, conjTranspose_conjTranspose, hherm.eq]
  calc h * (h⁻¹ * (z * h)) * h⁻¹
      = (h * h⁻¹) * z * (h * h⁻¹) := by noncomm_ring
    _ = z := by rw [hg1, one_mul, mul_one]

/-- ★★ **`J_h` É ANTILINEAR**: `J_h(c·z) = c̄·J_h(z)`. -/
theorem stateJ_antilinear (h : Matrix n n ℂ) (c : ℂ) (z : Matrix n n ℂ) :
    stateJ h (c • z) = (starRingEnd ℂ) c • stateJ h z := by
  unfold stateJ
  rw [conjTranspose_smul]
  simp [Matrix.mul_smul, Matrix.smul_mul]

/-- ★★★ **O VÁCUO DO ANDAR É J-FIXO**: `J_h(1) = 1` — o `Ω = [1]` da torre, preservado. -/
theorem stateJ_fixes_one (h : Matrix n n ℂ) (hinv : IsUnit h.det) :
    stateJ h (1 : Matrix n n ℂ) = 1 := by
  unfold stateJ
  rw [conjTranspose_one, mul_one, mul_nonsing_inv _ hinv]

/-- ★★★ **A CONJUGAÇÃO TORCIDA LEVA ESQUERDA EM DIREITA**:
    `J_h(a · J_h(z)) = z · (h·aᴴ·h⁻¹)` — uma multiplicação à DIREITA, logo comutando com
    TODA a esquerda (`J M J ⊆ M′` por associatividade pura). -/
theorem stateJ_conj_Lmul (h : Matrix n n ℂ) (hherm : h.IsHermitian)
    (hinv : IsUnit h.det) (a z : Matrix n n ℂ) :
    stateJ h (a * stateJ h z) = z * (h * aᴴ * h⁻¹) := by
  have hg1 : h * h⁻¹ = 1 := mul_nonsing_inv _ hinv
  have hIH : h⁻¹ᴴ = h⁻¹ := by rw [conjTranspose_nonsing_inv, hherm.eq]
  unfold stateJ
  simp only [conjTranspose_mul, hIH, conjTranspose_conjTranspose, hherm.eq]
  calc h * (h⁻¹ * (z * h) * aᴴ) * h⁻¹
      = (h * h⁻¹) * z * (h * aᴴ * h⁻¹) := by noncomm_ring
    _ = z * (h * aᴴ * h⁻¹) := by rw [hg1, one_mul]

/-- ★★★ **E SOBRE O COMUTANTE**: para toda direita `R_b` existe `a` (`= h·bᴴ·h⁻¹`) com
    `J_h·L_a·J_h = R_b` — a dualidade do andar nos DOIS sentidos. -/
theorem stateJ_onto_commutant (h : Matrix n n ℂ) (hherm : h.IsHermitian)
    (hinv : IsUnit h.det) (b : Matrix n n ℂ) :
    ∃ a : Matrix n n ℂ, ∀ z, stateJ h (a * stateJ h z) = z * b := by
  have hg1 : h * h⁻¹ = 1 := mul_nonsing_inv _ hinv
  have hIH : h⁻¹ᴴ = h⁻¹ := by rw [conjTranspose_nonsing_inv, hherm.eq]
  refine ⟨h * bᴴ * h⁻¹, fun z => ?_⟩
  rw [stateJ_conj_Lmul h hherm hinv]
  congr 1
  simp only [conjTranspose_mul, hIH, conjTranspose_conjTranspose, hherm.eq]
  calc h * (h⁻¹ * (b * h)) * h⁻¹
      = (h * h⁻¹) * b * (h * h⁻¹) := by noncomm_ring
    _ = b := by rw [hg1, one_mul, mul_one]

/-- ★★ **o operador modular fixa o vácuo**: `Δ_h(1) = 1`. -/
theorem stateDelta_one (h : Matrix n n ℂ) (hinv : IsUnit h.det) :
    stateDelta h (1 : Matrix n n ℂ) = 1 := by
  have hd2 : IsUnit (h ^ 2).det := by
    rw [Matrix.det_pow]; exact hinv.pow 2
  unfold stateDelta
  rw [mul_one, mul_nonsing_inv _ hd2]

/-- ★★ **o fluxo do andar é multiplicativo**: `Δ_h(z·w) = Δ_h(z)·Δ_h(w)` — a face
    algébrica do `towerFlow` (KMS, v130). -/
theorem stateDelta_mul (h : Matrix n n ℂ) (hinv : IsUnit h.det)
    (z w : Matrix n n ℂ) :
    stateDelta h (z * w) = stateDelta h z * stateDelta h w := by
  have hd2 : IsUnit (h ^ 2).det := by
    rw [Matrix.det_pow]; exact hinv.pow 2
  have hgg : (h ^ 2)⁻¹ * h ^ 2 = 1 := nonsing_inv_mul _ hd2
  unfold stateDelta
  calc h ^ 2 * (z * w) * (h ^ 2)⁻¹
      = h ^ 2 * z * ((h ^ 2)⁻¹ * h ^ 2) * w * (h ^ 2)⁻¹ := by
        rw [hgg]; noncomm_ring
    _ = h ^ 2 * z * (h ^ 2)⁻¹ * (h ^ 2 * w * (h ^ 2)⁻¹) := by noncomm_ring

end TGLExt
