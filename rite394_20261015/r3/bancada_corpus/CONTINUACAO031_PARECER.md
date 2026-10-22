# Continuação 031 — operador modular relativo, com domínio e fecho

[REAL / INPUT / OPEN] 06/09/2026. Continuação espontânea da ordem 007. Os quatro módulos finais passaram em Lean, sem erros, avisos ou dependências fora dos axiomas admitidos. A auditoria independente da gerência e a incorporação permanecem pendentes.

O avanço desta etapa é construir o operador relativo dos vetores efetivamente preparados na etapa 030. A identidade demonstrada é Δ_{Ψ|Ω}=R Δ_ω R, como operador fechado, com R=exp(L/2). A identificação com uma área física não decorre dessa identidade.

## Hipóteses e objetos efetivos

[INPUT] Trabalhamos na família somável já construída, com referência de sítio (1/3,2/3), amplitudes 0≤b_n≤1/12, soma finita e h(t)=t²/(1+t²). O parâmetro t varia o estado; s é tempo modular. L(t) é o gerador limitado de log-verossimilhança, e R=exp(L/2) é positivo, autoadjunto e invertível em M. A etapa 030 demonstrou RΩ=Ψ e ψ(A)=ω(RAR). Trata-se desta família de estados, não de todos os pares de estados de toda álgebra.

A etapa 031 constrói V=exp(-L/2), comprova RV=VR=I, V em M e VΨ=Ω, e reúne R e V numa equivalência linear contínua.

## Fecho relativo e adjunto

[REAL — fecho formalmente verificado] A convenção é S⁰_{Ψ|Ω}(AΩ)=A*Ψ, para A em M. O mapa de pares (x,y)↦(Vx,y) leva o gráfico algébrico de S_ω exatamente ao gráfico relativo. A mudança de variável A=VB é legítima porque V e R pertencem a M. Como o mapa de pares é um homeomorfismo, ele transporta o fecho inteiro do gráfico.

Disso resulta o operador fechado e densamente definido

S_{Ψ|Ω}=S_ω R, com D(S_{Ψ|Ω})={x: Rx∈D(S_ω)}.

O adjunto antilinear é R S_ω† em D(S_ω†). O código demonstra a identidade de pareamento e a maximalidade desse adjunto. Para a maximalidade, testar x=Vz converte a condição relativa em uma condição para S_ω†; o inverso limitado permite recuperar o valor do adjunto relativo. Não é apenas uma escolha de notação para o adjunto.

## Operador positivo e auto-adjunticidade

[REAL — lema genérico compilado] Para uma equivalência linear contínua e autoadjunta R, com inverso autoadjunto, e um operador positivo autoadjunto T densamente definido, a congruência RTR tem domínio R⁻¹D(T). Foram demonstrados gráfico, densidade, fechamento, pareamento adjunto, maximalidade, positividade e auto-adjunticidade. O módulo BoundedPositiveCongruence passou sem erros ou avisos; a lista de axiomas é extraída do log pelo auditor.

[REAL — aplicação formalmente verificada] Aplicando T=Δ_ω:

Δ_{Ψ|Ω}=R Δ_ω R,
D(Δ_{Ψ|Ω})={x: Rx∈D(Δ_ω)}.

A identificação com S_{Ψ|Ω}†S_{Ψ|Ω} inclui o domínio exato da composição. A forma quadrática é

Re⟨x,Δ_{Ψ|Ω}x⟩=‖S_{Ψ|Ω}x‖²≥0.

A positividade e a auto-adjunticidade são provadas para esse operador com esse domínio. Nenhuma igualdade com D(Δ_ω) é presumida.

## Relação com a pergunta sobre a inscrição angular

[CONJECTURE / OPEN] A proposta do operador distingue o gerador L da leitura angular que poderia dar área. Essa distinção é compatível com estudar u(s)=exp(isL) e suas variações. Uma fase pura tem módulo unitário: informação angular não aparece simplesmente em |u|². A etapa 030 construiu a alternativa F=(u-I)*(u-I), com adjunto no primeiro fator, e demonstrou F≥0 e F/s²→L² em norma no limite modular.

F e sua raiz positiva são operações diferentes. Para a parametrização t desta família, a estimativa formal é ‖F_t(s)‖≤36s²B²t⁴, com B=Σb_n e s fixo. A raiz tem uma escala de ordem no máximo t². A expressão pretendida pelo operador permanece em esclarecimento; esta etapa não escolhe silenciosamente entre módulo, módulo quadrático e área de duas direções.

