# Naturalidade com B₀: transporte para s e obstrução de curvatura no relativo

10/09/2026, frente 074. [DERIVED — demonstrações escritas delimitadas] [KNOWN — transgressão e representação semissimples indicadas]. Nenhum original, fonte congelada ou um.py foi alterado; não houve execução de um.py, Lean ou CAS.

**Resultados concretos:** (a) na completação formal especificada abaixo, normalizar pelos jatos de B₀ e projetar tipos tensoriais de Lorentz transporta uma primitiva de s para uma primitiva natural, desde que ela já pertença à mesma completação; (b) essa operação não é uma retração para d_H ou s|d_H: a forma de Euler do fundo fornece um contraexemplo explícito, inclusive on-shell no mesmo Einstein–sigma; (c) a diferença entre as formas de Euler de g e B₀ admite uma transgressão natural formal, enquanto o termo diagonal de B₀ sobrevive. Não se demonstrou uma anomalia não nula de ghost 1, nem exatidão natural geral de H¹,⁴.

## 1. Fontes e classe do problema

Li integralmente `COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md`, bem como as notas071 `COVARIANTIZACAO_E_H2_GLOBAL.md` e `COROLARIO_H5_E_ANOMALIA_LOCAL.md`. Elas distinguem a primitiva coordenada da classe natural, e funções suaves do campo completo de uma completação formal de flutuações.

Na apresentação mínima, B₀=(g₀,φ₀) e todos os seus jatos são inertes para s, mas d_H prolonga esses jatos. Naturalidade significa equivariância sob mudanças locais de coordenadas, transportando **simultaneamente** B₀ e os campos dinâmicos, e independência de uma escolha adicional de frame/coordenadas. É uma condição de covariância passiva; não é a afirmação de que a expressão seja s-fechada. O gauge quântico age nos campos completos, mantendo B₀ fixo.

Para o resultado positivo, use g=g₀+h e a álgebra formal na flutuação tensorial h, com as seguintes condições em cada coeficiente:

- ordem finita e grau polinomial finito nos jatos diferenciados e nos demais geradores tensoriais, ghosts e antifields;
- coeficientes C∞ nos valores escalares φ,φ₀, sem expandi-los em série;
- dependência tensorial em g₀,g₀⁻¹ e volume, admitindo também coeficientes suaves de g₀ em uma etapa coordenada intermediária;
- ausência de inversões de dφ, curvatura ou invariantes que eliminem os mapas constantes e os jatos simétricos usados como controle;
- a série e s definidos na mesma filtração, com somente um número finito de contribuições para cada coeficiente.

Um gerador tensorial de valor h pode ser formalmente expandido. Não se assume que uma função C∞ arbitrária de h pertença a um módulo Lorentz localmente finito antes dessa expansão. Também não se usa um máximo uniforme de ordem de jatos em todas as ordens formais.

## 2. Uma retração natural para s, com hipótese de classe explícita

### 2.1 Normalização dos jatos do espectador

Fixe um ponto x e um frame ortonormal orientado e temporalmente orientado de g₀ nesse ponto. Use as coordenadas normais de g₀ centradas em x, e um frame normal correspondente. Para qualquer ordem de jatos necessária, os jatos dessa transformação são determinados pelas equações das geodésicas e do frame, resolvidas recursivamente. Eles usam um número finito de jatos de g₀, com operações polinomiais nos derivados e fatores de g₀⁻¹. Não se avalia B₀ em pontos distantes para definir o valor do operador local.

As componentes normais de um tensor dinâmico e seus derivados podem ser expressas triangularmente por derivados covariantes de fundo; as componentes normais da métrica de fundo podem ser expressas por curvatura e seus derivados, com as relações algébricas pertinentes. Outra escolha do frame no mesmo ponto é uma transformação de SO⁺(1,3). Como a escolha é pela exponencial de g₀, não sobra uma mudança não linear arbitrária entre dois desses sistemas normais com o mesmo frame.

