# Complexo relativo quadrático e cálculo CE na referência espaço-forma fixa

10/09/2026. Investigação087 NOVA, excluída da entrega086. Autor: /root/finish_gibbs_realization. [DERIVED — demonstração escrita proposta à revisão independente]. [KNOWN — cohomologia finita da isotropia e fatos planos indicados nas primárias]. [REAL — somente custódia documental no manifesto]. Zero execução matemática, CAS, Lean ou um.py.

**Resultado demonstrado abaixo, no contrato fixado.** O complexo relativo quadrático natural tem cohomologia apenas em grau quatro, livre de posto dois sobre Rher, representada por I₀ν e J₀ν. No complexo CE completo da álgebra de Killing, restrito aos cochains invariantes pela isotropia, os grupos são livres de postos dois, quatro e dois nos graus quatro, sete e dez, respectivamente, e zero nos demais graus. A prova constrói os geradores CURVOS dos escalares e das formas, usando a injeção graduada086; não presume liberdade da torre curva de Weyl.

Esses grupos são os da diagonal quadrática depois do primeiro diferencial CE. Não são a cohomologia do BRST completo nem todos os seus diferenciais posteriores.

## 1. Categoria, objetos e antecedentes exatos

Fixe uma espaço-forma orientada Lorentziana em dimensão quatro, com K>0 real fixado e κ real não nulo. A matéria sigma é constante e já foi projetada ao setor métrico mínimo. A métrica e sua conexão bar∇ são inertes. Não há campos ou tensores espectadores, dependência coordenada ativa, inversos de dados dinâmicos ou coeficientes escolhidos conforme a solução de teste.

O coeficiente Rher é uma álgebra real unital não nula, inerte para os operadores fixados; pode conter nilpotentes. Todas as extensões escalares abaixo são ALGÉBRICAS sobre R. Cada expressão tem finitos jatos. Uma completação por valência não autoriza infinitos jatos em um único coeficiente dessa valência; Rher tensor Mcal não é substituído por um produto tensorial completado sem contrato adicional.

Sejam U as expressões lineares nos jatos de h, E a imagem dos prolongamentos das EOM Einstein lineares Hh e γ o gauge linear h↦R₀C. Ponha

        Mcal=kerγ/E ⊂ U/E,       N₂=Rher⊗Sym²Mcal.

A identidade HR₀=0 permite a inclusão. É o módulo efetivo da [comparação081](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>). As igualdades são no quociente pelas EOM e TODOS os prolongamentos, não em um conjunto selecionado de soluções nem módulo divergências.

Escreva g para a álgebra de Killing da referência e h=so(1,3) para sua isotropia. Há decomposição redutiva g=h⊕V, com [V,V]⊂h. O complexo relativo é

                    Bᵖ=(N₂⊗ΛᵖV*)^h,    0≤p≤4.       (1)

Seu diferencial d_B é a derivada exterior covariante antissimetrizada. A identificação com cochains horizontais relativa a h decorre da [ação CE082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>). Ela age em todos os índices dos jatos. A identidade d_B²=0 vale nas formas horizontais invariantes: o quadrado da derivada é a ação de curvatura da isotropia, cancelada nesse espaço. Também se pode realizar (1) como formas naturais na referência homogênea, quando se trata da identidade usual d_H²=0.

A [demonstração086](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md>) e seu [parecer específico](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md>) fornecem:

- estriteza da imagem filtrada das EOM por P↦P−BD, com DH=0;
- gr(U/E)≅Uflat/Eflat e uma injeção grMcal↪Mflat que entrelaça a derivada principal;
- na potência simétrica, filtragem pela SOMA das ordens em h;
- no módulo plano, Wᵣ⁺=(r+4,r) e Wᵣ⁻=(r,r+4), em pesos inteiros iguais a2j, de ordem r+2 em h;
- realização métrica das duas quiralidades planas e não nulidade das contrações por duas ondas;
- divergência injetiva em todo vetor natural quadrático finito.

