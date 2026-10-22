# Comutante escalar no domínio suave e nilpotência condicional da carga

10/09/2026, arco 073. [DERIVED — demonstração escrita]. Corolário novo da representação `FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md`. As fontes permanecem intactas; nenhum um.py, Lean ou CAS foi executado.

**Resultado:** a comutante dos campos livres de uma faixa de Cauchy completa é escalar entre os endomorfismos do domínio suave que são contínuos grau a grau e têm aumento finito do número de partículas. A mesma conclusão vale coeficiente a coeficiente para campos deformados cujo termo inicial é esse conjunto livre. Portanto, se uma carga ímpar Q(z) implementa um diferencial interagente nilpotente nesse domínio, então Q(z)²=0 sobre o anel C[[z]] com parâmetros de ghost zero. A implementação e a nilpotência do diferencial continuam hipóteses: este corolário não constrói a corrente ou demonstra a QME.

## 1. Domínio e classe de operadores: onde entra a continuidade

Conserve o domínio da fonte Fock073:

\[
\mathscr D=\bigoplus_{N\geq0}^{\mathrm{alg}}D_N,
\qquad D_N=\operatorname{Sym}_{\rm gr}^{N}
  (E_+^{\widehat\otimes N}),\qquad D_0=\mathbb C\Omega.
\tag{1.1}
\]

E₊ é o espaço nuclear de dados suaves de uma partícula nas imagens da polarização, com todos os setores físicos e auxiliares. Cada D_N tem sua topologia nuclear de funções suaves simetrizadas/antissimetrizadas sobre produtos de S³. A soma dos graus de partícula é finita em cada vetor; o produto tensorial dentro de um grau é completado.

Seja End_fin,∞(D) a classe de operadores lineares B para os quais existe d_B finito, não negativo, tal que

\[
B D_N\subset\bigoplus_{M=0}^{N+d_B}D_M
\quad\text{e}\quad
B|_{D_N}:D_N\longrightarrow\bigoplus_{M=0}^{N+d_B}D_M
\text{ é contínuo para cada }N.
\tag{1.2}
\]

Somas e composições preservam essa classe: para a composição, há somente um número finito de graus intermediários, e os aumentos de partículas se somam. A fonte Fock073, §5, fornece (1.2) para cada coeficiente Wick polinomial compacto microcausal. Consumo esse resultado; não substituo sua prova microlocal por uma alegação de continuidade Hilbert limitada.

O subespaço de tensores simples de cada D_N é denso **na topologia de D_N**, por definição do produto tensorial nuclear completado. A simetrização graduada é contínua, portanto as palavras de criadores sobre Ω são densas nessa mesma topologia em cada grau. Essa é a densidade que será usada para B. A mera densidade de D na Fock Hilbert não bastaria para um endomorfismo arbitrário.

## 2. A faixa de Cauchy completa fornece todos os criadores e aniquiladores

Seja O=I₀×S³ uma faixa aberta interior que contém uma superfície de Cauchy completa do fundo. Incluem-se todos os campos do sistema BRST livre, com testes complexos suaves compactamente suportados em O. Não se usa somente a álgebra de observáveis físicos nem uma região espacial própria.

Para qualquer solução suave Ψ do operador completo L, escolha χ temporal, zero antes de uma pequena subfaixa e um depois dela, com as transições contidas em I₀. Então

\[
f=L(\chi\Psi)=[L,\chi]\Psi
\tag{2.1}
\]

é suave e compacto: S³ é compacta e o comutador está suportado na transição temporal. As soluções retardada e avançada de f são χΨ e (χ−1)Ψ, respectivamente, pela unicidade com suporte causal. Para E_L=G_ret−G_adv,

\[
E_L f=\Psi.
\tag{2.2}
\]

Esse argumento usa os Green completos da fonte068 e vale também com o campo auxiliar b: L pode conter blocos algébricos, pois o cálculo por comutador e a identidade dos Green continuam válidos. Assim a faixa realiza todos os dados de Cauchy suaves do complexo, e não apenas dados de um subconjunto de harmônicos.

