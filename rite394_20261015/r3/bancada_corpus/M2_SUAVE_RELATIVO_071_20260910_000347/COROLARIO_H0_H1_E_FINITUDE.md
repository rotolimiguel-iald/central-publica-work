# Corolário de graus zero e um e controle de finitude

10/09/2026, arco 071. [DERIVED — adendo à demonstração escrita]. A nota `M2_SUAVE_POR_COMPATIBILIDADE_E_SPENCER.md` é mantida sem alteração. Usam-se exatamente a álgebra coordenada A_coord=C∞(x,g,y)[jatos diferenciados] e as cartas contráteis nela especificadas.

## 1. Grau um

Seja ρ₁ uma forma horizontal de grau um em E_∞, com d_Hρ₁=0. Pelo resultado E₁^{1,1}=0 da nota principal, existe uma forma α₁₀ de contato um e grau horizontal zero, na mesma classe, tal que

\[
d_V\rho_1+d_H\alpha_{10}=0.
\]

A forma d_Vα₁₀ é horizontalmente fechada. Como E₁^{2,0}=0 e não existem formas de grau horizontal negativo, d_Vα₁₀=0. Assim Ω₁=ρ₁+α₁₀ é uma 1-forma total fechada. A contração polinomial das fibras estacionárias e a homotopia suave da base contrátil fornecem Ω₁=df. Projetando para grau de contato zero,

\[
\rho_1=d_H f,\qquad H^1_{\rm hor}(E_\infty,A_{\rm coord})=0.
\]

## 2. Grau zero

Se d_H f=0, então d_H(d_V f)=0. A nulidade de E₁^{1,0}, novamente sem graus horizontais negativos, implica d_V f=0. Logo df=0 no espaço estacionário local conectado. Portanto

\[
H^0_{\rm hor}(E_\infty,A_{\rm coord})=\mathbb R
\]

(ou ℂ se a álgebra foi complexificada). Não se obtém uma função arbitrária do alvo: o termo d_H f(y)=∂_A f\,dy^A faz parte do diferencial utilizado.

## 3. Por que os três graus preservam a classe

Nos graus horizontais 0,1,2, são necessários no máximo dois levantamentos de contato. Cada levantamento da comparação de compatibilidade tem um número finito de etapas porque o grau horizontal está limitado por quatro. Cada homotopia de operadores remove a maior ordem do argumento distinguido por σh+hσ=r+4−q; derivar os coeficientes só transfere uma quantidade finita de derivados aos demais fatores. Os rebatimentos do complexo H→R† usam matrizes de jatos de ordem finita, derivadas do split triangular KT069.

Não se pressupõe um limite universal de ordem igual para todos os cociclos, nem que os antifields estejam limitados a uma ordem inicial arbitrariamente fixada. O enunciado é elemento a elemento: um cociclo com um número finito de jatos e um polinômio finito produz uma primitiva com um número finito de jatos e um polinômio finito. Durante a construção, a ordem pode aumentar por uma quantidade finita. Não são admitidas séries de grau derivativo ilimitado.

A homotopia de de Rham nas fibras livres integra monômios e preserva polinomialidade. A homotopia da base integra apenas funções suaves de x,g,y sobre caminhos interiores às cartas. Sua saída pode depender suavemente de g de modo não racional e pode conservar dependência explícita nas coordenadas. Não se reivindica uma primitiva natural covariante.

Os resultados locais H⁰=constantes e H¹=H²=0 fornecem dados para uma análise de sobreposições. Eles não colam sozinhos primitivas de s ou de d por uma partição de unidade do alvo: os termos dρ_i(y) e sρ_i(y) precisam ser tratados. A covariantização, a classe admissível dos contratermos e a colagem global são tarefas distintas deste corolário.
