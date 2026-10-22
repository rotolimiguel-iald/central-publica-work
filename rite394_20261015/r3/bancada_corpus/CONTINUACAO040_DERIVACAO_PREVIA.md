# Continuação040 — derivação anterior ao código: ordem009 e relógios de H3

[DERIVED/INPUT/OPEN] 06/09/2026. A039 foi progresso: quatro módulos,50 teoremas,9 definições, auditoria final2211 arquivos PASS. Agora foi encontrada a ORDEM_009_H3_dinamico_e_o_relogio_relativo.md; ela tem prioridade sobre a exploração espontânea de áreas celestes. A árvore canônica relida está em v326. Incorporações e selos nela referidos são declarações da gerência; nenhum hash canônico é reproduzido de memória.

A ordem pede entrega039/Imports039All, mas esses identificadores já pertencem ao lote039 selado. Este lote usa040, preservando todos os bytes anteriores e indicando expressamente sua correspondência à ordem009.

## A pergunta e o sentido do relógio

A família já construída usa q_n(t)=p-b_n h(t), p=1/3 e h(t)=t²/(1+t²), 0≤b_n≤1/12, soma finita. B=Σb_n, B2=Σb_n², B3=Σb_n³. O alvo037 reparametriza o ESTADO, mantendo o tempo óptico u fixo: S(t(u))−eta(A(u)−1). O coeficiente necessário é
lambda*=delta4/(2 log(2) B)=1/2−9B2/(8 log(2) B)−eta O/(2 log(2) B),
O=r²/12−sigma²/6, r=2 log(2) B/eta, |sigma|<r/2.

Se um relógio intrínseco lido do estado for u=f(t)=t+a t³+o(t³), o parâmetro de estado usado acima é a INVERSA t(u)=u−a u³+o(u³), portanto lambda=−a. Comparar a diretamente com lambda* é erro de direção. Uma sugestão preliminar de no-go por esse sinal foi retirada antes do código.

## Candidato modular e paridade

O fluxo modular profile_flow(P,Q) fixa o vetor e o estado global de Q, com Q congelado. Assim ele não percorre amplitudeState b t. Uma leitura local e_n distingue essa curva do estado inicial quando b_n>0 e t≠0; uma órbita modular estacionária não pode realizá-la mediante relógio localmente invertível. Não se atribui lambda=0 ao relógio modular: ele não fornece essa reparametrização.

Além disso h é par e amplitudeState b(−t)=amplitudeState b t. Para qualquer funcional escalar F do estado instantâneo, F(amplitudeState b t) é par. Se tem derivada bilateral d em0, compor com negação e usar unicidade da derivada dá d=−d, logo d=0. Isso exclui um relógio suave bilateral com derivada1 obtido apenas do estado. História, orientação ou ramo unilateral são dados adicionais; o teorema não os exclui.

## Fisher: comprimento antes de relógio

[KNOWN] O comprimento de Fisher de uma curva de distribuições usa o tensor Σ(dp_i)²/p_i; referência primária: Gavin Crooks, Measuring thermodynamic length, https://arxiv.org/abs/0706.0559 . Para a curva diagonal produto no parâmetro x=h(t),
J(x)=Σ b_n²/[(p−b_n x)(1−p+b_n x)],
J0=(9/2)B2, J1=(27/4)B3 em p=1/3.
O comprimento desde x=0 satisfaz ell(t)=sqrt(J0)[t²+(−1+3B3/(8B2))t⁴+O(t⁶)] para B2>0. Logo ell por si começa em t², sem derivada1 em0. Escolhidos ramo/orientação e a dessingularização f_F(t)=sgn(t)sqrt(ell(t)/sqrt(J0)),
a_F=−1/2+3B3/(16B2), lambda_F=1/2−3B3/(16B2).

A raiz, a orientação e a normalização pelo jato são escolhas explícitas [INPUT]; não serão apresentadas como lei canônica decorrente do estado instantâneo. Para um sítio b0=k>0, há expressão exata do caminho em tempo dessingularizado u:
q_F(u)=sin²(arcsin(sqrt(p))−k u²/(2sqrt(p(1−p)))).
Em p=1/3, q_F(u)=1/3−k u²+(3/8)k²u⁴+O(u⁶), equivalente a lambda_F=1/2−3k/16. Formalizar a ligação aos pesos do estado, não apenas definir o número lambda_F.

