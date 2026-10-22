# Revisão independente — domínio inicial de Tomita

2026-09-12T07:50:34-03:00. **Escopo DEV concluído: quatro módulos/14 alvos. Nenhum achado P0, P1 ou P2 nas fontes finais e na rota documental delimitada.** [REAL — leitura integral, recompilação independente e auditor próprio] As provas dão transferência de limites fortes uniformemente limitados pela ação ambiente, densidade de Λ(I∩I*) na norma GNS e um gráfico inicial univalente, invariante pela troca, com domínio denso. Não dão univalência do fecho ou operador Tomita fechado.

Esta revisão é nova. [REVIEW_GNS_REPRESENTATION.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_GNS_REPRESENTATION.md>) e os demais pareceres/custódias anteriores permanecem intocados. Os quatro módulos foram pinados por [tomita_domain_draft_status.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/tomita_domain_draft_status.json>); não se reutiliza o parecer anterior como evidência de seus novos teoremas. A rota [ROTA_DOMINIO_TOMITA_RASCUNHO.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/ROTA_DOMINIO_TOMITA_RASCUNHO.md>) foi lida integralmente, inclusive o adendo que passa de nove para 14 alvos.

## Provas, tipos e hipóteses

**DualOrbitStrongLimits.lean:14–56 (3 alvos).** `dualCharacterField a` é a família s↦D_(a·s), fortemente contínua, com cota de norma 1. Na mesma representação regular K=L²(ℝ,TowerHilbert P), a ação no Hilbert exterior L²(ℝ,K) satisfaz

`L_A = W₊ · fibre(A) · W₋`, com `W₊ = lift(s↦D_s)` e `W₋ = lift(s↦D_(-s))`.

O sinal e a ordem seguem da convenção efetiva `dualAmbient s A = D_s A D_s*` e de `D_s*=D_(-s)`, sem troca de representação ou de fluxo. A igualdade é provada por quatro igualdades a.e. para **A e f fixados**. Depois, W₊ e W₋ são operadores limitados fixos; nenhum conjunto conulo é intersectado ao longo da rede.

O teorema de transferência recebe explicitamente Tᵢ, o CLM limite S, uma cota real C com `∀ i, ‖T i‖≤C`, e `∀ v, T i v→S v` ao longo de **qualquer filtro** sobre `ι : Type*`. Aplica o lema herdado `fibre_tendsto_of_uniformly_bounded` ao único vetor W₋f e a continuidade de W₊. Esse lema herdado usa funções simples de medida finita e equicontinuidade; não exige enumerabilidade, separabilidade, topologia no índice, continuidade em norma de operador nem uma cota adicional de S. Não se afirma existência de um limite forte para uma família que não o tenha. A cota é para todos os índices, não apenas eventual; filtros triviais são admitidos pelo enunciado geral, e a aplicação de densidade usa o filtro não trivial indicado abaixo.

**ScalarGNSStarApproximation.lean:15–51 (3 alvos).** Para A∈I, a definição dá `A_h=X_h* A` no mesmo ideal esquerdo I para todo h. Para **h>0**, A_h* = A*X_h também pertence a I, pois X_h∈I e I é fechado por multiplicação à esquerda por operadores limitados; não se supõe A*∈I. Assim A_h∈I∩I*. O operador e seu adjunto são finitos no sentido uniforme que define esse ideal, não meramente finitos em um vetor escolhido.

Para a convergência, `‖X_h*‖≤1` vale para todo h e `X_h*→I` fortemente vem do lema de adjuntas de contrações, já revisado. Esse lema utiliza a cota de contração; não presume continuidade geral de `star` na SOT. A restrição de `𝓝[≠]0` para `𝓝[>]0` está na direção correta, pois h>0 implica h≠0. Aplicando a transferência ao vetor **fixo Λ(A)** e o entrelaçamento previamente provado, obtém-se Λ(X_h*A)→Λ(A) na norma do L² exterior. A única hipótese sobre A é A∈I; não se introduz estimativa ou convergência à direita de AX_h na norma ν, nem regularização bilateral.

