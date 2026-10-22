# Registro gravitacional conjunto
[REAL — composição e compilação; INPUT — certificados e leis gravitacionais explícitos]

O tipo GravitationalResponseRecord contém um LorentzProbabilityRecord e dez coeficientes reais de resposta suaves em U. Não guarda campos g e T independentes. recordMetric decodifica a métrica a partir das probabilidades; recordSource decodifica os dez coeficientes usando a inversa dessa mesma métrica; recordPreparation é a família unitária calibrada para esses campos.

## Encadeamento verificado

A suavidade da métrica é herdada do codec de probabilidades. A assinatura Lorentziana é o certificado R.metric.lorentz; ele não é derivado de normalização probabilística. Esse certificado permite construir a inversa e certificar a simetria da métrica em U.

A suavidade dos dez coeficientes passa pelas diferenças e divisões constantes do decoder. A reversão de traço então produz uma fonte suave e simétrica. Não se acrescenta uma hipótese de conservação por setor; a conservação total é uma hipótese separada no teorema de Einstein.

O estado rotulado do registro métrico recupera exatamente recordMetric. A preparação construída é normalizada e tem pesos não negativos, e seu limite entrópico quadrático nas direções nulas é −πT(d,d).

O novo teorema record_declared_responses_recovered completa a ida e volta: amostrar as dez respostas da preparação da fonte decodificada devolve exatamente R.responses x para x em U. Ele aplica source_response_samples_roundtrip com a métrica e a inversa do próprio registro. A recuperação da fonte a partir dessas respostas também está provada. Assim, não se troca a coleção de coeficientes durante a composição.

record_einstein_from_area conclui a equação geométrica de Einstein com uma constante cosmológica em U preconexo, recebendo explicitamente: U aberto/preconexo; eta não nulo; MetricScreenFamily da métrica decodificada; conservação total da fonte decodificada; e matching de área da MESMA preparação para todas as direções nulas não zero. A conclusão permanece condicional a essas leis e certificados.

## Limites e revisão

O registro tem dois blocos: probabilidades métricas e coeficientes de resposta. Uma única distribuição que reúna esses blocos é uma composição separada. Não se afirma aqui seleção física dos dados, acesso experimental a coeficientes exatos, origem física da codificação, ou fechamento de anomalias quânticas/UV. A folha não calcula custo de mistura, não identifica entropia absoluta com a Meia-Nat e não altera gate.

A revisão independente da fonte inicial do root foi semanticamente favorável. A fonte inteira passou sem correções em seus enunciados, APIs ou provas. A única adição é o teorema de retorno das respostas declaradas e sua auditoria; a comparação em bytes contra o backup comprova que o restante é idêntico.

## Custódia

Nenhum original canônico foi modificado, executado ou importado. A cópia do root foi preservada em backup imediato de bytes antes da adição; escrita por temporário verificado. O builder de folha foi copiado em bytes do builder já utilizado na resposta completa.

A folha e seu agregador foram recompilados contra treze módulos locais de builds PASS. Seus recibos, fontes e artefatos foram conferidos e copiados para um overlay novo, com fronteira medida antes/depois. As dependências canônicas e Mathlib usam binários preexistentes; esta rodada não recompila nem mede toda a árvore transitiva.

## Medição final

[REAL] 13 teoremas + 4 outros termos = 17 auditorias; dois exits 0, nenhum warning; axiomas restritos ao trio. Build BUILD_20260909_134305_403347/BUILD_RESULT.json. Fonte 8612 bytes, SHA-256 14745684ba6a267cc5d9ca9118c51a48b5b387cb7d30b5f3a45d7d6d687eedc1.

Declarações e linhas medidas:

- GravitationalResponseRecord: 19
- recordMetric: 24
- recordSource: 27
- recordPreparation: 30
- record_metric_smooth: 34
- record_metric_lorentz: 38
- record_metric_symmetric: 42
- response_tensor_smooth: 46
- record_source_smooth: 70
- record_source_symmetric: 79
- record_metric_recovered_from_labelled_state: 85
- record_source_recovered_from_preparation: 90
- record_preparation_normalized: 98
- record_preparation_nonnegative: 103
- record_preparation_entropy_null: 108
- record_declared_responses_recovered: 119
- record_einstein_from_area: 132