Nenhum desses itens é substituído pela hipótese de que grMcal seja sobrejetivo em toda a torre plana. A novidade abaixo realiza explicitamente apenas os tipos necessários para escalares e formas.

## 2. Geradores curvos explícitos e suas normalizações

Ponha W=W[1][h]. A estrela atua na última dupla de índices de Weyl e é paralela para a conexão de fundo. Para r≥0, defina

       Tᵣ=bar∇_(a₁…aᵣ) W,       T₀=W,
       Iᵣ=½⟨Tᵣ,Tᵣ⟩,           Jᵣ=½⟨Tᵣ,*Tᵣ⟩.         (2)

Os parênteses normalizam a simetrização por1/r!. A contração usa a inversa de g₀ em todos os r índices de derivadas e nos quatro índices de Weyl. São expressões locais naturais finitas, quadráticas e gauge-fechadas: γW=0 por W(g₀)=0, e γ comuta com a conexão fixa.

I₀=½W_abcdW^abcd e J₀=½W·*W=J_W. A normalização de I é a da [nota de uma derivada086](<C:/IALD/Central de Patentes/Chatgpt/CORRENTES_WEYL_UMA_DERIVADA_086_20260910/CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md>). Conforme seu [parecer](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CORRENTES_UMA_DERIVADA_086_20260910_065540_575112/PARECER_CLASSIFICACAO_E_NORMALIZACAO_086.md>), I082=2I₀, enquanto J mantém a normalização. Não se identifica I pelo nome sem esse fator.

No graduado principal, derivadas comutam e Tᵣ é o jato plano ∂_(a₁…aᵣ)W. As EOM/Bianchi planas retiram suas contrações inferiores; as partes restantes são Wᵣ±. A contração completa de cada quiralidade com ela mesma dá um singlete Sᵣ±. A paridade de troca é (−1)^((r+4)+r)=+1, logo esses singletes estão em Sym².

Os símbolos de Iᵣ,Jᵣ são duas combinações independentes de Sᵣ⁺,Sᵣ⁻, com uma matriz real/complexificada invertível: a estrela tem autovalores ±i e distingue as quiralidades. A simetrização de derivadas não acrescenta um fator r! no plano, pois as derivadas já comutam e a simetrização está normalizada. Assim

                 ord_eff(Iᵣ)=ord_eff(Jᵣ)=2r+4.          (3)

Para justificar a NÃO NULIDADE em (3), não basta um tensor abstrato. A086 constrói potenciais métricos TT planos que produzem somente uma das quiralidades. Duas ondas da mesma quiralidade, com ambos os brackets espinoriais não nulos, fazem Sᵣ± não nulo. O símbolo é, portanto, não nulo no quociente Einstein MÉTRICO plano. Se a expressão curva de (2) tivesse classe de menor ordem, a estriteza e a injeção086 fariam seu símbolo plano desaparecer no quociente, contradição.

Esse argumento também estabelece a independência dos dois símbolos e o seu levantamento curvo. Ele prova a sobrejetividade necessária dos SINGLETES por expressões de (2), não liberdade irrestrita de todos os jatos curvos.

## 3. Classificação e liberdade de B⁰

Na representação sl₂⊕sl₂, um singlete aparece no produto (a,b)⊗(c,d) apenas quando a=c e b=d, com multiplicidade um. Consequentemente, nos produtos da torre plana:

- Wᵣ⁺Wₛ⁺ tem singlete somente para r=s, e o mesmo vale para --;
- Wᵣ⁺Wₛ⁻ exigiria simultaneamente r+4=s e r=s+4, impossível;
- para r=s, a troca do singlete é par, conforme o §2.

Portanto há exatamente dois singletes em cada grau total 2r+4 e nenhum em grau ímpar ou menor que quatro. A injeção graduada086 limita o símbolo de um escalar curvo a esse espaço. Os dois levantamentos (2) atingem esse limite superior em cada grau.

