[REAL — correção documental ao lado; sem mudança Lean]

# Correção da referência de comutação CFC

2026-09-14T22:12:12.674131-03:00

O adendo anterior nomeava commute_cfc mas transcrevia commute_cfcHom. Corrigidos localizador e enunciado; os bytes anteriores são preservados como histórico. Nenhuma fonte ou compilação Lean foi alterada.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Commute.lean:87

```lean
protected theorem IsSelfAdjoint.commute_cfc {a b : A}
    (ha : IsSelfAdjoint a) (hb₁ : Commute a b) (f : 𝕜 → 𝕜) :
    Commute (cfc f a) b
```

O segundo fornecedor, Commute.cfcₙ_nnreal, permanece como no adendo anterior. O P2 foi documental; a construção já usava commute_cfc. Esta correção não é uma alegação de ficha anterior ao código: a ficha histórica permanece visível.
