# Precisão: fatoração dos operadores pela compatibilidade de jatos

10/09/2026, arco 071. [DERIVED — adendo à prova escrita]. Mantêm-se a classe coordenada A_coord e o complexo on-shell H→Δ→0 da nota principal. O objetivo é explicitar o passo de fatoração utilizado na comparação horizontal.

## 1. Um operador que anula H

Seja ∇ um operador de ordem r no argumento de equações, com coeficientes na classe adotada, tal que ∇H=0 sobre o espaço estacionário. Em ordem finita, escreva

\[
A:J^r(P_1)\longrightarrow Q
\]

para sua matriz de coeficientes em jatos do argumento. Tome as ordens de prolongamento compatíveis com H de ordem dois e Δ de ordem um. A exatidão da nota principal fornece

\[
\operatorname{im}(jH)=\ker(j\Delta).
\]

O operador ∇H=0 significa que A anula esse núcleo. Seja S_Δ uma seção à direita da aplicação sobrejetiva jΔ, na mesma ordem finita, construída por seu símbolo divergência e correções triangulares inferiores. Então

\[
I-S_\Delta(j\Delta)
\]

tem imagem em ker(jΔ). Logo

\[
A=A S_\Delta(j\Delta).
\]

A matriz A S_Δ representa um operador diferencial B no argumento de gauge, de ordem finita, e a identidade é precisamente

\[
\boxed{\nabla=B\Delta.}
\]

Se r=0, H já é sobrejetivo no nível dos valores das equações e A=0; não é necessário introduzir jatos de ordem negativa. A mesma razão mostra que um operador que anula o último mapa Δ é zero após prolongar às ordens necessárias.

## 2. Um operador que anula as variações estacionárias

O outro fatoramento empregado no complexo de contato também é finito. Se uma matriz T nos jatos das variações dos campos anula ker(jH), escolha a seção S_H de jH sobre ker(jΔ), obtida ao diferenciar o inverso triangular KT. Ponha Π=I−S_Δ(jΔ). Então

\[
T=(T S_H\Pi)(jH).
\]

A igualdade segue porque Π é a identidade na imagem de jH e a diferença entre uma variação v e S_H(jH)v pertence a ker(jH). Assim um operador que se anula nas variações estacionárias é múltiplo diferencial de H na mesma classe de coeficientes.

Essas são identidades de matrizes em espaços de jatos finitos; não se inverte um operador diferencial por propagador. A, T, S_Δ, S_H e Π têm coeficientes suaves nos valores e polinomiais nos jatos diferenciados do fundo. Composição e multiplicação preservam essa propriedade. As seções não contêm inversos de dy ou curvatura. Esse argumento implementa a fatoração de compatibilidade, incluindo o passo da Proposição 2.22 de Verbovetsky, na subclasse usada nesta tarefa.