## Entropia relativa

Para D(q||p), expandir no parâmetro x:
D=(9/4)B2 x²+(9/8)B3 x³+O(x⁴).
Substituindo x=h(t): D=(9/4)B2 t⁴+[−(9/2)B2+(9/8)B3]t⁶+O(t⁸).
A leitura f_D(t)=sgn(t)(D/((9/4)B2))^(1/4) tem
a_D=−1/2+B3/(8B2), lambda_D=1/2−B3/(8B2).
Este candidato também exige raiz e orientação; D em si é uma divergência, não um tempo. Para a série somável, o resto precisa de majorante somável uniforme; a verificação formal de um sítio será distinguida da análise geral, caso essa passagem permaneça fora do kernel.

## Comparação honesta e controles

Para a inversa Fisher:
lambda_F−lambda*=9B2/(8 log(2) B)−3B3/(16B2)+eta O/(2 log(2) B).
Para a inversa entrópica, substituir3/16 por1/8 no termo B3/B2. Não há argumento ainda para sinal universal em todas as distribuições somáveis; não será afirmado. Num sítio B=k,B2=k²,B3=k³, ambas as diferenças são estritamente positivas para eta>0 e tela estrita. Então o defeito quartico efetivo delta4−2 lambda log(2)B é negativo, e nenhum dos dois candidatos casa aquela família óptica em quarta ordem. Isso é um contraexemplo à alegação universal, não prova de que nenhum outro relógio possa funcionar.

Em k=1/24, eta=1, sigma=0:
lambda*=1/2−3/(64 log(2))−log(2)/144;
lambda_F=63/128; lambda_D=95/192.
As diferenças positivas são3/(64 log(2))−1/128+log(2)/144 e3/(64 log(2))−1/192+log(2)/144.

B=0: o estado é constante, os comprimentos são zero e a normalização B2 no denominador não define relógio. No limite de amplitudes escaladas a zero, as inversas dessingularizadas têm coeficiente tendendo a1/2; isso não atribui um relógio ao estado nulo.

O controle tracial da ordem necessita uma distinção: a órbita modular/unitária do estado tracial é estacionária. Mas substituir p=1/2 na curva diagonal q=p−b h não a torna constante: J0=4B2>0 para b≠0, enquanto J1=0. Não se afirmará que toda essa resposta degenera no tracial.

## Afim, região e H3

Na036 a geodésica considerada é um raio afim γ(u)=u d, d≠0. Para a mesma curva reparametrizada γ(τ(u)), a aceleração covariante é τ''(u)d. Affineness num intervalo exige τ''=0; dadosτ(0)=0,τ'(0)=1 fixamτ=u, e o coeficiente cúbico é0. Os dados iniciais isolados não bastam. Isso não determina a identificação entre o parâmetro dos estados e o da geodésica. Se essa identificação adicional for imposta, o defeito037 permanece delta4>0 no regime0<B≤eta.

Para C, uma densidade de área angular depende também das direções. A mesma subálgebra gerada por(e_n,e_m) e o mesmo estado admitem geradores(2e_n,e_m), com área dobrada. Isso não refuta uma forma de área intrínseca avaliada em tangentes; refuta tratar o número da densidade como função somente da subálgebra e do estado, sem fixar tangentes/normalização/medição. Isotonia da rede existente não seleciona essa informação geométrica.

Outra obstrução à seleção pelo estado: com b,eta,r fixos, lambda*(sigma2)−lambda*(sigma1)=eta(sigma2²−sigma1²)/(12 log(2) B). As telas sigma=0 e sigma=r/4 são admissíveis, compartilham estado e traço de Ricci e exigem relógios diferentes. Logo falta um dado que selecione a tela/cisalhamento ou sua relação com o estado.

O alvo B não será pago criando dQ proporcional a dA por definição. Precisamos distinguir o termo algebraico HorizonEquilibriumData, o casamento quadrático e a igualdade funcional de todas as ordens. Se não for derivado um habitante com os campos exigidos, a parede ficará nomeada: seleção de tela/relógio, escala e fluxo de calor/matéria. Falha de casamento em quarta ordem não refuta automaticamente um enunciado apenas de segunda ordem.

