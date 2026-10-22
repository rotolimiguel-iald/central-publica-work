[REAL — sete fornecedores existentes reproduzidos por Lake isolado e aceitos com revisão distribuída segundo a autoria. Quarenta declarações existentes; zero teoremas novos. A1(b), traço concreto, permanece OPEN.]

# ENTREGA 011 / A1 — reprodução dos sete fornecedores pendentes

2026-09-14T18:55:06.554993-03:00

Esta entrega quita a pendência documental e de reprodução dos sete módulos de A1 nomeados na ORDEM012. **Não reescreve matemática já incorporada na v353.** As sete fontes são as mesmas, em bytes, dos19módulos V351 presentes naquele snapshot. A retomada foi aberta depois de RECIBO_B6, em RETOMADA_A1B_012, preservando a bancada B e os artefatos antigos.

## Critérios

| Critério | Resultado |
|---|---|
| Ficha antes da retomada | PAGO; consumidor `regular_dual_weight_modular_implementation`, tipos exatos e fornecedores nomeados. |
| Reaproveitar os sete sem reescrever | PAGO; 36teoremas+4definições=40declarações existentes, zero novos. |
| Lake na raiz isolada | PAGO; autor e revisor recompilaram seus próprios objetos de projeto, rc0. Caches de pacotes explicitados abaixo. |
| Tipos completos e axiomas | PAGO; quarenta #check/#print, subconjuntos do trio. |
| Adulteração recusada | PAGO; duas aplicações adulteradas recusadas por TypeMismatch, sem erro de importação ou timeout no teste aceito. |
| Revisão distinta da autoria | PAGO por divisão explícita: sidecar revê cinco módulos de escala; principal revê dois antiunitários de autoria anterior do sidecar. |
| Habitante RegularCoreTraceData | NÃO PAGO; não é consequência destes sete fornecedores isolados. |
| Integração no um.py ou gate | NÃO EXECUTADA; estes fontes já estavam incorporados, e o programa canônico não foi alterado. |

## Alcance matemático

O cálculo funcional transporta o entrelaçamento de resolventes positivos para suas potências imaginárias. Para r>0, o resolvente escalado é Q_r=T[rI+(1-r)T]⁻¹. O multiplicador de entrelaçamento é limitado e pode ser não invertível; a prova não introduz inversa limitada de T(1-T). A densidade já demonstrada da imagem amortecida permite a extensão por continuidade.

A aplicação concreta usa o mesmo `scalarTomitaResolvent P`, o mesmo `scalarTomitaImaginaryPower P t`, os multiplicadores direitos reais e todo `ScalarGNSHilbert P`. A fase é exp(+it log r). A camada antiunitária fornece **JU_tJ⁻¹=U_t**, com os dois sinais conjugados cancelando; não U_−t. A conjugação é homomorfismo real de *-álgebras, e conjuga os escalares complexos.

Esses resultados não são sozinhos uma identificação de KMS ou da ação em todo o core. O consumo à esquerda e a conjugação no core são deltas posteriores separados. Ainda não há h regular positivo afiliado construído nem a perturbação pelo seu inverso que deve fornecer o traço. A recusa do peso dual como traço permanece válida; não é parede contra existência do traço.

## Reprodução e revisão

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\attempts\20260914_173309_164705\run.json`. O runner `run_replay.py` executou `lake build TGLExt.AuditA1Orphans` com Lean4.31.0, LEAN_PATH removido, sem objetos TGL/TGLExt externos. As 940 fontes/configurações originais e copiadas foram reconferidas. Mathlib e oito pacotes vieram de cache privado pinado; a biblioteca não foi recompilada.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao\independent_20260914_173529_454447\run.json`. Recompilação privada de 470 objetos de projeto, sem copiar objetos autorais. Seu auditor tem os quarenta tipos completos e axiomas. Nenhum aviso nos sete alvos nem no auditor; 178 avisos de fornecedores existentes preservados. Diferenças binárias em relação aos objetos HISTÓRICOS de OLD/build: TGLExt.V351ResolventImaginaryIntertwining, TGLExt.V351ScaledResolventFunctions, TGLExt.V351ScaledResolventCalculus, TGLExt.V351ImaginaryPowerScaling, TGLExt.V351ScalarImaginaryRightTransport, TGLExt.V351AntiunitaryResolventPhase, TGLExt.V351ScalarTomitaImaginaryConjugation. Fontes, tipos e axiomas foram conferidos separadamente; não se afirma reprodução byte a byte desses objetos históricos. Na comparação distinta com o Lake autoral NOVO desta retomada, 7/7 objetos coincidem em bytes. A comparação binária com o snapshot V353 está indisponível nos caminhos registrados e não é tratada como igualdade.

O parecer do sidecar mantém sua ressalva de autoria dos dois antiunitários. **Não o rebatizei como aprovação independente de sua própria obra.** A inspeção semântica do principal está em INSPECAO_PRINCIPAL_ANTIUNITARIOS; o aceite datado ACEITE_ORFAOS_A1B associa essa inspeção às duas reproduções agora concluídas. A nota semântica anterior, que dizia compilação pendente, sobrevive intacta.

Os negativos BadAntiunitaryPhase e BadImaginaryScaling adulteram, respectivamente, a identidade refletida por um fator2 e o sinal da fase escalada. A recusa prova que essas aplicações não fornecem o tipo requerido; não é uma nova demonstração de inexistência de outros operadores. Falhas históricas de compilação do desenvolvimento permanecem fora do conjunto aceito.

