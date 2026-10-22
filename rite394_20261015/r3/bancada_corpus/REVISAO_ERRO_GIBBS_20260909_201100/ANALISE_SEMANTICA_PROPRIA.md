# Revisão semântica: erro finito, Taylor Gibbs e janela de amostragem

09/09/2026. Análise própria desta tarefa, a partir das fontes e dos recibos indicados no manifesto acompanhante. Não é aprovação em nome do operador nem de outro agente. Nenhuma fonte revisada foi editada; não foi iniciada recompilação. A compilação e a análise matemática são evidências distintas.

**Conclusão da análise:** as constantes e os encadeamentos matemáticos conferem no escopo declarado. O resultado limita erros das componentes do tensor decodificado para g e gInv fixos. O ruído permanece uma hipótese de medição; o resto de Taylor é deduzido do protocolo; a janela de tempo tem raio positivo explícito. A cota explícita adicional M(k) abaixo é uma dedução escrita e ainda não é o conteúdo Lean dessas três folhas.

## 1. Propagação de erros: constantes verificadas

Em `FiniteResponseErrorBounds.lean`, linhas 18–37, o decodificador mantém quatro amostras como diagonais e usa (s_ij−s_i−s_j)/2 nas seis entradas independentes fora da diagonal. Se cada amostra tem erro absoluto ≤δ, cada diagonal tem erro ≤δ e cada entrada fora da diagonal ≤(δ+δ+δ)/2=3δ/2. Para δ≥0, a cota comum **3δ/2** está correta. É uma cota por componente, na base das dez direções escolhidas, e não uma norma tensorial independente de coordenadas.

Nas linhas 39–44, a normalização é exatamente `s/(-Real.pi)`, conforme a definição importada de `normalizedSamples`. O módulo do denominador é π>0, logo o erro das amostras normalizadas é δ/π. O sinal não desaparece no modelo: a resposta Gibbs é negativa, e a divisão por −π devolve o quadrático positivo da fonte antes da reversão do traço.

Nas linhas 46–64,

\[
|\operatorname{tr}(gInv(A-C))|
\le\sum_{i,j=0}^3|gInv_{ij}|\,|(A-C)_{ji}|
\le16B\epsilon.
\]

Existem exatamente 4×4 termos. A transposição dos índices do erro é a que o produto matricial exige; não falta fator de dimensão.

Nas linhas 66–88, a reversão do traço é A−tr(gInv A)g/2. Seu erro por componente é limitado por

\[
\epsilon+\frac12(16B\epsilon)G=(1+8GB)\epsilon.
\]

As hipóteses de módulo já implicam ε≥0 e G≥0; a folha explicita B≥0. Não há premissa inconsistente escondida na multiplicação das desigualdades. A composição nas linhas 91–98 é, portanto,

\[
\|\delta T\|_{\max}\le(1+8GB)\frac{3\delta}{2\pi}.
\]

O símbolo de norma aqui apenas abrevia o máximo das 16 componentes, conforme `TensorErrorBound`; não é uma norma lorentziana.

## 2. Diferenças finitas e a métrica fixa

Nas linhas 100–137, a desigualdade triangular aplicada a observado−resposta·t², seguida de divisão por t²>0, dá corretamente

\[
\left|\frac{\mathrm{observado}}{t^2}-\mathrm{resposta}\right|
\le\frac{\mathrm{noise}}{t^2}+C t^2.
\]

A premissa anterior é erro de truncamento ≤Ct⁴, e não ≤Ct². A divisão reduz a ordem para t²; nenhum fator de t é perdido. A cota tensorial resultante é

\[
\boxed{\|\delta T\|_{\max}
\le(1+8GB)\frac3{2\pi}\left(\frac{\mathrm{noise}}{t^2}+Ct^2\right).}
\]

