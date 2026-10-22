# Primitiva covariante de fundo para o setor de divergência do ghost

10/09/2026, arco 072. [DERIVED — demonstração escrita]. Construímos explicitamente uma família de primitivas locais que satisfazem as condições de regularidade, escala e ordem de Q2. A existência é demonstrada nesse setor; não é deduzida da nulidade de uma cohomologia ordinária numa álgebra maior. Nenhum um.py, Lean ou CAS foi executado.

## 1. A pergunta admissível de Q2 e o resultado desta nota

A [construção Q2](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>), §§1–4 e 6, exige contratermos locais e covariantes sob transporte simultâneo dos dados de fundo e dos campos. A quebra é fechada pelo BRST quântico, que conserva os fundos externos. A mesma nota exige ordem finita e as condições de escala/microlocais T1–T11 que importa.

Esses dois usos da palavra covariância não são iguais. No [dicionário BV](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>), §5, a ação sobre os campos completos é

\[
sg=\mathcal L_Cg,\qquad s\phi=\mathcal L_C\phi,\qquad
sC^\mu=C^\nu\partial_\nu C^\mu,\qquad s\bar g=0.
\tag{1.1}
\]

C é o ghost difeomórfico; não é a constante de acoplamento sigma. O fundo \(\bar g\) já é um dado de Q2. Não introduzimos um novo campo físico ou um referencial global.

**Teorema do setor de divergência.** Se \(\mathcal L=\ell\,d^4x\) é uma 4-forma real, de ghost zero, natural nos campos completos g,φ e nos parâmetros escalares constantes, com ordem local finita e

\[
s\ell=\partial_\mu(C^\mu\ell),
\tag{1.2}
\]

então o cociclo local

\[
a_{\mathcal L}=(\bar\nabla_\mu C^\mu)\mathcal L
\tag{1.3}
\]

possui a primitiva covariante de fundo

\[
\boxed{
B_{\mathcal L}=
 \log{\mu_g\over\mu_{\bar g}}\ \mathcal L,\qquad
a_{\mathcal L}=sB_{\mathcal L}-d_H D_{\mathcal L},\qquad
D_{\mathcal L}=\iota_C B_{\mathcal L}.
}
\tag{1.4}
\]

Aqui μ denota a densidade de volume positiva. Sua razão é um escalar positivo; não depende da escolha de coordenadas. A fórmula vale off-shell para quaisquer métricas Lorentzianas não degeneradas do domínio, e coeficiente a coeficiente na expansão formal de Q2. Preserva a ordem diferencial da densidade primitiva, a regularidade suave/analítica pertinente, realidade e escala quase homogênea.

A hipótese (1.2) é verificável: toda densidade antifield-free natural dos campos completos, sem fundo espectador em seus coeficientes, a satisfaz. Por exemplo, μ_g, Rμ_g, os invariantes sigma ou densidades EFT de quatro derivadas pertencem a esse setor. Não se afirma que a anomalia efetivamente gerada pelos grafos seja uma combinação dessas expressões; isso exige identificar seus coeficientes e seus outros setores.

## 2. Razão de volumes: domínio, naturalidade e ausência de um logaritmo matricial global

Defina

\[
b(g,\bar g)=\log{\mu_g\over\mu_{\bar g}}
 ={1\over2}\log{|\det g|\over|\det\bar g|}.
\tag{2.1}
\]

A transformação de ambas as densidades por uma mudança de coordenadas contém o mesmo Jacobiano absoluto, que se cancela. Logo b é um escalar natural sob transporte simultâneo das duas métricas:

\[
b(\psi^*g,\psi^*\bar g)=\psi^*b(g,\bar g).
\tag{2.2}
\]

μ_g/μ_barg é positivo para toda dupla de métricas não degeneradas; b é real e suave, e é real-analítico em seus valores dentro de cada componente não degenerada. Não é necessário escolher e, \(\bar e\), uma raiz quadrada global da métrica, uma base de autovetores ou um logaritmo matricial global.

Na expansão perturbativa g_t=\(\bar g+t h\), ponha \(H=\bar g^{-1}h\). Próximo de t=0, ou como identidade de séries formais,

