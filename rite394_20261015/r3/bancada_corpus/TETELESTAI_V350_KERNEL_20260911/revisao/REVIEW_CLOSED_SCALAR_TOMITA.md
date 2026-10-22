# Revisão independente — operador escalar de Tomita fechado

2026-09-12T10:06:20-03:00. **DEV concluído, sem achados P0–P2.**

[REAL — leitura integral e recompilação própria] Foram lidos os dois módulos finais, o relatório autoral e toda a dependência existente `TGLExt/ClosedAntilinearStandardSubspace.lean`. **Dois DEV + auditor próprio passaram rc0**, com os 24 tipos e 24 conjuntos de axiomas conferidos. Somente `propext`, `Classical.choice`, `Quot.sound`; os dois `.olean` próprios coincidem byte a byte com os autorais pinados. A dependência genérica também foi recompilada separadamente em árvore própria, rc0, para evitar uso de binário autoral de projeto. Nenhuma análise DEV necessária deste escopo permanece pendente.

O pacote constrói uma aplicação antilinear S no domínio denso D do **fecho do gráfico original**, prova igualdade de seu gráfico com esse fecho, invariância do domínio, involução e extensão da estrela do núcleo I∩I*. Constrói no mesmo H_I o subespaço real padrão K=Fix S, com D=K+iK e S(h+ik)=h−ik. Não identifica K com Fix J, o domínio com n_ν ou os dados polares/KMS do peso.

## Domínio, escolha e gráfico

**Objetos preservados.** H_I é `ScalarGNSHilbert P`, o subespaço fechado anterior do L² de órbitas. `scalarTomitaGraph P` continua a imagem de A∈`finiteDualStarCore P` pelo par `(scalarGNSStarEmbedding P A, scalarGNSStarEmbedding P (star A))`. Essa declaração herdada mantém fonte `712984b79b495de57936720ba4e39785947af20c28f5342709404409f110dae0` e binário próprio `01c56a31cc47591d9eb7fed8a355efc666e069ae3fea3f56c5904ed31334dc62`. Não foi reconstruída com outro espaço, vetor, peso ou ideal. A fechabilidade/univalência usada é a do pacote gaussiano anterior, conferido separadamente; não é uma nova premissa colocada sobre P.

**Instâncias locais — [ScalarClosedTomita.lean:12](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarClosedTomita.lean:12>) (12–24).** `scalarStarCoreAdd` usa o `AddCommGroup` do `NonUnitalRing` herdado da subálgebra sem unidade. `scalarStarCoreSMul` aplica c ao operador subjacente e usa `smul_mem` para recolocá-lo no subtipo. Essas são as operações do subobjeto; não alteram adição ou escala no H_I. Os lemas de inscrição reduzem às leis `map_add` e `map_smul` da mesma Λ sobre I. As identidades de estrela em zero, soma e escala são verificadas por `Subtype.ext` no operador subjacente. As duas instâncias são locais, não axiomas; seus usos são cobertos transitivamente pelos alvos auditados. Não foram contadas como dois novos alvos além dos 24 solicitados.

**Estrutura do gráfico — [ScalarClosedTomita.lean:26](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarClosedTomita.lean:26>) (26–85).** A inscrição de zero, a aditividade e a lei de estrela dão a estabilidade do gráfico por soma e por **(x,y)↦(cx,conj(c)y)**. Não se trata o gráfico antilinear como um subespaço complexo com escala idêntica nas duas coordenadas. O conjugado é efetivamente `starRingEnd ℂ`.

A aditividade do fecho é provada em duas aplicações de `closure_minimal`, fixando alternadamente cada somando e usando continuidade da adição. Escala conjugada e swap passam ao fecho pela continuidade das aplicações correspondentes no produto H_I×H_I. Não se invocam continuidade de S, limitação de S ou fechamento prévio do domínio.

**Domínio e escolha — [ScalarClosedTomita.lean:88](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarClosedTomita.lean:88>) (88–117).** O carrier de D é exatamente

`{x : H_I | ∃ y : H_I, (x,y) ∈ closure (scalarTomitaGraph P)}`.

As operações de submódulo complexo em D são construídas a partir das testemunhas no fecho: y+w para x+z e conj(c)y para cx. `Classical.choose x.property` é aplicado a uma existência contida no tipo de x; `choose_spec` prova que o valor escolhido está sobre x no fecho. Não há escolha em um conjunto possivelmente vazio.

