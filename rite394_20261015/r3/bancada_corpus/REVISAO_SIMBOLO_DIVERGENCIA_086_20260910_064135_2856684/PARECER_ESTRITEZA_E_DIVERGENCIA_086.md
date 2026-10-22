# Revisão independente da estriteza e da divergência quadrática em todas as ordens finitas

10/09/2026. Investigação086, separada da entrega085. Autor desta análise: /root/finish_gibbs_realization. [DERIVED — revisão matemática escrita]. [REAL — custódia e links medidos no recibo]. Nenhum cálculo matemático, CAS, Lean ou um.py foi executado nesta revisão.

**Conclusão da leitura adversarial:** não identifiquei erro material na demonstração de inexistência de V natural, quadrático nas classes lineares de Weyl/EOM e de ordem finita, com div₀V=J_W, no domínio expressamente fixado pela fonte. A prova não precisa que a torre curva de Weyl seja livre ou coincida com a torre plana. A estriteza da imagem das EOM, a injeção do graduado com sua derivada e a injetividade da divergência no módulo plano maior são suficientes. A presente conclusão é de minha autoria; não registra aprovação em nome do operador ou de outro agente.

A fonte examinada integralmente é [ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md>), acompanhada de seu [manifesto](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/MANIFESTO_SIMBOLO_DIVERGENCIA_086.json>). Os hashes efetivos, inclusive os dos antecedentes, estão no recibo desta revisão. A leitura do texto ocorreu antes e depois de sua confirmação de congelamento; a captura e a releitura final medem os arquivos congelados.

## 1. Qual é exatamente a afirmação examinada

O fundo é uma espaço-forma orientada de dimensão quatro, com métrica Lorentziana não degenerada, K>0 real fixado e campo sigma constante. O operador métrico Einstein linearizado está fixado. O setor em análise é puramente métrico; o alvo S³ e os campos sigma variáveis do habitante físico não são substituídos por esse setor sem hipótese adicional.

Se U denota as expressões lineares nos jatos de h, E o subespaço gerado por todos os prolongamentos de Hh e γ o gauge linear h↦R₀C, então Mcal=kerγ/E é um subespaço de U/E, pois HR₀=0. Os vetores naturais examinados pertencem a

                  (Rher⊗Sym²Mcal⊗V₀)^h.

Aqui h é a isotropia de Lorentz da referência, V₀ sua representação vetorial e Rher uma álgebra real unital não nula, inerte após fixar os operadores. As únicas dependências de fundo disponíveis são as dessa referência e os escalares herdados. Em particular, não há vetor de Killing escolhido, tensor espectador, coordenada ativa, inverso de um dado dinâmico ou série de ordens ilimitadas.

A exigência é mais forte que a covariância simultânea de uma expressão em (g₀,h): os fatores lineares já são classes invariantes por gauge no quociente efetivo. Isso é indispensável tanto para identificar o módulo quanto para comparar com a transgressão por conexão. O resultado é sobre uma igualdade local nesse quociente, não sobre integrais, igualdade módulo divergências ou uma identidade que valha apenas numa família de soluções TT.

## 2. A estriteza da imagem das EOM é o passo que remove relações inferiores ocultas

Conferi o uso do [lema polinomial079 e de sua fatoração diferencial](<C:/IALD/Central de Patentes/Chatgpt/SUBSETOR_ANTIFIELD_PURO_079_20260910_041018_659161/ANTIFIELD_PURO_FATORACAO_BIANCHI_E_DELTA.md>), com a normalização DH=0 e o fator dois que converte o gradiente simetrizado na divergência. O argumento086 usa uma consequência do lema de símbolo; não precisa supor PH=0 para toda a expressão em cada etapa.

De fato, se e=PHh tem ordem ≤j, mas P tem ordem r com r+2>j, a parte homogênea superior de PH é zero. Portanto σᵣ(P)σ₂(H)=0. A fatoração explícita do núcleo esquerdo fornece um símbolo B de ordem r−1 cujo produto pelo símbolo da divergência é σᵣ(P). Quantizando com derivadas simetrizadas de fundo e coeficientes à esquerda, P−BD tem ordem estritamente menor e

                         (P−BD)H=PH.

