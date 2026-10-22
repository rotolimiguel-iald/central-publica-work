# Continuação 034 — área angular na torre e teste de observabilidade

[REAL / DERIVED / INPUT / OPEN] 06/09/2026. Continuação espontânea da ordem007. Quatro módulos finais passaram em Lean: 56 teoremas e 12 definições impressas, com fontes estáveis, zero erros, zero avisos e somente propext, Classical.choice e Quot.sound. Auditoria e incorporação da gerência pendentes.

Foi demonstrada, na torre já construída, uma distinção concreta: duas direções angulares podem ter uma densidade de área projetiva positiva, enquanto o estado restrito à álgebra M permanece constante. Para essa órbita, qualquer área induzida pelas derivadas de uma coleção finita de observáveis fixos em M é zero.

## Construção e escolha das direções

[INPUT] Para qualquer SiteProfile admissível P, usamos os projetores e_n=siteZeroProjection P n e p_n=P.w n, com 0<p_n<1. Eles pertencem ao centralizador do estado omega e comutam entre sítios. São os mesmos operadores que aparecem nos termos locais do gerador de verossimilhança L da030.

A família de duas fases é
U(s,t)=exp(is e_n)exp(it e_m),  xi(s,t)=U(s,t)Omega.
A escolha de dois índices e de dois parâmetros angulares independentes é uma entrada explícita deste teste. Ela não deriva duas coordenadas espaciais da torre. Tampouco identifica essa família inteira com o cociclo de uma única dupla de estados normalizados.

[REAL] CentralizerPhaseOrbit.lean prova unitariedade, pertença ao centralizador e diferenciabilidade real da família. Suas derivadas coordenadas na origem são i e_n Omega e i e_m Omega. A família preserva a norma do vetor e todas as distâncias de Hilbert quando atua sobre dois vetores quaisquer.

Define-se a componente horizontal por
h(v)=v−<Omega,v>Omega.
A norma unitária de Omega garante <Omega,h(v)>=0. AngularAreaObservability.lean identifica, usando as derivadas efetivamente provadas,
h(partial_s xi(0,0))=i(e_n−p_n I)Omega,
h(partial_t xi(0,0))=i(e_m−p_m I)Omega.
Não se utiliza o valor padrão de deriv em função não diferenciável.

## Covariância e área exata

[REAL] SitePhaseCovariance.lean demonstra a fatorização omega(e_n e_m)=p_n p_m para quaisquer índices distintos. A prova usa o pertencimento do sítio posterior à álgebra da cauda e a esperança condicional já construída, generalizando o argumento anteriormente usado no sítio zero.

Os vetores v_n=(e_n−p_n I)Omega satisfazem
<Omega,v_n>=0,
<v_n,v_n>=p_n(1−p_n)>0,
<v_n,v_m>=0 quando n≠m.

[REAL] AngularScreenMetric.lean forma a matriz real de Gram dos vetores i v_n e i v_m. Para índices distintos,
g_ang=diag(p_n(1−p_n),p_m(1−p_m)).
Assim det(g_ang)>0 e
a_ang=sqrt(det(g_ang))>0.

Para o mesmo sítio repetido, as quatro entradas do Gram são p_n(1−p_n), seu determinante é zero e sua densidade de área é zero. Duas coordenadas nomeadas não garantem duas direções independentes.

[REAL] No perfil thirdThermalReference, com p_n=1/3, os controles exatos são
a_ang(0,1)=2/9,
a_ang(0,0)=0.
São igualdades provadas em Lean, não aproximações numéricas.

