# Revisão matemática independente — série e custo na torre, continuação 054

Estatuto: **[DERIVED — revisão matemática dos fontes, sem falha material encontrada]**. Esta nota não é uma revisão final do lote, um resultado de compilação ou um selo. Foi produzida durante uma sonda serial administrada pela raiz; nenhum processo Lean, runner ou auditor foi executado por este revisor nesta tarefa.

Revisor: Newton, agente `/root/relative_operator_domains`. Os dois módulos revistos foram escritos por outros agentes: `PolarizerCostSeries.lean` por Beauvoir e `TowerModularCost.lean` por McClintock. A revisão compreende a leitura integral dos enunciados e provas dos bytes identificados abaixo.

## Evidência medida

[REAL — bytes relidos por script] A tabela registra o estado lido para esta nota. Contagens são censos textuais de declarações e impressões, sem substituir a cobertura e a conferência de axiomas pelo auditor do lote.

| Arquivo | Bytes | SHA-256 |
|---|---:|---|
| [PolarizerCostSeries.lean](<C:/IALD/Central de Patentes/Chatgpt/PolarizerCostSeries.lean>) | 6011 | `52b147834a44d8d6e8b6a8af62d9d924e51d2c3243ba50214b4f602129f25342` |
| [TowerModularCost.lean](<C:/IALD/Central de Patentes/Chatgpt/TowerModularCost.lean>) | 16091 | `ab4216f6fb6cffa80d8ce452d745203c043a42aa4ecc2a63e28597a57759e451` |
| [ModularCostDerivative.lean](<C:/IALD/Central de Patentes/Chatgpt/ModularCostDerivative.lean>) | 16643 | `8373e71cf95e4bc3e152be9147ef0a0c5d15c39d64240beb9c4c8ba2326563ed` |
| [PATCH054_DOUBLE_COEFFICIENT_NEWTON.txt](<C:/IALD/Central de Patentes/Chatgpt/PATCH054_DOUBLE_COEFFICIENT_NEWTON.txt>) | 4031 | `0fba9247c60314f4a0abc89d9cdfa75eae55da266bae8e007b214db9fe4574f1` |
| [CONTINUACAO054_DERIVACAO_PREVIA.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO054_DERIVACAO_PREVIA.md>) | 7558 | `d9988eb729af6e8ae23bfb12cbeb0f1d8bf21098055ca8f65a1af76ce2b3863e` |
| [DERIVACAO054_GENERICO.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO054_GENERICO.md>) | 525 | `36d99148c29412fc25eb87ece0b1fbae28b706974233876e18d0441f0f0187df` |
| [DERIVACAO054_DERIVADA.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO054_DERIVADA.md>) | 1674 | `8416bb1d98590b61c207f40a54115e80598e396c9795b9f2d7b0a29dc61eff2c` |

Data da medição: 2026-09-07T06:48:10.457862+00:00. Os dois fontes revistos somam 36 teoremas, 5 definições e 41 comandos `#print axioms`. Não há declaração de instância nesses dois fontes. Os arquivos de derivação aparecem como contexto; o módulo de derivadas e o fragmento aparecem para delimitar a contribuição de autoria descrita adiante.

## Série escalar

`polarizer_cost_hasSum` parte da série convergente de `log(1+d)−log(1−d)`, sob `|d|<1`, e multiplica por `d`. O termo resultante é exatamente

`(2/(2n+1)) · d^(2(n+1))`

A prova inclui `d=0` e `d<0`; não divide pelo parâmetro assinado. A não negatividade é demonstrada termo a termo pela potência par. Para pesos estritamente positivos, `d=(w_i−w_j)/(w_i+w_j)` satisfaz a hipótese e a soma vale `d(log w_i−log w_j)`. A identidade da razão usa somente denominadores não nulos provenientes da positividade dos pesos; pesos iguais não são excluídos.

A passagem a `ENNReal` usa uma prova efetiva de `HasSum` e não negatividade antes de `ofReal_tsum_of_nonneg`. Assim, não há uso de uma soma real divergente cujo valor convencional zero fosse promovido a custo finito.

Os lemas `polarizer_cost_of_norm_powers` e `polarizer_cost_of_weight_norm_powers` têm uma hipótese explícita sobre todas as normas das potências de `D`. Essa hipótese é uma condição de avaliação do custo já definido. Ela não é atribuída a vetores arbitrários; o módulo da torre a constrói nos vetores locais utilizados.

