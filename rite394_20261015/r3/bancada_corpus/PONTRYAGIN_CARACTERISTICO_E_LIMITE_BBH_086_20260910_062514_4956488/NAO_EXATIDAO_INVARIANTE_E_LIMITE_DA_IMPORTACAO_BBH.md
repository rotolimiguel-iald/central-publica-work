# Pontryagin quadrático: exatidão ordinária e limite da importação cohomológica

10/09/2026. Investigação086 nova, excluída da consolidação085. [DERIVED — demonstração escrita e comparação de classes]. [KNOWN — referências primárias no alcance explicitado]. Zero CAS, Lean ou execução/importação de um.py. Fontes anteriores somente leitura.

**Resultado delimitado.** A não exatidão invariante de Pontryagin em grau quatro NÃO pode ser importada automaticamente dos teoremas examinados. O grau máximo é uma hipótese adicional na referência BBH1995, e nosso componente quadrático vive num complexo diferente daquele da teoria não linear sem referência espectadora. Além disso, no MESMO fundo desta investigação existe uma primitiva ordinária finita explícita:

                d_H T2 = J_W vol0,
                T2 = tr(L ∧ Dbar L),                      (1)

onde L é a variação de Levi-Civita. Ela é natural no par(g0,h), mas não é uma corrente gauge-invariante formada apenas por Weyl/jatos, nem mesmo modulo as EOM lineares. Demonstro essa distinção abaixo.

Não decidi se OUTRA corrente V, natural quadrática nos jatos Weyl/EOM finitos, satisfaz J_W=div V. O contrato restante é formulado precisamente por uma aplicação de conexão entre dois complexos, em(10). Os contraexemplos algébricos do §6 mostram por que não trivialidade não linear ou no limite plano não substituem esse contrato.

## 1. O problema exato preservado

Usamos a [redução084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>) e a [nulidade dos invariantes085](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>) como antecedentes escritos distintos. A referência é espaço-forma Lorentziana orientada, dimensão quatro, K>0 real fixo, κ não nulo fixo, setor métrico projetado com φ0 constante e coeficientes escalares inertes Rher. Cada elemento tem ordem finita de jatos. Mcal continua sendo o quociente linear Weyl/EOM, não uma torre livre.

Ponha N=Rher⊗Sym²Mcal. O complexo horizontal relativo relevante é

 A^p = (N⊗Λ^p V0*)^h,    d_A=d_rel,
 h=so(1,3),  p=0,…,4.                                   (2)

Sua realização por formas naturais ordinárias usa o coframe/volume de g0. A [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) inclui as relações dos jatos e a ação das transvecções. A questão é exatamente

                   [J_W vol0] ?= 0 em H⁴(A,d_A).          (3)

Não é H⁰ característico, não é toda H³ do CE invariante e não é cohomologia ordinária de de Rham de uma variedade. A conclusão N^g=0 de085 retira o coeficiente quadrático do canal Euler084; ela não anula H⁴(A).

## 2. O que as fontes primárias permitem, e o que não permitem

