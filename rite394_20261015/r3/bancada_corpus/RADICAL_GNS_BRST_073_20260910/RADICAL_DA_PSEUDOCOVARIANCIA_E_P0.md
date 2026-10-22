# Radical da pseudocovariância, carga livre e contrato P₀

10/09/2026, frente 073. [DERIVED — demonstração escrita, sem Lean ou CAS]. Resultado próprio, separado da entrega 072 congelada. Todos os arquivos anteriores permanecem intactos; nenhum um.py foi executado ou importado.

**Resultado central:** as condições documentadas em 068 não implicam automaticamente P₀ na representação cíclica indefinida da pseudocovariância. Depois de quocientar seu radical, podem aparecer novos vetores BRST-fechados provenientes do setor dos vínculos. Um bloco finito explícito admite um desses vetores com norma negativa, preservando CCR, Ward e a covariância física anterior. O bloco pode ser introduzido por correções suaves nas escolhas auxiliares permitidas em 068, sem mudar o estado físico 067 ou a condição Hadamard.

Isso é uma insuficiência do antecedente para aquela promoção de estatuto, **não** uma prova de inexistência de uma representação P₀ adequada, nem uma falha do estado físico 067. A nota também fornece duas condições exatas de saturação do radical que recuperam a cohomologia de uma partícula desejada. Se satisfeitas, a segunda quantização algébrica transporta a positividade sem inventar outra polarização; o domínio dos campos Wick/interações exige ainda estimativas próprias.

## 1. O que foi efetivamente lido

A fonte principal é `EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md`, especialmente (3.3)–(3.9), (5.1)–(5.6), (6.5)–(6.7) e (7.1). A fonte física é `HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md`. A involução e os sinais dos ghosts são os de `CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md`. O contrato P₀ aparece na nota 072 `POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md`, acompanhado de seu adendo de sinal.

