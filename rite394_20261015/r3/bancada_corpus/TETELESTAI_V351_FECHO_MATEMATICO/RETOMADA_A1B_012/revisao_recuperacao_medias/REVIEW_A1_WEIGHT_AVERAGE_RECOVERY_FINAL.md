# Revisão independente — recuperação do peso pelas médias

2026-09-14T22:03:43.054862-03:00

**A1_WEIGHT_AVERAGE_RECOVERY_REVIEW_ACCEPTED__CUTOFF_COMMUTATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2: **1 teorema público, 0 definições/helpers privados**. Fonte inteiro relido, módulo e auditor próprios rc0; #check completo com universos e #print axioms: somente propext, Classical.choice e Quot.sound.

[REAL — tipo e domínio] scalarWeight_square_eq_iSup_averages recebe somente P e A no core N. Não recebe HasFiniteScalarSquare, MemLp, finitude da integral, monotonicidade das amostras ou hipótese sobre seus minorantes. O resultado é uma igualdade em ENNReal para o mesmo dualQuadraticIntegral, regularVacuum, dualAmbient e regularAverage P (1/(n+1)), incluindo ν(A*A)=∞.

[REAL — limite e Haar] A sequência d_n=1/(n+1) converge a zero na vizinhança perfurada, com d_n≠0 provado. A convergência pontual da órbita existente passa a norma-quadrado e ofReal. O fator fixo ofReal dualHaarFactor permanece dentro de f_n e g; continuous_const_mul usa explicitamente ofReal_ne_top. Isso exige finitude da CONSTANTE, não finitude da integral. dualQuadraticIntegrand_star_mul liga exatamente as avaliações quadráticas às normas. Measurabilidade e lintegral_const_mul recuperam a normalização original.

[REAL — duas desigualdades] Fatou para a sequência atTop dá integral(g)≤liminf integral(f_n); a cota por iSup de todos os termos fecha esse sentido. No sentido oposto, iSup_le aplica scalarWeight_right_average_le a cada d_n, cujo fornecedor vale para todo A∈N. Não há DCT com integrabilidade escondida, rede arbitrária exigida por Fatou, ordenação das amostras, ou comparação (Ae_n)*(Ae_n)≤A*A em ordem de operadores.

[REAL — ficha, história e negativo] A ficha anterior ao código foi relida, com nove fornecedores pinados; a consulta é identificada como roteiro, não prova. Os dois DEV rc1 efetivamente encontrados são 215633_172434 e 215716_269572, ambos excluídos. O DEV 215753_855426 rc0 tem um aviso de change inútil; a remoção exata de uma linha (40 bytes) foi medida entre seu snapshot histórico e a fonte final reproduzida. Pins antigos apontam aos snapshots reais, nunca ao caminho vivo com hash antigo. A auditoria autoral final rc0 foi conferida; substituir o supremo por um único corte produz Type mismatch com imports resolvidos. Esse negativo não foi reexecutado e não demonstra que igualdade num corte seja impossível em casos especiais.

[REAL — proveniência] 672 objetos anteriores do Lake próprio preservados; acrescentados apenas módulo e auditor (total 674). Nenhum fornecedor antigo recompilado, nenhum objeto autoral/DEV herdado. Pacotes externos: cache pinado da reprodução anterior, sem nova auditoria integral. Run próprio rc0 em 34.624 s; zero avisos do alvo/auditor. 178 mensagens históricas de fornecedores constam no JSON. LEAN_PATH dos traces contém apenas V e seus pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte final | `a72b71ac86bb0b2a5c81d5bfaba3c6ad964bf4a8beffd0a9df89f7ee26391fac` |
| .olean próprio | `306d98e971c8d9a20ff11deb84ad33978a89bf32de07d985ea47a956678d38ec` |
| .olean cold autoral (comparação somente) | `306d98e971c8d9a20ff11deb84ad33978a89bf32de07d985ea47a956678d38ec` |
| Snapshot DEV anterior ao ajuste do linter | `a13db1e1d1cfcc902d660156b6aa47ff405805e63b06d5ceff159ad6741c58d8` |

Igualdade binária do alvo final medida: True.

[OPEN — limites] Há recuperação dos valores quadráticos para todo A∈N, inclusive ∞. A finitude dos quadrados regularizados é fornecedor anterior, não premissa desta prova nem novo alvo. Comutação dos cortes com as mesmas médias e a extensão correspondente da ordem dos pesos dos cortes ainda são obrigações posteriores. Tracialidade/A1(b) permanecem abertos; não se usa a propriedade falsa de minorantes positivos finitos de ν. Sem novas consultas, testes extra, monólito, recorder, escrita autoral ou alteração de memória/gate.

Artefatos próprios:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\compilation.json>) — SHA256 `40d39606c66fedf7130413a4f56bd5b1b918bc237fd0753e4273c45173bca783`.
- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\independent_20260914_220028_858888\run.json>) — SHA256 `74f0ef759cfabc4051d145f145f6c2521ce246bd5f7216a5877f074ed34d8bad`.
- [tipos e axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\independent_20260914_220028_858888\type_axiom_audit.json>) — SHA256 `7111aa61f06873fe52b06f3b31dc899d0e772c4d71c45be72eae8d2c5ac46c23`.
- [histórico/diff](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_recuperacao_medias\history_read.json>) — SHA256 `9a20a699bca7fe6a8b44941830ff40315b088f05698df1619fd4ac7abcfa0a17`.