## Sete fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351AntiunitaryResolventPhase` | `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8` | `f2788c22f86fec05bb06db0c0ef2ae3f52b33c151be11fdc356641660312b973` |
| `V351ImaginaryPowerScaling` | `fbb31118edeb1863430be521e7dde573c2cf29ce8ad5df556ccfeed49ca12a69` | `86f7045252bbcb0d28b87074362c4d08f158db72791ac4b67ea2a4e4142a7be5` |
| `V351ResolventImaginaryIntertwining` | `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5` | `22b5b4b8921934abd4decf15ac29777e87ba61192153a97d836b6a40b3de4c85` |
| `V351ScalarImaginaryRightTransport` | `5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349` | `2edd544ed663d54c1b16a4db7776dde48f103e228e6fc4dfd5ba8df4684a0037` |
| `V351ScalarTomitaImaginaryConjugation` | `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d` | `e251343e535ffd4a374d2bff1e1dece2746c11ae372cec141ae5c79e1c8c183a` |
| `V351ScaledResolventCalculus` | `89cac33fa016460aaeb44b0de83d296137f2d3d7f826491be6361bb1e2ad8a32` | `6a1c8d78ac795b7725d09e3f550660e2e68ffcbaececc41692e473fe30847866` |
| `V351ScaledResolventFunctions` | `1195b42b9581167d977137f6a8757e3446010f1b18f6d3eb5843f4a49f10adcb` | `1c97ae11718afcf3a737f9ae252bc7b484d18000442293cdda8ed50afb404956` |

## Axiomas das quarenta declarações existentes

| Nome completo | Axiomas |
|---|---|
| `TGLV350.Regular.complex_cfc_selfadjoint_intertwines` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.resolventDampingOperator_intertwines` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.resolventPhaseOperator_intertwines` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.resolventImaginaryPower_intertwines` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventCoordinate` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventDampingFactor` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventDenominator_scalar_pos` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventCoordinate_complement` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventCoordinate_ratio` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventCoordinate_damping` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventCoordinate_phase` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.positive_contraction_spectrum_bounds` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventDenominator_real_cfc` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventCoordinate_cfc` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventCoordinate_continuousOn_spectrum` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventDampingFactor_continuousOn_spectrum` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventDampingOperator` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventDampingOperator_isUnit` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledPositiveResolvent_damping` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledPositiveResolvent_phase` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scaledResolventDamping_denseRange` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.resolventImaginaryPower_scaled_intertwining` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.matrixUnit_imaginaryPower_right_scaling` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scalarTomitaImaginaryPower_regular_right_commutes` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.resolventPhaseFunction_reflection` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_star` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_add` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_smul` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugateRealHom` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_continuous` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_selfadjoint` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_real_cfc` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.complex_cfc_real_imaginary` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_complex_cfc` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_resolventPhase` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.antiunitaryConjugate_resolventDamping` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.resolventImaginaryPower_antiunitary` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scalarTomitaImaginaryPower_polar_conjugate` | propext, Classical.choice, Quot.sound |
| `TGLV350.Regular.scalarTomitaImaginaryPower_polar_operator` | propext, Classical.choice, Quot.sound |

## Arquivos de entrega

| Arquivo | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\REAPROVEITAMENTO_RETORNO_A1B.md` | `fb5e5cc4d652f263990363e0d999f92c5a241e622b10970e3af50af9708056de` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\REAPROVEITAMENTO_RETORNO_A1B.json` | `fe4afda08a480b7ea4aab98b8cc9ed6ace88c6d3193229674f60d6ba04c5a880` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ALVOS_RETORNO_A1B.json` | `1ed12f640009ebd39d88acb67af28d7f8cb65a901ad5f94d01f7d8386953a8d6` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\FONTES_REPLAY.json` | `d4aa6d5b5b75f00da317e847a79b2eafe3f534ff6707a2a1273ac3d38743ea42` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\CACHE_PROVENIENCIA.json` | `66000085dfbcffecbacdd2c489bbe060d6c18e37d227e4a1adcc66717cc2b212` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_ORFAOS_A1B.json` | `a1becfa99eac0b5bf9cf85600705f004bfc45c46c0eb0f86006fe5be4e5521dc` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\INSPECAO_PRINCIPAL_ANTIUNITARIOS.md` | `92e25a658bcab3c8678e95f48924088fc2deee8c3b1f3bb095559b696e9ae760` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\INSPECAO_PRINCIPAL_ANTIUNITARIOS.json` | `e8720da334ff3f8001770c1cd1b59dfa867a4f8a08d082d0b572f55fa92acf88` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_ORFAOS_A1B.json` | `6224f3252cd436aaf89984cd0fda7142adb8c0d3d14bf685b32ead4edc66f15f` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao\REVIEW_A1_ORPHANS_FINAL.md` | `b171a5525644171e7de65350626da06485269c454ffc2aa2124d0ce407ba3287` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao\REVIEW_A1_ORPHANS_FINAL.json` | `6be3a9c9c11a5254eb150c4b2160c035719ddbcf691f12ee29141f18ffb87c55` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao\compilation.json` | `2c0b7e73520a255c0b4d8055b9339b4f0765c00d9eafcd7fa5309d2f9031b3a5` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\prepare_replay.py` | `feee32355864f3d0cd437ca1a58f8ae4ac41abeb3e29d8aebb958d3f3a269322` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\run_replay.py` | `e925743dca794252e0f5d7399c2e263dd1b2036cc3e02293e287c11a0e621817` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\audit_orphans.py` | `1cae9f02741c1be7254f42f06efc9148fdf535d9685a3e1e4108c4630ef8fb01` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\inspect_antiunitary_principal.py` | `1fd84de5675be6dc299e29590191a77cb07e27cfad632f72aa52df1825b27b35` |
| `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\deliver_orphans.py` | `20769c570de6918c9f23e6fb501957e7b9b7cdb6acb0133eea60a2301943b369` |

MANIFESTO_ORFAOS_A1B e RECIBO_ORFAOS_A1B ligam esta entrega aos relatórios, fontes e objetos. A incorporação da gerência e a integração de outros deltas não são simuladas por este documento. Não houve leitura experimental, alteração do D1, criação de sigma, mudança de memórias canônicas ou gate.

## Parecer do sidecar, integral e com sua ressalva

# A1 — revisão e reprodução dos sete módulos órfãos

2026-09-14T18:53:09.513088-03:00 · **A1_ORPHANS_REVIEW**

[REAL] **Reprodução computacional dos sete aceita; cinco módulos de escala revisados sem P0–P2 encontrados.** Os dois antiunitários recebem minha conferência/reprodução e inspeção semântica independente do principal, pinada separadamente; preserva-se a autoria anterior deste sidecar. Sete fontes existentes, **40 declarações = 36 teoremas + quatro definições**, zero novos teoremas. Lake próprio rc0, quarenta `#check` com universos e mapas de axiomas próprios completos, apenas subconjuntos de `propext`, `Classical.choice`, `Quot.sound`. **A1(b) permanece OPEN.**

