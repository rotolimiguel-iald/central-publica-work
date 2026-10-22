# Continuação055 — derivação da resposta entrópica regional

[DERIVED — anterior ao fonte ExchangeEntropyResponse; nenhuma compilação anunciada]

A derivação global CONTINUACAO055_DERIVACAO_PREVIA.md foi lida. Este módulo trata das funções escalares das marginais, independentemente da implementação matricial da interação. O módulo de dinâmica deverá provar que suas restrições efetivas são exatamente estas distribuições; definir as funções não substitui essa prova.

## Dados, sinais e normalização

Para p,q reais, definir

    exchangeWeight p q t = p + (q-p) sin²t,
    exchangeHeat p q t = (p-q) sin²t,
    exchangeModularGap p = log p - log(1-p).

A distribuição regional é siteW(exchangeWeight p q t). Ela é normalizada para todo p,q,t. Sob 0<p,q<1, ambos os pesos são positivos em todo t, porque exchangeWeight é p cos²t+q sin²t; o complemento é a mesma combinação de 1-p e 1-q. A transferência Q0=p-p_t coincide com a variação da energia de níveis 0 e 1, cuja média é 1-p. A troca p↔q dá Q1=-Q0.

A derivada do primeiro peso é 2(q-p) sin t cos t; o outro peso tem derivada oposta. Em t=0 a tangente é zero, sem exigir p=q. Usaremos o registro EXISTENTE Micro021.DiagonalStateCurve(siteW p), com pesos, tangente, derivadas e normalização demonstrados. Não se introduz um segundo contrato abstrato de Bernoulli.

## Identidade exata e resposta infinitesimal

A identidade Micro021.relative_entropy_identity, de DiagonalRelativeEntropy.lean, fornece

    S(p_t)-S(p) = modularIncrement(siteW p,siteW p_t) - D(siteW p_t || siteW p).

A soma em Fin 2 dá modularIncrement=exchangeModularGap(p)*Q0. Portanto a primeira lei regional é exata. Sob fidelidade da referência, RelativeEntropyFisherLimit.relative_entropy_quadratic_zero_iff aplicado à curva acima e à sua tangente zero dá D/t²→0 no filtro passado perfurado.

UnitaryMarginalDynamics.frequency_sin_square_limit, da022, com frequência 1 dá sin²t/t²→1. Subtraindo o limite relativo da identidade exata, obtemos

    [S(p_t)-S(p)]/t² → exchangeModularGap(p)*(p-q).

O coeficiente de uma região pode ter qualquer sinal. O limite inicialmente formalizado é pelo passado, como o teorema021 reutilizado. Não o anunciar como bilateral sem outro argumento.

## Soma regional e controles

Definir C(p,q)=(p-q)(exchangeModularGap(p)-exchangeModularGap(q)). A soma dos incrementos modulares é C(p,q)sin²t. A função log p-log(1-p) é estritamente crescente em (0,1), portanto C≥0 e C=0 se e somente se p=q. Os dois fatos usam o domínio fiel explicitamente.

No controle p=2/3,q=3/4, C=(log 3-log 2)/12>0. A interação ainda não aparece neste módulo: seu acoplamento às marginais será demonstrado pela dinâmica055. A não negatividade de C não demonstra dissipação, estabilidade, área geométrica, H3, temperatura física ou reconstrução gravitacional; a família escalar é periódica e a transferência de energia total soma zero.

## Fontes lidas e fronteira

- Chatgpt/DiagonalStateCurve.lean: registro DiagonalStateCurve e regularidade da entropia relativa.
- Chatgpt/DiagonalRelativeEntropy.lean: relative_entropy_identity.
- Chatgpt/RelativeEntropyFisherLimit.lean: relative_entropy_quadratic_zero_iff.
- Chatgpt/UnitaryMarginalDynamics.lean: frequency_sin_square_limit e exemplo de curva de estado.
- Chatgpt/UnitaryEntropyResponse.lean: importação que disponibiliza os contratos anteriores.
- Mathlib/Analysis/SpecialFunctions/Log/Basic.lean: monotonicidade do logaritmo no domínio positivo.

Código em inglês, namespace ChatgptAudit.Exchange055, #print axioms para cada declaração. Nenhum axioma novo, execução de um.py, edição de original, alteração de selo ou compilação nesta gravação. H3=OPEN; physical_reconstruction=OPEN; canonical_gate_changed=false.

Emissão UTC: 2026-09-07T07:21:34.387094+00:00