Denote N₀ essa avaliação normal de uma expressão coordenada, com a origem da coordenada normal no ponto de avaliação. Uma dependência explícita em coordenadas de uma primitiva é avaliada nessa origem. Essa avaliação não é presumida covariante sobre expressões arbitrárias; será seguida pela projeção de índices. Sobre uma expressão já natural, ela recupera a mesma expressão escrita nos dados normais.

### 2.2 Por que N₀ comuta com s

O diferencial mínimo s é equivarante sob uma mudança **fixa** de coordenadas, inclusive sobre os jatos dos ghosts e antifields. A transformação usada em N₀ depende exclusivamente dos jatos de B₀. Como sB₀=0, suas matrizes e todos os coeficientes de transformação são s-inertes. Não há um termo adicional de variação da transformação. Segue, em cada ordem necessária,

\[
N_0(s\beta)=s_N(N_0\beta).
\tag{2.1}
\]

s_N é o mesmo diferencial escrito nos geradores normais. Avaliar x na origem também comuta com s, pois sx=0. As relações entre jatos normais são preservadas, dado que são relações do espectador inerte. O argumento vale para formas de qualquer grau, considerando seus índices exteriores entre os índices tensoriais.

O ponto é específico: não se afirma N₀d_H=d_HN₀. A derivada horizontal move o centro normal e diferencia os jatos de B₀; s não faz nenhuma dessas duas coisas.

### 2.3 Projeção Lorentz realmente finita

Depois da avaliação g₀=η no frame, cada coeficiente formal tem apenas um número finito de monômios tensoriais. Seus coeficientes C∞(φ,φ₀) são escalares para Lorentz. Esse coeficiente pertence a uma soma finita de módulos tensoriais de so(1,3), possivelmente com relações tensoriais/Bianchi. A semissimplicidade fornece a projeção algébrica P_inv no tipo trivial, compatível com mapas equivariantes. Quotientes pelas relações tensoriais não invalidam essa projeção, pois são submódulos nas representações finitas envolvidas.