Os projetores puros e a conjugação real de073 permitem escolher esses dados em um ramo ou no ramo conjugado. Ao complexificar os testes, a decomposição do campo em criador e aniquilador separa-se: um ramo fornece somente criação e o outro somente aniquilação, com a orientação e as fases fixadas na fonte. A simetria fundamental que converte os aniquiladores de Krein em aniquiladores Hilbert preserva dados suaves e é invertível; portanto o conjunto obtido contém a totalidade dos criadores e aniquiladores suaves de todos os setores, após as mudanças constantes de base já documentadas.

Consequentemente, comutar com todos os campos dessa faixa implica comutar com todos esses criadores e aniquiladores. Essa extração usa a faixa completa e a polarização. Não se invoca um teorema de irreducibilidade de uma pequena álgebra local.

## 3. Lema da comutante ordinária

**Lema.** Se B∈End_fin,∞(D) e

\[
[B,\Phi(f)]=0
\tag{3.1}
\]

para todos os campos e testes da seção 2, então existe c∈C tal que B=cI em D.

**Prova.** Como B comuta com os aniquiladores a(v),

\[
a(v)B\Omega=B a(v)\Omega=0
\quad\text{para todo dado suave }v.
\tag{3.2}
\]

O kernel comum desses aniquiladores, dentro de D, é CΩ. Para verificar, decomponha um vetor no número finito de graus de partícula que ele possui. Em cada grau positivo N, aniquilar com todos os dados suaves significa que todas as contrações de um slot de sua função de onda são zero. Os dados suaves são densos no espaço Hilbert de uma partícula e essas contrações são contínuas no grau N; logo todos os coeficientes tensorais são zero. Equivalentemente, uma base Hilbert com elementos suaves separa essas contrações. Isso vale nos setores bosônicos e fermionicos e suas somas, e independe do sinal da forma de Krein porque a simetria fundamental fornece o conjunto completo de aniquiladores Hilbert.

Portanto BΩ=cΩ. Comutar B sucessivamente com os criadores dá

\[
B,a^\dagger(v_1)\cdots a^\dagger(v_N)\Omega
=c\,a^\dagger(v_1)\cdots a^\dagger(v_N)\Omega.
\tag{3.3}
\]

Em cada N, as combinações dessas palavras são densas em D_N na topologia nuclear. Por (1.2), B−cI é contínuo de D_N para uma soma finita de espaços D_M, que é Hausdorff. Logo (3.3) vale em todo D_N. A soma algébrica sobre N fornece B=cI em D. ∎

A continuidade foi usada exatamente na passagem das palavras finitas para funções de onda suaves completadas. Não foi inferida do fato de B ser um operador definido num domínio Hilbert denso.

## 4. Comutante de campos formalmente deformados

Trabalhe sobre C[[z]], com z par e ghost zero. Cada coeficiente dos operadores abaixo pertence a End_fin,∞(D); não se requer uma cota uniforme de d_B em todas as ordens de z. Uma soma ou produto formal tem somente um número finito de termos em cada coeficiente.

Seja Φ_z(f)=Φ₀(f)+Σ_{n≥1}zⁿΦ_n(f), para todos os geradores da seção 2, e B(z)=Σ_{n≥0}zⁿB_n. Se

\[
[B(z),\Phi_z(f)]=0
\quad\text{para todo }f,
\tag{4.1}
\]

então B(z)=c(z)I para algum c(z)∈C[[z]].

**Prova por recorrência.** A ordem zero de (4.1) e o lema dão B₀=c₀I. Suponha B_j=c_jI para j<n. A ordem n de (4.1) é

\[
[B_n,\Phi_0(f)]+\sum_{j=0}^{n-1}[c_jI,\Phi_{n-j}(f)]=0.
\]

A soma é zero, portanto o lema dá B_n=c_nI. ∎

Não se alegou que os campos deformados possuam uma polarização interagente. A polarização é usada somente no termo livre inicial que controla a recorrência.

## 5. Corolário condicional para Q(z)²

**Hipóteses novas, não demonstradas aqui:** existe uma família Q(z)=ΣzⁿQ_n, ímpar de ghost +1, com Q_n∈End_fin,∞(D), e um diferencial representado d_z na álgebra dos campos deformados da faixa, tal que

\[
d_z A={i\over\hbar}[Q(z),A]_{\rm gr},\qquad d_z^2 A=0.
\tag{5.1}
\]

Fixe ħ real não nulo como normalização; a série é formal em z. As igualdades são de operadores em D[[z]], não somente identidades de funcionais antes de representação. Devem valer para o conjunto completo de campos usado acima.

