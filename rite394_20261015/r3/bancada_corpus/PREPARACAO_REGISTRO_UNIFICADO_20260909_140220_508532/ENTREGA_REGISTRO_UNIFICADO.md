# Entrega — preparação unificada do registro gravitacional

[REAL — escopo compilado] UnifiedRecordedPreparation.lean está congelado: 11944 bytes, SHA256 071301ea3ec02be1a7b68531f24aec5681b637115688ace6732d62a925b40dc8. Recibo: C:/IALD/Central de Patentes/Chatgpt/PREPARACAO_REGISTRO_UNIFICADO_20260909_140220_508532/BUILD_20260909_140416_241257/BUILD_RESULT.json.

A folha nova contém 16 teoremas e 9 definições/abreviações, com 25 auditorias. Compilação da folha e importador separado terminaram com código zero, sem erros nem avisos. Os termos usam apenas propext, Classical.choice e Quot.sound, ou nenhum deles. Foram reutilizados 16 módulos próprios, copiados byte a byte de builds PASS e conferidos contra fontes/recibos. A fronteira cacheada e as importações diretas medidas permaneceram inalteradas. As dependências locais não foram recompiladas nesta rodada; tampouco todas as dependências transitivas do kernel/Mathlib.

## O objeto construído

[INPUT] R é um GravitationalResponseRecord sobre U. Ele contém probabilidades do codec métrico, dez coeficientes de resposta por ponto e certificados explícitos de regularidade/assinatura. g é decodificado dessas probabilidades, e T é decodificado dos coeficientes e da métrica; o registro não recebe g e T como dois campos independentes escondidos.

[REAL] Para cada ponto x e direção d, unifiedPreparation R x d é uma DiagonalStateCurve com 48 resultados: 32 do bloco métrico e 16 do bloco dinâmico calibrado. O bloco estático recebe metade da massa, o dinâmico recebe metade e evolui em √2t. As duas cardinalidades, de probabilidades e de amplitudes, foram contadas em Lean.

[REAL] unifiedFlow é a família efetiva de operadores I ⊕ U_dyn(√2t), unitária nos dois sentidos. Sua ação sobre unifiedInitialAmplitude produz unifiedAmplitude. O quadrado do módulo dessa amplitude é exatamente a distribuição de unifiedPreparation, após a equivalência que troca apenas os dois índices internos do bloco dinâmico. Operador, amplitude e pesos não são recebidos como certificados independentes: foram ligados por teoremas.

[REAL] A normalização é global em t. Para x∈U, os pesos são não negativos em todo t e estritamente positivos perto de zero; a amplitude é normalizada. O registro métrico só certifica a positividade das suas probabilidades em U, por isso a interpretação física dos pesos é delimitada a esse domínio.

## Leituras demonstradas

[REAL] Multiplicar por 2 os pesos do bloco estático retorna exatamente recordState R.metric.data x. O decoder angular da dependência recupera recordMetric R. Essa leitura vale para qualquer d,t; não recebe a métrica novamente como saída suposta.

[REAL] Os limites quadráticos dos incrementos entrópico e modular da curva de 48 resultados são os da preparação fonte calibrada. A identidade usa a compensação (1/2)·(√2)²=1 já demonstrada na mistura.

[REAL] unified_ten_responses_reconstruct recebe dez números s_i e certificados de que são os limites quadráticos entrópicos desta MESMA preparação nas dez direções probeDirections. Pela unicidade dos limites, s_i coincide com R.responses(x)_i. O decoder de fonte aplicado a esses números retorna recordSource R x. A prova faz a ligação entre limites da curva e decodificação; não se limita a renomear um tensor fornecido.

[INPUT] São dez protocolos direcionais por ponto, sobre um campo R em U. Isso não afirma que um único evento/ângulo, nem a distribuição inicial sozinha, reconstrua toda U. O dado de matéria inclui preparação e resposta. As identidades usam coeficientes e limites exatos.

## Área e Einstein