`scalarClosedTomita` tem tipo **D→ₛₗ[starRingEnd ℂ]H_I**, uma aplicação semilinear, não uma CLM. As leis de soma e escala são demonstradas comparando dois pontos do fecho com a mesma primeira coordenada e aplicando a univalência já provada. Assim a escolha não introduz uma hipótese de linearidade nem ambiguidade no valor de S.

**Igualdade de gráfico e fechamento — [ScalarClosedTomita.lean:119](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarClosedTomita.lean:119>) (119–147).** A inclusão do gráfico de S no fecho decorre de `choose_spec`. Para o sentido inverso, de p=(x,y) no fecho constrói-se x como elemento de D usando y como testemunha; a univalência obriga Sx=y. Portanto a igualdade é efetiva:

`range (fun x : D => ((x : H_I), S x)) = closure (scalarTomitaGraph P)`.

O fecho é tomado no produto **H_I×H_I**, com a primeira coordenada incluída no ambiente, e não apenas no produto do domínio com H_I. Da igualdade segue `IsClosed` desse gráfico ambiente. A densidade de D vem da inclusão do domínio inicial denso no domínio do fecho. Não se declara D=H_I, D fechado ou D completo; não se aplica indevidamente o teorema do gráfico fechado para obter limitação de S.

**Involução e extensão — [ScalarClosedTomita.lean:149](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarClosedTomita.lean:149>) (149–168).** O swap de (x,Sx) fornece (Sx,x) no fecho, daí Sx∈D. A univalência na fibra sobre Sx dá S(Sx)=x, com a pertinência de Sx ao domínio explicitamente carregada no subtipo. É uma involução no domínio invariante, não uma operação definida em todo H_I. Para A∈I∩I*, o par inicial pertence ao fecho; isso fornece Λ(A)∈D e, novamente pela univalência, SΛ(A)=Λ(A*). Não se substitui I∩I* pelo domínio escalar máximo.

## Dependência genérica e subespaço padrão

A dependência [ClosedAntilinearStandardSubspace.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/ClosedAntilinearStandardSubspace.lean>) foi lida inteira, inclusive suas provas de linhas 44–221. O cabeçalho contém história de outras entregas; essas contagens e interpretações não foram tomadas como nova evidência deste pacote. Os passos utilizados são:

| Trecho da dependência | Conferência |
|---|---|
| 48–86: `fixedRealSubmodule`, `fixedRealSubmodule_closed`, `fixedClosedSubmodule` | Fix S é um submódulo **real**, com condição x∈D explícita. Sua fechadura vem da preimagem diagonal x↦(x,x) do gráfico fechado ambiente; não exige D fechado. A escala real é compatível porque o conjugado de um real é ele mesmo. |
| 89–139: `domainConjugation`, `domain_fixed_decomposition` | A hipótese de domínio invariante permite codrestringir S a D. Com involução, h=(x+Sx)/2 e k=−i(x−Sx)/2 são fixos; o cálculo usa conj(−i/2)=i/2 e dá simultaneamente x=h+ik e Sx=h−ik. Os sinais e o fator 1/2 são algébricos. |
| 141–158: `mem_domain_iff_fixed_sum`, `fixed_sum_tomita` | As duas inclusões de D=K+iK são efetivas. A volta usa h,k∈D e o fato de D ser submódulo complexo; a ação em h+ik vem da antilinearidade e dos valores fixos. |
| 160–185: `fixed_subspace_separating` | De x∈K∩iK, antilinearidade e as duas condições de fixação dão ix=−ix, logo x=0 porque 2i≠0. Não há operador J ou hipótese polar nessa prova. |
| 187–221: `fixed_subspace_cyclic`, `closedAntilinearStandardSubspace` | A decomposição inclui D no supremo de K e iK no reticulado de submódulos reais fechados; a densidade de D obriga esse supremo a ser todo H. As quatro hipóteses usadas são gráfico fechado, domínio invariante, involução e densidade. |

As linhas 178–184 da definição instalada de Mathlib `Analysis/InnerProductSpace/StandardSubspace.lean` também foram consultadas: a estrutura contém `toClosedSubmodule : ClosedSubmodule ℝ H`, `IsSeparating : K ⊓ K.mulI = ⊥` e `IsCyclic : K ⊔ K.mulI = ⊤`. O supremo aqui é de **submódulos fechados**. Assim a propriedade cíclica diz fecho(K+iK)=H; não diz que a soma algébrica já é fechada ou igual a H.

