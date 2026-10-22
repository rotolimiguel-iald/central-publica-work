[DERIVED / INPUT / OPEN] CONTINUAÇÃO 029 — existência de casamento entrópico em geometria curva e liberdade residual

06/09/2026. Derivação anterior ao código. A última resposta ao operador foi um esclarecimento de estado, sem nova demonstração; é classificada como NO PROGRESS para a meta persistente. A revalidação executou audit_continuation028.py: PASS, 730 hashes, 8 módulos, 112 teoremas e 6 definições impressas. Há somente ordens 001–007 no túnel. O Atlas declara incorporação até 023 na v317. Nada disso significa que H3 tenha sido derivada.

O alvo é construir e verificar um habitante curvo, com matéria não nula e com os estados globais reais da 028, para a condição harea em todas as telas locais. A construção escolhe uma família de métricas e resolve seu coeficiente de Ricci usando a resposta entrópica. Isso prova existência e mede a liberdade restante; não converte essa escolha em uma dinâmica microscópica ou em emergência geral.

Convenções da bancada: eta4=diag(1,-1,-1,-1); coordenadas (t,x,y,z). Tome k=(1,0,0,1), l=(1,0,0,-1), N=l⊗k. Temos N²=0. Para parâmetros a,c reais, H=a*x²+c*y², E=I+(H/2)N, D=I-(H/2)N. Provar E D=D E=I e
g=Eᵀ eta4 E=eta4+H k⊗k,
gInv=D eta4 Dᵀ=eta4-H l⊗l.
Ambos são suaves em todo R⁴. A assinatura lorentziana é herdada da escolha de eta4; não será alegada sua derivação.

Com v=(0,a*x,c*y,0), a conexão proposta é
Gamma_i^r_j = l_r (k_j v_i+k_i v_j)+v_r k_i k_j.
Derivar o primeiro jato de H e de g por fderiv. Provar que essa conexão é exatamente a Levi-Civita construída, sem nomear uma conexão independente como se fosse a geométrica. Provar seu jato e calcular o comutador/quadrado na definição de curvatura usada pela bancada.

A previsão, a conferir em Lean com os sinais locais, é
Ric=(a+c) k⊗k; scalarCurvature=0; Einstein=Ric;
R^1_{0 1 0}=a; R^2_{0 2 0}=c.
O covetor constante w=k é nulo em gInv, fechado e paralelo. Logo satisfaz a equação de onda e seu tensor escalar é T=kappa k⊗k, conservado. Demonstrar todas essas propriedades nos tipos existentes.

Para b:SummableAmplitude da 028, kappa=log(2)*sum b/pi. Para eta diferente de zero, definir r=2*pi*kappa/eta e escolher a=r/2+s, c=r/2-s, s livre. O balanço eta Ric(d,d)=2*pi*T(d,d) então segue do cálculo explícito; pela equivalência da 028, segue harea para toda tela local em toda direção nula não zero. Instanciar a construção localEquilibriumScreen e o casamento de calor. O Einstein da métrica satisfaz G=(2*pi/eta)T, com Lambda=0, sem uma hipótese harea no enunciado final desta FAMÍLIA ESCOLHIDA.

A família de estados usada continua amplitudeState b (frequency*time), frequency=k(d); suas marginais, fidelidade e limites conjuntos são os objetos provados nas 026–028. Evitar reduzir o casamento a uma função S definida à mão: fazer a ligação ao limite dos prefixos efetivamente lidos.

Controles adversariais:
1. O casamento deve impor a+c=r na família testada; parâmetro errado falha em direção nula explicitamente construída em x=0, onde g=eta4.
2. Variação de s mantém Ric, T e a família de estados, mas altera R^1_{0 1 0}-R^2_{0 2 0}=2s. Não inferir não-isometria global apenas de componentes em coordenadas.
3. b=0 e s≠0 dá Ric=0 e curvatura não zero: resposta entrópica nula não exige geometria plana nesta família.
4. b geométrico da 028 fornece matéria não nula e área correspondente. Registrar controles exatos, sem copiar hashes de memória.

[KNOWN] A família é uma onda plana de tipo Brinkmann escrita nas coordenadas acima, dentro de uma classe clássica de soluções exatas; não se reivindica sua descoberta. Referência de contexto a verificar: Matthias Blau, Plane Waves and Penrose Limits, https://blau.itp.unibe.ch/lecturesPP.pdf (o acesso inicial falhou; não usar conteúdo não lido). A prova local usará derivadas e álgebra exatas, sem importar resultados externos como axiomas.

[OPEN] A escolha do ansatz, de eta, de dimensão/assinatura, do covetor, da curva produto e do pareamento coeficiente–entropia é INPUT. Não deriva H3 para uma dinâmica microscópica geral, não constrói correspondência região–álgebra, correlações, energia positiva geométrica ou seleção de dados radiativos. A liberdade s testa precisamente uma parte da informação que a resposta de Ricci não controla. A meta ampla permanece ativa.

Escrita somente em Chatgpt. Originais, canônico, Atlas, memórias, selos, gate e entregas anteriores intocados. Auditoria independente e incorporação cabem à gerência. Tentativas rejeitadas e versões dos bytes serão preservadas.
