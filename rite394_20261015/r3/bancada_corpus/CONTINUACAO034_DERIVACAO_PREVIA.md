# Continuação 034 — duas direções angulares e teste de área observável
06/09/2026. [INPUT/DERIVED/OPEN] Derivação anterior ao código. Continuidade da ordem007 e da hipótese angular do operador.

A entrega033 foi reconferida: auditor somente leitura PASS. O avanço pretendido é testar a ponte área/fase na torre já existente, sem identificar área física por definição.

## Construção dentro da torre
Para SiteProfile P, sejam e_n=siteZeroProjection P n, p_n=P.w n, com 0<p_n<1. Os e_n são projetores autoadjuntos no centralizador e comutam entre sítios. A fatorização do estado-produto deve demonstrar omega(e_n e_m)=p_n p_m quando n≠m.
Os vetores centrados v_n=(e_n−p_n I)Omega satisfazem <Omega,v_n>=0, ||v_n||²=p_n(1−p_n) e <v_n,v_m>=0 para n≠m.

A órbita angular efetiva é U(s,t)=exp(is e_n) exp(it e_m). Ela é unitária e preserva omega na álgebra inteira. As derivadas em (0,0) são i e_n Omega e i e_m Omega. Remover suas componentes na direção complexa de Omega produz i v_n e i v_m. Assim a matriz real de Gram projetiva é diag(p_n(1−p_n),p_m(1−p_m)); seu determinante é positivo e sua densidade de área é a raiz do determinante.
Não bastará definir os vetores como tangentes: a relação com as derivadas da família exponencial será demonstrada.

## Teste de interpretação
A mesma órbita tem estado constante sobre M. Logo sua área projetiva positiva é uma geometria de vetores/purificações, não uma demonstração automática de área entre estados observáveis em M.
A comparação decisiva será entre dois sítios distintos e um único sítio repetido. O primeiro fornece Gram de posto dois e área positiva; o segundo, posto um e área zero, embora ambos preservem o mesmo estado em M. Uma função apenas desse estado não pode reproduzir simultaneamente essas duas leituras de órbita sem saber quais deformações estão sendo consideradas. Isso restringe os dados necessários, sem afirmar impossibilidade geral de geometria quântica.
Errata pré-código após revisão independente: escalar coordenadas modifica a densidade de área, não é por si uma diferença geométrica intrínseca. O teste usará a diferença de posto, e não reescalonamento apresentado como nova geometria.

## Refinamento do teste operacional, antes do módulo de integração
Para evitar confundir uma métrica com sua avaliação em tangentes escolhidas, o teste final usa derivadas de leituras. Para qualquer coleção finita de observáveis fixos A_i∈M, a aplicação q↦Re< U(q)Omega,A_i U(q)Omega > é constante. Seu jacobiano real J é zero, logo Jᵀ G J=0 para qualquer matriz real G sobre essas leituras. Essa métrica induzida não pode coincidir com o Gram positivo da órbita de purificações. O teorema é sobre essa órbita e esses observáveis fixos, sem impedir leituras como omega(F_s), nas quais o observável também varia, nem observáveis fora de M. A métrica abstrata de estados precisa de vetores tangentes para produzir área; não se confunde essa necessidade padrão com uma impossibilidade de reconstrução geral.

## Alvo e limites
[REAL apenas após compilar] Momento/produto, derivadas, Gram, positividade da área e invariância do estado, com axiomas usuais somente. [KNOWN] O uso de Gram das derivadas horizontais como métrica projetiva é a definição padrão; será separado da identificação gravitacional.
[OPEN] Esta etapa não deriva assinatura lorentziana, escala dimensional, região-algebra, lei de estabilização ou área de uma superfície gravitacional a partir do estado. Ela deve dizer qual dado adicional pode distinguir deformações fisicamente acessíveis. Se aparecer uma obstrução, será preservada e usada para escolher a próxima rota, sem redefinir a meta ampla.

Toda escrita somente em Chatgpt, originais e etapas seladas readonly. Backups de bytes antes de revisões próprias; compilações seriais; tentativas rejeitadas preservadas; revisão independente separada da gerência.