Para Q ímpar, o cálculo graduado exato dá

\[
[Q,[Q,A]_{\rm gr}]_{\rm gr}=[Q^2,A],
\qquad
d_z^2 A=-\hbar^{-2}[Q(z)^2,A].
\tag{5.2}
\]

Logo Q(z)² comuta com todos os Φ_z(f). Seus coeficientes são somas finitas de composições Q_iQ_j e pertencem à classe (1.2). A seção 4 implica

\[
Q(z)^2=c(z)I.
\tag{5.3}
\]

Cada coeficiente do lado esquerdo tem ghost +2, enquanto c(z)I tem ghost zero. Como o domínio tem graduação direta, Ω tem ghost zero e z e os escalares têm ghost zero, aplicar (5.3) ao vácuo força cada c_n=0. Portanto

\[
\boxed{Q(z)^2=0\quad\text{em }\mathscr D[[z]].}
\tag{5.4}
\]

Não se exige que Q(z) anule o vácuo livre. O uso do vácuo na última frase serve apenas para distinguir os graus de ghost de um operador escalar.

**Limite essencial dos coeficientes:** se o anel for ampliado por uma fonte central Ω_ext de ghost +2, Ω_ext I é central e possui exatamente o grau de Q². O argumento de graduação deixa então de eliminá-lo. Este corolário é sobre C[[z]] — ou uma extensão escalar inteiramente de ghost zero — depois de especializar fontes externas de ghost não nulo a zero. Não transporta automaticamente a conclusão para a álgebra de fontes de referência da frente072.

## 6. Supercomutante e uma consequência adicional de simetria

O mesmo método prova que a supercomutante é C·I em paridade par e zero em paridade ímpar. De fato, se T é ímpar e supercomuta com todos os criadores e aniquiladores, as relações com os aniquiladores ainda forçam TΩ=cΩ. Mas TΩ tem paridade ímpar e Ω tem paridade par, de modo que c=0. Supercomutar pelos criadores dá T=0 nas palavras; a continuidade nuclear estende a igualdade a D. A recorrência da seção 4 transporta essa conclusão para uma família formal ímpar supercentral.

Assim há ainda o seguinte corolário **condicional**. Suponha que Q(z) possua adjunto de Krein Q(z)^× no mesmo domínio, também com coeficientes na classe (1.2), e que a involução representada satisfaça, para A homogêneo,

\[
d_z(A^\times)=(-1)^{|A|}(d_z A)^\times.
\tag{6.1}
\]

Conserve z real pela involução. A relação (5.1) e a identidade

\[
[Q,A]_{\rm gr}^{\times}=-(-1)^{|A|}[Q^{\times},A^{\times}]_{\rm gr}
\]

mostram que Q−Q^× supercomuta com os campos. Esse operador é ímpar, logo a supercomutante formal dá Q=Q^× em D[[z]]. Isso demonstra simetria **se** o adjunto comum e a compatibilidade (6.1) estiverem construídos. Não afirma existência desse adjunto, fecho de operadores ou auto-adjunticidade Hilbert da carga nilpotente.

## 7. Relação com a construção perturbativa e fronteira

[KNOWN] [Dütsch–Fredenhagen, §§4.2–4.3, equação (4.8) e Teorema 4](https://arxiv.org/pdf/hep-th/9807078v2) formulam a estabilidade formal da positividade sob hipóteses sobre a carga e o espaço livre. [Rejzner, Teorema 4.2](https://arxiv.org/pdf/1301.7037v3) relaciona a carga interagente ao diferencial quântico sob identidades renormalizadas específicas. Esses resultados não dispensam a demonstração das hipóteses para o Einstein–sigma presente.

O corolário acima fornece um elo concreto: uma vez paga a implementação de um diferencial nilpotente na faixa completa, não sobra uma ambiguidade escalar de ghost +2 sobre C[[z]]. A prova073 de P₀ e do domínio Wick, combinada com essa nilpotência e com a simetria necessária, torna aplicável a recorrência condicional072 no domínio correto.

Continuam fora deste resultado: construção de d_z e sua QME; corrente renormalizada conservada; implementação de (5.1) e contatos; independência de cutoff ou de fundo; convergência da série; estado não perturbativo e UV. A comutante de uma pequena região espacial não foi identificada com escalares. O corolário usa expressamente toda uma faixa de Cauchy.
