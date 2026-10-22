[REAL / INPUT / KNOWN / OPEN] CONTINUAÇÃO 021 — entropia relativa e a ordem da ponte gravitacional

06/09/2026. A continuação 020 foi progresso: seu auditor reconferiu 591 hashes, sete módulos limpos, 48 teoremas e seis definições impressas. O túnel continua contendo somente ordens gerenciais 001–007. O objetivo amplo permanece ativo e não alcançado.

## O resultado que muda o próximo passo

A primeira lei diagonal existente controla a primeira variação do estado. A reconstrução geométrica de 020 exige que o resíduo de Clausius dividido por t² tenda a zero. A continuação 021 calcula o termo entre essas duas afirmações: a entropia relativa tem coeficiente quadrático F_p(q)/2, que zera exatamente quando a derivada inicial do estado é zero.

Foi construída uma resposta quadrática normalizada, p(t)=p+t²q, que satisfaz essa condição sem congelar o estado. A aplicação gravitacional fica reduzida a dois erros de identificação explicitados: entropia–área e calor–energia modular. O teorema tensorial recebe esses dois limites, e a resposta quadrática fornece a anulação da entropia relativa necessária para deduzir Clausius.

Isso é uma construção e uma implicação verificadas. O modelo físico ainda precisa fornecer as duas identificações e justificar a dependência quadrática do estado em relação ao parâmetro geométrico.

## Objetos e domínio da prova

diagonalRelativeEntropy(r,p)=Σ_i r_i(log r_i−log p_i).
modularIncrement(p,r)=Σ_i (r_i−p_i)(−log p_i).
diagonalFisher(p,q)=Σ_i q_i²/p_i.

A identidade D=ΔK−ΔS é exata para os funcionais definidos. A interpretação como entropia relativa usa pesos positivos e normalizados. A ponte modular_increment_is_generator_trace liga ΔK ao traço da variação da densidade diagonal multiplicada pelo MESMO diagonalModularGenerator já definido em 011. K aqui é o logaritmo negativo da densidade finita; a ligação física com o operador modular GNS e com o fluxo de calor continua OPEN.

DiagonalStateCurve p registra pesos r(t), sua tangente q(t), r(0)=p, normalização de traço, derivadas genuínas em zero e eventualmente à esquerda, e continuidade da tangente em zero. A soma das tangentes ser zero é demonstrada a partir da normalização. A positividade das componentes perto da origem é demonstrada a partir de p_i>0 e continuidade.

A extensão como função tem traço um em todos os tempos; a interpretação física de estado vale perto de zero, onde a positividade foi provada. Não se atribui essa interpretação aos valores polinomiais longe da origem. As hipóteses de derivabilidade e continuidade são locais; não se postula uma equação física para a evolução.

## O cálculo de segunda ordem

Para a curva normalizada, a derivada efetiva é

    D′(t)=Σ_i q_i(t)[log r_i(t)−log p_i].

O termo Σq_i(t) que aparece ao derivar x log x cancela por normalização. Cada quociente [log r_i(t)−log p_i]/t tende a q_i(0)/p_i. Logo

    D′(t)/t → Σ_i q_i(0)²/p_i,
    D(t)/t² → (1/2)Σ_i q_i(0)²/p_i.

O segundo limite usa o lema de primitiva quadrática já verificado, com derivada, continuidade, valor inicial e filtro t→0− explícitos. Não é um ajuste numérico. A forma diagonalFisher é não negativa e zera se e somente se q(0)=0.

Para a resposta afim p+tq, o coeficiente é F_p(q)/2. Para p+t²q, a tangente é 2tq e o coeficiente é zero. Nesta última família,

    ΔK(t)/t² → Σ_i q_i(−log p_i),
    ΔS(t)/t² → Σ_i q_i(−log p_i).

A família quadrática é um objeto matemático construído. Sua escolha não demonstra que o estado do programa evolui desse modo nem permite trocar livremente o parâmetro afim geométrico por uma perturbação do estado.

## A composição com os objetos geométricos

Escreva c=rate/(2π), A para a área da tela construída, Q para a integral temporal construída, e defina

    E_heat=Q−cΔK,
    E_area=ΔS−η(A−A(0)).

O resíduo B=Q−cη(A−A(0)) satisfaz B=E_heat+cD+cE_area exatamente. Sob os dois limites E_heat/t²→0 e E_area/t²→0,

    B/t² → rate/(2π)·F_p(q(0))/2.

Para rate≠0, a condição de Clausius de segunda ordem vale se e somente se q(0)=0. Na resposta quadrática, esse jato zero é construído e Clausius segue dos dois limites de identificação.

QuadraticScreenMatching contém referência positiva e normalizada, resposta de traço zero e os dois limites, aplicados à tela e ao calor efetivos de 020. Não recebe Clausius como campo. einstein_from_quadratic_microscopic_matching conclui G+Λg=(2π/η)T em U sob o fornecimento desses dados para cada ponto e direção nula, além de U aberto e IsPreconnected, solda e inversa suaves, T diferenciável/simétrico/conservado, rate≠0 e η≠0.

Esse teorema não torna o contrato automaticamente habitado no modelo geral. O número de hipóteses não é uma medida de fechamento físico: os dois limites precisam ser derivados de uma correspondência física independente.