**ScalarGNSStarDensity.lean:13–35 (3 alvos).** `scalarGNSStarEmbedding` é uma função no mesmo H_I, obtida restringindo a inscrição linear já existente; não é declarada aqui como novo `LinearMap`. `tendsto_subtype_rng` transporta a convergência do ambiente para a topologia de H_I, que é a topologia da norma de Hilbert. Para cada A∈I, sua inscrição pertence ao fecho da imagem de I∩I*, usando pertinência eventual para h>0 e `isClosed_closure.mem_of_tendsto`. O filtro `𝓝[>] (0:ℝ)` é não trivial; assim esse passo não extrai pertinência de um limite vazio. A densidade já provada de Λ(I) em H_I conclui `DenseRange` de Λ|_(I∩I*). Esta é densidade GNS efetiva; não é somente densidade forte de operadores em N.

**ScalarTomitaGraph.lean:11–41 (5 alvos).** A inscrição restrita é injetiva pela inscrição de I. O objeto novo tem exatamente o tipo

`scalarTomitaGraph P : Set (ScalarGNSHilbert P × ScalarGNSHilbert P)`

e é `{(Λ(A),Λ(A*)): A∈finiteDualStarCore P}`. Dois pares com a mesma primeira coordenada têm o mesmo A pela injetividade, logo a mesma segunda coordenada. O representante A* produz o par trocado porque star(star A)=A. A imagem pela primeira projeção é densa pela densidade GNS anterior. Todos os vetores e pares estão no mesmo H_I; a adjunta algébrica é tomada no mesmo subtipo de N, estável por `star`.

“Invariância pela troca” descreve uma relação involutiva; não é uma afirmação de operador simétrico ou auto-adjunto no sentido dos produtos internos. O arquivo não toma o fecho do conjunto, não prova que esse fecho seja univalente e não empacota um mapa parcial semilinear. Não há circularidade com fechabilidade, Tomita ou KMS: a univalência inicial depende apenas da injetividade já construída. Nos tipos finais de densidade/univalência/troca não restam hipóteses de densidade, fidelidade ou domínio máximo fornecidas pelo chamador.

## Recompilação e axiomas

**Quatro fontes + auditor próprio, cinco processos rc0**, sem warnings. O auditor contém `#check` de todas as 14 declarações nomeadas e `#print axioms` dos mesmos 14 alvos; conjuntos exatos comparados às fontes e ao status. Todos os alvos usam somente `propext`, `Classical.choice`, `Quot.sound`; nenhum `sorryAx` ou axioma adicional. A saída completa do auditor foi lida. Não houve tentativa de compilação própria falhada nesta etapa.

| Fonte DEV | Alvos | SHA256 da fonte congelada e viva | SHA256 .olean próprio = autoral |
|---|---:|---|---|
| DualOrbitStrongLimits | 3 | `6fdea7f8bb2fadb447c419c35ed5d03a6a622e51f3143623163afb6605179a64` | `892b150416b32c2757a8c48d68a4e569d6baf2d37d5356118942525d5fc4df5a` |
| ScalarGNSStarApproximation | 3 | `bca1af9c8413a21a4ee219a12cfdf0d647f8e8967928c606cbdf5a15a7e2a21a` | `c85dedc9019c78f13ccdb6fb749ddeafe94502dbe14f0c4155ba3b3e2fdbda97` |
| ScalarGNSStarDensity | 3 | `b84c1c06654ddfc9c65a6d9db66001b46ac503579480d7b5b8d4fdda715ba217` | `1262110bd47dadce71827bd7ad1cec176704171efbda95fb012e7fae66e4645a` |
| ScalarTomitaGraph | 5 | `712984b79b495de57936720ba4e39785947af20c28f5342709404409f110dae0` | `01c56a31cc47591d9eb7fed8a355efc666e069ae3fea3f56c5904ed31334dc62` |

| Fonte | Log final autoral conferido, sem executá-lo | SHA256 JSON do log |
|---|---|---|
| DualOrbitStrongLimits | DualOrbitStrongLimits_20260912_072050_985425.json | `0127d8941db9d279b4dd39bf374c5fb4be4c093f08b2295abe5a05c4c41f4677` |
| ScalarGNSStarApproximation | ScalarGNSStarApproximation_20260912_072226_987731.json | `e7827b7ab428ce9b2de7a183bf121f7d2b8bc243a1c2f00ce0447e9bee6659ef` |
| ScalarGNSStarDensity | ScalarGNSStarDensity_20260912_072829_112861.json | `cacf5daf862c2209e0a41a5c7f3b360671c753c5575a9fbdf99b62c0a578b180` |
| ScalarTomitaGraph | ScalarTomitaGraph_20260912_073122_861331.json | `cc7a320f0b4d891bffc8d5170b7410a3c28337df92da037cfa68d6b2dcee688b` |

