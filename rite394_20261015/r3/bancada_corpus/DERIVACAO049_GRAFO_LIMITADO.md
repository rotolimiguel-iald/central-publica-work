# Derivação049 — operador parcial construído de dois operadores limitados

07/09/2026. [DERIVED — antes da fonte e da compilação]
Escopo exclusivamente matemático, no Hilbert complexo completo E.

Dados: A e B são operadores lineares contínuos, A é injetivo. A auto-adjunticidade de A e B, a comutação AB=BA e A²+B²=I serão hipóteses dos teoremas que as usam, não campos contendo a conclusão.

## Construção e domínio

A induz uma equivalência LINEAR E ≃ range A. Não se exige inversa contínua.
Definimos T no domínio literal range A por T(Ah)=Bh. A injetividade de A garante o valor único. A parametrização do gráfico é demonstrada:
(x,y)∈graph T se e somente se existe h com Ah=x e Bh=y.

Com AB=BA e A²+B²=I, esse gráfico é exatamente Bx=Ay.
A ida usa comutação. Na volta, h=Ax+By fornece
Ah=A²x+BAy=A²x+B²x=x,
Bh=ABx+B²y=A²y+B²y=y.
Assim não se postula nem pertencimento de x ao domínio nem uma solução inversa.

## Fechamento e densidade

A igualdade Bx=Ay é a preimagem fechada de zero pela aplicação contínua (x,y)↦Bx−Ay. Essa prova vale para a topologia usual do produto; não se confunde sua norma máximo com a norma Hilbertiana soma de quadrados.

Se A é auto-adjunto e injetivo, (range A) perpendicular = ker A*=ker A={0}. O critério de fecho ortogonal dá domínio denso. Não se conclui range A=E, nem que T é limitado.

## Adjunto maximal

O pareamento de dois pontos do gráfico é simétrico:
〈Bh,Ak〉=〈h,BAk〉=〈h,ABk〉=〈Ah,Bk〉.
Logo T é adjunto formal de si próprio e T⊆T†.

A densidade será explicitamente passada à API Mathlib.adjoint_isFormalAdjoint. Se (x,y) está no gráfico de T†, testar contra todos (Ah,Bh) dá
〈y,Ah〉=〈x,Bh〉.
Pela auto-adjunticidade de A e B, isso equivale a Ay=Bx. A caracterização já provada do gráfico conclui (x,y)∈graph T. Portanto T†⊆T e T†=T, como igualdade de operadores parciais, com domínios.

## Positividade derivada

A premissa suficiente é uma desigualdade sobre os operadores LIMITADOS:
∀h, Re〈Ah,Bh〉≥0.
Para x=Ah no domínio, Re〈x,Tx〉=Re〈Ah,Bh〉≥0. Não se pressupõe T positivo.
O módulo concreto de multiplicadores fornecerá essa premissa por integral. Não é necessário impor adicionalmente IsPositive(A*B).

## Interfaces e alcance

BoundedGraphOperator.lean, namespace ChatgptAudit.Continuous049.
Definição pública boundedGraphOperator A B hAi; domínio range A.
Lemas: parametrização, equação Bx=Ay, domínio denso, operador fechado, adjunto formal, auto-adjunticidade e positividade.

Usaremos apenas Mathlib.Analysis.InnerProductSpace.LinearPMap e a equivalência linear sobre a imagem. Cada definição e teorema terá #print axioms; zero instâncias novas. Nenhum arquivo≤048 será alterado. Revisões terão cópia exata dos bytes antes da escrita temporária verificada.

[OPEN] Esta construção não identifica potências imaginárias, fluxo modular, Bisognano–Wichmann, área ou H3. A não limitação no modelo concreto exige prova própria; o lema abstrato admite também casos limitados.
