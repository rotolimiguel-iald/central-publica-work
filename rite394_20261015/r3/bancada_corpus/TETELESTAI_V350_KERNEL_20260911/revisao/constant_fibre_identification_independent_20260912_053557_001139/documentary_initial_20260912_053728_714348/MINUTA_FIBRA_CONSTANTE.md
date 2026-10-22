# Ação constante na fibra da álgebra fixa

{date}. [REAL — Lean, cópia isolada da v350]

Todo operador B da álgebra fixa F é a amplificação de um único operador
C sobre o Hilbert da torre: B=fibre(C), em todo L²(ℝ,H). O candidato é
construído explicitamente por C=e*Be, com e(v)=1_(0,1]v.
Não se exige separabilidade de H. A pertença de C à álgebra original M
ainda está aberta; este resultado não conclui F=base.

## Construção

UnitIntervalProjection constrói a isometria e, sua leitura e*f=∫_(0,1]f
e a projeção ortogonal Q=e e*. TranslationCorrelation prova integrabilidade
da correlação e sua integral por Fubini para funções L1. Com duas funções
recortadas no intervalo unitário, a correlação se anula fora de [-2,2].
UnitIntervalShiftProjection identifica Q=P_I (∫_[-2,2] S_t dt) P_I.
As integrais de operadores são construídas fortemente em vetores, sem
hipótese de continuidade em norma de B(H).

A comutação de B∈F com translações e recortes implica QB=BQ.
ConstantFibreCandidate extrai C=e*Be e prova Be=eC e e*B=Ce*.
L2CutIntegral aplica a unicidade por todos os integrais de conjuntos
finitos: um operador A local com e*A=0 satisfaz P_I A=0.
ZeroFromTranslatedCuts propaga essa nulidade pela cobertura contável de
translações inteiras de I e conclui A=0. ConstantFibreIdentification aplica
a cadeia a A=B−fibre(C). A unicidade de C usa a injetividade da amplificação.

A prova não reúne conjuntos excepcionais ae para uma família não enumerável
de vetores, nem presume avaliação pontual contínua em L². O uso de inteiros
é na cobertura da reta; os grupos de translação e caracteres continuam reais
contínuos. Não se substitui o core contínuo por uma versão discreta.

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

[OPEN] Falta C∈M para concluir F=base. Também permanecem a correspondência
geral espectral/predual, a interface padrão de peso operatorial, estado
modular/gerador/perturbação e o traço canônico fiel, normal e semifinito.
Three Locks/H1, H2/H3 físicos na mesma realização, interações/BRST/QME,
anomalias/UV, contrato ampliado consumido pelo gate e runtime integral
continuam abertos. Nenhuma dessas obrigações foi acesa por nomes de provas.

O original não foi importado ou executado. O inventário I/O continua
histórico e não libera o runtime da cópia atual. Objetivo geral ativo.