Foram conferidos hash da fonte, fonte inalterada durante o build autoral, rc0, hash do binário existente, stdout/stderr e igualdade dos streams com suas cópias congeladas. Os quatro .olean próprios são **byte a byte iguais aos autorais finais**. Tentativas anteriores autorais ficam nos logs e não foram tratadas como defeitos pendentes dos bytes finais. Os processos próprios e seus tempos/outputs constam de [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/compilation.json>); os vínculos e hashes de todos os streams estão em [verification_dev.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/verification_dev.json>).

Auditor próprio: fonte `d8977b711eefa4a8a2dbb42f4fcc378acb6ba515b0bc8d29d00f6ab88416191a`; .olean `d9b782a073724042dc744298d03bceddbce7a4de89b4d523d4645da942f92198`; stdout `f97b9b444ee1b6a875af9f13cfb9f2596a607fea8c6c4286f4088acae9077db5`. Declarações completas e tipos expandidos: [TomitaInitialDomainAudit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/sources/TomitaInitialDomainAudit.lean>) e [TomitaInitialDomainAudit.stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/logs/TomitaInitialDomainAudit.stdout.txt>).

**Dependências pinadas.** [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/manifest.json>) registra 385 dependências de projeto, suas fontes e binários próprios congelados, imports e origens nas árvores já revisadas de GNS/representação e domínio modular. Foram copiados apenas os módulos necessários desse catálogo; nenhuma dependência de projeto veio do build autoral. A árvore de saída deste run é a única entrada de projeto no `LEAN_PATH`; seguem apenas os pacotes existentes em modo leitura. Não se recompilou biblioteca nem os GNS anteriores. O compilador, versão e caminho efetivo estão no manifesto: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`, SHA256 `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`.

Permanece explícita a herança histórica de `DualSemifiniteIdeal`: fonte própria `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`, binário próprio `6a242f29df8816cf7e741cb043f6c24f88fb9e844fc60f90d3bce25a4c1f26df`, fonte autoral corrigida `f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3`. A diferença literal foi conferida e consiste somente no comentário já revisado, com provas intactas. Não se afirma reprodução byte a byte da cadeia inteira herdada; limitações binárias de pareceres anteriores permanecem válidas. `RegularScalarWeightCertificate`, que tinha limitação binária registrada anteriormente, não está no fecho de imports desta etapa. Todas as dependências próprias pinadas, as quatro fontes vivas e os pareceres anteriores permaneceram inalterados durante o build.

## Rota, estatuto e limites

Status congelado: `a118638af3630d28c410d4a3df99a7246eaf1d1d166b513310a0a0dd96491608`. Rota integralmente lida: `c94bd8fbc3598e866fc602a929483718c88ff78b66a56048e2d0cea3ac49f91b`; seu hash coincide com o status. O texto principal documenta a fatoração, a regularização esquerda suficiente e a densidade na norma GNS; o adendo explicita os cinco alvos do gráfico inicial e mantém fechabilidade aberta. As referências a nove alvos e à obrigação anterior são um estrato histórico preservado, atualizado pelo adendo para quatro módulos/14 alvos. Não encontrei exagero documental que promova densidade ou invariância por troca a fechabilidade.

Custódia anterior lida e pinada: `7ce9aded5a25d0f799d21c64d22af3055d75f85281e4006dce89de50b8e561be`. Seu pin de [REVIEW_GNS_REPRESENTATION.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_GNS_REPRESENTATION.md>) coincide com o hash vivo `abbf6b5cd3d225aac06bde97f387c0e2f65a6c8f7132e60e5a4fe92e7ecafa8f`. O snapshot anterior `c926ec8a1894a63ef98d4f0f9e56540452e123511617cd6c89f6a69db2eca6ba` e as contagens 92 registros/68 controles/6316 Audit são **herança da custódia GNS**, não evidência integrada dos quatro módulos novos. Não foi repetido o verifier de custódia ou seus 23 backups nesta revisão; a preservação dos pareceres foi conferida diretamente por hash.

**Conclusão exclusivamente DEV.** Nenhuma integração, raiz ou controle Python novo foi executado ou certificado aqui. As quatro recompilações próprias e o auditor encerram o exame autônomo solicitado; eventual integração exigirá inspeção separada de seus artefatos finais, sem usar contagens históricas como se fossem novas.

Continuam [OPEN / fora deste escopo]: univalência do fecho do gráfico, fechabilidade/operador Tomita fechado, normalidade da representação GNS, domínio escalar máximo, decomposição polar, identificação modular/KMS, traço, interfaces operatoriais/preduais, Three Locks/H1–H3, física, consumo de certificado pelo gate e runtime. Não se analisaram fontes posteriores de fechabilidade. Nenhuma análise necessária dos quatro módulos/14 alvos ficou pendente; nenhum gate foi promovido.

Originais, monólito, fontes autorais, memórias, recorders, testes, logs e pareceres anteriores permaneceram somente leitura. Não se executou/importou monólito ou programa autoral. Todas as saídas desta revisão estão em `revisao/`. Este parecer é um arquivo novo; adendos futuros, se solicitados antes de custódia, exigem backup imediato dos bytes e append preservando este estrato.


## Adendo de conferência integrada — 2026-09-12T08:03:09-03:00

**Integração conferida, sem defeito P0/P1 ou divergência nas provas. P2 documental aberto:** [MINUTA_DOMINIO_INICIAL_TOMITA.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/MINUTA_DOMINIO_INICIAL_TOMITA.md>), linhas 5–7, omite a condição **A∈I** antes de afirmar A_h=X_h*A∈I∩I* para h>0. O teorema efetivo `scalarGNSLeftRegularization_mem_starCore` recebe `A : finiteDualLeftIdeal P` (`ScalarGNSStarApproximation.lean:21–27`). A condição permite concluir que X_h*A pertence a I por fechamento à esquerda; não deve ficar implícita numa frase iniciada apenas pela referência à álgebra N. Correção documental sugerida: “Para A∈I, a regularização A_h=X_h* A pertence a I∩I* para h>0 e Λ_ν(A_h) converge para Λ_ν(A) na norma de H_I.” Este achado não pede mudança de Lean nem invalida a conclusão DEV anterior. A minuta inspecionada está congelada com o hash registrado abaixo.

[REAL — inspeção independente de bytes, hashes, imports, AST e registros autorais] Snapshot integrado final medido: **`940f72d47b0458b1696395253d6e66bb0bf85b59f346f06e891da571957ddaae`**, 798 embutidos. A cópia coincide com os pins de `integration.json` e `gate_tests.json`. O original canônico e `fontes/um_v350_original.py` foram relidos somente para SHA256: ambos `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`, igual ao pin de base. Nenhum monólito foi executado/importado.

| Evidência | Resultado e alcance |
|---|---|
| Recompilação própria anterior | Quatro DEV + auditor rc0; 14 tipos/alvos, somente trio. Continua sendo a evidência independente do estrato DEV, preservada acima; não foi repetida. |
| Build integrado autoral | 96 registros rc0, todos com hashes de fonte e .olean conferidos. 90 mantêm fonte/binário do estrato GNS custodiado; seis compilações são novas: quatro módulos e duas raízes. Não significa 96 recompilações. |
| Audit integrado autoral | 6330 declarações distintas, somente `propext`, `Classical.choice`, `Quot.sound`; mapa extraído do stdout exatamente igual ao mapa de `kernel_incremental_evidence.json`. Os 14 alvos novos coincidem em nomes e conjuntos de axiomas com o auditor próprio. |
| Controles autorais | 69/69 registrados como passados. Relatório, vínculo ao snapshot e texto/AST do novo controle foram inspecionados; nenhum teste autoral foi executado pelo revisor. |
| Gate/runtime | Seis flags maiores `false`; `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`. São estatutos conferidos nos registros, sem autorização de runtime ou fechamento de gate. |

**Fontes e tipos.** As quatro fontes integradas `TGLExt/V350*.lean` são exatamente os DEV congelados após a troca do prefixo de imports `TGLV350.` por `TGLExt.V350`. A comparação não precisou modificar finais de linha ou qualquer outro texto. Cada texto embutido coincide byte a byte com sua fonte integrada. Assim os corpos, tipos, quantificações e hipóteses conferidos na revisão DEV foram preservados; não houve um segundo `#check` independente das raízes nesta inspeção. A compilação integrada desses bytes é a execução autoral registrada.

