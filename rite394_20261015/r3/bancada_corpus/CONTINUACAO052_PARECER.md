# Continuação052 — plano horizontal, horizonte modular e área

[REAL — escopo das declarações compiladas e auditadas] UTC: 2026-09-07T04:40:36.050266+00:00

O lote liga duas direções efetivas de variação do estado ao horizonte modular da mesma torre. Nesse plano, a invariância de uma forma bilinear real simétrica pelo quarto de volta modular fixa sua forma até escala. Uma normalização explícita fixa a escala. Separadamente, o pareamento imaginário do estado com o quarto de volta orientado constrói uma forma positiva com escala dependente do estado. H3 e a reconstrução gravitacional geral permanecem OPEN.

## Correção ao lado da proposta051

A [nota de correção052](<C:/IALD/Central de Patentes/Chatgpt/NOTA052_CORRECAO_AREA051.md>) registra o limite da proposta de ponderar E e I−E por escalas distintas. A direção centralizante Z usada no exemplo é vertical para a órbita unitária do estado: ela não altera esse estado. No setor horizontal do exemplo, a família reduz-se a um múltiplo da forma GNS; normalizar pode remover essa liberdade. Além disso, a034 já define literalmente sua forma pelo produto GNS. Trocar a forma troca o critério daquela construção.

A proposta051 e sua custódia permanecem intactas. A nota052 é análise de escopo, não um novo teorema Lean de classificação do quociente global. A052 investiga diretamente um plano de variações observáveis.

## Mesmo estado, operadores e derivadas

Sejam p=P.w(0), com 0<p<1, r=2p−1 e ν=log(p)−log(1−p). No primeiro sítio, X e Y são os operadores de Pauli existentes. Para u=(u₀,u₁), definir H(u)=u₀X+u₁Y. Para p≠1/2, a expectativa centralizante efetiva da046 satisfaz E(X)=E(Y)=0. A relação com o pinching local é demonstrada pelas propriedades da mesma expectativa, sem introduzir outro operador E.

O pareamento da mesma torre é:

    Re ω(H(u)* H(v)) = u₀v₀+u₁v₁,
    Im ω(H(u)* H(v)) = r(u₀v₁−u₁v₀).

Aqui * denota adjunto; H(u) é autoadjunto. As duas direções têm norma GNS um e são ortogonais para a parte REAL. No espaço complexo, seu produto é i r, portanto não são ortogonais complexas quando r≠0.

Usando a curva unitária existente da035, com U(t)=exp(i t H(u)) e leitura ω(U(t)* B U(t)), as derivadas reais nas leituras X,Y são:

    resposta(u) = (−2r u₁, 2r u₀),
    determinante da matriz de resposta = 4r².

Quando p≠1/2, a resposta é injetiva. Assim, direções distintas desse plano produzem derivadas distinguíveis de leituras do estado global. Trata-se de um plano da órbita UNITÁRIA, não de todos os tangentes de estados ou de variações dos autovalores.

O lema quantum_centralizer_imaginary_zero demonstra ainda que a parte imaginária do pareamento entre um elemento autoadjunto centralizante e um elemento autoadjunto do fator é zero, pela ciclicidade e pela conjugação do estado. Isso identifica uma obstrução vertical; não constrói sozinho o quociente global completo.

## O quarto de volta é realizado pelo horizonte concreto

A ação modular existente satisfaz:

    σ_t(X) = cos(νt)X − sin(νt)Y,
    σ_t(Y) = sin(νt)X + cos(νt)Y.

No tempo t₀=−π/(2ν), essa ação induz R(u₀,u₁)=(−u₁,u₀). A igualdade entre adT do horizonte efetivo e H(Ru) foi demonstrada, usando os mesmos objetos das duas etapas anteriores.

[INPUT] Para selecionar a forma, exige-se bilinearidade real, simetria e invariância simultânea das duas entradas pelo quarto de volta efetivo. Não se postula previamente isotropia. Para uma função F nos operadores e sua restrição bilinear b(u,v)=F(H(u),H(v)), as hipóteses implicam:

    b = c · ReGNS,  com c=b(e₀,e₀).

A simetria exclui a componente antissimétrica. A positividade não é necessária para essa igualdade; quando desejada, impõe o sinal correspondente a c.

## Dois critérios de escala, explicitamente distintos

1. [INPUT] Normalização do traço relativo ao produto GNS real: b(e₀,e₀)+b(e₁,e₁)=1. Então c=1/2 e a densidade de área sobre o par fixo (e₀,e₁) é 1/2.

O lema da soma diagonal em pares unitários é usado DEPOIS da seleção b=c·ReGNS. Ele não deve ser citado como uma demonstração de invariância geral do traço antes dessa seleção.

2. Definir Ω(u,v)=Im ω(H(u)*H(v)) e tomar o tempo orientado tₒ=−π/(2|ν|)<0. A ação efetiva induz Q=sign(r)R. Construir a própria função:

    gΩ(u,v) = Im ω(H(u)* σ_tₒ(H(v))) = Ω(u,Qv).

Sua bilinearidade é provada a partir dessa expressão. A052 demonstra:

    gΩ(u,v) = |r| ReGNS(u,v),
    gΩ é simétrica, positiva e não degenerada para r≠0,
    área(gΩ; e₀,e₁) = |r|,
    Ω(u,v) = −gΩ(u,Qv),  Q²=−I.

A fórmula da compatibilidade tem sinal negativo com essa ordem dos argumentos. O tempo de quarto de volta positivo daria orientação oposta. Q é um operador linear real no plano e não a conjugação modular antilinear J, para a qual J²=I.