Esta igualdade usa a identidade diferencial completa DH=0. Não descarta os termos inferiores produzidos pela curvatura ou pela conexão; eles permanecem no resto para o passo seguinte. Não deriva uma extensão arbitrária dos coeficientes pontuais, pois os coeficientes do operador retirado permanecem à esquerda.

A redução termina porque r é um inteiro finito. No grau zero, o núcleo polinomial do símbolo esquerdo de Einstein é zero, conforme a fórmula079. Obtém-se um representante P' de ordem ≤j−2, ou a expressão zero quando j<2. Isso demonstra a igualdade de imagens filtradas da equação(4) da fonte, e não apenas uma inclusão entre símbolos.

Esse controle é suficiente para excluir o defeito típico de uma relação de alta ordem que cancelasse todos os seus termos superiores e deixasse uma nova relação de ordem baixa não gerada pelo símbolo plano. O procedimento troca exatamente tal relação por outra de menor ordem. Assim as relações iniciais do quociente U/E são os prolongamentos planos de Einstein.

Os denominadores do fator polinomial são inteiros não nulos dependentes de n+r, não p². O aberto p²≠0 é usado em079 apenas para provar que um polinômio é identicamente zero; não introduz um operador inverso no resultado. A naturalidade e a finitude do procedimento permanecem na classe requerida.

## 3. A injeção do graduado, com a derivada, basta

A passagem gr(U/E)≅Uflat/Eflat decorre da estriteza acima. Para Mcal, porém, a afirmação necessária é somente uma INJEÇÃO. A escolha da filtragem induzida pela inclusão Mcal⊂U/E torna essa inclusão estrita por definição. Logo grMcal injeta em gr(U/E).

É importante verificar que essa imagem está no núcleo gauge plano. Escolha um representante gauge-fechado de grau mínimo da classe curva. Se outro representante de menor ordem no quociente difere dele por EOM, continua gauge-fechado: HR₀=0 e seus prolongamentos anulam a variação da diferença. A parte superior de qualquer representante assim escolhido é aniquilada pelo símbolo de Killing plano. Portanto a imagem está em Mflat=kerγflat/Eflat. Não se usou uma afirmação de que todo elemento plano possa ser levantado ao fundo curvo.

Há também uma forma de testar diretamente a possível perda de injetividade: se a parte principal de um representante se tornar uma EOM plana, a estriteza permite retirar a EOM curva correspondente e diminuir sua ordem, preservando o fechamento gauge. Ela não pode continuar sendo um símbolo não nulo de grau mínimo. Isso esclarece por que uma simples comparação de dimensões não é necessária.

A conexão fixa de fundo comuta com a variação linear e preserva o ideal diferencial das EOM. Derivar acrescenta no máximo uma ordem. No graduado, seus termos principais são as derivadas totais planas; curvaturas e comutadores reduzem a ordem. Todos os índices de cada jato entram nessa operação. Assim a injeção entrelaça a derivada principal, e consequentemente a divergência principal. Uma injeção apenas como representações de Lorentz não bastaria para o passo final; a fonte paga a compatibilidade adicional.

Para os produtos quadráticos, a filtragem correta é a convolução pela SOMA das ordens dos dois fatores. Sobre R, espaços filtrados podem ser cindidos grau a grau. Tensorizar e tomar a potência simétrica preservam a injeção, e

                    gr Sym²Mcal ≅ Sym²(grMcal).

Não se trata da máxima ordem presente em apenas um fator. Por exemplo, o produto WᵣWᵣ₊₁ tem ordem total 2r+5 em h, e não r+3. As peças até cada ordem são representações finitas da isotropia; o símbolo de um vetor invariante continua invariante. Para a inclusão usada não é necessário presumir finitude local sob toda a álgebra de Killing.

## 4. O módulo plano é calculado sem importar liberdade curva

