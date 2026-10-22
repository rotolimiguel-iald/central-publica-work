[DERIVED / INPUT / KNOWN / OPEN] CONTINUAÇÃO 021 — entropia relativa e a ordem necessária à ponte gravitacional

06/09/2026. Derivação anterior ao código. A etapa 020 foi progresso: auditor reconferiu 591 hashes, sete módulos limpos, 48 teoremas e seis definições impressas. O túnel contém apenas ordens 001–007. A reconstrução de 020 ainda depende de Clausius; o objetivo amplo permanece ativo.

## O problema preciso

A primeira lei diagonal já formalizada dá igualdade de DERIVADAS em relação à perturbação do estado. A construção geométrica exige que um resíduo dividido por t² tenda a zero. É necessário controlar a entropia relativa nessa ordem, e não identificar sem prova o parâmetro de perturbação do estado com o parâmetro afim da curva.

O alvo é a face finita COMUTATIVA dos estados, ligada aos pesos towerW já existentes. Não se promete uma prova de entropia relativa para operadores não comutantes ou álgebras tipo III.

## Derivação

Para p_i>0, Σp_i=1 e pesos r_i, definir

    K_p(r)=Σ_i (r_i−p_i)(−log p_i),
    D(r||p)=Σ_i r_i(log r_i−log p_i),
    F_p(q)=Σ_i q_i²/p_i.

A identidade D=K_p(r)−[S(r)−S(p)] é algébrica. Para uma curva local normalizada r(t), com r(0)=p, derivada q(t) contínua em zero e q=q(0), a positividade vale perto de zero. Derivar o traço dá Σq_i(t)=0. Então

    dD/dt=Σ_i q_i(t)[log r_i(t)−log p_i],
    [log r_i(t)−log p_i]/t → q_i/p_i,
    D(r(t)||p)/t² → F_p(q)/2.

F_p(q)≥0, com igualdade exatamente quando q=0. Logo a primeira lei não zera automaticamente o resíduo de segunda ordem: para p=(1/2,1/2) e r(t)=p+t(1,−1), a primeira variação de S e de K é zero, mas D/t²→2.

Uma resposta quadrática r(t)=p+t²q, Σq=0, tem derivada inicial zero. A mesma prova deverá dar D/t²→0, K_p(r(t))/t²=Σq_i(−log p_i) para t≠0 e a mesma expansão quadrática de S. A positividade é somente local, provada; não se chamam de estados físicos os pesos negativos que a extensão polinomial possa ter longe de zero.

## Composição com a geometria construída

Para a área A e o calor Q de 020, c=rate/(2π), definir os DOIS erros de identificação:

    E_heat(t)=Q(t)−c K_p(r(t)),
    E_area(t)=[S(r(t))−S(p)]−η[A(t)−A(0)].

O resíduo B(t)=Q(t)−cη[A(t)−A(0)] satisfaz exatamente

    B=E_heat+cD+cE_area.

Sob E_heat/t²→0 e E_area/t²→0, resulta B/t²→rate F_p(q)/(4π). Para rate≠0, Clausius na segunda ordem é equivalente a q=0. Para a resposta quadrática, q(0)=0 é construído e Clausius segue dos dois erros de identificação. A reconstrução tensorial poderá então receber essas identificações explícitas, em vez de uma hipótese de Clausius sem decomposição.

Comparando o coeficiente geométrico já provado em 020, as identificações gerais impõem

    η Ric_p(v,v)=2π T_p(v,v)+F_p(q).

Isso é uma compatibilidade CONDICIONAL entre os dados, não uma correção física de Einstein já derivada. Não se assume que esse termo define um tensor covariante conservado ou um campo gravitacional.

## Literatura e fronteira de importação

[KNOWN] Jacobson 1995 parte da relação entropia–área e de Clausius para os horizontes locais. Fonte primária consultada: https://arxiv.org/abs/gr-qc/9504004.

[KNOWN] Jacobson 2016 trata de equilíbrio de entrelaçamento com hipóteses sobre o vácuo, volume fixo e primeira variação; o caso não conforme inclui uma conjectura. Fonte: https://arxiv.org/abs/1505.04753.

[KNOWN] Lashkari e Van Raamsdonk relacionam o termo quadrático de entropia relativa à informação de Fisher e, em AdS/CFT sob hipóteses próprias, à energia canônica. Fonte primária, seção 2.1 e introdução: https://arxiv.org/html/1508.00897v2. Essa identificação holográfica não é transferida à torre por nome.

[OPEN] Identificar a curva de estados com uma evolução física e com o parâmetro geométrico, pagar os dois erros de identificação a partir do modelo microscópico, estender a álgebra diagonal, construir o horizonte e a área espacial integrada, obter origem modular da solda e globalização. Uma escolha r(t)=p+t²q é matematicamente disponível; sua relevância física não é demonstrada pela reparametrização.

Toda escrita apenas em Chatgpt; originais e entregas anteriores imutáveis. Auditoria independente reservada à gerência. Nenhuma alteração de gate.
