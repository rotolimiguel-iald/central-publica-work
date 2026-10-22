# DERIVAÇÃO049 — domínio efetivo do multiplicador contínuo

[DERIVED, antes da compilação] Este módulo liga o operador parcial construído por coordenadas limitadas à multiplicação mensurável concreta. O espaço é SpectralHilbert = L²(ℝ, volume; ℂ). Não se presume que seu domínio seja todo o espaço.

## Dados já construídos

A e B multiplicam respectivamente por a(ξ) e b(ξ), com a(ξ)>0, b(ξ)=exp(-cξ)a(ξ), A²+B²=I e AB=BA. O módulo BoundedGraphOperator define T em range(A), prova o gráfico equivalente a Bf=Ag e prova densidade, fechamento, auto-adjunticidade maximal no sentido Mathlib e positividade pelo pareamento real de Ah e Bh.

## Ponte de gráfico e domínio

Definimos continuousModularOperator c como esse mesmo T para spectralA c e spectralB c. Para f,g em L²:
    (f,g) ∈ graph(T) ⇔ g(ξ)=exp(-cξ)f(ξ) quase em toda parte.
A direção direta cancela a(ξ)>0 na igualdade b(ξ)f(ξ)=a(ξ)g(ξ); a direção inversa usa Lp.ext. Nenhuma inversa contínua de A é introduzida.

Consequentemente:
    f ∈ D(T) ⇔ MemLp (ξ ↦ exp(-cξ)f(ξ)) 2 volume.
Na direção inversa, MemLp.toLp fornece g; o critério do gráfico fornece a pertença ao domínio. Assim a existência do valor e a identificação de sua classe em L² são demonstradas, não acrescentadas como hipótese.

## Ausência de autovetores

Para c≠0 e λ complexo arbitrário, a fibra {ξ | (exp(-cξ):ℂ)=λ} contém no máximo um ponto: a exponencial real, a inclusão em ℂ e a multiplicação por -c são injetivas. A medida de Lebesgue não tem átomos, então a fibra tem medida zero. A equação Tf=λf força f=0 fora dela, portanto f=0 em L².

O controle c=0 é explícito: D(T)=L² e T=I no domínio. Logo a hipótese c≠0 não pode ser omitida.

## Limites do resultado

[OPEN] Este módulo, por si só, não calcula o espectro completo, não prova continuidade absoluta de uma medida espectral e não identifica T com uma potência de um operador modular já reconstruído. O nome não prova Δ^it, Bisognano–Wichmann, covariância geométrica, H3 ou gravidade geral. Também não afirma, apenas pelo rótulo de operador parcial, que T seja não limitado: a caracterização do domínio e a ausência de autovetores são os enunciados aqui pagos.

## Custódia

A derivação precede o código. Somente novos arquivos em Chatgpt; revisões preservam bytes anteriores em backup imediato e usam temporário verificado. Fontes canônicas, memórias, Atlas e etapas seladas permanecem somente leitura. Probes novos são desenvolvimento e não selo final.
