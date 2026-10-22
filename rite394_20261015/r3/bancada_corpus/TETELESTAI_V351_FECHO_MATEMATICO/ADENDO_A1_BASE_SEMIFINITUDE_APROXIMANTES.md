[REAL — três pontes auxiliares verificadas; OPEN — A1(b), existência do traço, permanece aberta]

# A1: forma dual na base, domínio semifinito e recuperação por aproximantes

Data: 2026-09-14T09:10:11.180486-03:00

Este adendo preserva `LACUNAS_A1.md` e o manifesto anterior byte a byte. A1(a) e A1(c) já pagos permanecem pagos. A1(b) ainda não tem habitante concreto de `RegularCoreTraceData P`, nem parede contra sua existência.

## O que passa a ser fornecedor, para não ser refeito

1. `fixedFormOnBase` transporta uma forma afiliada ao fixo F para uma forma afiliada à própria base M. A afiliação é demonstrada pelos unitários de M′, amplificados por `fibre`, e pela identificação F=fibre(M). O transporte não pressupõe output limitado.
2. `baseDualWeight` é essa forma para o integral dual existente. Zero, soma, escala, ordem, fidelidade, bimódulo e normalidade por supremos internos estão provados. Avaliar no mesmo Ω dá exatamente `scalarDualWeight`, inclusive no infinito. Unidade tem valor infinito em todo vetor não zero; a média quadrática de comprimento 1 tem valor escalar 1.
3. `scalarWeight_square_finite_wot_closure` prova que nν={a∈N:ν(a*a)<∞} é WOT-denso no mesmo core N, reutilizando a aproximação forte anterior. `scalarWeight_unit_not_square_finite` recusa a unidade nesse domínio. O enunciado Lean não identifica topologias preduais arbitrárias.
4. `exists_base_moreau_approximant` produz, para c>0, D_c∈M, 0≤D_c≤cI, tal que a forma limitada de fibre(D_c) é o mínimo de q_A(w)+c‖w−v‖². Usa o resolvente já construído de A/c e c(I−R_c), sem refazer a representação do operador.
5. `exists_monotone_base_dual_approximation` produz D_n∈M positivo, crescente na ordem de operadores, e para TODO vetor da representação regular:

    q_A(v) = sup_n ofReal Re⟨v,fibre(D_n)v⟩.

A recuperação inclui q_A(v)=∞. Quando o supremo é finito, o bound de energia dá w_n→v, e o subnível fechado da mesma forma conclui a igualdade. Não foi presumida densidade do domínio finito da forma individual.

O novo delta tem três módulos, 17 teoremas e duas definições, totalizando 19 declarações auditadas no trio. São fornecedores formais de A1; não são funções novas no Python e não foram embutidos no monólito.

## A obrigação imediata, sem reiniciar o que já foi pago

Ponham-se M=theFactorObject P, N=regularCoreAlgebra P, ι=fibre e ψ∈M_*^+.
Os aproximantes agora EXISTEM em kernel. A próxima construção é

    m_A(ψ) := sup_n ofReal Re ψ(D_n(A)).

Ela deve usar funcionais normais positivos da MESMA M. Faltam tipar essa interface e provar aditividade/homogeneidade/semicontinuidade em ψ, a avaliação m_A(ω_v)=baseDualWeight(A)(v), e a extensionalidade necessária para transportar as leis em A.

Um fornecedor suficiente, precisamente delimitado, é: para cada funcional normal positivo ψ sobre esta M existe uma família v_k na Hilbert da base, com soma_k ‖v_k‖²<∞, tal que ψ(D)=soma_k ⟨v_k,Dv_k⟩ para todo D∈M. Convergência monótona dá então m_A(ψ)=soma_k baseDualWeight(A)(v_k). Alternativamente, uma extensão normal positiva ambiente com a mesma propriedade serve. Não presumir que todo ψ seja um único estado vetorial nem tratar um funcional positivo arbitrário como normal.

As buscas dirigidas no kernel e na Analysis da mathlib estão preservadas. A mathlib declara WStarAlgebra com existência abstrata de predual; isso não fornece por si só a interface concreta, sua identificação com esta representação ou o lema de decomposição. `GNSBridge` é um fornecedor de funcional finito em matrizes, não essa ponte infinita. O nome correto `exists_dualFormRepresentation` foi conferido e registrado no adendo da ficha; uma busca pelo nome com sublinhados foi negativa apenas por grafia.

## O que permanece depois dessa obrigação

As pontes 2–4 de `LACUNAS_A1.md` continuam: implementação modular do mesmo peso, gerador positivo afiliado h com h^{it}=Λ_t e perturbação por h^{-1} produzindo o traço fiel normal semifinito, tracial e com τ∘θ_s=e^{-s}τ. A invariância ν∘θ_s=ν não é essa escala; o peso ν não fornece τ diretamente. Não há parede contra a existência de τ neste marco.

Correção de exigência, ao lado do texto anterior: para o peso não tracial ν, usar o domínio nν fracamente denso como critério de semifinitude; não cobrar o campo de todos os minorantes positivos finitos de cada A, que pertence aqui ao contrato final do TRAÇO. Esse campo final não foi enfraquecido. A consulta independente registra um contraexemplo analítico de peso não tracial, explicitamente não Lean. Referência primária: Hiai, definições 7.1 e 8.1/8.5, https://arxiv.org/pdf/2004.02383.

Os três marcos não alteram o gate, não produzem dados físicos e não autorizam iniciar A2 antes de resolver A1. Canonicalidade/normalização não é inferida da mera lei de escala.