[KNOWN/INPUT] O Gram das derivadas horizontais é a construção usual da métrica projetiva de uma família de vetores normalizados. A literatura distingue a métrica real da curvatura de Berry; ver [Hetenyi–Levay, equações36–38](https://arxiv.org/pdf/2309.03621#page=5). Aqui se prova a identificação das tangentes na origem. Não foi acrescentado um teorema de transporte dessa métrica por toda a órbita.

[OPEN] Reutilizar a função screenArea(h)=sqrt(det h), já existente na bancada, não constrói uma GeometricScreenAlong nem demonstra que h é a métrica induzida de uma superfície no espaço-tempo. O valor2/9 é uma densidade nas coordenadas angulares escolhidas, sem escala de comprimento e sem integração sobre uma superfície física.

## O estado observável e seu jacobiano

[REAL] O estado usado no teste é o funcional vetorial efetivo
omega_(s,t)(A)=<xi(s,t),A xi(s,t)>.
A identidade com omega(U* A U) foi provada para operadores limitados. Quando A pertence a M, a pertença de U ao centralizador e sua unitariedade dão
omega_(s,t)(A)=omega(A).
phaseRestrictedState tem domínio exatamente o subtipo theFactorObject P. A igualdade não é estendida a todos os operadores de B(H).

Escolha qualquer coleção finita de observáveis fixos A_1,...,A_k em M. Para as leituras reais
f_i(s,t)=Re omega_(s,t)(A_i),
os dois teoremas HasDerivAt mostram que suas derivadas são zero em todo(s,t). A constância do funcional complexo foi provada antes de tomar a parte real.

[REAL] observablePhaseJacobian é a matriz formada por essas derivadas reais efetivas. O código prova
J=0.
Para qualquer matriz real G de tamanho k×k,
g_obs=J^T G J=0,
screenArea(g_obs)=0.
Não são necessárias simetria ou positividade de G: o resultado zera qualquer ponderação matricial. Se G for escolhido como uma métrica, o mesmo resultado se aplica. Se variar com o ponto, a igualdade vale em cada ponto, pois quantifica sobre toda matriz G.

[REAL] Para n≠m, g_obs na origem não coincide com g_ang; suas densidades de área também são diferentes. reference_phase_area_split reúne no mesmo enunciado o controle a_ang(0,1)=2/9, a_ang(0,0)=0 e a_obs=0.

Esse é o resultado operacional desta entrega: nessa órbita centralizante, o Gram projetivo positivo não pode ser o pullback de uma ponderação dessas leituras fixas em M.

## O que esse teste permite concluir

[DERIVED] Uma área de purificação positiva não é suficiente para demonstrar uma área obtida de mudanças do estado observável na mesma álgebra. A geometria de distinguibilidade trabalha precisamente com a alteração dos estados sob medições; ver [Braunstein–Caves](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.72.3439). O presente teste mostra a constância de todo o estado em M, não apenas a insensibilidade de um observável escolhido.

O resultado não exclui omega(F_s), porque nessa leitura o próprio observável F_s varia com o parâmetro. Também não exclui observáveis fora de M, referências interferométricas, correlações com observáveis evoluídos, outras famílias de estados ou geometrias declaradamente atribuídas a purificações.

[OPEN] Não foi demonstrada uma impossibilidade geral de geometria quântica, nem ausência de área física. A hipótese do operador sobre inscrição angular continua possível, mas a identificação precisa dizer quais deformações e quais acessos observacionais representam a superfície.

[DERIVED] Reescalar coordenadas muda uma densidade de área. Isso não foi usado como prova de diferença geométrica intrínseca: a derivação foi corrigida antes do código para usar a diferença entre direções independentes e repetidas e, depois, o jacobiano observável efetivamente zero. Os backups preservam essa correção.

[OPEN] A preservação das distâncias no espaço completo não demonstra estabilização; ela serve de controle contra inferir atração apenas do retorno de uma fase. Convergência de observáveis reduzidos ou uma dinâmica dissipativa exigem seus próprios enunciados.

## Próxima construção que o resultado indica

[DERIVED — candidata analítica, ainda não formalizada nesta entrega] Há uma opção concreta dentro de M para testar posto observável dois: usar Pauli X em dois sítios distintos e ler Pauli Y nesses mesmos sítios. Com U=exp(is X_n)exp(it X_m), a derivada na origem é i omega([Y_n,X_n])=2(2p_n−1), e as derivadas cruzadas são zero por comutação entre sítios. No perfil1/3, isso sugere J=diag(−2/3,−2/3), det J=4/9>0.

Essas igualdades são a próxima proposta analítica, não resultados do compilador desta etapa. Elas deverão ser ligadas aos operadores reais da torre, às derivadas das expectativas e a um controle não degenerado. O objetivo é construir deformações que alterem estados observáveis, em vez de apenas renomear a área de uma órbita centralizante.

[OPEN] Mesmo um jacobiano observável não degenerado ainda não fornece o mapa região–álgebra, dimensão, assinatura lorentziana, escala ou igualdade com a área de uma tela gravitacional. A029 já exibe liberdade de curvatura residual para os mesmos dados entrópicos. Uma regra microscópica de acoplamento e evolução deve resolver essa liberdade; impor a correspondência como hipótese apenas a recolocaria no enunciado.

## Verificação, revisão e preservação

O auditor da033 foi reconferido em modo somente leitura: PASS,763 hashes, três módulos,34 teoremas e três definições impressas. O túnel continua contendo ordens001–007; esta entrega é espontânea e não substitui a entrega original dos alvos A/B/C da007.

Os quatro módulos034 finais têm56 teoremas e12 definições impressas. Todos os enunciados foram cobertos por #print axioms, sem sorryAx e somente com os três axiomas admitidos. Contagens incluem auxiliares e não representam uma porcentagem de conclusão física.

Uma revisão independente somente leitura não identificou erro matemático. Conferiu em particular a ligação com derivadas efetivas, a restrição do estado a M, a constância complexa anterior ao Re, o jacobiano das duas derivadas reais e a arbitrariedade de G. A revisão não substitui recompilação e aprovação da gerência.

Tentativas rejeitadas foram preservadas: CentralizerPhaseOrbit exigiu substituir uma simplificação excessiva e uma automação de diferenciabilidade por provas explícitas; SitePhaseCovariance exigiu explicitar a coerção de pertinência ao centralizador; AngularAreaObservability exigiu calcular o determinante2×2 zero explicitamente. Não houve mudança das afirmações matemáticas para compilar. Todos os backups são dos bytes exatos.

Originais, um.py, kernel canônico, Atlas, memórias, diários, selos, gates e entregas anteriores permanecem intocados pela bancada. Toda escrita está em Chatgpt. A prova ampla da gravidade quântica e a reconstrução geral permanecem abertas.
