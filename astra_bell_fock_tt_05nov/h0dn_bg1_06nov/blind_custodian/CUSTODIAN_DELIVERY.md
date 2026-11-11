# Custódia cega e revisão estatística H0DN × BG1

[REAL — simulação condicional, 06/11/2026] A geração ocorreu uma única vez, depois de `FREEZE_R2.json`, com 64 blocos avaliados pelo estimador congelado em subprocessos sem rótulos. Os hashes dos escores foram fixados em `SCORES_COMMIT.json`; o coordenador conferiu os pinos e emitiu `ACK_SCORES.json` antes da abertura das classes. A primeira tentativa sob R1 recusou um pino BG1 alterado **antes da geração de sementes**; a comparação do coordenador identificou somente a data de criação alterada no JSON BG1. A recusa, R1 e R2 permanecem preservadas.

Foram pontuados 1.600.000 vetores completos: 100.000 por hipótese e cenário, mais 100.000 amostras de importância por modelo. Há **400.000 realizações primitivas independentes**, pois os sete cenários ordinários de cada hipótese reutilizam os mesmos erros, e os dois estimadores compartilham os mesmos vetores. Geração e avaliação: 63,0063 segundos; nenhuma chamada externa, custo marginal de API zero; energia e custo do equipamento não medidos. Os vetores de entrada foram temporários; sementes sob custódia e hashes dos arrays permitem reconstrução. Nenhum y observado foi lido ou ajustado.

## Resultado primário congelado

Teste unilateral `Z ≥ 5`, com `t = hhat_local − grad_h · bg`, desvio nulo próprio e α = Φ(−5) = 2,8665157×10⁻⁷. β/K e o fundo não foram ajustados às injeções. A hipótese de independência H0DN–BG1 e a covariância Gauss–Newton de BG1 são condições do ensaio.

| Quantidade | Basal publicado | Cepheid diferencial livre |
|---|---:|---:|
| Separação esperada D | 6,823355 | 5,316944 |
| Poder analítico | 96,5875% | 62,4357% |
| Poder MC | 96,609% | 62,485% |
| IC95% Wilson do poder MC | 96,4950–96,7194% | 62,1844–62,7846% |
| Cobertura nominal 95%, classe nula | 94,932% | 94,890% |
| Cobertura nominal 95%, classe TGL | 95,005% | 95,078% |
| Resíduo TGL padronizado: média / desvio | 0,004817 / 0,999908 | 0,003011 / 0,997075 |
| Cauda nula por importância | 2,84416×10⁻⁷ | 2,89059×10⁻⁷ |
| Erro padrão MC dessa cauda | 2,14812×10⁻⁹ | 2,17038×10⁻⁹ |

Ambas as caudas de importância são compatíveis com Φ(−5). As zero excedências nulas ordinárias não demonstram 5σ: com 100.000 ensaios, o limite superior unilateral 95% é 2,99569×10⁻⁵. A calibração de 5σ do primário vem da distribuição gaussiana linear especificada, verificada por importância. Separação D≥5 não significa poder de 95%; D=5 corresponde a poder de 50%. Nenhuma das duas variantes foi selecionada após a abertura.

## Nuisance pré-especificado

Tabela do estimador basal, com desvio padrão nominal congelado. O último campo recalibra somente a escala usando a variância verdadeira do cenário, conforme o plano; não representa novo ajuste de pesos.

| Cenário Cepheid, mag | Rejeição nula MC | Poder TGL MC | Cobertura TGL | Poder TGL com variância recalibrada |
|---|---:|---:|---:|---:|
| Sem acréscimo | 0/100000 | 96,609% | 95,005% | 96,609% |
| Viés fixo −0,05 | 20/100000 | 99,921% | 72,015% | 99,921% |
| Viés fixo +0,05 | 0/100000 | 67,810% | 72,484% | 67,810% |
| σ adicional 0,01 | 0/100000 | 96,073% | 94,084% | 94,387% |
| σ adicional 0,03 | 5/100000 | 92,271% | 87,151% | 60,948% |
| σ adicional 0,05 | 158/100000 | 86,006% | 75,227% | 16,853% |
| σ adicional 0,10 | 4283/100000 | 73,515% | 49,781% | 0,397% |

