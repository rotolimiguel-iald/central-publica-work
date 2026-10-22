# Revisão independente — CFC dos cortes inversos e raízes originais

2026-09-14T21:30:42.564513-03:00

**A1_CUTOFF_CFC_REVIEW_ACCEPTED__PERTURBED_WEIGHT_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 7 declarações (6 teoremas, 1 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] REAPROVEITAMENTO_A1B_CFC_CORTES MD/JSON e ADENDO_FICHA_CFC_RAIZ_HILBERT MD/JSON foram lidos integralmente e seus pins conferidos. A ficha antecede o código. O adendo declara honestamente ser posterior ao DEV e anterior ao aceite: explicita o fornecedor hilbertPositiveSqrt já existente. GeneralExpectationCP é apenas um molde numa álgebra distinta, não um teorema usado como se tivesse o mesmo tipo.

[REAL] São 7 declarações públicas (6 teoremas + 1 definição) com auditor próprio #check/pp.universes e #print axioms. Há separadamente 2 teoremas privados, regularResolvent_cfc_coordinate e hilbertPositiveSqrt_complex_cfc, lidos integralmente e compilados no módulo. Seus axiomas são incluídos transitivamente nos alvos públicos consumidores; não se alegam dois prints privados adicionais. A fonte inteira tem 8 teoremas e 1 definição.

[REAL] inverseCutoffFunction é uma função escalar total; os teoremas de continuidade, identificação e consumo exigem explicitamente ε>0. O denominador max(min(1,ε),1+(ε−1)Re z) é ≥min(1,ε)>0 em todo ℂ. No símbolo sigmoid a, a combinação convexa limita o denominador inferiormente e permite retirar max. A identidade final é ofReal((ε+exp(−a))⁻¹), com o sinal negativo correto e sem hipótese de gap de h.

[REAL] O helper de coordenadas usa o MESMO regularSpectralCoordinates e regularSpectralResolvent. A naturalidade CFC é aplicada com continuidade global e normalidade descarregada por positividade do multiplicador. realScalarMultiplier_cfc_ae continua recebendo o símbolo sigmoid em [0,1]; o corte completo não é indevidamente tratado como contração quando ε<1.

[REAL] Para Y=cfc Fε R e todo x, a prova obtém (Yx,x−εYx) no grafo do MESMO regularPositiveGenerator pela identificação espectral já existente. As igualdades a.e. de subtração/escala são usadas apenas para esse vetor fixo. O iff bilateral de regularInverseGeneratorCutoff, aplicado ao par, produz Bε((x−εYx)+εYx)=Yx e portanto Bεx=Yx. Não se redefine o inverso, não se assume a igualdade desejada, não se exige x∈D(h), e não se trata h como limitado.

[REAL] regularInverseGeneratorCutoff_right consome a ação direita de R que foi reproduzida e aceita no parecer seno11, aplica scalarRightAction_cfc e transporta a pertinência pela igualdade exata de operadores. A ação é na mesma scalarPolarRightAlgebra, cuja propriedade herdada quantifica todo A∈nν e usa o GNS/π/J originais. Não há família aproximante ou pertinência à álgebra direita como premissa residual do teorema concreto.

[REAL] A raiz é exatamente hilbertPositiveSqrt do fornecedor V350AntiunitaryPositiveConjugation:15, cuja definição é CFC.sqrt com instâncias fixadas em Hilbert genérico. O helper genérico usa CFC.sqrt_eq_real_sqrt com h0, cfcₙ_eq_cfc com continuidade de Real.sqrt e sqrt(0)=0, e cfc_real_eq_complex com autoadjunção derivada de h0. Assim não introduz raiz concorrente nem postula positividade. scalarRightAction_sqrt recebe b∈E e b≥0; o corolário concreto descarrega ambos usando o corte existente e ε>0.

[REAL] Histórico em history_read.json: dois DEV rc1 excluídos (cast/equações e ajuste de instâncias), seguidos do final 20260914_212240_170889 rc0 sem avisos, com os mesmos bytes do snapshot próprio e do Lake autoral. Nenhum print de tentativa falha foi aceito. A auditoria autoral e os streams foram relidos: BadCutoffCFCMirror é recusado por Type mismatch ao substituir R por I−R no CFC. É controle autoral relido, não reexecutado nesta revisão.

[REAL] Execução própria rc0 em 39.97 s. 665 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351InverseCutoffCFC | `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490` | `6c4f489bd40b3654a2b1e9e22e4344d58c16c6d831e460d5754d13e5aedba0db` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Este delta paga Bε=cfc Fε R e a ação direita do corte e da sua raiz positiva ORIGINAL para ε>0. Não constrói peso perturbado, limite/ordem das avaliações, tracialidade ou o traço final. Não há novo h, inverso, J, GNS ou condição do gate; nenhum monólito, memória, fonte autoral ou parecer anterior foi modificado. A1(b) completo permanece aberto.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\independent_20260914_212646_190543\run.json>) — SHA256 `c8cd3b958b79bbc2df94c212c67e904f42634992363a5979492172e62f08843b`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\compilation.json>) — SHA256 `8e5fdce08194bf6141f37d7a00ff732aa799e96dbeec6738dcd5d4207499d856`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\independent_20260914_212646_190543\type_axiom_audit.json>) — SHA256 `8f3e6391f4cdc802288073fd985e55300bd0f7bfaad10eb3edd7a5643e1fd846`.