**Ressalva de independência:** os dois módulos antiunitários tiveram autoria deste sidecar na manhã, conforme relatório histórico preservado. Esta rodada é independente em árvore, objetos e execução, com releitura adversarial; não constitui independência pessoal retrospectiva sobre a própria autoria. A auditoria histórica autoral não foi rebatizada como aprovação independente. A inspeção independente posterior do principal foi lida integralmente e seus 16 alvos/fontes conferidos: INSPECAO_PRINCIPAL_ANTIUNITARIOS.md/json. Ela não aponta P0–P2 e fica pinada separadamente. Assim se distinguem autoria anterior, nova reprodução e inspeção independente, sem atribuir a esta auto-releitura uma independência pessoal inexistente.

## Resultado matemático que foi conferido

1. **Entrelaçamento CFC:** a união compacta dos dois espectros permite indução para funções complexas contínuas. A etapa de conjugação usa auto-adjunção de ambos. Para U(T)R=RU(Q), T,Q são contrações positivas e ambos os extremos são injetivos. R é somente limitado, sem inversibilidade.
2. **Escala:** para r>0, D_r(x)=r+(1−r)x é positivo em [0,1]. F_r(x)=x/D_r(x), e_r(x)=r/D_r(x)²; as identidades de complemento, amortecimento e fase tratam as pontas separadamente. Não se supõe continuidade através de polos fora do espectro. A fase é **exp(+it log r)**.
3. **Cálculo funcional e cancelamento:** E_r=e_r(T) é unidade limitada por CFC, B_Q=B_T E_r e C_Q=exp(it log r) C_T E_r. A sobrejetividade de E_r dá densidade de Ran B_Q; a igualdade se estende por continuidade. **Não se inverte B_T=T(1−T)** nem o operador de entrelaçamento; não há gap novo.
4. **Aplicação concreta:** os dois resultados de transporte usam o MESMO `scalarTomitaResolvent`, `scalarTomitaImaginaryPower`, `ScalarGNSHilbert P`, `matrixUnitRightData` e `regularRightGNS`. Positividade, injetividades, r=localEigenvalue>0 e TR=RQ_r são descarregados por fornecedores reais. Os resultados valem para todos os vetores do Hilbert, sem uma premissa de domínio escondida.
5. **Antiunitariedade:** a conjugação é homomorfismo de *-álgebras **sobre ℝ**, conjugando escalares complexos. CFC real e decomposição real/imaginária provam `star(g_t(1−x))=g_t(x)`. Os dois sinais se cancelam: **JU_tJ⁻¹=U_t**, não U_−t. Na camada genérica J²=I não é hipótese necessária. A especialização consome o flip do **J polar original**, sem substituí-lo pelo J da torre ou por unidade gaussiana. A igualdade final é de operadores limitados complexos, além da igualdade pontual.

Esses são fornecedores efetivos para `regular_dual_weight_modular_implementation`, não sua conclusão inteira. Falta o consumo da ação à esquerda em toda a álgebra conforme o contrato; comutação/escala pela direita e invariância por J não são, isoladamente, KMS. Os sete não produzem gerador regular positivo h, perturbação pelo inverso, traço, nem habitante de `TGLV351.RegularCoreTraceData`.

## Fontes, ficha e histórico

`RECIBO_B6` e seus pins de entrega/manifesto foram conferidos **antes de escrever/preparar** esta reprodução. Ficha MD/JSON e ALVOS atuais foram lidos, seus tipos/linhas/pins confrontados com as sete fontes. Os **19 V351** coincidem com o snapshot V353, inclusive os sete. A retomada reutiliza fichas/buscas anteriores e não anuncia busca exaustiva nova.

