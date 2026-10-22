# Einstein–sigma acoplado: estado físico positivo e condição microlocal

09/09/2026. **[DERIVED + KNOWN — demonstração escrita, sem nova formalização Lean.]**

**Resultado.** Para a ação ambiente Einstein–sigma adotada, no fundo
\(g=dr^2-4\cos^2(r/2)\gamma_{S^3}\), \(\phi=\mathrm{id}_{S^3}\),
\(c>0,\ \kappa c=4,\ \Lambda=3/4\), a composição das reduções S/V e TT abaixo
constrói um estado quase livre positivo na álgebra dos observáveis lineares
invariantes de gauge. Sua covariância possui um representante distribucional
bisolução do operador de Jacobi acoplado e com frente de onda na relação nula
orientada de frequência positiva. A existência é demonstrada neste fundo pela
redução completa e pelos modos exatos, sem aplicar um teorema de vácuo Einstein
a um fundo com matéria.

O sentido preciso de “Hadamard físico” usado aqui é explicitado na seção 6:
CCR no quociente físico, bisolução do Jacobi e condição microlocal para um
representante da covariância. Não se afirma já construída uma matriz completa
de covariâncias de um operador BRST com CCR sobre todos os testes não invariantes.
A ação ambiente, sua relação com os dados selecionados e a extensão geométrica
a S³ inteira permanecem entradas declaradas.

## 1. Fontes locais e revisão das reduções

As demonstrações locais efetivamente lidas nesta análise são:

- [Operador de Jacobi, identidades de gauge e álgebra covariante](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>), em especial §§3–5.
- [Redução ADM escalar/vetorial](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531/REDUCAO_ADM_MODOS_FISICOS.md>), §§4–8, incluindo os mapas de teste (6.2)–(6.3).
- [Ação e modos TT](<C:/IALD/Central de Patentes/Chatgpt/MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md>), §§2–6.

**[REAL — leitura; DERIVED — parecer matemático próprio.]** A revisão dos três
textos encontrou uma composição coerente: as restrições S/V são resolvidas;
o termo de derivada total escalar usa a medida a³; a diferença de momento
proporcional a x não altera a forma simplética; os modos baixos são tratados
por transformações de gauge explícitas. Em TT, o coeficiente de ε² é metade
da segunda variação da curvatura e a matéria acrescenta \(2\kappa c=8\) ao
termo espacial 2. Isso produz massa espacial 10, e não a equação do vácuo.

Os recibos CAS conferem as identidades enumeradas por seus scripts. Não
constituem uma formalização da completude SVT, do cálculo microlocal ou desta
demonstração em Lean. Os hashes das versões lidas são medidos no manifesto desta nota.

Trabalhamos em \(M=I\times S^3\), com I qualquer intervalo aberto de (0,π).
Assim \(a>0\), \(H=\dot a/a<0\), e M é globalmente hiperbólico. Os mapas
espaciais inversos e a escolha temporal de gauge são regulares em compactos
interiores. Nenhum extremo a=0 ou H=0 é acrescentado.

## 2. Contratos primários: o que pode ser importado

A pesquisa foi dirigida às fontes primárias indicadas. A ausência de um
teorema diretamente aplicável nas fontes examinadas não é afirmação de
inexistência de resultado em toda a literatura.

