# Localidade da álgebra fixa do core regular

{date}. [REAL — Lean, cópia isolada da v350]

Se B pertence à álgebra fixa F da ação dual no core regular N, B comuta
com as translações ordinárias e preserva todo recorte mensurável do espaço.
Não há hipótese de medida finita para o conjunto recortado nem de
continuidade pontual dos vetores L².

## Construção

FixedCoreShiftCommutation prova que as translações ordinárias comutam com
os geradores do core e portanto pertencem ao seu comutante. A condição
de ponto fixo da ação dual dá a comutação com os caracteres.

FourierUniqueness prova unicidade quase em toda parte de funções L1 a
partir de suas integrais de Fourier, usando inversão em testes de Schwartz.
CharacterLocality aplica esse resultado aos pareamentos integráveis
⟨B* f(x),g(x)⟩ e ⟨f(x),B g(x)⟩. A comutação com todos os caracteres
iguala suas transformadas e por isso os pareamentos locais quase em toda parte.

L2MeasurableCut constrói multiplicação por indicadora como operador
linear contínuo de norma no máximo um. FixedCoreLocality integra a
igualdade dos pareamentos sobre cada conjunto mensurável e conclui
P_S B = B P_S. O argumento não usa avaliação pontual contínua em L².

## Verificação e alcance

{target_count} novos alvos; axiomas apenas propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações distintas no Audit; {embedded_count} arquivos embutidos.
Build incremental, sem recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`.
Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior; gate legado e seis flags maiores de core/canto/witness/H1/H2/H3 inalterados.

[OPEN] Ainda é necessário provar que a ação local é uma mesma ação na fibra
em todos os pontos, e que essa ação pertence à álgebra original. A inclusão
F⊆base não foi concluída. Não se usou Stone–von Neumann nem um teorema de
decomposição espectral como hipótese disfarçada.

Permanecem a correspondência geral espectral/predual, a interface padrão
de peso operatorial e estado modular/gerador/perturbação para o traço
canônico fiel, normal e semifinito. Three Locks/H1, H2/H3 físicos na mesma
realização, interações/BRST/QME/anomalias/UV, contrato ampliado consumido
pelo gate e runtime integral permanecem abertos.

O original não foi importado ou executado. O inventário estático de I/O
continua histórico e não libera a execução da cópia atual. Objetivo geral ativo.
