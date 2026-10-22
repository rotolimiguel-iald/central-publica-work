# Derivação prévia — fluxo da mistura estática e dinâmica

[INPUT] O bloco estático usa probabilidades q≥0 com soma 1. O bloco dinâmico é a preparação conjunta unitária C e frequências f já construída. O espaço de amplitudes é ι ⊕ (Fin 2 × κ); o espaço de probabilidades é ι ⊕ (κ × Fin 2). Uma equivalência explícita troca apenas os dois índices internos do bloco dinâmico.

Definimos U(t)=I ⊕ jointBlockFlow(C,f,√2t), e amplitudes Ψ₀=(√(1/2)√q, √(1/2)Ψ_dyn,0), Ψ(t)=(√(1/2)√q, √(1/2)Ψ_dyn(√2t)). A identidade estática e o fluxo dinâmico unitário produzem um operador unitário em ambos os sentidos; a álgebra por blocos fornece U(t)Ψ₀=Ψ(t).

A identidade |√(1/2)z|²=|z|²/2 e a leitura de pesos dinâmica já provada dão exatamente mixedCurve(q,X)(t) após a reindexação. A normalização global segue da mesma distribuição, sem postular o readout. A positividade estática e as normalizações não são necessárias à unitariedade do operador; são necessárias à interpretação dos pesos e à norma 1.

[OPEN] Este suplemento não identifica a distribuição inicial com a fonte T, não compõe o codec32 com a fonte16, não infere separância/fidelidade na álgebra matricial inteira e não preserva a entropia absoluta/custo. O fluxo é complexo e explicitamente construído; a palavra real significa construção efetiva, não matriz de entradas exclusivamente reais.
