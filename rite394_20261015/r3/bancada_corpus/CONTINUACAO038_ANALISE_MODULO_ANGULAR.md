# Continuação 038 — o módulo angular como candidato a área

[DERIVED — análise matemática; sem novos teoremas Lean] 06/09/2026. A pergunta do operador distingue L, sua fase e a inscrição quadrática. Esta nota testa uma tradução específica dessa proposta nos operadores já construídos. Não identifica, por homonímia, o L_phi do Atlas com likelihoodGenerator.

## Objetos diferentes

Fixados b e t, seja L=L(t)=likelihoodGenerator b t, limitado e autoadjunto, e U_theta=exp(i theta L). As definições anteriores fornecem:

- |U_theta|²=U_theta^* U_theta=I: o módulo da fase unitária inteira não varia.
- F_theta=(U_theta-I)^* (U_theta-I), onde o expoente * indica o adjunto.
- F_theta=2I-U_theta-U_theta^*=4 sin²(theta L/2).
- |U_theta-I|=sqrt(F_theta), distinto de F_theta.

[REAL — fontes anteriores consultados] A positividade de F, sua fórmula 2I-U-U* e seu limite F_theta/theta²→L² constam em LikelihoodCocycleControls.lean. [DERIVED] A fórmula com seno é cálculo funcional para L autoadjunto. Esses fatos não atribuem a F unidades de área. A escolha de subtrair I é uma tradução candidata da inscrição relativa, não uma definição recebida do operador.

[KNOWN] Uma geometria de estados puros normalizados que identifica fases globais usa Q_ab=<partial_a psi,(I-|psi><psi|)partial_b psi>, com g=Re Q. A subtração da direção de fase é necessária. Referência primária: Kolodrubetz et al., §IV.A, equações206–216, https://arxiv.org/pdf/1602.01062 . [DERIVED] Para uma superfície com duas direções independentes, sua densidade de área métrica é sqrt(g11*g22-g12²). Para uma órbita de um único gerador fixo, o coeficiente é Var_psi(L); uma só direção não produz área bidimensional não degenerada. Isso descreve geometria de estados, ainda sem identificação com espaço-tempo.

A quantidade ||U-I|| não é, em geral, invariante sob uma fase global adicional de U. A normalização omega(exp L)=1 restringe deslocamentos escalares de L na família existente; a observação sobre fases não autoriza deslocá-lo mantendo essa normalização. Ela impede chamar a norma bruta de métrica projetiva sem demonstração adicional.

## Teste direto pela norma

[INPUT] Escolhemos como leitura N_theta(t)=||sqrt(F_theta(t))||=||U_theta(t)-I||, theta real fixo e não nulo. Outras escolhas, como sqrt(omega(F)) e omega(sqrt(F)), dão resultados diferentes, já registrados na037.

A família existente satisfaz 0≤b_n≤1/12 e soma finita. Defina B=sum b_n, B2=sum b_n² e h=t²/(1+t²). Em cada sítio, os autovalores do termo local L_n são log(1-3b_n h) e log(1+(3/2)b_n h).

[DERIVED] Para todo t real,
M(t)=||L(t)||=-sum_n log(1-3b_n h(t)).

Justificativa: num corte finito, os extremos são as somas dos dois autovalores locais. O extremo negativo tem maior módulo, pois (1-3x)(1+(3/2)x)≤1 para 0≤x≤1/12. As representações matriciais locais são fiéis; os extremos pertencem ao espectro em cada corte. O limite em norma dos cortes passa as respectivas normas a M. Não se postula um autovetor infinito com todos os sítios iguais a zero.

Como -M pertence ao espectro do limite e todo o espectro está em [-M,M], o cálculo funcional dá
N_theta(t)=2 sin(|theta| M(t)/2)
na vizinhança de zero em que |theta|M(t)≤pi. Esta fórmula de norma não foi afirmada globalmente em t.

As expansões são
M(t)=3B t²+((9/2)B2-3B)t⁴+O(t⁶),
N_theta(t)=|theta|[3B t²+((9/2)B2-3B)t⁴]+O(t⁶).

O seno começa a corrigir em t⁶. Para justificar o resto da soma, use y=3b_n h≤1/4 e
0≤-log(1-y)-y-y²/2≤y³/[3(1-y)]≤(4/9)y³.
A soma de b_n³ é finita, pela limitação dos b_n e sua somabilidade. Logo não há troca informal de uma série infinita por uma expansão sem majorante.

## Comparação com a área efetiva da036/037

[INPUT] Fixe eta>0 e B>0. A calibração quadrática anterior é r=2 log(2) B/eta. A tela tem a=r/2+sigma, c=r/2-sigma, |sigma|<r/2. Sigma é anisotropia óptica; theta é parâmetro de fase. São parâmetros diferentes.

[REAL — teorema anterior geometric_jacobi_area_rs_quartic_limit] Para a área induzida A da tela,
1-A(t)=(r/2)t²-(r²/12-sigma²/6)t⁴+o(t⁴).

