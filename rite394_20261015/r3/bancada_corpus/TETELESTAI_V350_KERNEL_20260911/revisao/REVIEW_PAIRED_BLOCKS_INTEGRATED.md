# Revisão integrada — blocos de projeção e teste ponderado original

2026-09-13T07:32:14-03:00 — **PAIRED_BLOCKS_INTEGRATED_REVIEW**

**[REAL] Aprovado o delta integrado de quatro módulos/27 alvos, sem achados P0–P2.** As seis recompilações próprias e as conferências dos registros finais estão concluídas. O [parecer DEV27](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_PAIRED_BLOCKS_DEV.md>) permanece intacto, SHA256 `ddd998c429e36882c65fdd2c474679a3f96ee7eb24e343f2f1172da96e69a068`. Não resta análise necessária dentro deste escopo.

As quatro fontes são transposições literais dos bytes DEV, com a única troca `import TGLV350.` → `import TGLExt.V350`. As hipóteses, os tipos, os universos e os nomes são herdados do auditor DEV27 conferido. As raízes acrescentam apenas os quatro imports e os 27 pedidos de axiomas; preservam as declarações anteriores e suas multiplicidades.

## Execução própria e herança binária

**[REAL — seis execuções Lean próprias]** Árvore isolada em `revisao/`, sem build autoral no `LEAN_PATH`, sem recompilar dependências antigas. Todos os seis binários resultantes são byte a byte iguais aos autorais finais.

| Módulo | rc | Segundos | Alvos impressos distintos | Binário próprio/autoral |
|---|---:|---:|---:|---|
| TGLExt.V350ScalarPairedMultiplicationGraph | 0 | 191.535 | 5 | igual |
| TGLExt.V350HilbertProjectionOrder | 0 | 27.022 | 8 | igual |
| TGLExt.V350ScalarPairedProjectionBlocks | 0 | 210.838 | 12 | igual |
| TGLExt.V350ScalarWeightedProjectionTest | 0 | 56.712 | 2 | igual |
| TGLExt | 0 | 24.175 | 0 | igual |
| TGL.Audit | 0 | 30.246 | 7133 | igual |

O Audit próprio coincide integralmente com o mapa extraído do stream autoral corrente: **7133 declarações distintas**, todas com axiomas contidos em `propext`, `Classical.choice`, `Quot.sound`. As **7106 anteriores** permanecem com os mesmos axiomas; os **27 novos** coincidem exatamente com o manifesto e com o auditor DEV próprio.

**Limitação explícita de proveniência:** a reconstrução própria cobre os seis comandos acima, não a biblioteca inteira. As **900 dependências de projeto** foram copiadas da árvore própria anterior `square_resolvent_integrated_20260913_060615_561897`, com fontes/binários/pins conferidos: **307** vieram de caches próprios anteriores; **3** foram recompiladas independentemente no delta Square20; **205** têm origem em binários autorais integrados e custodiados; **385** têm origem na base canônica, sem reconstrução independente integral. Essas duas últimas categorias continuam herdadas, mesmo estando agora numa árvore própria. Não se renomearam binários DEV para fabricar aliases integrados. Os oito caminhos de pacotes externos ficaram readonly; compiler, imports externos diretos, fontes, binários e companheiros mantiveram os pins. A correspondência fonte→binário de dependências herdadas conserva essa limitação.

## Registros autorais conferidos por leitura

**[REAL — inspeção, sem reexecutar programas autorais]** Relidos os **220 pares fonte/binário**, seus logs JSON e streams: **214 registros idênticos aos da mãe e seis novos** (quatro módulos e duas raízes), com rc0 e fonte inalterada durante compilação. Os imports diretos dos seis novos têm outputs anteriores aos respectivos binários.

> [nota operacional do operador — omitida no retrato público]

