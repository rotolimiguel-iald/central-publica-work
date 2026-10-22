# Revisão independente — leis do peso limite

2026-09-14T22:46:05.542271-03:00

**A1_INVERSE_LIMIT_WEIGHT_REVIEW_ACCEPTED__FAITHFUL_SEMIFINITE_TRACIAL_SCALING_OPEN**

[REAL] **Sem achados P0/P1/P2.** Treze teoremas públicos + duas definições, zero privados. Módulo completo e auditor próprios rc0; quinze #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — objetos e domínio] As duas definições usam o mesmo PositiveCoreInput P, hilbertPositiveSqrt(Bε), dualQuadraticIntegral e regularVacuum P. Wε(X)=ν(sε* X sε) e o candidato limite é sup_n W_(1/(n+1))(X). O domínio é o cone positivo limitado do core; não exige finitude do valor. A expressão é definida para todo ε real, mas a interpretação como corte inverso positivo e a ordem entre reguladores usam ε>0. Não se afirma que os cortes são fixos pela ação dual; PositiveCoreInput.conjugate, restrito ao core fixo, não é aplicado indevidamente.

[REAL — leis dos cortes] Zero, aditividade, homogeneidade por r:NNReal e monotonia em X são transportadas das leis integrais existentes. A positividade de star b X b e a ordem sob conjugador FIXO vêm das leis de estrela. Não se deduz ordem de sanduíches a partir da ordem de conjugadores. Todos os valores são ENNReal; não se elimina infinito nem se divide por um valor de peso.

[REAL — normalidade] Para qualquer universo do índice ι, com Preorder, IsDirectedOrder e Nonempty, A é uma rede crescente de positivos no core e S seu supremo INTERNO limitado. A cota ||A_i||≤||S|| é deduzida. vonNeumann_exists_positive_isLUB constrói um limite forte D no core; unicidade do supremo dá D=S. A continuidade do CLM star b produz o limite forte dos sanduíches em todos os vetores, que alimenta a normalidade integral antiga. Não se recebe continuidade forte como premissa nem se pressupõe que conjugação preserve supremos internos.

[REAL — limite comum] A antitonia em ε é o alvo já entregue do módulo21. Para n≤m, 1/(m+1)≤1/(n+1), logo as avaliações crescem. ENNReal.iSup_add_iSup_of_monotone é usado nas DUAS famílias com o mesmo índice natural; não se aplica a igualdade falsa entre soma de supremos e supremo diagonal para famílias arbitrárias. Homogeneidade usa mul_iSup (inclusive zero e infinito), monotonia usa le_iSup no mesmo índice. A normalidade final troca os supremos n/i por iSup_comm, após a normalidade de cada corte. Não é argumento de convergência sequencial que restrinja a rede A a índices contáveis.

[REAL — documentos e evidências] Ficha 22:30:29 e adendo 22:31:48 foram lidos integralmente antes da conclusão desta revisão; ambos precedem o primeiro DEV 22:33:31. Nove fornecedores mais cinco do adendo foram confrontados com suas fontes, linhas, tipos, hashes e cópias próprias. Módulo e auditor independentes passaram; os 15 tipos com universos e respectivos axiomas foram lidos e reparsados. Não há helpers privados, sorry, axioma novo, native_decide ou trustCompiler.

[REAL — histórico e negativo] Duas tentativas autorais rc1 (22:33:31 e 22:35:54) ficam excluídas, mesmo que tenham prints parciais. Seus pins apontam a snapshots históricos reais, nunca à fonte viva. A final 22:36:37 está rc0. O negativo autoral substitui a soma por produto na conclusão de scalarInverseLimitWeight_add e é recusado por Type mismatch, com imports resolvidos. Fonte e streams desse controle foram relidos e pinados; nenhum controle autoral foi executado nesta revisão.

[REAL — proveniência] 680 objetos próprios anteriores preservados; somente módulo e auditor novos, total 682. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 37.249 s; zero avisos do alvo/auditor e 178 mensagens históricas de fornecedores separadas no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e |
| .olean próprio | 9ec83875d0e3314d78d2f0cc23fe22fc6d572a573561f3fddfd9a9e8f918aecf |
| .olean autoral standalone, apenas comparação | 9ec83875d0e3314d78d2f0cc23fe22fc6d572a573561f3fddfd9a9e8f918aecf |

Igualdade binária medida: True.

[OPEN — limites] Aceite exclusivo de 15 declarações: 13 teoremas e duas definições, zero privados. Normalidade provada para redes positivas crescentes, dirigidas e não vazias, com supremo interno no core; não afirma completude do cone de afiliados nem cobertura de todo predual. Fidelidade, semifinitude, tracialidade e escala dual deste peso limite permanecem OPEN neste delta. A consulta anterior é proposta independente, não prova Lean desses campos. Nenhum novo GNS, gap, minorantes positivos finitos de ν ou promoção de A1(b)/gate. O módulo23 é separado e não está aceito por este relatório. Reuso apenas de objetos próprios anteriores e cache de pacotes pinado. Nenhum objeto autoral/DEV, monólito, recorder, writer ou memória executado/modificado.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\compilation.json>) — SHA256 f6cd83f17218d3876bf6e703a614933979d6b7d25d11cff2cc3cf9589b6776c7.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\independent_20260914_224354_013292\run.json>) — SHA256 dd5e804970a5dfff7fe57332ec0379a0c938f7e94813fbdae75ee85d13dd41ee.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\independent_20260914_224354_013292\type_axiom_audit.json>) — SHA256 e5d0bcc95cbd216dc9e929d06c7cd645289046c8ad50e62f38e7490c031db83d.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\history_read.json>) — SHA256 849f895602d8a079a2e7c98a5222dc1ebf4b32d306a7e518447ca1cd694972a9.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\provider_checks.json>) — SHA256 b7a278164a1016fb2b377f96e858067574dab79ab8a782845caf4bd5b7a58daa.