Mesmo uma medida angular positiva ainda precisa de uma definição de superfície, escala de comprimento, regra região-álgebra e dinâmica para ser identificada com área gravitacional. A linguagem de cauda, poço, dobra da luz e retorno estabilizador permanece interpretação ontológica ou hipótese física, conforme a afirmação concreta. Nenhuma delas foi convertida em teorema pelo nome de L.

[DERIVED — exemplo escalar] Para uma fase e^{iθ}, |e^{iθ}-1|²=4sin²(θ/2), que é quadrático perto de θ=0. Esse exemplo esclarece uma leitura possível do termo inscrição quadrática, sem identificá-la com uma área física. O retorno periódico de uma fase também não demonstra estabilidade atrativa: essa afirmação exigiria uma dinâmica e um critério de estabilidade.

## Comparação com a literatura e próxima obrigação

[KNOWN] A definição de operador modular relativo pelo fecho de AΩ↦A*Ψ e por S†S é apresentada na seção 12.1 de [F. Hiai, Lectures on Selected Topics in von Neumann Algebras](https://arxiv.org/pdf/2004.02383). O teorema 9.4 relaciona perturbações por um operador positivo afiliado ao centralizador ao cociclo de Connes. A referência orienta a comparação matemática; não substitui as pontes formais desta bancada.

[OPEN] Falta provar nesta implementação que R e V preservam os domínios de Δ_ω e comutam com ele, para simplificar a congruência a exp(L)Δ_ω. A identificação com o cociclo de Connes pode seguir pelo cálculo espectral relativo ou por uma caracterização equivalente, como a do teorema 9.4 de Hiai. O cone natural fornece uma escolha canônica de representantes, mas formalizá-lo não é pré-requisito obrigatório para essa identificação. Identificar o fator polar relativo com o J canônico exige prova própria; o cone ou uma decomposição polar direta são vias possíveis. O nome deltaImaginaryPower existente é uma construção para o operador original; não é um cálculo funcional genérico automaticamente aplicável ao relativo.

Uma revisão independente somente leitura confirmou a ordem dos operadores, a convenção antilinear e os domínios propostos, sem identificar circularidade. Um refinamento adversarial corrigiu a lista de obrigações: o cone natural é uma via possível, não uma dívida universal obrigatória. De fato, substituir Ψ por W'Ψ, com W' unitário no comutante e Ω fixo, muda S relativo para W'S e deixa S†S invariante; essa observação é analítica aqui, não um teorema novo deste módulo. A revisão não é recompilação nem aprovação da gerência.

## Verificação e custódia

O auditor031 exige compilação limpa para os bytes finais de cada fonte, cobertura integral dos teoremas por impressão de axiomas e somente propext, Classical.choice e Quot.sound (ou lista vazia). As contagens e hashes são calculados dos artefatos. Tentativas rejeitadas, seus logs e backups dos bytes permanecem no inventário.

A primeira compilação de RelativeTomitaClosure foi rejeitada por duas reescritas inadequadas de componentes de pares, avisos de variáveis implícitas e um limite de custo do kernel. O processo terminou com exit 1 antes de uma tentativa de interrupção conseguir localizá-lo. Nenhum término foi registrado falsamente como compilação limpa. A correção separou as componentes e usou um lema genérico para reconstruir um gráfico unívoco. A segunda tentativa foi interrompida explicitamente pela bancada após localizar o custo no teorema de densidade; o registro de interrupção não é apresentado como saída do compilador. A densidade foi então reduzida ao lema genérico de congruência já verificado, e o módulo do fecho relativo passou limpo na terceira tentativa.

A primeira tentativa do módulo RelativeModularOperator foi interrompida por custo excessivo e preservada como registro de bancada. A tentativa diagnóstica seguinte foi rejeitada: mostrou uma expansão cara no transporte inverso do domínio, uma reescrita com testemunho de domínio mal convertido e inferência cara de parâmetros na congruência. A versão final reutiliza o transporte genérico já provado, compõe as igualdades diretamente e explicita os operadores nos argumentos. Passou com o limite de cálculo reduzido; não foi necessário aumentar esse limite para obter o resultado.

Todos os artefatos desta etapa ficam em Chatgpt. Os originais, um.py, kernel canônico, Atlas, memórias, selos e gates permanecem intocados. A etapa 030 mantém sua errata nominal ao lado; nenhum arquivo selado foi corrigido por sobrescrita.

[OPEN] A prova ampla de gravidade quântica e a reconstrução gravitacional geral permanecem abertas. O número de teoremas inclui auxiliares e não mede uma porcentagem de conclusão física.
