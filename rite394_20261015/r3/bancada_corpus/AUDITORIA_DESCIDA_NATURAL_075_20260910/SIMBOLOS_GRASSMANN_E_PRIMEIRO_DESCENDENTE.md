# Auditoria: símbolos, coeficientes Grassmann e primeiro descendente natural

10/09/2026, frente 075. [DERIVED — demonstração escrita independente]. Fontes anteriores somente leitura; nenhum um.py, Lean ou CAS executado. Esta nota não altera o resultado074 sobre Euler e não calcula os grupos E₂ ou uma anomalia interagente.

**Conclusão:** a redução por símbolos proposta é válida, com as convenções e hipóteses abaixo. Ela dá primitivas naturais para formas horizontais fechadas de grau menor que quatro e ghost positivo. Além disso, uma identidade variacional covariante fornece o primeiro descendente natural quando a topforma de ghost positivo já é ordinariamente exata. Assim a descida natural pode ser construída sem presumir exatidão de topformas arbitrárias.

## 1. Hipóteses que tornam o cálculo legítimo

Trabalhe na apresentação métrica/difeomórfica mínima ou em variáveis tensorializadas cujo transporte já tenha sido demonstrado. B₀ é um fundo não degenerado de ghost zero. Seus jatos podem aparecer nos coeficientes e não são congelados por d_H.

Z denota o conjunto dos geradores de ghost não zero: ghosts e antifields pertinentes, com todos os seus jatos. Esses jatos são **livres off-shell**. Nenhuma equação de onda dos ghosts ou relação estacionária que remova seus jatos principais é imposta neste lema. Os coeficientes são polinomiais finitos nesses geradores e nos demais jatos diferenciados, suaves nos valores de campos de ghost zero. As expressões são naturais, e uma conexão natural de fundo foi fixada nos fibrados tensorais usados para escrever os operadores.

Na completação perturbativa, cada coeficiente deve satisfazer essas condições e a conexão escolhida deve atuar nos fibrados perturbativos identificados com B₀, preservando a filtração. A prova vale coeficiente a coeficiente nessa situação; não identifica automaticamente uma completação de campos completos com outra de flutuações.

Uma constante externa de ghost positivo sem torre livre de jatos não é um Z desse enunciado. Por exemplo, uma constante ímpar ζ com d_Hζ=0 já fornece uma zeroforma fechada não nula; o lema não a elimina. O anel de constantes aqui tem ghost zero.

## 2. Linearização par, incluindo os sinais dos ghosts

Introduza novos geradores livres v com a mesma paridade, ghost e tipo tensorial de Z, e um parâmetro ε **par**, de ghost zero. Defina

\[
P[v]=\delta_v\omega
 :=\left.{d\over d\epsilon}\omega(Z+\epsilon v)\right|_{\epsilon=0},
\tag{2.1}
\]

prolongando a substituição a todos os jatos. δ_v é uma derivação par. Os v e seus jatos são independentes dos Z; em particular, v ímpar é um gerador Grassmann novo, não uma substituição antecipada por Z. Essa independência permite ler as equações dos coeficientes de um operador linear sem perder termos por nilpotência Grassmann.

Como a variação prolongada comuta com as derivadas totais e fixa a conexão de fundo,

\[
\delta_vd_H=d_H\delta_v.
\tag{2.2}
\]

Portanto d_Hω=0 implica d_HP[v]=0 como identidade de operadores sobre jatos livres de v. P é um operador diferencial linear em v, com coeficientes que podem conter Z ímpares. Não é necessário declarar esses coeficientes comutativos.

Adote uma convenção uniforme: escreva as formas dx à esquerda dos coeficientes Grassmann. Nesse formato, d_H=dx^i∧D_i e as D_i são pares. A variação par (2.1) não introduz um sinal extra ao passar por dx. Se se usa uma notação com coeficientes à esquerda, os sinais devem ser transportados por Koszul antes de comparar símbolos; a fórmula abaixo é na convenção declarada.

## 3. Identidade de símbolos e denominador

Considere um operador P de ordem r em v, com saída em q-formas. Seu símbolo principal é um polinômio homogêneo σ_r(P)(p) de grau r nas variáveis pares p_i. A parte de ordem r+1 de d_HP é

\[
\delta\sigma_r(P),\qquad
\delta=p_i dx^i\wedge.
\]

Defina o operador canônico no símbolo

