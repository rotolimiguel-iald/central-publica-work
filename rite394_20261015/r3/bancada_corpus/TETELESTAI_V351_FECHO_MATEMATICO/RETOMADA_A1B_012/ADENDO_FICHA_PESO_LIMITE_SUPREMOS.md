[OPEN — fornecedores antes do código]

2026-09-14T22:31:48.401781-03:00

A ordem de conjugação refere-se ao input X com conjugador fixo; não compara conjugadores ordenados. A soma de supremos usa MONOTONIA no mesmo índice natural (fornecedor ENNReal), evitando a igualdade falsa para duas famílias arbitrárias não dirigidas conjuntamente. Homogeneidade usa mul_iSup, inclusive nos valores infinitos. Normalidade do limite é troca de supremos do peso construído. Nenhuma lei deste delta implica tracialidade ou semifinitude.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Star\Basic.lean:214

```lean
theorem star_left_conjugate_nonneg {a : R} (ha : 0 ≤ a) (c : R) : 0 ≤ star c * a * c
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Star\Basic.lean:239

```lean
theorem star_left_conjugate_le_conjugate {a b : R} (hab : a ≤ b) (c : R) :
    star c * a * c ≤ star c * b * c
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Field\Basic.lean:69

```lean
theorem one_div_le_one_div_of_le (ha : 0 < a) (h : a ≤ b) : 1 / b ≤ 1 / a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Data\ENNReal\Operations.lean:686

```lean
lemma iSup_add_iSup_of_monotone {ι : Type*} [Preorder ι] [IsDirectedOrder ι] {f g : ι → ℝ≥0∞}
    (hf : Monotone f) (hg : Monotone g) : iSup f + iSup g = ⨆ a, f a + g a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Data\ENNReal\Inv.lean:807

```lean
lemma mul_iSup (a : ℝ≥0∞) (f : ι → ℝ≥0∞) : a * ⨆ i, f i = ⨆ i, a * f i
```