\[
b(g_t,\bar g)
 ={1\over2}\operatorname{tr}\log(I+tH)
 ={1\over2}\sum_{m\ge1}{(-1)^{m+1}t^m\over m}\operatorname{tr}(H^m).
\tag{2.3}
\]

A identidade matricial é utilizada **somente** nessa vizinhança/série formal. Ela não postula que \(\bar g^{-1}g\) possua um logaritmo principal real para toda dupla Lorentziana distante. A expressão escalar (2.1) já define o objeto exato sem esse postulado.

Os primeiros coeficientes são

\[
b_1={1\over2}\operatorname{tr}H,\qquad
b_2=-{1\over4}\operatorname{tr}H^2,\qquad
b_3={1\over6}\operatorname{tr}H^3.
\]

Cada coeficiente tem grau finito em h, usa apenas \(\bar g^{-1}\) e contém zero derivadas. Não há especialização de uma primitiva formal de outro regime em t=1: a identidade exata (2.1) é demonstrada primeiro, e sua série em torno do fundo é tomada depois.

## 3. Variação BRST e prova componente a componente

A fórmula de Jacobi para a variação do determinante dá

\[
sb={1\over2}g^{\mu\nu}sg_{\mu\nu}
 ={1\over2}g^{\mu\nu}
   (\nabla_\mu C_\nu+\nabla_\nu C_\mu)
 =\nabla_\mu C^\mu.
\tag{3.1}
\]

O denominador de (2.1) não varia por (1.1). Para qualquer vetor, com coeficientes Grassmann inclusive,

\[
\nabla_\mu C^\mu=
 \partial_\mu C^\mu+C^\mu\partial_\mu\log\mu_g,\qquad
\bar\nabla_\mu C^\mu=
 \partial_\mu C^\mu+C^\mu\partial_\mu\log\mu_{\bar g}.
\]

Subtrair as duas expressões produz a identidade exata

\[
\boxed{sb-C^\mu\partial_\mu b=\bar\nabla_\mu C^\mu.}
\tag{3.2}
\]

Portanto b se transforma como um escalar somente sob transporte **simultâneo**; sob s com fundo fixo, o termo adicional à derivada de Lie é a divergência de fundo. É esse termo que permite uma variação de contratermo não trivial.

Para fixar os sinais, calcule diretamente nas densidades. De (1.2),

\[
\begin{aligned}
s(b\ell)
 &= (sb)\ell+b\,\partial_\mu(C^\mu\ell)\\
 &=\partial_\mu(C^\mu b\ell)
   +(sb-C^\mu\partial_\mu b)\ell\\
 &=\partial_\mu(C^\mu b\ell)+(\bar\nabla_\mu C^\mu)\ell.
\end{aligned}
\tag{3.3}
\]

Definindo \(D_{\mathcal L}=C^\mu b\ell\,\iota_{\partial_\mu}d^4x\), temos \(d_HD_{\mathcal L}=\partial_\mu(C^\mu b\ell)d^4x\). Isso prova (1.4) com a convenção de s sobre os componentes do dicionário. Uma convenção bicomplexa que anticomute s e d_H regrada os descendentes de modo correspondente; a igualdade componente (3.3) fixa o conteúdo e não depende de uma escolha implícita de sinal.

Como s²=0, (1.4) implica a condição de consistência sa+d_H(\(\cdots\))=0. Não presumimos a consistência para fabricar a primitiva; ela decorre da construção explícita.

## 4. Uma família funcional maior, ainda com primitiva explícita

Se f é uma função real suave de uma variável e F é uma primitiva real, F'=f, então

\[
\boxed{
f(b)(\bar\nabla_\mu C^\mu)\mathcal L
 =s\bigl[F(b)\mathcal L\bigr]
  -d_H\iota_C\bigl[F(b)\mathcal L\bigr].
}
\tag{4.1}
\]

A prova repete (3.3), usando a regra da cadeia. Se f é analítica no domínio, F pode ser escolhida analítica; se o trabalho é formal em h, basta o germe analítico em b=0. A constante de F acrescenta uma densidade s-fechada módulo d_H e não altera o cociclo. Pode-se normalizar F(0)=0.

Essa família amplia (1.4) sem assumir uma decomposição geral de anomalias. A dependência suave/analítica adicional tem somente o escalar de ordem zero b como argumento. Não se introduzem funções não polinomiais de jatos diferenciados ou denominadores em gradientes.