| Módulo integrado | SHA256 fonte integrada | SHA256 .olean integrado autoral lido |
|---|---|---|
| DualOrbitStrongLimits | `a1c944185a25d4fe2c57491cae8f063845c2ae0d9c64d536ddfb7e4e797b15a3` | `7ae6834616fd325870eb114a31dfc0e9fdbef4acf7b455c8daf9824744fad955` |
| ScalarGNSStarApproximation | `e280a88c77e51272147eef2833d73db6d9e251b04c001804663e945a8b31de45` | `71c885933fdf3ebc4dd2440220d3b965ce5b7229b848101ac4fe37691cf1b4d5` |
| ScalarGNSStarDensity | `819bd5f30026f25b4097343f7f6ef84e47bb0f8c131ad5ffea9916507a75e28b` | `5fd4ae68bc59e418e48e2715fc3241eef1cd6e6baf9a0b6a248ad7db3c5ae3c5` |
| ScalarTomitaGraph | `a593af9d063ee60d621c500a6f872a924204b1c3c55efeff3d3f4e20e4d57532` | `c915388ba690be6a8d18963746d4d94826b505f14780cf61b73b21af0e746d17` |

`TGLExt.lean` e `TGL/Audit.lean` importam explicitamente os quatro módulos. Contra o dicionário anterior custodiado, há somente quatro entradas novas, nenhuma removida e apenas as duas raízes alteradas entre as entradas preexistentes. As seis compilações novas declaram fonte inalterada durante a execução e seus seis stdout não têm warnings. Os hashes de **stdout e stderr de cada uma das seis**, timestamps e equivalência dos streams vivos às cópias congeladas constam de [supplemental_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/final_integrated_20260912_080003_546024/supplemental_verification.json>); fontes e streams dos 96 registros foram preservados no mesmo snapshot. Os hashes de todos os binários foram relidos. A afirmação de identidade binária própria × autoral permanece limitada aos quatro DEV previamente recompilados, com as dependências herdadas e limitações explicitadas no primeiro estrato.

