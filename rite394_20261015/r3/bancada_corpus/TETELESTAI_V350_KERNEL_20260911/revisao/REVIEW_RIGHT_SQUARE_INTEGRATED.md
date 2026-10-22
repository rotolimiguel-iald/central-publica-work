Parecer integrado — escala direita no domínio de S†S

RIGHT_SQUARE_INTEGRATED_REVIEW

2026-09-12T16:50:59-03:00. **Revisão integrada 2/13 concluída, sem achados P0–P2.** [REAL — inspeção independente de fontes, bytes, AST, logs e helpers.] A matemática e as três execuções próprias DEV (dois módulos e auditor de 13 alvos) são herdadas de [REVIEW_RIGHT_SQUARE_DEV.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_RIGHT_SQUARE_DEV.md>), SHA-256 `98db1998676265cbda08dd44a7cc78276c02861a8affd95420d3a47bcb87d34a`. Nesta rodada não se recompilaram Lean/biblioteca nem se executaram monólito, testes ou helpers autorais.

**Transposição.** Os dois DEV permanecem iguais ao manifesto e aos snapshots próprios. A transposição é literal em bytes, somente `import TGLV350.` → `import TGLExt.V350`; os valores embutidos coincidem com as fontes integradas. Não mudaram tipos, hipóteses ou objetos. São **864 embutidos**, dois novos; entre as entradas anteriores só mudaram `TGLExt.lean` e `TGL/Audit.lean`. Ambas importam os dois módulos exatamente uma vez; o Audit acrescenta apenas os 13 nomes auditados.

| Fonte integrada | SHA-256 da fonte | SHA-256 do .olean relido |
|---|---|---|
| [V350HomogeneousRightSquareDomain.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/V350HomogeneousRightSquareDomain.lean>) | `cfeda2aff89a9b852347d3e9026fd3cac48c64fa3dfd43db42dc2cae3c5cdc93` | `d5ecd1b6da40e128705caa537b57fb3be8d35fa01ff4a6a3c0b8f417565e319d` |
| [V350MatrixUnitRightSquare.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/V350MatrixUnitRightSquare.lean>) | `27403f0368e77e9e8e9c1de5dfdb71e6ccd740a280c13afcbc6c6f68e43a07b9` | `a1fc5af57548a89868d57024260421f5c30f720db31319282bd0ddf0ea31bc2a` |

A cópia tem SHA-256 `735b15923897d1c14e13df7f506e3fa095ec2c5023889d63e0a562bcff3e2b43`. Seu AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com a mãe `f0f7c289ce2754e924f21af2de6204e950cc62cca95fee637c6ffbfbd1aad3a9`. O original canônico e a cópia-base foram somente relidos para hash, ambos `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`. `gate_extension.py` permanece idêntico à mãe, SHA-256 `c819810b5540747f0a0b7b07b36bb9d7f5e9dd868192ad7410ea15829c566a9e`.

**Evidência final.** Foram relidos **162 pares fonte/.olean**, JSONs e streams: rc0, saídas presentes, fontes/binários corretos e cada log igual ao respectivo registro agregado. **158 registros são exatamente herdados; quatro são compilações novas do autor** (dois módulos + duas raízes), com fonte inalterada, `lean_returncode=0` e dependências diretas presentes/frescas. Não são 162 recompilações novas.

Logs novos: [V350HomogeneousRightSquareDomain_20260912_164512_909794.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_square_integrated_20260912_164852_552496/logs/V350HomogeneousRightSquareDomain_20260912_164512_909794.json>); [V350MatrixUnitRightSquare_20260912_164557_169663.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_square_integrated_20260912_164852_552496/logs/V350MatrixUnitRightSquare_20260912_164557_169663.json>); [TGLExt_20260912_164631_075430.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_square_integrated_20260912_164852_552496/logs/TGLExt_20260912_164631_075430.json>); [Audit_20260912_164657_242982.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_square_integrated_20260912_164852_552496/logs/Audit_20260912_164657_242982.json>).

O mapa de axiomas foi reconstruído do stdout atual: **6717 distintos = 6704 anteriores preservados, inclusive seus axiomas, + 13**. Confere integralmente com `kernel_incremental_evidence.json`; os 13 novos coincidem com o auditor DEV próprio e os dois streams integrados. Todo o Audit usa somente subconjuntos de `propext`, `Classical.choice`, `Quot.sound`. O JSON Audit final tem SHA-256 `5719eeb4c2ffd9f4f20c85d0008e7a808db6b2f4e7d7f1cdd29bc33280453d5a`; seu stdout bruto tem SHA-256 `1c4dc33a57efc600e13c4a4bab76963c517ce465ea9b12c16d91aea510395c55`.

[REAL — resultados autorais relidos, não reexecutados] **91/91 controles**: os 90 anteriores foram preservados; a única adição é `same_square_full_domain_matrix_unit_right_scaling_does_not_discharge_KMS_trace_or_physical_frontier`. Confere os cinco lemas de transporte/escala, as seis flags falsas e a fronteira sem promoção. Veredito legado e objeto de fronteira coincidem com a mãe; `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`.

