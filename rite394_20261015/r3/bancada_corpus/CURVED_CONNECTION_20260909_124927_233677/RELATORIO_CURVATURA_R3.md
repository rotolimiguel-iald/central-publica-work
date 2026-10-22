# Variação não linear da curvatura canônica — entrega R3

[REAL — compilado aqui] A curvatura coordinateCurvature do kernel agora possui, nesta bancada, expansão exata ao longo de conexões suaves arbitrárias Γ(t)=Γ+tC, em carta de quatro coordenadas:
R(Γ+tC)=R(Γ)+t·L_Γ(C)+t²[C_i,C_j].

L_Γ(C)=dC+[Γ,C] é identificado com a diferença das mixedCovariantDerivative canônicas. A primeira variação é uma derivada REAL HasDerivAt, obtida da função de curvatura original, e a contração que define coordinateRicci recebe sua expansão e sua derivada. O termo t² foi preservado e possui controle explícito não nulo.

Para C_i=∂_iB+Γ_iB−BΓ_i, a prova mostra L_Γ(C)_ij=R_ij B−B R_ij. As derivadas segundas de B se cancelam por tensorFieldJet_commute, que deriva Schwarz da suavidade local. Não foi recebida uma hipótese independente de comutação das derivadas.

## Referências da fonte

CurvatureNonlinearVariation.lean:

- 54: curvature_exact_expansion — expansão exata, qualquer t real.
- 68: curvature_exact_remainder — resto exatamente quadrático.
- 78 e 96: curvature_parameter_derivative e curvature_first_variation — derivada real em qualquer t e em zero.
- 104 e 114: ricci_exact_expansion e ricci_first_variation — contração de Ricci canônica.
- 123 e 133: regularidade e primeira derivada da direção de gauge.
- 156 e 169: curvature_gauge_variation e curvature_gauge_derivative — δR=[R,B] com derivada real.
- 179: curvature_gauge_trace_zero — traço INTERNO de R_ij.
- 188: flat_curvature_gauge_variation_zero — o comutador zera se a curvatura correspondente for zero.
- 206: nonzero_quadratic_control — uma componente do termo quadrático vale 1.
- 213: nonzero_curved_gauge_control — exemplo suave constante com uma componente da variação igual a −1.
- 229: curvature_variation_covariant_exterior — ligação direta à derivada covariante existente.
- 238: ricci_gauge_variation — Ricci contrai um índice de base e um índice vetorial; não é o traço interno acima.

## Evidência e preservação

19 teoremas + 6 definições = 25 termos auditados.
BUILD_20260909_130130_487133/BUILD_RESULT.json: PASS_COMPILED_SCOPE.
CurvatureNonlinearVariation e ImportsRealization: exit 0; nenhum warning; axiomas de todos os termos contidos no trio propext, Classical.choice, Quot.sound.
A fonte e o agregador foram compilados de novo em diretório isolado; dependências canônicas preexistentes foram lidas. Fontes e binários diretamente importados, manifesto e ferramenta foram conferidos antes/depois pelo builder. Não se reivindica recompilação de todas as dependências transitivas.

Imports: TGLExt.VectorCurvatureCommutator e TGLExt.MetricCurvatureSymmetries.
Namespace: ChatgptAudit.CurvedConnection.
Nenhum import local necessita transposição. Cada declaração possui seu #print axioms.
O builder foi copiado em bytes da bancada GENERAL_LINEARIZED_20260909_115828_623341.

Todas as revisões da fonte tiveram backup imediato em bytes, na mesma pasta, antes da substituição atômica. Os builds intermediários foram preservados com seus erros ou warnings visíveis. Nenhum um.py foi executado/importado; nenhum original, Atlas ou índice canônico foi alterado.

## Alcance aprovado por revisão independente

[INPUT — parecer recebido do orquestrador /root nesta sessão] A revisão semântica independente leu a fonte integral e aprovou a expansão e os sinais no alcance declarado. Explicitou:

1. Γ+tC com C arbitrário não preserva automaticamente a classe Levi-Civita, compatibilidade métrica ou torção zero.
2. A direção infinitesimal dB+[Γ,B] não faz Γ+tD_ΓB tornar-se automaticamente a órbita FINITA de gauge além da primeira ordem.
3. O traço nulo é interno, distinto da contração de Ricci.
4. O resultado não deve ser ampliado para Ward métrica sob difeomorfismos, nem ausência de anomalias quânticas.

A última alteração posterior à leitura removeu apenas uma tática redundante; os enunciados permaneceram iguais e a versão final recompilou limpa.

## Próximo elo explícito

[OPEN nesta bancada] Derivar a variação da conexão de Levi-Civita em função de h e da métrica inversa, identificá-la com C na fórmula acima e compor a naturalidade sob difeomorfismos. Esse elo ainda não foi provado aqui. Em particular, não se identificou por nome o novo ricciVariation de conexões com o linRicci de perturbações métricas no fundo de Minkowski.

O objetivo métrico correto em fundo curvo envolve a derivada de Lie do tensor de fundo; não é declarar invariância zero do Ricci para qualquer fundo. A passagem ao fundo solução deve usar a equação tensorial pertinente e seus campos conjuntamente.

[ESCOPO] Avanço clássico, em conexões e curvatura, com termo quadrático. Não quantiza campos, não constrói amplitudes interagentes, não fecha anomalias quânticas nem fornece controle UV. A delimitação UV separada está em OBJETO_UV_E_ROTAS.md.