**AST e controle de fronteira.** A referência é a cópia anterior `c926ec8a1894a63ef98d4f0f9e56540452e123511617cd6c89f6a69db2eca6ba`, validada contra `gns_representation_custody.json`. Retirada somente a atribuição `_EMBEDDED_KERNEL_FILES`, a AST inteira de Python é idêntica. `gate_extension.py` também é idêntico em bytes, SHA256 `c819810b5540747f0a0b7b07b36bb9d7f5e9dd868192ad7410ea15829c566a9e`.

O único controle novo, `dense_initial_Tomita_graph_does_not_discharge_closed_Tomita_KMS_trace`, em `test_gate_extension.py:343`, exige a presença de seis declarações sobre limite, regularização, densidade e gráfico inicial, juntamente com as seis flags maiores falsas. Ele verifica presença de evidência e preservação da fronteira; não prova fechabilidade, Tomita fechado, KMS ou traço. Removida somente essa nova chamada, a AST inteira do teste coincide com a anterior. Nenhuma chamada antiga foi alterada/removida. As chamadas literais passam de 35 para 36; essa contagem sintática é distinta dos 69 controles do relatório autoral.

**Minuta e fronteira documental.** A minuta foi lida integralmente. Além do P2 de quantificação acima, preserva as distinções corretas: transferência por fatoração, densidade na norma de H_I, gráfico inicial como conjunto de pares, troca de coordenadas sem simetria de operador, fechabilidade e domínio máximo abertos. Seus placeholders de resultados são uma minuta de registro, não foram usados como evidência. Recorders específicos ainda não faziam parte desta solicitação e não foram inspecionados ou executados; esta revisão não atesta a futura execução/custódia desses scripts.

`ScalarGNSStrongContinuity` e `ScalarGNSNormality` foram confirmados ausentes das entradas e das referências embutidas. Não se leram nem compilaram suas fontes/logs para este adendo. Nenhum resultado posterior entra nos quatro módulos/14 alvos ou nas conclusões deste parecer. O inventário I/O conserva seu pin histórico `34133956b6a47012805003adfae734e7439b27e1f611466829af624b1857d89c` e a fonte histórica `c712532dc079b832d9eb1ecc26ea50f2d49aa2c387afa435cc777eb302e96e09`, comparados aos campos históricos da custódia anterior; não passa a ser liberação de runtime da cópia atual.