[KNOWN] A separação por tipos e a preservação de exatidão por projeção equivarante são precisamente o mecanismo de [BBH1995, Apêndice C](https://arxiv.org/pdf/hep-th/9505173v2). Aqui a projeção é aplicada somente depois de verificar o caráter tensorial finito de cada coeficiente. Não é uma média sobre o grupo Lorentz não compacto.

Como s_N é equivarante, P_inv comuta com ele. A transformação de jatos e essa projeção preservam o grau formal em h; as operações são compatíveis com os mapas equivariantes entre os graus que aparecem em s. Portanto definem um mapa coeficiente a coeficiente

\[
\mathcal R_N=P_{\rm inv}N_0,
\qquad\mathcal R_Ns=s\mathcal R_N,
\qquad\mathcal R_N\alpha=\alpha
\ \text{se }\alpha\text{ é natural}.
\tag{2.2}
\]

Reescrever o resultado em qualquer frame produz um operador local natural, porque os dados normais em dois frames se relacionam apenas por Lorentz, cuja invariância já foi imposta. Isso fornece a equivariância pelas mudanças não lineares de coordenadas por meio da normalização, e não por confundir Lorentz com todo o grupo de difeomorfismos.

**Lema de transporte.** Se α natural satisfaz α=sβ e β já pertence à álgebra coordenada formal especificada na seção1, então

\[
\boxed{\alpha=s(\mathcal R_N\beta)}
\tag{2.3}
\]

com primitiva natural da mesma classe formal. Assim a inclusão natural→coordenada é injetiva em H(s) nessa classe. A afirmação é para s; não implica injetividade em H(s|d_H).

**Limite da entrada073:** a exatidão para uma expressão suave do campo completo pode ser formalmente desenvolvida em h juntamente com sua primitiva; (2.3) aplica-se a esse par. Mas uma série formal arbitrária não é automaticamente a série de uma expressão local de ordem finita já abrangida pelo teorema073. Não se invoca Borel para esconder ordens de jatos não limitadas, não se avalia a série em h finito e não se transporta uma inversa cohomológica entre completações sem prova. A existência da primitiva ordinária na mesma completação é uma hipótese explícita de (2.3).

## 3. Contraexemplo relativo no próprio Einstein–sigma: Euler do espectador

Defina a 4-forma natural

\[
\mathcal E(g_0)=
(\bar R_{\mu\nu\rho\sigma}\bar R^{\mu\nu\rho\sigma}
-4\bar R_{\mu\nu}\bar R^{\mu\nu}+\bar R^2)\,dV_{g_0}.
\tag{3.1}
\]

É uma normalização não dividida por 32π² da forma de Euler, com a orientação escolhida. É s-fechada porque só depende de B₀. Em uma carta com frame escolhido existe uma forma de Chern–Simons CS₃(ω₀) com

\[
d_H\operatorname{CS}_3(\omega_0)=\mathcal E(g_0).
\tag{3.2}
\]

Uma expressão é P(ω₀,dω₀)+(2/3)P(ω₀,ω₀∧ω₀), com P o polinômio invariante quadrático normalizado para (3.1). Ela é local e de ordem finita, mas depende da escolha de conexão expressa no frame e não é uma 3-forma natural do campo métrico sozinho. [KNOWN] A identidade de transgressão é a construção de [Chern–Simons, §3](https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf).

**Proposição.** Não existem b₄⁻¹ e b₃⁰ naturais universais, regulares nos campos e jatos declarados na seção1, tais que

\[
\mathcal E(g_0)=s b_4^{-1}+d_H b_3^0
\tag{3.3}
\]

para o sistema mínimo Einstein–sigma com Λ>0, nem como identidade formal em h=g−g₀ que admita o coeficiente h=0. O mesmo vale se o espectador for sujeito às EOM universais.

**Prova direta em assinatura Lorentz.** Escolha localmente um espaço forma Lorentziano com

\[
g=g_0,\qquad R_{\mu\nu}(g_0)=\Lambda g_{0\mu\nu},
\qquad R_{\mu\nu\rho\sigma}
=K(g_{\mu\rho}g_{\nu\sigma}-g_{\mu\sigma}g_{\nu\rho}),
\quad K=\Lambda/3,
\tag{3.4}
\]

na convenção de curvatura que realiza essa Ricci. Tome φ=φ₀ constantes no S³, todos os ghosts e antifields zero. A fonte sigma é zero e as equações Einstein–sigma são satisfeitas. A denominação de Sitter/anti-de Sitter depende da convenção de curvatura com assinatura +---; a prova usa apenas (3.4).

Nessa configuração o campo vetorial BRST completo é zero: suas componentes de gauge contêm ghosts, e suas componentes KT contêm EOM ou antifields, todas nulas aqui. Logo o primeiro termo de (3.3) desaparece, também se b₄⁻¹ contém derivados de antifields.

Seja J₃ o valor de b₃⁰ nessa configuração. Naturalidade obriga J₃ a ser preservado por todas as isometrias locais orientadas e temporalmente orientadas do espaço forma. Em cada ponto, o grupo de isotropia é SO⁺(1,3), e

\[
(\Lambda^3\mathbb R^{1,3*})^{SO^+(1,3)}=0.
\tag{3.5}
\]

Com efeito, a dualidade de Hodge identifica uma 3-forma invariante a um vetor invariante. Invariância pelas rotações deixa somente a direção temporal, e invariância por um boost força também essa componente a zero. Os valores constantes φ,φ₀ não fornecem vetores do espaço-tempo. Assim J₃=0 em cada ponto e dJ₃=0.

Por outro lado, em dimensão quatro,

\[
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}=24K^2,
\quad R_{\mu\nu}R^{\mu\nu}=36K^2,
\quad R^2=144K^2,
\]

de modo que

\[
\boxed{\mathcal E(g_0)=24K^2\,dV_{g_0}\ne0.}
\tag{3.6}
\]