Os 16 registros históricos pertinentes foram lidos e pinados: 7 rc0 com fonte final e **9 rc1 excluídos**, inclusive saídas parciais. Seus axiomas rc0 coincidem com os próprios. Isso é histórico autoral distinto do novo Lake; falhas de ambiente/elaboração não são prova matemática nem adulteração válida. Nenhum teste negativo extra foi criado para esta reprodução de fontes imutáveis.

## Reprodução isolada

Projeto `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\v`; saída `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao`. Comando próprio: `lake build` dos sete módulos e `TGLExt.ReviewA1Orphans`. **469 fontes de projeto** copiadas em bytes da árvore antiga por fecho de imports; **470 objetos próprios** construídos incluindo o auditor. Nenhum .olean TGL/TGLExt autoral ou de V353 foi herdado. Toolchain Lean 4.31.0, configurações iguais às pinadas; LEAN_PATH verificado nas traces dentro de v.

Mathlib e oito pacotes auxiliares foram copiados **em bytes, sem hardlinks**, do cache privado anterior em V353/s. Cada arquivo foi lido, copiado e comparado, com manifestos próprios de SHA256. São **objetos de pacotes herdados**, não recompilação independente da biblioteca. O inventário dos 121.039 arquivos de pacotes não contém objetos TGL/TGLExt; a checagem está pinada em compilation.json. A raiz curta foi conferida antes da cópia; não houve escrita em V353. Relatórios/fontes antigos A1 e pins B1–B6 permaneceram inalterados.

Nenhum aviso nos sete módulos e no auditor próprio. Os **178 avisos de fornecedores existentes** permanecem nas traces/JSON e não foram suprimidos pela revisão. Total de jobs Lake inclui cache, não equivale a número de novas provas.

Diferenças de .olean medidas (sem forçar identidade): TGLExt.V351ResolventImaginaryIntertwining, TGLExt.V351ScaledResolventFunctions, TGLExt.V351ScaledResolventCalculus, TGLExt.V351ImaginaryPowerScaling, TGLExt.V351ScalarImaginaryRightTransport, TGLExt.V351AntiunitaryResolventPhase, TGLExt.V351ScalarTomitaImaginaryConjugation. Os pins de ambas as origens e os booleanos por comparação estão no JSON; nenhuma troca de objetos ou nova compilação foi usada para fazê-los coincidir.

Os sete objetos autorais antigos em OLD/build e os sete da reprodução autoral nova em k foram lidos para comparação; o run autoral rc0 e seus streams/pins também foram conferidos. Seus quarenta axiomas coincidem com os próprios. Nenhum objeto autoral foi usado no meu build. Os sete caminhos .olean de V353/kernel/.lake/build/lib/lean não existem (FileNotFoundError/Windows 2, confirmado com leitura elevada); a igualdade com V353 refere-se às fontes, e a comparação binária indisponível fica como null, não como igualdade ou divergência. Nenhum objeto foi buscado ou copiado para preencher essa ausência.

## Pins finais e evidência

| Módulo existente | Declarações | SHA256 fonte | SHA256 .olean próprio |
|---|---:|---|---|
| V351ResolventImaginaryIntertwining | 4 | `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5` | `22b5b4b8921934abd4decf15ac29777e87ba61192153a97d836b6a40b3de4c85` |
| V351ScaledResolventFunctions | 7 | `1195b42b9581167d977137f6a8757e3446010f1b18f6d3eb5843f4a49f10adcb` | `1c97ae11718afcf3a737f9ae252bc7b484d18000442293cdda8ed50afb404956` |
| V351ScaledResolventCalculus | 9 | `89cac33fa016460aaeb44b0de83d296137f2d3d7f826491be6361bb1e2ad8a32` | `6a1c8d78ac795b7725d09e3f550660e2e68ffcbaececc41692e473fe30847866` |
| V351ImaginaryPowerScaling | 2 | `fbb31118edeb1863430be521e7dde573c2cf29ce8ad5df556ccfeed49ca12a69` | `86f7045252bbcb0d28b87074362c4d08f158db72791ac4b67ea2a4e4142a7be5` |
| V351ScalarImaginaryRightTransport | 2 | `5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349` | `2edd544ed663d54c1b16a4db7776dde48f103e228e6fc4dfd5ba8df4684a0037` |
| V351AntiunitaryResolventPhase | 13 | `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8` | `f2788c22f86fec05bb06db0c0ef2ae3f52b33c151be11fdc356641660312b973` |
| V351ScalarTomitaImaginaryConjugation | 3 | `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d` | `e251343e535ffd4a374d2bff1e1dece2746c11ae372cec141ae5c79e1c8c183a` |

- [Parecer JSON](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/REVIEW_A1_ORPHANS_FINAL.json>) — `6be3a9c9c11a5254eb150c4b2160c035719ddbcf691f12ee29141f18ffb87c55`.
- [Compilação](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/compilation.json>) — `2c0b7e73520a255c0b4d8055b9339b4f0765c00d9eafcd7fa5309d2f9031b3a5`.
- [Run próprio](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/run.json>) — `1ca860d7d399dda0a5476acb9d2307a92a195092cab75453c3a8e6409ab3062b`.
- [Snapshot](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/source_snapshot.json>), [inspeção final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/final_inspection.json>) e [cache](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/cache_provenance.json>) e [inspeção separada do principal](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/principal_inspection_read.json>) e [replay autoral relido](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/revisao/independent_20260914_173529_454447/author_cold_replay_read.json>).

