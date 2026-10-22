# Continuação 033 — densidade centralizante, logaritmo e inscrição angular

[REAL / KNOWN / DERIVED / INPUT / OPEN] 06/09/2026. Bancada ChatGPT. Continuação espontânea da ordem 007 e da pergunta do operador sobre a área como leitura angular quadrática de L. Três módulos finais compilaram em Lean: 34 teoremas e três definições impressas, sem erros, avisos ou sorryAx nos resultados finais. A auditoria e incorporação da gerência permanecem pendentes.

## Resultado formal

[INPUT] A família permanece aquela construída nas etapas 028–032: referência de sítio (1/3,2/3), amplitudes somáveis 0≤b_n≤1/12, h(t)=t²/(1+t²), gerador limitado autoadjunto L, filtro R=exp(L/2), estado psi(A)=omega(R A R). Nenhum resultado desta entrega afirma que todo estado normal admite densidade limitada nessa representação.

[REAL] CentralizerDensity.lean constrói uma subálgebra complexa com a condição concreta
C_omega={A∈M : para todo B∈M, omega(A B)=omega(B A)}.
O fechamento por multiplicação usa omega(A C B)=omega(C B A)=omega(B A C), com todos os produtos dentro de M. Seu fechamento em norma já estava provado; somas locais e limite dos prefixos colocam L nessa subálgebra. A série exponencial coloca R, H=exp(L) e u_s=exp(isL) nela. A construção não define o fluxo modular para obter essa conclusão.

[REAL] LikelihoodDensityLog.lean define H=exp(L) e demonstra:
- H=R²; H é positivo, autoadjunto, invertível e pertence a M;
- omega(H)=1;
- CFC.log(H)=L e CFC.log(R)=L/2;
- se K é limitado autoadjunto e exp(K)=H, então K=L;
- exp(is CFC.log(H))=u_s, com unitariedade.

O logaritmo é o cálculo funcional contínuo real da biblioteca, aplicado com a hipótese efetiva de auto-adjunticidade. Não se atribui o nome log(H) a L como substituto de prova. A unicidade do logaritmo exige K autoadjunto; não se estende a todos os logaritmos complexos.

[REAL] DensityStateUniqueness.lean demonstra, para todo A∈M,
psi(A)=omega(H A)=omega(A H).
A passagem de omega(R A R) para essa fórmula usa a pertença de R ao centralizador.

A unicidade é mais geral: se H,K∈M e omega(H A)=omega(K A) para todo A∈M, então H=K. Escolhe-se D=H−K e A=D*. A hipótese dá omega(D D*)=0; a fidelidade aplicada a D* dá D*=0 e, portanto, D=0. Positividade das densidades concorrentes não é necessária para esse lema.

[REAL] O mesmo módulo demonstra omega(u_s* A u_s)=omega(A) para todo A∈M. Esta invariância vale na álgebra inteira, não apenas em níveis finitos. A etapa 032, reconferida por seu auditor somente leitura, conserva a igualdade de operadores com domínio: Delta_rel=exp(L)Delta_omega.

## Identificação analítica do cociclo

