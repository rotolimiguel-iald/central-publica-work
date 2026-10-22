# Dez limites Gibbs — entrega congelada

[REAL — Lean] SignedGibbsFiniteRecord passou: 2 teoremas, nenhuma definição adicional, 2 auditorias de axiomas; fonte e importador terminaram com exit 0, sem warnings e somente propext, Classical.choice e Quot.sound nas auditorias. Namespace: ChatgptAudit.SignedGibbsFinite.

[Fonte](<C:/IALD/Central de Patentes/Chatgpt/DEZ_LIMITES_GIBBS_20260909_210949_299699/SignedGibbsFiniteRecord.lean>): 1873 bytes; SHA-256 55d7c7877b91668b5bc44950ab86b14747453169bf4f8c0412f9de0f27beeeec.
[Recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/DEZ_LIMITES_GIBBS_20260909_210949_299699/BUILD_20260909_211130_717351/BUILD_RESULT.json>).

[REAL — enunciado] ten_entropy_limits_reconstruct_source recebe s:Fin 10→R e a hipótese de limite entrópico apenas nas dez direções probeDirections i. ten_modular_limits_reconstruct_source usa os dez limites modulares em seu lugar. Ambos concluem decodeSource g gi s=T. Não recebem uma função de resposta em todas as direções nem exigem limite nessas outras direções.

A prova identifica cada uma das dez amostras com seu coeficiente calibrado pela unicidade do limite e aplica a reconstrução finita já aprovada. Isso reduz efetivamente a hipótese universal em direções usada no último teorema de SignedGibbsCoverage.

[INPUT] k>0, g simétrica, gi*g=I e T simétrica. A preparação ainda é calibrada a partir de traceReverse(g,gi,T). A folha não remove T da entrada da calibração, não deriva uma dinâmica material e não paga a correspondência de área.

[OPEN] Dez limites exatos não equivalem a dez medições em tempos finitos com erro. A folha não formaliza estabilidade experimental nova, distribuição conjunta global dos oito probes ou quantização.

[REAL — revisão separada] [REVISAO_INDEPENDENTE_GIBBS_ASSINADO.md](<C:/IALD/Central de Patentes/Chatgpt/DEZ_LIMITES_GIBBS_20260909_210949_299699/REVISAO_INDEPENDENTE_GIBBS_ASSINADO.md>) registra a análise independente das duas fontes raiz SignedGibbsResponse e SignedGibbsCoverage, com hashes próprios medidos. O parecer é favorável aos sinais e à positividade e identifica precisamente o excesso no comentário sobre dez limites de Coverage. A folha nova paga a redução; nenhuma das duas fontes anteriores foi editada. O parecer não se apresenta como revisão independente desta nova folha, cujo autor é o mesmo.

[REAL — preservação] Construção em pasta nova Chatgpt; builder93 copiado em bytes e dependências Response/Coverage cached a partir dos recibos PASS. A única correção local abriu explicitamente o namespace de traceReverse e recebeu backup imediato em bytes, preservado. Fonte congelada após o PASS. Nenhum um.py foi executado/importado, nenhum original ou módulo anterior foi alterado. A compilação verifica a nova folha/importador e a fronteira descrita no recibo, sem declarar reconstrução integral de Mathlib ou do kernel canônico.