[REAL] unified_area_matching_iff vale para a MESMA função de área A(t) e o mesmo η nas duas curvas. A diferença dos erros de área é a diferença dos incrementos entrópicos, pois a parcela geométrica cancela. As duas curvas possuem o mesmo coeficiente quadrático, logo essa diferença dividida por t² tende a zero. Portanto, erro de área o(t²) da preparação unificada equivale ao da preparação fonte original. Não se alterou o relógio da função de área para fabricar o matching.

[REAL — suficiência condicional] unified_einstein_from_area produz uma constante Λ e a identidade G(g)+Λg=(2π/η)T para g=recordMetric R e T=recordSource R. Permanecem explícitos:
- U aberto e preconexo;
- R com seus certificados de regularidade e assinatura;
- MetricScreenFamily em U;
- η diferente de zero;
- conservação TOTAL de T pela inversa e Levi-Civita construídas de g;
- condição de área o(t²) desta própria preparação unificada, para todas as direções nulas não nulas em cada ponto.

A equivalência e a transferência foram demonstradas. A realização física da condição de área não foi concluída pelo transporte.

## API congelada

Namespace ChatgptAudit.UnifiedRecorded.

| Declaração | Linha |
|---|---:|
| UnifiedStateIndex | 18 |
| UnifiedAmplitudeIndex | 19 |
| unified_state_cardinality | 21 |
| unified_amplitude_cardinality | 24 |
| unifiedFrequency | 27 |
| unifiedBase | 31 |
| unifiedPreparation | 35 |
| unifiedFlow | 40 |
| unifiedInitialAmplitude | 44 |
| unifiedAmplitude | 48 |
| unified_flow_unitary | 52 |
| unified_flow_prepares | 58 |
| unified_flow_readout | 64 |
| unified_amplitude_normalized | 73 |
| unified_weights_normalized | 80 |
| unified_weights_nonnegative | 85 |
| unified_weights_positive_near | 92 |
| unifiedStaticReadout | 100 |
| unified_static_state_recovered | 104 |
| unified_metric_recovered | 111 |
| unified_entropy_quadratic_limit | 120 |
| unified_modular_quadratic_limit | 129 |
| unified_ten_responses_reconstruct | 138 |
| unified_area_matching_iff | 152 |
| unified_einstein_from_area | 181 |

## Limites preservados

[OPEN] O objeto é uma realização representacional a partir de R fornecido. Não prova que toda seleção física da TGL produza esse campo de probabilidades e respostas, nem uma lei de transformação física do codec entre cartas. Essa correspondência permanece uma obrigação precisa.

[INPUT] A geometria final está em carta quadridimensional e usa Levi-Civita, sem torção. A globalização e a dinâmica de torção não são conclusões deste módulo. A positividade das probabilidades não impõe condições de energia sobre T.

[INPUT] A entropia é a da leitura diagonal rotulada. O projetor do vetor puro global não possui essa entropia como entropia de von Neumann. Probabilidades estritamente positivas não tornam esse projetor fiel/invertível na álgebra matricial inteira, nem fornecem separância de Tomita.

[INPUT] A mistura preserva os incrementos e coeficientes quadráticos. Não preserva a entropia absoluta da base/custo absoluto, e não declara equivalência após marginalizar os rótulos.

[REAL — verificação] A primeira tentativa BUILD_20260909_140226_907694 permanece FAIL_VISIBLE: todos os núcleos de leitura passaram, mas a prova de área precisava explicitar a definição recordPreparation no último simpa. A segunda tentativa aprovada fez somente essa identificação definicional; nenhum enunciado foi enfraquecido. Backup imediato de bytes e ambas as tentativas foram preservados.

[DECLARADO — revisão independente recebida] O root leu a fonte completa e emitiu parecer semântico favorável, conferindo cardinalidade por preparação, operador/readout, recuperação da métrica, unicidade dos dez limites e transferência de área. Destacou corretamente o alcance por ponto e protocolos, bem como as distinções de entropia, custo e correspondência física acima.

[REAL — preservação] Escritas somente nesta nova pasta Chatgpt. Módulos congelados, lote de integração anterior, originais, Atlas e memórias canônicas não foram alterados. Nenhum um.py foi executado/importado.
