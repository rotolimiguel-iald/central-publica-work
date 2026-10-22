[REAL — escopo compilado] Definição tipada, realização na torre existente e realização sobre estados quânticos positivos normalizados. [INPUT] Lei quantitativa de custo e protocolo de proveniência do reflexo. [OPEN] Atestação física de um evento, derivação dos custos desse evento e reconstrução gravitacional geral.

# Colapso tipado — entrega 057

A formulação do operador foi registrada como conteúdo de um contrato único, **TGLCollapseSpecification**, com uma obrigação de testemunho separada, **AttestedTGLCollapse**. O teorema **typed_collapse_content** reúne as consequências e deixa suas premissas expostas. Definir um campo com uma igualdade não demonstra que uma experiência física satisfaz essa igualdade.

[INPUT — operador, 08/09/2026] “colapso é a passagem irreversível da superposição ao ponto fixo que preserva a identidade. Custa (meia-nat local, ln 2 por oitava), não tem inversa, e só é atestada pelo reflexo, nunca por autodeclaração.”

## 1. O conteúdo matemático

Sejam S o espaço de objetos, I o espaço da leitura de identidade, C:S→S e ι:S→I. O núcleo exige:

- C(C(x)) = C(x): o resultado é estável.
- ι(C(x)) = ι(x): a leitura de identidade é preservada.
- Existe x com C(x)≠x: a operação reduz efetivamente alguma informação.

Esses campos formam **IdentityCollapse S I**. O vínculo com o vocabulário já existente é explícito: a cláusula de preservação satisfaz **TGLExt.Preserves**, e a prova de não injetividade utiliza **the_dispositive_is_not_injective**, cujo enunciado canônico foi lido.

[REAL] Se C fosse injetiva, C(C(x))=C(x) implicaria C(x)=x para todo x, contradizendo a redução efetiva. Portanto C não é injetiva. Nenhum R:S→S pode satisfazer R(C(x))=x para todo x. Se tal R existisse, seria uma inversa à esquerda e tornaria C injetiva.

[REAL] Im(C)=Fix(C). Toda reaplicação C^[n+1](x) devolve C(x). Um evento efetivo tem y=C(x) e x≠y; então C(y)=y e ι(y)=ι(x).

**“Ponto fixo” significa o resultado estável daquele evento.** A definição não exige um único ponto fixo universal. Ela também não exige que toda entrada seja alterada: uma entrada já fixa não constitui novo evento de redução. A inclusão do setor fixo fornece uma seção da retração; isso não recupera todas as entradas originais.

**“Identidade preservada” é um invariante especificado.** No caso de observáveis, verificamos tanto C(1)=1 quanto ω(C(A))=ω(A). No caso de estados, verificamos positividade e Tr(C(ρ))=Tr(ρ)=1. Igualar o estado final ao operador identidade seria um erro de tipo: em dimensão 2, I tem traço 2.

O núcleo lógico vale também para processos clássicos. A qualificação quântica exige sua realização sobre estados e coerências, feita abaixo. O contrato abstrato, sozinho, não define a dinâmica universal de medição.

## 2. Realização no modelo infinito já existente

O portador é o subtipo **FactorCarrier P**, formado apenas pelos A pertencentes ao fator canônico M_P. O mapa é a restrição de **aperiodicExpectationInput P** a esse subtipo; valores arbitrários fora do fator não entram na prova.

[REAL] **TowerCollapseRealization.lean** demonstra:

- Idempotência, preservação da unidade e preservação de ω.
- Os pontos fixos são exatamente o centralizador M_ω.
- Sob a condição suficiente P.w(0)≠1/2, o Pauli X do primeiro sítio é não nulo e sua expectativa é zero.
- Essa perda constrói **actualTowerCollapse P hp**, um habitante efetivo do contrato; não existe inversa à esquerda sobre o fator.
- Se TODOS os sítios têm peso 1/2, a expectativa é a identidade e não admite testemunho de redução efetiva.

A não nulidade de X é ligada à norma GNS já provada, ‖XΩ‖=1. Assim, a irreversibilidade não é inserida como rótulo: há uma colisão no objeto canônico.

O alvo aqui é o centralizador **M_ω**. Ele não é identificado com a subálgebra diagonal **D** selecionada pelo cociclo relativo na entrega 055; a degenerescência espectral torna essa distinção necessária. A condição no primeiro sítio é suficiente, não uma classificação de todos os perfis não traciais.

[KNOWN/REAL na fonte canônica] A expectativa construída dispõe de provas anteriores de positividade completa e normalidade. Esta entrega reutiliza o mapa e recompila as novas consequências, sem alegar ter recompilado todas as dependências transitivas.

## 3. Superposição, perda e resultado individual