**Execução deste escopo encerrada.** A reprodução está concluída; a inspeção semântica por agente distinto dos dois antiunitários provém do documento do principal, não desta auto-releitura. Sem novo teorema-alvo, monólito, integração, entrega pelo túnel, alteração de gate/memória ou início de módulo posterior. O aceite é da reprodução e do significado limitado desses fornecedores; não quita A1(b).


## Inspeção do principal dos dois antiunitários

[REAL — inspeção semântica dos dois fornecedores; reprodução isolada ainda pendente]

# Revisão do principal: camada antiunitária

2026-09-14T18:07:22.267605-03:00

A revisão do principal é distinta da autoria anterior declarada pelo sidecar. O replay do sidecar continuará identificado como reprodução computacional. Nenhum P0, P1 ou P2 encontrado na leitura dos tipos e provas. Esta nota não antecipa rc0.

- The conjugation used throughout is J T J.symm, with J the specified semilinear isometric equivalence. J²=I is not assumed or needed in the generic proof.

- The real star-algebra homomorphism conjugates complex scalars. Real CFC transport and real/imaginary decomposition establish the complex CFC formula; no complex-linear automorphism is falsely attributed to J.

- The damped phase satisfies star(g_t(1-x))=g_t(x). Reflection of log((1-x)/x) and scalar conjugation cancel. Endpoint values are zero through damping; no undefined endpoint division is used to infer a nonzero limit.

- Norm-continuity of bounded antiunitary conjugation justifies CFC transport. Self-adjointness follows by adjoint identities. The CFC composition is supplied with its continuity and star-normality conditions.

- T and 1-T are injective positive contractions in the generic imaginary-power theorem. The already proved dense range of T(1-T) permits extension from damped vectors by continuity. No bounded inverse or spectral gap is introduced.

- The concrete specialization uses the original scalarTomitaResolvent and scalarTomitaPolarFactor. The actual polar-resolvent flip is a supplier, not an assumed new covariance. The resulting group is scalarTomitaImaginaryPower in the same ScalarGNSHilbert P.

- Final pointwise and bounded-operator equalities are JU_tJ^{-1}=U_t. Neither claims JU_tJ^{-1}=U_{-t}, nor a KMS theorem, affiliated regular generator, trace, or complete RegularCoreTraceData inhabitant.

- The existing module V350LocalBasePolarCommutation contains same-name add/smul statements. The actual combined import was accepted in a separate DEV check. This inspection does not label the repeated names a demonstrated compilation bug; the standalone delta build remains required.

## Fontes e declarações relidas

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AntiunitaryResolventPhase.lean` — `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8`

`TGLV350.Regular.resolventPhaseFunction_reflection` :14

```lean
theorem resolventPhaseFunction_reflection (t x : ℝ) :
    star (resolventPhaseFunction t (1-x)) = resolventPhaseFunction t x