Se F∈B⁰ é não nulo de ordem máxima2r+4, escolha Aᵣ,Bᵣ para que seu símbolo coincida com AᵣIᵣ+BᵣJᵣ. A diferença tem ordem estritamente menor. Repita até chegar ao grau mínimo. Há finitamente muitas etapas e todos os elementos retirados são naturais. Assim

             B⁰ = ⨁_(r≥0) (Rher Iᵣ ⊕ Rher Jᵣ).          (4)

A soma é DIRETA. Uma relação finita não trivial teria maior r com algum coeficiente não nulo, e seus dois símbolos independentes não poderiam se cancelar. A extensão para Rher será detalhada no §8; ela não depende de avaliar coeficientes nilpotentes.

Logo (4) é uma geração efetiva por redução do maior grau, não uma afirmação de local finitude sob g ou um pressuposto de liberdade da torre. As projeções de singletes são operações em representações finitas de h em cada corte; suas contrações e partes reais ficam na categoria natural. Coeficientes de parâmetros fixados permanecem inertes.

## 4. Formas de graus um e dois: geração e paridade

### 4.1. Toda uma-forma é um gradiente natural finito

Os tipos vetoriais planos foram classificados086. Um (1,1) aparece somente em Wᵣ±Wᵣ₊₁±, uma vez por quiralidade. A ordem total é2r+5; não há vetor em grau menor que cinco. Os símbolos de grad Iᵣ e grad Jᵣ geram essas duas cópias: no plano, grad Sᵣ± é não nulo, pois □Sᵣ± é não nulo nas duas ondas.

Como para (4), subtraia de uma uma-forma curva o gradiente de AᵣIᵣ+BᵣJᵣ que coincide com seu maior símbolo, e reduza a ordem. O processo é finito. Portanto

       B¹ = ⨁_(r≥0)(Rher d_BIᵣ ⊕ Rher d_BJᵣ),
       d_B:B⁰→B¹ é um isomorfismo de módulos.             (5)

O núcleo é zero porque o símbolo de grad Sᵣ± é não nulo e as quiralidades são independentes. Não é necessário inserir constantes em B⁰: B⁰ tem grau quadrático em campos, de modo que a unidade de Rher não pertence a ele.

### 4.2. Não existe duas-forma quadrática natural efetiva

Complexifique Λ²V*=(2,0)⊕(0,2). Considere primeiro dois fatores de mesma quiralidade Wᵣ⁺Wₛ⁺. Para o alvo(2,0), o singlete no segundo sl₂ exige r=s. Para o alvo(0,2), o singlete no primeiro sl₂ também exige r=s. Quando um desses tipos existe no produto tensorial, sua troca de fatores tem sinal

                      (−1)^((r+4)+r−1)=−1.              (6)

Explicitamente, no alvo(2,0) os dois fatores de troca são (−1)^(r+3) e (−1)^r; no alvo(0,2), são (−1)^(r+4) e (−1)^(r−1), quando r≥1. Para r=0, o segundo alvo nem aparece nessa quiralidade. Em todos os casos admitidos o tipo está na potência ANTISSIMÉTRICA dos dois fatores, e não em Sym². As expressões lineares de Weyl são bosônicas; seus produtos quadráticos usam Sym².

Os fatores de quiralidade negativa dão a mesma conclusão. Nos produtos cruzados, para (2,0), a igualdade do segundo peso exige r=s+4, deixando diferença oito no primeiro, incompatível com peso2. Para (0,2), a igualdade do primeiro deixa diferença oito no segundo. Não aparecem os alvos.

Logo não há duas-forma quadrática no módulo plano em NENHUMA ordem. Um elemento curvo não nulo teria símbolo não nulo injetado nesse espaço zero. Portanto

                              B²=0.                     (7)

A prova de (7) não usa um limite de graus nem supõe que uma relação curva simplesmente preserve uma contagem plana. Ela usa a injeção já demonstrada e o maior grau de cada elemento finito.

