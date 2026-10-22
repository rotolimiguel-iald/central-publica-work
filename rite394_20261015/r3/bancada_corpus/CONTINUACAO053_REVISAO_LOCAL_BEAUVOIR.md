# Revisão local053 — versões finais dos dois módulos locais

[REAL — leitura de fontes, metadados e logs de desenvolvimento]
Data: 2026-09-07. Revisor: agente review_global_cocycle (identificação de trabalho Beauvoir).

Esta nota registra a revisão matemática independente de LocalPolarizerWitness.lean e CovariantAreaCounterexample.lean, construídos pelo agente review_cocycle_covariance. O revisor é autor de SymplecticPolarizer.lean e contribuiu previamente apenas com o trecho da derivada em TowerStatePolarizer.lean; esses componentes próprios não recebem autoaprovação independente nesta nota. A autoria e a revisão cruzada são registros da colaboração, não uma autenticação fornecida pelo parser.

O vínculo abaixo é exclusivamente com a sonda de desenvolvimento completa. Não é CONTINUACAO053_REVISAO_INDEPENDENTE.md, não emite aprovação do build final, não sela053 e não controla o processo final da raiz.

## Evidência relida

Marcador: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO053_DEVELOPMENT_20260907_053849_427670.json

SHA256 do marcador, medido nesta leitura: 5b5378d14aed03e1eaef75af65a9c44d59ccd23da68e326053e57e290f9c55ba

Diretório: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO053_DEVELOPMENT_20260907_053849_437570

O marcador declara status PASS, development_only=true, seis etapas; seus seis metadados confirmam exit_code=0, passed=true, entradas/fontes estáveis, cobertura exata e ausência de issues. Não se reclassifica essa sonda como build final.

| Fonte | Bytes | Teoremas | Definições | Instâncias | Prints | SHA256 atual |
|---|---:|---:|---:|---:|---:|---|
| LocalPolarizerWitness.lean | 20361 | 33 | 8 | 0 | 41 | fd96e40e0020189f09f0d37f03b70443b4675edf5cdc6c2604bcc11ff2300bf8 |
| CovariantAreaCounterexample.lean | 15612 | 23 | 2 | 0 | 25 | 7ebd9e02979150d639850cb95ddaffe04cbe0e915accb102ad6dd25e4bfc2804 |

As duas fontes atuais são idênticas por bytes às cópias compiladas. Os logs04_LocalPolarizerWitness.log e05_CovariantAreaCounterexample.log foram relidos no diretório acima:41 e25 linhas de axiomas, respectivamente, contendo somente propext, Classical.choice e Quot.sound; nenhuma linha warning/error/sorryAx foi encontrada. Total dos dois módulos revistos:56 teoremas,10 definições,0 instâncias,66 prints.

Foram relidos os enunciados e os ajustes de prova dos dois fontes. A comparação preserva o diagnóstico matemático anterior. As correções incluem a ordem dos fatores após star_mul, casos na conjugação da diagonal, parâmetros e coerções explícitos, o auxiliar local_real_smul_action e a prova das quatro entradas escalares do Gram antes da igualdade matricial. A abertura de ClosedSubmodule reutiliza a estrutura real existente; não introduz uma nova instância declarada nestes módulos. Não houve enfraquecimento das hipóteses ou dos alvos examinados.

## Identificação do polarizador local com o global

O candidato local tem entradas

    b_ij = i (w_i−w_j)/(w_i+w_j) a_ij.

A fidelidade dos pesos paga o denominador positivo. Para a hermitiana, b é hermitiana e satisfaz a equação de Sylvester

    ρb+bρ = i(ρa−aρ).

Essa identidade produz Re tState(xb)=Im tState(xa) para todo x local hermitiano. O passo decisivo de state_polarizer_local não se limita aos testes locais: recebe B arbitrário autoadjunto no fator global, usa state_local_right para reduzir as duas expressões a expectationMatrix(B), e usa expectationMatrix_hermitian. O critério tower_polarizer_eq_of_pairing conclui a igualdade com o operador D definido por projeção sobre o mesmo subespaço real fechado. Não se pressupõe que um cálculo num corte já identifique o operador global.

## Pares, respostas e calibração

No primeiro par de Pauli, o Gram GNS real é I₂ e D atua com fator1/3. No par bruto doubleFlipX,doubleFlipY entre00 e11, o Gram é (5/9)I₂ e D atua com fator3/5. Os sinais são DX₁=Y₁/3, DY₁=−X₁/3 e DX₂=3Y₂/5, DY₂=−3X₂/5.

A expectativa aperiódica efetiva da046 anula ambos os flips duplos por seu pinching local. As curvas e as leituras fixas são as da035; a resposta calculada é (2u₁/3,−2u₀/3). Sua injetividade assegura que o segundo plano contém direções efetivas de variação do estado, não apenas alterações de purificação ou direções centralizantes.

A mesma família global hε é normalizada por2(1/9+ε/81). Para ε≥0 esse denominador é positivo e o Gram no primeiro par é sempre I₂/2. No segundo par BRUTO, o Gram anterior à normalização é

    (1/5+9ε/125) I₂.

Por isso as áreas, definidas como raiz do determinante do Gram, são9/10 para ε=0 e1377/1250 para ε=1, com diferença126/625. Não se misturam aqui os valores do segundo par normalizado para norma GNS um. A calibração comum também força que qualquer possível reescalamento global tenha fator um; a discrepância no segundo par então o exclui.

## Quantificadores e alcance

normalized_covariant_invariant quantifica sobre todo h:TowerHorizon thirdThermalReference, usando sua ação adT original em operadores autoadjuntos do mesmo fator. A prova herda o implementador GNS efetivo, que preserva o subespaço real; não restringe os horizontes a fluxo modular ou permutações, nem presume que o unitário original do horizonte fixe Ω.

Para ε≥0, o radical nos autoadjuntos limitados do fator é exatamente o centralizador. As identidades de adição em cada entrada pagam a descida por essas direções estacionárias. normalized_covariant_response_kernel identifica o mesmo radical com a anulação de todas as respostas reais autoadjuntas. Não se afirma que esse resultado classifique todos os vetores da completude real, todos os tangentes de estados normais, ou uma variedade global de estados.

Conclusão da leitura matemática: não foi encontrada falha material nas versões vinculadas. Elas fornecem duas formas globais covariantes, com a mesma calibração e radical, que dão áreas distintas nas mesmas direções efetivas. Isso é um negativo para a suficiência desses critérios de seleção. Não exclui critérios adicionais, não identifica essas áreas com áreas de horizonte, não deriva H3, não estabelece Bisognano–Wichmann e não encerra reconstrução gravitacional.

Nenhuma compilação, auditoria final ou alteração de fonte/infraestrutura/derivação foi executada pelo revisor nesta conferência. Este documento novo é a única escrita da revisão.
