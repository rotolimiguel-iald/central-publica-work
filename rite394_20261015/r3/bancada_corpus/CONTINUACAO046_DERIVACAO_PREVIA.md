# Continuação 046 — roteiro anterior à compilação final

Este roteiro integra seis módulos em desenvolvimento. As derivações listadas abaixo foram criadas antes dos respectivos módulos; este roteiro de integração foi criado depois das primeiras fontes e antes do lote final. Compilação de desenvolvimento não é o selo final.

## Alvo e quantificadores

A ORDEM_010, alvo A.3, pede a construção de aperiodicExpectationInput quando possível. O alvo aqui é para TODO P:SiteProfile, sem hipótese de período comum. Para cada A no fator, construir o limite forte de C_n(A)=periodAverage(P,n+1,A), não assumir o limite como premissa.

## Cadeia e registros prévios

1. DERIVACAO046_APERIODICA.md → AperiodicPhaseAverage.lean: média de uma fase não ressonante tende a zero; fase zero permanece um; média matricial converge ao pinching por igualdade de pesos.
2. DERIVACAO046_LEVANTAMENTO.md → BoundedOmegaLimit.lean: limite em Ω de sequência uniformemente limitada no fator produz limite forte B no fator usando a órbita direita densa, completude e bicomutante.
3. DERIVACAO046_VETORIAL.md → AperiodicVectorAverage.lean: contração vetorial, convergência local, densidade e completude produzem o limite para todo vetor; em AΩ ele coincide com a média por conjugação; o passo2 constrói B.
4. DERIVACAO046_PREFIXO.md → AperiodicAveragePrefix.lean: projeção em cada corte comuta com a média e força a identidade prefixal do limite.
5. DERIVACAO046_ESPERANCA.md → AperiodicCentralizerExpectation.lean: escolha clássica do B construído, into, fixes e ortho por pinching e limites; obtém o registro ExpectationInput, a cota ‖E(A)‖≤‖A‖ e idempotência no fator.
6. DERIVACAO046_LEVANTAMENTO_GERAL.md → AperiodicTowerLift.lean: aplica unicidade e levantamento canônicos ao termo construído, sem reprovar esses antecedentes; compatibilidade periódica/tracial, covariância por todo horizonte do contrato e do funcional E∘K sob as hipóteses explícitas de K.

A infraestrutura tem derivação própria DERIVACAO046_INFRA.md. A nota histórica CONTINUACAO045_APERIODIC_REVIEW.md documentou o caminho antes deste código.

## Critérios da verificação

- Fontes exatas recompiladas em diretório novo, seis módulos juntos e Imports046All.
- Todas as definições/teoremas têm #print axioms; zero sorry/admit/axioma novo; somente propext, Classical.choice e Quot.sound nos relatórios.
- Nada de instâncias anônimas. As construções são termos nomeados, não registro de typeclass.
- Dependências locais transitivas copiadas e verificadas contra os selos anteriores; fronteira externa declarada sem inventar proveniência.
- Manifesto, auditor e revisão por outro autor; evidência separa compilações de desenvolvimento e lote final.
- Arquivos canônicos, memórias, Atlas, um.py e selos anteriores permanecem somente leitura.

## Estatuto e limites

[DERIVED — até o lote final] A rota fornece uma prova matemática candidata do contrato no modelo de torre. [OPEN] A normalidade e a positividade completa da esperança, além das exigências do registro atual, necessitam provas próprias. Escolha clássica de limites não é um algoritmo numérico executável de convergência uniforme. Valores do mapa fora do fator são zero por definição e não recebem promessa de linearidade global.

[OPEN] A identificação com geometria gravitacional, a seleção de métrica/regiões/telas, H3 e o problema completo de gravidade quântica continuam abertos. Os horizontes aqui são objetos do contrato algébrico, e o funcional K continua sujeito às hipóteses declaradas. Nenhum gate canônico muda.