As duas primárias efetivamente consultadas são usadas em um alcance delimitado. A seção3.1 de [Khavkine, 2018](https://arxiv.org/pdf/1805.03751) apresenta o complexo de Calabi na curvatura constante, com o operador de Killing, a curvatura linearizada e Bianchi. O caso plano dá a geração dos invariantes lineares de métrica por curvatura. Não usei essa referência para afirmar liberdade de jatos de Weyl na referência curva.

No setor plano, a geração também se vê na decomposição homogênea dos jatos de h: os diagramas de Young ocupados pela transformação de gauge deixam apenas o tipo de Riemann e seus prolongamentos. Em dimensão quatro, as EOM de Einstein retiram Ricci e seus prolongamentos. Bianchi reduz a parte restante às duas equações de spin2 sem massa.

As equações(2.1)–(2.4) de [Anco–Pohjanpelto, 2002](https://arxiv.org/pdf/math-ph/0202019) descrevem os jatos simetrizados do sistema plano, e (2.6)–(2.7) sua derivação total. Esse é o dado importado da fonte. Sua classificação de correntes com coeficientes de Killing externos não é aplicada aqui.

A redução spinorial é compatível com o quociente métrico: em ∂EE'ψABCD, a contração nos índices não primados é a equação de divergência. Ao prolongar, as derivadas planas comutam; contrações primadas de duas derivadas reduzem a □ψ, consequência das mesmas EOM. Restam, como limite superior, as representações

                 Wᵣ⁺=(r+4,r),    Wᵣ⁻=(r,r+4),

com pesos inteiros iguais a 2j e ordem r+2 em h. Esse raciocínio por geração e relações é uma afirmação sobre o módulo plano. Não se transforma em um pressuposto de jatos curvos independentes.

Conferi também a realização métrica usada para mostrar que nenhuma das duas cópias planas é apagada por relações adicionais do potencial h. Para pAA'=λA·tildeλA', escolha tildeξ com [tildeλ tildeξ]≠0 e tome

 hAA'BB'=λAλB·tildeξA'tildeξB'·exp(i p·x)/[tildeλ tildeξ]².

O traço e a divergência são zero pela contração λAλᴬ=0. Como p²=0, a onda resolve o operador Einstein plano em gauge TT. Na curvatura não primada, as duas derivadas contraem os spinors primados e cancelam o denominador. O resultado é um múltiplo não nulo de λAλBλCλD exp(i p·x). A outra quiralidade contém uma contração λAλᴬ e é zero. O fator global depende da normalização de R e da escolha exp(i p·x); somente sua não nulidade é utilizada, e ele pode ser removido por reescala do potencial.

Variar λ e tildeλ gera os tensores puros de cada representação irredutível Wᵣ⁺; a construção com índices trocados realiza Wᵣ⁻. Uma cópia irredutível não nula não admite que apenas uma parte dela seja retirada por relações equivariantes. Com o limite superior anterior, isso identifica cada grau plano. Graus diferentes são homogêneos distintos. A conclusão não depende de escolher uma solução curva que realize jatos arbitrários.

## 5. Conferência de todos os tipos vetoriais, sem corte arbitrário de derivadas

Para cada sl₂, o peso1 aparece em a⊗c precisamente quando |a−c|≤1 e a+c é ímpar; sua multiplicidade é um. Nas duas componentes de Lorentz, essa regra se aplica simultaneamente.

No produto Wᵣ⁺⊗Wₛ⁺, ambas as condições dão |r−s|=1; o mesmo vale para a quiralidade negativa. No produto cruzado, seriam necessárias |r−s+4|≤1 e |r−s−4|≤1, que não podem ocorrer juntas. Logo todas as cópias vetoriais são

                       Wᵣ⁺Wᵣ₊₁⁺ e Wᵣ⁻Wᵣ₊₁⁻.

Como os dois fatores têm ordens distintas, cada par não ordenado fornece uma única cópia em Sym² do módulo total. Não há uma multiplicidade extra proveniente da troca de fatores. O primeiro grau total em h é cinco; em cada grau 2r+5 há uma cópia por quiralidade. Nos outros graus o espaço vetorial é zero.

Esta contagem considera todas as ordens r≥0 elemento a elemento. Ela não supõe uma lista finita de candidatos universais e não confunde a finitude de cada expressão com uma cota uniforme sobre todo o módulo. O controle de símbolos é necessário depois da contagem: uma cópia vetorial poderia, em princípio, ter divergência identicamente zero.

## 6. Por que a divergência de cada cópia é não nula e por que as imagens não se cancelam

Se Sᵣ⁺ é a contração completa de Wᵣ⁺ com ele mesmo, sua paridade de troca é (−1)^(2r+4)=+1. Portanto ela é realmente um escalar quadrático simétrico. A derivada grad Sᵣ⁺ pertence à única cópia vetorial correspondente, e analogamente para a outra quiralidade.

O teste por duas ondas é um teste de não nulidade no próprio quociente plano, pois as ondas são soluções de um potencial métrico. Tome p=λ·tildeλ e q=μ·tildeμ, com AMBAS as contrações <λμ> e [tildeλ tildeμ] não nulas. No campo que soma duas ondas puramente positivas, o termo cruzado de Sᵣ⁺ é um múltiplo não nulo de

           <λμ>^(r+4)[tildeλ tildeμ]^r exp(i(p+q)·x).

Os termos trocados somam porque a contração é simétrica. O operador □ multiplica esse termo por −(p+q)²=−2p·q, e p·q é proporcional ao produto dos dois brackets. Portanto □Sᵣ⁺ não é zero. Uma forma equivalente de acompanhar a polarização, usando exp(p·x), é escrever o termo cruzado como 2ab(p·q)^r<λμ>⁴ exp((p+q)·x); sua derivada □ é 4ab(p·q)^(r+1)<λμ>⁴ exp((p+q)·x), a menos de constantes convencionais não nulas. A versão com i altera apenas o sinal e as potências globais de i.

A condição dos DOIS brackets é relevante. No complexo, dois vetores nulos distintos podem compartilhar um dos spinors; apenas dizer que não são colineares seria insuficiente. A equação(12) da fonte já impõe as duas condições, de modo que não há correção a pedir nesse ponto.

Como □Sᵣ⁺ é não nulo, grad Sᵣ⁺ também é e gera a única cópia vetorial positiva. O mesmo vale para a negativa. Para separar as duas imagens, use apenas ondas métricas positivas, quando todos os geradores negativos são zero, e depois faça a escolha inversa. Nenhuma combinação linear não trivial das duas divergências pode ser a expressão zero. Isso prova injetividade em cada grau do espaço dos vetores invariantes.

A prova não identifica as expressões módulo curls. Um vetor identicamente conservado nesse espaço seria precisamente um elemento do núcleo da divergência já excluído. Correntes com tensores de Killing externos ou com índices livres adicionais estão fora do espaço contado; sua existência na literatura não constitui um contraexemplo ao argumento.

## 7. A comparação de graus retorna ao problema curvo e ao anel herdado

Se V é um elemento curvo não nulo e finito, existe um maior grau efetivo d na filtragem induzida. O símbolo principal não é zero e injeta no espaço vetorial plano maior. Pelo entrelaçamento da derivada e pela injetividade plana, a parte de grau d+1 da divergência curva é não nula. Logo div₀V tem grau exatamente d+1≥6.

J_W é quadrático em Weyl linear e tem grau quatro em h. Seu símbolo não é zero: a parte quiral de Pontryagin é um múltiplo não nulo de S₀⁺ ou S₀⁻, e as mesmas duas ondas separam essas partes. Uma relação efetiva curva que retirasse esse símbolo contrariaria a estriteza e a injeção já estabelecidas. Assim não há igualdade div₀V=J_W; V=0 também não satisfaz a equação.

K está fixado e tem grau zero nesta filtragem de ordem de derivadas em h. Multiplicá-lo, ou multiplicar por qualquer função permitida de parâmetros fixados, muda coeficientes e termos inferiores, mas não cancela o símbolo não nulo do maior grau de um vetor efetivo. Não há aqui uma declaração sobre a filtragem de engenharia ou sobre um anel universal no qual K ainda varie.

Sobre Rher, os mapas relevantes são extensões escalares de mapas reais do operador já fixado. Todo espaço vetorial real é plano como módulo sobre R; portanto tensorizar preserva as injeções. A mesma escolha de maior grau funciona para um elemento finito com coeficientes herdados. Nilpotentes não são separados por avaliações numéricas: a extensão escalar é o argumento que os cobre. O elemento 1⊗J_W continua não nulo numa álgebra real unital não nula.

Uma série de ordens crescentes não possui necessariamente maior grau e não é coberta. Tampouco se cobre a alteração do operador ou a introdução de tensores espectadores e dependências espaciais ativas. Esses limites não são detalhes dispensáveis do enunciado.

## 8. Transgressão ordinária e consequência cohomológica

O controle inicial por conexões é coerente. Na apresentação GL do mesmo fibrado tangente, a diferença A entre duas conexões sem torção satisfaz Aᵃ_b∧e₀ᵇ=0. Como R₀ é K e₀∧e₀, isso anula tr(A∧R₀). O coeficiente quadrático da transgressão ordinária é d tr(L∧Dbar L)=tr(W₁∧W₁). A primitiva existe como expressão simultaneamente covariante em (g₀,h), mas sua variação linear de gauge não é zero em geral. Ela não pertence a Sym²Mcal. Portanto não contradiz a obstrução demonstrada.

Transportar a conexão ao fibrado ortonormal de g₀ não permite reutilizar automaticamente a condição de torção no mesmo coframe. A fonte mantém corretamente o termo 2tr(a₂∧R₀) nessa apresentação. Não identifiquei confusão entre essa transgressão e o símbolo da corrente invariante.

Para a consequência CE, a fonte utiliza dois antecedentes explicitamente separados: a [forma normal084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>) reduz a exatidão à equação J_W=div₀V+K²f, com f∈N^g; a [análise085](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>) remove esse último termo no mesmo domínio. Com esses contratos, a presente inexistência de V implica não exatidão do alvo CE fixado.

A [transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>) relaciona a imagem de d₁ em E5 à liberdade de levantamento que preserva a classe líder em C3. Nesse domínio, a consequência atinge as correções admissíveis dessa classe líder, não apenas uma expressão particular escolhida anteriormente. Isso continua sendo uma obstrução do passo e do líder especificados. Não se transforma em uma classificação de todos os líderes, de toda a cohomologia natural com espectadores ou de um complexo causal interagente diferente.

O resíduo tem ghost quatro. Não foi calculado um coeficiente de anomalia física de ghost um, nem uma violação de QME em uma teoria renormalizada construída. Não há conclusão sobre UV, reconstrução gravitacional geral, confirmação ou falsificação da TGL. Nenhuma fase, ramo interno já pago ou H3 canônico é reaberto por homonímia com esse grupo H³ cohomológico.

## 9. Estatuto documental e encerramento desta revisão

[DERIVED] A análise acima reexaminou os elos matemáticos e não identificou erro material no alcance declarado. Ela não é uma compilação formal nem uma execução de testes algébricos. A conferência curta recebida sobre ondas planas é compatível com a conta aqui exposta; não é tratada como revisão integral de toda a fonte por outro autor.

[REAL] O helper novo desta pasta apenas lê bytes, calcula SHA256, verifica os pins registrados, confere links locais e publica os novos documentos por temporário verificado. O recibo separa a contagem desses controles documentais do conteúdo matemático da revisão. Foram capturadas a nota, seu manifesto e os sete antecedentes pinados pela fonte; não houve auditoria recursiva das entregas antigas.

[REAL] Nenhum original, fonte congelada, memória canônica, Atlas, selo ou gate foi alterado. Zero novas execuções matemáticas, CAS e Lean; nenhum um.py foi importado ou executado. Os pins desta revisão apontam somente para caminhos finais existentes, não para o nome temporário renomeado durante a publicação.

[OPEN — fora do enunciado] Correntes com infinitos jatos, dependência ativa ou tensores espectadores; mudança do fundo ou da categoria de coeficientes; o fundo sigma físico não constante; outros líderes e a construção interagente geral. Essas questões não são resolvidas nem refutadas pela prova revista.
