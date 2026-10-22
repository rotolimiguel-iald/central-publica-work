# Forma positiva fechada do integral dual

2026-09-11T23:24:34-03:00. [REAL — construção e compilação Lean na cópia; revisão independente com escopo próprio.]

**A avaliação do integral dual agora tem as leis de uma forma positiva estendida,
semicontinuidade inferior, domínio finito construído e invariância unitária pelo
comutante da mesma álgebra. O traço canônico continua aberto.**

Para A≥0 na representação regular, q_A(v) é o integral em ENNReal dos cortes da ação
dual, com a constante (2π)⁻¹ já adotada. Foram provadas:

    q_A(c v) = |c|² q_A(v),
    q_A(v+w) + q_A(v−w) = 2q_A(v) + 2q_A(w),
    q_(r A)(v) = r q_A(v),  r≥0.

As igualdades valem com infinito, inclusive c=0. A prova não subtrai infinitos.
A semicontinuidade é obtida da igualdade, já compilada, com o supremo das avaliações
contínuas dos cortes. `ClosedPositiveForm` reúne homogeneidade vetorial,
paralelogramo, semicontinuidade inferior e q(0)=0. A homogeneidade em A é um teorema
separado sobre a família `dualQuadraticIntegral`, não um campo dessa estrutura.
Nela não foi incluída como campo uma representação espectral ainda não construída.

`finiteDomain` é o submódulo complexo construído a partir de {v | q(v)<∞}.
Os subníveis {v | q(v)≤c} são fechados. Isso não diz que o domínio finito inteiro é
fechado ou denso. Os controles formais distinguem os extremos:

    D(q_I) = {0},    D(q_0) = H.

Para A na mesma `regularCoreAlgebra P`, todo unitário U que comuta com essa álgebra
preserva q_A(Uv)=q_A(v). A prova usa que cada corte pertence à álgebra e passa pelo
supremo, sem pressupor um operador ilimitado já afiliado. O tipo
`AffiliatedPositiveForm` expressa essa invariância da forma, não entrega sozinho
uma medida espectral, um operador auto-adjunto ou o cone ampliado da álgebra de base.

[KNOWN — referência conceitual] A definição A.13, o lema A.14 e o teorema A.15 de
[Hiai](https://arxiv.org/pdf/2004.02383#page=154) ligam formas positivas estendidas
semicontínuas à representação por operador auto-adjunto no fecho do domínio finito.
**Essa equivalência de representação ainda não foi formalizada neste incremento.**

## Obrigações que permanecem

1. Construir a representação da forma no cone ampliado e identificar os pontos fixos
   da ação dual com a imagem da base. A invariância no comutante do core não substitui
   essa identificação com a base.
2. Construir o peso com valores nessa base e provar bimodularidade, fidelidade,
   normalidade e semifinitude. O ideal/domínio finito relevante para semifinitude
   é na álgebra; não se deve exigir D(q_A) denso em H para todo A positivo.
   D(q_I)={0} não contradiz, por si só, a semifinitude de um peso futuro.
3. Compor com o peso normal fiel da base, identificar o grupo modular correspondente
   e construir o operador afiliado de Λ_t, sua perturbação e o traço com a lei de escala.
4. Construir Three Locks e H1/H2/H3 nos mesmos objetos; completar o setor quântico
   interagente no alcance pretendido; ligar um contrato dependente forte ao gate.

A v350 canônica permanece com o gate que não consome as oito flags de fronteira.
Nesta etapa nem a função legada nem o corpo Python da cópia foram modificados: a
comparação AST com a etapa anterior excluiu somente o conteúdo embutido do kernel.
As novas formas não quitam core, canto, H1/H2/H3 ou testemunha total.

## Evidência e limites

27 registros Lean integrados válidos; 50 controles Python
aprovados; 5937 declarações distintas no Audit, com axiomas
no trio propext, Classical.choice e Quot.sound. 729 arquivos
embutidos. A compilação e os controles são incrementais; o monólito inteiro não foi executado.

Original SHA-256 `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`.
Cópia SHA-256 `80d168b66d543803444f970aaebbc18030ceeeaaaaff6ec13b1ca42549f4c0c0`.

| Fonte integrada | SHA-256 lido |
|---|---|
| DualQuadraticLaws | `7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3` |
| DualClosedForm | `69a47c01fc1a366a61b871b86e1d7114e43e865b025a04cd57918f09ed7c5be7` |

[Parecer independente](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_CLOSED_FORM.md>): ler ali quais fontes foram recompiladas
pelo revisor e quais evidências de integração foram apenas conferidas por leitura e hash.
O P2 documental apontado na minuta foi corrigido antes desta gravação: o texto agora
separa os campos de `ClosedPositiveForm` da homogeneidade em A. A minuta original
permanece no snapshot do revisor; nenhuma prova Lean precisou mudar para essa correção.
Os logs das tentativas com erros de elaboração foram preservados; só execuções com
rc=0 e fontes/binários correspondentes entram na evidência aceita.

O original continua intacto. Não houve transposição canônica, publicação ou novo selo.
O objetivo integral permanece ativo: este incremento reduz uma obrigação, não fecha
o plano nem estabelece confirmação física.


## TETELESTAI_V350_DUAL_FORM_TRANSPORT_20260911 — 2026-09-11T23:44:09-03:00

[REAL — Lean em cópia] `DualFormTransport` e `DualFormFaithfulness`:
q_(b*Ab)(v)=q_A(bv), com b da base; conjugado positivo permanece no mesmo core;
q_(θ_rA)(v)=q_A(D_-rv), q_A(D_rv)=q_A(v) e domínio finito preservado.
Para A≥0, (∀v q_A(v)=0)↔A=0, e A≤B implica q_A(v)≤q_B(v).
Fidelidade aqui é da família de avaliações; não é fidelidade de um traço pronto.

29 registros Lean, 52 controles,
5952 declarações distintas no Audit, axiomas no trio.
Base `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; cópia `50208cb93e4b26cc9d78b797ae8e40970e9a039e804e2b701000460e2349da3d`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/RELATORIO_TRANSPORTE_E_FIDELIDADE_DUAL.md>).
[Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_FORM_TRANSPORT.md>).

[OPEN] Cone ampliado da base/pontos fixos; normalidade e domínio semifinito do peso;
identificação modular do peso da base, gerador afiliado/perturbação/traço;
Three Locks, H1/H2/H3, interações/BRST/QME/anomalias/UV, contrato ampliado e runtime
integral. Nenhuma flag de core/canto/H1/H2/H3/testemunha total foi quitada nesta etapa.
Objetivo integral ativo; nenhum novo selo, transposição ou confirmação física.
