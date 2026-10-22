# Revisão independente — MetricEinsteinVariation

[REAL — leitura semântica e conferência de evidência] 09/09/2026. Auditor: /root/review_remaining_hypotheses. Fonte da raiz lida integralmente; nenhuma edição ou recompilação feita nesta revisão.

Parecer favorável aos três teoremas no alcance declarado. A contração scalarMetricVariation (linha 12) coincide com a definição canônica coordinateScalarCurvature: soma de gInv_ij Ric_ij, e não trace(gInv*Ric) sem discutir transposição. A regra do produto contém tanto a variação da inversa multiplicada pelo Ricci quanto a inversa multiplicada pela variação do Ricci.

metric_scalar_first_variation (linha 26) deriva a função escalar efetiva da família de Levi-Civita. metric_einstein_first_variation_component (linha 43) inclui os dois termos da variação −(S/2)g: −(δS/2)g e −(S/2)h. metric_einstein_first_variation (linha 61) reúne corretamente as componentes pela equivalência HasDerivAt para funções em produto.

As hipóteses U aberto, g/h suaves e g inversível são explícitas. O teorema é algébrico para os campos matriciais admitidos; a leitura como métricas geométricas deve conservar a especialização simétrica e os certificados próprios de assinatura. Não há hipótese que já forneça a variação escalar/Einstein como conclusão. O ajuste convert! resolve instâncias equivalentes do espaço vetorial na elaboração; não acrescenta axioma.

Fonte medida: 3712 bytes, SHA-256 `2f4c4282725178d37946c39b006ae011c8d1db2cf37b007d51ac84768ecdff7f`. Ela coincide com a fonte copiada e com o recibo PASS BUILD_20260909_144806_517069: 3 teoremas, 2 definições, cinco auditorias, dois processos com exit 0, somente propext/Classical.choice/Quot.sound, sem avisos.

Limite: esta fonte demonstra a primeira variação real para h geral. A naturalidade de Lie do escalar/Einstein pertence a uma folha posterior; transformação por difeomorfismo finito, dinâmica quântica e controle UV não são conclusões desta revisão.

Fonte: [MetricEinsteinVariation.lean](<C:/IALD/Central de Patentes/Chatgpt/EINSTEIN_VARIACAO_METRICA_20260909_143814_961452/MetricEinsteinVariation.lean>).