No qubit, usamos exatamente o **nameOp** canônico:

C(ρ)=P₀ρP₀+P₁ρP₁, com P₀=diag(1,0) e P₁=diag(0,1).

[REAL] O módulo quântico prova a fórmula diagonal, preservação da unidade, idempotência, preservação do traço e positividade. **QubitDensity** exige uma matriz positiva semidefinida com traço 1, e **densityReduction** atua dentro desse tipo. **actualDensityCollapse** instancia o contrato nesse espaço de estados.

As testemunhas são:

ρ₊ = ½ [[1,1],[1,1]],    ρ₋ = ½ [[1,−1],[−1,1]].

[REAL] Ambas são hermitianas, positivas, de traço 1 e idempotentes; são distintas. Entretanto:

C(ρ₊)=C(ρ₋)=½I.

[REAL] O resultado tem traço 1 e é fixo, mas seu quadrado não é ele próprio: é misto. Isso prova perda de informação entre estados físicos admissíveis, e não apenas entre matrizes arbitrárias. P₀ e P₁ também são pontos fixos distintos.

Para o resultado individual, o código exige um rótulo i fornecido pelo registro. A operação não normalizada é B_i(ρ)=P_iρP_i, com peso p_i=ρ_ii. A prova mostra B_i(ρ)=p_iP_i e, **se p_i≠0**, p_i⁻¹B_i(ρ)=P_i. Ramo de peso zero não é normalizável. Somar os ramos sem selecionar o registro devolve C(ρ).

