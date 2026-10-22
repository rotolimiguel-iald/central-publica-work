# Convenções para a próxima construção do traço

[REAL — Lean] A ação já construída satisfaz θ_s(Λ_t)=exp(−ist)Λ_t.

[KNOWN] Na construção de Hiai, Λ_t=A^{it}, A positivo não singular, e
τ=(φ̃)_{A⁻¹}. A definição exige o peso dual, operadores afiliados e perturbação
de pesos; não é apenas uma multiplicação formal de matrizes.
Fonte: [Hiai, Teorema 10.15, p. 99](https://arxiv.org/pdf/2004.02383).

[DERIVED — verificação algébrica de convenções, não formalizada em Lean]

| Gerador escolhido | Fluxo | Ação dual | Densidade escalar compatível |
|---|---|---|---|
| L=log A | Λ_t=e^{itL} | θ_s(L)=L−s | e^{−x} dx |
| K=−log A | Λ_t=e^{−itK} | θ_s(K)=K+s | e^{x} dx |

De fato, ∫f(x−s)e^{−x}dx=e^{−s}∫f(x)e^{−x}dx;
na segunda convenção, ∫f(x+s)e^x dx=e^{−s}∫f(x)e^x dx.
Misturar θ_s(K)=K+s com e^{−K}dK inverteria a escala desejada.

O gerador aqui é o da representação regular inteira, incluindo a translação.
Sua identificação com um gerador somente da torre requer prova própria.

[OPEN] A, afiliação, peso dual e traço ainda não foram construídos neste kernel.
Esta tabela fixa sinais; não fornece τ nem habilita flag.


## TETELESTAI_V350_DUAL_WEIGHT_CUTS_20260911 — 2026-09-11T22:49:55-03:00: normalização além do sinal

[DERIVED — convenção de Haar/Fourier; ainda não teorema Lean de Fourier]
Para dt de Lebesgue e caracteres exp(−ist), a medida dual usada na construção de
Hiai é ds/(2π). A tabela anterior determina o sinal da densidade, mas não sua
constante multiplicativa. A mesma lei τ∘θ_s=e⁻ˢτ vale para qualquer múltiplo
positivo de τ; ela sozinha não autoriza dizer que τ(P)=1.
Os cortes implementados usam (2π)⁻¹ fixo e não dividem pelo comprimento 2R.
O traço canônico continua aberto. Ver revisao/DUAL_WEIGHT_CONSTRUCTION.md e
RELATORIO_PESO_DUAL.md. A escolha de medida é preservada como entrada explícita.
