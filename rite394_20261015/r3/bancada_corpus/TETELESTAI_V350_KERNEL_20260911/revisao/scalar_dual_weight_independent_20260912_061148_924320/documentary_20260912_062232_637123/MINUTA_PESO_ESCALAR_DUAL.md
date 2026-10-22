# Peso escalar dual fiel e normal

{date}. [REAL — Lean, cópia isolada da v350]

O peso ν(A)=q_A(η), com η=1_(0,1]Ω, foi construído no cone positivo da
mesma álgebra regular N. É aditivo, homogêneo para escalares não negativos,
monótono, fiel e normal para supremos dirigidos internos. O ideal complexo
esquerdo já construído é fortemente denso e todos os seus quadrados têm ν
finito. Estas são as propriedades expressas pelos teoremas deste pacote.
ν ainda não foi identificado como traço nem teve seu grupo modular provado.

## Construção e ligação à base

FixedBaseEquivalence empacota a amplificação M→F como equivalência de
álgebras com involução e isomorfismo de ordem; a inversa é e*Be.
BoundedBaseDualValues coloca os valores positivos limitados efetivamente
em M, prova sua unicidade e a aproximação forte por entradas com quadrados
finitos. A composição usa F=imagem amplificada de M já provada.

ScalarDualWeightFaithfulness prova que η é separante para F usando Ω
separante para a mesma M. Se q_A(η)=0, o resolvente R minimizador dá Rη=η.
Como R∈F, segue R=I. Sua identidade de energia, depois da prova de finitude,
dá q_A(v)=0 para todo v, e a fidelidade da forma conclui A=0.
Não se usa toReal para disfarçar um valor infinito como zero.

ScalarDualWeight fornece as leis do peso escalar. A normalidade parte do
supremo interno em N, sem receber um limite forte externo como hipótese.
A densidade usa A·X_h→A fortemente, h>0, com X_h a média regular já
construída. A condição de quadrado finito fornece uma única cota para todos
os vetores e, em η de norma 1, um valor escalar finito. Não se reivindica
convergência em norma de operadores nem finitude de ν em toda N+.

Quando o valor operatorial é limitado e vale fibre(D), a leitura escalar
é exatamente ofReal⟨Ω,DΩ⟩. A ligação com o estado original é demonstrada
nesse caso. A correspondência geral espectral/predual permanece separada.

## Verificação e alcance

{target_count} alvos novos, axiomas somente propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações no Audit; {embedded_count} arquivos embutidos.
Build incremental, sem recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`. Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior; gate legado e seis flags maiores preservados.

[OPEN] Identificação do grupo modular de ν/condição KMS, gerador afiliado,
perturbação e traço canônico com escala dual. Permanecem a interface geral
de peso operatorial/predual, Three Locks/H1, H2/H3 físicos na mesma
realização, interações/BRST/QME/anomalias/UV, contrato ampliado consumido
pelo gate e runtime integral isolado. Invariância por um fluxo candidato
não basta para identificá-lo como grupo modular. As propriedades de ν
não substituem essas construções. Inventário I/O histórico; original não
importado/executado. Objetivo geral ativo.
