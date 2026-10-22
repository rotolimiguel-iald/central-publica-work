[OPEN — fornecedores CFC, antes do código]

2026-09-14T22:02:12.332613-03:00

A comutação do CFC complexo e da raiz NNReal será consumida diretamente. A raiz é o empacotamento hilbertPositiveSqrt antigo; nenhum cálculo funcional novo.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Commute.lean:67

protected theorem IsSelfAdjoint.commute_cfcHom {a b : A} (ha : p a)
    (ha' : IsSelfAdjoint a) (hb : Commute a b) (f : C(spectrum 𝕜 a, 𝕜)) :
    Commute (cfcHom ha f) b

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Commute.lean:200

protected theorem Commute.cfcₙ_nnreal {a b : A} (hb : Commute a b) (f : ℝ≥0 → ℝ≥0) :
    Commute (cfcₙ f a) b