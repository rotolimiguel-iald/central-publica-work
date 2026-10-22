# Preparação da revisão — conjugação polar de toda a base

BASE_POLAR_STATIC_PREPARATION

[REAL] Apenas dependências anteriores e custódia mãe consultadas. Nenhuma fonte nova em elaboração foi lida, congelada ou recompilada. Nenhum parecer de aceitação do novo lote é emitido; aguardam-se fontes finais e pins rc0.

Pontos preparados para conferir:

1. Restrição de towerExpectation ao fator M: positividade exige A∈M. O mapa real positivo/unital e a decomposição em quatro positivos devem dar uma única cota 4‖A‖ independente do nível. Completeness/C*-instâncias devem ser derivadas do fechamento do duplo centralizador, sem hipótese acrescentada a P.
2. A cota anterior expectation_bounded usa ‖expectationCLM P N‖, dependente de N; sozinha não paga o limite forte. expectation_omega_limit já fornece E_N(A)Ω→AΩ. bounded_omega_tendsto recebe explicitamente pertinência ao mesmo fator, cota uniforme e convergência em Ω; seu enunciado não recebe ExpectationInput.
3. Transferência TowerHilbert→fibre em L²→scalarGNSRepresentation no mesmo H_I: usar as duas pontes existentes de limites fortes uniformemente limitados, preservando os objetos e as coerções. Isso não exige nem demonstra convergência em norma de operadores.
4. Soma finita de unidades matriciais: expandir os mesmos elementos da base e a mesma inclusão; conjugação pelo antiunitário J conjuga os coeficientes complexos. Conferir essa conjugação ao passar da unidade matricial à matriz geral.
5. Passagem ao limite: J é o scalarTomitaPolarFactor efetivo. Para cada a fixo de N, transportar o limite por J/J⁻¹ limitados e a comutação com π(a) por continuidade em vetores. Não usar continuidade conjunta irrestrita de produtos SOT, nem continuidade SOT do adjunto.
6. Alcance pretendido: Jπ(base)J⁻¹⊆π(N)′. Não concluir igualdade global dos comutantes, conjugação do core inteiro, identificação A^it/fluxo, KMS, traço ou promoção de flags.

[REAL — inspeção das fontes anteriores] LevelExpectationFamily e ExpectationInput são contratos diferentes: o primeiro aproxima níveis; o segundo exige imagem no centralizador. A obstrução expectation_not_imported_contract possui hipótese explícita P.w 0≠1/2; não se deve substituir um contrato pelo outro por nome.

A custódia matrix_polar e sua verificação foram lidas; o verificador autoral não foi reexecutado. Os pins das dependências próprias selecionadas foram relidos; lista e eventuais dependências ainda ausentes estão em preparation.json. Nenhuma biblioteca foi recompilada. Pareceres anteriores, fontes autorais, monólito e memórias permanecem intocados.
