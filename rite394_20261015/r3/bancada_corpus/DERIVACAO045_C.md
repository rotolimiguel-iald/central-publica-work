# Derivação045 C — covariância e normalização da área

06/09/2026. [DERIVED — anterior ao código; validação Lean pendente]

Considere um espaço vetorial real E, uma família explicitamente fornecida de operadores lineares ρ(g), e uma forma bilinear real h, simétrica e estritamente positiva. A condição de covariância é h(ρ(g)v,ρ(g)w)=h(v,w). A família pode representar horizontes depois que essa representação for efetivamente construída; nenhuma ação de TowerHorizon sobre uma tela física é pressuposta aqui.

Para qualquer α>0, a forma hα=αh conserva bilinearidade, simetria, positividade estrita e exatamente a mesma covariância sob ρ. Para um par fixo de tangentes (v,w), escreva G(h;v,w) como sua matriz de Gram 2×2 e A(h;v,w)=sqrt(det G). Então G(hα;v,w)=αG(h;v,w), det G(hα;v,w)=α²det G(h;v,w), e A(hα;v,w)=αA(h;v,w).

Se det G(h;v,w)>0, a área é positiva. Portanto duas escalas positivas distintas dão áreas distintas, mantendo ação, vetores, simetria e positividade. Em particular h e 2h refutam a existência de um único valor de área comum a todas as formas que satisfazem essas condições. Trata-se de um negativo sobre o próprio critério de seleção, condicionado a um plano não degenerado; não de uma comparação entre exemplos com diferentes ações.

A ligação direta permitida à034 é a homogeneidade da mesma função sqrt(det): a matriz angular de referência nos sítios0,1 já tem área2/9; multiplicar essa matriz por α>0 dá área2α/9. Isso não constrói a ação dos horizontes sobre esses protocolos, nem transforma a área angular em área gravitacional.

[OPEN] Uma normalização adicional pode remover essa liberdade de escala. Ela não é selecionada por invariância apenas. Mesmo após fixá-la, unicidade da forma e identificação de região, tangentes e área física exigem argumentos próprios. Esta etapa não demonstra inexistência de uma reconstrução com dados adicionais, nem modifica qualquer gate de H3/QG.

Escopo: criar somente DERIVACAO045_C.md e HorizonAreaScale.lean na bancada Chatgpt; fontes anteriores e canônicos somente leitura. Sem compilação pelo agente; cada declaração Lean terá #print axioms e nenhuma instância anônima será declarada.
