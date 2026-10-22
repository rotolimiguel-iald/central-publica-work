# Classes de Euler e Pontryagin on-shell: uma prova no setor covariante algébrico

09/09/2026. Adendo novo à nota BV do arco 068. [DERIVED — demonstração escrita, sem Lean]. A nota anterior permanece intacta.

**Resultado:** para Einstein com Λ>0 e escalares minimamente acoplados, nenhuma combinação não nula das 4-formas características de Euler e Pontryagin admite um certificado de exatidão covariante modulo o ideal diferencial das equações de movimento, na classe natural algébrica definida abaixo. A prova usa métricas Einstein compactas em S⁴ e CP², mas não presume que esses espaços admitam métricas lorentzianas. A passagem de assinatura e a globalidade da primitiva são demonstradas para a classe escolhida.

**Limite:** isto paga a obstrução característica específica da condição C0/(7.33) nesse setor e nessa apresentação do ideal. A aplicação completa da classificação BRST ainda requer a resolução local/regularidade que identifica igualdade fraca com o ideal utilizado, além dos demais contratos da nota BV. Não se afirma ausência irrestrita de todas as anomalias do sigma global.

## 1. A questão exata em BBH

[KNOWN] A condição (7.33) de [Barnich–Brandt–Henneaux 1995](https://arxiv.org/pdf/hep-th/9505173) exige não trivialidade on-shell das classes características de grau máximo na cohomologia equivariante. O artigo a mantém como hipótese e explica no §9 por que é razoável para a ação padrão; isso não é uma demonstração específica somente pela ausência do acoplamento axion.

A distinção entre suas álgebras é decisiva: em (3.19)–(3.20), A₂ é polinomial nos tensores covariantes, antifields covariantes e ghosts não diferenciados. A dependência suave arbitrária no vielbein pertence a A₁. A tradução (8.4)–(8.8) de uma primitiva equivariante é

\[
\beta=\frac1{3!}e^a\wedge e^b\wedge e^c\,\beta_{abc}(T),
\tag{1.1}
\]

com transformação tensorial que torna β invariante de referencial; nela Dβ=dβ. Isso identifica o setor relevante para testar (7.33), sem transferir automaticamente resultados sobre todo A₁.

## 2. Classe admissível e certificado que será excluído

[INPUT — escolha precisa do complexo de contra-termos] As formas são naturais sob difeomorfismos orientados e mudanças locais de referencial. Seus componentes se obtêm por um número finito de operações tensorais em g, g⁻¹, volume orientado, curvatura, derivadas covariantes da curvatura, campos escalares e seus jatos. São polinomiais nos jatos diferenciados. Podem ter coeficientes suaves nos escalares sem derivadas, regulares em ao menos um valor constante y₀ admissível.

Em coordenadas de vielbein, a dependência métrica é racional, com denominadores apenas potências de det e; constantes não nulas como κ podem ser invertidas. Não são permitidos denominadores em ∂y, em invariantes de curvatura que possam zerar nos testes, funções arbitrárias dos componentes do vielbein, referencial preferido, coordenadas externas ou primitivas de Chern–Simons que não sejam tensoriais. É a classe natural algébrica usada nesta demonstração, não uma afirmação sobre qualquer classe concebível de funcionais locais.

Para a referência da nota BV, ponha

\[
\mathcal E_g=G+\Lambda g-\kappa T_{\rm scalar},\qquad
\mathcal E_y=\Box_g y,
\quad \Lambda>0.
\]

Os fatores não nulos que relacionam essas expressões às derivadas funcionais densitizadas não alteram o ideal. O ideal diferencial \(\mathcal I_{\rm EOM}\) contém somas finitas de contrações dos jatos \(\nabla^I\mathcal E_g,\nabla^I\mathcal E_y\), com coeficientes na classe acima.

Sejam E₄ e P₄ as formas características lorentzianas correspondentes ao Pfaffiano e ao traço quadrático da curvatura. Queremos excluir, salvo A=B=0, a identidade universal

\[
A E_4+B P_4=d\beta+
\sum_I\langle U_I,\nabla^I\mathcal E_g\rangle
+\sum_J\langle V_J,\nabla^J\mathcal E_y\rangle.
\tag{2.1}
\]

Todas as parcelas têm grau de forma quatro e os coeficientes A,B são constantes. A identidade (2.1) é **off-shell**: os termos de EOM mostram como a igualdade se torna exatidão quando se passa ao quociente pelo ideal. Não se presume que uma identidade que vale só nos jatos de uma solução particular se estenda a todos os campos.

Essa formulação evita uma dificuldade desnecessária: não precisamos provar que os jatos lorentzianos de soluções Einstein são densos em uma variedade complexa de soluções. A identidade a complexificar é uma identidade racional nos jatos **livres**, antes de impor as equações.

## 3. Complexificação demonstrada para o certificado

**[DERIVED] Lema.** Uma identidade da forma (2.1), na classe definida, que vale para todo jato real lorentziano com det e>0 e para todos os campos admissíveis, possui uma extensão racional aos jatos complexos não degenerados. Após fixar y=y₀ e todas suas derivadas iguais a zero, pode ser avaliada em jatos de métricas riemannianas.

**Prova.** Primeiro restrinja a identidade a y₀ constante. Coeficientes suaves em y tornam-se números; seus termos diferenciados que contêm dy desaparecem. Ainda se trata de uma identidade off-shell para a métrica, que pode ser qualquer métrica lorentziana. Escolha uma ordem de jato suficientemente grande para conter todas as parcelas.

Escreva g=eᵀηe, η=diag(1,−1,−1,−1), com e e seus jatos como variáveis. O volume orientado é representado por det e, evitando introduzir uma função |det g| sem definição holomorfa. Inversas de e, conexões de Levi-Civita e todos os jatos envolvidos são racionais nessas variáveis. Multiplicar por uma potência suficiente de det e transforma cada componente de (2.1) em uma identidade polinomial.

Os jatos reais com det e>0 formam um aberto não vazio do espaço real de variáveis independentes. Um polinômio complexo que se anula nesse aberto tem todos os coeficientes nulos. Portanto a identidade vale para todos os jatos complexos, e a identidade racional original vale onde det e≠0.

Para um coframe riemanniano real e_R, tome T=diag(1,i,i,i). Temos TᵀηT=I e det T=−i≠0. A substituição e_L=T e_R representa g_R=e_Rᵀe_R no prolongamento complexo da expressão lorentziana. Como T é constante, prolonga-se da mesma forma a todos os jatos. As equações Einstein complexificadas continuam sendo G+Λg=0, com o mesmo Λ, e admitem assim a avaliação g=g_R. Não é necessário produzir uma métrica lorentziana global em S⁴ ou CP². □

**Normalizações características.** A conjugação induzida por T é um isomorfismo entre as álgebras complexificadas so(1,3) e so(4). Ela induz uma mudança invertível de base no espaço bidimensional dos polinômios invariantes quadráticos. O traço quadrático é preservado por conjugação; o Pfaffiano pode adquirir um fator complexo não nulo conforme a convenção de volume. Assim os coeficientes A,B se tornam A′,B′ por uma transformação linear invertível. Não é necessário escolher a fase desse fator para provar que A=B=0; seria errado presumir, sem convenção, que todas as normalizações reais se mantêm idênticas.

## 4. Por que a primitiva é global nas variedades de teste

**[DERIVED]** Na classe natural tensorial, β(g_R,y₀) não é uma forma definida apenas por escolher uma carta: em sobreposições, seus ingredientes e as contrações transformam tensorialmente. Os valores calculados em cartas diferentes coincidem. Logo β glua como uma 3-forma complexa global suave em toda variedade riemanniana orientada em que a métrica seja não degenerada e y₀ seja admissível.

Na apresentação de (1.1), mudanças de coframe cancelam entre e^a∧e^b∧e^c e β_{abc}. O polinômio é invariante pelo grupo conectado de Lorentz e, por complexificação da identidade de transformação, pelo grupo complexo conectado correspondente; em particular pela forma real SO(4) necessária na avaliação riemanniana. Não se requer um coframe global. CP² não ser spin não impede o argumento: estamos usando tensores e referenciais orientados, sem espinores.

A restrição dos denominadores é indispensável. Uma expressão que contivesse, por exemplo, 1/|dy|² não poderia ser avaliada em mapas constantes. Uma primitiva de Chern–Simons local da conexão também não satisfaria esta globalidade tensorial: ela pode mudar por termos não triviais entre cartas. Por isso não contradiz a conclusão seguinte.

## 5. Dois testes Einstein compactos

Com y constante, T_scalar=0 e \(\mathcal E_y=0\). Em quatro dimensões, G+Λg=0 equivale a Ric=Λg. Portanto qualquer variedade Einstein riemanniana positiva, reescalada para essa constante, anula todos os termos de EOM e suas derivadas em (2.1).

**[KNOWN — fontes primárias]** S⁴ redonda e CP² com Fubini–Study são Einstein compactas de Ricci positiva. As fórmulas de Chern–Gauss–Bonnet e assinatura utilizadas aqui são expostas em [Gursky–LeBrun, §§1–2, equações (6)–(7)](https://arxiv.org/pdf/math/9807055). Os números e(CP²)=3 e p₁(CP²)=3 são explicitados também em [Bouwknegt–Evslin–Mathai, §2, após o Lema 2.4](https://arxiv.org/pdf/1409.1296).

Adote agora as normalizações riemannianas usuais \(\int E_4^R=\chi\) e \(P_4^R=p_1(TM)\). Os testes dão

| Variedade, orientação usual | ∫E₄ᴿ | ∫P₄ᴿ |
|---|---:|---:|
| S⁴ redonda | 2 | 0 |
| CP² Fubini–Study | 3 | 3 |

Para S⁴, o raio √(3/Λ) fornece Ric=Λg. Para Fubini–Study, se Ric(g_FS)=λ_FS g_FS com λ_FS>0, a métrica (λ_FS/Λ)g_FS tem Ric=Λg; isso segue da invariância da conexão sob reescala constante. Não se precisa escolher uma normalização numérica particular de g_FS.

Os números topológicos também podem ser conferidos: S⁴ possui uma célula em graus 0 e 4 e H²=0, logo χ=2 e assinatura zero. CP² possui uma célula em graus 0,2,4 e a classe do hiperplano tem auto-interseção +1, logo χ=3 e assinatura +1. Em dimensão quatro, a fórmula de assinatura dá ∫p₁=3τ.

Integrar (2.1) complexificada nos dois testes mata as EOM e dβ por Stokes. Obtém-se

\[
2A'=0,\qquad 3A'+3B'=0.
\tag{5.1}
\]

A matriz de avaliação é \(\begin{pmatrix}2&0\\3&3\end{pmatrix}\), de determinante 6. Portanto A′=B′=0 e, pela mudança de base invertível da seção 3, A=B=0.

**[DERIVED] Teorema.** Na classe natural algébrica da seção 2, com Λ>0, Euler e Pontryagin são linearmente independentes modulo \(d\Omega^3_{\rm nat}+\mathcal I_{\rm EOM}\). Em particular não existe um certificado de trivialidade covariante on-shell da forma (2.1) para uma combinação não nula. □

## 6. Relação precisa com C0 e com o sigma

A condição característica (7.33) pode agora ser separada dos outros componentes de C0. Se a igualdade fraca empregada no complexo for, por definição ou por sua resolução Koszul–Tate, a igualdade modulo \(\mathcal I_{\rm EOM}\) nessa classe, o teorema estabelece essa condição para as duas classes gravitacionais de grau quatro. Sem gauge interno, não há classes características de Yang–Mills adicionais a testar.

**Passo residual identificado:** se “≈” for definido apenas como anulação sobre a superfície estacionária, é preciso verificar que uma igualdade fraca no setor polinomial A₂ admite um certificado finito com coeficientes da classe usada em (2.1). Isso é a identificação do ideal de anulação com o ideal diferencial das EOM, ou o correspondente passo de regularidade/resolução KT. Um lema de Hadamard com coeficientes suaves arbitrários em todas as variáveis não fornece automaticamente o certificado racional necessário à complexificação. A definição explícita pelo ideal evita essa ambiguidade; aplicar a classificação BBH exige compatibilizar suas hipóteses de resolução com essa definição.

O ganho sobre a nota anterior é concreto: a continuação de assinatura e a globalidade deixaram de ser hipóteses vagas para os certificados definidos. Há uma prova da não trivialidade característica nesse setor. Não declaramos, por essa razão isolada, todos os demais pressupostos de C0 verificados nem H^{1,4}(s|d)=0 na álgebra global irrestrita.

**Corolário de escopo útil.** O mesmo teste de certificados vale para uma métrica alvo suave h_AB(y), inclusive S³ numa carta, se mapas constantes y₀ forem soluções, não houver potencial que desloque a constante cosmológica e os coeficientes forem regulares nesse valor. A razão é que a prova fixa y=y₀ antes de complexificar a métrica; não exige continuação complexa de todo o alvo. Todas as derivadas de y desaparecem, restando a mesma equação Einstein vazia. Isso paga o teste Euler/Pontryagin também para certificados desse setor sigma; não prova a classificação completa das outras possíveis classes do sigma não polinomial ou global.

O resultado é universal no espaço dos campos admissíveis, não apenas numa vizinhança de jatos do mapa identidade com posto espacial três. Se a álgebra fosse restrita a mapas de posto não nulo e admitisse denominadores nesses gradientes, os mapas constantes estariam excluídos e esta prova não se aplicaria. Os observáveis relacionais e o mapa de reconstrução podem exigir tal domínio; isso não autoriza acrescentá-lo silenciosamente ao complexo de contra-termos locais.

## 7. Consequências operacionais e custódia

Para a continuação BV, registrar separadamente:

1. [DERIVED] Não trivialidade Euler/Pontryagin modulo o ideal de EOM natural algébrico, com Λ>0.
2. [KNOWN/contrato] Correspondência A₂ ↔ formas invariantes, conforme (8.4)–(8.8) de BBH.
3. [OPEN específico] Resolução KT/igualdade fraca no mesmo espaço de coeficientes e demais hipóteses de C0, se não adotadas como contrato importado verificado.
4. [OPEN] Cálculo H¹ completo do sigma, especialização formal quando necessária, matriz BV forte, QME renormalizada e independência entre fundos.

A prova exclui uma obstrução matemática definida; não usa dados observacionais e não altera o gate. Somente arquivos novos nesta pasta foram escritos. A nota BV e demais fontes continuam intactas. Nenhum um.py, Lean ou script CAS foi executado para produzir esta demonstração.
