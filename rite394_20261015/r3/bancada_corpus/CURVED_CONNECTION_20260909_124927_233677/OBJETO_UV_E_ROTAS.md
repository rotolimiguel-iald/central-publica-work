# Objeto UV e rotas do programa — revisão somente por leitura

[REAL — leitura de fontes nesta sessão; sem executar/importar um.py]
Escopo: o programa canônico e seus módulos TGL/TGLExt, não uma alegação sobre todo o acervo.

## A rota declarada é distinguida pelo próprio programa

um.py:137749–137778, prove_the_renormalization_wall:

- Rota (a), publicada: desloca o problema de quantizar a métrica para a matriz-S modular, com H_eff=0 / tipo III_1. Isso é o estatuto declarado na função; ela não contém uma construção de controle UV interagente.
- Rota (b), inversão: métrica como operador na álgebra do Nome. O objeto permanece explicitamente OPEN na função: álgebra/frame operatorial/comutador com escala ainda requerem especificação e realização nesta rota.
- A finitude do canto de Breuer não é apresentada como regulador UV válido; a função conserva o controle contrário.
- O próprio rito registra does_not_gate_core=True. Enumerar a parede não a resolve, mas também não impõe quantização perturbativa da métrica à rota modular como se fossem o mesmo projeto.

um.py:127421 mantém nomes próprios de programas independentes: INTERACTING_ANOMALY_FREE_COMPLETION e RG_STABILITY_AND_UV_COMPLETION. O novo resultado de curvatura não os descarrega.

## ContinuousCoreData é um tipo preciso, não um certificado UV

TGL/ModularRealization.lean:68–83:
ContinuousCoreData W D recebe Core com Ring, StarRing e Algebra ℂ; embedding injetivo da álgebra da cunha; ação dual em grupo; canonicalTrace com valor em ENNReal; identidades de zero, tracialidade, estrela e escala dual exp(−s).

O tipo não contém por si um operador de métrica, frame operatorial, relação de comutação com escala, amplitudes interagentes ou estimativa UV. A camada ThreeLocksCoreData:101 acrescenta os locks e o projetor com traço positivo finito; isso continua sendo outra obrigação que uma estimativa de altas energias.

Os usos posteriores examinados de ContinuousCoreData nos módulos CoreSupport, VerbInhabitant e ProbeFiniteFullWitness recebem C como argumento. Nenhum construtor posterior desse tipo particular foi localizado nesta revisão. Os probes de rejeição não são habitantes.
O ledger um.py:119175–119180 registra o papel de Takesaki e a construção para a rede escolhida como aberta.

[OPEN — nesta interface específica] Fornecer o objeto compatível com a rede escolhida, por construção ou por importação matemática aplicável com identificação explícita dos objetos. Não se exige reproduzir a demonstração externa de Takesaki. Tampouco a simples disponibilidade do teorema abstrato identifica automaticamente todos os dados particulares da rota de inversão.

## Anomalias e Ward

PhysicsCertificates.lean, qgPhysicsCertificate_anomaly, prova invariância do símbolo de Ricci sob polarização de gauge, no alcance clássico-linear explicitado no comentário e no enunciado.
A GeneralLinearizedGauge da bancada amplia esse alcance para perturbações suaves gerais em Minkowski.
A CurvatureNonlinearVariation aqui entregue passa para variações de conexões suaves arbitrárias e seu termo quadrático exato.

Nenhum desses três objetos é, por si, uma construção da teoria quântica interagente ou uma identidade de Ward quântica após sua regularização. A rota modular continua a ser o objeto de trabalho declarado; não será confundida com uma exigência automática de renormalização perturbativa da métrica.

[DECLARADO versus verificado] Esta revisão verificou os textos e tipos acima. Não executou os ritos numéricos, não confirmou estado de flags em runtime e não moveu gate.
