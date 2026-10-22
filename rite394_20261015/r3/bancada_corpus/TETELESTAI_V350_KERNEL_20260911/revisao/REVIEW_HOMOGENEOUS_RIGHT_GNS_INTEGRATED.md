# Revisão independente da integração — direita homogênea no GNS

INTEGRATED_HOMOGENEOUS_RIGHT_GNS_REVIEW

2026-09-12T15:58:35-03:00. **[REAL — inspeção independente de bytes, registros e scripts] Nenhum achado P0, P1 ou P2. Integração dos mesmos cinco módulos/28 alvos conferida; gravação da nova memória/custódia ainda pendente.**

Escopo: transposição DEV→TGLExt, conteúdo embutido, raízes, 157 registros fonte/binário/log, Audit atual, 86 controles registrados e os três helpers. A matemática e a recompilação própria dos cinco DEV/28 alvos são herdadas do [parecer DEV preservado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_HOMOGENEOUS_RIGHT_GNS.md>) (SHA256 `6aec98088b94f676679ba8d0933c57722be68c47fd0785321b23164dae38e561`). Nesta rodada houve **zero compilações Lean e zero execuções de monólito, integrador, testes autorais ou recorder**. O novo `ScalarRightStarGraph.lean` e quaisquer desenvolvimentos posteriores estão excluídos; suas provas não foram examinadas.

| Evidência | Resultado conferido | Origem |
|---|---|---|
| Transposição | 5/5, somente prefixo de import; demais bytes idênticos | Comparação própria com snapshots DEV já auditados |
| Embutido | 859 arquivos; exatamente cinco novas chaves; nenhuma antiga removida | Extração literal por AST, sem importar/executar um.py |
| Raízes | TGLExt: cinco imports; Audit: cinco imports e 28 impressões novas; conteúdo anterior preservado | Diff próprio contra cópia da mãe com hash conferido |
| Build incremental | 157 registros rc0: 150 idênticos aos da mãe + cinco módulos novos + duas raízes recompiladas | Registros autorais, relidos e confrontados aos arquivos atuais |
| Audit | 6.687 declarações distintas = 6.659 anteriores + 28 exatas; nenhum nome/axioma anterior perdido | Novo stdout reparseado e comparado integralmente a `axiom_report` |
| Controles | 86/86 registrados como aprovados; 84 anteriores preservados e dois novos | Leitura do relatório autoral; testes não repetidos |
| Fronteira | Seis flags maiores falsas; mesmo gate legado e mesma frontier; runtime integral false | Relatórios atuais e comparação com mãe |
| Memória | 34 superfícies iguais à custódia DEV imediata; nova gravação ainda ausente | Hashes/prefixos relidos, sem editar memória |

**Identidade das fontes e evidência de compilação.** As cinco fontes DEV continuam nos pins do manifesto revisado; a comparação por bytes substitui exclusivamente `import TGLV350.` por `import TGLExt.V350`. O corpo das declarações, namespaces, quantificações e hipóteses permanece idêntico. Os cinco streams de compilação integrada contêm exatamente os alvos de seus módulos e os mesmos axiomas do auditor DEV próprio. Para todos os 157 registros foram relidos a fonte, o `.olean`, stdout, stderr e JSON individual; `returncode=0`, existência do binário, hashes e correspondência entre registro agregado e JSON individual conferem. Os sete registros novos também têm `lean_returncode=0` e fonte inalterada durante compilação. Não se confundem os 157 registros válidos com 157 novas recompilações.

| Fonte integrada/raiz | SHA256 fonte | SHA256 .olean | Log autoral aceito |
|---|---|---|---|
| [TGLExt/V350LocalRightModularTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/V350LocalRightModularTransport.lean>) | `6ff17a665e3c0fc1e156b1e3fe7440e44dcbd811bd1acee2e6963de420bca222` | `b24243ce49769d4bdf12ec2058b8ee0341a664f7b7c42ef0bfb8ddf8a611cf74` | [20260912_154536_985999](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/V350LocalRightModularTransport_20260912_154536_985999.json>) |
| [TGLExt/V350HomogeneousCommutantTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/V350HomogeneousCommutantTransport.lean>) | `d1a8ed8a028d8f9dcb6ab910a3e05721a26a599e2d265f284f0a84f58c3493b3` | `22a1884db88a7906acd83b4e57934ef5281a1022cfaf3db265d9820454f7834d` | [20260912_154606_111838](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/V350HomogeneousCommutantTransport_20260912_154606_111838.json>) |
| [TGLExt/V350ScalarHomogeneousRightOrbit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/V350ScalarHomogeneousRightOrbit.lean>) | `dea570f1f1d43c026874d322b44fbf7e9c30856c2fac17e252319d799085c730` | `a38f12ce77d3d6714087f1beb5fa9705ba31d367b63c027324ee23d06954e1d6` | [20260912_154640_099178](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/V350ScalarHomogeneousRightOrbit_20260912_154640_099178.json>) |
| [TGLExt/V350HomogeneousRightData.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/V350HomogeneousRightData.lean>) | `46248d901ed72c327b0c5c5e1c5a467882c69c215270452134307149e2241b17` | `ae940be73f92eb68ce7acfa63e5c70b2ec40d93884d376decf8a0bc32a5beb9f` | [20260912_154710_383981](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/V350HomogeneousRightData_20260912_154710_383981.json>) |
| [TGLExt/V350ScalarHomogeneousRightGNS.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/V350ScalarHomogeneousRightGNS.lean>) | `3bea19100acbd1fa6dc5caeba5f81bc3222aa67a3cef9169bfe9f6b46124d0a0` | `0a32d9861f67003ba83228764188a00e966d158d3425f26c0f9d26705046f318` | [20260912_154743_740608](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/V350ScalarHomogeneousRightGNS_20260912_154743_740608.json>) |
| [TGLExt.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt.lean>) | `c2a270c8ad387551c2e720a8bb826355ed794f9d110661bf6bae126edd950f95` | `fbf0607bfaaf128458b7cfda176e9cd82965f67640a6448721f32de0a939536b` | [20260912_154831_160626](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/TGLExt_20260912_154831_160626.json>) |
| [TGL/Audit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGL/Audit.lean>) | `dd20f65ff4992186aef78d000b77426455714b673a5ec3523a83d41b48f93bcd` | `48f23968918b0182c3b165d8b6cc10e229225f3fb2848be8ee0045b48593c6e7` | [20260912_154900_598751](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/Audit_20260912_154900_598751.json>) |