**Aplicação aos mesmos D e S — [ScalarTomitaStandardSubspace.lean:12](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaStandardSubspace.lean:12>) (12–39).** As quatro hipóteses genéricas são fornecidas pelas quatro provas concretas do primeiro módulo. O tipo impresso é `StandardSubspace (ScalarGNSHilbert P)`. O teste de pertinência é definicionalmente `∃ hx:x∈D, S⟨x,hx⟩=x`, de modo que K é Fix **S** no mesmo H_I. Os teoremas seguintes dão D=K+iK como soma algébrica e a decomposição conjunta x=h+ik, Sx=h−ik. Não se muda de Hilbert, não se insere um antiunitário J e não se usa identificação modular do peso para preencher algum campo.

## Alvos e evidência própria

| Módulo | 24 alvos novos conferidos |
|---|---|
| ScalarClosedTomita | `scalarGNSStarEmbedding_add`, `scalarGNSStarEmbedding_smul`, `scalarTomitaGraph_zero`, `scalarTomitaGraph_add`, `scalarTomitaGraph_conj_smul`, `scalarClosedGraph_add`, `scalarClosedGraph_conj_smul`, `scalarClosedGraph_swap`, `scalarClosedTomitaDomain`, `scalarClosedTomitaValue`, `scalarClosedTomitaValue_graph`, `scalarClosedTomita`, `scalarClosedTomita_graph`, `scalarClosedTomita_graph_eq`, `scalarClosedTomita_is_closed`, `scalarClosedTomita_domain_dense`, `scalarClosedTomita_maps_domain`, `scalarClosedTomita_involutive`, `scalarStarCore_mem_closedTomitaDomain`, `scalarClosedTomita_extends_star` |
| ScalarTomitaStandardSubspace | `scalarTomitaStandardSubspace`, `scalarTomitaStandardSubspace_mem`, `scalarClosedTomitaDomain_fixed_sum`, `scalarClosedTomita_fixed_decomposition` |

Árvore principal: [closed_scalar_tomita_independent_20260912_100020_793911](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_scalar_tomita_independent_20260912_100020_793911>). Ela usa **399 dependências de projeto pinadas**: 398 reaproveitadas da árvore gaussiana própria [gaussian_closability_independent_20260912_094053_879658](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gaussian_closability_independent_20260912_094053_879658>), mais a dependência genérica recompilada nesta revisão. A árvore dessa recompilação é [closed_antilinear_dependency_independent_20260912_095836_800005](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_antilinear_dependency_independent_20260912_095836_800005>). Seus 12 `#print axioms` existentes ficaram no trio; não são somados aos 24 alvos novos.

Genérica recompilada: fonte `a90532fc36bb1eb4310885a94159e3bac3d59a919b421976d498fffa2015ecb8`, `.olean` próprio `bffe7c1851d8259440ed741d1e7a3742c7f6e5102739fc34129730b2bd78f23e`. Esse mesmo `.olean` foi copiado para o build principal e seu hash conferido. Registro próprio: [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_antilinear_dependency_independent_20260912_095836_800005/compilation.json>), SHA256 `3be5a53b080ff87084b7ad43f75b98a03195233d35963c2e52266691980bd0d2`. Não se utilizou o binário autoral dessa dependência.

