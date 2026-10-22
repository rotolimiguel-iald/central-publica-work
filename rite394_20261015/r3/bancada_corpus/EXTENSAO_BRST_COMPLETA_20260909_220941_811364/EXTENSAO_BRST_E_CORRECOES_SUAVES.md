# Extensão BRST linear completa do estado Einstein–sigma

09/09/2026. **[DERIVED + KNOWN — prova escrita; não nova formalização Lean.]**

**Enunciado.** No mesmo fundo ambiente \(M=I\times S^3\), \(I\subset(0,\pi)\),
\(g=dr^2-a^2\gamma\), \(a=2\cos(r/2)\), \(\phi=\mathrm{id}\),
\(c_{\!m}>0,\ \kappa c_{\!m}=4,\ \Lambda=3/4\), o estado físico linear da
entrega 067 admite uma extensão a um par completo de pseudocovariâncias
Hadamard de gauge/auxiliar/ghost. A extensão satisfaz as equações completas,
as CCR/CAR graduadas e as identidades BRST lineares exatas. Sua restrição ao
quociente físico é o estado positivo 067.

“Pseudocovariância” é deliberado: não há positividade requerida em todas as
componentes não físicas. O resultado fornece o dado livre para o produto
estrela graduado de funcionais microcausais, inclusive os não lineares;
não prova a identidade mestra quântica da interação, ausência de anomalias,
existência não perturbativa ou limite UV.

A diferença frente a 067 não é uma mudança de nome: ali as CCR só foram
identificadas no quociente físico; aqui são realizadas no operador BRST
completo. Não se substitui \(CK\) por \(K^*K\).

## 1. Entradas fixadas e notação de adjuntos

As fontes locais são a [nota Jacobi 066](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>)
e a [demonstração física 067](<C:/IALD/Central de Patentes/Chatgpt/HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md>),
com suas reduções S/V e TT. Aqui adotamos:

- V: perturbações \(u=(h,\xi)\), posto 13.
- W: vetores de gauge, identificados com covetores pelo g de fundo.
- \(\mathcal H=\mathcal H^*\): Hessiana variacional da ação Einstein–sigma.
- \(K v=(\mathcal L_vg,\mathcal L_v\phi)\).
- C: leitura de Donder de h; ignora ξ.
- \(\ell=1/(2\kappa)>0\): parâmetro constante de fixação. Não é o grau harmônico.
- \(D=\mathcal H+\ell C^*C\), \(Q=CK=Q^*\).
- \(\mathfrak h=\dot a/a\ne0\): Hubble; não é o operador \(\mathcal H\).

O asterisco * é o adjunto formal para as formas bilineares não degeneradas
das fontes. O símbolo † será reservado ao adjunto simplético nos dados de
Cauchy. Q é normalmente hiperbólico; \(D=\mathcal B\mathcal P\), com
\(\mathcal P\) normalmente hiperbólico e
\(\mathcal B=\mathrm{diag}(-I_{\mathrm{tr}}/(4\kappa),-c_{\!m}I)\) invertível.
Os Green de D são \(G_D=G_{\mathcal P}\mathcal B^{-1}\), não os Green
normalizados brutos.

As identidades já derivadas na fonte são
\[
\mathcal HK=0,\quad K^*\mathcal H=0,\quad
DK=\ell C^*Q,\quad K^*D=\ell QC .
\tag{1.1}
\]
Logo, para cada escolha avançada/retardada,
\[
G_DC^*=\ell^{-1}KG_Q,\qquad CG_D=\ell^{-1}G_QK^* .
\tag{1.2}
\]
Valem também para funções causais \(E_D,E_Q\).

Mantemos uma convenção única de CCR em todos os blocos: escreva
\(W^+-W^-=\epsilon E\), onde \(\epsilon\) é o fator \(+i\hbar\) ou
\(-i\hbar\) determinado pela orientação já fixada de E e pela ordem dos
campos em 067. A literatura citada usa \(i^{-1}E\) com ℏ=1. Nenhum passo
abaixo depende de trocar essa convenção; todos os setores usam o mesmo ε.

## 2. Operador BRST completo sem a hipótese C=K*

