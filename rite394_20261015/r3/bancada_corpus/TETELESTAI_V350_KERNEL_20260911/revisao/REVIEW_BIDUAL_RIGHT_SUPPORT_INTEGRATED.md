# Revisão integrada — bidual original e suporte direito

## Preliminar estática — 2026-09-13T04:36:49.963165-03:00

BIDUAL_RIGHT_SUPPORT_INTEGRATED_REVIEW

**ESTADO: PRELIMINAR; REVISÃO INTEGRADA FINAL PENDENTE.** O marcador identifica o escopo deste documento; não significa aceite final. Build, binários integrados e testes desta etapa ainda não foram considerados concluídos. Nenhum P0–P2 identificado na inspeção estática delimitada.

[REAL — medido por script, sem executar código autoral.] Cópia SHA256 `b75e541ce53aedab47a8b92848b286dc7934dfe8e33050cdf011f260ac5b7470`; `integration.json` SHA `1f254571c529d9e985dd5aa80ebee3af45d5b000077d0d5fbc23645110428669`. Foram contados **915 embutidos**. Comparação com o backup da cópia mãe de SHA `b996c33b29d2215bee6f66ff58c4cd8c38e696861a01016ceb1225187597c32b`: somente dois novos arquivos Lean, com mudanças nos dois agregadores; todos os outros embutidos preservados. O AST Python fora de `_EMBEDDED_KERNEL_FILES` é igual ao da mãe. `gate_extension.py` conserva SHA `c819810b5540747f0a0b7b07b36bb9d7f5e9dd868192ad7410ea15829c566a9e`.

| Fonte DEV | SHA256 DEV | SHA256 integrada |
|---|---|---|
| ScalarTomitaBidual | `7aaece20ddf3f9a2b197e0ef92319a7d5be7a49543e79123c22e057932f179b9` | `6d8c6b5f02e52c0c07b73b92095a2b4425e50ab1a95a966e50180fbf7953d2d0` |
| ScalarRightFunctionalStability | `4fe83c09767c53a903ad0abeaee648ad4838ea8731c612314cb8c8eeb89c421e` | `ab44460d765921cec0a9c7082728c730a50b4345c2a12d1edca7f08170c5402a` |

A transformação de cada fonte é literalmente apenas `import TGLV350.` → `import TGLExt.V350`, comparada em bytes; fontes no disco e strings embutidas coincidem. Foram reutilizadas as recompilações DEV próprias dos dois módulos, auditor9, tipos e axiomas já revistos: fontes e binários DEV ainda conferem o respectivo snapshot. Nenhum Lean foi recompilado nesta inspeção. Parecer DEV preservado, SHA `8c2bac1ba4cbf96c9a70c342553ed2d7fb144f8fda1259eb2c28ec8d7273909f`.

[REAL — fonte, não execução do Audit.] `TGLExt.lean` e `TGL/Audit.lean` importam os dois módulos uma vez. Os **7.077 nomes distintos** anteriores e suas multiplicidades foram preservados; os **nove nomes novos** são exatamente o manifesto DEV. A fonte Audit agora tem **7.086 nomes distintos**. O batch do integrador soma **729 alvos**, sem duplicatas, contra 720 antes. Isso ainda não é leitura do stdout do Audit integrado.

[REAL — scripts lidos estaticamente.] As diferenças contra backups com hashes da mãe limitam-se a: dois nomes no integrador e contagem 720→729; dois módulos no compilador antes das raízes; um grupo adicional no teste. O grupo `original_bidual_and_right_support_does_not_discharge_KMS_trace_or_physical_frontier` exige presença de cinco alvos representativos, seis flags falsas, `legacy_gate_changed=false` e `full_plan_complete=false`. A conferência final dos nove alvos completos dependerá do Audit corrente; não foi substituída pelo grupo de cinco.

`prepare_bidual_right_support_stage.py`, `record_bidual_right_support_progress.py` e `verify_bidual_right_support_custody.py` foram lidos integralmente, sem execução. O preparador exige leitura do DEV, pins da mãe/fontes/binários e backups em bytes antes das substituições. O recorder exige os dois pareceres, fontes/binários dos registros integrados, transposição, axiomas, identidade do AST e memória prévia. Seus writes usam cópia imediata de bytes, temporário verificado, rechecagem do prefixo original e substituição atômica por arquivo; não são uma transação atômica de todas as superfícies. O verifier relê pares fonte/.olean, pins de artefatos/reviews e backups/prefixos. A presença de marcador é uma guarda textual, não substitui a leitura humana do parecer final.