[KNOWN/DERIVED] Para o estado normal fiel omega, H positivo invertível no centralizador e psi(A)=omega(H^(1/2) A H^(1/2)), Pedersen–Takesaki dá [Dpsi:Domega]_s=H^(is). Aplicando o resultado a H=exp(L)=R², obtemos [Dpsi:Domega]_s=exp(isL)=u_s. A normalização omega(H)=1 já está provada. A normalidade plena decorre externamente da fórmula vetorial, e a condição de comutação do estado identifica o centralizador canônico. Referência: [Hiai, Lema 9.1 e Teorema 9.4(2)](https://arxiv.org/pdf/2004.02383#page=84).

[OPEN — formalização] Essas pontes gerais da literatura não são apresentadas como novos teoremas compilados. Continuidade WOT sequencial não foi promovida a normalidade plena. O teorema geral de Pedersen–Takesaki, potências imaginárias do operador modular relativo não limitado e cálculo funcional conjunto continuam fora do que foi formalizado nesta entrega. A igualdade acima é uma especialização matemática justificada pela literatura; sua dependência está explícita. A identificação integral com entropia de Araki também não foi formalizada aqui.

## A hipótese angular do operador

[DERIVED] A distinção proposta é matematicamente fértil: o gerador L, a fase u_s e sua resposta quadrática são objetos diferentes. Para L limitado autoadjunto, o cálculo funcional fornece
u_s=exp(isL),
F_s=(u_s−I)*(u_s−I)=2I−u_s−u_s*=4 sin²(sL/2).
Aqui o asterisco do primeiro fator indica adjunto. A fase pura satisfaz u_s* u_s=I; a informação angular está na diferença em relação à identidade.

[REAL] Positividade de F_s, a fórmula 2I−u_s−u_s* e a convergência F_s/s²→L² em norma já estavam demonstradas na 030. A 033 acrescenta phase_quadratic_time_even: F_(-s)=F_s. Logo essa leitura não distingue, sozinha, os sentidos de ida e retorno.

[DERIVED — análise, não novos lemas Lean] Se por módulo se entende a raiz positiva, |u_s−I|=sqrt(F_s)=2|sin(sL/2)|, e sqrt(F_s)/|s|→|L|. Se se entende módulo ao quadrado, a leitura é F_s. São ordens diferentes: o limite ||L(t)||=O(t²) fornece sqrt(F_s)=O(t²) e F_s=O(t⁴) para s fixo. A escolha entre essas operações não foi assumida em nome do operador.

[KNOWN/DERIVED] Para um vetor unitário xi e uma leitura que identifica fases globais, a distância quadrada mínima é
min_theta ||u_s xi−exp(i theta)xi||²=2−2|<xi,u_s xi>|.
Seu coeficiente em s² é Var_xi(L), e não simplesmente <L²>_xi. Por exemplo, L=cI pode produzir F_s não nulo enquanto o raio do vetor permanece fixo. Esse exemplo é um teste geral de interpretação, não uma nova instância normalizada da família de estados acima. A distinção entre métrica projetiva e variação vetorial é tratada no [tensor geométrico quântico, equações 36–38](https://arxiv.org/pdf/2309.03621#page=5).

[REAL/DERIVED] Há um teste ainda mais específico desta torre: omega permanece invariável sob a conjugação por u_s, conforme o teorema compilado. Portanto uma órbita de vetores GNS pode ter movimento sem alterar o estado restrito a M. Analiticamente, psi também é invariável porque u_s comuta com R; essa segunda invariância não foi acrescentada como teorema Lean nesta etapa. F_s continua sendo um observável legítimo, mas interpretá-lo como distância entre estados físicos exige identificar os observáveis, uma referência interferométrica ou o acesso à purificação. A distinção operacional de estados tem formulação em [Braunstein–Caves](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.72.3439).

[DERIVED] Para gerar área bidimensional por uma métrica induzida de fases, um teste mínimo é haver duas direções reais independentes. Com um único gerador fixo e U(q)=exp(i f(q)L), a métrica projetiva é
g_ab=Var(L) partial_a f partial_b f,
de posto no máximo um: sua área bidimensional é zero. Isso não exclui L variando realmente em direções independentes.

Uma construção com dois geradores K_1,K_2 usa g_ab=Re<delta K_a xi,delta K_b xi>. O teste de área é det(g)>0. Em C³, xi=(1,1,1)/sqrt(3), K_1=diag(1,0,0), K_2=diag(0,1,0), dão g=(1/9)[[2,−1],[−1,2]], det(g)=1/27. Este é um exemplo analítico exato de área métrica em espaço de parâmetros; não foi incorporado como prova de área física da TGL. Mesmo geradores comutantes podem produzir essa área; curvatura de Berry não é requisito.

[OPEN] Para identificar essa área com uma superfície gravitacional, faltam uma superfície/região definida independentemente, a correspondência com as deformações, a escala dimensional e a prova da igualdade entre as áreas. Definir A=c omega(F_s) não demonstra por si essa identificação. L como cauda/poço e a inscrição angular como o ponto onde a luz dobra são interpretações propostas pelo operador; não há nesta etapa uma identificação provada com potencial, trajetória luminosa ou gráviton.

[DERIVED/OPEN] Retorno não implica atração: L=diag(−1,1) dá F_s=4 sin²(s/2)I, com retornos e sem amortecimento. A evolução unitária preserva distâncias no espaço completo. Estabilização de observáveis reduzidos pode ser uma hipótese pertinente, mas pede uma dinâmica e um sentido de convergência especificados. O próximo teste geométrico deve confrontar duas deformações observáveis independentes, sua métrica e uma lei de retorno demonstrável.

## Verificação, revisão e custódia

As três compilações finais apresentam exit 0 e fontes estáveis, com todos os 34 teoremas e três definições cobertos por #print axioms. Somente propext, Classical.choice e Quot.sound aparecem. As contagens incluem lemas auxiliares; não medem porcentagem de conclusão de gravidade quântica.

Uma revisão independente somente leitura não identificou erro matemático ou circularidade nos três módulos. Ela conferiu o centralizador concreto, as hipóteses do logaritmo, a prova de unicidade, a distinção entre potências limitadas e modulares não limitadas e as pontes externas. Não substitui a recompilação e aprovação da gerência.

Foram preservadas as tentativas rejeitadas: a primeira positividade de H exigiu corrigir o uso do adjunto; no módulo de unicidade, duas tentativas de acesso ao fechamento por adjunto falharam na resolução de classes. A versão final usa, no controle de invariância, a identidade u_s*=u_(-s) e a pertença desse cociclo a M. Nenhuma hipótese matemática foi enfraquecida para compilar. Backups são cópias dos bytes, e o auditor preserva os logs rejeitados.

Todos os novos arquivos estão sob Chatgpt. Originais, kernel canônico, um.py, Atlas, memórias, selos, gates e entregas anteriores permanecem intocados pela bancada. O registro está nesta entrega para a gerência auditar e incorporar nas superfícies canônicas. A última ordem encontrada continua sendo a 007. A prova ampla e a reconstrução gravitacional geral permanecem abertas.