## Mesmo operador global, pesos e fatores

`towerModularCost P` e `towerModularCostDomain P` aplicam as definições genéricas ao **mesmo `statePolarizer P` da continuação 053**. `state_polarizer_local_power` demonstra, por indução, que as potências desse operador global coincidem com as iterações da matriz local em `towerPi P a Ω`, para `a` hermitiana. A identificação de cada iteração usa a ponte anterior `state_polarizer_local`; não é postulada por semelhança das fórmulas.

A norma GNS quadrática é
`Σ_j Σ_i w_j · d_ij^(2n) · |a_ij|²`
O **peso de coluna `w_j`** é o correto para `Tr(ρa^*a)`. A soma finita dos resultados escalares dá o custo local e prova sua finitude; a fidelidade dos pesos fornece `|d_{ij}|<1` para cada par, sem exigir uma lacuna espectral global.

Para `a=a^*`, a troca `i↔j` e `|a_{ji}|^2=|a_{ij}|^2` dão a fórmula em pares ordenados
`C_P(aΩ) = ½ Σ_i Σ_j (w_i−w_j)(log w_i−log w_j)|a_ij|²`
O fator **1/2** está correto: as duas parcelas de um par não ordenado somam o coeficiente completo, e a soma ordenada o conta duas vezes. Não encontrei fator 2 suplementar nem inversão de sinal.

Os controles mantêm os vetores anteriores: o primeiro Pauli tem norma GNS quadrática 1 e custo `log 2/3`; o segundo flip é bruto, com norma quadrática `5/9`, e custo `2 log 2/3`. O emprego das razões escalares 2:1 e 4:1 no lema auxiliar não substitui o estado da torre por pesos sem normalização: as normas GNS efetivas permanecem na expressão.

## Domínio, radical e covariância

O custo é estendido, com valores em `ENNReal`. A fórmula finita é provada para vetores dos prefixos autoadjuntos, não para todo vetor ou todo operador global limitado.

A nulidade equivale a `statePolarizer P x=0`. A identificação com o centralizador e com o núcleo de todas as respostas é formulada **para operadores autoadjuntos pertencentes ao fator**. Não há classificação do radical por operadores arbitrários fora desse setor.

A covariância vale para todo `h : TowerHorizon P`, todo vetor e o **mesmo perfil P**. Usa `horizonGNSUnitary P h`, construído em 053, e sua restrição real `horizonCostIsometry`. O transporte de `AΩ` para `adT h A Ω` emprega `horizon_gns_apply_factor`; não pressupõe que o implementador algébrico bruto de `h` fixe Ω. O domínio é preservado nos dois sentidos.

`tower_cost_domain_dense_real` conclui
`closure(Dom C_P ∩ R_P) = R_P`
na **topologia de Hilbert**, usando as aproximações locais da esperança e sua convergência em Ω. Isto não prova que os prefixos sejam um núcleo para a norma da forma, nem demonstra aqui uma forma quadrática fechada ou sua unicidade. A semicontinuidade inferior é explicitamente transportada do resultado genérico, sem promovê-la a essas conclusões adicionais.

## Autoria e limites desta revisão

`PolarizerModularCost.lean` é de minha autoria e **não recebe aprovação independente nesta nota**.

Produzi `PATCH054_DOUBLE_COEFFICIENT_NEWTON.txt`, integrado pela raiz a `ModularCostDerivative.lean`, como proposta de reparo da prova de `local_modular_double_coefficient`: regras diagonais antes da expansão de produtos, conjugação explícita, parte real das somas e simetrização. Isso é **contribuição de autoria**, não revisão independente do módulo de derivadas, e o fragmento não foi compilado por mim. A identificação dos bytes desse módulo na tabela não lhe confere aprovação; sua revisão independente e a compilação permanecem processos separados.

Esta nota não demonstra a identificação do custo global com uma forma de `log Δ`, a entropia relativa de Araki global, uma métrica espacial ou uma área gravitacional. O custo e a covariância aqui examinados não pagam por si os contratos `hheat` e `harea`, nem selecionam tensor material, tela física ou relógio. **H3 e a reconstrução física geral permanecem [OPEN].**

Conclusão delimitada: não foi encontrada falha matemática material em `PolarizerCostSeries.lean` e `TowerModularCost.lean` nos bytes medidos. A validação final do lote, de suas dependências e dos axiomas impressos não é objeto desta nota.
