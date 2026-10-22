# Revisão independente — cortes do inverso do gerador regular

2026-09-14T20:18:35.747142-03:00

**A1_INVERSE_CUTOFF_REVIEW_ACCEPTED__WEIGHT_PERTURBATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 8 declarações (7 teoremas, 1 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Escopo único: V351InverseGeneratorCutoff, sete teoremas e uma definição. Fonte, ficha MD/JSON e adendo bilateral MD/JSON lidos integralmente. A definição usa exatamente o R, h e a ação dual já revisados; nenhum novo cálculo funcional ou gerador é introduzido. O consumidor indicado é pedersen_takesaki_inverse_generator_trace em LACUNAS_A1, ainda aberto.

[REAL] regularInverseGeneratorCutoff é uma definição total em ε real; membership em N vale para todo ε. As afirmações de positividade, cota, inversão e escala exigem explicitamente ε>0. Não se interpreta o valor formal em ε=0 ou ε<0 como resolvente positivo. regularInverseGeneratorCutoff_le prova a desigualdade de ordem Bε≤ε⁻¹I; o módulo não acrescenta um teorema separado de norma.

[REAL] Afiliação anterior fornece R∈N, e regularDualAction fornece sua imagem em N. A positividade e a cota usam a ordem usual dos operadores no Hilbert, conjugação unitária e escalar real positivo. Não há CompleteSpace do subtipo N assumido, nem comutação genérica de sanduíches. O controle B₁=R respeita Real.log_one e a ação identidade.

[REAL] A equação (Bεx,x−εBεx)∈graph(h) transporta (Rz,z−Rz) pelo caráter com s=log ε e z=C_(−s)x, depois escala ambas as componentes por ε⁻¹. Real.exp_log recebe a hipótese estrita correta. Isso prova imagem no domínio e (h+ε)Bε=I no mesmo grafo, sem identificar apenas um operador homônimo.

[REAL] A escala θ_sBε=e^s B_(εe^s) usa dualAmbient_add, log(εe^s)=log ε+s e cancelamento do escalar não nulo. O fator e^s e o parâmetro εe^s são consistentes com Ad(C_s)h=e^(−s)h. Nenhuma hipótese de comutação com C_s foi introduzida.

[REAL] O último iff é bilateral para quaisquer x,y no Hilbert: (x,y)∈graph(h) ↔ Bε(y+εx)=x. Na ida, subtraem-se dois pares do mesmo grafo; a positividade aplicada a (u−x,−ε(u−x)) força ε‖u−x‖²≤0 e u=x. A volta substitui na equação do grafo já paga. Não há domínio total de h, inversa limitada de h, gap ou premissa oculta de unicidade.

[REAL] Histórico autoral medido: 20260914_200800_436723: rc1; 20260914_200930_786636: rc1; 20260914_201051_634827: rc0; 20260914_201238_097443: rc1; 20260914_201337_906102: rc1; 20260914_201442_615970: rc0. Somente a fonte final sem avisos é selecionada para reprodução. Qualquer rc1 e seus prints parciais/sorryAx são excluídos. Os DEV rc0 anteriores são histórico, não substituem o Lake independente nem fornecem objetos. [history_read.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\history_read.json>), SHA256 `28b663e3d83f7108ea551331a1d2054978b5ea8e4ad2c23a2c7438b043ef1813`.

[REAL] O negativo autoral BadInverseCutoffSign foi lido e pinado, não reexecutado: trocar a segunda componente x−εBεx por x+εBεx causa Type mismatch com imports válidos. Não é falha de ambiente. Ficha antecedente e complemento pré-iff são preservados; a busca declarada é delimitada, sem alegação de inexistência global de fornecedores.

[REAL] Execução própria rc0 em 39.26 s. 650 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351InverseGeneratorCutoff | `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227` | `e9301f745f1e598bc57f0f2d5e64c78dc19fdb8713d4981cce1bc3fe872b1e03` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Construção e identificação bilateral dos cortes aceitas; nenhuma nova definição abstrata de h⁻¹. Monotonicidade de avaliações perturbadas, ação direita GNS dos cortes, limite do peso perturbado e tracialidade não são afirmados neste delta. A1(b) completo permanece aberto. Não se infere ordem de sanduíches da ordem dos cortes; nenhuma cobrança de minorantes positivos para a semifinitude usual de ν. Nenhum monólito, recorder, memória ou arquivo selado anterior foi alterado; zero promoção de gate.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\independent_20260914_201637_202511\run.json>) — SHA256 `9252ca53f705eb15380ae104ec0750e5638caa028f4288cc019c8874585f7611`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\compilation.json>) — SHA256 `262af9f2cd8d1622cf2938757e3eff07500062cf1f0adf3c9167a1d248018f13`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\independent_20260914_201637_202511\type_axiom_audit.json>) — SHA256 `0464e8e74d94a89ae6123777224a2cdd82427e87a475326efcd9f8375603e2c8`.