Isso contradiz (3.3). A prova é local; não integra sobre uma variedade compacta, não usa continuação Riemanniana e não depende de uma escolha de frame global. Na série em h, basta o coeficiente h=0, com todos os seus jatos zero; não ocorre ressoma. ∎

No valor Λ=3/4 da ação usada nas entregas, o coeficiente de (3.6) é 3/2. Seu sinal global acompanha a orientação da forma, mas sua não nulidade não depende dessa escolha.

**Consequência exata:** a classe de Euler do espectador é zero no complexo relativo coordenado por (3.2), mas não no subcomplexo natural por (3.3). Esta é uma obstrução concreta em H⁰,⁴(s|d_H), não uma classe demonstrada de H¹,⁴. Não contradiz o teorema ordinário073 de anomalias; impede usar esse teorema como se a inclusão natural preservasse exatidão em todos os graus.

O teste pressupõe a família universal regular que inclui campos constantes e espaços formas. Uma classe restrita à referência FRW, ou equipada com um vetor/tempo adicional ou inversos de dφ, seria outra classe e não recebe automaticamente essa conclusão.

## 4. Por que normalizar e projetar Lorentz não resolve o relativo

No frame normal em um ponto, ω₀=0. Por isso N₀CS₃(ω₀)=0 em todos os pontos quando a receita é recentrada ponto a ponto, enquanto N₀d_HCS₃=E(g₀). A projeção Lorentz não altera nenhum desses dois fatos. Assim, sobre esse elemento coordenado,

\[
\boxed{\mathcal R_Nd_H\operatorname{CS}_3
-d_H\mathcal R_N\operatorname{CS}_3=\mathcal E(g_0).}
\tag{4.1}
\]

A curvatura não foi eliminada pela escolha Γ₀(x)=0: os jatos derivados da conexão permanecem. O lado direito de (4.1) mede a falta de comutação com a derivada horizontal. A invariância do valor normal sob Lorentz não transforma essa avaliação em um mapa do complexo relativo.