\[
h=\sum_i{\partial\over\partial p_i}\,\iota_{\partial_i}.
\tag{3.1}
\]

A contração e a derivada em p operam somente nos fatores exteriores e no polinômio de símbolo. Não reordenam os coeficientes Grassmann. Para um símbolo a de grau r e forma q, o cálculo dá

\[
h\delta a
=na+p_i\partial_{p_i}a
 -dx^i\wedge\iota_{\partial_i}a-\delta h a,
\]

portanto

\[
\boxed{\delta h a+h\delta a=(r+n-q)a.}
\tag{3.2}
\]

É uma identidade de módulos sobre a álgebra de coeficientes Grassmann. Não exige invertibilidade ou ausência de nilpotentes nesses coeficientes. O símbolo tautológico δ e o operador h são canônicos sob mudança de base; a construção não depende de projetar apenas invariantes Lorentz.

Em n=4, q<4, o denominador r+4−q é sempre estritamente positivo. Se d_HP=0, então δσ_r(P)=0, e para r≥1

\[
\sigma_{r-1}(Q)=\frac{h\sigma_r(P)}{r+4-q}
\quad\Longrightarrow\quad
\delta\sigma_{r-1}(Q)=\sigma_r(P).
\tag{3.3}
\]

O símbolo de Q tem grau **r−1**, não r. Essa redução é o que termina o procedimento.

## 4. Realização covariante e terminação

Realize (3.3) como um operador natural por contração de seus coeficientes com as derivadas covariantes **simetrizadas** ∇̄_(i₁…i_(r−1))v. Isso define Q_r de ordem r−1 com o símbolo desejado. Para fibrados que incluem índices do alvo, use a conexão natural apropriada já transportada à apresentação escolhida; na classe perturbativa, mantenha explícita sua identificação com o fibrado de fundo.

Então P−d_HQ_r tem ordem no máximo r−1 em v e continua d_H-fechado, pois d_H²=0. Derivar coeficientes gera somente ordem menor em v. Os comutadores entre derivadas covariantes geram curvatura e ordens menores; por isso não impedem o cancelamento do símbolo nem a indução. É precisamente a redução da **ordem em v** que é controlada; a ordem dos jatos nos coeficientes pode crescer, mas em um número finito de etapas.

Repita até a ordem zero. Nesse último caso, δσ₀(P)=0 e hσ₀(P)=0. Pela (3.2),

\[
(4-q)\sigma_0(P)=0,
\]

portanto o operador restante é zero. Conclui-se, após no máximo r remoções,

\[
\boxed{P=d_HQ\quad(1\le q<4),}
\tag{4.1}
\]

com Q natural, linear em v e de ordem finita. Para q=0, o mesmo cálculo mostra diretamente P=0; não se introduz uma forma de grau −1.

O procedimento é global enquanto as conexões e os fibrados naturais usados são globais: os símbolos são tensoriais e a realização por uma conexão fixada entrelaça as mudanças de trivialização. Não requer escolher uma origem no espaço-tempo, uma primitiva integral em x ou uma partição nos valores do alvo. A conexão serve para realizar os símbolos, não é declarada plana.

## 5. Avaliação v=Z e Euler_Z

O passo de substituição é seguro quando feito **depois** da identidade de operadores. A aplicação

\[
\mathrm{ev}:v_I^A\longmapsto Z_I^A
\tag{5.1}
\]

é um mapa de álgebras diferenciais graduadas: respeita os produtos, as paridades e D_i v_I=v_(Ii), ou sua escrita covariante equivalente. Por isso

\[
\mathrm{ev}(d_HQ[v])=d_H(\mathrm{ev}Q[v]).
\tag{5.2}
\]

Mesmo se os coeficientes de Q contêm Z, a igualdade permanece: d_H diferencia tanto esses coeficientes quanto v, e depois da avaliação diferencia as duas ocorrências correspondentes de Z. Não se confunde avaliação com linearização.

Decomponha ω nas componentes homogêneas para Euler_Z, que conta cada ocorrência de Z ou de um de seus jatos com peso um. d_H preserva essa contagem. Para uma componente ω_N, N>0, a variação par satisfaz

\[
P[Z]=\delta_Z\omega_N=N\omega_N.
\tag{5.3}
\]

Logo, por (4.1) e (5.2),

\[
\boxed{\omega_N=d_H\bigl(Q[Z]/N\bigr),\qquad1\le q<4.}
\tag{5.4}
\]