O `LEAN_PATH` principal tem somente seu build de projeto, seguido de oito caminhos de pacotes externos readonly. O build genérico também é próprio; pacotes/compiler foram apenas lidos. Nenhum build autoral de projeto integrou a resolução de módulos. TMP/TEMP são próprios. Compilador: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`, SHA256 `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`. Não houve rebuild de bibliotecas ou dos módulos cíclicos/gaussianos anteriores.

Permanece a exceção histórica de comentário em `DualSemifiniteIdeal`: fonte própria `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`, binário herdado `6a242f29df8816cf7e741cb043f6c24f88fb9e844fc60f90d3bce25a4c1f26df`, fonte autoral atual `f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3`. A diferença literal foi novamente conferida como somente a errata documental já revisada. As limitações binárias herdadas permanecem as dos pareceres anteriores; a coincidência com os binários autorais aqui declarada é a dos dois DEV novos.

| Módulo DEV | Alvos | SHA256 fonte final lida | SHA256 `.olean` próprio = autoral |
|---|---|---|---|
| ScalarClosedTomita | 20 | `d13e11274b04a3d87b6baad0002075f93bcd2f41222912494db6d7e4540c4668` | `93fd61ead70b6b89bd2788c2b77909d99e93d8a92a06172db1d2a09db0891a99` |
| ScalarTomitaStandardSubspace | 4 | `80aa5210897ad0615d26c51c8978eb150f6d720752830c5e532553ebb10669e1` | `1ff96eca53513727cecf92cb1fa416b56cf54793f949a61a250f803b8039d89f` |

| Processo executado nesta revisão | rc | Segundos |
|---|---|---|
| TGLExt/ClosedAntilinearStandardSubspace.lean | 0 | 17.89 |
| TGLV350/ScalarClosedTomita.lean | 0 | 55.616 |
| TGLV350/ScalarTomitaStandardSubspace.lean | 0 | 32.352 |
| ClosedScalarTomitaAudit.lean | 0 | 30.672 |

Total: **quatro processos próprios**, incluindo a genérica, os dois DEV e o auditor. Todos ficaram sem warnings e com stderr vazio. Auditor novo: fonte `220e47425df63cc44f68fbe9708001f298a80caa5b78272551a55c0bc130b48d`, `.olean` `318091dded073d2f3cfa459ba5cdd10a6451d94c15f39fe64ba960bc3eecb1d0`, stdout `3d828855988ffb89a175a929b133049e4f07e02e037ae4fa406c2e879a43b06c`. Os 24 `#check` com universos e os 24 `#print axioms` cobrem exatamente a lista do status, sem pressupostos adicionados ao auditor. Nenhum `sorryAx` ou axioma fora do trio apareceu.

| Log autoral final inspecionado | SHA256 JSON |
|---|---|
| [ScalarClosedTomita_20260912_095107_652662.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/ScalarClosedTomita_20260912_095107_652662.json>) | `d6c6b6e3bb5df3769a15b028e119d4070bfc02ba13263add555c461a78007b77` |
| [ScalarTomitaStandardSubspace_20260912_095352_511239.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/logs/ScalarTomitaStandardSubspace_20260912_095352_511239.json>) | `bb85a90ce6714f854a91bee70e10e6cb5daa301ff8ee49aa4f9b982923d3e6b3` |

Fontes, binários, logs JSON e streams autorais foram comparados aos pins e aos snapshots. Os logs aceitos registram rc0 e fonte inalterada; tentativas autorais anteriores não foram apagadas nem usadas como êxito. **Execução própria** em [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_scalar_tomita_independent_20260912_100020_793911/compilation.json>); **hashes e comparação com o autor** em [verification_dev.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_scalar_tomita_independent_20260912_100020_793911/verification_dev.json>); **deps, comandos e LEAN_PATH** em [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_scalar_tomita_independent_20260912_100020_793911/manifest.json>); **tipos e axiomas completos** em [ClosedScalarTomitaAudit.stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_scalar_tomita_independent_20260912_100020_793911/logs/ClosedScalarTomitaAudit.stdout.txt>). Nenhum teste, recorder, integrador ou monólito autoral foi executado/importado.

A leitura de todas as fontes e a inspeção adicional [source_structure.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_scalar_tomita_independent_20260912_100020_793911/source_structure.json>) conferem as duas instâncias locais e somente as opções `autoImplicit`, `linter.unusedSectionVars`, `maxHeartbeats`. Não há `axiom`, `sorry`, `admit`, declaração `unsafe`, atributo de redutibilidade ou relaxamento de transparência nos novos arquivos. Essa inspeção é complementar à recompilação e à auditoria transitiva de axiomas.

## Documentação, preservação e limites

`RELATORIO_TOMITA_FECHADO_DEV.md` foi lido integralmente, SHA256 **`67adbf7ff16b18e3a7d56b38311daf233aa67d7f5f180010af1984cfea311eb0`**, igual ao pin e ao snapshot. Suas afirmações sobre D, escolha, antilinearidade, fecho, involução, extensão, Fix S e soma K+iK correspondem às provas. Os limites relativos a Fix J, domínio máximo e dados polares estão corretamente explicitados. Nenhum P2 documental encontrado; o estatuto de revisão pendente é o do arquivo congelado antes deste parecer.

