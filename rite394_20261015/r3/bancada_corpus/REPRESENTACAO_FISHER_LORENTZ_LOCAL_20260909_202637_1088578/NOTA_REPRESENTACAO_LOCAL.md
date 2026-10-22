# Toda métrica lorentziana suave admite representação local por Fisher refletida

[DERIVED — demonstração em texto, sem compilação Lean] A construção proposta é válida. Adota-se a assinatura (+,-,…,-), e a métrica de Fisher de uma família finita positiva é definida sem fator adicional por `Fisher(P)=Σᵢ dPᵢ⊗dPᵢ/Pᵢ`. A existência do mergulho isométrico suave usado abaixo é [KNOWN — teorema de Nash, fonte primária indicada]. O argumento não é um resultado compilado no kernel desta rodada.

**Enunciado local.** Se `g` é uma métrica lorentziana `C∞` de dimensão `n≥2` e `x₀` é um ponto, existem uma vizinhança `V` de `x₀` e funções `C∞`, `P₀,…,P₂N>0`, com soma igual a um, tais que `F=Fisher(P)` é positiva definida, `c=dP₀` nunca se anula e

\[
g=\frac{2c\otimes c}{F^{-1}(c,c)}-F.
\]

O número de probabilidades é finito e pode depender do limite dimensional escolhido para o mergulho. A construção abaixo permite `N=n(3n+11)/2`; em dimensão quatro, são `N=46` coordenadas euclidianas e `2N+1=93` probabilidades. Não se afirma minimalidade.

## 1. Escolha de um relógio local pequeno

Escolha uma coordenada suave `τ`, com `τ(x₀)=0`, cujo diferencial seja temporal em `x₀`. A condição `a=g⁻¹(dτ,dτ)>0` é aberta. Portanto, após restringir uma carta relativamente compacta `U`, ela vale em toda `U`, e `a+τ²` é limitada superiormente por algum `M>0`.

Escolha `ε>0` com `ε²M<1/4` e defina

\[
q=\tfrac12+\varepsilon\tau,\qquad c=dq,\qquad
b=g^{-1}(c,c)=\varepsilon^2a>0.
\]

Então `0<q<1` e

\[
b<q(1-q)=\tfrac14-\varepsilon^2\tau^2.
\]

Essa desigualdade é obtida uniformemente na vizinhança escolhida. Em particular, `c≠0`.

## 2. Reflexão positiva e seu inverso

Defina

\[
F=\frac{2}{b}\,c\otimes c-g.
\]

Se `v=g♯c`, então `c(v)=g(v,v)=b`. Todo vetor tangente tem decomposição única `X=λv+w`, com `c(w)=0`. O complemento ortogonal de um vetor temporal, na assinatura adotada, é negativo definido. Consequentemente,

\[
F(X,X)=\lambda^2b-g(w,w)>0\quad (X\ne0).
\]

Assim, `F` é uma métrica riemanniana suave. Além disso, para qualquer vetor `X`,

\[
F(v,X)=2c(X)-g(v,X)=c(X).
\]

Logo `F♯c=v` e **`F⁻¹(c,c)=b`**. Esta identidade verifica que o denominador da reflexão final é de fato o inverso de `F`, embora `b` tenha sido inicialmente definido usando o inverso de `g`. Portanto,

\[
\frac{2c\otimes c}{F^{-1}(c,c)}-F=g.
\]

## 3. Reserva positiva para as probabilidades restantes

Pela desigualdade de Cauchy–Schwarz de `F`,

\[
c(X)^2=F(v,X)^2\le F(v,v)F(X,X)=bF(X,X).
\]

Defina

\[
H=\frac{F-c\otimes c/[q(1-q)]}{1-q}.
\]

Segue a estimativa explícita de formas quadráticas

\[
H(X,X)\ge
\frac{1-b/[q(1-q)]}{1-q}\,F(X,X)>0\quad(X\ne0).
\]

Portanto, `H` é riemanniana suave. Não basta apenas `b>0`: a margem estrita `b<q(1-q)` é o passo que assegura a positividade desta reserva.

## 4. Nash e realização na esfera de raio dois

É suficiente uma versão compacta de Nash. Dentro da carta, tome vizinhanças `U₂ ⊂⊂ U₁ ⊂⊂ U`. Identifique `U₁` com um aberto de `Sⁿ`, escolha uma função de corte `χ` igual a um em `U₂`, com suporte em `U₁`, e uma métrica suave positiva `h₀` em `Sⁿ`. A combinação `χH+(1−χ)h₀`, definida como `h₀` fora do suporte, é suave, positiva e coincide com `H` em `U₂`.

