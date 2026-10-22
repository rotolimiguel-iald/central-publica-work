# Derivação048 — localização fiel e retorno geométrico

07/09/2026. [DERIVED — antes do código e da compilação]
Arquivo novo em Chatgpt. Originais, memória, Atlas e etapas seladas permanecem somente leitura.

A hipótese a testar é uma identificação global entre a ação modular da torre e uma ação geométrica sobre uma família de regiões distinguíveis. Não se constrói uma rede física nesta etapa e não se preenche H3.

## Argumento geral

Se localize : R → X é injetiva, a covariância localize(Phi_s(r)) = sigma_s(localize(r)) e o retorno sigma_T = id implicam Phi_T(r) = r. Trata-se de cancelamento por uma localização fiel, sem supor a conclusão na definição de um recorde.

Para a torre, X pode ser o conjunto das partes de B(H). A ação observável é a imagem de conjuntos por modularConjugation P s. De modularFlow P T = id e do inverso do fluxo decorre modularConjugation P T = id em todos os operadores. Logo sua imagem deixa qualquer conjunto invariante no instante T.

A versão mínima só precisa que dois rótulos sejam separados: se A(exp(-rate*T)) ≠ A(1), não pode valer
sigma_s '' A(r) = A(exp(-rate*s)*r)
para todos s e r. A versão com A injetiva, rate ≠ 0 e T > 0 deduz essa separação, pois exp(-rate*T) ≠ 1.

## Ligação à geometria já existente

O fluxo044 efetivo satisfaz
boostFlow rate s (centralNullCurve r) =
centralNullCurve (exp(-rate*s)*r).
A curva é injetiva, porque opticalPhaseCoordinate(centralNullCurve r)=r.
Assim o boost não retorna em um ponto central r ≠ 0 quando rate*T ≠ 0.

Para uma família N : Coordinate4 → Set B(H), basta que r ↦ N(centralNullCurve r) seja injetiva. Sua covariância global sob boostFlow e modularConjugation produziria a covariância por dilatação acima e, num perfil modular periódico, a contradição. Não se exige injetividade de N em toda a carta.

A referência thirdThermalReference tem peso constante 1/3. Escolhe-se o período efetivamente já provado:
T3 = 2*pi / |log(1/3)-log(1-1/3)|.
O denominador é não zero por stationary_log_gap_ne_zero, T3 é positivo e lattice_modular_period fornece modularFlow T3 = id. Não é necessário inventar um período nem atribuir periodicidade ao perfil aperiódico.

## Controles e limites

Uma localização constante, por exemplo a que associa o fator inteiro a todo rótulo, é modularmente covariante e não é fiel. Esse controle explicita que o negativo não proíbe toda covariância nem torna o contrato inabitável.

Um wedge isolado preservado pelo boost não distingue os rótulos utilizados e não cai na hipótese de separação. A obstrução é global no tempo e nas regiões da família; não refuta automaticamente covariância de germes, um boost aproximado, ou o balanço infinitesimal H3. Covariância apenas em uma vizinhança de zero também precisa ser analisada quanto aos domínios e à composição: se as ações e a covariância uniforme puderem ser iteradas mantendo a família, o retorno no período pode ser recuperado; não se declara uma fuga apenas por restringir a linguagem ao tempo local. Perfis sem período modular não são excluídos pelo argumento. A ação044 é um fluxo geométrico explícito; seu defeito de Killing na métrica pp-wave e a ausência de uma identificação modular física continuam como antes.

## Fontes e caminho Lean

- StationaryModularPeriod.lean: stationary_log_gap_ne_zero, stationary_site_log_lattice, lattice_modular_period.
- ModularFlowHilbert.lean: modularFlow_inverse.
- ModularFlowAlgebra.lean: modularConjugation, modularConjugation_preserves_factor.
- ThermalLimitControls.lean: thirdThermalReference.
- ApproximateBoostFlow.lean (044): boost_flow_central.
- JacobiRiccatiProfile.lean (043): optical_phase_coordinate_central.

O novo módulo FaithfulGeometricLocalization será somente uma cadeia de teoremas com hipóteses explícitas, sem instâncias novas ou recordes de existência. Cada declaração terá #print axioms. O resultado só receberá estatuto REAL após compilação e auditoria. H3 e reconstrução física geral permanecem OPEN.
