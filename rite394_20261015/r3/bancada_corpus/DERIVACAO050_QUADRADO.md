# DERIVAÇÃO050 — o quadrado do operador contínuo e seu domínio

[DERIVED, anterior ao código] A continuação049 construiu T_c como operador parcial positivo auto-adjunto, com gráfico equivalente a g(ξ)=exp(-cξ)f(ξ) quase em toda parte, e provou D_c={f∈L²:exp(-cξ)f∈L²}. As fontes e selos049 permanecem somente leitura.

## Domínio efetivo da composição

Definiremos o submódulo D_sq={f: existe hf:f∈D_c com T_c(f,hf)∈D_c}. O operador continuousModularSquare tem exatamente esse domínio e valor T_c(T_c f). A API Mathlib LinearPMap.comp requer invariância de todo o domínio do primeiro operador; não a utilizaremos para supor tal invariância. O gráfico do operador composto será demonstrado equivalente à existência de h com (f,h)∈graph(T_c) e (h,g)∈graph(T_c).

## A inclusão que precisa ser provada

Para m=exp(-cξ)>0 vale m≤1+m², portanto |mf|≤|f|+|m²f|. Se f∈D_(2c), então f e m²f pertencem a L². A soma de suas normas pertence a L²; MemLp.mono' aplica a dominação à função mensurável mf e prova f∈D_c. Não há premissa adicional f∈D_c nessa inclusão global.

A identidade m²=exp(-(2c)ξ) será provada pela lei de soma da exponencial, com casts complexos explícitos.

## Igualdade de operadores

O gráfico da composição implica g=m²f por duas igualdades quase em toda parte. Reciprocamente, de (f,g)∈graph(T_(2c)) extraímos f∈D_(2c), aplicamos a inclusão acima e construímos h=T_c f. As igualdades quase em toda parte fornecem (h,g)∈graph(T_c). Logo os gráficos coincidem e a extensionalidade de LinearPMap fornece:
    continuousModularSquare c = continuousModularOperator (2*c).

A igualdade de submódulos domínio é consequência dessa igualdade de operadores. O enunciado vale para todo parâmetro real c, incluindo c=0. Não é apenas uma igualdade de fórmulas em uma interseção previamente escolhida.

## Alcance e custódia

[OPEN] Este módulo não identifica sozinho o quadrado com S†S; essa integração requer o adjunto antilinear e será realizada em módulo distinto. Também não calcula poderes imaginários nem prova BW, H3 ou reconstrução gravitacional.

Escritas somente em arquivos novos050 dentro de Chatgpt; backups imediatos de bytes antes de revisões, temporário verificado, sem alteração de049, Atlas, memórias, um.py ou kernel canônico. Sondas exclusivas são desenvolvimento, não selo.
