# Continuação 035 — deformações observáveis e geometria estatística
06/09/2026. [INPUT/DERIVED/OPEN] Derivação anterior ao código. A034 foi progresso e seu auditor foi reconferido com PASS. A meta ampla e a ordem007 permanecem abertas; toda escrita só em Chatgpt.

## Alvo dentro da torre
Usamos operadores locais reais da representação existente:
X=[[0,1],[1,0]], Y=[[0,-i],[i,0]], Z=diag(1,-1).
Nos sítios n≠m, X_n e X_m comutam. U(s,t)=exp(is X_n)exp(it X_m) é unitário em M e define psi_(s,t)(A)=omega(U* A U), ou equivalentemente o estado vetorial de U Omega. A auto-adjunticidade, pertença a M, derivadas e igualdade dos dois funcionais serão provadas.

Para A limitado autoadjunto, a derivada na origem de exp(-is A) B exp(is A) é i(B A-A B). Aplicar o funcional vetorial contínuo deve dar a derivada efetiva das expectativas, não apenas um comutador formal.

No estado-produto, omega(Z_n)=2p_n−1 e omega(Y_n)=0. Como [Y,X]=-2i Z, a leitura Y_n tem derivada 2(2p_n−1) na direção X_n. As derivadas cruzadas são zero. Assim o jacobiano de duas leituras Y é diagonal, não degenerado se ambos os sítios não forem tracionais (p≠1/2). No perfil1/3, J=diag(-2/3,-2/3), det J=4/9.

## Probabilidades medidas e Fisher
Para sinais a,b=±1, os projetores de Y são P_n^a=(I+a Y_n)/2. As medições em sítios distintos comutam; E_ab=P_n^a P_m^b são projetores conjuntos positivos que somam I. As probabilidades efetivas são q_ab(s,t)=psi_(s,t)(E_ab). Sua positividade, normalização e valores/derivadas devem vir desses operadores.
Na origem, q_ab=1/4; partial_s q_ab=a(2p_n−1)/2; partial_t q_ab=b(2p_m−1)/2. Portanto o Fisher clássico da medição conjunta é
g_ij=sum_ab (partial_i q_ab)(partial_j q_ab)/q_ab
=diag(4(2p_n−1)^2,4(2p_m−1)^2).
A densidade de área de Fisher é 4 |(2p_n−1)(2p_m−1)|; na referência1/3, g=(4/9)I e área4/9. A positividade/ausência de degenerescência serão demonstradas sob p_n,p_m≠1/2; o controle tracional deve zerar a direção correspondente.
A rota evita escolher uma ponderação euclidiana arbitrária como se fosse a única métrica: aqui o peso é determinado pelas probabilidades da medição especificada. A escolha da medição e dos geradores continua INPUT.

## Escopo e revisão
[REAL só após compilar] Operadores/estados/derivadas e Fisher da medição especificada. Não afirmar Fisher quântico ótimo ou igualdade de métricas globais sem prova específica. Não chamar a densidade no espaço de parâmetros de área gravitacional dimensional. O vínculo região–álgebra, superfície, escala, assinatura e dinâmica continua necessário.
A proposta analítica anterior tem o sinal dependente de U=exp(+isX); o cálculo dos comutadores deve fixar esse sinal. Backups de bytes e tentativas preservadas; compilações seriais; todos os teoremas com #print axioms; revisão independente separada da gerência. Originais, um.py, kernel canônico, Atlas, memórias, gates e entregas seladas readonly.