Status `tomita_closed_draft_status.json`: `430e3f3510251cb4458bfc8d95483a7d0ec95861403370deebcb3d5576b904e8`. Parecer gaussiano pai `820d2eb7704c8c908b12a9c8bc008cda5df2d59355208a2749e72b569285b6e2` e status gaussiano `6edb15f067e2e5496160b0cc455d23b4766d2f332866c664bbcbfe0c850c7849` coincidem com os pins. A custódia integrada anterior `gns_cut_maps_custody.json` permanece `45b4c37be83bdff179e7e451a06cc5150e1c2d9a40052e0639ce919174ee5e57`. As contagens **103/72/6357** e a cópia `93755159fdd0832132c3992cd38715e6940ce62602ac7c527d2bb1ba36f1a643` são do estrato integrado anterior, lido da custódia; o hash da cópia foi conferido novamente ao encerrar. Não houve inspeção de integração nova ou soma destes DEV àquelas contagens.

Os 29 pareceres anteriores mantiveram seus hashes, inclusive os cíclicos e gaussianos ainda aguardando integração. Fontes autorais, originais, monólito, memórias, status e custódias permaneceram intocados. Todas as saídas foram gravadas em `revisao/`.

**Conclusão delimitada:** dois módulos/24 alvos e a dependência genérica conferidos, com recompilação própria, sem P0, P1 ou P2. Está construído S antilinear, fechado e densamente definido no domínio do fecho do gráfico original, involutivo no domínio invariante e estendendo a estrela de I∩I*. K=Fix S é um subespaço real padrão do mesmo H_I; D=K+iK e S(h+ik)=h−ik. Não se concluem I=n_ν, identificação de domínio máximo, adjunto/decomposição polar modular, Fix J, KMS, traço, escala física, Three Locks/H1–H3, consumo pelo gate ou runtime. **Nenhuma análise DEV necessária resta neste escopo.**


## INTEGRATED_CLOSED_SCALAR_TOMITA_REVIEW — 2026-09-12T10:27:00-03:00

**[REAL — revisão integrada delimitada concluída; nenhum achado P0, P1 ou P2.]** Este adendo cobre os mesmos 15 módulos/99 alvos: cíclicos 4/26, gaussianos 9/49 e operador fechado/subespaço padrão 2/24. Preserva integralmente o parecer DEV acima e herda as análises matemáticas dos três pareceres. Não acrescenta resultados de módulos posteriores.

**Escopo efetivo da execução própria.** Recompilei novamente as **15 fontes DEV congeladas e um auditor próprio: 16 processos rc0**, com 99 `#check` (universos explícitos) e 99 `#print axioms`. Os 99 tipos impressos coincidem com os auditores próprios anteriores, e os 15 binários DEV coincidem byte a byte com as recompilações próprias anteriores. Todos os alvos usam apenas `propext`, `Classical.choice`, `Quot.sound`. Esta execução usa os nomes de módulo **TGLV350**: a versão **TGLExt/V350**, seus binários e as duas raízes foram conferidos por transposição literal, leitura de logs e hashes; **não foram recompilados pelo revisor com os nomes integrados**. A distinção vale também para as contagens autorais abaixo.

O ambiente reutilizou 394 dependências de projeto congeladas da árvore própria e oito pacotes externos somente leitura; nenhum build autoral de projeto entrou no `LEAN_PATH`. Fontes e binários herdados, sua proveniência e as limitações anteriores permanecem explicitados no manifesto. A errata de comentário de `DualSemifiniteIdeal` continua a exceção histórica documentada; não houve recompilação global de bibliotecas nem nova certificação dos binários herdados. Compilador: `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f` (Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)).

Evidência própria: [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_tomita_batch_independent_20260912_101455_759612/manifest.json>), [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_tomita_batch_independent_20260912_101455_759612/compilation.json>), [comparação dos 99 tipos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_tomita_batch_independent_20260912_101455_759612/type_comparison.json>) e [auditor completo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_tomita_batch_independent_20260912_101455_759612/logs/ClosedTomitaBatchAudit.stdout.txt>). Fonte do auditor `bdf682eb45893f316cf7ca6431449bf0df258f55f8b78f16cddd9ae698ab6e73`; binário `a5c2e5ee96b748599850c6c13c6f34ec948c04b99d12385078ca8fb1db3ff9db`; stdout `9f31ae1109d99e43293a51f1016ab4756b0b26caaa0a120102eb0d40344e0b48`. O manifesto registra hashes das três execuções anteriores reaproveitadas; nenhuma aprovação foi inferida apenas dos nomes.