[INPUT] Usar Ω e esse quarto de volta para calibrar a forma é um critério adicional à covariância; a covariância sozinha deixa c livre. Não se identifica aqui gΩ com Fisher, Bures ou uma área física de horizonte.

Para o perfil de referência com p=1/3, a densidade calibrada nesse par é exatamente 1/3. Esse par de Pauli não é a tela de outro lote; comparar esse valor com uma área de outra tela exige primeiro identificar os pares e os critérios.

Essas áreas são densidades de Gram no par de geradores fixado, transportáveis às derivadas identificadas pela resposta injetiva. Não são a área total da órbita nem a área espacial de uma região. Os dois critérios não precisam dar o mesmo número.

## Controle tracial e fronteira da afirmação

Se p=1/2, a resposta dessas duas direções é zero; E fixa X,Y; a ação modular nesse sítio é a identidade; Ω e quantumOrbitPairing são zero. O mapa auxiliar orbitOrientedTurn(0)=0 não representa essa ação identidade. Outros sítios não traciais podem manter não trivial o fluxo modular da torre inteira.

O relógio modular e a curva unitária usada para medir a resposta são fluxos diferentes. A existência de um quarto de volta no primeiro não identifica automaticamente os seus parâmetros nem fornece o relógio físico da curva do segundo.

[KNOWN — contexto externo] [Petz–Sudar](https://arxiv.org/abs/quant-ph/0102132) discutem a família de métricas quânticas monótonas; isso ajuda a explicar por que uma seleção exige critérios. [Contreras–Ercolessi–Schiavina](https://arxiv.org/abs/1501.00054) estudam órbitas de estados mistos e o tensor de Fisher. Esses trabalhos são contexto; nenhuma identificação com os seus tensores é transportada para a052 sem prova das convenções e normalizações.

## Verificação e custódia

| Módulo052 | Teoremas | Definições | Instâncias | Prints | Alcance |
|---|---:|---:|---:|---:|---|
| [LocalHorizontalPauli.lean](<C:/IALD/Central de Patentes/Chatgpt/LocalHorizontalPauli.lean>) | 30 | 4 | 0 | 34 | Pinching, pareamento GNS e derivadas efetivas do estado. |
| [ModularHorizontalRotation.lean](<C:/IALD/Central de Patentes/Chatgpt/ModularHorizontalRotation.lean>) | 20 | 3 | 0 | 23 | Rotação e orientação pelo horizonte modular concreto. |
| [HorizontalAreaSelection.lean](<C:/IALD/Central de Patentes/Chatgpt/HorizontalAreaSelection.lean>) | 20 | 8 | 0 | 28 | Seleção por quarto de volta e dois critérios de escala. |
| [QuantumOrbitArea.lean](<C:/IALD/Central de Patentes/Chatgpt/QuantumOrbitArea.lean>) | 24 | 2 | 0 | 26 | Ligação ao estado, horizonte, positividade e densidade de área. |

Total052: 94 teoremas, 17 definições, 0 instâncias, 111 prints. Compilação conjunta: 5/5 etapas, incluindo importador. Zero avisos/erros; cobertura exata das declarações; somente propext, Classical.choice e Quot.sound nos relatórios de axiomas. A revisão independente está vinculada ao hash e ao diretório final.

Diretório final: C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO052_CLEAN_20260907_043311_769301

Build SHA256: fe87aac834619c82f929aa476de24161ba810cddc2146661f7dd438dcd7eda9a

Os quatro fontes052 foram copiados por bytes e compilados em diretório exclusivo. As dependências históricas foram verificadas e copiadas por pins; não foram recompiladas nesta rodada. O auditor repete o vínculo upstream045 entre origens, snapshots e adaptações. Imports externos diretos e companheiros Mathlib/stdlib foram medidos; não se afirma reconstrução exaustiva do fecho transitivo externo. Fontes locais usadas apenas para descoberta de imports não ganham proveniência fonte–binário por terem hash de leitura.

Sondas falhas, logs e backups ficam preservados como história, sem valor de prova. Escritas deste lote somente em Chatgpt. canonical_gate_changed=false registra esse escopo, sem auditar mudanças feitas por terceiros. Atlas, índice, um.py, kernel e memórias canônicas não recebem incorporação deste lote.

## Caminho ainda aberto

[OPEN] Selecionar fisicamente estado, álgebra, região e observadores; ampliar e compatibilizar os planos em outros pontos/sítios; justificar escala dimensional e área de horizonte; reconstruir métrica lorentziana e dinâmica; demonstrar o vínculo Ricci–matéria de H3. A052 estabelece uma construção e uma seleção condicionada em um setor concreto, sem resolver a reconstrução gravitacional geral.

Revisão: [CONTINUACAO052_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO052_REVISAO_INDEPENDENTE.md>). Entrega: [ENTREGA_052_setor_horizontal_e_area.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_052_setor_horizontal_e_area.md>). QG não está declarada confirmada, resolvida ou provada.


## Adendo documental antes do selo052

[REAL — correção de metadados] UTC: 2026-09-07T04:44:22.126774+00:00. A primeira tentativa de selagem foi interrompida antes da criação do manifesto ou de seu temporário: o auditor ainda continha a descrição de escopo e quatro limitações herdadas da051. Foram corrigidas somente essas strings, sem alteração da lógica de auditoria, das fontes Lean, do runner ou do build. A revisão independente registra o achado e a correção ao lado. Os documentos anteriores permanecem em backups exatos de bytes; os hashes da entrega foram atualizados.

Auditor corrigido SHA256: f7fe2613376d5d82859750f293b0f9cca85c8a5aacc8a24802e9aa8e4fb83a60

Revisão atualizada SHA256: 31a9a0c70b54bbfd2ea0efdd659d26ed6db2cd891d285e5cf025352cd44ce84a
