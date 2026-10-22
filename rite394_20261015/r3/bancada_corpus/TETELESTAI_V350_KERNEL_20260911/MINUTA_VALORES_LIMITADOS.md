# Valores limitados do peso dual na álgebra fixa

{date}. [REAL — Lean, cópia isolada da v350]

Toda forma dual positiva com cota uniforme q_A(v)≤C||v||² é representada
por um único operador positivo limitado B da álgebra fixa F do mesmo core
regular N. O resultado é q_A(v)=ofReal(re⟨v,Bv⟩), com B≤C·I.
A cota uniforme era conhecida; a representação em F foi construída nesta etapa.

## Construção

BoundedDualValues começa pela ordem e unicidade de operadores autoadjuntos
determinadas por todas as avaliações quadráticas. A cota de q_A limita cada
corte positivo C_n por C·I. O teorema monotônico de operadores produz o limite
forte B; o fechamento da mesma álgebra dá B∈N. A igualdade entre q_A e o
supremo dos cortes identifica a forma de B. A invariância dual da forma,
junto com a unicidade, prova θ_s(B)=B e portanto B∈F. As únicas conversões
para reais nesta prova são de valores ofReal já finitos e não negativos.

BoundedFiniteSquares aplica essa representação ao ideal anterior. Para todo
A em seu domínio, q_(A* A) tem valor limitado positivo em F. Para as médias
X_h=h^(-1)∫_0^h Λ_t dt, h>0, esse valor é exatamente h^(-1)·I, com a
normalização Fourier/Haar já demonstrada. Para qualquer A∈N, A X_h→A
fortemente e os quadrados dos aproximantes têm valores limitados em F.

## Verificação e alcance

{target_count} novos alvos, axiomas apenas propext, Classical.choice e Quot.sound.
{build_count} registros Lean integrados válidos; {controls} controles;
{audit_count} declarações distintas no Audit; {embedded_count} arquivos embutidos.
Essa contagem descreve o build incremental e não recompilação integral de Mathlib.
[Revisão independente](<{review_path}>).

Original preservado: `{base_sha}`.
Cópia integrada: `{working_sha}`.
Corpo Python fora do dicionário Lean inalterado por AST em relação à etapa
anterior; gate legado e seis flags maiores de core/canto/witness/H1/H2/H3 inalterados.

[OPEN] Identificação F=base; correspondência geral espectral/predual;
interface padrão de peso operatorial e estado modular/gerador/perturbação
que produzem o traço canônico fiel, normal e semifinito. Three Locks/H1,
H2/H3 físicos na mesma realização, interações/BRST/QME/anomalias/UV,
contrato ampliado consumido pelo gate e runtime integral permanecem abertos.
O critério de densidade agora inclui valores limitados efetivos em F; isso
não identifica por si só a álgebra de base nem constrói o traço escalar.

O monólito original não foi importado ou executado. O runtime integral da
cópia continua pendente. O inventário estático de I/O é histórico, com seu
hash de origem preservado; não libera a execução da cópia atual.
Objetivo geral ativo; nenhuma confirmação física é reivindicada.
