# Revisão independente — representação GNS no fecho do ideal finito

Estrato DEV encerrado em 2026-09-12T07:37:23-03:00. Integração e controles finais ainda aguardam o estrato de inspeção abaixo; não são resultados de recompilação própria.

**Parecer matemático delimitado: nenhum achado P0, P1 ou P2 nas cinco fontes finais.** [REAL — leitura integral e recompilação independente] Os 21 alvos novos elaboram, o auditor cumulativo confere seus tipos e axiomas, e a construção entrega uma representação complexa unital fiel da mesma álgebra N sobre o Hilbert H_I, fecho da imagem do ideal I. Não há premissa residual de fidelidade, densidade do domínio máximo ou continuidade forte da operação adjunta.

Este parecer acrescenta **cinco módulos/21 alvos** ao pacote anterior de três módulos/14 alvos. O status autoral de oito módulos/35 alvos é cumulativo. Os três anteriores foram reutilizados a partir da árvore independente aprovada em [REVIEW_GNS_ORBIT.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_GNS_ORBIT.md>), que permanece intocada; não foram recompilados nesta etapa. Hash lido desse parecer: `7aecc6cbdaa978f4a8ba267e1fc94bc99b7ca2ed729e74fd5ed7305bbf4c2baf`.

## Enunciados e composição conferidos

- **OperatorFieldAlgebra.lean:12–69.** Constantes, soma, produto, escala complexa e adjunta são compatíveis com o lift. A ordem do produto é F(s)G(s), aplicada como F(s)(G(s)v). As igualdades em L² usam interseções finitas de conjuntos de medida total para cada vetor fixado, sem uniformização a.e. não enumerável. O lema da adjunta (57–69) recebe **duas famílias já fortemente contínuas e uniformemente limitadas**, com G(s)=F(s)*; a prova por produtos internos integrados não constrói continuidade forte de F* a partir da de F. Na aplicação dual, a segunda família é a família efetiva de A*, e a igualdade vem de `map_star`.
- **ScalarGNSCompletion.lean:13–60.** H_I é literalmente o submódulo `(scalarGNSLinear P).range.topologicalClosure` de L²(ℝ,L²(ℝ,TowerHilbert P)), com as duas medidas de Lebesgue herdadas. A completude vem do fecho em um Hilbert; a inscrição é a mesma aplicação linear com contradomínio restrito. A ação preserva primeiro a imagem, pois BA pertence ao mesmo ideal esquerdo I, e depois o fecho pela continuidade do operador ambiente. A norma da restrição é ≤‖B‖ e o entrelaçamento é π(B)Λ(A)=Λ(BA). Trata-se da norma induzida pela inscrição/ν, não de uma afirmação de que a inscrição seja limitada na norma de operador herdada por I.
- **DualOrbitRepresentation.lean:14–37.** O campo θ_s(A) define um `StarAlgHom` unital sobre o L² exterior. Soma, produto e escala usam as leis da mesma `dualAmbient`; a unidade é o lift do campo constante identidade. A operação `star` é a adjunta Mathlib do CLM no Hilbert exterior. A representação ambiente está definida em todos os operadores limitados do Hilbert regular; a composição final restringe sua entrada ao subtipo N.
- **ReducingStarRepresentation.lean:14–53.** A restrição genérica exige um submódulo completo e invariância para **todo** elemento da álgebra, portanto também para as adjuntas. Essa hipótese basta para a identidade ⟨w,ρ(a*)v⟩=⟨ρ(a)w,v⟩ na restrição. Não se deduz redutibilidade de mera invariância por um único operador. No módulo final, completude e invariância são fornecidas pelos resultados concretos anteriores; não ficam como premissas novas.
- **ScalarGNSRepresentation.lean:14–26.** `scalarGNSRepresentation P` compõe a inclusão de N com a representação ambiente e a restrição ao mesmo `scalarGNSSubspace P`. A aplicação subjacente é a já chamada `scalarGNSAction`, como verifica a elaboração do entrelaçamento na prova seguinte. `scalarGNSEmbedding_denseRange` demonstra agora explicitamente a densidade, via fatoração pela imagem e inclusão no fecho; não pressupõe a continuidade da inscrição na norma de operador de I.
- **ScalarGNSRepresentation.lean:28–65.** Fidelidade: π(B)=0 implica Λ(BA)=Λ(0) para todo A∈I; injetividade da inscrição dá BA=0 na representação regular original. Para h>0, X_h pertence a I e BX_h→B fortemente, lema herdado com os mesmos P e B. Para cada vetor v, a família é eventualmente zero no filtro `𝓝[>] (0:ℝ)`, que é não trivial, e a unicidade do limite no Hilbert força Bv=0. `ext1 v` mantém a igualdade de vetores L², sem presumir representantes pontuais contínuos. O caso reverso vem de `map_zero`; a injetividade usa B−C. O enunciado final só recebe P, e a equivalência de nulidade recebe adicionalmente B∈N.