| Fonte primária e localizador | Conteúdo que foi conferido e aplicação aqui |
|---|---|
| [Hack–Schenkel 1205.3484v2](https://arxiv.org/html/1205.3484v2), Def. 3.4, §§4–5 | Constrói a estrutura de álgebra gauge; o centro e as representações exigem análise própria. Não fornece um teorema geral de existência de Hadamard positivo para todo sistema acoplado. Seu contrato inclui \(K^\dagger K\) Cauchy-hiperbólico e fixação \(P+TK^\dagger\). |
| [Hack 1403.3957v2](https://arxiv.org/html/1403.3957v2), Teorema 2.1, §§2–3 | Trata Einstein–Klein–Gordon com um escalar, incluindo redefinição de campos e condições de não degenerescência. A especialização cosmológica usa espaço plano R³ e escalar dependente do tempo. Não é o sigma de três componentes tangentes com mapa identidade em S³; a construção algébrica não paga sozinha a covariância física positiva. |
| [Gérard 2311.11043v1](https://arxiv.org/html/2311.11043v1), Teorema 1.1, §1.1.3 | Prova existência para gravidade linearizada em dimensão quatro, Cauchy compacta e fundo Einstein \(\mathrm{Ric}=\Lambda g\). A positividade no quociente é uma condição separada da equação e da frente de onda. A hipótese Einstein falha exatamente no fundo desta nota. |
| [Gérard–Wrochna 1403.7153v2](https://arxiv.org/html/1403.7153v2), Hip. 1.1/1.3 e Teorema 1.2 | Há existência para Yang–Mills linearizado em fundo on-shell, com os requisitos geométricos e de fibrado indicados. S³ é compacta e paralelizável, mas isso não identifica o operador Einstein–sigma com Yang–Mills. O método de projeção física e correção infravermelha é pertinente; o teorema não é importado por homônimo. |
| [Wrochna–Zahn 1407.8079v2](https://arxiv.org/html/1407.8079v2), Def. 3.1, Lema 3.2, Obs. 3.3 e Prop. 3.4 | O transporte BRST exige covariâncias Hadamard com entrelaçamento de gauge e positividade física já verificadas. A observação distingue CCR/equações modulo gauge, suficientes para o estado físico linear, de condições mais fortes usadas em funcionais não lineares. Não fornece gratuitamente as covariâncias que faltam. |
| [Gérard–Wrochna 1209.2604v2](https://arxiv.org/html/1209.2604v2), Teorema 7.1 e §7.2 | A caracterização pseudodiferencial separa a orientação microlocal da positividade. Usamos esse cálculo e a parametriz de meia onda como ferramentas conhecidas; a positividade, a normalização e o transporte físico deste modelo são demonstrados abaixo. |
| [Gérard–Wrochna 2405.00866v2](https://arxiv.org/html/2405.00866v2), Teoremas 1.2–1.3 | No caso de Sitter, um candidato euclidiano pode ter boa estrutura Hadamard/gauge e falhar em positividade; uma modificação restaura um estado. Esse exemplo impede promover “Hadamard” a “estado positivo” sem teste. Não é uma obstrução de existência no nosso modelo. |
| [Lindblom–Taylor–Zhang 1709.08020v1](https://arxiv.org/html/1709.08020v1), §§2–4 | Fornece os harmônicos escalares, vetoriais e tensoriais da esfera e suas identidades de autovalor, traço, divergência e ortogonalidade. A decomposição usa o grau principal chamado k nessa referência, denotado ℓ nesta nota. |

Duas incompatibilidades de contrato são concretas.

**Fundo não Einstein.** Escreva \(W=\phi^*\gamma\) e
\(T=c(W-\tfrac12\mathrm{tr}_g W\,g)\). Traçar
\(G+\Lambda g=\kappa T\) em dimensão quatro e substituir de volta dá
\[
\mathrm{Ric}=\Lambda g+\kappa cW=\tfrac34g+4W.
\]
Como \(W_{rr}=0\) e \(W_{ij}=\gamma_{ij}\), a componente rr obrigaria qualquer
constante Einstein a valer 3/4; as componentes espaciais impedem a igualdade.
Logo o teorema de vácuo não se aplica. Isso não demonstra ausência de estado.

**Adjunto e fixação não são homônimos.** Na nota local,
\(K^\dagger(f,\chi)=-2\,\mathrm{div}\,f+u\cdot\chi\), enquanto C é a leitura
de Donder da perturbação métrica. Portanto \(Q=CK\), já demonstrado onda,
não é identificado com \(K^\dagger K\). Uma aplicação literal do contrato de
Hack–Schenkel exigiria conferir outra identificação/forma bilinear. A prova
direta pelas identidades \(HK=0\) e pelas relações de \(H_{\mathrm{gf}},C,K,Q\)
continua disponível e é a utilizada; não recebe uma hipótese de adjunto
hiperbólico por troca de nome.

## 3. Espaço físico completo e normalização

As reduções lidas estabelecem, modulo difeomorfias infinitesimais suaves
espacialmente compactas, a decomposição dos modos físicos em S, V e TT com ℓ≥2.
Em Cauchy S³, esse grupo inclui os Killing espaciais globais dependentes do tempo.
Não se está usando um grupo menor, restrito por condições de bordo inexistentes.

- Escalar: \(\lambda=\ell(\ell+2)\),
  \(K_S=4(\lambda-3)/(\lambda+3)>0\),
  \(p_S^2=\lambda+3=(\ell+1)^2+2\ge11\).
- Vetorial: \(D=\ell(\ell+2)-3\),
  \(K_V=4D/(D+8)>0\),
  \(p_V^2=D+7=(\ell+1)^2+3\ge12\).
- Tensorial: \(\lambda_{TT}=\ell(\ell+2)-2\),
  \(p_{TT}^2=\lambda_{TT}+9=(\ell+1)^2+6\ge15\).

No setor homogêneo escalar não há gradiente sigma; a restrição e o calibre
temporal removem o restante. Os modos ℓ=1 S/V são exatamente os calibres
residuais descritos na fonte. Não há uma frequência zero física na lista acima.
Essa exclusão é justificada por campos K(v), não por apagar estados incômodos.

Com \(d\eta=dr/a\), \(a=2\mathrm{sech}\eta\), as variáveis canônicas são
\[
u_S=a\sqrt{K_S/\kappa}\,x_S,\quad
u_V=a\sqrt{K_V/\kappa}\,x_V,\quad
u_{TT}=a\,t/(2\sqrt\kappa).
\]
Cada amplitude tem ação
\[
\tfrac12\int d\eta\,[u'^2-(p^2+2\mathrm{sech}^2\eta)u^2].
\]
A forma simplética é a soma das formas canônicas correspondentes. Em S/V isso
foi conferido diretamente por \(\Theta_m=ca^3\langle\dot\xi-b,\delta\xi\rangle\);
em TT vem do momento \(a^3\dot t/(4\kappa)\). Termos de fronteira temporais
alteram a potencial por diferencial exata, sem alterar a forma simplética.

A completude não é apenas uma contagem de cinco graus de liberdade: SVT
remove E/F/traço por gauge onde H≠0; os núcleos baixos são identificados;
lapse/shift são então determinados; a transversalidade do corte e a identidade
de Noether recuperam as equações métricas eliminadas. Os mapas e seus inversos
têm ordem espectral finita, preservando dados espaciais suaves.

## 4. Teorema de Darboux para a covariância reduzida

Seja A um operador autoadjunto estritamente positivo de ordem um, raiz
de um operador elíptico L de ordem dois e símbolo principal \(|\xi|_\gamma^2\)
sobre uma variedade espacial compacta. Pode-se restringir a um subespaço
invariante dado por um projetor pseudodiferencial ortogonal Π de ordem zero
que comuta com L. Considere
\[
(\partial_\eta^2+A^2+2\mathrm{sech}^2\eta)u=0.
\]
Para uma base ortonormal real de autovetores \(Ae_n=p_ne_n\), defina
\[
f_p(\eta)=\frac{(p-i\tanh\eta)e^{-ip\eta}}
{\sqrt{2p(p^2+1)}},\qquad
W(\eta,z;\eta',z')=\hbar\sum_n
 f_{p_n}(\eta)\overline{f_{p_n}(\eta')}\,
 e_n(z)\otimes e_n(z').
\tag{4.1}
\]
Então W define uma distribuição positiva, bisolução da equação, com CCR
canônico no subespaço Π e orientação microlocal de frequência positiva.

**Equação e CCR.** Ponha \(T=\tanh\eta\), \(S=1-T^2\) e \(b=p-iT\).
Temos \(b'=-iS,\ b''=2iST\), e
\[
b''-2ipb'+2Sb=0.
\]
Além disso,
\[
b\bar b'-b'\bar b=2ipS,\quad |b|^2=p^2+T^2,
\]
portanto
\[
f_p\bar f_p'-f_p'\bar f_p
=\frac{2ip(S+p^2+T^2)}{2p(p^2+1)}=i.
\]
Assim a diferença entre W e sua transposta tem os dados de Cauchy do
comutador canônico. Unicidade da evolução de cada modo e completude da base
dão CCR, com Π no lugar da identidade ambiente quando se trabalha num setor
projetado. A convenção conjunta do propagador e da forma simplética fixa o sinal.

**Positividade e existência distribucional.** Para teste j suave compacto,
\[
W(\bar j,j)=\hbar\sum_n\left|
 \int d\eta\,\overline{f_{p_n}(\eta)}\,j_n(\eta)\right|^2\ge0.
\]
Em compactos temporais, todas as derivadas de f têm crescimento polinomial
em p. Coeficientes harmônicos de j decaem rapidamente; as multiplicidades
têm crescimento polinomial por elipticidade em espaço compacto. A soma
converge como distribuição, pode ser diferenciada e preserva a desigualdade.
O argumento não assume a positividade de um produto interno indefinido de treze
componentes: usa a forma positiva da ação física reduzida.

**Condição microlocal.** Escreva
\[
W_0(\eta,\eta')=(2A)^{-1}e^{-iA(\eta-\eta')},\quad
D_\eta=(A-i\tanh\eta)(A^2+1)^{-1/2}.
\]
Então \(W=D_\eta W_0D_{\eta'}^*\), com o fator ℏ entendido.
O cálculo funcional elíptico dá \(D_\eta\in\Psi^0\), suave em η,
com símbolo principal 1; A tem símbolo principal \(|\xi|_\gamma\).
A parametriz de meia onda para \(e^{-iA(\eta-\eta')}\) tem relação canônica
do fluxo geodésico de γ e uma única orientação temporal. Composição com
\((2A)^{-1}\), D e Π conserva essa relação e sua orientação. Potenciais de
ordem zero só afetam amplitudes; os caminhos nulos são os do produto
\(d\eta^2-\gamma\), também os de \(g=a^2(d\eta^2-\gamma)\).

Precisão técnica: D e Π são famílias **espaciais** pseudodiferenciais.
Não se declara que qualquer extensão com kernel δ(η−s) seja um operador
clássico de ordem zero em todas as covariáveis do espaço-tempo. Na composição
com a meia onda, todas as covariáveis características têm componente espacial
não nula. A relação conormal diagonal da parte espacial transporta essas
covariáveis; a parte espacial suavizante, inclusive fora da diagonal, não
encontra uma covariável de entrada espacial não nula e produz termo suave.
A composição limpa/FIO nessa região prova a inclusão de frentes de onda.
Alternativamente, cortes microlocais onde \(|\tau|\asymp|\xi|\ne0\) reduzem
o argumento ao cálculo usual; a região complementar da meia onda é suave.

Não é necessário D ser unitário: positividade decorre da forma \(DW_0D^*\);
a igualdade exata de CCR decorre do Wronskiano calculado, e não apenas do
símbolo principal. A retirada de finitos autovalores baixos é suavizante.

**Convenção de orientação.** A fase dos modos é \(e^{-ip\eta}\), p>0.
Usando covariáveis da fase \(e^{i\varphi}\), a primeira covariável temporal
de WF(W) é negativa e a segunda é positiva; em WF′ ambas são negativas.
Denotamos essa relação por \(\mathcal C_{\mathrm{freq}+}\), sem identificar
por nome o sinal com \(\mathcal C_+\) de uma referência de assinatura oposta.
O conjugado tem a orientação contrária. Trocar as duas covariâncias troca
também a convenção do comutador; os sinais não são intercambiados silenciosamente.

## 5. Aplicação aos três setores e mapas reais de observáveis

Para S use \(L_S=-\Delta_\gamma+3\), restrito a ℓ≥2.
Para V use \(L_V=-\Delta^{\mathrm{rough}}_\gamma+5\), na parte transversal
ℓ≥2. Para TT use \(L_{TT}=-\Delta^{\mathrm{rough}}_\gamma+9\), no subespaço
TT. Na esfera de curvatura constante esses operadores comutam com os
projetores indicados. Os projetores vêm da decomposição de Hodge/York por
inversos elípticos, modulo seus núcleos finitos, logo têm ordem zero.
Pode-se estender os operadores sobre o fibrado ambiente por escolhas positivas
no complemento; o resultado restrito não depende dessa extensão.

Se R_A reconstrói \((h,\xi)\) a partir do campo canônico do setor A,
então a covariância conjunta é
\[
\mathbb W=\sum_{A=S,V,TT}R_AW_AR_A^*.
\tag{5.1}
\]
Não há um novo estado assumido nessa fórmula: cada W_A é a soma explícita (4.1).

Para fixar a tipagem de \(R_A^*\), escreva o teste como
\[
F(h,\xi)=\int dr\,a^3\int_{S^3}
 [f^{\mu\nu}h_{\mu\nu}+\langle\chi,\xi\rangle]dV_\gamma .
\]
Os testes f são simétricos contravariantes; \(K^\dagger(f,\chi)=0\) caracteriza
invariância. No setor escalar, com \(y=y_1\dot x+y_0x\),
\(z=z_1\dot x+z_0x\), defina
\[
A_n=\int f^{rr}Y_n,\quad B_n=\int f^{ri}\gamma_{ij}U_n^j,\quad
C_n=\int\langle\chi,U_n\rangle,
\]
\[
R_n=a^3(2z_1A_n-2a^2y_1B_n),\quad
Q_n=a^3(2z_0A_n-2a^2y_0B_n+C_n).
\]
Os coeficientes y,z são exatamente (5.2) da nota S/V; não são funções
livres. Integração por partes e \(x=\sqrt{\kappa/K_S}\,u/a\) dão
\[
j_{S,n}=\sqrt{\kappa/K_S}\,(Q_n-\dot R_n).
\tag{5.2}
\]
No setor vetorial,
\[
j_{V,n}=\sqrt{\kappa/K_V}
 \left[a^3C_{V,n}+\frac d{dr}\frac{16a^5B_{V,n}}{D+8}\right].
\tag{5.3}
\]
O fator dois dos termos de shift é necessário porque f é simétrico. No setor TT,
\(h_{ij}=-a^2t_{ij}\) e \(t=2\sqrt\kappa\,u/a\), logo
\[
j_{TT,n}=-2\sqrt\kappa\,a^5\int f^{ij}T_{n,ij}\,dV_\gamma .
\tag{5.4}
\]
Todas as funções na direita são avaliadas em r(η). Em particular,
dr=a dη cancela o 1/a de x em (5.2)–(5.3); não se acrescenta outro fator a.

Esses operadores e seus transpostos têm ordem espacial finita e um número
finito de derivadas temporais, com coeficientes suaves em I. Preservam teste
suave e suporte temporal compacto; a esfera compacta evita dificuldade de
suporte espacial no transposto não local. Sua composição com a meia onda
conserva a relação \(\mathcal C_{\mathrm{freq}+}\) pelo argumento microlocal
da seção 4. Portanto
\[
\mathrm{WF}(\mathbb W)\subset \mathcal C_{\mathrm{freq}+}.
\tag{5.5}
\]
A inclusão é a apropriada para uma matriz com polarizações físicas:
não se afirma uma singularidade de identidade nas treze componentes.

## 6. Descida ao quociente físico e CCR local

Sejam H o Jacobi variacional formalmente autoadjunto e K o gerador de gauge
da nota local. Tome
\[
\mathcal V_{\mathrm{obs}}
=(\ker K^\dagger\cap\Gamma_c) / H\Gamma_c,\qquad
\sigma([F],[G])=\langle F,E_{\mathrm{gf}}G\rangle,
\]
com a orientação do propagador escolhida compatível com o Wronskiano.
As identidades diretas da nota local asseguram a definição dessa forma:
HK=0, o operador de gauge Q=CK é hiperbólico e a função causal gauge-fixada
leva teste invariante a solução de H modulo gauge.

**Descer.** As reconstruções satisfazem \(HR_Au_A=0\) quando u_A resolve sua
equação. Assim \(\langle HF,R_Au_A\rangle=0\) por integração por partes para
teste compacto, e a covariância (5.1) anula \(H\Gamma_c\) em ambas as entradas.
Para F invariante, \(\langle F,Kv\rangle=0\); qualquer mudança de representante
da solução por gauge não muda a leitura. Os setores baixos removidos são
precisamente Kv e não acrescentam covariância física.

**Positividade.** Com \(j_{A,n}\) de (5.2)–(5.4),
\[
\boxed{\Lambda(\overline{[F]},[G])=
 \hbar\sum_{A,n}
 \overline{\left(\int\overline{f_{p_{A,n}}}j_{A,n}[F]\,d\eta\right)}
 \left(\int\overline{f_{p_{A,n}}}j_{A,n}[G]\,d\eta\right).}
\tag{6.1}
\]
É uma forma de Gram convergente, positiva e hermitiana. Seu conjugado,
com a orientação oposta, também é positivo.

**Identificar o comutador, sem presumir localidade de SVT.** A reconstrução
é uma bijeção simplética entre soluções físicas suaves modulo gauge e a soma
dos modos reduzidos. A identidade de Green identifica o funcional
\(v\mapsto\langle F,v\rangle\) com a solução \(E_{\mathrm{gf}}F\) através da
forma simplética. Para aplicá-la a um representante que não esteja em de Donder,
resolva \(Qw=-Cv\) com dados de Cauchy suaves: v+Kw está nesse gauge,
mantém H(v+Kw)=0 e a mesma classe. Não se exige controle microlocal dessa escolha
auxiliar de representante suave. A integral de F e a forma física não mudam
sob essa transformação, pois \(K^\dagger F=0\) e gauge é nulo na forma restrita.

Transportar a identidade de Green pela bijeção simplética dá, para todos os
testes invariantes reais,
\[
\sigma([F],[G])=\sum_A \langle j_A[F],E_Aj_A[G]\rangle.
\tag{6.2}
\]
O Wronskiano da seção 4 então implica
\(\Lambda(F,G)-\Lambda(G,F)=i\hbar\sigma(F,G)\), na convenção fixada.
Portanto (6.1) é a covariância de um estado quase livre da álgebra CCR física,
e sua extensão aos produtos é a regra de Wick. Mesmo se se mantiver uma
apresentação presimplética com radical, o transporte define um estado que
fatora pelo radical; não se pressupõe uma representatividade experimental.

A identidade (6.2), com o propagador causal covariante, é que assegura
comutatividade para observáveis invariantes com suportes causalmente separados.
Uma variável TT isolada ou um potencial de lapse resolvido não é declarado
local; seus projetores espaciais são não locais.

**Sentido exato do enunciado Hadamard.** O estado (6.1) tem o representante
distribucional (5.1), bisolução de H, com a orientação microlocal (5.5) e
CCR exata sobre testes físicos. Essa é a existência física linear estabelecida.
Não identificamos (5.1) com uma covariância do operador \(H_{\mathrm{gf}}\)
satisfazendo CCR sobre testes arbitrários de treze componentes, nem com uma
matriz BRST completa. O problema de extensão para esse contrato mais forte
permanece separado. A distinção entre o estado linear modulo gauge e o uso
em funcionais não lineares aparece expressamente na
[Observação 3.3 de Wrochna–Zahn](https://arxiv.org/html/1407.8079v2);
a demonstração aqui é direta, não uma aplicação da Proposição 3.4 sem conferir
seus adjuntos.

## 7. Obrigações que não foram convertidas em conclusão

1. **[INPUT] Ação e campos ambiente.** Perturbações independentes de g e φ
   pertencem à extensão Einstein–sigma adotada. A família mínima de cinco
   probabilidades, cuja variação local é gauge, não ganha automaticamente
   esses graus de liberdade físicos.
2. **[INPUT] Domínio geométrico/global.** S³ inteira é extensão suave de g e φ,
   não uma carta global dos cinco pesos positivos. A restrição do estado a um
   diamante causalmente convexo na ortante original é válida para a álgebra
   local induzida; não se identifica automaticamente com toda álgebra obtida
   por outro grupo de gauge ou outras condições de bordo.
3. **[DERIVED + KNOWN, não Lean] Linearização neste fundo.** As três reduções,
   os modos e a prova microlocal compõem a existência acima. Isso não é um
   teorema para qualquer fundo Einstein–matéria ou qualquer métrica selecionada.
4. **[OPEN] Extensão BRST forte, interações e renormalização.** Não se exibiu
   uma família completa de propagadores de gauge/ghost com todas as identidades
   requeridas para funcionais não lineares; não se pagou equação mestra
   quântica, anomalias, fechamento de contra-termos ou limite UV.
5. **[OPEN] Integrabilidade e extremos.** Em Cauchy compacta com simetrias,
   condições de segunda ordem podem restringir quais perturbações lineares
   integram soluções não lineares. Também não se prova estabilidade não linear
   ou uniformidade até a=0/H=0. Nenhuma dessas questões invalida por nome
   a álgebra linear construída no domínio interior.
6. **[OPEN/INPUT] Seleção e natureza.** A escolha dos modos não foi derivada
   como seleção única da natureza, não é um resultado de confirmação da TGL
   e não prova que toda realização pelo registro selecionado produz esse estado.

O avanço em relação à nota acoplada anterior é concreto: a positividade física
e a orientação microlocal já não são apenas uma hipótese abstrata **neste
modelo linearizado e neste quociente**. A matriz completa de gauge e a teoria
interagente não são absorvidas nessa afirmação.