[KNOWN] [BBH1995, Teorema7.1(ii), (7.32), (7.33), Teorema7.2 e §8](https://arxiv.org/pdf/hep-th/9505173v2): a não trivialidade característica demonstrada tem restrição de grau. Em grau máximo, (7.33) é uma hipótese adicional. O Teorema7.2 a assume expressamente. A classe equivariante de §8 exige formas covariantes, sem ghosts, antifields ou dependência explícita das coordenadas. O exemplo(9.8–9.9), com um escalar acoplado a uma densidade característica, mostra uma classe máxima tornando-se divergência invariante on-shell apesar de a teoria continuar normal. Portanto normalidade/irreducibilidade não implica por si a hipótese máxima. Li os enunciados e esse exemplo diretamente no PDF.

A comparação com(3) tem três obrigações independentes:

1. **Grau.** Aqui a forma tem grau quatro numa teoria quadridimensional. Um teorema de não trivialidade apenas abaixo desse grau não alcança o alvo. Inserir uma hipótese de não exatidão máxima idêntica a(3) seria circular.
2. **Objeto dinâmico.** Nosso sistema é estritamente linear em h sobre g0 fixado e nosso alvo é o coeficiente quadrático de Weyl. Não identificamos esse coeficiente com a classe característica da teoria completa sem um teorema de comparação que preserve a não trivialidade.
3. **Álgebra.** Nosso uso da referência inerte permite diferenças tensorais de conexões no ambiente auxiliar. Covariância sob mudanças simultâneas de apresentação de(g0,h) e invariância sob o gauge ativo h→h+Lieξg0 são condições distintas. A segunda, satisfeita por W1 e seus jatos, é indispensável em(2).

[KNOWN] Examinei também [Dragon–Brandt2012, Teorema15, (5.73–5.74), e §7.3, (7.42)](https://arxiv.org/pdf/1205.3293). O resultado linear de formas tensoriais usa o diferencial e as variáveis ali definidos sem impor o shell Einstein curvo de(2). A discussão característica mantém o setor de grau máximo. A palavra “linearizado” no título do lema não fornece a comparação de módulos e de relações exigida aqui.

[KNOWN] [Cnockaert–Henneaux2005, (1.7), (1.14) e apêndiceA.2](https://arxiv.org/pdf/hep-th/0504169) trabalha a expansão em torno de η, com γ0h=∂C+∂C e curvatura linearizada plana. O lema covariante citado ali não é um cálculo do quociente on-shell Einstein em K>0 fixo. Sua prova separa contagens de derivadas que não se conservam literalmente sob comutadores curvos. Nenhum teorema desse artigo é aqui aplicado para concluir(3).

O fato de a álgebra das transformações de h ser abelianizada não a transforma, por homonímia, num conjunto dos “fatores abelianos livres” de Yang–Mills. Essa expressão não elimina a obrigação de comparar os campos, operadores e classes efetivamente usados.

## 3. Primitiva ordinária explícita no mesmo fundo

Trabalhe localmente com g(t)=g0+t h e denote por

 A(t)=Γ(g(t))−Γbar=tL+t²L2+O(t³),
 L^a_bμ=½g0^ad(∇bar_b h_dμ+∇bar_μ h_db−∇bar_d h_bμ).

A é uma 1-forma End(TM). O parâmetro t é apenas formal. O coeficiente L2=−HL, H=g0⁻¹h, e a corrente tr(L∧DbarL) já aparecem na [comparação GL–ortogonal079](<C:/IALD/Central de Patentes/Chatgpt/COMPLETAMENTO_GL_ORTOGONAL_079_20260910/CORRENTE_QUADRATICA_E_EQUIVALENCIA_DAS_CONEXOES.md>). Aqui extraímos sua consequência para a forma ordinária, sem identificar os ghosts com dx.

As duas conexões de Levi-Civita são livres de torção. Para qualquer coframe de referência e0,

 A^a_b∧e0^b=0,  R0^a_b=K e0^a∧e0_b,
                  tr(A∧R0)=0.                            (4)

A última igualdade segue da primeira: tr(A R0)=K A^a_b∧e0^b∧e0_a. Em particular tr(L2 R0)=0. Não se presumiu que A seja g0-antissimétrica; esta é a apresentação GL da diferença das conexões.

Uma expansão direta de R(t)=R0+Dbar A+A², com Dbar R0=0 e ciclicidade graduada, fornece

 tr(R(t)∧R(t))−tr(R0∧R0)
 =d_H[2tr(A∧R0)+tr(A∧Dbar A)+(2/3)tr(A³)].               (5)

Por(4), o coeficiente de t² da primitiva é exatamente T2=tr(L∧DbarL). O termo cúbico começa em t³. Isso não é uma escolha de Chern–Simons de uma conexão nua: a diferença A transforma tensorialmente quando ambas as conexões são transportadas.

Para uma conexão de Levi-Civita, a decomposição R=W+e∧P em Weyl e Schouten dá

                     tr(R∧R)=tr(W∧W).                    (6)

Pode-se conferir(6) algebricamente: os termos cruzados usam a Bianchi W^a_b∧e^b=0; o quadrado da parcela Schouten zera pela simetria de P_ab e pela antissimetria exterior. Esta identidade independe das equações Einstein. Como W(g0)=0,

 W(g(t))=tW1+O(t²),
 [t²]tr(R(t)²)=tr(W1∧W1)=J_W vol0.

Extrair t² em(5) prova(1) **off-shell**. Os objetos são finitos: L usa uma derivada de h, DbarL no máximo duas, e a diferenciação de T2 permanece local. Não há inversa diferencial ou série infinita de jatos dentro do coeficiente.

**Precisão de apresentação.** Se antes se transporta a conexão por S=(g0⁻¹g)^(1/2), sua diferença em so(g0) não é a mesma A. A transgressão quadrática transportada pode conter 2tr(a2R0). A identidade de torção(4) é da diferença GL no coframe fixo; não autoriza apagar esse termo na apresentação transportada. As duas expressões devem ser relacionadas por seu transporte, não por homonímia. A prova acima usa somente GL.

## 4. Por que T2 não é uma corrente admitida em(2)

O campo W1 é invariante sob δξh=Lieξg0 porque W(g0)=0. Já L se transforma com segundas derivadas do parâmetro. Em coordenadas normais no ponto, se ξ e ∇barξ são zero,

                  (δξL)^a_bμ=∇bar_μ∇bar_b ξ^a.            (7)

Se também os terceiros jatos covariantes de ξ forem zero, DbarδξL=0 nesse ponto. Essas escolhas de jatos são compatíveis: os comutadores dos segundos/terceiros jatos dependem de ξ e de seus primeiros jatos, que foram postos a zero.

Escolha somente os Hessianos simétricos ∇bar_0∇bar_1 ξ²=∇bar_1∇bar_0 ξ²=1 não nulos. Então δξL²_1=dx0 e δξL²_0=dx1. A variação

 δξT2=tr(δξL∧DbarL)+tr(L∧DbarδξL)

tem, no ponto, componente023 igual a (DbarL)^1_223. Pode-se torná-la não nula mesmo no shell linear, sem presumir que todos os jatos Weyl sejam livres:

- Use a [solução TT081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>) com k=0, f(z0)=0, f′(z0)=1. Ela tem h(p0)=0 e parte elétrica de Weyl não nula, proporcional a diag(E,−E,0), E≠0.
- Uma rotação da isotropia espacial que mistura os eixos1 e3 produz uma componente elétrica13 não nula. Pela identidade algébrica da parte espacial de um Weyl sem Ricci, W1223 é essa componente a menos de um sinal, portanto também não nula.
- A transformação da solução pela isometria da referência conserva as EOM em uma vizinhança e h(p0)=0. Nesse ponto DbarL=R1=W1: as parcelas Ricci lineares e as parcelas proporcionais a h(p0) desaparecem.

Assim δξT2 não é zero em uma solução linear efetiva. Não se trata de um teste que pretenda separar todas as classes: basta uma solução para mostrar que esta corrente particular NÃO é gauge-invariante modulo EOM. A variação de uma expressão proporcional às EOM e seus prolongamentos também zera on-shell, pois H0R0=0. Logo acrescentar somente termos desse ideal a T2 não remove o defeito exibido.

Isso não demonstra que T2 seja impossível de melhorar por uma **corrente ordinária fechada**. Essa liberdade é exatamente a que permanece em(10) abaixo. A primitiva ordinária(1) não resolve a busca de uma primitiva em A.

Também explica o limite de uma prova global por números característicos. Se g0 e h são globais numa variedade fechada e a família g(t) é admissível, T2 é global, pois L é uma diferença tensorial. Portanto ∫J_W vol0=∫dT2=0. Um número de Pontryagin não nulo de OUTRA geometria completa não separa esse coeficiente quadrático. A variação do número de Euler também é zero; ela não deve ser identificada automaticamente com o alvo Pontryagin quadrático nem com uma classe em(2).

## 5. O contrato restante como aplicação de conexão

Há uma formulação algébrica exata que evita trocar classes. Realize A por suas formas locais naturais quadráticas, modulo o ideal LINEAR das EOM. Seja B o complexo maior de formas locais quadráticas nos jatos originais de h, modulo o mesmo ideal, permitindo coeficientes suaves em x numa carta. As formas de A injetam em B pela inclusão Sym²Mcal→Sym²(U/E), já paga085. A derivada preserva ambos os espaços e o ideal. Trabalhamos com elementos finitos; nenhuma completação adicional é necessária.

Temos a sequência curta de complexos reais, também válida após extensão por Rher,

             0 → A → B → B/A → 0.                         (8)

Como d_HT2=a, a=J_W vol0∈A⁴, a imagem q(T2) é um ciclo de grau três em B/A. A aplicação de conexão da sequência(8) satisfaz

              ∂[q(T2)]=[a] em H⁴(A).                     (9)

Em particular, a questão procurada é equivalente ao contrato concreto

 [a]=0 em H⁴(A)
 ⇔ [q(T2)] pertence à imagem de H³(B)→H³(B/A).             (10)

Prova direta: se a=dV com V∈A³, então T2−V é fechado em B e sua imagem representa [q(T2)]. Reciprocamente, se existe j∈B³ fechado e U∈B² tais que q(T2−j)=dq(U), então V=T2−j−dU pertence a A³ e satisfaz dV=a. As mesmas igualdades valem modulo as EOM já incorporadas aos dois complexos.

O problema não é a existência de uma primitiva em B: ela já foi dada por(1). É saber se sua classe no quociente B/A pode ser removida por uma corrente ordinária conservada. KT linear e H⁰ característico085 não calculam essa imagem de grau três. O uso auxiliar de B não promove suas correntes a A nem presume uma covariantização automática.

Assim uma prova por não exatidão característica deve pagar precisamente que [q(T2)] NÃO está nessa imagem, ou um teorema equivalente de não trivialidade de [a] no complexo(2), com K fixo e shell linear. A afirmação não pode entrar como hipótese silenciosa de uma aplicação de BBH.

## 6. Duas inferências de especialização que são falsas em geral

Estes são controles algébricos de lógica, não modelos físicos substitutos.

**Não trivialidade completa não implica não trivialidade do líder.** Considere um complexo sobre R[[t]], com C³=R[[t]]b e C⁴=R[[t]]a⊕R[[t]]c, diferencial db=a+t c e diferencial seguinte zero. A classe [a]=−t[c] é não nula no complexo completo: se a=f(t)(a+t c), a comparação da componente a impõe f=1, e a componente c seria t=0. Porém, no diferencial inicial d0, temos a=d0b. Multiplicar tudo por t² coloca o mesmo exemplo a partir de um líder quadrático. Uma classe completa não trivial pode começar por uma fronteira do complexo linear.

**Não trivialidade plana não implica não trivialidade em K fixo não nulo.** Sobre R[K], tome C³=R[K]b, C⁴=R[K]a e db=K a. Na especialização K=0, a não é fronteira. Em qualquer especialização real K=k0≠0, a=d(b/k0). Não há paradoxo: a categoria de coeficientes mudou na especialização, e 1/k0 é um real permitido.

Esses exemplos não afirmam que a nossa densidade seja exata. Demonstram que seriam inválidas, sem contrato adicional, as inferências usadas para transportá-la. Em nossa categoria K é fixo antes de estender por Rher; coeficientes reais como K⁻¹ estão disponíveis. Portanto uma estratégia por K→0 precisa de controle real de filtragem, símbolos e relações, e não pode simplesmente avaliar no plano uma identidade cuja primitiva só exista após essa especialização.

Nilpotentes de Rher não são testados por valores numéricos nesses argumentos. As construções são sobre o corpo real ou sobre o anel explicitamente declarado; a extensão escalar inerte usa as mesmas igualdades. Também não se supõe que as avaliações TT separem N.

## 7. Consequência prática e limite desta investigação

[DERIVED] Foi pago um limite preciso da rota bibliográfica: os enunciados examinados não fornecem a não exatidão pretendida sem uma nova comparação no grau máximo e no módulo linear curvo. A fórmula(1), a diferença de gauge do §4 e o critério(10) mostram onde uma prova legítima teria de atuar.

[OPEN] A existência de V em(3) continua sem decisão nesta nota. A [exclusão084 do múltiplo de gradiente](<C:/IALD/Central de Patentes/Chatgpt/CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md>) permanece válida e delimitada; não é convertida numa classificação de todas as ordens. Uma prova por símbolos curvos ou por correntes conservadas pode atacar(10), mas seus lemas de liberdade/filtragem precisam ser demonstrados, não inferidos da geração de Weyl080.

Não há aqui uma afirmação de anomalia efetiva, cancelamento do resíduo, QME, UV ou reconstrução geral. A regularidade e os resultados085 ficam intactos; apenas não são estendidos do grau zero ao grau quatro. Outras investigações086 correm separadamente e não são consumidas como se já estivessem provadas nesta fonte.

[REAL — custódia] O manifesto mede sete fontes locais antes/depois, a nota final e o helper documental. Os controles são de bytes, links e preservação, não testes matemáticos. As referências primárias foram lidas pela ferramenta web; não lhes foi atribuído hash de PDF não medido. Duas URLs versionadas devolveram falha de cache; as respectivas URLs arXiv sem sufixo foram então lidas com sucesso. Nenhuma falha de consulta foi tratada como prova. Todos os arquivos são novos em Chatgpt, sem modificar originais, fontes congeladas ou a entrega085.