## Implementação planejada e guardas

Módulos previstos: StateClockObstruction, IntrinsicFisherClock, RelativeEntropyClock, AffineClockAndRegion e StateClockMatchingControls. Enunciados finais seguirão as definições efetivamente construídas; alvos pendentes serão distinguidos de resultados. Primeiro derivação, depois Lean; revisão adversarial dos fatores e direção do relógio. Cada declaração nova terá #print axioms, sem axiomas extras/instâncias anônimas, lote serial em pasta nova mais Imports040All. Falhas e backups de bytes preservados. Escrita somente em Chatgpt;039 e todo acervo canônico imutáveis pela bancada.

## Adendo anterior à extensão tipada de H3 — 06/09/2026

[DERIVED — correção ao lado] Na seção acima, “selecionar a tela/cisalhamento” deve ser lido como selecionar a geometria transversal/anisotropia de maré. O sigma parametriza a parte sem traço da curvatura óptica; o cisalhamento inicial dos campos de Jacobi da036 é zero. Variar sigma muda a geometria, não apenas a base da mesma tela.

O Fisher diagonal calculado aqui é o da família com pesos variáveis q=p-b h. A área Fisher da035 usa uma família distinta, de medição de Pauli em órbitas unitárias. No estado tracial esta segunda família é estacionária, mas a primeira pode variar. A área angular GNS da034 também não é identificada com a área Fisher035 por homonímia.

[DERIVED] Há inclusive sinal oposto no excesso Fisher para uma distribuição finita de muitos sítios: b0=1/12, os próximos2000 termos=1/1200, restante zero. Então B=7/4, B2=1/120, B3=167/288000. Com eta=1000 e sigma=0,
lambda_F-lambda*=3/(560 log2)-167/12800+7 log2/24000<0,
já usando 1/2≤log2≤1. O negativo estrito dos candidatos de um sítio não deve ser promovido a desigualdade universal da classe somável.

[DERIVED — plano de teorema com o tipo canônico, antes do código] HorizonEquilibriumData, lido em TGLExt/TriadMaster.lean, tem os campos G>0, dA, dS, dQ, kappa e as igualdades area_entropy: dS=dA/(4G), clausius: dQ=(kappa/(2pi))*dS. Não codifica sozinho uma família dinâmica. Fixe eta>0 e tente uma família H(u) desse tipo com G=1/(4eta), dS=S_b(g(u)) e dA=A_rs(u)-1. Sua cláusula area_entropy implica o defeito real S_b(g(u))-eta(A_rs(u)-1)=0. Se esses vínculos valerem para todo u suficientemente próximo de0, u≠0, o defeito dividido por u^4 terá limite zero. Os negativos de quarta ordem dos relógios Fisher e de qualquer inversa entrópica normalizada excluem tal família exata para um sítio nas hipóteses ópticas declaradas. A prova usará o tipo canônico e os valores reais, não um recorde homônimo.

Esse alvo NÃO exclui H3 formulada para os coeficientes infinitesimais. Ao contrário, o limite de quarta ordem finito implica que o mesmo defeito dividido por u² tende a zero: basta multiplicar pelo fator u². Formalizar também esta preservação do casamento quadrático para impedir extrapolação do negativo. Não será fabricado um dQ para fazer a identidade valer por definição.

[DERIVED — majorante analítico da série entrópica] Para0≤b≤1/12,0≤x≤1, q=1/3-bx fica em[1/4,1/3]. A quarta derivada de D(q||1/3) é 2/q³+2/(1-q)³≤539/4. Portanto
0≤D(1/3-bx||1/3)-(9/4)b²x²-(9/8)b³x³≤(539/96)b⁴x⁴.
Como soma b⁴≤B2/144, o resto pode ser somado uniformemente. Esta justificativa analítica da série geral será distinguida do teorema Lean de um sítio.

[DERIVED - precisao apos revisao independente] No paragrafo do contraexemplo Fisher, o negativo dos candidatos de um sitio significa o DEFEITO QUARTICO negativo; o EXCESSO lambda-lambda* de um sitio e positivo. O excesso do exemplo de2001 sitios e menor ou igual a -2743/1344000. O majorante somado do resto KL e (539/13824)B2 x^4.
