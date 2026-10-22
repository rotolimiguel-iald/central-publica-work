# Revisão independente — fechamento da inscrição GNS do peso

2026-09-14T20:36:04.666344-03:00

**A1_GNS_CLOSEDNESS_REVIEW_ACCEPTED__RIGHT_ACTION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 3 declarações (3 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Delta delimitado de três teoremas, zero definições. Fonte e ficha MD/JSON foram lidas integralmente. Os objetos são scalarWeightLeftIdeal, scalarWeightGNSEmbedding e ScalarGNSHilbert já existentes; o resultado não substitui o ideal completo por finiteDualLeftIdeal nem cria outro GNS.

[REAL] scalarGNSCutMap_weight_embedding estende de fato a identidade dos cortes a TODO a∈nν. A prova mantém scalarCutVacuum com sqrt(dualHaarFactor), o mesmo regularVacuum e dualOrbitRepresentation. Usa eventos a.e. finitos para cada corte e linearidade complexa; não normaliza artificialmente um vetor de corte nem o declara separante.

[REAL] scalarWeightGNSEmbedding_of_cut_actions usa somente os índices n naturais. A união de Ioc(−n,n) cobre ℝ; ae_all_iff é aplicado à família contável, sem uniformização sobre todos os vetores ou um filtro não enumerável. Da igualdade a.e. com v∈L² e sqrt(dualHaarFactor)>0, recupera MemLp da órbita pela escala inversa. hasFiniteScalarSquare_iff_memLp dá a pertinência real de A ao ideal completo, e scalarWeightOrbit_ae identifica a inscrição no mesmo H_I.

[REAL] scalarWeightGNSEmbedding_closed_of_bounded_strong tem índice de universo arbitrário, filtro l e [NeBot l] explícito. A cota uniforme é de norma de operadores; hstrong e hgns são premissas separadas. A continuidade de cada scalarGNSCutMap e dualOrbit_tendsto_of_uniformly_bounded dão dois limites do MESMO vetor cortado; tendsto_nhds_unique usa a não trivialidade. Não se deduz convergência GNS de forte isolada, nem se requer convergência dos adjuntos para este teorema.

[REAL] Cinco fornecedores antigos estavam ausentes em v: V350ScalarGNSCutMaps, V350DualCutLinearMap, V350ScalarBoundedCuts, V350ScalarGNSCutNorm e V350ScalarCutVacuum. Foram copiados em bytes de OLD/kernel após comparação com K e recompilados pelo Lake próprio. Os nomes/pins individuais estão em snapshot e compilation. O build de fornecedores do autor não foi importado nem contado como reprodução própria.

[REAL] Histórico medido: 20260914_202656_437844: rc1; 20260914_202921_830010: rc1; 20260914_203030_719820: rc0. O primeiro rc1 é ausência do objeto ScalarCutVacuum, não refutação matemática; o segundo contém erro de coerção real/complexa e uso inválido de MemLp.congr, com sorryAx transitivo, e está excluído. Só a fonte final rc0 sem avisos é aceita. [history_read.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\history_read.json>), SHA256 `4cb65d43723733b46c5245e873d8523a891e2d96c784e0f025b59c848a3d0216`.

[REAL] Auditoria autoral e negativo BadGNSCutNormalization relidos com hashes, sem execução pela revisão: acrescentar fator 2 à identidade do corte produz Type mismatch, não falha de importação ou ambiente. Um rótulo auxiliar do script validate_gns_closedness menciona INVERSE_CUTOFF; não foi usado para identificar/aceitar este delta. A evidência selecionada é AUDITORIA_FECHAMENTO_GNS_A1B com os três nomes exatos e streams correspondentes; essa observação de rótulo não altera o resultado formal.

[REAL] A ficha antecede o código e aponta consumidor específico: extensão da ação direita para os cortes na perturbação do peso. O fechamento remove uma obrigação real dessa rota, mas não fornece por si uma família de aproximantes nem a segunda convergência exigida.

[REAL] Execução própria rc0 em 124.13 s. 652 objetos próprios anteriores preservados; 5 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351ScalarGNSClosedness | `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8` | `be2da58e27670921dc50a1edf8c79f7b9ca94ea38c282d56fd03dd9f1cb8c335` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Ação direita de elementos além dos fornecedores já pagos, geração forte limitada e passagem a sqrt(Bε) são obrigações posteriores. Nenhuma monotonicidade de sanduíches ou de avaliações perturbadas, tracialidade, novo predual ou pagamento completo de A1(b). Sem cobrança de minorantes positivos para ν, sem mudança de J, gate ou memória. Consulta posterior por grafos/projeções é separada, sem alvos Lean adicionais.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\independent_20260914_203300_093571\run.json>) — SHA256 `15b46bb3014f9fa0b223c8167d2c7607b2280ce39cc04046ee0d1072acb66926`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\compilation.json>) — SHA256 `c2467b1050a3daf7be793feef2fde41c658133810d207d0649c773e3703059d6`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\independent_20260914_203300_093571\type_axiom_audit.json>) — SHA256 `3e498a672b2bf74a7e75b14a73644613058e7c1b698d8841c9d7ba5559c3f1e2`.