A cópia atual tem SHA256 `59ff71f557b8a2c6b6912535114bbc6555ed254eb8635cfd69fd974b3667ad6e`. A comparação da AST Python, substituindo apenas o valor de `_EMBEDDED_KERNEL_FILES` por um marcador, foi igual à cópia da mãe `ae47315d39ca6db7787c3f70d39a4dee747cbc5ad0474b5fbb7a2fcfca28189c`, localizada por hash em [um.py.bak_20260912_154502_841075](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/um.py.bak_20260912_154502_841075>). Entre as 854 chaves antigas, somente os dois agregadores mudaram. `gate_extension.py` permaneceu byte a byte igual à mãe: `c819810b5540747f0a0b7b07b36bb9d7f5e9dd868192ad7410ea15829c566a9e`. O original canônico e `fontes/um_v350_original.py` foram relidos somente para hash e coincidem com o pin original `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`.

**Audit atual, sem usar os campos históricos como âncora.** O log aceito é [Audit_20260912_154900_598751.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/Audit_20260912_154900_598751.json>), SHA256 JSON `74ccbe01552b3affbff79aa5b36e65ee352daff39705ed2cda91bd35da9dd881`. Seu stdout tem SHA256 **`4ce20a5579e3ab2b069ff23a22a694e605f7cf069278fb0e7dad61ee215f176f`**; stderr vazio, rc0, sem warnings. A reanálise completa desse stream produz exatamente o mapa de 6.687 entradas do evidence atual, somente com axiomas do trio `propext`, `Classical.choice`, `Quot.sound`. Todos os 28 alvos do auditor próprio DEV reaparecem com o mesmo conjunto de axiomas, além dos 6.659 anteriores preservados.

