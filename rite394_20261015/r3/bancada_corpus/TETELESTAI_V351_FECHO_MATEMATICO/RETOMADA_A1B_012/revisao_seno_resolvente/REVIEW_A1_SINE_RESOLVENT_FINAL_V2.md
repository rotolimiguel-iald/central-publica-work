# Revisão independente — aproximantes seno e ação direita do resolvente

2026-09-14T21:25:36.126925-03:00

**A1_SINE_RESOLVENT_REVIEW_ACCEPTED__CUTOFF_RIGHT_ACTION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 11 declarações (9 teoremas, 2 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] A ficha REAPROVEITAMENTO_A1B_APROXIMANTES_SENO MD/JSON e o ADENDO_FICHA_SENO_DCT MD/JSON foram lidos inteiros e seus fornecedores confrontados aos bytes. A ficha antecede a implementação dos aproximantes; o adendo antecede o adaptador DCT. O consumidor prometido é realizado por regularSpectralResolvent_right, não acrescentado como hipótese. As buscas anteriores continuam consultas delimitadas, não prova de exaustividade do acervo.

[REAL] Contagem separada: 11 declarações públicas (9 teoremas + 2 definições) têm #check com universos e #print axioms próprios. Além delas, há 6 teoremas privados e 1 definição privada: sineWindow; sineWindow_continuous, sineWindow_nonneg, sineWindow_le_one, sineWindow_character, sineWindow_multiplier e scalarMultiplier_sequence_tendsto. Foram lidos integralmente e compilados no mesmo módulo; seus axiomas são cobertos transitivamente pelos alvos públicos consumidores. Não se alegam sete prints privados adicionais. Inventário em private_declarations.json.

[REAL] O sinal está correto para characterPhase=e^(-isξ): X_m=I/2+(Λ_(-1/m)−Λ_(1/m))/(4i) tem símbolo (1+sin(2πξ/m))/2. regularSineWindowCore_right reutiliza a álgebra da ação direita e os dois geradores regulares. regularSineWindowCore_spectral usa o MESMO V=regularSpectralCoordinates e a igualdade já paga com regularUnitary. As fórmulas para m real não exigem m>0; no limite usa-se exclusivamente m=n+1>0.

[REAL] regularSineResolvent_cfc identifica o aproximante espectral com CFC de X_m: f_m(z)=ofReal(sigmoid(m(2 Re z−1))). A função é globalmente contínua; o multiplicador de X_m está efetivamente em [0,1] e a normalidade usada em map_cfc decorre da positividade. Não se aplica a interface contratante diretamente ao símbolo assinado m sin. A pertinência ao core e à álgebra direita resulta de scalarRightAction_cfc; não foi postulada.

[REAL] sine_rescaled_tendsto usa sinc contínua em zero. O adaptador DCT é sequencial e vale no L² vetorial original: φ_n=(g_n−g)^2‖u‖², dominante integrável ‖u‖² por Lp.memLp. MemLp, a identidade L2_integral_norm_sq e a raiz quadrada transportam o limite da integral para a norma. Os eventos a.e. usados em cada igualdade são finitos para um n e vetor fixos. Não se exige medida finita de ℝ, separabilidade de H, continuidade do representante u ou evento comum a todos os vetores.

[REAL] regularSineResolvent_nonneg e norm_le dão operadores positivos de norma ≤1. A autoadjunção de cada aproximante e de R produz a convergência dos adjuntos a partir da convergência forte demonstrada. regularSpectralResolvent_right aplica scalarRightAction_closed_of_bounded_strongStar com cota 1 e todas as hipóteses descarregadas; conclusão para todo P, sem família aproximante residual. A definição herdada de ScalarPolarRight quantifica TODO A∈nν e usa o MESMO scalarWeightGNSEmbedding, scalarGNSRepresentation e scalarTomitaPolarFactor original. Como R*=R, a conclusão pertence à álgebra com as duas propriedades, não só à propriedade unilateral.

[REAL] Histórico preservado em history_read.json: cinco DEV [rc1, rc0, rc1, rc1, rc0], três falhas excluídas. O rc0 intermediário das 21:09 não é certificado deste delta completo. O DEV de 21:13 ainda tinha um change redundante e um aviso; seus bytes não são apresentados como finais. A comparação byte a byte verificou exclusivamente a remoção dessa linha antes do Lake autoral final, cujos bytes coincidem com o snapshot próprio e cuja compilação não tem avisos de alvo. Nenhum print parcial de rc1 foi aceito.

[REAL] AUDITORIA_APROXIMANTES_SENO_A1B.json e seus streams foram lidos e pinados. O negativo BadSineResolventLimit usa imports funcionais e é recusado por Type mismatch ao trocar o limite R por I−R; não é falha de ambiente. Trata-se de execução autoral relida, sem nova execução do negativo nesta revisão.

[REAL] Execução própria rc0 em 42.29 s. 663 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351SineResolventApprox | `a1c6f5e77916ee527da3716f634431ddaf1f36c9dd80376ceee83aeb63c20c01` | `a487088b4a5384c1455841e0488803ba903fabdb90644ac19ca8464785011529` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] A ação direita do MESMO R está paga neste delta. A igualdade CFC do corte inverso existente e a ação da sua raiz ainda são passos separados; a consulta por equação de grafo não é uma prova Lean aceita neste relatório. Não se prova convergência em norma de operador, monotonicidade dos aproximantes ou DCT para redes arbitrárias. Não se constrói novo GNS/J/h, não se identifica h regular com Δν por homonímia, não se obtém tracialidade nem se altera gate/memórias/custódias.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_seno_resolvente\independent_20260914_211936_715768\run.json>) — SHA256 `7e3808f65b4c61313ee4b197c873073d71a1848256e811d87181515f7f8d3ee7`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_seno_resolvente\compilation_v2.json>) — SHA256 `35dae21196726c18692cd62f70ad60a0486be31f261fa72d8945b46719f6860b`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_seno_resolvente\independent_20260914_211936_715768\type_axiom_audit.json>) — SHA256 `d98aeae0340cfe324b331c53d9745b9adaa13fcc01a0a935463de6f38b97df24`.


Adendo de custódia V2 — 2026-09-14T21:30:08.828280-03:00

[REAL] A entrega da versão anterior foi recusada corretamente antes de emissão: o campo histórico source tinha o hash do DEV mas apontava ao caminho vivo K. Agora aponta aos bytes preservados em [V351SineResolventApprox.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\dev_sine_resolvent\20260914_211359_468646\V351SineResolventApprox.lean>), SHA256 `fc83c5ac59ff78f3dd08c2fb001e447ca42c4da1b5db0c6d1d656d611f30beff`, 13976 bytes. O caminho original consta apenas como historical_location. A mesma precisão foi aplicada ao histórico próprio V2. Fonte final, objetos, execução, tipos, axiomas e conclusão sem P0–P2 permanecem os mesmos. Não houve recompilação; originais do parecer/compilation preservados. Este V2 substitui a versão anterior para entrega.