A correção documental anterior permanece: `original_S_is_maximal_adjoint_of_F`, `selfadjoint_right_pairs_stable_under_commuting_multipliers` e `right_pair_vectors_in_multiplier_range_closure`; os dois nomes errados estão ausentes do manifesto atual. Os parágrafos de resultados/limites do recorder distinguem bidualidade, estabilidade condicional e suporte; as rotas racionais e de quadrados continuam explicitamente DERIVED/OPEN. Não foram promovidas a provas do lote.

[REAL — custódia e memória pré-gravação.] Mãe integrada e documental única: `phase_variational_custody.json`, SHA `49ee6ee4981f189562e67f2d4b5de5ad83860f20f0858cb53b58bf9f5aaa4a76`; seu pin coincide com o draft e a verificação mãe. **34/34 superfícies atuais** coincidem byte-hash com os pins da mãe. Os novos relatório integrado autoral, custody e verification ainda não existiam na captura: não declaro gravação, execução do recorder ou verificação futura. Original canônico e cópia-base foram relidos apenas por hash, ambos `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`. Pareceres anteriores pinados permanecem intactos.

O AST confirma a separação de entradas do gate: `evaluate_quantum_gravity_closure(formal, physics, experiment)` recebe qgc_, qgp_ e feed; `kernel_frontier` é anexado depois. As seis flags qgf/gpf não se tornam entradas diretas por esta integração. Seus valores falsos na mãe foram conferidos; a evidência final desta etapa ainda será relida. Nenhuma afirmação de runtime integral ou objetivo completo.

**Pendências objetivas para o adendo final:** aviso autoral final; leitura dos registros atuais fonte/binário/log/stdout/stderr/dependências (expectativa 213=209 herdados+2 módulos+2 raízes); novo stdout Audit e mapa reparsado, com os nove alvos somente no trio e preservação dos 7.077 anteriores; igualdade dos dois hashes globais Audit ao stream corrente e separação do histórico; controles atuais (expectativa 105), evidência/flags e pins finais de helpers/memórias. `integrated_compile.json`, `gate_tests.json` e `kernel_incremental_evidence.json` vivos não foram consumidos como resultados desta rodada.

Evidência própria: `revisao\bidual_right_support_integrated_20260913_043432_221716/static_verification.json`, SHA `aca3c1b373e42c4c449b453c22473c630aedd16d8fe74d7122b2d239008c26c8`; snapshots, diferenças dos três scripts/raízes, fontes transpostas e `gate_wiring.json` na mesma pasta. As contagens de execução acima são expectativas, não resultados medidos. Não executei monólito, integrador, recorders, testes autorais ou novos rebuilds; todas as escritas desta revisão estão em `revisao/`.

[OPEN] Inversa dos comutantes pelo mesmo J, aproximação racional/quadrados e teste ponderado, identificação modular/KMS, traço, flags maiores e runtime integral permanecem fora do aceite deste preliminar.


## Adendo final — 2026-09-13T04:40:49.317016-03:00

BIDUAL_RIGHT_SUPPORT_INTEGRATED_REVIEW

**ESTADO FINAL: CONCLUÍDO NO ESCOPO INTEGRADO 2 MÓDULOS/9 ALVOS. Nenhum P0–P2 novo ou pendente.** As pendências do preliminar acima foram conferidas após o aviso de término autoral. Seu texto e seus pins foram preservados por backup imediato de bytes e append; o presente adendo contém o veredito final.

[REAL — inspeção independente dos artefatos autorais, sem novo rebuild.] Foram relidos os **213 registros** de `integrated_compile.json`: fonte, .olean, JSON de log, stdout e stderr, com hashes e rc0. **209 registros são literalmente os mesmos da mãe**, inclusive pins de fonte/binário/log/streams; os **quatro novos** correspondem aos dois módulos e duas raízes. Não são 213 execuções novas. Nas quatro novas compilações, `source_unchanged_during_compile=true`, `lean_returncode=0`, sem warnings ou stderr; imports diretos de projeto foram pinados e sua precedência temporal em relação aos novos binários foi conferida.

| Novo log autoral aceito | rc | SHA256 .olean relido |
|---|---:|---|
| V350ScalarTomitaBidual_20260913_043259_788572.json | 0 | `616770352908fd24aa1a3a87c2b4e969f49b410248024fc8171dd4edea958a0f` |
| V350ScalarRightFunctionalStability_20260913_043326_538216.json | 0 | `1a7057426fc50fa69a3fc9454473fa13341ac95751b0fb3ec74026fbb7f36770` |
| TGLExt_20260913_043614_073794.json | 0 | `1abc39b2c4198085645b2321fa1d8400f283845b68be43d6dbf92c1c0bf4983b` |
| Audit_20260913_043640_144511.json | 0 | `e09283735d66d77f591fd2cd06f0e4bb999c4b4ec72a95746d29eba474f06c67` |

