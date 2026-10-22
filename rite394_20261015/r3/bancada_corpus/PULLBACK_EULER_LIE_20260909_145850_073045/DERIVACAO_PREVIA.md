# Derivação prévia — pullback efetivo de Euler e derivada de Lie

[INPUT] Na carta real de dimensão quatro, φ_t(x)=x+t V(x). Para V diferenciável em x, Dφ_t(x)=I+t DV(x). Essa igualdade será provada para a derivada de Fréchet efetiva e também para o Jacobiano coordenado; não será apenas uma denominação.

[DERIVED — a verificar] J_t=I+t P, P=DV_x; J_0=I e dJ_t/dt=P. Para g diferenciável em x, d[g(φ_t(x))]/dt em zero é ∑_k V^k ∂_k g. A regra do produto aplicada a J_tᵀ g(φ_t(x)) J_t produz Pᵀg+∑_k V^k∂_k g+gP, igual à função canônica coordinateMetricLie. O lema coordinate_metric_lie_matrix_formula de LieMetricJets será usado explicitamente.

A prova pontual precisa apenas de diferenciabilidade de g e V em x. Um corolário com campos suaves no aberto U fornecerá esses requisitos. A família temporal é real e a derivada matricial final será HasDerivAt, obtida das derivadas de todas as componentes.

[DERIVED — a verificar] Continuidade do determinante e det J_0=1 dão det J_t>0 para t suficientemente próximo de zero, em cada x fixo. A abertura de U e φ_0(x)=x garantem φ_t(x)∈U localmente. Não se afirma raio uniforme em todos os x.

[OPEN / limite] A família de Euler não é apresentada como fluxo exato de V. Não será afirmado difeomorfismo global, completude do fluxo, inversa global, compatibilidade de atlas ou conservação/matching físico. Não se pretende demonstrar naturalidade não linear finita de Einstein neste módulo; o alvo é ligar a direção de Lie a um pullback métrico efetivo.

Escritas somente nesta nova pasta Chatgpt; fontes originais e módulos congelados permanecem em leitura. Nenhum um.py é executado/importado.