[KNOWN] [Wrochna–Zahn, §§3.1–3.3, Definição 3.1 e Lema 3.2](https://arxiv.org/html/1407.8079v2) distingue a função de dois pontos auxiliar de um estado positivo no quociente físico e discute a representação indefinida. O uso da segunda construção requer identificar seu kernel concreto; a passagem pelo radical é mantida explícita abaixo. [Dütsch–Fredenhagen, equação (4.8) e Teorema 4](https://arxiv.org/pdf/hep-th/9807078v2) exige, no domínio da carga livre, positividade do kernel e igualdade dos vetores fechados nulos com a imagem. São as condições que testamos, não apenas a positividade da forma sobre testes fechados antes do quociente.

O fundo permanece M=I×S³, I contido em (0,π), a=2cos(r/2), φ=id, κc_sigma=4 e Λ=3/4. Não se muda a ação ambiente, os modos físicos ou o grupo de gauge declarado.

## 2. Complexo de Cauchy e matriz que as Ward realmente fixam

Complexifique os espaços de dados suaves E e F de 068. Conservamos seus mapas k:F→E, c:E→F, r:F→E e p:E→E, com

\[
ck=0,\quad cr=1,\quad p^2=p,\quad cp=0,\qquad
E=H\oplus kF\oplus rF,\quad H=\operatorname{im}p.
\tag{2.1}
\]

Aqui H é o **espaço físico de Cauchy complexificado**, antes do radical da covariância; não é ainda o espaço de uma partícula Hilbert. A identificação física anterior é ker c/im k≃H.

Fixe o sinal + das pseudocovariâncias. Denote por G=B_Q^+ a forma ghost em F e por B=B_D^+ a forma bosônica em E. Os símbolos Q e D neste parágrafo são os operadores de onda da fonte, não a carga de estados. A identidade Ward (5.5) diz

\[
B(kx,u)=\ell G(x,cu),\qquad \ell={1\over2\kappa}>0.
\tag{2.2}
\]

Na ordem u=(v,x,y)≡v+kx+ry, isso equivale à matriz de formas hermitianas

\[
\boxed{B=
\begin{pmatrix}
A&0&C\\
0&0&\ell G\\
C^*&\ell G&D_c
\end{pmatrix}.}
\tag{2.3}
\]

A é a covariância física 067 em H; logo A≥0. C(v,y)=B(v,ry), e D_c(y,y')=B(ry,ry') é o bloco dos vínculos. O asterisco em C* indica a forma transposta conjugada, não a existência de algum adjunto limitado em Hilbert. A Ward fixa o bloco gauge–vínculo ℓG, mas não fixa C ou D_c.

O complexo de uma partícula antes do radical tem graus −1,0,1:

\[
V=F_{-1}\oplus E_0\oplus F_1,\qquad
q(a,u,d)=(0,ka,\ell cu),\qquad q^2=0.
\tag{2.4}
\]

A forma nos graus ímpares é cruzada, com entradas G, e não há pareamento entre paridades diferentes. Então (2.2) é precisamente a simetria de q na forma total W=B⊕G_ghost. Seus fatores podem ser fixados a partir do dicionário 069: antes de uma fase constante nos vetores ghost, s₀ envia antighost→−k e E→ℓc; a carga é proporcional a −i s₀. Multiplicar os dois tipos de vetores ghost por −i dá (2.4), nas unidades ħ=1, sem mudar sua matriz hermitiana cruzada ou qualquer norma bosônica. Isso é apenas uma escolha de base complexa de estados; não inverte comutadores graduados por uma regra sem paridade.

Sem quociente adicional, H^{-1}(V,q)=H^1(V,q)=0 e H^0(V,q)=H. Esses fatos seguem de k injetivo, c sobrejetivo e (2.1), como demonstrado em 068.

## 3. Construção cíclica: onde o radical entra

Seja ω_W o funcional gaussiano hermitiano da álgebra polinomial graduada, definido por W e pela regra de Wick. Não é apresentado como funcional positivo na álgebra auxiliar. Seu radical cíclico é

\[
\mathcal N=\{A:\ \omega_W(B^*A)=0\ \text{para todo }B\}.
\tag{3.1}
\]

É um ideal à esquerda: substitua B por C*B para conferir CA∈N. Assim a multiplicação à esquerda atua no quociente cíclico. As Ward de dois pontos, a regra de Wick e a compatibilidade da involução implicam ω_W(s₀A)=0. Elas também tornam N estável pelo diferencial, que se promove a uma carga simétrica e nilpotente nesse domínio algébrico.

Para um vetor linear, (3.1) reduz-se exatamente ao radical da forma de uma partícula:

\[
N=\operatorname{rad}W,\qquad \bar V=V/N.
\tag{3.2}
\]

De fato, se W(v,w)=0 para todo w, toda contração de v com um polinômio de Wick é zero; a recíproca é obtida testando contra vetores lineares. A simetria de q implica qN⊂N. Portanto o diferencial de uma partícula relevante para essa representação é **bar q em bar V**, não apenas q em V.

Como as paridades não se misturam,

\[
N=N_G[-1]\oplus N_E[0]\oplus N_G[1],\qquad
N_G=\operatorname{rad}G,\quad N_E=\operatorname{rad}B.
\tag{3.3}
\]

As Ward dão kN_G⊂N_E e cN_E⊂N_G. Um vetor bosônico u representa um bar q-fechado se e somente se

\[
cu\in N_G.
\tag{3.4}
\]

Esta condição é mais fraca que cu=0. Ela é o ponto preciso em que a simples importação da homologia de Cauchy falha.

## 4. Duas condições exatas de saturação

Denote N_A=rad A. Defina o subespaço

\[
J=p(N_E\cap\ker c)
 =\{v\in N_A:\ \exists x\in F,\quad C^*v+\ell Gx=0\}.
\tag{4.1}
\]

As equações de formas significam igualdade contra todos os testes; Gx é um elemento do dual antilinear de F. Não se supõe que G possua uma inversa nesse dual. Em dimensão infinita, injetividade de G não é sobrejetividade.

**Proposição.** Há uma sequência exata natural

\[
\boxed{0\longrightarrow H/J
\longrightarrow H^0(\bar V,\bar q)
\longrightarrow N_G/cN_E
\longrightarrow0.}
\tag{4.2}
\]

Além disso H^{-1}(bar V,bar q)=H^1(bar V,bar q)=0.

**Prova direta.** Se ka∈N_E, (2.2) contra ry para todo y implica a∈N_G; assim o mapa de grau −1 continua injetivo no quociente. O mapa de grau zero continua sobrejetivo em F/N_G porque c já era sobrejetivo. Isso elimina os graus ±1. Para uma classe de grau zero representada por u fechado no sentido (3.4), envie-a a cu modulo cN_E. Acrescentar um radical muda cu por cN_E, e acrescentar um exato kx não muda cu; a aplicação está definida. É sobrejetiva: use u=ry para y∈N_G. Seu kernel admite representante com cu=0, subtraindo um radical que tenha o mesmo c. Tal representante é v+kx; modulo exatos resta v∈H. Ele é zero se e somente se v+kx∈N_E para algum x, o que equivale a (4.1). Isso prova (4.2).

O espaço de uma partícula físico do estado 067 é H/N_A, com a forma A induzida. Para que ele se identifique **pela aplicação canônica**, isometricamente e sem setores extras, com H^0(bar V,bar q), são necessárias e suficientes as condições

\[
\mathrm{S1}:\quad cN_E=N_G,
\qquad
\mathrm{S2}:\quad p(N_E\cap\ker c)=N_A.
\tag{4.3}
\]

S1 permite retirar todo vínculo que ficou fechado por entrar no radical ghost. S2 garante que cada vetor físico nulo pode ser retirado por um radical total mais gauge. Se S2 falha, N_A/J fornece vetores fechados nulos não exatos, violando a completude de P₀. Se S1 falha, há classes extras; elas podem ter sinal negativo, como a próxima seção demonstra. Não se afirma que toda falha de S1 necessariamente produza sinal negativo.

Em blocos, S1 exige que para cada y∈N_G existam v,x tais que

\[
Av+Cy=0,\qquad C^*v+\ell Gx+D_cy=0.
\tag{4.4}
\]

S2 exige a solução da segunda equação de (4.4) com y=0 para cada v∈N_A. Essas são condições de imagem/radical na classe de dados escolhida, não apenas identidades de matrizes formais ou espectros de curvatura.

## 5. Bloco finito: todas as contas explícitas

Considere um plano real de dados gauge F_R=R², complexificado a F=C², com

\[
\Omega=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
G^+={1\over2}\begin{pmatrix}1&i\\-i&1\end{pmatrix},\qquad
G^-=\overline{G^+}.
\tag{5.1}
\]

Então G^± são hermitianas, G^+−G^-=iΩ, e

\[
y=\begin{pmatrix}1\\i\end{pmatrix},\qquad
G^+y=0,\qquad y^*y=2.
\tag{5.2}
\]

Use apenas E=kF⊕rF, com ck=0, cr=1. Para t>0 fixe

\[
B^+=\begin{pmatrix}0&\ell G^+\\\ell G^+&-tI_2\end{pmatrix},\qquad
B^-=\overline{B^+},\qquad
\Omega_E=\begin{pmatrix}0&\ell\Omega\\\ell\Omega&0\end{pmatrix}.
\tag{5.3}
\]

B^± são hermitianas; Ω_E é real, antissimétrica e não degenerada. Temos B^+−B^-=iΩ_E e a Ward B^+(kx,u)=ℓG^+(x,cu). Sobre o kernel clássico ker c=kF, B^+ é zero; esse kernel é todo exato. Um bloco físico A≥0 pode ser acrescentado ortogonalmente sem mudar nenhuma das contas.

O radical bosônico é exatamente kN_G. Para vê-lo, escreva um vetor radical como (x,z). A primeira equação é G^+z=0. A segunda é ℓG^+x−tz=0. Como G^+ é um projetor hermitiano, sua imagem e seu kernel têm interseção zero; logo z=0 e x∈N_G. Portanto cN_E=0, enquanto N_G=Cy≠0: S1 falha.

No quociente de uma partícula, o vetor v=ry satisfaz

\[
\bar q[v]=[\ell y]_{F_1/N_G}=0,
\qquad
\boxed{[v,v]=B^+(ry,ry)=-2t<0.}
\tag{5.4}
\]

Ele não é radical porque sua norma não é zero; não é exato porque todo exato é nulo pela simetria e nilpotência de bar q. A cohomologia de grau zero tem, neste bloco, uma dimensão complexa com sinal negativo. Na decomposição espectral de G^+, ficam um quarteto exato e esse singlete negativo. Isso identifica explicitamente a classe extra N_G/cN_E de (4.2).

O parâmetro t desta seção mede uma liberdade auxiliar de covariância; não é o tempo, o acoplamento cinético sigma ou uma nova matéria de sinal negativo. Nenhum resultado empírico é inferido da matriz.

## 6. Por que o bloco é uma liberdade permitida em 068

Uma condição Hadamard não controla uma alteração de posto finito com dados suaves. Mais precisamente, no espaço gauge de Cauchy do mesmo fundo, escolha um par canônico real de dados suaves f₁,f₂, Ω_Q(f₁,f₂)=1. Ele define um plano simplético F₀ e uma projeção simplética real de posto finito P₀, cujos coeficientes são pareamentos com esses dados suaves.

Os dados de Cauchy das pseudocovariâncias Hadamard têm frente de onda conormal diagonal; sua contração com um dado suave em uma entrada é suave na outra. Portanto remover seus blocos cruzados entre F₀ e seu complemento e substituir o bloco F₀ por (5.1) altera B_Q^± por formas de kernel suave. Os blocos antissimétricos permanecem iΩ_Q, pois a decomposição é simplética. A diferença acrescentada é a mesma nos dois sinais e é real, preservando a relação de conjugação.

Evoluir esses dados pelo operador Q produz uma alteração bisolução suave. Não é necessário escolher uma polarização de todas as frequências: apenas um plano de dados foi alterado. A nova forma G tem um y não nulo no radical, pertencente a esse plano e sem pareamento cruzado com o complemento.

A mudança de G pode ser acompanhada pela fórmula de correção Ward (5.3) de 068. O novo defeito é suave; a correção h_d é suave, preserva CCR e restaura (2.2). Como q p=q r=0 para o extrator q da fonte, essa correção não muda o bloco físico A. Aqui o símbolo q nessa frase é o mapa extrator de 068, não o diferencial (2.4).

Por fim, uma forma real simétrica suave T em F define

\[
h_T(u,u')=T(cu,cu').\tag{6.1}
\]

Somá-la igualmente a B_D^± preserva CCR e realidade. Como ck=0, h_T(kx,u)=0: a Ward permanece exata. Como c=0 nos dados físicos fechados, h_T não altera o estado físico 067. Os mapas c têm ordem espacial finita; uma forma T de posto finito e kernel suave continua suave depois da composição. Evolução em ambas as entradas conserva suavidade e as equações.

Escolha T negativa no plano F₀ e suficientemente grande em módulo para que

\[
(B_D^++h_T)(ry,ry)<0.
\tag{6.2}
\]

O vetor ry continua fechado depois do radical ghost e tem norma negativa. Nem o bloco misto C com H nem o restante da forma impedem essa conclusão. Desse modo existe uma escolha dentro da liberdade documentada de pseudocovariâncias 068 que falha em P₀, mesmo no mesmo fundo e com o mesmo estado físico 067.

**Precisão de custódia e lógica:** não se efetuou nenhuma dessas alterações nos arquivos ou na construção existente. A fonte 068 apresenta uma família com escolhas iniciais e correções; ela não fixa um kernel numérico único que tenha sido medido aqui como negativo. O argumento refuta a implicação universal “os contratos escritos em 068 ⇒ P₀ para sua realização cíclica”, e identifica a condição a acrescentar. Não refuta a existência de outra escolha adequada nessa família.

## 7. O que a segunda quantização de fato transporta

Esta seção responde positivamente ao passo algébrico **se S1–S2 forem verificados para a pseudocovariância escolhida**, sem trocar W por uma polarização inventada.

No domínio gerado por produtos finitos de campos lineares suavizados, a ordenação de Wick dá uma identificação triangular com

\[
\mathcal D_{\rm alg}=\bigoplus_{n\ge0}\operatorname{Sym}_{\rm gr}^{n}(\bar V),
\tag{7.1}
\]

usando a forma W induzida. Graus de partícula distintos são ortogonais. Em grau n, o pareamento é a soma das contrações entre as duas palavras, com os sinais de permutação dos slots ímpares. O radical é exatamente o ideal tensorial gerado por rad W: em cada conjunto finito de vetores, a não degenerescência do quociente permite escolher pareamentos duais, e os produtos simétricos/exteriores conservam a não degenerescência. Esse argumento justifica (7.1) no domínio algébrico da representação cíclica, mesmo quando ω_W é indefinido.

As Ward fazem o diferencial comutar com a ordenação de Wick. A carga Q₀ em (7.1) é, portanto, a extensão por derivação graduada de bar q e mata o vácuo. Sua simetria também segue diretamente da invariância de ω_W e da regra da involução; sua nilpotência é algébrica.

Escolha uma decomposição linear do complexo bar V em representantes de sua cohomologia e pares exatos. Isso é apenas uma homotopia de vetores do espaço **já determinado por W**, não uma nova escolha de covariância. Para a homotopia h dos pares, bar q h+h bar q=1−p_coh. Ao estendê-la às palavras, o anticomutador com Q₀ conta o número de fatores auxiliares. Dividi-lo pelo inteiro positivo desse número contrai todo setor que contenha um fator auxiliar. Assim

\[
H(\mathcal D_{\rm alg},Q_0)
\simeq \operatorname{Sym}_{\rm gr}H(\bar V,\bar q).
\tag{7.2}
\]

Sob S1–S2, a direita é a Fock bosônica algébrica de H/N_A, concentrada em ghost zero. A forma induzida é a Fock da forma física A: basta escolher representantes fechados e aplicar a mesma regra de contrações. Como A é positiva não degenerada nesse quociente, a forma em (7.2) é positiva e não degenerada. Consequentemente todo vetor fechado nulo de D_alg é Q₀-exato. Isso fornece P₀ **algébrico**.

Se, ao contrário, o bloco (5.4) estiver presente, ele já fornece um vetor negativo no grau de partícula um. Nenhuma segunda quantização pode retirar esse fato sem alterar o espaço, o diferencial ou a covariância que está sendo representada.

## 8. Domínios e obrigação residual precisa

D_alg contém palavras finitas de campos lineares suavizados. Ele não é automaticamente um domínio comum para todos os campos Wick locais e produtos renormalizados de 069: por exemplo, um campo Wick suavizado pode criar uma função de onda de duas partículas que não seja uma soma finita de tensores simples. Uma extensão a espaços completados de funções de onda precisa controlar a continuidade das projeções, das primitivas de (4.4) e da homotopia da seção 7.

Portanto o contrato P₀ pode agora ser desdobrado em passos verificáveis:

1. Escolher efetivamente B_Q^±, B_D^± dentro da família Hadamard 068 e calcular seus radicais na classe de dados declarada.
2. Demonstrar S1 e S2 por mapas explícitos que preservem essa classe. “G é injetivo” não substitui a existência dos x em (4.4).
3. Usar a seção 7 para obter a carga e a positividade no domínio polinomial sem mudar W.
4. Provar que os mapas de homotopia/levantamento preservam um domínio comum dos campos Wick e dos coeficientes interagentes; nesse domínio, verificar de novo a igualdade nulo=imagem, sem trocar imagem algébrica por fecho silenciosamente.

Os passos 1–2 não são verificados pelas identidades 068 já lidas. O passo 3 está demonstrado aqui condicionalmente a eles. O passo 4 permanece analítico. A consequência prática é uma nova especificação de P₀, mais estreita e testável que “existe um estado Hadamard físico”. A construção condicional 072 continua válida sob as hipóteses que ela já declarou.

Não se promove este achado a anomalia interagente, não se altera a contagem física S/V/TT e não se infere refutação da TGL ou inexistência de uma teoria interagente. A nota trata exclusivamente o elo entre a pseudocovariância livre e a representação de estados exigida pelo teorema de positividade formal.
