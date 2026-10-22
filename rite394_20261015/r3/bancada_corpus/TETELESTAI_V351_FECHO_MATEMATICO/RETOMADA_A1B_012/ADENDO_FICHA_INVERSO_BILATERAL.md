[OPEN — complemento da ficha antes da equivalência bilateral]

2026-09-14T20:12:34.780350-03:00

(x,y) in graph h iff B_epsilon(y+epsilon x)=x. The converse and uniqueness use positivity of the same h. No new definition.

Fornecedor: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:138; sha256 d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390

```lean
theorem regularPositiveGenerator_positive (P : SiteProfile)
    (x : (regularPositiveGenerator P).domain) :
    0 ≤ (inner ℂ (x : RegularHilbert (TowerHilbert P)) (regularPositiveGenerator P x)).re
```

O alvo inicial já tinha a identificação como inverso. A equivalência explicita a unicidade pela positividade, em vez de deixar essa inferência somente na frase. O antecedente escalar continuous_resolvent_unique vive em outro espaço; não é aplicado por homonímia. Mesmas buscas da ficha original, cujo padrão inclui o nome-base do corte; nenhum novo objeto.
