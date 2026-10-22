# Naturalidade infinitesimal do Ricci em carta curva

[REAL — fonte compilada e auditada no alcance especificado]

A entrega demonstra a identidade de primeira variação
δRic_g[Lie_V g] = Lie_V(Ric_g)
para g matricial simétrico, não degenerado e suave em um aberto U de R⁴, e V suave arbitrário. A função efetivamente derivada é coordinateRicci da família canônica perturbedLeviCivita g (coordinateMetricLie g V) t. O operador de Lie é o coordinateMetricLie já existente no kernel, aplicado ao tensor covariante em seus dois índices.

## Encadeamento

1. LieMetricJets escreve a fórmula canônica em matrizes, calcula seu jet espacial real e demonstra a identidade do jet inferior da Levi-Civita. A simetria do Hessiano do campo vetorial decorre de Schwarz; as simetrias dos jets métricos são transportadas das igualdades locais dos campos.

2. LeviCivitaLieVariation deriva a suavidade da inversa g⁻¹, sua derivada espacial e o jet real da Levi-Civita. A variação resultante coincide com a conexão de Lie: transporte ξ·∂Gamma, transformação do índice da 1-forma, transformação dos índices vetoriais e Hessiano de ξ. A identificação é provada em todo o aberto antes de transportar jets para ricciVariation.

3. RicciLieNaturality separa apenas para o cálculo a parte de transporte/base e a parte D_Gamma(P). Ambas participam da prova. A derivada da curvatura transporta seus dois índices de base e seus índices vetoriais. A contração canônica cancela os termos do índice superior contraído, restando a derivada de Lie de Ricci em seus dois índices covariantes. Essa identidade é finalmente ligada à derivada real da família de Levi-Civita pelo módulo MetricRicciVariation já congelado.

Não há hipótese que forneça δGamma, δRic ou uma igualdade de jets espaciais/temporais como conclusão antecipada. A regularidade é C∞; não se otimizou o número mínimo de derivadas.

## Alcance e próximo passo

O fundo g pode ser curvo e V pode variar arbitrariamente no espaço. O teorema não exige equações de Einstein ou Ricci nulo. A resposta correta em um fundo curvo genérico é Lie_V Ric, que pode ser não nula; não se afirma invariância zero de Ricci em qualquer fundo.

Esta é naturalidade infinitesimal em carta curva. A passagem a pullback por um difeomorfismo finito, integração de fluxo, domínio global do fluxo e compatibilidade entre cartas exige o teorema correspondente, que não está sendo pressuposto ou declarado concluído aqui. A menção à curva x+tξ na dedução prévia motivou o cálculo infinitesimal; não representa uma construção de difeomorfismo global nesta entrega.

A variação de escalar/Einstein está sendo tratada pelo agente raiz em suplemento próprio, evitando duplicação. Assinatura Lorentziana, identificação física dos dados, torção/spin, anomalias interagentes e controle UV não decorrem destas identidades clássicas.

## Revisão e preservação

O agente /root leu integralmente cada um dos três módulos e aprovou os enunciados e a estratégia matemática no alcance acima. Correções de compilação posteriores preservaram os enunciados; trataram inferência de tipos, aplicações da API, simplificação algébrica e auditorias.

Fontes originais, Atlas, memórias e módulos anteriormente congelados permaneceram somente leitura. Nenhum um.py foi executado ou importado. Os arquivos novos residem nesta bancada Chatgpt. Cada edição de fonte própria foi precedida por backup em bytes na mesma pasta, seguida de escrita temporária, verificação e substituição. Falhas intermediárias permanecem preservadas; somente os recibos PASS finais sustentam o estatuto REAL.

Os builds de folha usam dependências locais PASS copiadas e verificadas, mais binários canônicos/Mathlib existentes. A fronteira direta é hasheada antes/depois. Esta rodada não recompilou nem voltou a hashear todas as dependências transitivas.

## Recibos finais medidos

| Módulo | Teoremas | Definições | Auditorias | Build PASS |
|---|---:|---:|---:|---|
| LieMetricJets | 10 | 3 | 13 | BUILD_20260909_142905_572937 |
| LeviCivitaLieVariation | 10 | 1 | 11 | BUILD_20260909_144318_488862 |
| RicciLieNaturality | 10 | 1 | 11 | BUILD_20260909_144746_841562 |

Total exclusivo deste suplemento: 30 teoremas + 5 definições = 35 declarações auditadas. Cada build retornou exit 0 para a folha e para seu agregador de imports; logs contêm somente auditorias no trio propext, Classical.choice e Quot.sound, sem avisos ou erros.

As assinaturas de todas as declarações foram comparadas por script com a primeira versão de cada fonte: inalteradas. As fontes congeladas coincidem byte a byte com suas cópias nos builds PASS.

## Pontos de integração

- [LieMetricJets](<C:/IALD/Central de Patentes/Chatgpt/METRIC_LIE_NATURALITY_20260909_142557_511892/LieMetricJets.lean>): 7880 bytes; SHA-256 `742752d60f65b49d6e24585683f75a50c0ded20367f935d234a790b08d8edab4`.
  `coordinate_metric_lie_jet`: linha 135.
  `lower_lie_jet_identity`: linha 167.
- [LeviCivitaLieVariation](<C:/IALD/Central de Patentes/Chatgpt/METRIC_LIE_NATURALITY_20260909_142557_511892/LeviCivitaLieVariation.lean>): 9932 bytes; SHA-256 `cace954fd0db33d1dfbb1e52e04a444b89f67a311a0606580988176e9d3902ed`.
  `metric_lie_connection_variation`: linha 132.
  `metric_lie_connection_first_derivative`: linha 172.
- [RicciLieNaturality](<C:/IALD/Central de Patentes/Chatgpt/METRIC_LIE_NATURALITY_20260909_142557_511892/RicciLieNaturality.lean>): 9233 bytes; SHA-256 `0c3a834d353b11b9eecbfff05166d7ade471dd69e9b6527f7e7f3dbf81404430`.
  `curvature_connection_lie_variation`: linha 132.
  `ricci_connection_lie_variation`: linha 151.
  `metric_lie_ricci_naturality`: linha 179.

A transposição para o kernel troca somente imports locais por seus nomes TGLExt; os namespaces internos permanecem distintos. LieMetricJets importa MetricRicciVariation e TGLExt.BoostMetricPullback; LeviCivitaLieVariation importa LieMetricJets; RicciLieNaturality importa LeviCivitaLieVariation. O arquivo CACHE_NATURALIDADE_FINAL.json fornece recibos e fontes congelados para futuras compilações isoladas. Nenhuma incorporação no um.py foi feita por este agente.
