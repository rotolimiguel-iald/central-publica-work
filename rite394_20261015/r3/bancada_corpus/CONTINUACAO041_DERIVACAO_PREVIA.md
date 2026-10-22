# Continuação 041 — derivação prévia: fluxo na tela de Jacobi
06/09/2026. [DERIVED / INPUT / OPEN]

Escopo: responder à leitura angular do operador e testar a compatibilidade dinâmica da tela036. Nenhum original, selo anterior, Atlas ou um.py será alterado. Todos os artefatos novos ficam em Chatgpt; incorporação canônica permanece externa.

A distinção L/área exige cuidado: L=log H da030 e L_phi do Atlas ainda não têm identificação tipada. Para L autoadjunto limitado, U=exp(iθL) tem U*U=I; (U−I)*(U−I)=4 sin²(θL/2). Retirada a fase global de um vetor normalizado, a velocidade horizontal é i(L−〈L〉)ψ, cuja norma quadrática é Varψ(L). Uma área usa duas tangentes e sqrt(det Gram). A034 demonstra área de purificação positiva com estado restrito constante; a035 usa outra família operacional. Positividade não seleciona orientação nem prova retorno estabilizador. [OPEN] área física, dinâmica e estabilidade.

Alvo novo: primitiva do fluxo avaliado nos campos reais036, sem definir calor pela área. A geodésica γ(u)=u d satisfaz w(d)=1. Para T=waveMatter(a,c,m), T(γ)(d,d)=m. A(u)=geometricJacobiArea(a,c,u)=|cos(√a u)cos(√c u)| é a área induzida das colunas de Jacobi. Definir Q(u)=∫_0^u −κ s m A(s) ds. Este é o integrando geométrico usado em screenHeatFlux, avaliado na mesma γ,d,T,tela; não afirma existir P:EquilibriumScreenData. O campo constante d não é nulo num bairro aberto dessa métrica. A ponte com constructedHeat(P) permanece OPEN.

Para a,c≥0 e u próximo de zero, r=a+c e
A=1−r u²/2+(a²+6ac+c²)u⁴/24+o(u⁴).
FTC dá Q'=−κ u m A, Q(0)=0. Integrar o resto por l'Hôpital dá
(Q+κm u²/2)/u⁴ → κm r/8.

Impor APENAS o casamento quadrático ηr=2πm [INPUT] cancela o termo de ordem2 do resíduo C=Q−κη(A−1)/(2π). Então
C/u⁴ → κη(a²+c²)/(24π)
       = κη/(2π)·(r²/24+σ²/6), σ=(a−c)/2.
Para κ,η>0 e a ou c não nulo, o coeficiente é positivo. Portanto falha a igualdade FINITA exata de Clausius nessa família; C/u²→0 continua verdadeiro. Isto não refuta H3 infinitesimal nem toda dinâmica gravitacional. Não chamar o resíduo de produção de entropia sem uma lei física que o identifique.

Controle: a=c=1, κ=1, η=π, m=1 satisfaz casamento quadrático e coeficiente=1/12. a=c=0 dá A=1; com ηr=2πm resulta m=0 e Q=C=0. Anisotropia σ é de maré; a tela inicia com cisalhamento zero.

Consequência analítica possível (não afirmar Lean sem prova): se ΔK_b(t)=−log2 B·t²/(1+t²), m=log2 B/π e g(u)=u+λu³+o(u³), então (Q−κ ΔK_b(g)/(2π))/u⁴→κm(λ−1/2+r/8). O fluxo selecionaria λ_Q=1/2−r/8 para casamento quártico calor–energia, sob essas identificações. Isso não elimina o resíduo geométrico C independente de g.

Validação planejada: módulos novos OpticalHeatFlow e OpticalHeatClausius; compilação serial em diretório novo; fronteira histórica pinada incluindo040 quando necessário; importador conjunto; cada declaração com #print axioms; zero erros, avisos, sorry, axiomas extras e instâncias anônimas. Revisor independente somente leitura. H3 e meta ampla OPEN; nenhum gate movido.