Nos tipos auditados não há hipótese de separabilidade de H, vetor η fixado pela ação dual, identificação I=n_ν, GNS de domínio máximo, nem fidelidade da representação dada como hipótese. Não foi introduzida conversão de um valor infinito por `toReal` nestas cinco fontes. A identidade de norma herdada conserva sua tipagem: `ENNReal.ofReal ‖Λ(A)‖² = ν(A*A)`.

## Evidência própria e pins

Primeiro estrato: [quatro recompilações + auditor de 17 alvos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation4_independent_20260912_072536_210455/compilation.json>). Segundo estrato: [quinto módulo + auditor cumulativo de 21 alvos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073231_721305/compilation.json>). Resultado: **cinco módulos e dois auditores, sete processos rc0**, sem warnings nas cinco fontes finais. O auditor cumulativo contém **22 `#check`** (inclui o abreviador `ScalarGNSHilbert`) e **21 `#print axioms`**; cada alvo depende somente de `propext`, `Classical.choice`, `Quot.sound`. Conjuntos exatos comparados ao status e às declarações das fontes.

| Fonte DEV | Alvos | SHA256 fonte lida | SHA256 .olean próprio = autoral |
|---|---:|---|---|
| OperatorFieldAlgebra | 5 | `35ccb04dce7dae3df0da2eaee57a29539039669bb34030f12e356914fd03b0e3` | `a7c7835e744e07769974128fbd8eea879f54abb0c5eedb6ff4c28a93de70bd0a` |
| ScalarGNSCompletion | 9 | `658c9b58fb79da9700d94c2e4f8cd1f52cad7f8b71eb98df3d5608a350106e5c` | `f6f1c35ae002e6b2d60b46135e67805f3441e1d59d29f63fca72c4903439a683` |
| DualOrbitRepresentation | 2 | `dfa8541d94f0072edc9bcf88874a9b87fb88ce08849d71f7381296e825627528` | `fd6efb5a3f35b091b3a687ed84f283c1faef247eb17c2ad21450b98ca01bd5db` |
| ReducingStarRepresentation | 1 | `79a0c03282c1328f5b4d6963242a3ee1737a11c12353cec5f8244a5030b5f2fa` | `558bdba8562cf38b29b142317b0f73f4172c9a530a093a8d1e8217957f48c195` |
| ScalarGNSRepresentation | 4 | `df53d6dfbc3ac90485d7474d4c86ecfad38f876cd6c3363761af1a88bd74dbef` | `80ed0cd924018aba8809900062de2fa07e9a7c4a4756dd953f9864d278a09564` |

