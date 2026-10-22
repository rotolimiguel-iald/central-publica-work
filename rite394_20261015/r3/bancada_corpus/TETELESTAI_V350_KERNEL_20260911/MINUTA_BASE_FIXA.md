# A álgebra fixa é a base amplificada

{date}. [REAL — Lean, cópia isolada da v350]

Na representação regular construída sobre a mesma torre e o mesmo fluxo,
a álgebra fixa da ação dual é exatamente a amplificação da álgebra original:
B∈F se, e somente se, existe C∈M com B=fibre(C). C é único e é dado por e*Be.
Isso resolve a pertença à base que estava aberta no relatório da fibra constante.

## Construção

StrongOperatorField constrói o operador de multiplicação de um campo de
operadores fortemente contínuo e uniformemente limitado no espaço L²(ℝ,H).
OperatorFieldFaithfulness prova que sua ação em L² determina o campo ponto
a ponto. A continuidade e a positividade da medida de abertos elevam a
igualdade quase sempre a igualdade em todo ponto. Para cada vetor fixado,
somente uma família enumerável de testes intervalares é reunida. Não há
hipótese de separabilidade de H nem avaliação pontual contínua em L².

Para D∈M', TwistedCommutantField constrói T_D(x)=Δ^(ix)DΔ^(-ix), com o mesmo
fluxo da torre. O campo permanece em M', é fortemente contínuo, uniformemente
limitado por ||D|| e satisfaz T_D(x)Δ^(it)=Δ^(it)T_D(x−t).
Seu operador de multiplicação comuta com as duas famílias geradoras de N.
RegularCoreCommutant estende a comutação à álgebra gerada, tratando os
adjuntos explicitamente, e coloca o operador de multiplicação em N'.

Se fibre(C)∈N, essa comutação reflete-se no campo e, no ponto zero, dá
DC=CD para todo D∈M'. Pelo bicomutante, C∈M. A etapa anterior já deu
B=fibre(C) para todo B∈F. A composição fornece F=base amplificada; a
recíproca usa a inclusão fixa já provada e a unicidade usa a fidelidade.

Nenhum estado, fator, parâmetro de torre ou representação é trocado para
obter a conclusão. A identificação é interna ao modelo modular construído;
ela não identifica esse modelo com uma geometria física de horizonte.

## Verificação e alcance

{target_count} alvos novos, com axiomas apenas propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações no Audit; {embedded_count} arquivos embutidos.
Build incremental, sem recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`. Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior. A identificação não acende as seis flags maiores nem muda o gate legado.

[OPEN] Correspondência geral espectral/predual, interface padrão de peso
operatorial, estado modular/gerador/perturbação e traço canônico fiel, normal
e semifinito. Permanecem Three Locks/H1, H2/H3 físicos na mesma realização,
interações/BRST/QME/anomalias/UV, contrato ampliado consumido pelo gate e
runtime integral isolado. A prova de F=base não fornece essas construções.
O inventário I/O permanece histórico e não libera o runtime atual.
Original não importado/executado. Objetivo geral ativo.
