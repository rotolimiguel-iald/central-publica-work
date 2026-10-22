# Continuação052 — plano horizontal de Pauli e resposta efetiva

[DERIVED — derivação anterior ao código; ainda sem compilação052]

Fixar SiteProfile P, p=P.w 0∈(0,1), r=2p−1. Os operadores X=sitePauliX P 0 e Y=sitePauliY P 0 pertencem à mesma álgebra local já representada na torre035. Definir A(v)=v₀X+v₁Y para v:Fin 2→ℝ, usando escalares complexos reais.

A esperança E é exatamente (aperiodicExpectationInput P).E, construída046. global_expectation_restricts_to_pinching aplicado ao corte0 reduz EX e EY ao pinching das respectivas matrizes. Para p≠1/2, os pesos p e 1−p diferem, eliminando as duas entradas fora da diagonal; logo EX=EY=0. Para p=1/2, o pinching local é identidade e E fixa X e Y. Não há hipótese de período comum nem novo postulado de esperança.

Usar X²=Y²=I, XY=iZ, YX=−iZ e ωZ=r. Os geradores A(v) são autoadjuntos e centrados. O pareamento completo é

    ω(A(u)* A(v)) = u₀v₀+u₁v₁ + i r(u₀v₁−u₁v₀),

onde o asterisco indica adjunto. Consequentemente a parte real é o produto euclidiano dos coeficientes, a imaginária é r vezes a área orientada, e ‖A(v)Ω‖²=v₀²+v₁². Em particular XΩ e YΩ têm norma1 e parte real do produto interno zero. A norma é GNS, não uma alegação geral de norma de operador1.

O elo com estados deve usar a curva existente035: f_B(t)=orbitExpectation P (A(v)) 0 B t 0 = ω(U(t)* B U(t)), U(t)=exp(+itA(v)). As derivadas verdadeiras fornecidas pelo teorema035 são iω(BA−AB). Para as leituras fixas X e Y:

    d Re f_X/dt|₀ = −2r v₁,
    d Re f_Y/dt|₀ =  2r v₀.

O mapa dessas duas respostas é linear com matriz [[0,−2r],[2r,0]] e determinante4r². Para r≠0 é injetivo: duas direções com a mesma resposta em todo observável têm, em particular, a mesma resposta em X e Y, logo os mesmos coeficientes. Isto demonstra direções efetivas da órbita unitária no fator; não classifica todos os tangentes do espaço de estados. A relação matricial equivalente δρ=i[A,ρp]=r(v₀Y−v₁X) orienta os sinais, mas não substitui a derivada operacional da torre.

Em p=1/2, a resposta local desaparece, EX=X/EY=Y e a parte imaginária é zero. Não se aplica o argumento de injetividade. A stationariedade não é necessária para os enunciados locais; thirdThermalReference fornece uma instanciação não tracial concreta.

APIs previstas: pauliHorizontal; pauli_horizontal_add/smul/mem_factor/selfadjoint/state; aperiodic_pauli_x_zero/y_zero; pauli_horizontal_expectation; pauli_horizontal_pairing/re_pairing/im_pairing/gns_norm_sq; leituras horizontais reais, derivadas, matriz de resposta e injetividade. Todos os resultados permanecem locais ao plano do primeiro sítio. Não se afirma kerE global=span{X,Y}, Fisher, Bures, área gravitacional ou H3.

Custódia: criação exclusiva em Chatgpt, antes do fonte LocalHorizontalPauli.lean; revisões exigem backup exato de bytes. Originais e selos≤051 permanecem somente leitura.