Esse controle é compatível com a distinção de [BBH1995, Teorema7.1 e condição7.33](https://arxiv.org/pdf/hep-th/9505173v2), que conserva classes características na cohomologia covariante em vez de tratá-las como divergências covariantes automáticas. Aqui a não trivialidade de um representante específico foi demonstrada diretamente e não importada para todos os graus.

## 5. Uma reparação natural que funciona: diferença de classes características

O contraexemplo não impede a transgressão entre **duas** conexões. Ela fornece um controle positivo útil na completação formal g=g₀+h.

Ponha A=g₀⁻¹g e S=A^{1/2}, pela série binomial em A−1. S é g₀-autoadjunto e satisfaz

\[
g(u,v)=g_0(Su,Sv).
\tag{5.1}
\]

Transporte a conexão de g para o fibrado métrico g₀:

\[
\nabla^1=S\nabla^gS^{-1},\qquad
\nabla^0=\nabla^{g_0},\qquad \theta=\nabla^1-\nabla^0.
\tag{5.2}
\]

Ambas são conexões métricas para g₀; θ é uma 1-forma tensorial com valores em so(g₀). A definição é natural conjuntamente nos dois campos. Para ∇^t=∇⁰+tθ,

\[
R_t=R_0+tD_0\theta+t^2\theta\wedge\theta.
\]

A invariância de P e Bianchi dão ∂_tP(R_t,R_t)=2dP(θ,R_t). Portanto

\[
T_P(g,g_0)=2\int_0^1P(\theta,R_t)\,dt,
\qquad
\boxed{d_HT_P=\mathcal E(g)-\mathcal E(g_0).}
\tag{5.3}
\]

A integral é polinomial em t e pode ser escrita como 2P(θ,R₀)+P(θ,D₀θ)+(2/3)P(θ,θ∧θ). Ela usa apenas dados locais dos dois campos. Em cada grau formal de h, S e S⁻¹ têm um número finito de termos, e (5.3) conserva ordem finita de jatos e naturalidade. Não exige interpretar a raiz para métricas afastadas da carta formal nem continuar a série para h finito.

Ao pôr h=0, θ=0 e T_P=0. Assim a transgressão remove a **diferença** característica; não produz uma primitiva de E(g₀). Esse exemplo separa explicitamente a parte relativa que admite correção natural da classe diagonal que permanece.

## 6. Critério suficiente específico para o grau cinco, sem apagar a curvatura

Para compor com a conjugação natural investigada em paralelo, pode-se usar o seguinte critério abstrato finito. Ele é uma proposição condicional, não uma afirmação de que todos os seus antecedentes foram pagos.

Suponha que na mesma álgebra natural formal exista uma conjugação finita por grau de forma que transforme s+d_H em

\[
\mathbb Q=s+E+C,
\quad\deg E=(0,1),\quad\deg C=(-1,2),
\quad\mathbb Q^2=0.
\tag{6.1}
\]

Então {s,E}=0 e E²=−{s,C}; logo E induz um diferencial \bar E na cohomologia de s, mesmo que E não seja nilpotente antes desse quociente. Filtre pelo grau de forma q=0,…,4. A primeira página é H(s), e o diferencial seguinte é \bar E. Se

\[
H^1(s)=H^2(s)=H^5(s)=0,
\tag{6.2}
\]

e os dois grupos da segunda página

\[
E_2^{4,1}=H^1(\bar E;H^4(s))=0,
\qquad E_2^{3,2}=H^2(\bar E;H^3(s))=0,
\tag{6.3}
\]

forem nulos **na classe natural formal**, todos os cinco canais de grau total cinco desaparecem: (5,0),(4,1),(3,2),(2,3),(1,4). Páginas posteriores são subquocientes e não os recriam. A filtração tem cinco níveis, logo esse argumento não exige uma convergência infinita em grau de forma. Conclui-se H⁵(𝕼)=0.

Para deduzir H¹,⁴(s|d_H)=0 disso, a anomalia deve ainda admitir sua descida dentro da mesma álgebra natural. Esse antecedente também precisa ser demonstrado, não importado de uma descida coordenada que use primitivas fora da classe.

O lema da seção2 pode transportar as nulidades (6.2) **se** suas primitivas ordinárias já forem conhecidas na mesma completação. Ele não transporta automaticamente (6.3), justamente porque R_N não comuta com a parte horizontal. Os grupos (6.3) são com coeficientes na cohomologia dinâmica indicada; não podem ser substituídos, sem um mapa demonstrado, por H¹/H² de de Rham de S³ ou por um cálculo de curvaturas escalares sem esses coeficientes.

A classe Euler encontrada está em grau total quatro. Ela não constitui por si um canal sobrevivente de anomalia em grau cinco: seria preciso uma composição de graus e uma consistência BRST que esta nota não afirma. Sua utilidade é provar que o termo de curvatura e a mudança de classe precisam de cálculo, mesmo quando todas as primitivas ordinárias relevantes existem.

## 7. Entrega e resíduo preciso

[DERIVED] Há uma covariantização de primitivas de s por jatos normais do espectador e projeção tensorial finita. [DERIVED] Não há uma covariantização universal que também comute com d_H: Euler fornece o controle explícito. [DERIVED] A transgressão relativa (5.3) é natural e formalmente local, e deixa a classe diagonal exposta.

[OPEN] Para a anomalia efetiva de referência, falta conferir a existência ordinária na mesma completação, os grupos naturais com coeficientes (6.3), a descida natural e as condições adicionais de regularidade/escala/contatos dos contratermos. A nota não os substitui por semissimplicidade Lorentz, por C∞ localmente finito ou por uma avaliação em uma única solução.

Esses resultados não alteram as entregas071–073. Eles delimitam o próximo elo matemático sem afirmar uma anomalia interagente não nula, QME demonstrada ou completude da gravidade quântica.