O Teorema 2 de Nash, p. 59, dá mergulho isométrico de métricas compactas `Cᵏ`, para `3≤k≤∞`, em dimensão euclidiana `n(3n+11)/2`. Aplicado à extensão acima e restrito a `U₂`, fornece `y=(y₁,…,y_N)` suave com `Σⱼdyⱼ⊗dyⱼ=H`. [Nash, *The Imbedding Problem for Riemannian Manifolds*, Annals of Mathematics 63 (1956), 20–63, Teorema 2](https://mccuan.math.gatech.edu/courses/6455/nash55.pdf); [registro DOI do artigo](https://doi.org/10.2307/1969989).

Escolha constantes `aⱼ>0` com `Σⱼaⱼ²=4` e defina, para `j=1,…,N`, o par

\[
\Psi_{2j-1}=a_j\cos(y_j/a_j),\qquad
\Psi_{2j}=a_j\sin(y_j/a_j).
\]

Temos `ΣₗΨₗ²=4` e

\[
\sum_{\ell=1}^{2N}d\Psi_\ell\otimes d\Psi_\ell
=\sum_{j=1}^{N}dy_j\otimes dy_j=H.
\]

Uma transformação ortogonal **constante** leva `Ψ(x₀)` ao vetor da esfera de raio dois cujas `2N` coordenadas são todas `2/√(2N)>0`. Aplicando-a a toda a aplicação `Ψ`, preservamos a norma e a métrica induzida. Por continuidade, depois de restringir novamente a vizinhança, todas as coordenadas são estritamente positivas. É essencial que a rotação seja constante; uma rotação dependente do ponto introduziria termos de derivada.

Escreva `Qₗ=Ψₗ²/4`. Então `Qₗ>0`, `ΣₗQₗ=1` e

\[
\frac{dQ_\ell\otimes dQ_\ell}{Q_\ell}
=d\Psi_\ell\otimes d\Psi_\ell,
\qquad \operatorname{Fisher}(Q)=H.
\]

## 5. Inclusão do relógio como a própria probabilidade zero

Defina `P₀=q` e `Pₗ=(1−q)Qₗ` para `ℓ≥1`. Todas são suaves e positivas; sua soma é um. Usando `ΣₗQₗ=1` e `ΣₗdQₗ=0`, os termos cruzados cancelam e obtemos

\[
\begin{aligned}
\operatorname{Fisher}(P)
&=\frac{dq\otimes dq}{q}
 +\frac{dq\otimes dq}{1-q}
 +(1-q)\operatorname{Fisher}(Q)\\
&=\frac{dq\otimes dq}{q(1-q)}+(1-q)H=F.
\end{aligned}
\]

Como `dP₀=dq=c`, a reflexão de Fisher com o relógio exigido devolve exatamente `g`. Isso conclui a demonstração local.

## Alcance e questões que esta representação não resolve

- [DERIVED] Há cobertura cinemática local de toda métrica lorentziana suave da assinatura escolhida por uma família finita suficientemente grande de probabilidades. O relógio é o diferencial de uma das próprias probabilidades.
- [INPUT na construção] A métrica `g` é fornecida primeiro; as probabilidades são escolhidas a partir dela. Isso não prova que as probabilidades produzidas pelo registro físico TGL satisfaçam a reconstrução desejada.
- [OPEN] Não se deduzem equações de Einstein, lei de área, matéria, regularidade de soluções dinâmicas ou seleção física a partir da existência dessa representação.
- [OPEN] Não se prova cobertura por cinco probabilidades, nem por qualquer alfabeto fixado anteriormente no modelo. Um limite suficiente obtido por Nash não demonstra minimalidade nem compatibilidade automática com um registro que usa outro número de componentes.
- [OPEN] A construção é local. Uma representação global exigiria, entre outras condições, um `P₀` global com diferencial temporal não nulo; isso é uma exigência geométrica adicional. A rotação que torna todas as coordenadas positivas foi justificada apenas numa vizinhança.
- [OPEN] Nenhuma estimativa de dependência contínua ou estável das escolhas de Nash/`P` em função de `g` foi estabelecida. A obstrução anterior à estabilidade geral da decodificação por caráter continua válida.

Não houve execução Lean, integração, execução/importação de `um.py` ou alteração de arquivos existentes nesta revisão. A nota é nova e não atribui aprovação física ou compilação formal a esta demonstração em texto.