## 5. Graus três e quatro e o operador triangular □

A métrica e a orientação identificam B³ com B¹. Para evitar um sinal implícito de Hodge Lorentziano, escreva a três-forma associada a um vetor V como q_V=ι_Vν, onde ν é o volume. A normalização satisfaz exatamente

                     d_Bq_V=(div₀V)ν.                   (8)

Assim B³ é livre nos geradores q_grad Iᵣ,q_grad Jᵣ. Toda quatro-forma é Fν, F∈B⁰, e

                              B⁴=B⁰ν.                   (9)

Precisamos determinar a imagem de (8), não apenas sua injetividade. Pela geração(5), toda divergência é □F com F∈B⁰. Provaremos a fórmula triangular

       □Iᵣ=2Iᵣ₊₁+Lᵣ,       □Jᵣ=2Jᵣ₊₁+L'ᵣ,
       ord_eff(Lᵣ),ord_eff(L'ᵣ) ≤2r+4.                  (10)

Os restos pertencem a B⁰ e, por (4), são combinações FINITAS de Iₛ,Jₛ com s≤r. Não se pressupõe que todo resto seja um múltiplo único de K Iᵣ; sua forma precisa não é necessária para a redução.

**Prova de(10).** A métrica, o volume e a estrela são paralelos. Para T=Tᵣ de (2), Leibniz dá

       □(½⟨T,T⟩)=⟨bar∇T,bar∇T⟩+⟨T,□T⟩.             (11)

No caso dual vale a mesma fórmula com uma estrela em cada contração correspondente; sua bilinearidade simétrica permite combinar os dois termos cruzados. A estrela comuta com □ e com bar∇.

Na espaço-forma, ∇R₀=0. O comutador [□,bar∇] de qualquer tensor é uma combinação de R₀·bar∇T e, em geral, (∇R₀)·T; a segunda parcela é zero. Isso se obtém expandindo [∇ᵃ∇ₐ,∇_b] e aplicando o comutador de duas derivadas a TODOS os índices, inclusive aos índices de derivada já presentes. Por indução,

       □bar∇_(r)W = bar∇_(r)(□W)
                    + combinações de K·bar∇_(r)W
                    e termos de menor ordem.            (12)

No shell Einstein linear vale □W=6KW, como derivado083 e mantido na nota086 de uma derivada. Portanto □Tᵣ tem ordem efetiva no máximo r+2, em vez da ordem ingênua r+4. A segunda contração de (11) tem ordem no máximo2r+4.

Na primeira contração, bar∇Tᵣ difere de Tᵣ₊₁, com seu índice externo incluído na simetrização, por comutadores que trocam duas derivadas por curvatura. Para r≥1, o resto tem no máximo r−1 derivadas de W, isto é, ordem r+1 em h; para r=0 o resto é zero. O termo cruzado entre esse resto e Tᵣ₊₁ tem ordem no máximo(r+1)+(r+3)=2r+4, e o quadrado do resto é ainda inferior. Por (2),

       ⟨bar∇Tᵣ,bar∇Tᵣ⟩=2Iᵣ₊₁+ordem≤2r+4,

e a identidade dual dá2Jᵣ₊₁. Isso prova (10), com coeficiente superior exatamente DOIS. A simetrização normalizada não modifica esse coeficiente. ∎

Como controle de r=0, a fórmula completa conhecida é □I₀=2I₁+12KI₀ e □J₀=2J₁+12KJ₀. O fator12 é consistente com (11) e □W=6KW. Não foi executado cálculo novo para obter essa identidade; ela serve de comparação escrita com as normalizações anteriores.

## 6. Redução finita do quociente B⁰/□B⁰

De(10), cada Iᵣ₊₁ ou Jᵣ₊₁ é congruente, módulo □B⁰, a uma combinação de índices≤r. Dada uma expressão finita F, remova seu maior índice pela subtração de □(Aᵣ₊₁Iᵣ+Bᵣ₊₁Jᵣ)/2. Repita. Como o índice cai, a redução termina em

                 F = λI₀+μJ₀+□G,    G∈B⁰ finito.        (13)

Somente a divisão por2 aparece na etapa diagonal. Não há inversão de K, de uma derivada, de um operador hiperbólico ou de um elemento dinâmico. As operações que determinam cada resto são covariantes finitas; seus coeficientes permanecem na classe fixada.

A representação das duas classes restantes é única. Se λI₀+μJ₀=□G e G≠0 tem maior índice r, a fórmula(10) dá parte superior2AᵣIᵣ₊₁+2BᵣJᵣ₊₁ não nula de grau2r+6≥6. Não pode coincidir com um escalar de grau≤4. Se G=0, a independência de I₀,J₀ força λ=μ=0. Portanto

                 B⁰/□B⁰ ≅ Rher[I₀]⊕Rher[J₀].           (14)

O mesmo argumento mostra que □ é injetivo em B⁰. Isso é coerente com a injetividade086 da divergência em B³, mas a triangularidade acrescenta a descrição da imagem e de seu quociente. Não foi afirmado que □ admita inversa em todo B⁰.

Com(5),(7)–(9),(14), o complexo relativo é totalmente calculado:

| Grau p | Módulo Bᵖ | Diferencial relevante | Cohomologia |
|---|---|---|---|
| 0 | soma direta dos Iᵣ,Jᵣ | d_B isomorfo sobre B¹ | 0 |
| 1 | soma direta de d_BIᵣ,d_BJᵣ | alvo B²=0 | 0 |
| 2 | 0 | zero | 0 |
| 3 | soma direta dos q_grad Iᵣ,q_grad Jᵣ | □B⁰ν, injetivo | 0 |
| 4 | B⁰ν | alvo zero | Rher[I₀ν]⊕Rher[J₀ν] |

Assim

        Hᵖ(B,d_B)=0 para p≠4,
        H⁴(B,d_B)=Rher[I₀ν]⊕Rher[J₀ν].                  (15)

Trata-se de cohomologia relativa natural no quociente linear efetivo. Não é a cohomologia horizontal ordinária com coeficientes coordenados ampliados; a primitiva ordinária por conexão086 continua pertencendo a outra classe.

## 7. Do relativo ao CE completo invariante pela isotropia

Considere

               Cⁿ=Cⁿ(g,N₂)^h
                  =⨁_(p+q=n)(N₂⊗ΛᵖV*⊗Λᵠh*)^h.

O índice p conta ghosts de translação, q ghosts de isotropia. Escreva dCE=d_h+d_V+d_R, com bidegraus (0,1),(1,0),(2,−1). Essa é a decomposição da ação082: o último termo substitui um ghost de isotropia pela curvatura Kpp; o segundo é a derivada covariante horizontal. Não se identifica o diferencial total com d_B antes de tratar os ghosts de isotropia.

A filtração decrescente pela quantidade mínima de ghosts de translação tem somente cinco passos, p=0,…,4. Em seu graduado inicial, o diferencial é d_h. Cada expressão usa um corte finito de jatos, estável sob a isotropia. Esses cortes são módulos finitos de h; suas cisões e homotopias algébricas são finitas e naturais sob a isotropia. Não se exige que o módulo seja localmente finito sob TODA g.

[KNOWN — importação delimitada] A cohomologia de uma álgebra semissimples em um módulo finito é a cohomologia de coeficientes triviais tensorizada com os invariantes. Aplicada à isotropia, dá a primeira página abaixo. O mecanismo com primitivas finitas e as classes de Lorentz estão descritos em [BBH1995, apêndiceB, B.1–B.3, e decomposição7.17–7.23](https://arxiv.org/pdf/hep-th/9505173). Importa-se apenas esse cálculo de álgebra de Lie; não se importa a classificação não linear de característica máxima.

Para explicitar o alcance: tomar invariantes no complexo vertical também é exato nos cortes finitos semissimples. Sua ação induzida na cohomologia é trivial, pela homotopia de Cartan. Portanto restringir a cochains h-invariantes não remove as classes verticais. O cálculo passa ao limite DIRETO algébrico dos cortes, porque qualquer cociclo ou primitiva usa um corte finito. A extensão por Rher é tratada no próximo parágrafo; não se introduz uma completude topológica.

Há dois geradores reais independentes ω₃,tr e ω₃,E da cohomologia de h=so(1,3), ambos de grau três. A álgebra é exterior:

                 H*(h,R)=Λ(ω₃,tr,ω₃,E),

com graus0,3,6 de dimensões1,2,1. Pode-se verificar a contagem complexificando h para sl₂⊕sl₂ e usando as duas primitivas cúbicas; BBH fornece também a forma real de traço e de epsilon. Não se aplica Whitehead à álgebra g de Killing com coeficientes infinitos.

Assim a primeira e a segunda páginas da filtração horizontal são

       E₁^(p,q)=Bᵖ⊗Hᵠ(h,R),
       E₂^(p,q)=Hᵖ(B,d_B)⊗Hᵠ(h,R).                     (16)

O diferencial de E₁ é d_B no primeiro fator: d_V não diferencia os representantes constantes ω da isotropia, e d_R só aparece dois passos à frente. A curvatura não foi descartada; está explicitamente reservada aos diferenciais seguintes.

Por(15), E₂ tem somente a coluna p=4, nas linhas q=0,3,6. Todo diferencial posterior tem bidegrau(r,1−r), r≥2. Saindo dessa coluna ultrapassa p=4; chegando nela partiria de uma coluna que já é zero. Logo todos são zero. A filtração é finita e limitada, então converge sem questão de limite inverso:

                          E₂=E∞.                        (17)

Para cada grau total sobrevivente há somente uma peça filtrada, portanto não há problema de extensão entre colunas. Consequentemente

       Hⁿ(C(g,N₂)^h,dCE) ≅
           Rher²,  n=4;
           Rher⁴,  n=7;
           Rher²,  n=10;
           0,      nos demais graus.                    (18)

Os representantes podem ser escritos explicitamente:

- grau4: I₀ν e J₀ν;
- grau7: I₀ν·ω₃,tr, J₀ν·ω₃,tr, I₀ν·ω₃,E, J₀ν·ω₃,E;
- grau10: I₀ν·ω₃,trω₃,E e J₀ν·ω₃,trω₃,E.

Aqui ω designa o polinômio puro nos ghosts de isotropia. Os produtos escritos são ciclos do CE COMPLETO. A derivada horizontal de I₀ν ou J₀ν teria cinco ghosts de translação e é zero; a parte vertical é invariante. A variação de curvatura de ω acrescenta dois ghosts de translação, também anulados por ν. Portanto não é necessária uma série de correções para esses representantes de volume máximo. A independência e a exaustão vêm de(16–17), não apenas desse fechamento explícito.

## 8. Finitude, anel herdado e a natureza efetiva da redução

Cada etapa de geração remove um símbolo superior por combinações finitas dos representantes covariantes(2). Os espaços de símbolos são tensoriais finitos sob h; projetar no singlete ou no vetor e tomar a parte real preserva naturalidade. Nunca se escolhe um vetor temporal, um spinor externo ou uma primitiva coordenada para depois presumir que seja natural.

As relações da seção2 são suficientes para os levantamentos requeridos: para escalares há dois candidatos curvos com símbolos independentes e um limite superior de duas cópias; para uma-formas seus gradientes atingem os dois tipos vetoriais. Para duas-formas a injeção em zero basta. O cálculo não necessita de uma afirmação mais ampla sobre a liberdade de toda a torre curva.

Em(10) o maior índice cai na redução de(13). Em(16), a filtração de ghosts horizontais tem comprimento cinco. A homotopia vertical fica em um corte finito de jatos; d_V pode aumentar a ordem, mas só é usado finitamente muitas vezes na eliminação de uma cochain de ghost finito. As primitivas obtidas têm, portanto, finitos jatos. Não se trocou uma sequência de primitivas de ordens crescentes por uma primitiva de ordem infinita.

Sobre Rher, toda construção é extensão escalar de mapas reais do operador já fixado. Tensorizar sobre o corpo R é exato. As bases e injeções em cada símbolo sobrevivem; um coeficiente nilpotente não é perdido por uma suposta avaliação numérica. Na redução triangular,2 é uma unidade. As cisões verticais também são de mapas reais e podem ser tensorizadas. Não há hipótese de que Rher seja corpo, domínio, reduzida ou Noetheriana.

É importante não substituir esse contrato por Rher completado em que se permitam somas infinitas ∑aᵣIᵣ dentro de uma única expressão. Uma tal corrente pode não ter maior ordem e não está em(4). Do mesmo modo, permitir que os operadores variem com novos campos ou acrescentar tensores espectadores altera as representações e os diferenciais. O cálculo(18) não é declarado para essas categorias.

## 9. Relação com086 e limite físico

A investigação086 calculou H³ CE quadrático igual a zero e uma linha livre de Pontryagin em H⁴, além da consequência para a imagem cúbica dos truncamentos. O resultado(18) é compatível e o refina: no MESMO setor CE quadrático, H⁴ é exatamente de posto dois, com a classe escalar I₀ν e a pseudoescalar J₀ν. Seu grau três continua zero. A entrega086 permanece congelada; este refinamento087 não é retroativamente atribuído a ela.

Pela identificação082, o CE em(18) calcula a diagonal m=E−gh=2 após o primeiro diferencial induzido por s₁. Os graus4,7,10 correspondem às valências6,9,12 dessa diagonal. Diferenciais superiores do BRST completo podem mudar m e interagir com outros setores. Não foi demonstrado que todas essas classes sobrevivam na cohomologia total, nem que os demais setores sejam zero.

Não foi calculado um coeficiente de anomalia quântica de ghost um. Não se conclui QME, positividade interagente não condicional, completamento UV, reconstrução física geral ou veredito da TGL. O sigma físico não constante, a admissibilidade causal e o transporte entre fundos permanecem problemas distintos. A fase/ramo e H3 interno do programa não são reabertos por esses graus cohomológicos.

## 10. Proveniência e estado de revisão

[DERIVED] A novidade própria é a geração curva dos singletes e das uma-formas, a ausência das duas-formas, a fórmula triangular com diagonal2 e a composição finita que calcula(15) e(18). Esses elos são oferecidos à revisão independente integral.

As fontes planas usadas na086 foram [Anco–Pohjanpelto, equações2.1–2.7](https://arxiv.org/pdf/math-ph/0202019) e [Khavkine, seção3.1](https://arxiv.org/pdf/1805.03751), consultadas diretamente durante a revisão anterior. A nova consulta primária087 foi ao cálculo vertical e às primitivas reais do apêndiceB de BBH. Nenhuma dessas referências é apresentada como teorema pronto para o sistema quadrático curvo completo aqui calculado.

Recebi uma conferência estrutural curta sobre os símbolos de Iᵣ,Jᵣ e o fator2 em Leibniz; ela é compatível com a demonstração acima, mas não é uma revisão integral desta nota. Não se atribui aprovação a outro autor ou ao operador.

[REAL — documental] O manifesto mede as nove fontes antes/depois e os novos arquivos finais. O helper somente lê, calcula hashes, verifica links e publica a nota por temporário conferido. Zero matemática executada, CAS, Lean ou um.py. Nenhum original, Atlas, memória canônica, selo, gate ou documento086 foi alterado. Somente novos arquivos nesta pasta087.