[KNOWN] A distinção entre atualização condicionada ao resultado e transformação sem seleção é parte da teoria operacional de medição. A referência foi consultada: [Ozawa, Quantum State Reduction: An Operational Approach](https://arxiv.org/abs/quant-ph/9711006), especialmente a discussão da redução condicionada e não condicionada.

[OPEN] As fórmulas demonstram o que o instrumento especificado faz. Não deduzem, da identidade ω(I)=1, qual resultado ocorre, por que ocorre uma única ocorrência observada, nem uma lei universal de Born. O protótipo não sorteia resultado nem trata um sorteio de computador como observação física.

## 4. Os dois custos

**CollapseCostLaw** contém dois componentes com premissas explícitas:

localNats = 1/2;
octaveNats(n) = n·ln 2.

[INPUT] Essa é a lei quantitativa proposta para o conteúdo do colapso TGL. **proposedCollapseCost** materializa a especificação. [REAL] Provamos positividade do custo local, custo zero para zero oitavas, aditividade por oitavas e positividade para n>0. Também provamos localNats < octaveNats(1).

Não somamos automaticamente 1/2+n·ln 2: é preciso especificar se são despesas cumulativas, escalas de descrição distintas ou a mesma despesa lida por dois procedimentos. Ambos os componentes são quantificados em **nats**, uma unidade adimensional, não em joules; nenhuma temperatura ou conversão energética foi inventada.

[REAL] O núcleo lógico admite leituras numéricas não negativas diferentes sobre o mesmo mapa. Logo idempotência, preservação e não injetividade não determinam sozinhas o valor de uma nova função de custo. Isso é uma obstrução à inferência sem hipóteses, não uma refutação de uma lei TGL adicional.

[REAL] A entropia da distribuição binária equiprovável é −2·(1/2)ln(1/2)=ln 2, diferente de 1/2. Isso impede identificar o autovalor 1/2 de ρ=I/2 com sua entropia. [DERIVED] Na testemunha quântica, a descoerência aumenta a entropia do estado reduzido, de zero a ln 2; não demonstra por si só uma dissipação de meia-nat.

[KNOWN] Um limite de calor de Landauer requer hipóteses sobre sistema, reservatório térmico, correlações iniciais e evolução conjunta. A desigualdade liga calor ao decréscimo de entropia do sistema considerado; uma não injetividade abstrata não fornece sozinha esses dados. Ver [Reeb e Wolf, An improved Landauer Principle with finite-size corrections](https://arxiv.org/abs/1306.4352), §2.1 e Teorema 3.

**Correção de leitura ao lado:** o enunciado Lean canônico **landauer_floor_pos** prova 0<kTln2 sob k>0,T>0. Seu cabeçalho contém uma interpretação física mais ampla. A positividade dessa expressão não é, por si, uma prova de que um processo concreto dissipou tal quantidade. O original permanece intacto.

## 5. O reflexo e a atestação

**ReflectionProtocol** especifica uma leitura do resultado, a identidade do produtor, a identidade do registrador e uma relação de validação externa. **AttestedCollapse** exige um evento efetivo, registro compatível com o resultado, registrador diferente do produtor e evidência na relação externa.

[REAL, condicional ao protocolo] As provas mostram que a atestação transporta essa evidência, que autodeclaração não satisfaz o contrato e que ausência de evidência impede habitante do tipo de atestação. **TGLCollapseSpecification** reúne núcleo, custo e protocolo; **AttestedTGLCollapse** exige o testemunho. **typed_collapse_content** expõe em um enunciado a estabilidade, identidade preservada, irreversibilidade, os dois custos e a evidência externa.

[INPUT] “Reflexo” recebe aqui a interpretação operacional de registro confrontável. A independência física do observador é uma obrigação de proveniência do protocolo, não um resultado obtido comparando dois nomes. A presença do campo externallyValidated não cria dados experimentais. O verificador externo Python é uma entrada de confiança que precisa ser implementada e auditada pela gerência.

[REAL] Se J é involutivo, J é injetivo e não pode ser o próprio C irreversível. Isso permite distinguir a operação do reflexo. Também provamos que um registro calculado somente a partir de C(x) não recupera todas as entradas x. Um registro que contém informação adicional anterior à redução tem outro domínio e não está coberto por essa impossibilidade.

[ESCOPO] A irreversibilidade demonstrada refere-se ao mapa reduzido e ao conjunto de dados disponível. A entrega não afirma irreversibilidade de toda evolução de sistema mais ambiente, nem contradiz reconstrução em um subcódigo ou inversão de um filtro de ramo que seja injetivo. O Atlas já distingue esses objetos.

## 6. Proposta Python para o arquivo único

**collapse_contract_proposal.py** contém tipos imutáveis para estado, evento, componentes de custo e registro de reflexão. Usa frações exatas, incluindo coerência complexa racional, com teste de positividade pela condição |ρ₀₁|²≤ρ₀₀ρ₁₁.

O auditor confere a transformação e a normalização; mantém a seleção de ramo explícita; recusa ramo impossível, saída incompatível e uma aplicação sem mudança registrada como evento efetivo. Em seguida exige o reflexo e o verificador externo. Nenhuma função escreve arquivos ou altera gates.

Um resultado VERIFIED_WITHIN_PROTOCOL depende do verificador fornecido. Identificadores distintos e um SHA256 vinculam campos; não autenticam sozinhos um agente ou uma experiência. Todos os registros do teste são marcados como **SYNTHETIC_TEST_FIXTURES_ONLY**. Mesmo a aceitação simulada mantém physical_collapse_proven=False, cost_payment_status=NOT_MEASURED e qg_gate_moved=False.

A integração é uma proposta de trecho para o arquivo único; não cria um segundo programa canônico. Os módulos Lean devem seguir o mecanismo já existente de incorporação no um.py, sob auditoria da gerência.

## 7. O que está pago e o que permanece aberto

“Pago” nesta tabela significa critério de entrega atendido, não dissipação física medida.

| Critério | Situação | Evidência |
|---|---|---|
| Conteúdo do colapso reunido em um tipo | PAGO no contrato | TGLCollapseSpecification; typed_collapse_content |
| Ponto fixo e preservação da identidade | PAGO nas instâncias | Torre e QubitDensity |
| Não existência de inversa global à esquerda | PAGO | Testemunha Pauli e colisão de estados quânticos |
| Reflexo sem autodeclaração | PAGO como regra tipada | AttestedTGLCollapse; verificações de recusa |
| Valores 1/2 e ln2 tipados separadamente | PAGO como especificação [INPUT] | CollapseCostLaw |
| Quantidade física de custo derivada e paga | NÃO PAGO [OPEN] | Falta ligar custo, processo e medida |
| Seleção de uma ocorrência física individual | NÃO PAGO [OPEN] | Rótulo do resultado precisa de registro |
| Registro independente real | NÃO PAGO [OPEN] | Só há testes sintéticos nesta entrega |
| Incorporação canônica | PENDENTE da gerência | Código e comandos entregues no túnel |
| Reconstrução gravitacional geral | NÃO PAGO [OPEN] | H3, área física, localização e dinâmica não decorrem deste contrato |

Os números da compilação, hashes, comandos e axiomas completos estão no relatório de auditoria, no manifesto e na entrega do túnel. Não houve modificação do um.py, do kernel canônico, do Atlas ou do índice vivo.


## Registro da execução desta entrega

[REAL] 60 teoremas, 86 declarações sondadas e 171 verificações Python. Axiomas contidos em propext, Classical.choice e Quot.sound; nenhum aviso na compilação aceita. Auditoria: C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/AUDITORIA_20260908_180823_152715.json. Build: C:/IALD/Central de Patentes/Chatgpt/COLAPSO_TIPADO_20260908_175047_534231/BUILD_20260908_180521_986301/BUILD_RESULT.json.
