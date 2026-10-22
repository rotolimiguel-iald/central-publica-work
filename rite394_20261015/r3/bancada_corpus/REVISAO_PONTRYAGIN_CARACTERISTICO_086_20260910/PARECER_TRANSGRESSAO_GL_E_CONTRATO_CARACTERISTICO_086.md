# Revisão independente086 — transgressão GL e limite da importação característica

10/09/2026. [DERIVED — revisão matemática escrita]. [KNOWN — fontes primárias consultadas no alcance indicado]. [REAL — proveniência e preservação no recibo]. Li integralmente a nota de Turing e o manifesto. Não identifiquei erro material no resultado delimitado: a primitiva ordinária foi construída, sua invariância gauge modulo EOM foi refutada para esse representante e a pertinência à imagem da classe invariante permanece uma obrigação distinta.

Fonte revista: [Não exatidão invariante e limite BBH](<C:/IALD/Central de Patentes/Chatgpt/PONTRYAGIN_CARACTERISTICO_E_LIMITE_BBH_086_20260910_062514_4956488/NAO_EXATIDAO_INVARIANTE_E_LIMITE_DA_IMPORTACAO_BBH.md>). Esta revisão não consome resultados de outra investigação086 para decidir sua pendência.

## 1. O grau máximo realmente é hipótese adicional nas fontes

