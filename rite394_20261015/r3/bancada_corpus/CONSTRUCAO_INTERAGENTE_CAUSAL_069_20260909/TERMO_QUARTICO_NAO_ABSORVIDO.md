# Um termo de uma volta não absorvido pelos parâmetros da ação de duas derivadas

09/09/2026. [DERIVED — demonstração escrita condicionada ao coeficiente acoplado calculado em 069]. O alcance é a prescrição de operadores normalizados e a classe local covariante de contratermos explicitadas abaixo. Não é uma afirmação de impossibilidade de toda rota UV da TGL.

## 1. O coeficiente utilizado e seu alcance

A frente [calor completo 069](<C:/IALD/Central de Patentes/Chatgpt/CALOR_COMPLETO_EINSTEIN_SIGMA_069_20260909_224252_371553/VERIFICACAO_CALOR_COMPLETO.json>) calcula a combinação de uma volta \(\frac12\operatorname{tr}_{13}b_4-\operatorname{tr}_4b_4^{\rm ghost}\) no sistema Einstein–sigma gauge fixado, com o auxiliar tratado algebricamente. No fundo físico, com \(x=a^{-2}\), o resultado incluindo derivadas totais é
\[
\mathcal C_4(x)=\frac{7440x^2+1616x-211}{96}
=\frac{155}{2}x^2+\frac{101}{6}x-\frac{211}{96}.
\tag{1}
\]
Essa é a densidade escalar local da divergência na prescrição descrita pela nota de cálculo, multiplicada pelo fator universal e por μ_g. A conta usa o sistema acoplado, com os graus físicos e os fantasmas, e não apenas o sigma em métrica externa. A interpretação como coeficiente covariante local é distinta da existência de um núcleo de calor lorentziano global, de uma rotação de Wick global ou de uma integral funcional convergente. Fatores de medida/contorno são os declarados na frente de cálculo.

## 2. Teste funcional no fundo

Use \(a=2\cos(r/2)\), \(H=\dot a/a\), \(H^2=x-1/4\) e \(\dot H=-x\). Então
\[
\dot x=-2Hx,\qquad \ddot x=6x^2-x,\qquad
\Box x=\ddot x+3H\dot x=\frac x2.
\tag{2}
\]
As invariantes do mesmo fundo são
\[
Q=-3x,\quad W_{\mu\nu}W^{\mu\nu}=3x^2,\quad
R=3-12x,
\]
\[
\operatorname{Ric}^2=48x^2-18x+\frac94,\qquad
\operatorname{Riem}^2=48x^2-12x+\frac32.
\tag{3}
\]
Consequentemente a densidade de Euler, sem seu fator topológico de normalização, é
\[
\mathcal E_4=\operatorname{Riem}^2-4\operatorname{Ric}^2+R^2
=\frac32-12x.
\tag{4}
\]
Pontryagin vale zero nesse fundo FRW. De (2), \(\Box R=-6x\) e \(\Box Q=-3x/2\). Os valores x percorrem um intervalo aberto; não são uma constante escolhida num único ponto.

Renormalizar somente os coeficientes dos termos originais \(\mu_g,\mu_g R,\mu_g Q\) produz, sobre esse fundo, apenas combinações \(\mu_g(A+Bx)\), com A,B constantes. Adicionar Euler, Pontryagin, □R ou □Q tampouco produz x². Redefinições locais de campos acrescentam termos proporcionais às equações completas e divergências; as equações se anulam no fundo usado.

Portanto não existem A,B constantes tais que \(\mathcal C_4(x)=A+Bx\) em todo o intervalo: a segunda derivada de (1) em x é 155. Esse teste de dependência funcional exclui uma absorção pelos termos listados, sem escolher um ponto ou ajustar uma constante a uma amostra isolada.

## 3. Por que as divergências totais pertinentes não escondem x²

A classe aqui utilizada é: densidades naturais sob difeomorfismos, invariantes pela isometria O(4) do alvo S³, polinomiais nos jatos derivados, sem denominadores em gradientes ou invariantes de curvatura, na ordem de até quatro derivadas da EFT. Coeficientes podem depender das constantes do modelo. A divergência total correspondente tem uma corrente de até três derivadas. Não se introduzem campos de relógio adicionais ou coordenadas preferidas nessa classe ambiente.

Nessa ordem, correntes métricas singletas de três derivadas reduzem a ∇R pela Bianchi contraída. Uma corrente da matéria com três derivadas e dois índices de alvo contraídos é combinação de \(\langle u^\nu,D_\mu u_\nu\rangle=\frac12\nabla_\mu Q\) e \(\langle u_\mu,\tau\rangle\), com \(\tau=D_\nu u^\nu\). O alvo não possui um vetor ou uma 1-forma O(4)-invariante que permita uma corrente linear em uma derivada, nem um tensor invariante de três índices que forme uma corrente cúbica polar. Termos de curvatura alvo não geram novos tensores nessa contagem, pois sua curvatura é constante e construída da métrica.

Se se exigir apenas a isometria orientada SO(4), pode aparecer a dual da 3-forma pullback do volume de S³. Sua divergência é zero porque essa 3-forma é fechada. Correntes não tensoriais de Chern–Simons são excluídas como correntes covariantes, mas suas divergências características Euler/Pontryagin já foram permitidas separadamente em (4).

O mapa identidade satisfaz τ=0 em todo o domínio. Assim as divergências totais da classe reduzem, nesse fundo, a □R, □Q ou zero; todas são afins em x. Essa enumeração não vale para correntes arbitrárias de ordem superior, expressões localizadas em gradientes não nulos ou prescrições com novos campos. Tais extensões não foram usadas para provar (1) nem são renormalizações apenas dos três coeficientes originais.

## 4. Conclusão limitada, mas efetiva

[DERIVED] Sob o coeficiente acoplado (1) e a classe de contratermos da seção 3, a divergência de uma volta não é absorvível apenas por mudanças dos parâmetros da ação de duas derivadas, mesmo permitindo os termos topológicos, divergências totais pertinentes e termos de equações. É necessário admitir operadores independentes de quatro derivadas. Isso dá conteúdo concreto à ampliação EFT, já permitida pela construção causal Q2.

O resultado não prova que todos os termos de quatro derivadas sejam independentes, não seleciona seus coeficientes finitos, não calcula uma anomalia de número fantasma um e não fecha a rota UV. Uma escolha distinta de medida que acrescente uma densidade local desse tipo terá introduzido a mesma informação adicional que precisa ser declarada; ela não será contada como simples renormalização de κ,c,Λ dentro da classe acima.

Não houve execução Lean ou alteração de originais. O adendo é uma demonstração de não absorção na classe especificada, apoiada no cálculo acoplado e em suas hipóteses, com as equações intermediárias exibidas para revisão.
