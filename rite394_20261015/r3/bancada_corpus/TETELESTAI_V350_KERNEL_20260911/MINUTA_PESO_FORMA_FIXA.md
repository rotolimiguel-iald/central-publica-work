# Peso normal e fiel com valores em formas afiliadas à álgebra fixa

{date}. [REAL — Lean incremental na cópia, revisão independente delimitada.]

O mapa `dualFixedWeight` recebe um operador positivo da mesma álgebra regular N
e devolve a forma q_A no cone `AffiliatedPositiveForm F`, com F=dualFixedCore P.
Seu valor em cada vetor é literalmente a integral dual já construída. Não se
escolhe uma forma diferente por equivalência abstrata.

`PositiveFormCone` fornece zero, soma, escala NNReal e pré-composição de formas
fechadas; as operações preservam afiliação quando cabível. A ordem é pontual
nos valores ENNReal, e são provadas antissimetria, leis aditivas, distributivas
e monotonicidade de soma/escala. A escala inclui zero, sem converter infinito
em número real. Não se reivindica uma estrutura de espaço vetorial: formas
positivas estendidas não admitem subtração arbitrária.

`DualFixedWeightLaws` prova igualdades no próprio cone de saída:

- T(0)=0; T(A+B)=T(A)+T(B); T(rA)=rT(A), para r não negativo finito;
- T(B* A B)=B* T(A) B para todo B∈F, representado pela pré-composição q_A(Bv);
- monotonicidade e T(A)=0 se e somente se A=0;
- preservação do supremo interno de toda rede positiva crescente dirigida,
  não vazia, que possua supremo em N. O resultado é um IsLUB no cone de saída;
  a positividade do supremo de entrada é derivada. Não se exige convergência
  forte adicional nem se reduz a redes sequenciais.

A identidade bimodular usa θ_s(B)=B para todos os elementos da álgebra fixa,
incluindo os que ainda não foram identificados como operadores da base amplificada.
Essa extensão do domínio de B é parte do enunciado, não uma mudança de nome.

[OPEN] Este é um peso com valores no cone concreto de formas afiliadas a F.
Não foram provadas a identificação F=base, a correspondência geral com o cone
positivo ampliado pelo predual/cálculo espectral, nem a semifinitude do peso na
álgebra. Normalidade e fidelidade não bastam para a última propriedade. A
semifinitude exige produzir um ideal suficientemente denso de entradas com
peso finito; a densidade de vetores no suporte de uma forma não a substitui.

[OPEN] Seguem o estado modular da base, gerador, perturbação, traço canônico
fiel normal semifinito e escala dual; Three Locks/H1; H2 e H3 na mesma realização;
estado quântico interagente/BRST/QME/anomalias/UV; contrato dependente ampliado
consumido pelo gate e execução integral isolada do monólito.

## O que pode mover o gate da v350

[REAL — leitura da fonte] `evaluate_quantum_gravity_closure` consome seis flags
formais qgc, cinco físicas qgp e quatro entradas experimentais; as qgf/gpf de
fronteira não são entradas dessa função. Por isso, provar essas obrigações não
muda automaticamente a string do gate. O avanço deve habitar um contrato mais
forte, que identifique os objetos entre certificados, e ser consumido por uma
etapa correspondente da decisão. O contrato legado ContinuousCoreData aceita
traço zero; seu contraexemplo compilado não passa pelos Three Locks. Preencher
apenas o tipo legado não entrega o traço canônico pretendido.

A H2 experimental da v350 com pycbc é distinta da H2 geométrica do kernel.
O texto da versão diz que a primeira não move o gate. O teorema que alimenta
`relevant_anomalies_absent` prova o Ward clássico-linear; não é um controle de
anomalias quânticas interagentes. O teorema mestre H1∧H2∧H3 já existe: falta
produzir antecedentes compatíveis na realização física do alcance ampliado.

## Evidência e custódia

{target_count} alvos novos, {build_count} registros Lean integrados válidos,
{controls} controles aprovados, {audit_count} declarações distintas no Audit,
{embedded_count} arquivos embutidos. Axiomas dos alvos limitados a propext,
Classical.choice e Quot.sound. Dependências reutilizadas e conferidas;
compilação incremental, sem reconstrução integral da biblioteca.

Base `{base_sha}`; cópia `{working_sha}`.
As seis flags maiores continuam falsas. Corpo Python fora dos arquivos Lean
embutidos idêntico por AST ao estrato anterior, gate legado inalterado.

[Revisão independente](<{review_path}>).
O parecer distingue processos próprios e inspeção dos registros integrados.
O inventário estático de I/O anterior continua vinculado à cópia anterior;
não é nova execução nem prova de isolamento da cópia atual. Não houve execução
integral do monólito, transposição canônica ou confirmação física.

Tentativas que falharam por elaboração/inferência foram mantidas nos logs;
somente processos rc0 da fonte final integram a evidência aceita. As memórias
recebem adendo e backup imediato de bytes. O objetivo integral permanece ativo.
