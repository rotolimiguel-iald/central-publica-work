[REAL — esclarecimento de fornecedor após DEV, antes da aceitação]

2026-09-14T21:24:15.159308-03:00

Existing generic Hilbert CFC.sqrt wrapper fixes canonical instances before specialization. Direct CFC.sqrt on the specialized Lp type caused an instance diamond in first DEV. The target uses the EXISTING wrapper, whose definition is literally CFC.sqrt, and an explicit generic real/complex CFC equality. No new square root or root hypothesis. GeneralExpectationCP was only a reuse model on a different algebra.

A ficha anterior cobre o alvo da raiz original e os conversores CFC; este adendo fixa o empacotamento já existente de V350AntiunitaryPositiveConjugation.lean:15. A consulta confirma a rota pelo grafo e é registrada separadamente.