Os dois campos `audit_stdout_sha256` e `audit_capture_sha256_full` apontam aos **bytes atuais**, ambos `1c4dc33a57efc600e13c4a4bab76963c517ce465ea9b12c16d91aea510395c55`; `audit_stdout_path` e `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES` conferem. O histórico explícito permanece igual à base e à mãe, ambos os valores `8bc3e69e0bad91bfe9e07bb1c516d8bca5a54fb790edadbe2fa5c6f818402fe1`. A lógica desses hashes não mudou neste incremento.

**Helpers e mãe única.** `prepare_right_square_stage.py`, `record_right_square_progress.py` e `verify_right_square_custody.py` foram lidos integralmente e parseados, sem execução por este revisor. Os diffs efetivos, contra backups de hash materna, restringem-se aos dois módulos, batch **347 → 360**, ordem antes das raízes e único grupo de controle; não modificam a lógica do gate nem a dos hashes Audit.

| Artefato | SHA-256 lido |
|---|---|
| [prepare_right_square_stage.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/prepare_right_square_stage.py>) | `ed2ab4d8be84ccd1ce13900d2882124e93e915546d9bc5370e026544cc3f7b6c` |
| [record_right_square_progress.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/record_right_square_progress.py>) | `d137999dcec6ca2c34165422255404c7423320a94523ac1fd7c075788c8e7c9e` |
| [verify_right_square_custody.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/verify_right_square_custody.py>) | `3a266939c589f0b578a2cc4709eaa701f772edd64df0a04761c67ee72f0e7f11` |

O preparador exige leitura do parecer, vínculo materno e pins. O recorder exige `--review-read` e os marcadores DEV/integrado; confere original/cópia/AST, registros, controles, stream Audit, os 13 alvos exatos e 34 estados anteriores. O verificador relê fonte e binário de todos os registros, além dos artefatos/pareceres pinados e backups/prefixos. Ambos conferem o stream atual, sem confiar somente no booleano do agregado.

A mãe **integrada e de memória é a mesma**: `scalar_right_tomita_custody.json`, SHA-256 `0106dc15bb5fd4d485e8959906bde88dfdce3d432392ec549026e8d7161df7b9`. Os **34 arquivos atuais e 34 backups** continuam nos hashes e prefixos dessa mãe. O recorder prevê backup imediato de bytes na mesma pasta e append por temporário verificado → substituição; atomicidade por arquivo, sem alegar transação única das 34 superfícies. Recusa novos arquivos de saída já existentes e confere o estado anterior antes da substituição.

A minuta preserva o alcance provado: para unidades matriciais locais, `R_y D(A)⊆D(A)` e `A R_y x=(w_i/w_j)R_y A x` no mesmo `A=S†S` e em todo `D(A)`. Não promove a relação local a identificação de `A^it`, KMS ou representação direita de toda a álgebra. O próximo gerador regular está rotulado como obrigação futura; não integra os 13 alvos. As frentes físicas são limites documentais, sem nova certificação por esta revisão.

[REAL — pré-registro] `right_square_custody.json`, sua verificação e `RELATORIO_ESCALA_DIREITA_SQUARED_INTEGRADA.md` ainda estavam ausentes na conferência final. A análise estática não atesta execução futura dos recorders nem nova gravação das 34 memórias. Os pareceres custodiados e o DEV permaneceram intactos.

| Artefato | SHA-256 lido |
|---|---|
| [integration.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/integration.json>) | `369471602fc2ebd1989195bf5f3ddcb9fd551c222d750f0188949aa29305d8b4` |
| [integrated_compile.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/integrated_compile.json>) | `bda1a4df9df49853f5ab19b3edbcd5230810e03aac0ea07047161940f1558ab7` |
| [gate_tests.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/gate_tests.json>) | `33d2c65a40b37d2c1ea05ecbbbd757ddc36b3d0efd7c27609939360281673630` |
| [kernel_incremental_evidence.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel_incremental_evidence.json>) | `8d5f64835c1f7c07e87d2a6f45742fbb0ba41947ef3ae1d28d7a5c170d1e1282` |

Evidência própria: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_square_integrated_20260912_164852_552496/verification.json>), SHA-256 `15566c4acef7df25dd4f4d02b20c724394f5bc926b2df958bd5d5929e69c9d98`; [static_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/right_square_integrated_20260912_164852_552496/static_verification.json>), SHA-256 `7527ebdaab74812b93d63cda4e3c56715dcdfa58a5c04f72c56e29dd0df46332`. Incluem pins dos 162 registros/streams, transposições, diffs, mapa Audit refeito e estado materno. Nenhuma execução Lean nova nesta rodada.

**Escopo encerrado sem pendências de revisão.** [OPEN] Identificação do fluxo/KMS global, traço, Three Locks, H1–H3 e runtime não são conclusões deste pacote. Nenhuma das seis flags foi promovida. Todas as escritas próprias ficaram em `revisao/`; fontes autorais, originais e memórias não foram modificados.