```

`TGLV350.Regular.antiunitaryConjugate_star` :28

```lean
theorem antiunitaryConjugate_star (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (star T) = star (antiunitaryConjugate J T)
```

`TGLV350.Regular.antiunitaryConjugate_add` :44

```lean
theorem antiunitaryConjugate_add (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T V : H →L[ℂ] H) :
    antiunitaryConjugate J (T+V) = antiunitaryConjugate J T + antiunitaryConjugate J V
```

`TGLV350.Regular.antiunitaryConjugate_smul` :49

```lean
theorem antiunitaryConjugate_smul (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (c : ℂ) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (c • T) = star c • antiunitaryConjugate J T
```

`TGLV350.Regular.antiunitaryConjugateRealHom` :57

```lean
def antiunitaryConjugateRealHom (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    (H →L[ℂ] H) →⋆ₐ[ℝ] (H →L[ℂ] H)
```

`TGLV350.Regular.antiunitaryConjugate_continuous` :78

```lean
theorem antiunitaryConjugate_continuous (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    Continuous (antiunitaryConjugate J)
```

`TGLV350.Regular.antiunitaryConjugate_selfadjoint` :85

```lean
theorem antiunitaryConjugate_selfadjoint (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) : IsSelfAdjoint (antiunitaryConjugate J T)
```

`TGLV350.Regular.antiunitaryConjugate_real_cfc` :89

```lean
theorem antiunitaryConjugate_real_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℝ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc f T) = cfc f (antiunitaryConjugate J T)
```

`TGLV350.Regular.complex_cfc_real_imaginary` :95

```lean
theorem complex_cfc_real_imaginary (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (f : ℝ → ℂ) (hf : Continuous f) :
    cfc (fun z : ℂ => f z.re) T =
      cfc (fun x : ℝ => (f x).re) T + Complex.I • cfc (fun x : ℝ => (f x).im) T
```

`TGLV350.Regular.antiunitaryConjugate_complex_cfc` :111

```lean
theorem antiunitaryConjugate_complex_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℂ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc (fun z : ℂ => f z.re) T) =
      cfc (fun z : ℂ => star (f z.re)) (antiunitaryConjugate J T)
```

`TGLV350.Regular.antiunitaryConjugate_resolventPhase` :124

```lean
theorem antiunitaryConjugate_resolventPhase (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) :
    antiunitaryConjugate J (resolventPhaseOperator T t) = resolventPhaseOperator T t
```

`TGLV350.Regular.antiunitaryConjugate_resolventDamping` :143

```lean
theorem antiunitaryConjugate_resolventDamping (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) :
    antiunitaryConjugate J (resolventDampingOperator T) = resolventDampingOperator T
```

`TGLV350.Regular.resolventImaginaryPower_antiunitary` :150

```lean
theorem resolventImaginaryPower_antiunitary (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (hi : Function.Injective T) (hj : Function.Injective (1-T : H →L[ℂ] H))
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) (x : H) :
    J (resolventImaginaryPower T hT h1 hi hj t x) =
      resolventImaginaryPower T hT h1 hi hj t (J x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarTomitaImaginaryConjugation.lean` — `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d`

`TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes` :14

```lean
theorem scalarTomitaImaginaryPower_polar_commutes (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (scalarTomitaImaginaryPower P t x) =
      scalarTomitaImaginaryPower P t (scalarTomitaPolarFactor P x)
```

`TGLV350.Regular.scalarTomitaImaginaryPower_polar_conjugate` :23

```lean
theorem scalarTomitaImaginaryPower_polar_conjugate (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarTomitaImaginaryPower P t ((scalarTomitaPolarFactor P).symm x)) =
        scalarTomitaImaginaryPower P t x
```

`TGLV350.Regular.scalarTomitaImaginaryPower_polar_operator` :31

```lean
theorem scalarTomitaImaginaryPower_polar_operator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap =
        (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap
```



## Ficha anterior, integral

[OPEN — ficha anterior à reprodução standalone; fontes matemáticas existentes, sem alteração]

# Retomada A1(b) após B6

2026-09-14T17:31:00.813331-03:00

REUSAR sete módulos já presentes no snapshot v353, todos idênticos em bytes à bancada A1. Não criar outro teorema ou camada para repetir seus resultados. Produto: auditoria de40 declarações, reprodução Lake, revisão independente e entrega própria que faltavam.

Consumidor: regular_dual_weight_modular_implementation, em LACUNAS_A1.md:25; contrato final TGLV351.RegularCoreTraceData, V351RegularCoreTraceContract.lean:43. Estas pontes tratam o grupo do MESMO resolvente/GNS e J polar, sem provar por si a implementação modular integral ou o traço.

## Fornecedores e tipos exatos

### V351ResolventImaginaryIntertwining

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ResolventImaginaryIntertwining.lean` · `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5` · REUSAR, sem editar.

Linha 15: `TGLV350.Regular.complex_cfc_selfadjoint_intertwines`
```lean
theorem complex_cfc_selfadjoint_intertwines (A B R : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (h : A*R=R*B)
    (f : ℂ → ℂ) (hf : Continuous f) : cfc f A * R = R * cfc f B
```
Linha 51: `TGLV350.Regular.resolventDampingOperator_intertwines`
```lean
theorem resolventDampingOperator_intertwines (T Q R : H →L[ℂ] H)
    (h : T*R=R*Q) : resolventDampingOperator T * R = R * resolventDampingOperator Q
```
Linha 57: `TGLV350.Regular.resolventPhaseOperator_intertwines`
```lean
theorem resolventPhaseOperator_intertwines (T Q R : H →L[ℂ] H)
    (hT : IsSelfAdjoint T) (hQ : IsSelfAdjoint Q) (h : T*R=R*Q) (t : ℝ) :
    resolventPhaseOperator T t * R = R * resolventPhaseOperator Q t
```
Linha 64: `TGLV350.Regular.resolventImaginaryPower_intertwines`
```lean
theorem resolventImaginaryPower_intertwines (T Q R : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1T : T ≤ 1) (hiT : Function.Injective T)
    (hjT : Function.Injective (1-T : H →L[ℂ] H))
    (hQ : 0 ≤ Q) (h1Q : Q ≤ 1) (hiQ : Function.Injective Q)
    (hjQ : Function.Injective (1-Q : H →L[ℂ] H)) (h : T*R=R*Q)
    (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1T hiT hjT t (R x) =
      R (resolventImaginaryPower Q hQ h1Q hiQ hjQ t x)
```
### V351ScaledResolventFunctions

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScaledResolventFunctions.lean` · `1195b42b9581167d977137f6a8757e3446010f1b18f6d3eb5843f4a49f10adcb` · REUSAR, sem editar.

Linha 11: `TGLV350.Regular.scaledResolventCoordinate`
```lean
def scaledResolventCoordinate (r x : ℝ) : ℝ
```
Linha 12: `TGLV350.Regular.scaledResolventDampingFactor`
```lean
def scaledResolventDampingFactor (r x : ℝ) : ℝ
```
Linha 14: `TGLV350.Regular.scaledResolventDenominator_scalar_pos`
```lean
theorem scaledResolventDenominator_scalar_pos (r : ℝ) (hr : 0<r) (x : ℝ)
    (hx : x ∈ Set.Icc (0 : ℝ) 1) : 0<r+(1-r)*x
```
Linha 21: `TGLV350.Regular.scaledResolventCoordinate_complement`
```lean
theorem scaledResolventCoordinate_complement (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
    1-scaledResolventCoordinate r x = r*(1-x)/(r+(1-r)*x)
```
Linha 28: `TGLV350.Regular.scaledResolventCoordinate_ratio`
```lean
theorem scaledResolventCoordinate_ratio (r x : ℝ) (hx : x≠0) (hd : r+(1-r)*x ≠ 0) :
    (1-scaledResolventCoordinate r x)/scaledResolventCoordinate r x = r*((1-x)/x)
```
Linha 36: `TGLV350.Regular.scaledResolventCoordinate_damping`
```lean
theorem scaledResolventCoordinate_damping (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
    resolventDamping (scaledResolventCoordinate r x)=
      resolventDamping x * scaledResolventDampingFactor r x
```
Linha 45: `TGLV350.Regular.scaledResolventCoordinate_phase`
```lean
theorem scaledResolventCoordinate_phase (r : ℝ) (hr : 0<r) (t x : ℝ)
    (hd : r+(1-r)*x ≠ 0) :
    resolventPhaseFunction t (scaledResolventCoordinate r x)=
      modularPhase t (Real.log r) * resolventPhaseFunction t x *
        (scaledResolventDampingFactor r x : ℂ)
```
### V351ScaledResolventCalculus

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScaledResolventCalculus.lean` · `89cac33fa016460aaeb44b0de83d296137f2d3d7f826491be6361bb1e2ad8a32` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.positive_contraction_spectrum_bounds`
```lean
theorem positive_contraction_spectrum_bounds (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) {x : ℝ} (hx : x ∈ spectrum ℝ T) :
    x ∈ Set.Icc (0 : ℝ) 1
```
Linha 21: `TGLV350.Regular.scaledResolventDenominator_real_cfc`
```lean
theorem scaledResolventDenominator_real_cfc (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (r : ℝ) :
    cfc (fun x : ℝ => r+(1-r)*x) T = scaledResolventDenominator T r
```
Linha 27: `TGLV350.Regular.scaledResolventCoordinate_cfc`
```lean
theorem scaledResolventCoordinate_cfc (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (r : ℝ) (hr : 0<r) :
    cfc (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T = scaledPositiveResolvent T r
```
Linha 39: `TGLV350.Regular.scaledResolventCoordinate_continuousOn_spectrum`
```lean
theorem scaledResolventCoordinate_continuousOn_spectrum (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    ContinuousOn (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) (spectrum ℂ T)
```
Linha 49: `TGLV350.Regular.scaledResolventDampingFactor_continuousOn_spectrum`
```lean
theorem scaledResolventDampingFactor_continuousOn_spectrum (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    ContinuousOn (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) (spectrum ℂ T)
```
Linha 61: `TGLV350.Regular.scaledResolventDampingOperator`
```lean
def scaledResolventDampingOperator (T : H →L[ℂ] H) (r : ℝ) : H →L[ℂ] H
```
Linha 64: `TGLV350.Regular.scaledResolventDampingOperator_isUnit`
```lean
theorem scaledResolventDampingOperator_isUnit (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    IsUnit (scaledResolventDampingOperator T r)
```
Linha 74: `TGLV350.Regular.scaledPositiveResolvent_damping`
```lean
theorem scaledPositiveResolvent_damping (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    resolventDampingOperator (scaledPositiveResolvent T r) =
      resolventDampingOperator T * scaledResolventDampingOperator T r
```
Linha 98: `TGLV350.Regular.scaledPositiveResolvent_phase`
```lean
theorem scaledPositiveResolvent_phase (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) (t : ℝ) :
    resolventPhaseOperator (scaledPositiveResolvent T r) t =
      modularPhase t (Real.log r) • (resolventPhaseOperator T t * scaledResolventDampingOperator T r)
```
### V351ImaginaryPowerScaling

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ImaginaryPowerScaling.lean` · `fbb31118edeb1863430be521e7dde573c2cf29ce8ad5df556ccfeed49ca12a69` · REUSAR, sem editar.

Linha 13: `TGLV350.Regular.scaledResolventDamping_denseRange`
```lean
theorem scaledResolventDamping_denseRange (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r) :
    DenseRange (resolventDampingOperator (scaledPositiveResolvent T r))
```
Linha 28: `TGLV350.Regular.resolventImaginaryPower_scaled_intertwining`
```lean
theorem resolventImaginaryPower_scaled_intertwining (T R : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r)
    (hR : T*R=R*scaledPositiveResolvent T r) (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (R x)=
      modularPhase t (Real.log r) • R (resolventImaginaryPower T hT h1 hi hj t x)
```
### V351ScalarImaginaryRightTransport

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScalarImaginaryRightTransport.lean` · `5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.matrixUnit_imaginaryPower_right_scaling`
```lean
theorem matrixUnit_imaginaryPower_right_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (homogeneousRightGNS (matrixUnitRightData P N i j) x)=
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaImaginaryPower P t x)
```
Linha 27: `TGLV350.Regular.scalarTomitaImaginaryPower_regular_right_commutes`
```lean
theorem scalarTomitaImaginaryPower_regular_right_commutes (P : SiteProfile) (s t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (regularRightGNS P s x)=
      regularRightGNS P s (scalarTomitaImaginaryPower P t x)
```
### V351AntiunitaryResolventPhase

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351AntiunitaryResolventPhase.lean` · `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.resolventPhaseFunction_reflection`
```lean
theorem resolventPhaseFunction_reflection (t x : ℝ) :
    star (resolventPhaseFunction t (1-x)) = resolventPhaseFunction t x
```
Linha 28: `TGLV350.Regular.antiunitaryConjugate_star`
```lean
theorem antiunitaryConjugate_star (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (star T) = star (antiunitaryConjugate J T)
```
Linha 44: `TGLV350.Regular.antiunitaryConjugate_add`
```lean
theorem antiunitaryConjugate_add (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T V : H →L[ℂ] H) :
    antiunitaryConjugate J (T+V) = antiunitaryConjugate J T + antiunitaryConjugate J V
```
Linha 49: `TGLV350.Regular.antiunitaryConjugate_smul`
```lean
theorem antiunitaryConjugate_smul (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (c : ℂ) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (c • T) = star c • antiunitaryConjugate J T
```
Linha 57: `TGLV350.Regular.antiunitaryConjugateRealHom`
```lean
def antiunitaryConjugateRealHom (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    (H →L[ℂ] H) →⋆ₐ[ℝ] (H →L[ℂ] H)
```
Linha 78: `TGLV350.Regular.antiunitaryConjugate_continuous`
```lean
theorem antiunitaryConjugate_continuous (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    Continuous (antiunitaryConjugate J)
```
Linha 85: `TGLV350.Regular.antiunitaryConjugate_selfadjoint`
```lean
theorem antiunitaryConjugate_selfadjoint (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) : IsSelfAdjoint (antiunitaryConjugate J T)
```
Linha 89: `TGLV350.Regular.antiunitaryConjugate_real_cfc`
```lean
theorem antiunitaryConjugate_real_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℝ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc f T) = cfc f (antiunitaryConjugate J T)
```
Linha 95: `TGLV350.Regular.complex_cfc_real_imaginary`
```lean
theorem complex_cfc_real_imaginary (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (f : ℝ → ℂ) (hf : Continuous f) :
    cfc (fun z : ℂ => f z.re) T =
      cfc (fun x : ℝ => (f x).re) T + Complex.I • cfc (fun x : ℝ => (f x).im) T
```
Linha 111: `TGLV350.Regular.antiunitaryConjugate_complex_cfc`
```lean
theorem antiunitaryConjugate_complex_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℂ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc (fun z : ℂ => f z.re) T) =
      cfc (fun z : ℂ => star (f z.re)) (antiunitaryConjugate J T)
```
Linha 124: `TGLV350.Regular.antiunitaryConjugate_resolventPhase`
```lean
theorem antiunitaryConjugate_resolventPhase (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) :
    antiunitaryConjugate J (resolventPhaseOperator T t) = resolventPhaseOperator T t
```
Linha 143: `TGLV350.Regular.antiunitaryConjugate_resolventDamping`
```lean
theorem antiunitaryConjugate_resolventDamping (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) :
    antiunitaryConjugate J (resolventDampingOperator T) = resolventDampingOperator T
```
Linha 150: `TGLV350.Regular.resolventImaginaryPower_antiunitary`
```lean
theorem resolventImaginaryPower_antiunitary (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (hi : Function.Injective T) (hj : Function.Injective (1-T : H →L[ℂ] H))
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) (x : H) :
    J (resolventImaginaryPower T hT h1 hi hj t x) =
      resolventImaginaryPower T hT h1 hi hj t (J x)
```
### V351ScalarTomitaImaginaryConjugation

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScalarTomitaImaginaryConjugation.lean` · `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes`
```lean
theorem scalarTomitaImaginaryPower_polar_commutes (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (scalarTomitaImaginaryPower P t x) =
      scalarTomitaImaginaryPower P t (scalarTomitaPolarFactor P x)
```
Linha 23: `TGLV350.Regular.scalarTomitaImaginaryPower_polar_conjugate`
```lean
theorem scalarTomitaImaginaryPower_polar_conjugate (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarTomitaImaginaryPower P t ((scalarTomitaPolarFactor P).symm x)) =
        scalarTomitaImaginaryPower P t x
```
Linha 31: `TGLV350.Regular.scalarTomitaImaginaryPower_polar_operator`
```lean
theorem scalarTomitaImaginaryPower_polar_operator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap =
        (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap
```

## Aproveitamento, buscas e limites

As fichas anteriores e BUSCAS_A1 registram as seis modalidades: fontes embutidos por nomes/tipos; notasV350; entregas/bancadas; árvore; TOE; índice do acervo. Seus arquivos e hashes constam no JSON. A retomada acrescenta comparação em bytes contra o snapshot v353, que já contém os sete. Não se anuncia varredura nova exaustiva.

Os 19V351 originais, relatórios e quatro entregas anteriores ficam intactos. O contrato forte e as provas anteriores não são refeitos. A cópia Lake nesta subpasta usa fontes da bancada antiga, caches Mathlib/pacotes pinados da bancada B e nenhum objeto de projeto autoral herdado. Falhas de compilação da manhã permanecem na casa antiga e não são confundidas com esta reprodução. A auditoria histórica antiunitária era autoral do sidecar: a nova revisão será separada.

A1(b) continua OPEN: nenhuma instância de RegularCoreTraceData é prometida por esta entrega documental. O próximo consumidor matemático é o transporte à esquerda dos geradores, pela ponte polar já existente; qualquer novo código exige sua própria ficha.