| Fonte | Log final autoral conferido | SHA256 JSON do log |
|---|---|---|
| OperatorFieldAlgebra | OperatorFieldAlgebra_20260912_070559_888219.json | `fd988b2d65af0e0ccdb1d95b2c9664864d5c66ec655c452b031cd3e083734754` |
| ScalarGNSCompletion | ScalarGNSCompletion_20260912_070711_145603.json | `fd33c125b4ca323f1be66f38a8a76742d67e100c5b6c929d7acbe0754fc7b3ca` |
| DualOrbitRepresentation | DualOrbitRepresentation_20260912_071319_704386.json | `3b5a6dcf9da0161d1673b924544eeacb892cc968b65b36abc006d09f80a6e39f` |
| ReducingStarRepresentation | ReducingStarRepresentation_20260912_071905_448410.json | `91e29ea4ca1f24525705973f72a424b950093e7d69559f4b6ffa5641916ffd81` |
| ScalarGNSRepresentation | ScalarGNSRepresentation_20260912_072442_080042.json | `a2506fe11937c00e78c100a1700bb0c87d7f0669322a14e255dc4d61766aee95` |

Os logs autorais acima são **evidência inspecionada**, distinta das execuções próprias. Foram conferidos rc0, fonte inalterada durante a compilação, hash do binário presente, stdout/stderr e correspondência com o status congelado. Os cinco binários independentes são byte a byte iguais aos autorais finais. Todos esses vínculos, hashes dos streams e ausência de warnings constam de [verification_dev.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073231_721305/verification_dev.json>). Status congelado de oito módulos/35 alvos: `1897d61bdb5d63bd6baadd59c32d31c2c641427537cb3a9dc7bbdeceb9631545`.

Auditor cumulativo: fonte `b263e749da3749fa824f68c94ad2c08e2eb151d43df50ca5b85abc1c95dfe260`; binário `2ff88f42a23f0291a72a47effa3ff7cb3a2445e63bdd3f18d960116b9377020f`; stdout `58492968981d9e6b941435181594e28e32f148ccea4831d70fd8c7749e497aca`. A saída impressa foi lida, incluindo o `StarAlgHom` final e os tipos de densidade/fidelidade sem hipóteses extras.

