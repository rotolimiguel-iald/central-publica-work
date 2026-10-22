# Primeira variação real do escalar e do tensor de Einstein

09/09/2026. [REAL — compilado, com hipóteses explícitas]

`MetricEinsteinVariation.lean` deriva as funções canônicas `coordinateScalarCurvature` e `geometricEinsteinTensor` avaliadas na família métrica g+t h, com a inversa efetiva e a conexão de Levi-Civita calculadas dessa mesma família. Usa a primeira variação do Ricci já demonstrada; a variação de Ricci não é recebida como hipótese nova.

A contração canônica é Σij gInv_ij Ric_ij. Sua derivada contém as duas parcelas: a derivada da inversa, -gInv·h·gInv, contraída com Ricci, e gInv contraída com a derivada de Ricci. A primeira variação de Einstein é então δRicci - (δR/2)g - (R/2)h. Ambas as parcelas da variação da contração foram preservadas.

## Alcance

U é aberto de R⁴; g e h são campos matriciais C∞ em U; g(x) é inversível para x em U. A derivada é local em t=0, sem exigir intervalo uniforme de não degenerescência. O enunciado algébrico admite matrizes não simétricas; sua aplicação à geometria de métricas usa g,h simétricos. O resultado não produz assinatura.

Há três teoremas: derivada do escalar, derivada componente a componente de Einstein e derivada matricial de Einstein. As duas definições explicitam os coeficientes obtidos. A naturalidade para h=Lie_ξg será uma folha complementar, usando a naturalidade do Ricci em desenvolvimento separado.

## Evidência

Recibo aprovado: `BUILD_20260909_144806_517069/BUILD_RESULT.json`. São 3 teoremas, 2 definições, 5 auditorias, duas execuções com código zero, sem avisos/erros e com axiomas restritos ao trio padrão.

As tentativas anteriores permanecem preservadas. Corrigiram-se o escopo sintático da soma dupla, a conversão entre instâncias escalares equivalentes de Mathlib e argumentos de simplificação sem uso. Os recibos com falha ou avisos não foram promovidos a PASS.

Dependências locais PASS foram copiadas e conferidas por bytes; imports diretos/cache foram verificados antes e depois. Não houve reconstrução integral das dependências transitivas. Não foram executados/importados programas um.py ou alterados arquivos canônicos. A fonte aprovada está congelada; novos resultados usam fontes e recibos separados.