Os binários desta tabela são da transposição integrada. A reprodução independente DEV, seus dois binários próprios e auditor9 foram reutilizados do parecer anterior, com pins relidos; não foram confundidos com os binários integrados nem recompilados nesta rodada. Os nove axiomas dos dois novos stdout são exatamente os do auditor próprio e do manifesto corrigido. Tipos/hipóteses preservados pela transposição literal de imports já conferida no preliminar e reconferida agora.

[REAL — Audit atual reparsado.] O registro real `Audit_20260913_043640_144511.json` aponta o stream atual de **897169 bytes**, SHA256 `f77d74be55ea6000f6a02f0045d2b5f14a6afe6a4299c174c7473950d9ba6c27`. Reparseei esse stream para obter **7.086 declarações distintas**, todas restritas a `propext`, `Classical.choice`, `Quot.sound`. As **7.077 anteriores** conservam seus conjuntos de axiomas; as **nove novas** são exatamente o manifesto DEV, sem perda de nomes ou alteração das multiplicidades na fonte Audit. `axiom_report` da evidência coincide integralmente com esse mapa.

Os campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com o SHA do stream atual acima; `audit_stdout_path`, rc0 e `audit_hash_scope=CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES` conferem. Os valores históricos permanecem separados em `historical_v350_audit_metadata`, idênticos aos da mãe; não foram usados como hash do stdout atual.

[REAL — controles autorais relidos, não reexecutados.] `gate_tests.json` contém **105/105 controles aprovados**: os 104 anteriores preservados e somente o novo `original_bidual_and_right_support_does_not_discharge_KMS_trace_or_physical_frontier`. Seu conteúdo exige presença dos alvos representativos e mantém as seis flags falsas, `legacy_gate_changed=false` e `full_plan_complete=false`. O gate legado e a fronteira são iguais aos registros da mãe. A leitura não é execução independente desses testes nem runtime integral.

[REAL — preservação reconferida.] Cópia `b75e541ce53aedab47a8b92848b286dc7934dfe8e33050cdf011f260ac5b7470`, **915 embutidos**, batch **729**. AST Python fora do dicionário Lean igual à mãe; `gate_extension.py` inalterado. As duas fontes integradas/embutidas diferem do DEV apenas pelos imports; somente as duas raízes mudaram entre os embutidos já existentes. Original canônico e base local foram novamente relidos por hash: `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`. As seis flags qgf/gpf atuais são falsas. O rótulo de escopo herdado `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT` não constitui prova nova da inclusão inversa dos comutantes neste lote.

[REAL — helpers e memória antes da gravação.] Os helpers permanecem com os hashes da inspeção estática integral; os dois nomes de metadados corrigidos continuam coerentes com as provas. A errata documental encerrada no DEV não reabriu. O plano de backup e as verificações do recorder/verifier foram examinados, **não executados pelo revisor**. Todos os **34 pins atuais de memória** ainda coincidem com a mãe `phase_variational_custody.json`, SHA `49ee6ee4981f189562e67f2d4b5de5ad83860f20f0858cb53b58bf9f5aaa4a76`. Custódia, verificação e relatório integrado autorais novos ainda não existiam na conferência final. Não afirmo que a gravação futura ocorreu ou que os 34 backups futuros já existem.

Pins finais dos artefatos:

- `integration.json`: `1f254571c529d9e985dd5aa80ebee3af45d5b000077d0d5fbc23645110428669`.
- `integrated_compile.json`: `4f903dc2d463cc7c758283c46a3c769f401ef7205b173b51563eb27143dbf8e9`.
- `gate_tests.json`: `8edd7a776cbd17d0226646a419741098e8c30fd98112b931026d38fb261eb715`.
- `kernel_incremental_evidence.json`: `e1c7861335efdfb4d2186c765e73250bd6937b40d1555987bcdda80b7497bf18`.

Evidência própria completa: `revisao\bidual_right_support_integrated_20260913_043432_221716/verification.json`, SHA `20bd797906e8774729c208bb3ea685e2d66453817856af368438174d873ee381`. A pasta contém os 213 registros/streams capturados, `axioms.json`, `new_module_axioms.json`, `own_DEV_axioms.json`, fontes, diffs e inspeção estática anterior. Essa é a base verificável das contagens; os números não foram tomados da mensagem autoral.

[OPEN — alcance preservado.] O lote identifica o adjunto maximal de F com S no domínio original, constrói Ta como par auto-adjunto sob T*=T, T∈M′ e Ta=aT, e situa cada vetor de par no fecho de Ran R. Não prova ainda cortes racionais, combinações de quadrados como núcleo de gráfico, domínio automático do par ponderado, multiplicador limitado, inclusão inversa pelo J original, identificação de Δ^it/KMS ou traço. Sem promoção de flags, gate ou objetivo integral. Não resta verificação necessária neste escopo integrado delimitado; custódia e gravação de memória continuam atos posteriores do principal.