Para uma curva de estados geral, comparar o novo coeficiente com o de 020 impõe

    η Ric(v,v)=2π T(v,v)+F_p(q(0)).

A fórmula é uma compatibilidade local CONDICIONAL. Não se construiu um tensor de Fisher covariante e conservado, nem se identificou esse termo com energia gravitacional ou uma correção física da equação de Einstein.

## Controles e contato com a torre

1. Referência p=(1/2,1/2) e resposta q=(1,−1): a primeira variação de S é zero, e D/t→0, mas D/t²→2. first_order_does_not_imply_second_order refuta a passagem automática entre as duas ordens.

2. Com a mesma referência e resposta quadrática, D/t²→0 e p(t) difere de p para t≠0. A eliminação do defeito não exige uma família constante.

3. Para p=(1/3,2/3), a resposta quadrática tem coeficientes de ΔS e ΔK iguais a log 2>0. nontracial_quadratic_response fornece esse controle não trivial.

4. state_curve_purification_near constrói, por reutilização da purificação explícita, densidades bipartidas positivas, normalizadas e idempotentes, cuja marginal direita é a densidade diagonal da curva. A entropia relativa calculada é a da marginal diagonal. Não se afirma uma fórmula para a entropia relativa entre as densidades bipartidas puras.

5. tower_quadratic_relative_zero instancia a construção nos pesos canônicos towerW(P,N), para cada andar finito e resposta de traço zero. Não se demonstrou coerência entre respostas de andares diferentes nem um limite de dinâmica.

6. flatVacuumMatching é um habitante efetivamente construído no fundo plano com T=0. Usa a tela e a integral de 020 e a resposta quadrática não constante. Os dois erros de identificação têm os limites requeridos. Isso demonstra consistência do contrato nesse controle, sem reivindicar uma correspondência microscópica geral.

7. O fundo plano com T=diag(1,0,0,0), simétrico e conservado, não admite QuadraticScreenMatching: sua existência produziria o Clausius já refutado em 020. O novo contrato preserva o negativo anterior.

## Relação com a literatura

[KNOWN] Jacobson 1995 recebe entropia proporcional à área e o balanço de Clausius para horizontes locais. A referência é uma derivação sob essas premissas, não uma prova de que qualquer estado KMS as satisfaz. [Fonte primária](https://arxiv.org/abs/gr-qc/9504004).

[KNOWN] Jacobson 2016 trata de primeira variação do vácuo e equilíbrio de entrelaçamento com volume fixo e hipóteses geométricas e de matéria; o caso não conforme envolve uma conjectura adicional. Não se transportou esse resultado ao modelo sem suas hipóteses. [Fonte primária](https://arxiv.org/abs/1505.04753).

[KNOWN] Lashkari–Van Raamsdonk distinguem a primeira lei do termo de segunda ordem da entropia relativa e relacionam a informação de Fisher à energia canônica no contexto holográfico considerado. O cálculo presente formaliza a face diagonal finita e não importa a identificação AdS/CFT para a torre. [Fonte primária, introdução e §2.1](https://arxiv.org/html/1508.00897v2).

## Fronteira remanescente e custódia

[OPEN] Modelo físico de resposta do estado, correspondência região–álgebra, coerência entre andares, limite não comutativo/tipo III, relação entre parâmetros, identificação de T, erros entropia–área e calor–energia modular, unidades e coeficientes físicos, hipersuperfície nula imersa, área espacial integrada, origem modular da solda e colagem global.

A auditoria local confere fontes, objetos compilados, logs, hashes, axiomas impressos e tentativas preservadas. Os números são lidos por script antes da entrega. Ela não substitui recompilação e leitura adversarial independentes pela gerência. As dependências locais e objetos TGL/TGLExt copiados são fixados; a biblioteca externa Lean 4.31.0/mathlib é resolvida pelo wrapper e não constitui um pacote portátil integral.

Todas as escritas estão em C:\IALD\Central de Patentes\Chatgpt. Backups são cópias de bytes; substituições passam por temporário verificado. Nenhum um.py executado, importado ou editado, nenhuma alteração de kernel canônico, Atlas, memórias, selos ou gate pela bancada. Nenhuma afirmação de gravidade quântica resolvida ou confirmada.

## Contagens verificadas antes da entrega

7 módulos com compilação final limpa, 49 teoremas e 3 definições com axiomas impressos separadamente. Foram preservadas 5 tentativas rejeitadas, incluindo uma compilação com avisos.

| Módulo | Teoremas | Definições impressas |
|---|---:|---:|
| DiagonalRelativeEntropy | 6 | 0 |
| DiagonalStateCurve | 7 | 0 |
| RelativeEntropyFisherLimit | 5 | 0 |
| QuadraticStateResponse | 6 | 2 |
| MicroscopicClausiusBridge | 5 | 0 |
| MicroscopicEinsteinBridge | 2 | 0 |
| RelativeEntropyGravityControls | 18 | 1 |

As contagens foram lidas dos fontes e logs pelo auditor. O manifesto final inclui este adendo e seu backup imediato. Nenhuma contagem de teoremas substitui a verificação do alcance de seus enunciados.
