[REAL — construção compilada das potências imaginárias pelo resolvente; OPEN — identificação da ação modular e traço de A1(b)]

# A1 — o grupo do mesmo S* S, sem novo GNS

Este adendo registra a ponte construída em 14/09/2026. Os módulos são fornecedores da bancada; ainda não foram embutidos no programa terminal. Os hashes, horários e reproduções pertencem ao manifesto e aos relatórios acompanhantes.

## O que foi construído

O fornecedor `scalarClosedTomita_graph_eq_weight` já identifica o S fechado com a estrela do peso escalar completo. O fornecedor `scalarTomitaResolvent_graph` já identifica T com o resolvente (I+S* S)⁻¹, incluindo o domínio do operador parcial. Esses fornecedores foram reutilizados.

Para um operador limitado T em Hilbert complexo completo, com 0≤T≤I e T, I−T injetivos, a construção introduz

    b(x) = x(1−x),
    g_t(x) = b(x) exp(i t log((1−x)/x)),
    B = T(I−T),
    C_t = cfc(z ↦ g_t(Re z), T).

O log usado é o log real da biblioteca. A função amortecida está definida e é conjuntamente contínua em todo ℝ×ℝ, inclusive x=0,1, onde b=0. Não foi necessário estendê-la por zero fora [0,1]. No espectro real de uma contração positiva só interessa [0,1], e no interior a razão (1−x)/x é positiva.

As identidades verificadas são

    C_0 = B,
    C_t* = C_−t,
    C_s C_t = B C_{s+t},
    C_t* C_t = B²,
    |C_t| = B,
    ‖C_t x‖ = ‖B x‖.

A positividade de B e sua injetividade implicam imagem densa. A imagem de C_t também foi provada densa: C_t C_−t=B² e Ran(B²) é densa. Não se infere imagem densa da mera injetividade de um operador arbitrário; não se supõe B⁻¹ limitado.

O fornecedor existente `denseLinearEquiv` estende a isometria definida na imagem de B e produz uma equivalência linear isométrica sobrejetiva U_t, caracterizada por

    U_t B = C_t.

A lei U_s U_t=U_{s+t} é demonstrada primeiro em Ran(B²), depois por densidade. U_0=I. O cálculo funcional dá continuidade de t↦C_t na norma de operadores; a identidade acima dá continuidade em Ran B, e a estimativa isométrica uniforme estende-a a todo Hilbert. A continuidade conjunta de (x,t)↦U_t x foi provada. Não se afirma continuidade de t↦U_t na norma de operadores.

## Aplicação ao objeto concreto

`scalarTomitaResolvent_complement_injective` usa o J efetivamente construído a partir de S e sua relação JTJ⁻¹=I−T para descarregar a segunda injetividade. A primeira, a positividade e T≤I já estavam provadas. Logo, **para todo SiteProfile P**, `scalarTomitaImaginaryPower P t` é construído no **ScalarGNSHilbert P original**, sem receber um novo estado, GNS ou operador modular como hipótese.

Sua caracterização por U_t b(T)=g_t(T), com T=(I+S* S)⁻¹, é a definição concreta da fase exp(it log(S* S)) pelo resolvente. Não é uma igualdade por homônimo com alguma API abstrata de potências de LinearPMap: tal API não foi usada. `scalarTomitaImaginaryPower_unique` prova a unicidade entre mapas limitados que satisfaçam essa caracterização. Grupo, inversa e continuidade forte foram especializados ao objeto concreto.

## Pagamento e próximo consumo

O subpasso **construir Δ_ν^{it} a partir do mesmo Δ_ν=S* S** está pago pelos cinco módulos. Isso retira uma lacuna específica da implementação modular.

Ainda não foi provada a identificação

    U_t π_ν(a) U_−t = π_ν(λ_t a λ_−t)  para todo a∈regularCoreAlgebra P.

Os fornecedores da escala resolvente matricial e do transporte pelo J original continuam disponíveis; não devem ser reprovados. Os próximos lemas de ponte, ainda [OPEN], são:

1. **Escala funcional:** de TR=R Q_r, Q_r=T[rI+(1−r)T]⁻¹, obter U_t R=exp(it log r) R U_t. Transportar também b(Q_r)=b(T) r[rI+(1−r)T]⁻²; o cancelamento é por imagem densa. Esses nomes são descrições de obrigações, não alegações de declarações já existentes.
2. **Conjugação antiunitária:** de JTJ⁻¹=I−T, obter JU_tJ⁻¹=U_t. Conjugação de i e inversão do log cancelam os sinais. A fórmula com U_−t não é o alvo correto.
3. **Consumo dos geradores:** combinar essas pontes com `matrixUnit_polar_conjugate_generator`, `scalarTomitaPolar_regular_generator`, a aproximação `represented_levelExpectation_strong_tendsto` e `scalarGNS_commutation_from_generators`, para a identificação modular em toda π_ν(N).

A igualdade das automorfias não implica, isoladamente, igualdade literal U_t=π_ν(λ_t)R_−t; uma ambiguidade no comutante permanece possível. A consulta independente registra uma rota por vetores positivos regularizados caso esse consumidor adicional seja necessário. Não introduzir Γ(1), porque a unidade tem peso infinito.

Depois ainda faltam o gerador positivo h afiliado com h^{it}=λ_t e a perturbação por h⁻¹ que produza τ fiel, normal, semifinito, tracial e com τ∘θ_s=e⁻ˢτ. A invariância de ν não substitui essa construção. A cobertura de todo o predual por séries, aberta no adendo anterior, não foi necessária para construir o grupo e não deve virar uma camada obrigatória sem consumidor.

## Validação e limites

Cinco módulos, 39 declarações: compilação autora com Lean 4.31.0, sem avisos, só `propext`, `Classical.choice`, `Quot.sound`. Dois controles matemáticos adulterados foram recusados: duplicar a norma da fase e substituir s+t por s−t na lei concreta de grupo. Os fontes e objetos bons permaneceram idênticos após os controles.

As tentativas fracassadas, incluindo um timeout determinístico de elaboração no corolário de continuidade, foram preservadas. O timeout foi resolvido explicitando o tipo da função de composição, sem aumentar o limite de heartbeats. Os `sorryAx` que o Lean imprimiu em tentativas de elaboração malsucedidas pertencem exclusivamente a resultados recusados; não há `sorry` no fonte candidato.

A auditoria autora reconferiu 448 pares de dependências herdadas e todos os arquivos dos três manifestos anteriores. A revisão independente, com compilação própria, é registrada à parte e precisa estar concluída para a entrega ser emitida.

A1(a) permanece PAGO. A1(c) está PAGO no delta. **A1(b) permanece NÃO PAGO:** nem o habitante de RegularCoreTraceData nem uma impossibilidade tipada foram produzidos. A2–A7 não foram iniciados. Nenhum Python do programa, original canônico, resultado de natureza, memória de outra casa ou gate foi alterado. O objetivo A1 permanece ativo.
