[OPEN — fornecedores antes do código]

2026-09-14T22:23:56.003280-03:00

Usar CFC somente para comutação de funções do mesmo R. A ordem vem da identidade resolvente e da positividade do PRODUTO de cortes que comutam; não da ordem de sanduíches. A comparação de sanduíches sob o peso usa o teorema all_positive já compilado com suas hipóteses explícitas. Aplicar o fornecedor genérico Commute.mul_nonneg em Hilbert antes da especialização fixa as instâncias. A raiz original satisfaz sqrt(B)*sqrt(B)=B e é autoadjunta por positividade.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unital.lean:377

```lean
lemma cfc_commute_cfc (f g : R → R) (a : A) : Commute (cfc f a) (cfc g a)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Instances.lean:292

```lean
lemma Commute.mul_nonneg {a b : A} (ha : 0 ≤ a) (hb : 0 ≤ b) (h : Commute a b) :
    0 ≤ a * b
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:265

```lean
lemma sqrt_mul_sqrt_self (a : A) (ha : 0 ≤ a := by cfc_tac) : sqrt a * sqrt a = a
```