Conferi diretamente [BBH1995](https://arxiv.org/pdf/hep-th/9505173), Teorema7.1(ii)/(7.32), a passagem para(7.33), Teorema7.2 e §9/(9.8–9.9). A extensão da não trivialidade ao grau máximo é assumida separadamente. O exemplo com escalar e acoplamento à densidade característica continua normal e torna essa densidade uma divergência invariante on-shell. Portanto normalidade não paga sozinha(7.33). O §8 trata a classe equivariante especificada; não identifica automaticamente o componente quadrático do sistema Einstein linear com referência inerte à teoria completa usada ali.

[Dragon–Brandt, Teorema15/(5.73–5.74)](https://arxiv.org/pdf/1205.3293) usa o diferencial linear tensorial dφ; a expressão característica(7.42) conserva uma parcela de grau máximo. [Cnockaert–Henneaux, apêndiceA.2](https://arxiv.org/pdf/hep-th/0504169) usa a curvatura e o gauge linearizados em torno de η. Nenhum deles foi falsamente convertido, na nota revista, em um resultado de não exatidão no quociente Einstein curvo com K fixado. A necessidade de comparar objetos, diferencial, shell, grau e coeficientes é real.

Essas leituras delimitam a importação; não são um teorema bibliográfico de que toda possível rota característica falha. A nota preserva corretamente essa diferença.

## 2. Transgressão GL: torção e coeficiente quadrático

Use a MESMA identificação do fibrado tangente para as duas conexões. A=Γ(g)−Γbar é uma 1-forma End(TM), e a diferença de suas torções é A^a_b∧e0^b. Ambas são livres de torção, portanto essa expressão é zero para qualquer coframe comum. Como R0^a_b=K e0^a∧e0_b,

tr(A∧R0)=K A^a_b∧e0^b∧e0_a=0.

Não se usa A∈so(g0). A conclusão é para a diferença GL; uma mudança por S=(g0⁻¹g)^(1/2) também transporta a conexão e seu termo diferencial. A nota corretamente não reutiliza essa identidade para apagar o termo quadrático da apresentação ortogonal por homonímia.

A fórmula padrão, verificável expandindo R=R0+Dbar A+A², é

tr(R²)−tr(R0²)
=d[2tr(A R0)+tr(A Dbar A)+(2/3)tr(A³)].

Com A=tL+t²L2+... e L2=−HL, o primeiro termo é identicamente zero pela torção; A³ começa em t³. Assim a primitiva quadrática é T2=tr(L Dbar L).

Uma conferência independente dos termos de curvatura: Dbar²L=R0L−LR0, e a ciclicidade graduada fornece

d tr(L Dbar L)=tr((Dbar L)²)+2tr(R0 L²).

O coeficiente quadrático da expansão de tr(R²) é essa expressão mais 2tr(R0 Dbar L2). A parcela extra é d[2tr(L2R0)] e zera pela MESMA identidade de torção. Não foi omitido um termo de curvatura do fundo.

## 3. Identificação do alvo sem impor EOM

Para Levi-Civita, escreva R^a_b=W^a_b+e^a∧P_b−e_b∧P^a. A primeira Bianchi de W anula os termos cruzados no traço. A simetria P_ab anula o quadrado da parcela Schouten. Portanto tr(R∧R)=tr(W∧W) algebricamente, antes das EOM. Como W(g0)=0, seu coeficiente t² é tr(W1∧W1)=J_W vol0.

Isso verifica d_HT2=J_W vol0 off-shell, com a normalização da nota. Nenhuma condição de positividade, equação de onda, identificação s0=dH ou transformação dos ghosts em dx foi necessária. L usa uma derivada de h e DbarL usa até duas, logo o coeficiente é local finito.

Se os dados são globais e existe a família global admissível, T2 é global porque a diferença de conexões é tensorial. A integral do coeficiente quadrático numa variedade fechada zera por Stokes. Essa afirmação condicional não fornece um exemplo de variedade compacta com qualquer assinatura ou fundo desejado; seu papel é impedir que um número característico de outra geometria completa seja usado como detector deste coeficiente.

## 4. O defeito de gauge sobrevive no shell — avaliação explícita

Em coordenadas normais no ponto, ξ=0 e ∇barξ=0 eliminam os termos inferiores de curvatura na variação de Levi-Civita. Assim

(δξL)^a_bμ=∇bar_μ∇bar_b ξ^a.

É consistente impor também os terceiros jatos covariantes iguais a zero: seus comutadores contêm ξ ou ∇barξ, já nulos. Isso dá DbarδξL=0 no ponto. Alternativamente, DbarδξL é a variação de curvatura e a expressão de Lie no fundo zera para esses dados de ξ. Pode-se realizar esses jatos por um campo suave local; não se exige que ξ seja Killing, pois o teste é de invariância sob gauge ARBITRÁRIO.

Escolha ξ²_01=ξ²_10=1 como únicos Hessianos não nulos. Então δL²_1=dx0, δL²_0=dx1. Na componente exterior023,

(δT2)_023=(DbarL)^1_2,23.

A segunda parcela tr(L DbarδL) zera, e a parcela de δL²_0 contém dx1 e não contribui a023. O fator da duas-forma é consistente: escrever suas componentes como (1/2)Rμνdxμ∧dxν deixa o coeficiente de dx2∧dx3 igual a R23.

A solução TT de k=0 da fonte081 tem h(p0)=0 e tensor elétrico Eij=diag(E,−E,0), E=−1/(2z0), na normalização ell=z0. Faça uma rotação espacial de isotropia cujo bloco13 seja

R13 = [[cosα,−sinα],[sinα,cosα]],   α=π/4,

escolhendo a ação sobre a solução de modo que E' = R E R^T. Então E'13=E/2. Para Weyl puramente elétrico na assinatura +---,

W_ijkl=−ε_ijm ε_kln E_mn,

portanto W1223=−E'13=−E/2. Levantar o primeiro índice1 acrescenta o sinal −. No ponto, h=0 e as EOM Einstein lineares anulam a parte Ricci restante, de modo que DbarL=R1=W1. Consequentemente,

(δT2)_023=+E/2=−1/(4z0) ≠ 0.

Essa avaliação torna explícito o não zero deixado sem normalização na nota. A rotação é realizada por uma isometria da referência e conserva a solução em uma vizinhança; não presume liberdade de todos os jatos Weyl. A realização dos prolongamentos permanece a da solução TT, e não uma atribuição pontual incoerente.

Adicionar somente termos proporcionais às EOM e seus prolongamentos não corrige o defeito: H0R0=0, e a variação de cada coeficiente desses termos ainda multiplica uma EOM que zera no shell. Uma corrente ordinária FECHADA é liberdade diferente; não foi excluída por essa avaliação. Logo o teste refuta apenas a invariância de T2, não a existência de outra primitiva invariante.

## 5. A sequência curta compara os complexos corretos

A é o complexo de formas naturais de Weyl/EOM quadráticas, com coeficientes escalares inertes, realizado localmente; B contém formas quadráticas nos jatos métricos originais modulo as MESMAS EOM lineares, com coeficientes coordenados auxiliares. A inclusão Sym²M→Sym²(U/E) é a inclusão algébrica085, não uma identificação de toda a cohomologia. A naturalidade e a homogeneidade da espaço-forma realizam essa inclusão como formas locais. Ambos os diferenciais preservam o ideal prolongado.

Assim 0→A→B→B/A→0 é uma sequência curta de complexos de espaços reais. Não é necessário que A seja um submódulo de B sobre todas as funções coordenadas. Extensão inerte por Rher preserva a exatidão por planura sobre R.

Como dT2=a∈A⁴, q(T2) é fechado no quociente e a aplicação de conexão envia [q(T2)] a [a]. Se a=dV em A, T2−V é fechado em B. Reciprocamente, se q(T2−j)=dq(U) com dj=0, então V=T2−j−dU∈A e dV=a. Os sinais da fórmula e o grau de U, igual a dois, conferem.

O critério(10) é, portanto, necessário e suficiente. Ele não foi apresentado como uma solução da imagem de H³(B). KT/Hchar de grau zero085 não a calcula. Naturalidade de T2 sob transporte simultâneo de(g0,h) também não implica invariância sob a transformação ativa de h mantendo g0 inerte.

## 6. Os contraexemplos de transporte são válidos e delimitados

No complexo formal db=a+t c, a seria fronteira apenas se a=f(a+t c), o que obriga simultaneamente f=1 e t=0. Logo sua classe é não nula; no diferencial inicial, porém, a=d0b. Multiplicar por t² conserva o fenômeno num líder de ordem dois. A fonte não conclui daqui que uma classe particular de Einstein tenha esse comportamento.

No segundo complexo db=K a, a não é exato após K=0, mas é exato em cada fibra real k0≠0, com primitiva b/k0. Isso demonstra a insuficiência de especializar cegamente uma alegação ao limite plano. No domínio fixado, 1/k0 é um real; num anel polinomial universal restrito ele não foi acrescentado por decreto.

Esses controles lógicos não refutam uma comparação por SÍMBOLO principal que prove estriteza e controle de ordens. A nota explicitamente deixa essa rota aberta. Sua advertência é contra trocar a prova da comparação por uma analogia entre fundos.

## 7. Parecer e custódia

Parecer favorável no escopo declarado: fórmula ordinária off-shell, defeito gauge on-shell para o representante T2, sequência curta e limites das importações. Não é parecer de inexistência geral de corrente, anomalia efetiva, QME, UV ou fechamento físico. Os resultados085 permanecem intactos, e a investigação086 por símbolo geral é independente desta nota.

Este revisor é autor do antecedente GL–ortogonal079; reapreciou aqui diretamente a transgressão ordinária e a nova avaliação de gauge de Turing. A identidade BRST079 não foi usada como aprovação automática desta nova prova. Os demais antecedentes foram consultados nas partes necessárias, aproveitando leituras anteriores já registradas.

O manifesto de origem tem16 controles documentais, não16 provas matemáticas. Seu helper foi pinado como proveniência, sem execução nem alegação de auditoria integral de código. Os PDFs primários foram consultados pela web e não receberam hashes locais inventados. O recibo desta revisão mede os arquivos efetivamente alcançados pelos pins antes/depois; zero execução matemática, CAS, Lean ou um.py. Somente novos arquivos nesta pasta Chatgpt.