Os campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` continuam com `8bc3e69e0bad91bfe9e07bb1c516d8bca5a54fb790edadbe2fa5c6f818402fe1`, igual ao estrato histórico e diferente do stdout corrente. Essa ressalva conhecida é mantida: tais campos **não certificam o stream novo**. A evidência usada aqui é a cadeia registro Audit→JSON→stdout atual→mapa reparseado. Não há nova execução independente do Audit integrado nesta rodada.

**Scripts e controles.** Os três helpers foram lidos integralmente, incluindo os textos interpolados de relatório e memória, e suas ASTs foram analisadas sem execução:

| Helper | Linhas lidas | SHA256 |
|---|---:|---|
| [prepare_homogeneous_right_stage.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/prepare_homogeneous_right_stage.py>) | 91 | `ab0c2ee989e121509f3473574a438083d94b5ee6b7203de42259024a5320f06b` |
| [record_homogeneous_right_progress.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/record_homogeneous_right_progress.py>) | 215 | `c0ef624e8b1eabad85c62f5c37d334f98032e6c46522a89d617c8cc90a418149` |
| [verify_homogeneous_right_custody.py](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/verify_homogeneous_right_custody.py>) | 64 | `78f4dd2bc3b61ca397e2baebfdad5dd30997da7d4475ab974db085bf2f79705a` |

`prepare_homogeneous_right_stage.py` exige o parecer DEV pinado e as duas mães, verifica o estado anterior e prevê backup imediato de bytes/temporário antes de alterar os scripts. Os diffs contra backups cujos hashes coincidem com a mãe confirmam somente: cinco entradas no lote do integrador e contagem 302→330; cinco fontes antes das raízes no compilador; dois grupos adicionais no teste. Não houve enfraquecimento das condições anteriores.

Os dois controles acrescentados são:

- `homogeneous_right_full_scalar_weight_domain_does_not_discharge_KMS_trace_or_physical_frontier`;
- `homogeneous_right_same_GNS_adjoint_pairing_does_not_discharge_KMS_trace_or_physical_frontier`.

Eles verificam presença dos respectivos lemas, as seis flags falsas e a ausência de promoção do gate/plano. São controles de fronteira, não demonstrações de KMS. A tabela de gate continua consumindo somente as três pontes anteriores de tipos exatos em Lean; a existência dos 28 nomes novos não amplia esse consumo.

**As duas mães e o estado pré-gravação.** Mãe matemática: [scalar_weight_gns_custody.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/scalar_weight_gns_custody.json>), SHA256 `87ae3f4ab20548f71ce318b2f7a28304a14cd4a4a100afce5c871bac231122e7`. Mãe imediata de memória: [homogeneous_right_dev_custody.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/homogeneous_right_dev_custody.json>), SHA256 `456a03ff0f32fe34c5edf73ec340031ce554f5ed8847fe1caf2363a3ab4ea25f`. O vínculo desta última à mãe matemática confere, assim como o pin do parecer DEV. As 34 superfícies atuais coincidem com a custódia DEV e preservam os prefixos dos 34 backups já gravados naquela etapa; seus hashes diferem dos anteriores à gravação DEV. Não se exigiu incorretamente que permanecessem iguais à mãe matemática.

O recorder novo usa `memory['surface_sha256']` como estado imediato, verifica esse estado antes da escrita e prevê **novos** backups de bytes ao lado de cada arquivo, append de prefixo preservado e temporário→replace verificado por arquivo. A atomicidade é por arquivo, não uma transação indivisível das 34 superfícies. A custódia projetada guarda separadamente `previous_custody_*` (memória DEV) e `previous_integrated_custody_*` (mãe matemática). O verifier também confere esses dois vínculos, relê todos os pares fonte/binário dos registros compilados, confere artefatos/reviews e exige crescimento com prefixo idêntico ao backup. Não foi retirado o reexame dos `.olean`.

Os 17 caminhos da lista de artefatos que o recorder pretende pinar existem. Na inspeção final **não existem ainda** `homogeneous_right_custody.json`, `homogeneous_right_custody_verification.json` ou `RELATORIO_DIREITA_MODULAR_GNS_INTEGRADA.md`; as 34 memórias continuam no estado DEV. A presente revisão avalia a lógica e os bytes desses helpers; **não declara o recorder/verifier executado nem a nova custódia, seus backups ou suas atualizações de memória concluídos**. O texto que eles gerarão está adequadamente rotulado e mantém a diferença entre adjunto local e KMS global.

**Alcance herdado.** Ficam transportados os operadores direitos para os dados homogêneos e suas instâncias matriciais, no mesmo H_I, com preservação de n_ν e pareamento para quaisquer A,B∈n_ν. Não se assume I=n_ν nem D(S) igual à imagem algébrica. Não se construiu nesta integração uma representação direita de toda N, a extensão por somas a toda matriz local, a identificação do fluxo com (S†S)^it, KMS global, traço, escala/canto Three Locks, hipóteses físicas ou consumo/runtime completo. Essas fronteiras permanecem abertas, sem constituir bugs deste pacote. As dependências e a matemática DEV previamente revisadas foram reutilizadas; não se refez a biblioteca nem a auditoria matemática anterior.

Pins principais e evidência própria:

| Artefato | SHA256 |
|---|---|
| [integration.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/integration.json>) | `793e7fae3419aff53a957d2f8bd53033f9fcfcd13efc0e53752f1307d9948c98` |
| [integrated_compile.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/integrated_compile.json>) | `e8eedf9a22c849a276a34da849194585620e5ff62de9a44436552cea9525946e` |
| [gate_tests.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/gate_tests.json>) | `b9646e9804918cd2366a7e0cdbcd5aafc6644a627371a38b8e73138e3a830c9d` |
| [kernel_incremental_evidence.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel_incremental_evidence.json>) | `e969455c969ec02523607cf4bbaaff5b5a042155398f0e70028073167fb01b63` |
| [Reconciliação própria dos 157 registros](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/homogeneous_right_integrated_20260912_155452_339076/verification.json>) | `feaec248cbfb3c319fc924521a4d6b41f99ed8e4e077989ffc2b2e333f44e732` |
| [Mapa Audit reparseado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/homogeneous_right_integrated_20260912_155452_339076/axioms.json>) | `e14c7a9b9e7b8a6bc1be610f110f743e1f2e57aad5b79f6f78a9f5d7748ff220` |

Os snapshots das fontes, logs e helpers, os diffs e os pins completos estão em [homogeneous_right_integrated_20260912_155452_339076](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/homogeneous_right_integrated_20260912_155452_339076>). Todas as escritas próprias ficaram em `revisao/`; o parecer DEV e as custódias anteriores permanecem intactos. **Revisão integrada delimitada encerrada sem P0–P2; registro posterior de memória/custódia permanece pendente.**