Uma forma de ghost positivo não possui componente N=0 sob a hipótese sobre as constantes da seção1. A soma finita das primitivas (5.4) resolve o caso não homogêneo. Em q=0, P=0 e (5.3) dão ω=0.

Isso prova H^q(d_H) de ghost positivo igual a zero para 0≤q<4 na classe natural declarada. O método preserva polinomialidade em Z e nos jatos por operações finitas. Ele preserva também coeficientes C∞ nos campos de ghost zero, sem pressupor que essas funções pertençam a representações Lorentz finitas.

## 6. Complemento para a topforma já ordinariamente exata

O denominador da seção3 não elimina um operador residual de ordem zero quando q=4. Portanto não se afirma que toda 4-forma natural fechada seja exata. A forma de Euler do espectador da entrega074 permanece um controle de que isso seria falso.

Entretanto, suponha que F seja uma 4-forma natural, de ghost positivo, e que **já exista** uma identidade ordinária F=d_Hβ₃. Cada derivada de Euler–Lagrange de F em relação a Z é então zero. Esse fato é a caracterização usual de uma divergência, não uma hipótese de naturalidade de β₃.

Escreva F=f dV_(g₀) e linearize por (2.1). Integre por partes **algebricamente**, usando a conexão natural fixada, cada derivada de v. Após um número finito de passos obtém-se a identidade de primeira variação

\[
\delta_v F=\sum_A v^A\mathcal E_A(F)+d_H\Theta_F[v].
\tag{6.1}
\]

Os sinais da derivada de Euler são os determinados pela variação par e pela posição declarada de v; as integrações por partes movem derivadas covariantes pares, não introduzem uma regra informal para trocar dois geradores ímpares. A corrente Θ_F é natural, linear em v e finita em jatos: cada etapa usa somente contrações tensoriais, derivadas covariantes e a forma volume paralela de g₀. Não se efetuou uma integral não local no espaço-tempo.

Como E_A(F)=0, decompomos F em graus Euler_Z e avaliamos v=Z em (6.1), obtendo

\[
\boxed{F_N=d_H\bigl(\Theta_{F_N}[Z]/N\bigr).}
\tag{6.2}
\]

Assim uma topforma natural ordinariamente exata, com ghost positivo, admite uma primitiva **natural** nessa classe. O antecedente de exatidão ordinária é indispensável; a forma de Euler tem ghost zero e N=0 e não é afetada por (6.2).

O uso de Euler–Lagrange aqui é consistente com [BBH2000, Teorema4.1, equação4.10 e §4.5](https://arxiv.org/pdf/hep-th/0002245v3). A passagem natural da corrente foi explicitada por integração por partes covariante; não é uma promoção automática da homotopia coordenada dessa fonte.

## 7. O que fica pago para a descida e o que não fica

Se uma anomalia natural a₄¹ satisfaz s a₄¹+d_Ha₃²=0 com algum a₃² ordinário, então F=s a₄¹ é uma topforma natural de ghost2, ordinariamente exata. A seção6 permite escolher a₃² natural. Aplicar s à identidade fornece d_H(s a₃²)=0. Como essa forma tem grau3 e ghost positivo, a seção5 fornece a₂³ natural. Repita nos graus2 e1; no grau0, o resultado de q=0 termina a descida com s a₀⁵=0. Cada etapa é finita e preserva a classe declarada.

[KNOWN] Essa é a estrutura da descida de [BBH2000, §9.2](https://arxiv.org/pdf/hep-th/0002245v3). O que esta nota acrescenta é o controle natural dos operadores/primitivas com o espectador curvo, inclusive o primeiro descendente.

O resultado supõe s natural, s²=0, sd_H+d_Hs=0 e a consistência inicial como identidade local off-shell na mesma álgebra. Não prova essas identidades para uma quebra renormalizada concreta, não resolve os dois grupos E₂ da frente074, não demonstra uma QME nem remove uma anomalia por si. Não inclui fontes centrais de ghost positivo sem jatos livres ou mudanças não verificadas de completação.

O papel da curvatura é preciso: ela aparece em ordens inferiores da construção covariante e é absorvida pela indução finita para um operador **linear em um jato livre de ghost não zero**. Isso não fornece uma retração universal que comute com d_H em ghost zero e não contradiz o contraexemplo Euler.
