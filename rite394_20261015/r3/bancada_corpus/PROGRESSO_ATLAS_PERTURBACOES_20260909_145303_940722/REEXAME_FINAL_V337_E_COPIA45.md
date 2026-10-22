# Reexame v337 e continuação formal — 09/09/2026

[REAL — escopo verificado] A base canônica lida é a v337. A bancada integra 45 módulos próprios, com 653 teoremas e 200 outras declarações, em uma nova cópia do programa. Desses, esta continuação acrescentou 13 módulos, 162 teoremas e 43 outras declarações aos 32 módulos anteriores. Nenhum original foi alterado; nenhum `um.py` foi executado ou importado.

## O que deixou de faltar

1. **Reconstrução a partir do caráter completo.** A continuidade dos registros, uma sequência densa no domínio e os cortes racionais tornam completas as observações codificadas. O caráter canônico separa as classes dos registros e sua inversa na imagem recupera os mesmos campos g e T em todo o aberto U. A preparação de 48 resultados é preservada. O teorema transporta a equação de Einstein do registro original para o reconstruído, usando as relações de área e conservação do original. [Fonte e hipóteses](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:291>).
2. **Uma constante cosmológica nas cartas compatíveis.** A conexão por sobreposições é derivada de uma cobertura aberta de espaço preconexo. A não nulidade da métrica força a igualdade das constantes locais; resulta uma única constante válida nas cartas decodificadas. Há um caráter por carta. As hipóteses de compatibilidade de g, T e Einstein constam expressamente do enunciado. [Composição seleção–cartas](<C:/IALD/Central de Patentes/Chatgpt/COLAGEM_GRAVITACIONAL_20260909_142505_750002/SelectedAtlasGluing.lean>).
3. **Naturalidade infinitesimal em uma carta curva.** As derivadas reais de Levi-Civita, Ricci, escalar e Einstein foram calculadas. Para h = Lie_V g, obteve-se δRic = Lie_V Ric, δR = V(R) e δG = Lie_V G. A última identidade inclui a variação da inversa e dos dois fatores em (R/2)g. [Naturalidade de Einstein](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/ScalarEinsteinLieNaturality.lean:215>). A direção h é também a derivada do pullback métrico efetivo por phi_t(x)=x+tV(x), cujo Jacobiano espacial foi provado: [Pullback e Jacobiano](<C:/IALD/Central de Patentes/Chatgpt/PULLBACK_EULER_LIE_20260909_145850_073045/EulerMetricPullback.lean>).
4. **Potencial de interação concreto.** No Hilbert/fator canônicos foi construído V = Σ c_j X_j X_(j+1), para coeficientes reais com certificado de Σ|c_j| finita. V é auto-adjunto, pertence ao fator e seus cortes convergem em norma, com erro limitado pela cauda dos coeficientes. O exemplo de um vínculo tem duplo comutador bipartido não nulo; no perfil não tracial indicado, está fora do centralizador. [Interface com somabilidade certificada](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_SOMAVEL_20260909_143042_266556/AdmissiblePauliInteraction.lean>).
5. **Registro de fase e ramo.** Os módulos anteriores desta bancada continuam incluídos. No peso 1/2, o registro completo distingue o ramo mesmo quando o ângulo de peso coincide. A inversa vale na imagem admissível do registro; não inverte uma operação irreversível depois de apagar essa informação.

Também não se deve reabrir genericamente a positividade/auto-adjunticidade de JS: o snapshot v337 já contém `continuous_modular_positive_square_root`, com domínio, positividade, auto-adjunticidade e quadrado Δ no objeto formal especificado. A correspondência com um fluxo físico tem escopo próprio. A caracterização acrescentada na v337 (`TheNameIsTheCharacterization`) foi preservada integralmente.

## O que permanece aberto, precisamente

