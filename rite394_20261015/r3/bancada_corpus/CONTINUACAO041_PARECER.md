# Continuação 041 — área angular e calor da tela de Jacobi

06/09/2026. [REAL / DERIVED / INPUT / OPEN]. Complemento à ordem009. Compilação final e auditoria independente do build concluídas; o manifesto final reúne a evidência desta entrega.

A ideia do operador distingue o gerador e sua leitura geométrica: a área poderia surgir de uma inscrição angular quadrática. Há uma formulação matemática coerente dessa proposta, mas a identificação física e o retorno estabilizador continuam abertos. A contribuição nova desta etapa é calcular uma primitiva efetiva do fluxo na tela036 e testar sua relação com a área, além da ordem quadrática.

## A precisão sobre L e a fase

[DERIVED] Se L é autoadjunto limitado e Uθ=exp(iθL), então Uθ*Uθ=I. A resposta variável à identidade é
Fθ=(Uθ−I)*(Uθ−I)=4 sin²(θL/2)≥0.
Ela não é automaticamente uma área. Além disso, Fθ ainda contém a fase global: L=cI pode dar Fθ≠0 embora o raio do estado não mude.

[KNOWN] Para um vetor normalizado ψ, retirar a componente paralela ao próprio estado dá a tangente horizontal i(L−〈L〉I)ψ, onde 〈L〉=〈ψ,Lψ〉. Sua norma quadrática é a variância de L. Com duas direções horizontais vi, a matriz gij=Re〈vi,vj〉 é semidefinida positiva e a densidade de área é sqrt(g11*g22−g12²), positiva quando as duas direções reais são independentes. É a construção usual da métrica quântica; referência primária: Kolodrubetz et al., “Geometry and non-adiabatic response in quantum and classical systems”, [artigo dos autores](https://arxiv.org/abs/1602.01062). Uma fase global isolada não produz essa geometria.

[REAL — enunciados existentes consultados] AngularScreenMetric.lean constrói o Gram de duas direções GNS centradas. AngularAreaObservability.lean demonstra que, na família centralizante estudada, a área da purificação pode ser positiva enquanto o estado restrito ao fator permanece constante. A035 constrói outra família operacional; a040 mede a dependência da densidade de área nas tangentes/parametrização. Esses resultados não identificam a área GNS com uma área do espaço-tempo.

[OPEN / ONTO] O L=likelihoodGenerator=log H da030 e o L_phi registrado no Atlas ainda não estão identificados por uma ponte tipada. “Poço/cauda” e “luz que dobra e retorna como estabilização” são leituras propostas, não consequências da positividade. Fθ=F−θ também perde a orientação. Uma forma positiva não demonstra atração, equilíbrio dinâmico ou convergência.

## O fluxo calculado

[REAL — comprovado nos módulos041 compilados] Os módulos041 trabalham com os objetos existentes da036:
γ(t)=centralNullCurve(t), d=centralNullDirection e A(t)=geometricJacobiArea(a,c,t).
A é literalmente inducedArea da métrica waveSolder e das colunas geometricJacobiColumns. Seu valor é
A(t)=|cos(√a t) cos(√c t)|,
e vale A(0)=1. Os coeficientes a,c são autovalores da matriz de maré na tela; a+c é a contração de Ricci na direção nula normalizada.

Escolhida a matéria T=waveMatter(a,c,m), o lema wave_matter_quad e a normalização w(d)=1 dão T(γ(t))(d,d)=m. A041 define
f(t)=−κ t m A(t),     Q(t)=∫₀ᵗ f(u)du.
O teorema optical_heat_flux_geometric identifica esse integrando com a expressão completa envolvendo T, γ, d e inducedArea. FTC fornece Q'=f e Q(0)=0. A área positiva, com módulo, é usada na integral global; a passagem à expressão sem módulo só entra na expansão local, onde A>0.

[INPUT] A família de métrica, matéria, os parâmetros κ,m,η e a normalização afim pertencem à construção escolhida. Esta etapa não deduz sua seleção a partir de um estado quântico arbitrário. O peso afim −κt é mantido exatamente na fórmula do fluxo; não foi deduzido um campo de Killing que justifique essa escolha em todas as ordens. Modificar esse peso ou a matéria pode modificar o coeficiente quártico e exigiria outro teste.

[OPEN] Não construímos P:EquilibriumScreenData com esses campos. Esse tipo exige um campo nulo/geodésico suave num bairro aberto e compatibilidade de transporte da tela. A036 fornece os campos ao longo da geodésica; no caso curvo a+c>0, o vetor constante d não é nulo em todo esse bairro. Esta qualificação também esclarece a formulação abreviada da derivação prévia congelada: no controle plano a=c=0, d é nulo no bairro. Portanto Q é a primitiva do fluxo avaliado na tela de Jacobi; não declaramos sua igualdade com constructedHeat(P), nem um habitante novo de H3.

## O resultado de quarta ordem

[REAL — limites demonstrados em Lean041] Para a,c≥0, escrevendo r=a+c, os resultados037 dão
A(t)=1−r t²/2+(a²+6ac+c²)t⁴/24+o(t⁴).

O novo lema primitive_quartic_limit aplica l'Hôpital às derivadas reais, sem supor de antemão uma expansão da integral. Aplicado a Q(t)+κm t²/2, ele dá
limₜ→₀ [Q(t)+κm t²/2]/t⁴ = κm(a+c)/8.

[INPUT] Sob o casamento quadrático η(a+c)=2πm, defina o resíduo finito
C(t)=Q(t)−[κ/(2π)]η[A(t)−1].
A041 demonstra
limₜ→₀ C(t)/t²=0,
limₜ→₀ C(t)/t⁴=κη(a²+c²)/(24π).

Com r=a+c e σ=(a−c)/2, o segundo coeficiente é
[κη/(2π)]·[r²/24+σ²/6].
σ é anisotropia de maré, não cisalhamento inicial: a tela036 tem velocidade de Jacobi inicial zero.

[DERIVED] Para κ,η>0 e a+c>0, o coeficiente é positivo, C(t)>0 num entorno perfurado suficientemente pequeno e a igualdade FINITA exata de Clausius não vale eventualmente. A concordância quadrática é preservada. É um resultado sobre esta família e estas definições de incrementos; não refuta a relação infinitesimal de equilíbrio nem uma teoria gravitacional geral.

Não chamamos C de produção física de entropia: tal leitura precisa de lei dinâmica, interpretação e orientação adicionais. Na convenção usada, Q e A−1 podem ser negativos; positividade aqui se refere ao resíduo C, não ao próprio calor.

Controles incluídos:
- a=c=1, κ=m=1, η=π: casamento quadrático válido, coeficiente quártico=1/12.
- a=c=0: o casamento força m=0; Q=C=0 exatamente.

## A consequência para o relógio relativo

[DERIVED — cálculo analítico, NÃO formalizado nos módulos041] Para a família somável já construída, ponha ℓ=log2, B=Σbn e m=ℓB/π. O incremento renormalizado da expectativa da energia modular de referência é ΔK(t)=−ℓB·t²/(1+t²). Já ψ_t(L(t))=KL(ψ_t‖ω), com L(t)=log H(t): outro objeto, outra expectativa e outra ordem.

Se g(u)=u+λu³+o(u³), então
lim [Q(u)−κΔK(g(u))/(2π)]/u⁴ = κm(λ−1/2+r/8).
Para κm≠0, o casamento quártico calor–energia exigiria λQ=1/2−r/8. Esse valor vem do fluxo escolhido, em vez de ser escolhido para zerar o defeito entropia–área. Ainda é uma consequência condicional da família; não seleciona um relógio físico universal.

Nenhuma escolha de g altera o próprio C=Q−κη(A−1)/(2π) calculado acima, pois Q e A já estão definidos na mesma coordenada afim. Não há contradição entre a falha finita e o casamento de ordem dois.

## Validação e custódia

Os originais, um.py, kernel canônico, Atlas, memórias e entregas anteriores permaneceram somente em leitura. Artefatos041 e seus backups ficam exclusivamente em Chatgpt. A atualização canônica, se desejada, pertence ao operador/orquestrador pelo túnel.

O construtor clean_continuation041.py cria uma pasta inédita a cada execução, copia dependências locais com conferência de hashes dos manifestos029/032/033/034/035/036/037/040 e importa as revisões limpas mais recentes dessas etapas. A raiz irrestrita de Chatgpt não integra LEAN_PATH. Compila os módulos novos em série e depois Imports041All. Cada declaração tem #print axioms; erros, avisos, sorryAx e instâncias anônimas impedem PASS.

Limite da verificação: as dependências históricas pinadas não são recompiladas nesta etapa. Fontes canônicos sem pin histórico de fonte são lidos para descoberta de imports; isso não prova sua proveniência até o binário. Apenas dependências externas diretas são hashadas, não todo o fechamento transitivo de Mathlib/toolchain. O auditor041 confere bytes, fontes, logs, censo, cobertura de axiomas, cópias da fronteira, importador conjunto e estatutos do manifesto; não substitui revisão física.

Resultado da compilação final [REAL]: OpticalHeatFlow contém 12 teoremas e 2 definições; OpticalHeatClausius contém 9 teoremas e 1 definição. Total: 21 teoremas, 3 definições, 24 impressões de axiomas, zero instâncias. Os dois módulos e Imports041All passaram em diretório novo, com fontes iguais às cópias, entradas estáveis, zero erros/avisos/sorryAx e somente propext, Classical.choice e Quot.sound. Tentativas anteriores e backups foram preservados. A auditoria independente --build-only retornou BUILD_PASS/exit0: 2028 registros de arquivos do build e 163 registros históricos conferidos. O revisor também conferiu separadamente os três logs, metadados e cópias. O auditor completo é uma adaptação da040, incluindo resolução de imports e entradas congeladas; o primeiro auditor simplificado foi substituído antes da custódia final.

H3: OPEN. Reconstrução gravitacional geral a partir do estado: OPEN. Meta ampla de gravidade quântica: OPEN. Nenhum gate canônico foi alterado.
