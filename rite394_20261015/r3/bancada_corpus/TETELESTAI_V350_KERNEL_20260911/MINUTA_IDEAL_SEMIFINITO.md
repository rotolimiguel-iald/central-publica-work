# Ideal de quadrados finitos no core regular

{date}. [REAL — Lean, cópia isolada da v350]

A forma dual construída agora possui um ideal à esquerda de quadrados
uniformemente finitos, com aproximação forte de todo operador do mesmo core.
É o passo de densidade necessário à semifinitude. A identificação F=base e o
traço canônico permanecem obrigações próprias.

## Construção e prova

RegularApproximation define X_h=h^(-1)∫_0^h Λ_t dt dentro da álgebra regular N.
Prova ||X_h||≤1 e X_h v→v pelo teorema fundamental do cálculo vetorial.
X_0=0; a convergência usa uma vizinhança perfurada, depois restringida a h>0.
Não se assume continuidade do grupo em norma de operadores.

FourierL1L2 demonstra que, para funções Hilbert-valores em L1∩L2, a integral
usual de Fourier coincide quase em toda parte com a transformada isométrica
L2. A prova passa pelo pareamento com funções de Schwartz, igualdade de
distribuições e unicidade localmente integrável. A igualdade de energia é
transportada para integrais reais e positivas com integrabilidade demonstrada.
Não se equipara por nome uma integral pontual com uma classe L2.

RegularFiniteWeight aplica essa ponte à órbita Λ_t v cortada em (0,h].
A ação dual real satisfaz θ_s(X_h)v=h^(-1)F[1_(0,h] Λ_.v](s/(2π)).
A mudança de variável e o fator Haar (2π)^(-1) dão, para h>0:

    q_(X_h* X_h)(v) = ofReal(h^(-1) ||v||²).

A cota vale com um mesmo coeficiente para todos os vetores. Não é apenas
finitude num domínio vetorial denso. h=0 não recebe esta fórmula.

DualSemifiniteIdeal define HasFiniteDualSquare(A) pela existência de C≥0
com q_(A* A)(v)≤C||v||² para todo v. Prova fechamento por soma, multiplicação
escalar complexa e multiplicação à esquerda. A interseção desse domínio com N
é o submódulo finiteDualLeftIdeal. Para cada A∈N, A X_h pertence a esse domínio
para h>0 e A X_h v→A v. Isso entrega explicitamente a aproximação forte.

## Validação e alcance

{target_count} novos alvos de auditoria, todos limitados a propext,
Classical.choice e Quot.sound. Build incremental: {build_count} registros
válidos, {controls} controles, {audit_count} declarações distintas no Audit,
{embedded_count} arquivos embutidos. O número de registros é uma contagem
do build incremental, não uma declaração de recompilação integral do Mathlib.

[Revisão independente](<{review_path}>).

Original: `{base_sha}`.
Cópia integrada: `{working_sha}`.

O corpo Python fora do dicionário Lean é igual ao da etapa anterior por AST.
O gate legado permanece inalterado. As seis flags maiores de core/canto/
witness/H1/H2/H3 continuam false. Estas novas declarações não as promovem.

[OPEN] Ainda falta demonstrar, no contrato adotado, que as formas uniformemente
finitas correspondem a operadores limitados de F; identificar F com a álgebra
de base; completar a correspondência espectral/predual e o peso operatorial
padrão; construir estado modular, gerador e perturbação que fornecem o traço
canônico fiel, normal e semifinito da mesma realização. Seguem as Three Locks,
H1–H3 físicos, interações/BRST/QME/anomalias/UV, o contrato ampliado consumido
pelo gate e o runtime integral isolado.

Não foi executado ou importado o monólito original nem realizado o runtime
integral da cópia. O inventário estático de I/O é histórico, preservado com o
hash da cópia que examinou; não libera a execução atual. Objetivo geral ativo.