| Artefato integrado/documental lido | SHA256 |
|---|---|
| integration.json | `5725e7a4c3c233fdf009317ed279b30e39acd376d2c4c7d37667b53b894717e3` |
| integrated_compile.json | `f8473110e80f44ba8f0f7aced10644d74375b2bec5eb950649ba6bcd151ae167` |
| gate_tests.json | `ef19d031c8108f6157bbd2321e462caeeaa0abacba8daa4539d8114a1a2c1824` |
| kernel_incremental_evidence.json | `da01e12e5c2893a504c592223bd6a11d7584f8b8a884feddf8e31e83f65782b3` |
| MINUTA_DOMINIO_INICIAL_TOMITA.md | `567ffa4da076677e2c6081e172da10baa5ebea13d41aaf481bfbf9aed4209362` |

Evidência detalhada: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/final_integrated_20260912_080003_546024/verification.json>) e [supplemental_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/tomita_initial_domain_independent_20260912_074527_749705/final_integrated_20260912_080003_546024/supplemental_verification.json>). Os arquivos pinados e a cópia foram reconferidos antes deste append. A integração foi inspecionada; **não houve novas recompilações próprias, rebuild de biblioteca/raízes ou execução de testes, recorders, verifiers ou monólito autorais**.

**Conclusão:** a conferência integrada dos quatro módulos/14 alvos está encerrada. Permanece a conclusão matemática do DEV: densidade GNS de Λ(I∩I*) e gráfico inicial univalente, invariante por troca, com domínio denso. Não há achado Lean pendente; há a correção P2 documental de A∈I a fazer na minuta. Fechabilidade, normalidade GNS, domínio máximo, KMS/traço, gate e runtime seguem fora da conclusão. As afirmações anteriores de “sem integração certificada” descrevem o estrato DEV e ficam superadas apenas pela inspeção integrada delimitada deste adendo.

Preservação: os 13585 bytes anteriores, SHA256 `8defc48b12cdfa287e53d1a1eb3efa9d67aba277c893447685da7e833a7adf6b`, foram guardados imediatamente em [REVIEW_TOMITA_INITIAL_DOMAIN.md.bak_20260912_080309_532719](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_TOMITA_INITIAL_DOMAIN.md.bak_20260912_080309_532719>). O novo texto é append desse prefixo exato. Nenhum parecer/custódia anterior foi modificado e nenhuma escrita saiu de `revisao/`.


## Adendo documental — P2 encerrado — 2026-09-12T08:06:11-03:00

[REAL — comparação literal de bytes, sem novas compilações ou testes] A única alteração da minuta foi inserir **“para A∈I”** na linha 6, passando a dizer: “construídos, para A∈I, a regularização A_h=X_h* A pertence a I∩I* para h>0 e”. A hipótese agora coincide explicitamente com `scalarGNSLeftRegularization_mem_starCore`; o P2 documental do adendo integrado está **RESOLVIDO**. Não restam achados pendentes dentro do escopo revisado.

Minuta anterior: `567ffa4da076677e2c6081e172da10baa5ebea13d41aaf481bfbf9aed4209362`. Minuta corrigida: `ac72f178c6dedc058803916a5d1d963488fe122ab6b9dd3980ff1594b86a3470`. A substituição literal reproduz todos os bytes atuais, sem qualquer outra diferença. O backup autoral [MINUTA_DOMINIO_INICIAL_TOMITA.md.bak_20260912_080513_218889](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/MINUTA_DOMINIO_INICIAL_TOMITA.md.bak_20260912_080513_218889>) foi conferido byte a byte contra a minuta anterior congelada.

Este adendo é somente documental. Não houve releitura/recompilação das fontes Lean, repetição de controles ou nova inspeção integrada; valem as evidências e limitações dos estratos anteriores. Os recorders agora preparados não foram inspecionados nem executados neste exame. Normalidade DEV e demais desenvolvimentos posteriores continuam fora do pacote.

O estado “P2 aberto” fica preservado historicamente e superado por este encerramento. Antes do append, os 23272 bytes do parecer, SHA256 `f56ba415450afa924ba491532d49d873d1d756940c6dd83bc44b63afd13a3cd5`, foram guardados em [REVIEW_TOMITA_INITIAL_DOMAIN.md.bak_20260912_080611_061601](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_TOMITA_INITIAL_DOMAIN.md.bak_20260912_080611_061601>). O prefixo anterior foi preservado integralmente. Nenhuma escrita fora de `revisao/`; nenhuma alteração em pareceres/custódias anteriores.