**Proveniência e limite binário.** [Manifesto dos quatro módulos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation4_independent_20260912_072536_210455/manifest.json>) pina 377 dependências de projeto vindas das árvores independentes anteriores, incluindo os três GNS já revisados. O quinto reutiliza esses 377 e os quatro novos binários próprios: 381 módulos herdados, materializados numa única árvore própria para a resolução dos imports. [Manifesto do quinto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073231_721305/manifest.json>) registra os hashes, fontes congeladas, caminhos, versão e `LEAN_PATH` efetivo; nenhum build de projeto do autor entrou no `LEAN_PATH`. Pacotes e compilador foram reutilizados somente para leitura, sem reconstrução da biblioteca. Compilador: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`; SHA256 `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`.

Permanece a exceção histórica explícita `DualSemifiniteIdeal`: fonte própria congelada `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`, binário próprio `6a242f29df8816cf7e741cb043f6c24f88fb9e844fc60f90d3bce25a4c1f26df`; fonte viva `f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3`. O congelamento conferiu a diferença literal exclusivamente no comentário já objeto de errata, com provas intactas. Não se afirma identidade binária de toda a cadeia herdada nem se revogam limitações de revisões anteriores. `RegularScalarWeightCertificate`, cujo parecer anterior registrou divergência binária, não pertence a este fecho de imports.

Uma tentativa própria inicial do quinto falhou antes da elaboração por resolução de imports: a primeira entrada `LEAN_PATH` continha o prefixo TGLV350, mas não `ScalarGNSCompletion.olean`; a segunda entrada não supriu esse prefixo. Evidência preservada em [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073201_614035/compilation.json>). Corrigiu-se apenas a montagem da árvore própria, copiando os binários já pinados; a nova execução acima passou. Essa falha de ambiente não é ocultada nem contada entre os sete rc0. Nenhuma fonte Lean foi editada.

## Documentação e fronteira

A minuta [MINUTA_REPRESENTACAO_GNS.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/MINUTA_REPRESENTACAO_GNS.md>) foi lida integralmente: SHA256 `07a0acbf059d5ade55c6a949c265cf4df42b4728d93b67fbe16f1411a35bd415`. As afirmações nas linhas 5–25 correspondem à inscrição anterior e às cinco fontes finais: completude do fecho de I, densidade da inscrição, ação limitada, *-homomorfismo unital e fidelidade pelo aproximante forte. A fidelidade que era apenas anunciada antes do quinto rc0 agora tem prova conferida. Os placeholders de contagens são destinados ao registro integrado; não foram tomados por resultados já medidos. Os scripts de registro/custódia são inspecionados estaticamente, nunca executados pelo revisor; sua versão final e a nota posterior serão delimitadas no adendo integrado.

**Limites mantidos [OPEN / fora deste parecer]:** identificar I com n_ν máximo ou estender a inscrição a esse domínio; densidade GNS de Λ(I∩I*); normalidade da representação; construção/fechabilidade de Tomita, identificação modular e KMS; traço canônico e interfaces operatoriais/preduais; Three Locks/H1–H3/física, consumo do certificado pelo gate e runtime integral. A norma ≤‖B‖ de cada operador da representação não é um teorema de normalidade de π. A densidade de Λ(I) no fecho que a define não resolve as outras densidades.

Desenvolvimentos posteriores de limites fortes, aproximação/densidade por I∩I* e gráfico inicial não foram lidos, congelados ou compilados nesta revisão. Uma nota autoral separada sobre eles não os inclui nos 21 alvos revisados ou no pacote cumulativo de 35. Pareceres anteriores, originais, fontes autorais, memórias e logs permanecem intocados. Sem execução/importação de monólito, recorders, verifiers ou testes autorais, e sem aprovação de QG/gate/runtime.


## Adendo final — integração e documentação encerradas

2026-09-12T07:41:03-03:00. [REAL — inspeção independente de fontes, binários, AST e registros autorais; sem recompilação própria das raízes ou execução dos controles]

**Escopo concluído. Nenhum achado P0–P2 nas cinco fontes finais nem na integração/documentação delimitada.** O estrato DEV acima permanece preservado. A menção anterior à pendência de integração é superada por este adendo, que conserva a distinção entre execuções próprias e registros inspecionados.

Snapshot final medido: **`c926ec8a1894a63ef98d4f0f9e56540452e123511617cd6c89f6a69db2eca6ba`**, 794 arquivos embutidos. O hash da cópia coincide com `integration.json` e `gate_tests.json`. Original canônico e cópia-base foram lidos somente para hash e coincidem com o pin: `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`. Nenhum deles foi importado/executado.

| Evidência | Resultado | Como foi conferida |
|---|---|---|
| Cinco DEV desta revisão | 21 alvos; cinco recompilações próprias rc0 | Duas árvores próprias sucessivas e auditor cumulativo de 21 alvos/22 tipos; sete processos rc0 contando os dois auditores. |
| Três DEV do parecer GNS_ORBIT | 14 alvos anteriores reutilizados | Pins e axiomas da revisão anterior comparados ao novo status e Audit integrado; sem nova recompilação. |
| Build integrado autoral | 92 registros válidos | Fonte e .olean de cada registro conferidos por hash; 82 registros preservam fonte/binário do estrato 84, e dez compilações são novas: oito módulos GNS e duas raízes. Não significa 92 recompilações. |
| Controles Python autorais | 68/68 registrados como passados | JSON, hash da cópia e AST do controle novo inspecionados. Não executados pelo revisor. |
| Audit integrado autoral | 6316 nomes distintos, todos no trio | Extração do stdout e igualdade exata com `kernel_incremental_evidence.json`; 35 alvos GNS cumulativos, sendo 21 novos nesta revisão e 14 anteriores. |
| Gate e runtime | Seis flags maiores `false`; `legacy_gate_changed=false`; `full_plan_complete=false`; runtime `false` | Registros finais, AST e bytes do helper inspecionados; não constituem autorização de runtime ou fechamento do gate. |

**Correspondência da integração.** Os oito DEV finais são iguais às fontes TGLExt e aos textos embutidos após a única tradução `import TGLV350.` → `import TGLExt.V350`. Não foi necessária normalização adicional de finais de linha. As duas raízes importam os oito módulos; em relação ao snapshot custodiado anterior só esses oito arquivos foram acrescentados ao dicionário e só as duas raízes anteriores mudaram. Os quatro desenvolvimentos posteriores estão ausentes do dicionário e das referências embutidas.

| Módulo integrado TGLExt/V350 | SHA256 da fonte integrada |
|---|---|
| ScalarGNSOrbit | `0acfc1da712e3ee99a19f3ddc63355fa26038d1841e9d54ceeec385ee4b045d2` |
| ScalarGNSLinear | `1e2708f65d937e7529792d690ff989806064336a5dc1eba886aabf2f174f0562` |
| ScalarGNSAction | `529982d9d3489dd900c8259599cede7cbf866525e4001e8196054679fae8f65a` |
| OperatorFieldAlgebra | `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d` |
| ScalarGNSCompletion | `f2bff58e02c1e454c7832b51c0b8712816bd3f6c0e99f91f67811dd007d9771b` |
| DualOrbitRepresentation | `01d61dbe3b2f4193dc48b345a1e765f017964a73a9e05070bf4e34e0510753dd` |
| ReducingStarRepresentation | `79a0c03282c1328f5b4d6963242a3ee1737a11c12353cec5f8244a5030b5f2fa` |
| ScalarGNSRepresentation | `4f30495b0f3531889367a9b8b2754f7ec561dbc5e5460f8b4c3f63cf9d19347d` |

Os dez logs novos, seus timestamps, stdout/stderr e hashes estão preservados no snapshot [final_integrated_20260912_073812_180579](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073231_721305/final_integrated_20260912_073812_180579>). Em todos os dez registros a fonte permaneceu inalterada durante a compilação; não há warnings nesses dez stdout. Os resultados não autorizam extrapolar a reprodução binária própria para as raízes ou toda a biblioteca. A igualdade byte a byte **própria × autoral** afirmada neste parecer refere-se aos cinco .olean DEV medidos, com a herança explicitada no primeiro estrato.

**Python e controle novo.** A AST de `um.py`, excluída somente a atribuição `_EMBEDDED_KERNEL_FILES`, é idêntica à da cópia anterior pinada por `modular_domain_custody.json` (`6d1c9ba4f585fd507e4db6edc8464e97076e0f68938104c84c697adee80ffa60`). `gate_extension.py` é byte a byte idêntico, SHA256 `c819810b5540747f0a0b7b07b36bb9d7f5e9dd868192ad7410ea15829c566a9e`. O único controle acrescentado é `finite_ideal_GNS_representation_does_not_discharge_Tomita_KMS_trace`, em `test_gate_extension.py:331`: exige a presença de oito declarações representativas e a manutenção das seis flags falsas. É um controle de fronteira e presença de evidência, não uma prova de Tomita/KMS/traço. Removida apenas essa chamada nova, a AST inteira do teste coincide com a anterior; nenhuma chamada antiga foi alterada ou removida. A contagem sintática de chamadas literais passa de 34 para 35, distinta dos 68 controles gerados/executados pelo autor.

**Minuta e recorder finais.** A minuta permanece idêntica ao pin já lido; seu relato distingue a completude de H_I, a fidelidade provada e as obrigações abertas. O recorder e o verifier atualizados foram lidos estaticamente, inclusive o adendo posterior, e ambos passam `ast.parse`. O recorder usa backup binário imediato e append preservando prefixos, substituição por temporário verificado, pin do parecer GNS_ORBIT e validação de fontes/binários/AST; o verifier confere esses hashes e os prefixos. Nenhum dos dois foi executado nesta revisão, portanto não há aqui atestado de custódia já produzida ou de execução futura bem-sucedida.

A nota adicionada pelo autor separa nominalmente quatro módulos posteriores/14 alvos em `post_scope_development`, com `independently_reviewed=False` e `integrated=False`, sem somá-los aos oito/35 deste registro. Conferi somente essa separação de estatuto e a ausência no pacote embutido. **Não revisei os enunciados, provas, logs ou binários desses quatro módulos**, nem a rota posterior; as afirmações matemáticas dessa nota permanecem [DECLARADO — autor, fora desta revisão]. A presença da nota não certifica densidade por I∩I* ou gráfico de Tomita neste parecer.

O inventário I/O é explicitamente histórico: hash `34133956b6a47012805003adfae734e7439b27e1f611466829af624b1857d89c`, fonte histórica `c712532dc079b832d9eb1ecc26ea50f2d49aa2c387afa435cc777eb302e96e09`, ambos comparados aos campos históricos da custódia anterior. Essa comparação não o transforma em inventário da cópia atual nem em liberação de execução.

| Artefato final lido | SHA256 |
|---|---|
| integration.json | `62a2a44df4f2cc3c73916602e4c4b4b898c3dd8b510b117abb244998adef369f` |
| integrated_compile.json | `cf654dae0212bc062fc051777ccea46d124f044c09f0a5e907f783addee3f9a0` |
| gate_tests.json | `27a65c438c2bfe00268000497ed0bdcfe96a917136ff5157c5508536a197b22e` |
| kernel_incremental_evidence.json | `1599d6e88ea84dde28498db34216c458bc757ebbafa056748cbcb37879ea64ff` |
| MINUTA_REPRESENTACAO_GNS.md | `07a0acbf059d5ade55c6a949c265cf4df42b4728d93b67fbe16f1411a35bd415` |
| record_gns_representation_progress.py | `482e2e7a6771500cab1a360f184f8a497a83aab0ef9907f94f09ebaf63dfb967` |
| verify_gns_representation_custody.py | `62244aa099b9f16c89abcaf82e78dc739f4f98ce66059ede49c9dbccbfc74f0f` |

Evidência de inspeção: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073231_721305/final_integrated_20260912_073812_180579/verification.json>), [supplemental_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073231_721305/final_integrated_20260912_073812_180579/supplemental_verification.json>); evidência de execução própria: [verification_dev.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_representation5_independent_20260912_073231_721305/verification_dev.json>) e os dois `compilation.json` ligados acima. Todos os arquivos finais pinados foram reconferidos antes deste append. O parecer anterior GNS_ORBIT e os demais pareceres permanecem byte a byte preservados.

**Conclusão verificável:** representação complexa unital fiel da mesma N sobre o fecho H_I da inscrição do ideal I, com imagem densa, entrelaçamento e cota de norma. Nenhuma análise necessária dentro dos cinco módulos/21 alvos ficou pendente. A integração dos oito/35 foi conferida pelos meios descritos; controles/raízes são evidência autoral inspecionada. Permanecem os limites de domínio máximo, normalidade, Tomita/KMS/traço, gate e runtime já delimitados. Escopo encerrado; sem extensão às fontes posteriores.

Preservação deste parecer: prefixo anterior de 13081 bytes, SHA256 `301ce895b03addb744690a13b8043234bbc85d9a46b114f18183e0c3dfb716ad`, guardado imediatamente em [REVIEW_GNS_REPRESENTATION.md.bak_20260912_074103_160470](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_GNS_REPRESENTATION.md.bak_20260912_074103_160470>) antes do append. Pareceres custodiados anteriores não foram tocados.