- Cópia atual: `fd611111866dc6ff30e9ed355b62bec32cdba505b742d550ffa3351ffd08e566`; **922 embutidos**, batch **776**.
- Mãe `square_resolvent_custody.json`: `52a83cf4d0f6b3927ab8ef706153f325005ce97e0f11400d7ac3b583d4ca04c5`.
- Original e cópia-base relidos somente por hash: `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`.
- Corpo Python fora de `_EMBEDDED_KERNEL_FILES` idêntico ao backup da mãe; `gate_extension.py` idêntico. As seis flags maiores permanecem falsas; gate legado preservado, `full_plan_complete=false`, nenhum runtime integral.
- Audit corrente: **Audit_20260913_072507_908638.json** → stdout bruto → mapa reanalisado. SHA256 do stream `3d4801d3c556deb68193d9b7dc6bd46dfeb1e189510d2e098ee647b6b4b4fd93`; `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com esses bytes. Os valores históricos permanecem separados em `historical_v350_audit_metadata`.

## Helpers e estado anterior à gravação

Lidos integralmente e inspecionados estaticamente `prepare_paired_blocks_stage.py`, `record_paired_blocks_progress.py` e `verify_paired_blocks_custody.py`. O delta dos scripts altera somente a lista/batch de integração, os quatro módulos antes das raízes e o grupo de controle. O preparador exige leitura do DEV e seus quatro pares de pins; o recorder exige os dois pareceres, confere pai, fontes/binários/rc0, Audit corrente/histórico e 34 estados anteriores. O verifier relê os pares compilados e os backups/prefixos, além dos pins do relatório e artefatos.

As **34 memórias continuam byte a byte nos pins da mãe**, relidos antes de concluir. Recorder/verifier novos não foram executados por esta revisão; a nova custódia e o relatório autoral integrado ainda estão ausentes. Os backups/appends futuros são apenas lógica examinada: backup imediato de bytes na mesma pasta, verificação de prefixo e substituição atômica por arquivo; não uma transação atômica conjunta de 34 arquivos.

O texto do recorder distingue corretamente as seis flags qgf/gpf das entradas diretas do avaliador legado (`qgc_`, `qgp_`, feed), com `kernel_frontier` como anexo. Referências a roteiros seguintes permanecem OPEN; não houve nova análise matemática desses guias nem novos alvos atribuídos a eles.

## Alcance matemático mantido

No mesmo H_I, E e S original: o gráfico dos pares fornece os blocos A,B,D na álgebra efetiva M, com `0≤A≤I`, A injetivo, `BB*=A(I−A)` e `BD=(I−A)B`, sem supor `[A,B]=0`. A é bloco de projeção, não o operador modular Δ.

Para η fixo pelo S original e **e∈M, e*=e, [e,A]=0** explícitos, as duas ações de `K=e(I−A)B` são provadas; `Yη=eBB*η` pertence ao domínio original e `S(Yη)=B*eBη=Zη`. Para a seleção variacional e `Re z>0`, vale `2〈ξ,Zη〉=z〈η,Zη〉+conj(z)〈Yη,η〉`. Isso não pressupõe positividade de e nem a deduz, e não afirma comutação de e com B.

**[OPEN]** Cota inferior uniforme positiva de A/inverso limitado, escolha CFC que a produziria, inclusão inversa pelo J original, identificação de Δ^it/KMS, traço e obrigações posteriores. O scope legado `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT` não identifica por homonímia seu J com o J original do peso. Sem promoção de gate, aprovação QG ou execução/importação de monólito. **Aceite limitado à integração DEV27.**

## Evidências e pins finais

- [Verificação final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/paired_blocks_integrated_20260913_072221_079187/verification.json>) — `bb56f23a219488fd02b226f97b5aa7928bb190c1c27c7461dcd96a7b2dd5a462`.
- [Seis recompilações próprias](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/paired_blocks_integrated_20260913_072221_079187/compilation.json>) — `7f96a672920fcb65adf25acb2f1f661ddd2bfc8b272d649f433974da812daf6e`.
- [Fontes, dependências e proveniência](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/paired_blocks_integrated_20260913_072221_079187/build_manifest.json>) — `6c465ed69d2870fc39f3fd5868736208c0081b97c6c69f89b6504c259c118649`.
- [Inspeção estática dos helpers](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/paired_blocks_integrated_20260913_072221_079187/helper_static_inspection.json>) — `c1eeac0cbbf5c69a6d3832030987724df465e09e239867cea689febccf562cc2`.
- [Audit atual reanalisado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/paired_blocks_integrated_20260913_072221_079187/axioms.json>); [Conferência dos 220 registros autorais](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/paired_blocks_integrated_20260913_072221_079187/author_verification.json>); streams próprios e cópias dos logs autorais na mesma árvore.

| Fonte | SHA256 fonte integrada | SHA256 binário próprio = autoral |
|---|---|---|
| TGLExt/V350ScalarPairedMultiplicationGraph.lean | `a6f2c606eb0e314df1ae98d7fb18c3c6be2f8180fde403ef12705f0b8397ab9e` | `5815ac2573464bc9914476f39c45da798d0a8688f9d1599e1fca7c9a50a479df` |
| TGLExt/V350HilbertProjectionOrder.lean | `de3932a91e87dc12beeb0c5eb4ef38d0e036649090d089435d9a08006b3158a3` | `bf748f827acceab857b3a1cac3f1e2637aa557c6fd754c6405764677bba178c3` |
| TGLExt/V350ScalarPairedProjectionBlocks.lean | `d801fa3a06af332b658d334b519518eb1c10bd1dea553699d8c0e786ca330c2d` | `601c0f76fe95e04be6874558f60aac6eb376b2bba18c7e24fd000569ff4b526e` |
| TGLExt/V350ScalarWeightedProjectionTest.lean | `ccc0263f4272c9547fd1ee22596d337793462173d30a105a829e9b5993c3701b` | `b748754cf50c3d48f003cfd340190980d68dee47d4f251bae59820bfb5963f6c` |
| TGLExt.lean | `378df01cd3a9018694dfb2f2407f27da88a49e63b64ef96985966592058f3e1b` | `d566f9d00e9b7d4e78a4d63891cabe1e71d9d49ee048ad98eac0dcf7aed244c3` |
| TGL/Audit.lean | `532d03930258de4181664411ed0bdb57589eccdc73610814aee1be993a31ece3` | `97ba975cdbd64e35bc0bc2b10410103a6ec6b0202bb0bc636f79929c440e70ea` |
