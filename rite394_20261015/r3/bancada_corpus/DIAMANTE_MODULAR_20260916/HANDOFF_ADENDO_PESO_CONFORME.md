# Adendo ao handoff — um peso conforme escalar não basta

16/09/2026. Complementa o [handoff anterior](HANDOFF_TESTE_WEYL_E_PONTE_FISICA.md), preservando a ponte dephasing–torre já recebida. Não solicita outra função de pinching, outro cociclo ou mudança automática de gate.

**[DERIVED — demonstração escrita, não Lean]** No estado linear Einstein–sigma 067, a ação candidata sobre o Weyl inteiro

\[
D_\xi C=\mathcal L_\xi C+w\psi_g(\xi)C
\]

não pode coincidir com o fluxo modular para nenhum peso escalar constante real w, nos diamantes interiores considerados, com raio angular L≠π/2. Isso amplia o no-go anterior, que tratava apenas w=0.

## A ligação nova

O resultado anterior dizia corretamente que a leitura magnética reescalada a b_n fica estacionária. **Essa leitura isolada não inclui a componente elétrica do Weyl.**

Pela invariância modular necessária, continuação analítica e centros antipodais, a variância de qualquer componente sob a ação candidata teria de satisfazer V'=2w tanhη V. A leitura magnética obriga w=1. Já o cálculo direto da componente elétrica dá

\[
\operatorname{Var}(aE_n)
=\hbar c_n^2[p_n^2(\lambda_n+6)^2+16\tanh^2\eta],
\]

cuja derivada é estritamente positiva para η>0. O mesmo peso não preserva as duas leituras do mesmo tensor. A [demonstração completa](WEYL_ELETRICO_E_PESO_CONFORME.md) explicita os fatores métricos na variação de Weyl e as restrições de suporte.

Não há contradição com a nota anterior: seu controle reescalado continua correto, mas agora foi testado em outra componente que também precisa ser conservada. A razão Var(E_n)/Var(b_n) varia com η e não pode ser corrigida por uma reescala temporal escalar comum.

## O que o motor deve registrar

Reutilizar o registro do fornecedor geométrico existente. Se sua ação se restringir à família acima, ela falha nesse estado e nessa classe de diamantes. Não usar apenas a estacionariedade do magnético como aprovação. Se o fornecedor gera mistura entre campos, transformações diferentes entre componentes ou termos adicionais, o resultado desta nota não decide esse caso: apontar a ação concreta e testá-la no mesmo estado.

O coeficiente 16 em uma variância deste modo não é o primeiro coeficiente não central R1. Ele vem dos modos e do fundo fixados, não é universal para campos/diamantes e não é um sinal experimental. O estado interagente UV completo, o espectro regional e a ação física renormalizada de Kξ permanecem questões próprias.

## Verificação e custódia

[REAL — controles] `verify_electric_weyl.py` conferiu nove pares modo/tempo; em três deles, uma linearização por diferenças centrais da curvatura não linear de uma métrica Bianchi IX diagonal reproduziu o Weyl elétrico homogêneo TT de n=2, com convergência quadrática. Resultado em [ELECTRIC_WEYL_CHECKS.json](ELECTRIC_WEYL_CHECKS.json). A prova não depende desses números para sua generalidade.

O parecer matemático independente e o manifesto desta etapa acompanham a entrega. A prova escrita não recebeu formalização Lean. Toda gravação desta bancada fica em Chatgpt, com backups imediatos de bytes das memórias. Encaminhar a atualização ao Atlas/índice/diário/desenho canônicos pela gerência; não promover o adendo a prova da completude UV ou alterar o gate por esse diagnóstico.