**Escopo indispensável:** g e gInv são os mesmos nos dois decodificadores. A folha prova estabilidade de uma transformação algébrica parametrizada por essas matrizes. Para interpretá-la fisicamente, a relação gInv=g⁻¹ deve ser satisfeita no modelo. Ela não estima erros na reconstrução da própria métrica, na sua inversa, nas derivadas da métrica, em Ricci ou Einstein. Também não fornece uma garantia uniforme em uma família que se aproxime de métricas degeneradas: B pode crescer.

## 3. O resto quartico é obtido, não presumido

Em `MixedGibbsFiniteAccuracy.lean`, linhas 15–21, a suavidade da entropia provém da suavidade dos pesos e da positividade estrita de cada peso, que permite compor com log. O parâmetro satisfaz k>0.

Nas linhas 23–40, `exists_taylor_mean_remainder_bound` é aplicado ao intervalo compacto [0,1], com ordem n=1 e regularidade de ordem 2 obtida de ContDiff∞. A identificação da derivada unilateral no extremo 0 com a derivada real é justificada por `uniqueDiffOn_Icc`. O polinômio de Taylor é f(0)+as. A substituição C↦max(C,0) assegura C≥0 sem diminuir a cota. Consultei também a formulação e o corpo desse teorema da Mathlib: a constante é obtida por uma cota do supremo da derivada de ordem dois no intervalo.

Nas linhas 42–58, a derivada linear usada é

\[
f_k'(0)=-k\operatorname{sech}^2k.
\]

Com s=v²t²∈[0,1], o resto Cs² torna-se Cv⁴t⁴. Assim a constante do relógio é C_v=C_s v⁴, não C_s v². Isso coincide com o coeficiente −k sech²(k) v² da resposta. O termo linear é o da entropia dos pesos medidos do protocolo misto; a folha não substitui silenciosamente esse objeto pela entropia de von Neumann.

Nas linhas 60–84, as somas finitas sobre j e sobre as dez sondas produzem uma única constante C≥0 que funciona para todas as sondas e tempos na janela. A ordem dos quantificadores está correta: C é escolhido antes de t, do ruído e dos dados observados. Não há hipótese de resto fornecida externamente no teorema final `gibbs_measured_source_error`; a hipótese externa restante é o limite do ruído.

A fonte de comparação é `decodeSource` aplicado à resposta exata. A identidade importada `ten_probes_reconstruct_source`, junto de `gibbs_coupling`, a identifica com a soma dos tensores de covetores de acoplamento k_j/(πcosh²k_j). Isso mantém a normalização e a fonte da cadeia anterior.

## 4. A janela contém efetivamente tempos não nulos

Em `GibbsSamplingWindow.lean`, ponha v_ij=w_j(d_i),

\[
V=1+\sum_{i=0}^9\sum_j|v_{ij}|,\qquad R=1/V.
\]

Como J é finito e os termos são reais não negativos, V≥1>0 e R>0. Cada |v_ij|≤V. Portanto, para |t|≤R,

\[
|v_{ij}t|\le V R=1\quad\Longrightarrow\quad v_{ij}^2t^2\le1.
\]

Isso satisfaz todas as condições do resto de Taylor simultaneamente. O tempo t=R é uma testemunha não nula admissível; t=−R também satisfaz a desigualdade, embora a primeira testemunha já baste ao enunciado. A presença de 1 em V evita divisão por zero quando todos os covetores se anulam ou J é vazio. Não se presumem covetores não nulos para demonstrar a janela.

**Limite da conclusão:** a janela não vazia não é uma prova de que um erro-alvo arbitrário pode ser alcançado para um ruído fixo. `noise_truncation_balance` demonstra somente a identidade sob Ct⁴=noise. Não afirma que essa equação tem solução dentro da janela. Para noise>0 e C>0, a escolha formal t_opt=(noise/C)^(1/4) equilibra os termos e precisa também satisfazer t_opt≤R. Essa observação é análise escrita; não é um teorema adicional dessas folhas. Os casos noise=0 ou C=0 exigem tratamento separado.