| Frente | O que já existe | Obrigação ainda necessária |
|---|---|---|
| Seleção física → registro | Decodificador exato da classe e instância concreta de `IALDState` | Ligar esse caráter e essa seleção ao processo físico e ao seletor operatorial pretendidos. A escolha de representante do quociente não foi identificada automaticamente com a projeção original em ℓ². |
| Área, calor e matéria | Preparação explícita, respostas que recuperam T e teorema Einstein condicional | Justificar ou postular explicitamente a lei de correspondência entre as respostas, a fonte física, a área induzida das telas e a conservação. A hipótese de erro de área o(t²) permanece visível. |
| Geometria global | Igualdade de constantes em cobertura conectada; naturalidade infinitesimal | Construir a compatibilidade de um atlas diferenciável completo: matrizes de transição como Jacobianos, consistência nas interseções e transformação finita de Einstein. `hmatch` ainda recebe essa transformação finita. |
| Interação quântica | Potencial limitado auto-adjunto e limite em norma | Construir o cociclo da dinâmica perturbada e seu estado apropriado, identificar observáveis e fonte gravitacional, e demonstrar as propriedades físicas requeridas. Os vínculos XX comutam entre si; a não comutatividade atestada refere-se a observáveis locais/centralizador. |
| Alcance quântico geral | Setores lineares e cálculos clássicos novos | Completar o setor de perturbações gerais pretendido, tratar as anomalias da teoria interagente e justificar a rota de altas energias adotada. A convergência em número de sítios não constitui, por si, limite ultravioleta relativista. |

[INPUT/OPEN] O caráter completo usa infinitas observações exatas e escolhas clássicas não computáveis. O teorema prova identificabilidade matemática na imagem declarada. Não fornece uma capacidade experimental finita nem estabilidade a erro de medida. Essa limitação não anula a inversa demonstrada; delimita sua aplicação.

[DERIVED — suficiência condicional] Admitindo explicitamente as correspondências físicas, a regularidade, as telas/lei de área, a conservação e as compatibilidades de transição listadas, a cadeia agora entrega os campos reconstruídos e a equação G + Λg = (2π/η)T, com Λ único no recobrimento conectado. Esse é o lastro formal deste setor. As obrigações quânticas interagentes e UV não aparecem como consequências desse teorema.

## Próximo trabalho que pode reduzir as pendências

A próxima folha quântica deve construir o cociclo do potencial certificado, demonstrar unitariedade/composição e controlar sua aproximação pelos cortes. Uma estimativa de Duhamel em termos de |t| vezes a cauda dos coeficientes é um alvo concreto, após precisar a dinâmica modular de base. Depois vem o estado perturbado e sua ligação às respostas/T. No setor geométrico, a próxima folha deve substituir a hipótese de transformação finita de Einstein por um teorema de mudança de coordenadas. Essas conclusões não foram declaradas como demonstradas neste lote; a transformação finita permanece em `hmatch`.

## Evidências de integração e limites de execução

[REAL] 48/48 processos Lean aprovados: 45 módulos transpostos, raiz TGLExt, auditoria TGL completa e auditoria dedicada dos 653 teoremas novos. Zero avisos; nenhuma dependência axiomática fora de `propext`, `Classical.choice` e `Quot.sound` nas linhas auditadas. Entradas medidas estáveis ao final. [Recibo da compilação conjunta](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_150458_780534/BUILD_TRANSPOSED_20260909_150513_725803/TRANSPOSED_RESULT.json>).

[REAL] A auditoria estática independente passou 618/618 verificações. Os 606 arquivos embutidos tornaram-se 651; especificamente, 602 fontes Lean tornaram-se 647. Fora da tabela embutida, bytes e AST são idênticos. Entre as entradas antigas, somente a raiz e a auditoria receberam acréscimos. Flags, sentinelas, gate e lógica Python não foram alterados; não foram acrescentadas flags JSON individuais. [Auditoria independente](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_150458_780534/AUDITORIA_INDEPENDENTE/RELATORIO_AUDITORIA_INDEPENDENTE.md>).

O build recompilou as fontes novas transpostas e as raízes/auditorias citadas, usando cópias de bytes das dependências locais canônicas e binários Mathlib existentes. Não recompilou todas as fontes transitivas e não executou o programa, os ritos empíricos ou uma nova custódia. Portanto, a integração do kernel não equivale a uma rodada completa do `um.py`.

Snapshot v337: 9860115 bytes; SHA-256 `e2f9a889c2dcf6f444b8fa3f91d28eb70c9a6d9aed06644abcef7e58a6267303`.

