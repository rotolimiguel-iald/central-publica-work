# Parecer da raiz — estado BRST interagente formal

10/09/2026. [DERIVED — revisão matemática interna]. Li integralmente ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md e confrontei diretamente [DF, Teorema4 e condição4.8](https://arxiv.org/pdf/hep-th/9807078v2) e [Rejzner, Teorema4.2](https://arxiv.org/pdf/1301.7037v3). Os teoremas primários são usados com suas condições, sem importar a verificação de QED para o modelo Einstein–sigma.

**Resultado:** a construção condicional de quociente e estado formal é consistente com P0–P2. Uma precisão de orientação do bracket, comunicada ao autor, deve acompanhar a tradução da referência Rejzner. Ela não altera as provas que usam a convenção fixa2.3 da nota.

## Quartetos e inversa na imagem

As relações cruzadas bosônicas e fermiônicas3.1 produzem as ações indicadas dos dois operadores nos criadores. Seu anticomutador é a derivação que conta os criadores auxiliares e mata o vácuo, portanto é N_aux. O quadrado de Q é zero. Com a projeção ortogonal P sobre o vácuo auxiliar, um vetor fechado obedece psi=Ppsi+Q N_aux^-1 h psi. A inversa de N é usada apenas nos graus auxiliares positivos e é bem definida no domínio algébrico de partículas finitas.

Simetria e nilpotência anulam os termos exatos e cruzados da norma; resulta ||Ppsi||². Isso prova positividade e exatidão dos vetores nulos nesse modelo algébrico. R0=(N_aux^-1 h)|imQ é uma escolha de inversa à direita. O texto conserva a obrigação de realizar os campos Hadamard e de Wick no mesmo domínio, sem inferir essa compatibilidade de uma decomposição simplética arbitrária de Cauchy.

## Recorrência e radical

No passo N+1, Q Psi^(N)=z^(N+1)r+O(z^(N+2)). Q²=0 implica Q0r=0. A identidade [Q Psi^(N),Q Psi^(N)]=0, extraída no grau2N+2, implica [r,r]=0. A segunda condição de P0 torna r exato e define psi_(N+1)=−R0r. Este argumento não exige postular separadamente ausência de cohomologia de ghostum nos vetores.

Para a positividade, retirar repetidamente o termo inicial exato reduz o representante sem mudar sua norma. O primeiro coeficiente físico não nulo aparece com potência par e coeficiente estritamente positivo; se ele nunca aparece, a série inteira é exata na topologia formal. Isso prova o radical afirmado, sem usar uma imagem fechada num espaço de Hilbert ainda não construído. O módulo físico identificado com H0[[z]] depende de escolhas; a nota não o chama de identificação isométrica canônica.

## Carga, domínio e orientação

A Jacobi fornece [Q,[Q,A]_gr]_gr=[Q²,A]. A comutante escalar da álgebra completa numa faixa de Cauchy, juntamente com a graduação sem escalares de ghostdois, elimina o possível quadrado central. O contrato de faixa inteira é indispensável: a comutante de uma região pequena não possui a propriedade utilizada. A corrente renormalizada, sua implementação e os domínios comuns continuam hipóteses efetivas.

A seção2 comenta converter a orientação i[Q,A]_gr para i[A,Q]_gr por Q→−Q. Para A ímpar, a tradução geral exige o fator de paridade:

\[
[A,Q]_{gr}=-(-1)^{|A|}[Q,A]_{gr}.
\]

A troca uniforme de sinal de Q é suficiente apenas no setor par. Pode-se conservar2.3 como convenção desta nota e traduzir o diferencial da referência com o fator graduado. Esta observação foi enviada ao autor para adendo; a prova de positividade depende de Q simétrico e nilpotente e permanece intacta. A comparação BV–carga de Rejzner requer QME e sua hipótese de anomalia, como a nota declara.

## Estado e alcance físico

A raiz inversa formal da norma1+O(z) existe e normaliza o levantamento do vetor físico. Para A fechado, A Omega é fechado e sua norma fornece omega(A* A)≥0. Termos exatos não mudam o estado. Isso exige que A, a carga e os coeficientes do vetor atuem no domínio comum; a existência abstrata de distribuições renormalizadas não basta para essa hipótese.

A prova levanta vetores, não todos os observáveis locais. O estado depende do cutoff e da representação escolhidos. A nota mantém em aberto o transporte coerente entre cutoffs/fundos, a representação auxiliar Hadamard compatível e a implementação QME. A organização univariada em z foi declarada; não se avalia uma série infinita em z=1 ou em ħ para inferir positividade não perturbativa.

Este parecer sustenta o teorema **condicional** e a recorrência operacional. Não constitui construção completa do estado físico Einstein–sigma sem P0–P2. Nenhum Lean, CAS, um.py ou teste de natureza foi executado; revisão interna por agente não é validação externa independente.