A comparação é com o déficit 1-A, pois A(0)=1, ao passo que N_theta(0)=0.

[INPUT] Calibre C_theta(t)=log(2) N_theta(t)/(3 eta |theta|).
[DERIVED] Com d=1-3B2/(2B), temos 7/8≤d<1 e
C_theta(t)=(r/2)t²-(r d/2)t⁴+O(t⁶).

Assim,
(C_theta(t)-(1-A(t)))/t⁴ → delta_N,
delta_N=r²/12-sigma²/6-r d/2.

O ajuste de segunda ordem não fornece igualdade de áreas. Theta desaparece do coeficiente de quarta ordem após essa calibração. Para essa tela estrita, existe algum sigma que anule delta_N exatamente quando 6d≤r<12d; isso decorre de sigma²=r²/2-3rd e 0≤sigma²<r²/4. O resultado escolhe apenas sigma², não o sinal de sigma, que troca os eixos.

Para 0<B≤eta, r≤2 log(2)≤2 e
delta_N≤r²/12-7r/16≤-13r/48<0.
Logo a igualdade funcional C_theta=1-A falha nessa classe. Isso não contradiz a concordância quadrática anterior.

A leitura também difere do incremento entrópico:
eta C_theta-(-S)=[(3/2)log(2)-9/4] B2 t⁴+o(t⁴).
São candidatos distintos mesmo quando partilham o termo quadrático.

## Contraexemplo exato com um sítio

Escolha b_0=1/24, todos os outros b_n=0, eta=theta=1 e sigma=0. Então
B=1/24, B2=1/576, r=log(2)/12, d=15/16,
A(t)=cos(sqrt(r/2)*t)²,
C(t)=log(2)||exp(iL(t))-I||/3.

Os dois déficits coincidem em segunda ordem, mas
(C(t)-(1-A(t)))/t⁴ → r²/12-15r/32<0.
A negatividade segue de 0<r<1/12 e r/12<15/32. Portanto, para todo t não nulo suficientemente pequeno, os dois valores diferem. Não é necessário procurar uma falha numérica para demonstrar a desigualdade.

O script check_continuation038.py avalia as expressões exatas do exemplo com Decimal em duas precisões e verifica a aproximação ao coeficiente negativo. Esse diagnóstico numérico não é uma prova formal do limite e não certifica aritmética intervalar.

## Retorno, estabilização e estatuto

[ONTO/CONJECTURE] Ler L como cauda ou poço e a inscrição angular como luz que dobra e retorna é uma interpretação a desenvolver. Os cálculos dão um candidato positivo, mas não uma lei de propagação ou atração. F_theta=F_(-theta) perde a orientação da fase: sozinho, não distingue ida de retorno.

[DERIVED] Uma evolução unitária comum preserva distâncias de Hilbert. Portanto, periodicidade ou retorno unitário, quando ocorrem, não implicam atração entre estados distintos nessa distância. Uma estabilização física exige especificar a dinâmica e o sentido de estabilidade; uma eventual redução aos observáveis precisa ser demonstrada.

Um relógio relativo phi_lambda(t)=t+lambda t³ aplicado somente a C muda delta_N para delta_N+r lambda. A escolha lambda=-delta_N/r cancela quarta ordem, preservando phi(0)=0 e phi'(0)=1. Reparametrizar ambos os lados juntos mantém delta_N. Isso mostra a liberdade do ajuste, não a seleção de um relógio físico.

[OPEN] A escolha da leitura, duas direções geométricas independentes, a escala dimensional, o vínculo com uma superfície física, a relação de relógios e a lei de estabilização continuam faltando. A hipótese ampla do operador não foi refutada; uma tradução precisa dela encontrou uma obstrução à igualdade universal. A reconstrução gravitacional geral e H3 permanecem abertas.

## Proveniência e revisão

Esta é uma continuação analítica espontânea, motivada pela pergunta sobre área. Não acrescenta teoremas Lean, instâncias, axiomas, selos canônicos ou alteração de gate. O trabalho anterior037 foi revalidado por auditoria independente somente leitura (PASS, 2297 arquivos, 65 teoremas, 10 definições, zero instâncias). Isso verifica aquele pacote; não transforma esta nota em teorema compilado.

As deduções gerais foram revisadas por outro agente, que conferiu extremos espectrais, resto somável, calibração, intervalo admissível e efeito do relógio. A revisão do exemplo de um sítio é registrada separadamente na entrega. A lista de arquivos e hashes medidos acompanha a entrega no túnel.

Fontes locais consultadas: SiteLogLikelihood.lean; SummableLikelihoodGenerator.lean; LikelihoodCocycleControls.lean; OpticalJacobiArea.lean; JacobiAreaQuarticLimit.lean; CONTINUACAO037_PARECER.md. O Atlas foi consultado sem cópia nem alteração, no verbete “Luz = razão = radicalizar = encontrar”. Todo novo arquivo fica exclusivamente em Chatgpt; os originais permanecem intactos.