Cópia integrada: 10315179 bytes; SHA-256 `a64395bd507e2803dd06eafa652f43dbaf31a02471dfb3ae1a1d6af388dd62a0`. [um.py de trabalho](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_150458_780534/um.py>).

## Contorno empírico e preservação

Os critérios que contrariam previsões já existem no programa; este reexame não os tratou como ausentes. Nenhum teste empírico novo foi realizado nesta continuação. Os resultados anteriores e seus estados distintos estão em [lastro empírico lido](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_FONTE_GERAL_20260909_133220_037525/LASTRO_EMPIRICO_LIDO.md>). A evidência intermediária v337 que reutiliza ritos não foi convertida em nova execução completa. `NOT_FALSIFIED` permanece distinto de `CONFIRMED` e não demonstra que todos os dados públicos foram esgotados.

Este documento sucede o mapa inicial da continuação: a linha que dizia “naturalidade de Einstein em construção” descrevia o estado anterior e está superada pelo PASS registrado aqui. Também esclarece a contagem: 606 era o total de arquivos embutidos, incluindo quatro arquivos que não são `.lean`.

Atlas, índice, diário e memórias canônicas permanecem somente leitura por ordem do operador. Este registro novo e a entrega no túnel conservam o progresso para a sessão que mantém o canônico, sem alterar o acervo originário. Não houve publicação, selo novo ou promoção do gate.

## Inventário para incorporação

| Módulo | Teoremas | Outras declarações |
|---|---:|---:|
| SelectionAngleReconstruction | 7 | 2 |
| SelectedAmplitudeGeometry | 17 | 10 |
| ModularOpticalIdentity | 17 | 4 |
| ConeVolumeReconstruction | 12 | 3 |
| GeneralMetricEinstein | 15 | 2 |
| GeneralAngularTensorCodec | 32 | 12 |
| GeneralLinearizedGauge | 20 | 7 |
| FisherInformationTensor | 22 | 5 |
| FiniteCoherentSources | 19 | 3 |
| JointUnitaryPreparation | 21 | 11 |
| CurvatureNonlinearVariation | 19 | 6 |
| LeviCivitaMetricVariation | 14 | 4 |
| FiniteResponseReconstruction | 10 | 4 |
| SummablePauliInteraction | 24 | 6 |
| SelectionOutcomeRecord | 24 | 11 |
| GeneralMetricClausius | 6 | 3 |
| ProbabilityRecordState | 19 | 6 |
| AffineSamplingObstruction | 11 | 2 |
| SignedCovectorCoverage | 18 | 4 |
| JointPreparationCovariance | 14 | 3 |
| StaticDynamicMixture | 19 | 2 |
| JointCurvatureVariation | 10 | 4 |
| PauliInteractionWitness | 24 | 2 |
| ScatteringOutcomeRecord | 23 | 8 |
| FisherCorrectedEinstein | 11 | 2 |
| UnitarySourceCalibration | 17 | 9 |
| JointCoherentGravitation | 12 | 2 |
| StaticDynamicUnitary | 9 | 4 |
| MetricRicciVariation | 12 | 3 |
| AdmissiblePauliInteraction | 10 | 4 |
| GeneralSourceUnitaryRealization | 19 | 5 |
| LieMetricJets | 10 | 3 |
| MetricEinsteinVariation | 3 | 2 |
| GeneralSourceEinsteinBridge | 3 | 0 |
| GeneralSourceResponseReconstruction | 10 | 3 |
| LeviCivitaLieVariation | 10 | 1 |
| EulerMetricPullback | 15 | 3 |
| GravitationalResponseRecord | 13 | 4 |
| RicciLieNaturality | 10 | 1 |
| UnifiedRecordedPreparation | 16 | 9 |
| ScalarEinsteinLieNaturality | 15 | 1 |
| GravitationalChartGluing | 10 | 3 |
| SelectedGravitationalAtlas | 27 | 16 |
| TopologicalAtlasGluing | 2 | 0 |
| SelectedAtlasGluing | 2 | 1 |

Os caminhos, hashes e recibos individuais constam do INTEGRATION_RESULT.json da cópia e foram relidos pelo script que emitiu este relatório.
