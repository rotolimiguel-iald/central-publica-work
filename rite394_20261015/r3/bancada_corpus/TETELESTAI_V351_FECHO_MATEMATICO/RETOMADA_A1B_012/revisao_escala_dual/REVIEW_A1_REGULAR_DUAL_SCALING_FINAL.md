# Revisão independente — escala dual do gerador regular

2026-09-14T20:09:36.682572-03:00

**A1_REGULAR_DUAL_SCALING_REVIEW_ACCEPTED__TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 7 declarações (7 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Delta único: V351RegularGeneratorDualScaling, sete teoremas, nenhuma definição. Ficha e adendo foram lidos integralmente; seus fornecedores são verificados por bytes. As oito entregas anteriores são base reutilizada e permanecem preservadas, sem somar seus alvos a este aceite.

[REAL] Convenções verificadas: Fourier inversa transporta shift(t) para characterMultiplier(−2πt); Fourier transporta characterMultiplier(s) para shift(−s/(2π)). A primeira prova usa SchwartzMap.fourierInv_coe explicitamente, a passagem ao L² usa densidade e continuidade de operadores limitados. Não há hipótese de separabilidade de H nem interseção a.e. não enumerável.

[REAL] operatorFieldLift_commutes_character decorre de linearidade complexa ponto a ponto e eventos a.e. finitos. A aplicação usa o V=WF⁻¹ já construído, no mesmo espaço regular, e não supõe W∈N. regularSpectralCoordinates_dual produz V⁻¹C_s=shift(−s/(2π))V⁻¹.

[REAL] O grafo é o mesmo regularPositiveGenerator. A translação das coordenadas exp(−2πξ) dá h C_s x=e^s C_s h x para todo x no domínio. A implicação inversa usa −s, characterMultiplier_inverse e e^(−s)e^s=1. Assim a igualdade de domínios é efetiva e a leitura de conjugação é Ad(C_s)h=e^(−s)h. Não se supõe domínio total, inversa limitada de h, gap, ou uma nova identificação espectral.

[REAL] Histórico relido: DEV 19:55:13 rc1 contém erro de change/coerção de Fourier inversa, erro de simplificação e sorryAx; está excluído. DEV 19:59:17 é rc0 COM um aviso de tática inútil; não foi contado como rc1 nem usado como fonte final. O candidato 20:00:33 é rc0 sem avisos. history_read.json registra os streams e a correção de uma expectativa preliminar incorreta do revisor sobre essa contagem, sem repetir compilação.

[DECLARADO / documentação conferida] A primeira preparação da ficha usou caminho de fornecedor inexistente; a ficha registra correção para V350StrongOperatorField antes do código. Isto é falha de preparação, não negativo matemático. O adendo explicita o fornecedor SchwartzMap.fourierInv_coe. A busca foi delimitada: não alego exaustividade do acervo.

[REAL] O controle autoral BadRegularDualScalingSign foi relido com hashes de fonte/streams: substituir e^s por e^(−s) na segunda componente do grafo produz Type mismatch, com imports válidos. Esta revisão executou seu próprio Lake e auditor; não reexecutou o negativo autoral.

[REAL] Execução própria rc0 em 40.66 s. 648 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351RegularGeneratorDualScaling | `2bd647d5a4c6526780853e16b5ef1ee8f1acddc36570ebdcdc8d74f230e08d50` | `b8e254850037cebfa3129f551c2068b2bfb875b37d97d4961dc5d385d014ebc2` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] A escala dual do mesmo grafo é aceita neste delta. Não há construção de τ, prova de tracialidade ou pagamento de A1(b) completo. A proposta posterior de cortes por escala dual é consulta separada, não alvo Lean destes sete teoremas. Nenhum monólito, recorder, memória, fonte autoral ou relatório anterior foi alterado; nenhuma promoção de gate.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\independent_20260914_200357_657003\run.json>) — SHA256 `342135140bdc78277949e3298a8a4c957f44a773d1d615b59fcee33cd16d39e2`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\compilation.json>) — SHA256 `2ea267f0889505291e68b38bd92772fe94f66ef845957aa7f0dbf9fb47733454`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\independent_20260914_200357_657003\type_axiom_audit.json>) — SHA256 `e3edab754647b23f719d36ae0b2278c4a186bc4d49c15d7717e065a6066103e3`.