**Transposição e mesmo objeto.** Nos 15 arquivos, a diferença byte a byte é exclusivamente `import TGLV350.` → `import TGLExt.V350`. Não mudou enunciado, hipótese, universo, definição, prova ou instância local. As fontes integradas coincidem com as strings incorporadas no monólito. Só foram acrescentados 15 arquivos; entre os arquivos antigos, só mudaram `TGLExt.lean` e `TGL/Audit.lean`. Cada raiz importa os 15 exatamente uma vez, e o Audit acrescenta exatamente os 99 alvos sem retirar os anteriores. Evidência: [inspeção de fontes, roots e AST](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_tomita_batch_independent_20260912_101455_759612/source_integration_20260912_102052_281772/verification_source.json>) e seus diffs congelados.

| Módulo integrado (TGLExt/V350) | Alvos | SHA256 fonte integrada |
|---|---:|---|
| ScalarCutVacuum | 4 | `524ca91fbe926c9cca9d556da92933d7b1ba037cf57dfd572250a7f12770c24e` |
| ScalarCutCyclicSpace | 13 | `6b80dd3a58161b692c3cf4679c899c4205446b233b7b3ceda60e79da045f6091` |
| ScalarCutVectorFunctional | 2 | `a5f8006dc3fd6a845e1a43f2cc421395bbd1cd8a8d27401530a68e9e854d4cc2` |
| ScalarCutGNSProperties | 7 | `89c398c46a2829e3c0ceb1134481af2792a330ba73efedf8679754bbf9d3e7cb` |
| L2PositiveMultiplier | 6 | `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf` |
| L2GaussianProfile | 5 | `b310c30ec1a4d69f637b358ccbd9a48dd73436d06368e5796a6139e8b167f5fb` |
| FibreVonNeumann | 4 | `48ba27a3b9701bc7c6dfb1b28128fbc10d00cec335cf24f4d3be27d0041eb5a8` |
| ScalarGaussianVacuum | 4 | `550fae23297d4b225ac9ac12c04221195afdf973fdebdb8e04045f0d948ac565` |
| SeparatingCyclicCommutant | 6 | `b7abd60e1dc54dde28cce905cbbac547eac88b807af52c6d0989e321de21c9a2` |
| DualOrbitVonNeumann | 9 | `b00ffd7618a281ddb9cd74f01418de030e0ec6ffdaf2ff54fa195a4e175bad67` |
| ScalarGaussianGNSMap | 5 | `bc00455275254f92ab3b7405a23ba41351680e80c65608ed81475cf2d1dadb7d` |
| VectorTomitaClosability | 5 | `cc8e1c704d6eea35a5415c6650d89c7cee048504d5e388b347df14a3c697e703` |
| ScalarGaussianClosureTransport | 5 | `cb0e7921903f4e77bf08baef2791c98d3220c3ce8e13ee5478de5a8b06a266ae` |
| ScalarClosedTomita | 20 | `4d87af66ab6aecfe92e0c53db83c324d649c32b15016190f3a5b07f5cccc8c8f` |
| ScalarTomitaStandardSubspace | 4 | `ff5c152c886b3824064722677b62ddc0349df7d7f43cae79a7ee060d75b221c9` |

**Snapshot autoral final inspecionado.** Cópia `4309a3cc34b3e8360872e1c49ff78334c422359df1eb4cfa45890084abee15f8`, **820 arquivos incorporados**. `integrated_compile.json` contém **118 registros rc0: 101 herdados com fonte/binário iguais ao estrato anterior e 17 compilações novas (15 módulos + 2 raízes)**. Conferi hashes atuais de fontes/binários, os JSON originais dos logs, streams e fonte inalterada durante as 17 compilações novas. Estas contagens descrevem a execução autoral lida, não 118 recompilações próprias.

