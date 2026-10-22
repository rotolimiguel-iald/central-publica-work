[DERIVED / INPUT / OPEN] CONTINUAÇÃO 023 — resposta direcional coerente, matéria e conservação

06/09/2026. Derivação anterior ao código. A etapa 022 foi progresso: auditor reconferiu 649 hashes, sete módulos limpos, 73 teoremas e duas definições impressas. O túnel contém ordens 001–007; o objetivo amplo permanece ativo.

## Alvo

A etapa 022 permite parâmetros escolhidos separadamente em cada tela. Construir agora uma família comum: eixo a,b e amplitudes u,v fixos, e frequência em cada ponto/direção dada pela avaliação de UM campo de covetores w. A resposta deve definir um tensor quadrático, e a identificação calor–modular deve ser testada com esse tensor em todas as direções nulas.

Não será afirmado que essa família é a dinâmica canônica do acervo, nem que ela cobre todo tensor de matéria. Com um único covetor, o gerador direcional é degenerado: direções no núcleo de w produzem frequência zero.

## Derivação

Dados a²+b²=1, u,v>0, u²+v²=1 e um campo de covetores w_mu(x), definir:

    ell_x(v)=sum_mu w_mu(x) v^mu,
    H_x(v)=ell_x(v) M, M=[[a,b],[b,-a]],
    U_x(v,t)=pairFlow(a,b,ell_x(v),t).

Como a frequência é linear na direção, o Hamiltoniano é linear, e os fluxos obedecem à composição U_x(v+z,t)=U_x(v,t)U_x(z,t). Isso é coerência algébrica em cada ponto; não identifica uma translação geométrica ou uma rede de álgebras.

Pela etapa 022:

    L_x(v)=L0 ell_x(v)^2,
    L0=transferCoefficient(a,b,u,v) log(v²/u²).

Aqui u,v nas amplitudes são números; os vetores geométricos serão nomeados direction no código. A matriz da resposta é L0 w⊗w, simétrica. Sua transformação por mudança de base deve concordar com a transformação de um covetor.

Definir coupling kappa=-L0/pi. No controle negativo de 022, kappa>0. Uma extensão tensorial que tem as contrações nulas exigidas é:

    T_mu nu = kappa [w_mu w_nu - (1/2)g_mu nu q],
    q=gInv^{ab} w_a w_b.

A escolha do termo de traço é INPUT até sua análise de conservação. Em vetores nulos:

    T(direction,direction)=kappa ell(direction)^2,
    L(direction)=-pi T(direction,direction).

Comparando os limites efetivos do calor de 020 e da energia modular de 022, o erro calor–modular/t² deve tender a zero para esse T. A normalização de T é escolhida para essa correspondência; sua unidade física e sua identificação como matéria permanecem INPUT.

## Conservação, calculada

Seja W_i j=partial_i w_j-sum_k Gamma_i^k_j w_k. Definir div(w)=sum_ik gInv^{ik} W_i k.

Sob compatibilidade métrica e inversa efetiva, calcular a derivada de q e a divergência do tensor acima. A identidade geral esperada é:

    div(T)_j = kappa [div(w) w_j
                + sum_ik gInv^{ik} w_k (W_i j-W_j i)].

Para covetor fechado e conexão sem torção, W é simétrico. Então:

    div(T)_j = kappa div(w) w_j.

Logo div(w)=0 é suficiente para conservação. Quando kappa≠0 e w(x)≠0, é também necessário no ponto. O código não deve receber conservação como substituta dessa demonstração.

Caso potencial: w=dphi para phi suave. As derivadas parciais comutam, fornecendo fechamento; a condição div(w)=0 é a equação de onda covariante. Ela é uma hipótese dinâmica, ainda não deduzida da evolução unitária finita.

A forma do tensor escalar e a dependência da conservação nas equações de movimento são conhecidas na literatura: Carroll, Lecture Notes on General Relativity, capítulo 1, equações (1.112)–(1.113), e capítulo 4 para covariantização. Aqui a identidade será verificada no cálculo da própria bancada, e não importada por citação.

## Ambiguidade de traço e Einstein

Qualquer outro tensor simétrico com as mesmas contrações nulas difere por f(x)g. Se ambos forem conservados e o domínio for preconexo, o resultado anterior da bancada força f constante. Tentar tipar essa unicidade sob conservação, mantendo os antecedentes visíveis.

O erro entropia–área tem coeficiente:

    L_x(direction)+(eta/2)Ric_x(direction,direction).

Portanto sua anulação equivale ao balanço nulo de Einstein para T. É essencial registrar essa equivalência: renomear Einstein como erro pequeno não demonstra a origem física da lei entropia–área.

Com o erro de área como hipótese e a conservação calculada sob fechamento/onda, aplicar a reconstrução geral existente. Não afirmar fechamento incondicional.

## Controles

1. Vácuo dinâmico degenerado w=0: resposta e tensor zero.
2. Plano, w=e0 constante, controle negativo de 022: tensor não nulo, simétrico, conservado; correspondência calor–modular satisfeita, mas erro entropia–área não nulo. Demonstra que pagar um erro não paga o outro.
3. Plano, w=x0 e0 (gradiente de phi=x0²/2): W simétrico, div(w)=1, divergência de T=kappa x0 e0; em x0=1 não se conserva. Unitariedade e coerência direcional não implicam a equação de onda.

## Limites e custódia

Permanecem INPUT/OPEN a seleção do covetor/potencial, sua equação de onda a partir do acervo, normalização física do tensor, parâmetro afim, entropia–área, coerência entre regiões e andares, origem modular de dimensão/assinatura/solda, limite tipo III e globalização.

Escritas apenas em Chatgpt; originais, entregas anteriores, um.py, kernel canônico, Atlas, memórias e gate intocados. Backups de bytes antes de revisar artefatos próprios. Nenhum novo juízo de confirmação física.
