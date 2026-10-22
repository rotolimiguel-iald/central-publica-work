[DERIVED / INPUT / OPEN] Continuação 012 — a área geométrica da tela e sua compatibilidade com a entropia. Derivação anterior ao código, 05/09/2026.

A entrega 011 foi reconferida: houve progresso no turno anterior. O túnel ainda termina na ordem 007. O objetivo amplo permanece aberto.

## Alvo e relação com o caminho crítico

Em 010, A'=θA era um campo recebido por LocalHorizonPencil. Em 011, a entropia dos pesos canônicos foi calculada, mas a área continuou uma contagem calibrada. Esta rodada ataca a área independentemente da entropia: a densidade de área de uma tela transversal regular será definida pela métrica induzida h=SᵀgS, como √det h.

A finalidade é pagar a lei de variação da área sob dados geométricos explícitos e compô-la com a reconstrução anterior. Não é definir área como S/η. A existência global de cortes e a lei entropia-área permanecem perguntas diferentes.

## Derivação

1. Para h(t) uma matriz real 2×2 e b uma matriz 2×2, h'=bᵀh+hb implica (det h)'=2 tr(b) det h. Isso sai da regra do produto nas quatro entradas e da fórmula do determinante. Se det h>0, A=√det h tem A'=tr(b)A. A positividade geométrica da tela é uma condição explícita.

2. Num referencial nulo F=(k,n,e₁,e₂), com inversa D, a matriz de Gram é G=FᵀgF, com bloco nulo [[0,-1],[-1,0]] e bloco transversal h. Para B=∇V, defina b=D B F. Se Bk=0 e g(k,Bn)=0, então b₀₀=b₁₁=0. A invariância do traço dá tr(B)=tr(b)=tr(b_transversal). A derivação não chama o traço transversal de expansão ambiente por definição: a igualdade precisa ser provada.

3. Ao longo de uma curva γ com tangente V, a compatibilidade métrica dá g'=Lᵀg+gL, onde L=Σ_i V^i Γ_i. Para duas direções de tela transportadas por Lie, S'=(B−L)S. A regra do produto cancela L e dá h'=Sᵀ(Bᵀg+gB)S. Usando o referencial nulo, isso é b_transversalᵀ h+h b_transversal. Portanto A'=tr(B)A, com A calculada da métrica, não recebida pronta.

4. No uso com a conexão canônica, g é o campo métrico e Γ é Levi-Civita; a compatibilidade já foi provada. As direções de tela, o referencial regular, sua positividade, o transporte e a existência da congruência são dados geométricos que devem ser nomeados. Bk=0 representa geodesicidade afim; g(k,Bn)=0 é a preservação da nulidade na direção auxiliar. Não se deve ocultar tais condições dentro de uma suposta prova de existência.

5. Um contrato de área geométrica ao longo da curva deverá produzir a lei A'=θA exigida por 010. A composição preservará as demais premissas do balanço de calor, do limite de Clausius e de conservação de T. A reconstrução resultante seguirá condicional aos dados físicos que não foram construídos.

6. A entropia de um perfil P e andar N fixos é constante ao longo do parâmetro. Se essa mesma constante satisfaz S_N=ηA(t) numa vizinhança, com η≠0, então A'=0. Para a área geométrica regular, isso força θ=0. Em particular, uma entropia congelada não pode acompanhar uma tela em expansão não nula. É necessário mover o estado, o corte, a álgebra ou o número efetivo de fatores. O enunciado será local e não excluirá mecanismos dinâmicos que ainda não foram construídos.

7. Controles devem exibir uma tela positiva com área variável e um caso constante. A transformação linear dos vetores transversais recalibra a densidade de área de modo conhecido; sem parâmetros de superfície e integração não se chamará essa densidade de área total de um horizonte.

## Limites do que se quer provar

[KNOWN] A relação entre expansão e variação do elemento de área aparece na equação (3) da fonte primária de Jacobson, 1995: https://arxiv.org/html/gr-qc/9504004. Aqui a meta é calcular essa relação em Lean a partir do Gram da tela.

[OPEN] Entropia-área microscópica, escolha da escala, área total integrada, rede de regiões, existência de congruências/telas gerais, limite quântico contínuo, calor, H3, assinatura, dimensão e globalização não são presumidos como quitados. O equilíbrio B=0 de 010 continua mais forte que o equilíbrio apenas da tela, salvo prova específica em contrário.

## Adendo do controle de assinatura — antes da correção

O controle plano encontrou eta4=diag(1,−1,−1,−1), a convenção +--- do kernel. A condição inicialmente escrita 0<h₀₀ no contrato NullScreenAt é incompatível com uma tela espacial dessa assinatura. Ela será corrigida para h₀₀<0, mantendo det h>0. O referencial escolhe g(k,n)=−1 e a tela tem Gram −I. Como det(−h)=det h em dimensão dois, A=√det h continua sendo a densidade de área da métrica espacial positiva −h. A derivação de A'=θA não depende do sinal de h₀₀ e permanece válida. A versão com a condição errada e o log do controle negativo serão preservados; não constituem resultado geométrico aceito.

Todos os teoremas novos terão #print axioms. Logs com erros, avisos ou sorryAx serão rejeitados e preservados. Escritas somente em Chatgpt; nenhuma execução/importação de um.py ou edição no acervo canônico, Atlas, memórias, selos e gate.
