# Próxima etapa: gráfico dos pares e bloco limitado

[OPEN — roteiro; não é uma nova prova Lean ou quitação do gate]

O pacote dos resolventes/quadrados fornece o critério do S original.
A aplicação exige uma construção diferente do gráfico antigo:

- Antigo: scalarRightMultiplicationGraph, ideal esquerdo do peso, Λ, η∈Fix F.
- Necessário: Gη=fecho{(j(a),a.val η):a∈E}, E=scalarPairedRightAlgebra P,
  j=scalarRightPairVector P e η∈Fix S, escolhida pela equação variacional.

[DERIVED — rota de prova a implementar] A simetria sobre E deve usar
j(a*b)=a.val j(b), F j(a)=j(a*) e o pareamento bidual com Sη=η.
A invariância do gráfico por E e E* dá comutação de sua projeção com
as ações diagonais de E. As entradas A,B,D dessa projeção devem então
ser reconhecidas no comutante de E, que precisa ser identificado com
a MESMA imagem GNS de M por seus lemas já compilados.
Não se pode substituir esse argumento por uma identificação nominal
com o gráfico antigo. A,B,D são blocos limitados; A não é Delta.

[OPEN] Obrigações do bloco antes da inversão:

1. P²=P=P*, A=A*, 0≤A≤I, BB*=A(I−A), BD=(I−A)B.
2. A injetivo: densidade de j(E) e energia da projeção no primeiro eixo.
3. Ações B j(a)=A aη, B aη=(I−A)j(a), B* aη=D j(a), com as
   identificações e sinais conferidos. Não pressupor [A,B]=0.
4. Para e=e(A), formar ζ=eBB*η e ζflat=B*eBη, mantendo a ordem.
   K=e(I−A)B e K*=B*e(I−A) devem realizar as DUAS ações sobre j(a)
   exigidas por scalarClosedTomita_of_boundedPairAction.
5. Só depois usar a equação variacional no par que efetivamente pertence
   ao gráfico do S original, obtendo a estimativa ponderada da consulta RVD.
6. Com c=1+||a0.val||², provar A≥c⁻¹I; esta cota uniforme, e não apenas
   injetividade, permitirá a inversa limitada. A aplicação completa ainda
   precisa ser formalizada. A inclusão inversa por J requer passos posteriores.

[REAL — bibliotecas consultadas em disco, sem compilação nova nesta consulta]

- ContinuousLinearMap.nonneg_iff_isPositive e isPositive_iff': declarar a
  auto-adjunticidade/simetria e demonstrar a positividade dos pareamentos.
- Submodule.norm_starProjection_apply_le e as identidades de energia de
  HilbertProjectionBlocks podem ser reutilizadas para o bloco no novo gráfico.
- CFC.posPart_sub_negPart, posPart_mul_negPart, posPart_nonneg,
  le_posPart e posPart_eq_zero_iff orientam o passo e=(I−cA)⁺.
  Conferir as hipóteses IsSelfAdjoint explicitamente: a definição total de
  parte positiva pode retornar zero fora dessa classe; esse zero não é prova
  da estimativa. O caminho real é Analysis/SpecialFunctions/..., encontrado
  após uma tentativa de localização em CStarAlgebra/... ter falhado.

[REAL — diagnóstico de elaboração reutilizável] No pacote atual, pontes
abstratas sobre E:NonUnitalStarSubalgebra ℂ (H→L[ℂ]H), com hipóteses concretas
descarregadas em metas separadas por refine, permitiram compilar a 200000.
Remover classes isoladamente ou aumentar orçamento sozinho não resolveu as
falhas registradas. Isso é evidência de variantes testadas, não demonstração
da causa interna única de isDefEq/whnf. Conservar a prova geral e instanciar
no GNS apenas ao final é uma rota de implementação já testada.

Leituras de referência: revisao/CONSULTA_RVD56_BLOCO_INVERSIVEL_CFC.md,
revisao/CONSULTA_INVERSA_J_APOS_GRAPH_CORE_F.md e o pacote DEV20 discriminado
em square_resolvent_draft_status.json. Nenhum enunciado deste guia foi
acrescentado ao Audit, às flags ou ao runtime.

Data: 2026-09-13T05:59:27.031014-03:00.

- `Analysis/InnerProductSpace/Positive.lean` — SHA256 `eb187f321fed60ab42530e50cd061eccc100e07e4292c4031e16f9beac30e4b6`.
- `Analysis/InnerProductSpace/Projection/Basic.lean` — SHA256 `833c7b4ef410230086bd5b879ee51234e0e359e2aca3c9233d75cec5162fa5b2`.
- `Analysis/SpecialFunctions/ContinuousFunctionalCalculus/PosPart/Basic.lean` — SHA256 `dc4440de5a6521adcc2604a61502ecf29995c61bd742cd3f291af9ee3cb09361`.