Introduza b em W e os dois setores ghost c e antighost \(\bar c\).
A parte bosônica da ação livre é
\[
S_B(u,b)=\tfrac12\langle u,\mathcal Hu\rangle+
\langle b,Cu\rangle-\tfrac1{2\ell}\langle b,b\rangle.
\tag{2.1}
\]
Eliminar b dá b=ℓCu e a Hessiana D para u. Na convenção matricial graduada
de Wrochna–Zahn, defina sobre \(V\oplus W^{\oplus3}\):
\[
L=\begin{pmatrix}
\mathcal H&C^*&0&0\\
C&-\ell^{-1}&0&0\\
0&0&0&Q\\
0&0&Q&0
\end{pmatrix},\qquad
\gamma=\begin{pmatrix}
0&0&K&0\\
0&0&0&0\\
0&0&0&0\\
0&1&0&0
\end{pmatrix}.
\tag{2.2}
\]
A graduação é (0,0,1,−1). Diretamente,
\[
\gamma^2=0,\quad L=L^*,\quad \gamma^*L=L\gamma.
\tag{2.3}
\]
Na última identidade, os únicos blocos não nulos são Q:
\(CK=Q\) e \(K^*C^*=Q\). Não aparece \(K^*K\).
A homologia compacta de γ em grau −1 é zero porque b é enviado
identicamente ao antighost. São exatamente os pontos estruturais a conferir
no contrato abstrato, não uma aplicação do caso particular T=K.
[Wrochna–Zahn, Hipótese 2.15 e §2.7](https://arxiv.org/html/1407.8079v2).

Os Green completos são explicitamente
\[
\boxed{G_L^{\mathrm{ret/adv}}=
\begin{pmatrix}
G_D&KG_Q&0&0\\
G_QK^*&0&0&0\\
0&0&0&G_Q\\
0&0&G_Q&0
\end{pmatrix}^{\mathrm{ret/adv}}.}
\tag{2.4}
\]
Para verificar o bloco superior esquerdo:
\(\mathcal HG_D+C^*G_QK^*=1\) por (1.2).
O bloco inferior esquerdo bosônico é
\(CG_D-\ell^{-1}G_QK^*=0\).
O bloco inferior direito é \(CKG_Q=QG_Q=1\).
Os blocos restantes seguem de \(\mathcal HK=0\) e dos adjuntos.
Logo \(LG_L=G_LL=1\), com o suporte causal correto. O termo b–b nulo
não foi omitido: no complemento de Schur,
\(\ell^2CG_DC^*-\ell=0\), pois \(QG_Q=1\).
Isso também verifica a identidade do propagador causal completo.

## 3. Extrator de gauge: a hipótese de sobrejetividade é derivada

Neste fundo, \(\mathcal L_v\phi=v^i\). Para uma perturbação qualquer
\(u=(h,\xi)\), defina o operador diferencial local
\[
(\mathcal Eu)^i=\xi^i,\qquad
(\mathcal Eu)^r=
\frac{-a^{-2}\gamma^{ij}h_{ij}-2\,\mathrm{div}_\gamma\xi}
{6\mathfrak h}.
\tag{3.1}
\]
Ele depende de uma derivada espacial de ξ, mas não de uma inversão global.
Para \(u=Kv\),
\[
-a^{-2}\gamma^{ij}(\mathcal L_vg)_{ij}
=6\mathfrak h\,v^r+2\,\mathrm{div}_\gamma v_{\mathrm{sp}},
\quad \xi=v_{\mathrm{sp}},
\]
portanto
\[
\boxed{\mathcal EK=1\quad\hbox{off-shell}.}
\tag{3.2}
\]
Assim K não tem núcleo, inclusive nos modos globais baixos. A propriedade
mais útil é a inversa esquerda explícita, e não apenas a ausência de núcleo.

Fixe \(\Sigma=\{r_0\}\times S^3\). Sejam \(\mathscr E,\mathscr F\) os espaços
de dados de Cauchy suaves para D e Q, com formas simpléticas não degeneradas
\(\Omega_D,\Omega_Q\). Escreva \(U_D,U_Q\) para as evoluções e ρ para os
operadores de traço valor/derivada normal. Defina
\[
k=\rho_D K U_Q,\qquad
c=\rho_Q C U_D,\qquad
e=\rho_Q\mathcal E U_D.
\tag{3.3}
\]
Em e, ρ_Q significa apenas extrair os dois jets de \(\mathcal E U_Du\);
não se afirma que \(Q(\mathcal E U_Du)=0\). Quando se deseja uma solução Q,
evoluem-se esses dados por U_Q. Os três mapas são diferenciais de ordem
espacial finita: derivadas temporais superiores de soluções são eliminadas
pelas equações de Cauchy.

De (1.1) e (3.2),
\[
ck=0,\qquad ek=1.
\tag{3.4}
\]
A identidade de Green e (1.2) dão
\[
\Omega_D(kz,u)=\ell\,\Omega_Q(z,cu),\qquad k^\dagger=\ell c.
\tag{3.5}
\]
Uma verificação independente do fator é tomar \(z=\rho_QE_Qf\):
\(KE_Qf=\ell E_DC^*f\) e aplicar Green duas vezes.
Como \(ek=1\), segue
\[
c(\ell e^\dagger)=1.
\tag{3.6}
\]
Logo c é sobrejetivo e possui uma inversa direita que preserva dados suaves.
Não se inferiu sobrejetividade da mera condição \(\ker K=0\).

Uma decomposição simplética conveniente é obtida pondo
\[
q=e-\tfrac12(ee^\dagger)k^\dagger,\quad
r=\ell q^\dagger,\quad
p=1-kq-rc .
\tag{3.7}
\]
Como \(k^\dagger k=0\), cálculo algébrico dá
\[
qk=1,\quad qq^\dagger=0,\quad cr=1,\quad qr=0,
\quad p^2=p=p^\dagger,\quad cp=qp=0.
\tag{3.8}
\]
Por exemplo,
\(qq^\dagger=ee^\dagger-\tfrac12ee^\dagger-\tfrac12ee^\dagger=0\).
Todo dado tem a decomposição única
\[
u=pu+k(qu)+r(cu).
\tag{3.9}
\]
A primeira parcela é física, a segunda é gauge e a terceira é o levantamento
dos vínculos. As duas últimas formam um par simplético; a primeira é seu
complemento simplético. O quociente \(\ker c/\mathrm{Ran}\,k\) é representado
por \(\mathrm{Ran}\,p\). No complexo de Cauchy BRST, os graus ±1 também têm
homologia zero, por \(\ker k=0\) e \(\mathrm{Ran}\,c=\mathscr F\).

Todos os adjuntos aqui são calculados com as matrizes cinéticas verdadeiras.
Elas são não degeneradas e locais, de modo que os adjuntos dos mapas
diferenciais continuam de ordem finita. Esses mapas não são declarados
preservadores de frequência positiva. Serão usados sobre correções já suaves.

## 4. Pares Hadamard iniciais e o defeito Ward suave

Precisamos primeiro de pares de pseudocovariâncias, sem positividade exigida,
\[
W_{D,0}^\pm,\quad W_Q^\pm,
\]
bisoluções hermitianas de D e Q, com diferença \(\epsilon E_D,\epsilon E_Q\)
e orientações microlocais opostas. Escolhem-se compatíveis com a conjugação real.

**[KNOWN — contrato conferido.]** A construção de projetores Hadamard para
fibrados hermitianos não degenerados fornece esses pares; positividade não é
parte desse passo. São suficientes a forma de onda com símbolo principal
escalar, autoadjunticidade na forma hermitiana e geometria espacial limitada.
Em S³ compacta, num pequeno intervalo em torno de r₀, esses requisitos valem.
[Gerárd–Murro–Wrochna, §5.2, Proposição 5.4 e Observação 5.5](https://link.springer.com/article/10.1007/s00023-025-01539-1).

A aplicação não usa o teorema de vácuo do artigo: D normalizado é onda num
fibrado de posto 13 com forma cinética não degenerada, e Q é onda no fibrado
de posto 4. Transporte paralelo temporal para a conexão do operador e a
mudança da densidade pela raiz do volume espacial retiram a primeira
derivada temporal e fixam a forma de fibra. Restam
\(\partial_r^2+A(r)\), com A autoadjunto nessa forma e símbolo
\(|\zeta|_{a^2\gamma}^2\,1\). Os coeficientes e todos os seus jets são
limitados no intervalo pequeno escolhido. Propagar seus dados por D e Q
estende as bisoluções a todo I; propagação de singularidades conserva a
orientação. Não se assume uniformidade até as extremidades excluídas.

Defina o defeito
\[
\mathcal D^\pm=\ell C W_{D,0}^\pm-W_Q^\pm K^* .
\tag{4.1}
\]
Por (1.2) e CCR,
\[
\mathcal D^+-\mathcal D^-
=\epsilon(\ell CE_D-E_QK^*)=0.
\tag{4.2}
\]
A frente de onda de \(\mathcal D^+\) está numa orientação nula e a de
\(\mathcal D^-\) na contrária; operadores diferenciais não aumentam essas
frentes. As orientações são disjuntas. Como são a mesma distribuição,
\[
\boxed{\mathcal D^+=\mathcal D^-\in C^\infty.}
\tag{4.3}
\]
É uma propriedade exata, não um limite assintótico truncado.

## 5. Correção explícita das Ward em dados de Cauchy

Escreva \(B_0^\pm\) e \(B_Q^\pm\) para as formas de pseudocovariância sobre
\(\mathscr E,\mathscr F\), isto é,
\[
W_{D,0}^\pm(F,G)=B_0^\pm(\rho_DE_DF,\rho_DE_DG),
\]
e analogamente para Q. Essa convenção usa a identificação simplética de
observáveis com soluções; não confunde a forma B com a simples restrição
dos dois índices do kernel W à superfície.

O defeito de Ward nessa representação é
\[
d^\pm(z,u)=B_0^\pm(kz,u)-\ell B_Q^\pm(z,cu).
\tag{5.1}
\]
Ele é a versão, com os fatores simpléticos, dos dados de \(\mathcal D^\pm\).
Portanto \(d^+=d^-=d\) tem kernel suave. Além disso,
\[
d(z,kz')=B_0^\pm(kz,kz')
\tag{5.2}
\]
é hermitiano em z,z′, pois ck=0. A compatibilidade real dos pares e o
cancelamento dos comutadores tornam a correção abaixo a mesma para ±.

Usando a inversa esquerda q de (3.7), ponha
\[
\boxed{h_d(u,v)=
-d(qu,v)-\overline{d(qv,u)}+d(qu,kqv).}
\tag{5.3}
\]
O último termo é hermitiano por (5.2); logo \(h_d=h_d^*\).
Como qk=1, os dois últimos termos se cancelam em \(h_d(kz,v)\), deixando
\[
h_d(kz,v)=-d(z,v).
\tag{5.4}
\]
Defina \(B_1^\pm=B_0^\pm+h_d\). Então
\[
B_1^\pm(kz,u)=\ell B_Q^\pm(z,cu).
\tag{5.5}
\]
h_d é suave porque d é suave e q,k têm ordem espacial finita. É acrescentado
igualmente aos dois sinais, preservando a diferença CCR. Ao propagar os
dados, a correção é uma bisolução suave, portanto o par continua Hadamard.
Esta última afirmação usa a continuidade da evolução nos espaços C∞ sobre
compactos, em ambas as variáveis; não a suposta complex-linearidade de q.

No espaço-tempo, (5.5) equivale às identidades exatas
\[
\boxed{\ell C W_{D,1}^\pm=W_Q^\pm K^*,\qquad
\ell W_{D,1}^\pm C^*=KW_Q^\pm.}
\tag{5.6}
\]
Até aqui não se demonstrou positividade física; ela é tratada no passo seguinte.

## 6. Substituir o bloco físico preservando Hadamard

Um projetor arbitrário de Cauchy, mesmo diferencial, pode misturar os dois
ramos de frequência após evolução. Por isso não substituímos o bloco por
uma congruência arbitrária e depois o chamamos Hadamard. Primeiro provamos
que a diferença a transportar é suave.

### 6.1 Extrator físico espacial

A decomposição SVT da fonte 067 fornece um operador S sobre perturbações
arbitrárias, local no tempo e pseudodiferencial espacial de ordem finita.
Para explicitar sua invariância, escreva \(b_{ij}=-a^{-2}h_{ij}\) e decomponha
\[
b_{ij}=2\psi\gamma_{ij}
+2(\nabla_i\nabla_j-\tfrac13\gamma_{ij}\Delta)E
+2\nabla_{(i}F_{j)}+t_{ij}.
\]
No setor de grau ≥2, uma transformação espacial com parâmetro
\(\nabla E+F\) remove as partes E/F, e a transformação temporal
\[
T=(\psi-\Delta E/3)/\mathfrak h
\]
remove o traço que resta. Defina a matéria no corte por
\[
\xi_{\mathrm{flat}}=\xi-(\nabla E+F).
\tag{6.1}
\]
Projete seus componentes longitudinais/transversais sobre grau ≥2;
extraia também t TT e aplique as normalizações canônicas 067.
Esse é S. Em \(u=Kv\), E/F reproduzem a parte espacial de v no grau ≥2,
enquanto \(\xi=v_{\mathrm{sp}}\); o tensor TT é zero. Os graus baixos são
removidos pelo projetor já justificado como gauge. Portanto
\[
SK=0\quad\hbox{off-shell}.
\tag{6.2}
\]
Os inversos de Hodge/York, a retirada de núcleos finitos e os fatores
\(a,\mathfrak h^{-1},K_S^{1/2},K_V^{1/2}\) são suaves no domínio e têm ordem
espacial finita. Não há evolução temporal escondida em S.

### 6.2 Comparação no sistema reduzido

Considere a matriz de covariâncias reduzidas
\[
W_{\mathrm{red},1}^\pm=S W_{D,1}^\pm S^*.
\tag{6.3}
\]
Para teste j reduzido, \(S^*j\in\ker K^*\), por (6.2). Então (5.6) dá
\(CW_{D,1}^\pm S^*j=0\); como \(DW_{D,1}^\pm=0\), também
\(\mathcal HW_{D,1}^\pm S^*j=0\).
A redução completa 067 mostra que (6.3) é uma bisolução das equações
canônicas S/V/TT. Green e a identificação simplética dão exatamente sua
CCR reduzida, inclusive a nulidade dos comutadores cruzados.

A composição espacial com S preserva a orientação microlocal pela prova
de 067: covariáveis características têm parte espacial não nula, e
composição com os operadores espaciais de ordem finita conserva a relação
de meia onda. Isso não usa um projetor de Cauchy propagado arbitrariamente.

Se \(W_{\mathrm{red},067}^\pm\) é o par positivo exato por modos,
\[
\Delta^\pm=W_{\mathrm{red},067}^\pm-W_{\mathrm{red},1}^\pm
\]
satisfaz \(\Delta^+=\Delta^-\), pois ambos os pares têm a mesma CCR.
Cada sinal tem a correspondente orientação microlocal. Assim
\[
\boxed{\Delta^+=\Delta^- \text{ é uma bisolução suave}.}
\tag{6.4}
\]
Não foi assumida a suavidade da diferença no quociente.

### 6.3 Estender somente a diferença suave

Seja δ a forma suave de dados de Cauchy de Δ, com os fatores simpléticos
canônicos incluídos. Seja
\(s=\rho_{\mathrm{red}}S U_D\) o extrator dos dados canônicos; ele é definido
também fora de \(\ker c\) usando os jets das soluções D.
Sobre \(\ker c\), s identifica o quociente por gauge com os dados físicos
067, preservando a forma simplética.

Ponha
\[
h_{\mathrm{phys}}(u,v)=\delta(spu,spv),\qquad
B^\pm=B_1^\pm+h_{\mathrm{phys}}.
\tag{6.5}
\]
Como δ é suave, aplicar s e p de ordem espacial finita, e então evoluir,
produz uma bisolução suave. Portanto Hadamard é preservado. Como pk=0,
\(h_{\mathrm{phys}}(kz,u)=0\); as Ward (5.5) permanecem exatas. A mesma
correção em ± conserva CCR e realidade.

Para u em \(\ker c\), \(pu=u-kqu\), portanto u e pu têm a mesma classe
física e \(spu=su\). A restrição de B ao quociente é precisamente
\[
B^\pm|_{\ker c/\mathrm{Ran}\,k}=B_{\mathrm{red},067}^\pm.
\tag{6.6}
\]
Logo é positiva. Definindo \(W_D^\pm\) pela evolução/identificação com
\(\rho_DE_D\), obtivemos simultaneamente
\[
DW_D^\pm=W_D^\pm D=0,\quad
W_D^+-W_D^-=\epsilon E_D,\quad
W_D^\pm=W_D^{\pm*},
\]
\[
\ell CW_D^\pm=W_Q^\pm K^*,\quad
\ell W_D^\pm C^*=KW_Q^\pm,\quad
W_D^\pm\ge0\text{ em }\ker K^*,
\tag{6.7}
\]
e a orientação Hadamard em todos os índices de campo.

## 7. Covariâncias completas: fórmulas e verificações

Finalmente, sobre \((u,b,c,\bar c)\), defina
\[
\boxed{
\Lambda_L^+=
\begin{pmatrix}
W_D^+&KW_Q^+&0&0\\
W_Q^+K^*&0&0&0\\
0&0&0&W_Q^+\\
0&0&W_Q^+&0
\end{pmatrix},\quad
\Lambda_L^-=
\begin{pmatrix}
W_D^-&KW_Q^-&0&0\\
W_Q^-K^*&0&0&0\\
0&0&0&-W_Q^-\\
0&0&-W_Q^-&0
\end{pmatrix}.}
\tag{7.1}
\]
A estrutura de sinais ghost corresponde à relação graduada; não é uma
probabilidade negativa nem um estado positivo na álgebra auxiliar inteira.

**Equações.** No bloco u–u,
\[
\mathcal HW_D^\pm+C^*W_Q^\pm K^*
=DW_D^\pm-\ell C^*CW_D^\pm+C^*W_Q^\pm K^*=0.
\]
No bloco b–u, \(CW_D^\pm-\ell^{-1}W_Q^\pm K^*=0\).
Os demais seguem de \(QW_Q^\pm=0\) e \(\mathcal HK=0\).
Assim \(L\Lambda_L^\pm=\Lambda_L^\pm L=0\) exatamente.

**CCR/CAR graduadas.** No setor bosônico a diferença entre os sinais é
ε vezes (2.4) causal. Nos dois blocos ghost, a soma relevante na regra
graduada é \(W_Q^+-W_Q^-=\epsilon E_Q\), devido ao sinal menos em
\(\Lambda_L^-\). Logo a regra vale em todas as componentes, não somente
sobre testes invariantes.

**BRST.** Multiplicação matricial dá
\(\gamma\Lambda_L^+=\Lambda_L^+\gamma^*\).
Para ambos os sinais, \(\Lambda_L^\pm\mathrm{Ran}\,\gamma^*
\subset\mathrm{Ran}\,\gamma\), com o sinal graduado correspondente no
setor menos. Por exemplo, a imagem relevante tem a forma
\((KW_Q^\pm f,0,0,\pm W_Q^\pm K^*g)\), explicitamente γ de uma seção.
As identidades são exatas, sem resto suave.

**Hadamard.** Todas as entradas não nulas são \(W_D^\pm,W_Q^\pm\) ou suas
derivadas por K/K*. Diferenciação não amplia as frentes de onda; cada
entrada tem a orientação do sinal indicado. A propriedade decorre das
correções suaves das seções 5–6, e não apenas das CCR/Ward.

**Positividade física.** Em grau zero, \(\ker\gamma^*\) é constituído por
\((F,B,0,0)\) com \(K^*F=0\). Os termos cruzados com b desaparecem:
\(\langle F,KW_QB\rangle=\langle K^*F,W_QB\rangle=0\).
Resta \(W_D^\pm(F,F)\ge0\), exatamente o estado físico 067.
A homologia em grau zero é a álgebra física anterior: b é exato, e
as equações reduzem ao denominador \(\mathcal H\Gamma_c\).
Para excluir uma contribuição adicional compacta de b, usa-se que
\(Qb=0\) e suporte compacto implicam b=0 por unicidade de Cauchy.

Os critérios matriciais acima são os que entram no contrato de
[Wrochna–Zahn, §3.2](https://arxiv.org/html/1407.8079v2).
A prova não invoca sua Proposição 3.4 na hipótese T=K:
verifica diretamente L, γ, seus Green e as covariâncias.

## 8. Alcance para funcionais não lineares e limites restantes

A matriz (7.1) fornece o kernel de contração livre do produto estrela
graduado formal sobre funcionais microcausais de suporte compacto.
A condição microlocal permite as contrações; a relação graduada exata
reproduz o propagador completo no comutador, e a identidade BRST linear
permite tratar o diferencial livre como derivação compatível.
É esse requisito livre que não estava assegurado pelo representante
apenas físico 067.

Isso não é a solução da teoria interagente. Produtos ordenados no tempo
e sua extensão às diagonais exigem renormalização; o diferencial BRST
não linear e a identidade mestra quântica requerem análise de anomalias
e normalizações próprias. A existência dessas escolhas, sua compatibilidade
com o protocolo selecionado e qualquer conclusão UV não foram derivadas aqui.

As entradas geométricas continuam específicas: \(\phi=\mathrm{id}_{S^3}\)
permite (3.1), e \(\mathfrak h\ne0\) permite recuperar a direção temporal.
Em outro fundo, \(\mathcal EK=1\) pode falhar; não se proclama o teorema
para qualquer Einstein–matéria. Não se inclui r=0, a=0 ou um domínio com
outras condições de bordo. S³ inteira permanece uma extensão geométrica
do fundo; não uma única carta global dos cinco pesos positivos.

O operador BRST é linearizado e a construção é de prova escrita com
ferramentas analíticas conhecidas. Não houve execução/importação de
nenhum um.py, alteração de fontes congeladas, nova auditoria Lean,
confirmação observacional ou afirmação de fechamento da gravidade quântica.