## 5. Verificação das condições locais de Q2

[KNOWN — contrato primário] Em [Hollands2008, T1–T5, T11 e Teorema2](https://arxiv.org/pdf/0705.3340), a covariância é uma condição distinta de escalamento, suavidade e analiticidade. As ambiguidades são distribuições locais na diagonal, sujeitas também às identidades funcionais e à graduação. A construção Q2 já importou esse contrato para o sistema acoplado. A seguir verificamos as propriedades da densidade construída, sem importar uma remoção de anomalias de outro modelo.

**Naturalidade.** b é natural pelo cancelamento dos Jacobianos em (2.2); \(\mathcal L\) é natural por hipótese. A divergência \(\bar\nabla C\) também é natural nos dados de fundo e no ghost transportados simultaneamente. Assim B,a,D são definidos sem escolha de coordenadas. b não depende de φ ou de uma carta no alvo, de modo que sua multiplicação conserva a globalidade já existente de \(\mathcal L\) em S³.

**Regularidade.** Os coeficientes de (2.3) são contrações racionais em valores não degenerados de \(\bar g\), logo analíticos nesses valores. Para uma família suave/analítica de todos os dados, B preserva a regularidade de \(\mathcal L\). Isso verifica uma propriedade mais forte que mera suavidade para este fator. Não se usa uma partição de unidade C∞ do alvo para afirmar analiticidade. Na família (4.1), o mesmo vale quando F tem a regularidade requerida.

**Ordem e finitude perturbativa.** Multiplicar \(\mathcal L\) por F(b) não acrescenta derivadas. Se \(\mathcal L\) tem ordem de jato r, o contratermo tem ordem no máximo r. Se \(\mathcal L=\sum_{n\ge0}t^n\mathcal L_n\), o coeficiente de t^N do produto é uma soma finita de coeficientes com índices até N. Cada parcela é polinomial finita em h e nos outros campos perturbativos. A série não precisa convergir para definir esses coeficientes.

A quantidade de pernas pode crescer; a ordem diferencial não cresce por esse fator. Assim, se o termo de \(\mathcal L\) pertence ao teto diferencial EFT da ordem examinada, o contratermo também pertence. Não se promete manter um teto arbitrário de número de pernas quando Q2 usa uma expansão formal com infinitos vértices. Contratermos de laço constantes, lineares ou quadráticos seguem as regras já declaradas em Q2.

**Escala.** Para a rescalagem geométrica simultânea

\[
g\mapsto\lambda^2g,\qquad \bar g\mapsto\lambda^2\bar g,\qquad \lambda>0,
\]

a razão de volumes é invariável: \(b\mapsto b\). Logo, se \(\mathcal L_\lambda\) satisfaz uma lei quase homogênea de peso w e ordem logarítmica N,

\[
(\lambda\partial_\lambda-w)^N\mathcal L_\lambda=0,
\]

então

\[
(\lambda\partial_\lambda-w)^N
 \bigl[F(b)\mathcal L_\lambda\bigr]=0.
\tag{5.1}
\]

Não se acrescenta uma potência de log λ. As escalas dos campos normalizados e acoplamentos são as da densidade \(\mathcal L\); o fator b é dimensionless sob a transformação simultânea. Não se substitui essa lei por uma rescalagem arbitrária das coordenadas.

**Suporte e frente de onda.** Para teste χ de suporte compacto interior, o funcional \(\int\chi B\) tem suporte dentro de supp χ. Suas derivadas funcionais têm suporte na diagonal e são somas finitas de derivadas de delta com coeficientes locais da regularidade indicada. Multiplicar pelo fator de ordem zero não introduz uma frente de onda nova fora do conormal da diagonal nem um inverso diferencial no espaço-tempo. A polarização em ordem perturbativa fixa fornece kernels locais de ordem finita.

**Realidade.** Para g,\(\bar g\),\(\mathcal L\) reais, b e B são reais. O dicionário admite C*=C; como bℓ é par e real, a e D têm a involução compatível. Não se alteram sinais do antighost, de anticampos ou das contrações de Feynman: eles não entram nesta primitiva.

A conclusão desta seção é que B pertence ao espaço de **densidades locais EFT** com essas condições de Q2. O encaixe numa hierarquia completa de mudanças finitas de todos os T_n mantém as suas condições de multilinearidade/identidades funcionais e deve usar a polarização correspondente. A nota não declara que qualquer escolha isolada de kernels, sem essas identidades, já defina outra prescrição T_n.

## 6. Cutoff: o termo de derivada não é apagado

Com sχ=0, integrar (1.4) dá

\[
s\int\chi B_{\mathcal L}
 =\int\chi a_{\mathcal L}
  -\int d\chi\wedge D_{\mathcal L}.
\tag{6.1}
\]

O sinal segue de \(\int\chi dD=-\int d\chi\wedge D\). Na região em que χ é constante, o termo extra desaparece; globalmente com cutoff, ele permanece explicitamente. Essa é a mesma distinção de Q2 entre identidade local na região de interação constante e contatos/termos de borda do cutoff. Nenhum limite adiabático de estados é presumido.

## 7. Troca de referência: identidade local, não independência de fundo

Se duas referências \(\bar g_1,\bar g_2\) são usadas e

\[
\sigma=\log{\mu_{\bar g_1}\over\mu_{\bar g_2}},
\]

então \(b_2-b_1=\sigma\), com sσ=0. Os contratermos e os representantes diferem por

\[
B_2-B_1=\sigma\mathcal L,\qquad
a_2-a_1=-C^\mu\partial_\mu\sigma\,\mathcal L
       =s(\sigma\mathcal L)-d_H\iota_C(\sigma\mathcal L).
\tag{7.1}
\]

A igualdade das divergências de fundo verifica o mesmo sinal. A diferença é uma renormalização local na classe ampliada dos dois fundos. Isso não constrói a conexão de comparação entre álgebras, não prova sua planicidade e não afirma independência quântica da cisão de fundo.

## 8. Por que isso é uma resposta concreta ao controle logdet, mas não ao caso geral

O corolário071 mostrou que a forma racional \(d(\det e)/\det e\) tem uma primitiva suave log(det e) que não é racional e não é escalar sob transporte do único vielbein. Essa observação delimitava a álgebra. Em Q2, a referência métrica já está disponível. A diferença dos logaritmos torna-se o escalar b, e sua expansão (2.3) tem coeficientes racionais nos valores do fundo e polinomiais finitos nas flutuações.

Portanto **esse** impedimento de apresentação não bloqueia a primitiva (1.4) na classe perturbativa de Q2. O alargamento necessário não é uma função não local ou um coeficiente arbitrário dos jatos: é um escalar local de ordem zero construído dos dois volumes.

Há, entretanto, uma razão algébrica para não dizer que basta tornar toda primitiva “básica”. No complexo covariante completo071, um elemento sem ghost de Lorentz tem

\[
\mathrm{gh}=\deg_\xi-\mathrm{antigh},\qquad \deg_\xi\le4.
\]

Um elemento básico de ghost 4 só pode ter ξ-grau4 e antifield zero. É ΘL(T); sua variação s básica tem ξ-grau5 e é zero. Portanto uma primitiva geral de ghost4 para um cociclo total de ghost5 não pode ser transformada arbitrariamente numa expressão básica do **mesmo gauge completo** mantendo esse cociclo não nulo. A retirada finita de ghosts usada no grau2 de071 não pode ser repetida por nomenclatura no grau5.

A covariância simultânea exigida por Q2 é uma condição relativa aos dados de fundo. Seu complexo e sua descida precisam ser construídos; não são o subcomplexo básico do único campo completo. A fórmula (3.2) oferece um exemplo exato dessa diferença.

**Resultado retirado:** o setor \((\bar\nabla\cdot C)\mathcal L\), e a família (4.1), têm primitivas reais, locais, covariantes de fundo, suaves/analíticas e compatíveis com a escala/ordem da densidade escolhida.

**[OPEN]** Não demonstramos que toda anomalia gravitacional/sigma de Q2 pertença a esse setor. Permanecem a comparação geral dos complexos com fundos espectadores, a transferência de primitivas às identidades completas de renormalização e a remoção indutiva da quebra efetiva. Não se afirma QME, estado físico interagente, ausência de anomalias globais ou completude UV.
