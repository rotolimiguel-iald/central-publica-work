# Domínio do peso e certificado da mesma representação — desenvolvimento

[REAL — Lean local, ainda sem integração ou revisão independente]
Cinco módulos, 17 alvos. Os hashes de fontes e binários e os logs aceitos
estão em modular_domain_draft_status.json. As tentativas anteriores falhas
continuam nos logs; nenhuma delas é tratada como prova.

ScalarModularInvariance prova invariância de ν por A↦Λ_t* A Λ_t. O argumento
usa as translações ordinárias no comutante de N, a bimodularidade da forma
dual e Δ^(it)Ω=Ω. Este resultado NÃO identifica o grupo modular: KMS falta.

RegularScalarWeightCertificate reúne 13 campos em Prop, parametrizados
pelo mesmo SiteProfile e referidos às definições efetivas de N, F, M, q e ν.
O construtor descarrega os campos, inclusive normalidade para redes de
universo arbitrário, densidade do ideal esquerdo e invariância. Não recebe
as propriedades como hipóteses residuais. O certificado ainda não é
consumido pelo gate Python e não contém traço ou dados físicos.

ContractionAdjointLimit prova: contrações que tendem fortemente à identidade
têm adjuntos que também tendem fortemente à identidade. O controle de norma
é essencial; não se usa continuidade geral da adjunção na topologia forte.
StrongBoundedApplication permite mover o vetor numa família de operadores
uniformemente limitada, com uma estimativa de norma explícita.

FiniteDualStarCore constrói a subálgebra complexa sem unidade I∩I*, onde I
é o ideal esquerdo de quadrados limitados da forma dual. Para todo A∈N,
A_h=X_h* A X_h pertence a essa subálgebra quando h>0, ||A_h||≤||A||, A_h→A
e A_h*→A* fortemente. Tanto ν(A_h* A_h) quanto ν(A_h A_h*) são finitos.
Não se afirma que A_h seja positivo para A arbitrário, que esteja abaixo de
A, ou que a aproximação seja em norma. Tampouco se identifica o domínio
algébrico com um espaço GNS completo antes de construí-lo.

[OPEN] Próximo passo matemático: inscrição GNS da forma ν e condição KMS,
seguida do gerador afiliado, perturbação e traço canônico com escala dual.
Three Locks/H1, H2/H3 físicos, estado quântico interagente, BRST/QME/anomalias,
UV, contrato ampliado consumido e runtime integral isolado permanecem no
objetivo. As seis flags maiores seguem false na integração custodiada.
Original preservado; este rascunho não amplia o escopo da custódia integrada.