Estes valores de viés/ruído são sensibilidades declaradas, não medições. A redução de cobertura e o aumento da rejeição nula mostram por que o basal não admite a atribuição de 5σ sob um nuisance ignorado. No modelo Cepheid livre, a influência sobre essa coluna é numericamente zero; os sete cenários têm exatamente as mesmas contagens: poder 62,485%, cobertura TGL 95,078%, nula 94,890%, e zero excedências nulas ordinárias. Isso protege contra **essa coluna específica**, sem proteger contra toda sistemática possível. Os ICs e previsões analíticas de todos os cenários estão no JSON integral.

## Logaritmo exato do fundo

[DERIVED/REAL — cálculo determinístico] Para H0 de BG1 normal no parâmetro físico, integramos `φ(z) sf((q + log10(1 + σBG z/H0) − δ)/σlocal)` em −12..12, `epsabs=10⁻¹⁷`. A massa omitida é menor que 3,56×10⁻³³. Não houve clipping, redraw ou novas amostras. O logaritmo exige H0 positivo; a massa gaussiana de H0≤0 está muito além do domínio de integração e é explicitada por log-probabilidade no recibo.

| Diagnóstico exato | Basal | Cepheid livre |
|---|---:|---:|
| Cauda exata no corte congelado 5σ₀ | 2,9205341×10⁻⁷ | 2,8957223×10⁻⁷ |
| Significância normal equivalente | 4,996399 | 4,998045 |
| MC por importância menos integral, em SE MC | −1,122 | +1,139 |
| Corte futuro q/σ₀ para α=Φ(−5) | 5,003604985 | 5,001955991 |
| Poder nesse corte futuro | 96,568351% | 62,383835% |
| Cobertura MC exata, classe TGL | 95,008% | 95,078% |
| Cobertura MC exata, classe nula | 94,932% | 94,892% |

O corte futuro caracteriza a pequena diferença de parametrização; **não substitui o teste congelado, não reclassifica escores e não retuna o ensaio**. Cobertura exata dos 14 cenários ordinários consta do suplemento. Cauda exatamente gaussiana não deve ser atribuída ao logaritmo não linear.

## Covariância entre os degraus

[REAL — revisão delimitada] Recalculados os envelopes de variância para os pesos congelados a partir de `network.npz`; concordância máxima 4,86×10⁻¹⁷ em desvio padrão. O bloco de 55 calibradores e uma interceptação HF é diagonal e independente dos demais na matriz publicada. Com diagonais/cal-cal fixas, o complemento de Schur permite o termo cruzado entre `±2√(vcal vhf)`. Permitindo toda correlação PSD no bloco com diagonais fixas, a norma de uma soma de vetores Gram fornece os limites de polígono: superior `(Σ|li|σi)²`, inferior `max(2 max |li|σi − Σ|li|σi,0)²`, acrescidos da variância externa. As misturas ρ<1 verificadas permanecem positivas nesse bloco.

São limites exatos do estimador fixo **nessa família declarada**, não correlações físicas medidas, veto à TGL, estimativa de variância minimax ou licença para transportar a covariância Pantheon+ diretamente. A revisão documental leu `AUDIT.json`; não repetiu a construção de IDs/agregações nem as comparações primárias. Os valores GLS reotimizados do agente construtor não foram reexecutados nesta checagem. A ausência do mapa de agregação e a separação pendente da parcela Cepheid limitam qualquer transplante. Sensibilidades PSD orientam a busca documental, sem transformar ρ escolhido em dado da natureza.

## Evidências

`UNBLINDED_RESULTS.json`: resultados integrais, ICs, classes e caudas de importância.
`EXACT_BG_SUPPLEMENT.json`: quadratura, cobertura exata dos escores existentes, massa omitida e custos.
`CROSS_ENVELOPE_REVIEW.json`: verificação independente dos envelopes e escopo documental.
`INDEPENDENT_GEOMETRY_REVIEW.json`: comparação independente BLUE/KKT, suporte PSD e fixtures pré-freeze.
`CUSTODIAN_RECEIPT.json`: pinos calculados dos artefatos desta entrega.

[OPEN] Esta entrega demonstra capacidade prospectiva **condicional** e a sensibilidade ao modelo de covariância; não é um desvio observado, confirmação experimental, aceite oficial ou mudança de gate.