## 5. Revisão da constante explícita proposta M(k)

[DERIVED — dedução escrita, não Lean nesta entrega] Para s∈[0,1] e k>0, defina

\[
A=k+s,\quad r=\sqrt{A^2+s^2},\quad n=A/r,\quad
z=n\tanh r,\quad q=(1+z)/2.
\]

Temos k≤r≤k+2, 0<n≤1, |r'|≤√2≤2 e

\[
r'=\frac{A+s}{r},\qquad r''=\frac{k^2}{r^3}\le\frac1k.
\]

Para n,

\[
n'=\frac1r-\frac{Ar'}{r^2},\qquad
n''=-\frac{2r'}{r^2}-\frac{Ar''}{r^2}+\frac{2A(r')^2}{r^3}.
\]

Usando A/r≤1, r≥k e as cotas anteriores,

\[
|n'|\le\frac{1+\sqrt2}{k}<\frac3k,\qquad
|n''|\le\frac{2\sqrt2+1+4}{k^2}<\frac8{k^2}.
\]

As derivadas de tanh são sech²r e −2sech²r tanh r, limitadas em módulo por 1 e 2. Assim

\[
|z'|\le3/k+2,\qquad
|z''|\le8/k^2+13/k+4.
\]

O termo 13/k pode ser obtido diretamente de 2·(3/k)·2+1/k. Uma conta mais apertada daria (6√2+1)/k, mas a cota proposta é válida e não exige esse refinamento.

Considere H(q)=−q log q−(1−q)log(1−q). Como

\[
\tfrac12\le q\le\tfrac{1+\tanh r}{2}<1,
\]

as derivadas de H são regulares na faixa efetivamente percorrida. A monotonicidade de log(q/(1−q)) e q(1−q)≥sech²r/4 fornecem

\[
|H'(q)|\le2r\le2(k+2),\qquad
|H''(q)|=\frac1{q(1-q)}\le4\cosh^2r\le4e^{2(k+2)}.
\]

É essencial conservar os fatores q'=z'/2 e q''=z''/2 na regra da cadeia. Com eles,

\[
|(H\circ q)''|
\le e^{2(k+2)}(3/k+2)^2
+(k+2)(8/k^2+13/k+4)
=:M(k).
\]

Todos os fatores da proposta conferem. O resto integral de Taylor dá, para 0≤s≤1,

\[
|f(s)-f(0)-f'(0)s|
\le\int_0^s(s-u)M(k)\,du=\frac{M(k)}2s^2.
\]

Portanto uma constante simultânea explícita válida é

\[
\boxed{C_{\rm explicit}
=\sum_{i=0}^9\sum_j\frac{M(k_j)}2\,v_{ij}^4.}
\]

Não é necessário identificar essa expressão com a escolha existencial de C feita pelo Lean; ela é outra testemunha que satisfaz a mesma desigualdade, pela prova escrita acima. A fórmula é finita para cada conjunto finito de k_j>0. Ela é conservadora, não ótima: cresce quando k se aproxima de zero e também contém uma exponencial para k grande. Para uso numérico, é necessário controlar a avaliação e a faixa de parâmetros; a divergência dessa cota não prova divergência do resto real.

## 6. Estatuto final da revisão

[REAL — leitura e medição] As fontes, hashes correspondentes aos recibos e registros de axiomas são identificados no manifesto. Nenhum resultado de recompilação é atribuído a esta revisão.

[DERIVED — análise própria] Não identifiquei erro semântico nas constantes, no sinal, na normalização, na obtenção do resto ou na não vacuidade da janela. Os limites de escopo acima devem acompanhar qualquer descrição dos resultados: componentes em base fixa, métrica e inversa fixas, ruído como entrada e C explícito ainda em prova escrita.

Nenhum desses resultados afirma confirmação física, resolve o setor gravitacional quântico interagente ou move o gate.