| Raiz compilada pelo autor | Identificação do log final | SHA256 .olean lido |
|---|---|---|
| TGLExt.lean | `20260912_101813_443925` | `73588a125c1dd4b749fd2410f78f73dbf161461559747f592b0ad9839c0d2296` |
| TGL/Audit.lean | `20260912_101845_331425` | `37126c7121b019069cdb42f484f82b1a85dc8e92d9cc44b9f41e1082917c1144` |

O stdout do Audit contém **6456 declarações distintas**, todas no trio; coincide com `kernel_incremental_evidence.json`, e os 99 alvos novos coincidem com o auditor próprio. `gate_tests.json` registra **75/75 controles aprovados**; os três acréscimos são `cyclic_cut_GNS_does_not_discharge_KMS_trace_or_physical_frontier`, `Gaussian_closability_does_not_discharge_KMS_trace_or_physical_frontier` e `closed_Tomita_and_standard_subspace_does_not_discharge_KMS_trace_or_physical_frontier`. O único acréscimo no AST do teste é o laço desses três controles; as instruções anteriores permanecem iguais e na mesma ordem. Não executei esses testes nem as raízes.

O AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com a cópia custodiada `93755159fdd0832132c3992cd38715e6940ce62602ac7c527d2bb1ba36f1a643`; `gate_extension.py` permanece byte a byte igual. As seis flags maiores continuam falsas, `legacy_gate_changed=false`, `full_plan_complete=false` e `full_runtime=false`. Original relido e igual à cópia-base/pin: `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`. Evidência final e todos os hashes de fontes, logs, streams e documentos: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_tomita_batch_independent_20260912_101455_759612/final_integrated_20260912_102641_100736/verification.json>). Não executei/importei monólito, integrador, testes, recorder ou verifier autorais.

**Minuta e custódia: inspeção estática dos bytes finais.** Li o texto interpolado de relatório/memórias de `record_closed_tomita_progress.py`, SHA `8fc1737407ef74a54d7d8763f1e44455d8df1dbac165c8abbaabac767b3438a0`, e o mecanismo de `verify_closed_tomita_custody.py`, SHA `ab61a213a02251be39c386186d6ef028773eeb01c9e2721c0cd83ab15487ff4c`. A redação preserva H_I, o gráfico original, a injetividade de T sem inversa limitada, Fix(S) e D=Fix(S)+iFix(S); não promove esses resultados a Fix(J), identificação polar, KMS, traço ou consumo pelo gate. O comentário documental de H2/PyCBC foi confrontado apenas com a interface nomeada no original; não foi realizado rito físico.

Os scripts preveem backup imediato de bytes, append e registro do hash do estado imediatamente anterior, inclusive mudanças intervenientes nas memórias compartilhadas. O verifier compara os prefixos/bytes atuais e documenta a diferença perante a custódia anterior; não presume imutabilidade dessas memórias desde 09h12. Esta é leitura de código, **não execução nem confirmação antecipada da futura custódia**. `ROTA_APOS_TOMITA_FECHADO.md`, SHA `b4356029ff29b98aeb7044d17bb369262bb50e9dc6ace5ce72934a09c76aa8a3`, fica somente pinada como roteiro posterior sem prova nova; a marca de que I=n_ν não é uma obrigação automática está explícita. Suas propostas não foram incluídas na revisão matemática dos 99 alvos. O inventário I/O segue histórico e não fornece liberação de runtime.

**Conclusão e limites herdados.** O pacote integrado conserva as provas DEV: cortes cíclicos com injetividade conjunta; fecho univalente do gráfico original no mesmo H_I; S antilinear fechado, densamente definido e involutivo no domínio; K=Fix(S) padrão real e D=K+iK. Não se presume I=n_ν, fidelidade/separação de cada corte, inversa gaussiana limitada ou troca de representação. Identificação com o domínio/core adequado do peso, adjunto e decomposição polar modular, KMS, traço canônico/escala dual, Three Locks/H1–H3, física, certificado consumido e runtime permanecem fora da conclusão. **Nenhuma análise necessária resta neste escopo de integração.**

Preservação: o prefixo DEV de 18327 bytes, SHA `a0ffd70ffb62a2b70d920ed95f4c8cc07c7f5e54198890945ad14d44e1569054`, foi guardado em backup imediato exato antes deste append. Os demais pareceres, fontes, originais, logs e memórias não foram alterados. Todas as saídas do revisor permanecem em `revisao/`.
