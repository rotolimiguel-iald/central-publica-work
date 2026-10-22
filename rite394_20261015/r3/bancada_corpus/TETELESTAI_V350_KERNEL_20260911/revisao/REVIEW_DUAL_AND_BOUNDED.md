# Revisão adversarial independente — ação dual, limites fortes limitados e adendo WOT

Fechamento: 2026-09-11T21:37:13-03:00. Bancada: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911`. Escritas restritas a `revisao`.

**[REAL — fontes, recompilação e auditoria independentes] Parecer favorável aos quatro módulos solicitados e ao adendo `RegularTopology`, nos enunciados efetivamente provados. Nenhum defeito concreto P0–P3 identificado.** `Ad(Dₛ)` restringe-se a um automorfismo da álgebra gerada inteira, fixa a inclusão do fator e satisfaz Weyl com sinal negativo e lei de grupo. A amplificação preserva limites fortes sob cota global uniforme para filtros arbitrários. O adendo prova bicomutante ⇒ fechado em WOT.

**Escopo:** esses resultados não fornecem, por si só, certificado de core tracial, traço canônico, Three Locks ou QG. Nenhum gate adicional foi habilitado. O parecer anterior [REVIEW_MODULAR_AND_REGULAR.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_MODULAR_AND_REGULAR.md>) permanece byte a byte intacto.

## Achados priorizados

**Nenhum achado corretivo demonstrado nos cinco módulos.** Foram especificamente examinados: inversão do sinal da fase, ordem de composição de automorfismos, restrição só sobre geradores, troca da realização/Hilbert, omissão da cota uniforme, redução indevida a sequências e confusão entre WOT e norma de operador. A análise e as sondas abaixo não encontraram esses defeitos.

Ausência de normalidade formalizada, traço e demais contratos físicos não foi classificada como bug: não são conclusões reivindicadas por este pacote. Os limites de leitura são explicitados ao fim.

## Evidência independente e fronteira de confiança

| Módulo dev recompilado | Resultado | Declarações auditadas integralmente |
|---|---|---:|
| [L2CharacterMultiplier.lean:1](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2CharacterMultiplier.lean:1>) | exit 0 | 24 |
| [GeneratedEquivariance.lean:1](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/GeneratedEquivariance.lean:1>) | exit 0 | 6 |
| [RegularDualAction.lean:1](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularDualAction.lean:1>) | exit 0 | 18 |
| [L2BoundedStrongContinuity.lean:1](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2BoundedStrongContinuity.lean:1>) | exit 0 | 6 |
| [RegularTopology.lean:1](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularTopology.lean:1>) — adendo | exit 0 | 3 |

Os quatro módulos iniciais passaram **4/4** em uma árvore própria. `DualFullAudit.lean` passou e auditou **54/54 declarações**, incluindo auxiliares não impressos nas fontes standalone. O adendo passou **1/1**, e `TopologyFullAudit.lean` auditou **3/3** teoremas. Portanto, **57 declarações dos cinco módulos** foram verificadas independentemente com axiomas contidos em `{propext, Classical.choice, Quot.sound}`. Os hashes dos `.olean` produzidos foram reconferidos.

As **305 dependências de projeto** vieram dos binários congelados e da recompilação bem-sucedida da revisão anterior. Foram copiadas para a nova árvore e conferidas por SHA-256; suas fontes atuais coincidem com as fontes congeladas. Nenhum desses binários foi modificado durante a recompilação. Não se usou o build de projeto em mutação do implementador como fallback. Lean/Mathlib instalados continuam como base de confiança, lidos em modo somente leitura; não reconstruí nem recopiei integralmente Mathlib. Compilador: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`.

As quatro fontes dev e suas versões `TGLExt/V350*.lean` diferem apenas pelo prefixo de importação. O mesmo foi verificado para `RegularTopology`; os cinco conteúdos integrados conferem com o monólito. O monólito foi tratado apenas como dados/AST, sem execução ou importação.

**Sonda independente adicional:** [DualTypeBoundary.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/sources/DualTypeBoundary.lean>) passou, verificando conjuntamente (a) a fase negativa sobre o gerador já inserido como elemento da álgebra, (b) a inversa com tempo `−s` para qualquer elemento da álgebra, (c) a mesma inclusão fixada e (d) o lema sob `Filter ι` de universo arbitrário, sem topologia no índice e sem `NeBot`. A primeira tentativa atingiu o limite padrão de 200 mil heartbeats ao elaborar a inversa; a repetição com o orçamento de um milhão já usado nos módulos passou. Fonte, log e registro anteriores foram preservados em backups. Não houve mudança de prova na implementação.

## Conferência dos quatro módulos

### Multiplicador de caracteres e sinal de Weyl

[L2CharacterMultiplier.lean:21](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2CharacterMultiplier.lean:21>) define exatamente `characterPhase s x = exp(−i s x)`. `RegularHilbert H` continua sendo Lebesgue `Lp H 2 volume`, com `H` Hilbert complexo completo. As linhas 54–74 provam integrabilidade e preservação da norma antes de construir o operador no quociente quase em toda parte. As leis lineares, grupo, inversa e adjunto são verificadas nas linhas 76–148; `star Dₛ = D₋ₛ` é o adjunto de operador, não conjugação escalar aplicada a um objeto de outro tipo.

O cálculo escalar de [L2CharacterMultiplier.lean:46](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2CharacterMultiplier.lean:46>) é:

`exp(−i s x) · exp(+i s (x−t)) = exp(−i s t)`.

Isso paga precisamente [L2CharacterMultiplier.lean:160](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2CharacterMultiplier.lean:160>): `Dₛ Sₜ Dₛ* = exp(−i s t) • Sₜ`, para `(Sₜ f)(x)=f(x−t)`. A igualdade quase em toda parte da segunda fase é transportada pela translação preservadora de Lebesgue; não se pressupõe igualdade pontual de representantes de `Lp`.

[L2CharacterMultiplier.lean:179](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2CharacterMultiplier.lean:179>) usa convergência dominada dos coeficientes com majorante integrável `‖f(x)‖²`. A identidade da norma ao quadrado e a raiz quadrada dão continuidade forte na linha 206. O parâmetro é ℝ com sua topologia usual. Não há afirmação de continuidade em norma de operador.

### Transporte do bicomutante e restrição completa

[GeneratedEquivariance.lean:12](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/GeneratedEquivariance.lean:12>) trata as duas condições do **centralizador estelar** e usa injetividade do `StarAlgEquiv` para voltar. `centralizer_image`, linha 33, usa a inversa para pagar a sobrejetividade, requisito indispensável ao transporte de todo o centralizador.

[GeneratedEquivariance.lean:48](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/GeneratedEquivariance.lean:48>) transporta o bicomutante aplicando esse resultado duas vezes. A prova é algébrica; não pressupõe continuidade de um automorfismo abstrato para transportar um fecho topológico. `generated_maps_into`, linha 56, usa a minimalidade da álgebra gerada para estender a preservação dos geradores a **todos** os elementos.

[GeneratedEquivariance.lean:66](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/GeneratedEquivariance.lean:66>) exige preservação dos geradores tanto por `e` quanto por `e.symm`. Constrói ida, volta e ambas as inversas no mesmo subtipo da álgebra gerada. Esses dois pressupostos do lema geral estão explícitos e são efetivamente descarregados em `RegularDualAction`; não ficam como dívida do resultado final.

### Ação dual no mesmo objeto

[RegularDualAction.lean:18](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularDualAction.lean:18>) define o automorfismo ambiente por conjugação pelo unitário construído `Dₛ`. A fórmula na linha 23 é literalmente `Dₛ A Dₛ*`. `dualAmbient_add`, linha 30, considera corretamente que `(eₛ.trans eₜ)(A)=eₜ(eₛ(A))`; a comutatividade do grupo aditivo permite escrever `D_(s+t)=DₜDₛ`. Não há erro de ordem disfarçado na lei de grupo.

[RegularDualAction.lean:54](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularDualAction.lean:54>) atua sobre **o mesmo** `regularUnitary P t = fibre(modularFlowCLM P t) * shift t` da revisão anterior. A fibra modular comuta com `Dₛ`, portanto o fator escalar continua `exp(−i s t)`, com os mesmos parâmetros e o mesmo `P`.

[RegularDualAction.lean:65](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularDualAction.lean:65>) preserva a primeira classe de geradores por igualdade e a segunda por multiplicação escalar dentro da *-álgebra. Na linha 76, `regularDualAction P s` tem tipo fechado:

`(regularCoreAlgebra P).toStarSubalgebra ≃⋆ₐ[ℂ] (regularCoreAlgebra P).toStarSubalgebra`.

A preservação inversa é demonstrada com `dualAmbient_symm` e o resultado para `−s`. Não se cria outra álgebra, outra cópia do fator nem uma lista formal de geradores usada como substituto da álgebra inteira. As linhas 83–114 provam a fórmula da restrição, identidade, composição e fixação da inclusão original `regularCoreEmbedding P`.

[RegularDualAction.lean:122](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularDualAction.lean:122>) aplica continuidade conjunta da família isométrica `Dₛ` ao vetor variável `A(D₋ₛ f)`. Isso justifica a continuidade forte da conjugação sem assumir continuidade conjunta irrestrita do produto de operadores na topologia forte. Na linha 144, a conclusão restringe-se a cada `A` da álgebra gerada e cada vetor `f`. O lema da linha 136 tem `s` fixo e transporta continuidade forte de famílias arbitrárias `A(z)`; não troca essa quantificação pela continuidade simultânea de todos os parâmetros.

### Amplificação e limites fortes uniformemente limitados

[L2BoundedStrongContinuity.lean:20](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2BoundedStrongContinuity.lean:20>) usa a estimativa `‖fibre T‖ ≤ ‖T‖`. O controle de Lipschitz da linha 30 toma `max C 0`, garantindo uma constante não negativa sem supor que o índice tenha habitantes. Isso não remove a hipótese real `‖T‖ ≤ C` onde há um operador.

[L2BoundedStrongContinuity.lean:40](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2BoundedStrongContinuity.lean:40>) prova continuidade conjunta para qualquer espaço topológico `Z`, com cota global `∀ z, ‖T z‖ ≤ C` e continuidade forte da família original. A passagem por indicadores de conjuntos de medida finita e funções simples densas usa os lemas da mesma amplificação `fibre` previamente revisada.

[L2BoundedStrongContinuity.lean:70](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2BoundedStrongContinuity.lean:70>) é um enunciado genuinamente sobre **filtros arbitrários**:

`∀ i, ‖T i‖ ≤ C` e `∀ v, T i v →[l] S v` implicam `∀ f, fibre(T i) f →[l] fibre(S) f`.

Não há instância `TopologicalSpace ι`, primeira enumerabilidade, escolha de subsequência ou premissa `NeBot l`. Para o filtro vazio, a conclusão tem a semântica usual de convergência vacuamente verdadeira; não se afirma unicidade do limite nesse caso. `S` já é fornecido como operador linear contínuo, porém não recebe hipótese separada `‖S‖ ≤ C`.

A cota uniforme dá equicontinuidade. `Equicontinuous.isClosed_setOf_tendsto` torna fechado o conjunto de vetores para os quais a convergência vale, usando a continuidade de `fibre S`. O conjunto contém as funções simples densas, logo contém todo L². Não se intercambia um limite geral com uma integral sem hipótese de dominação nem se usa compacidade do índice. **A cota é global em todos os índices, não apenas eventual**; a versão com cota eventual não está enunciada aqui.

## Adendo — `RegularTopology.lean`

**[REAL — recompilação independente]** Fonte congelada com 47 linhas; SHA-256 lido `a9a0f1296dae3b109dabcf773179988f0a780f46afae05967805db5865b9980d`. O módulo e a auditoria completa passaram; os três teoremas têm somente axiomas do trio.

[RegularTopology.lean:11](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularTopology.lean:11>) transporta o centralizador ordinário de operadores limitados para a cópia `ContinuousLinearMapWOT`, por `ofCLM`/`toCLM` e suas propriedades algébricas. A função `toCLM` é usada para identificar o portador; a prova não precisa nem reivindica sua continuidade da WOT para a norma.

[RegularTopology.lean:26](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularTopology.lean:26>) reescreve o portador de uma `VonNeumannAlgebra` como o centralizador do seu centralizador. Após transportar o centralizador externo à cópia WOT, aplica `Set.isClosed_centralizer`. A assinatura desse lema foi conferida na auditoria: exige **multiplicação separadamente contínua** e espaço Hausdorff, não multiplicação conjuntamente contínua. A definição Mathlib de `ContinuousLinearMapWOT` foi consultada: sua topologia é induzida pelos coeficientes `y(Ax)`; trata-se efetivamente de WOT.

[RegularTopology.lean:39](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/RegularTopology.lean:39>) aplica a direção geral à mesma `regularCoreAlgebra P`. Não afirma a conversa “WOT fechada ⇒ bicomutante”, a existência de predual, normalidade de traço ou normalidade da inclusão. O nome `vonNeumann_wot_closed` corresponde ao enunciado efetivo. Nenhum defeito corretivo encontrado no adendo.

## Integração: estratos 17 e 18 preservados

| Estrato | Evidência conferida nesta revisão | SHA-256 do monólito lido |
|---|---|---|
| 17 módulos | 17 registros exit 0; 11 reaproveitados da etapa anterior e 6 recompilados (4 novos + 2 raízes); 44 controles Python registrados; 5879 declarações distintas no trio. | `a1962a6327c546f1c5be53cc629ca4b98176d6946c5f836ffac6316aa80d26a2` |
| **18 módulos — final** | 18 registros exit 0; 15 reaproveitados do estrato 17 e 3 recompilados (`RegularTopology` + 2 raízes); 44 controles Python registrados; 5881 declarações distintas no trio. | `6a4eea56670454d2962847e8bf603e851809f7dfa35544b60048c55622a5c0f1` |

Ambos os estratos tiveram o conjunto esperado de arquivos, os hashes de fontes e os hashes de `.olean` reconferidos. O estrato final embute **720 arquivos**, com 16 arquivos novos e 2 raízes atualizadas no rebuild. As contagens de auditoria foram recalculadas dos stdout, sem depender apenas da contagem declarada no relatório. Reaproveitamento foi identificado comparando fonte, binário e registro com o estrato anterior.

Estas linhas descrevem **inspeção independente dos registros/binários do implementador**. Não são 18 recompilações feitas por este revisor. A recompilação independente aqui abrange os cinco módulos e suas auditorias; a suíte Python integral de 44 controles foi conferida pelos registros, sem ser reexecutada nesta revisão adicional.

O `gate_extension.py` permaneceu idêntico à revisão anterior e à versão embutida no monólito final, conferida por AST. O relatório final mantém escopo `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT`, `legacy_gate_changed = False` e `full_plan_complete = False`. Nenhuma flag adicional foi habilitada por ação dual, continuidade limitada ou WOT.

## Limites que permanecem explícitos

- **Normalidade como teorema/contrato formal:** há continuidade forte da ação e preservação de limites fortes uniformemente limitados pela amplificação. Não se apresentou nesta etapa a ponte formal para preservação de supremos positivos ou continuidade ultra-fraca. Esses resultados são insumos analíticos para essa ponte; não justificam atribuir um campo formal ainda não construído.
- **Traço/core tracial:** não há construção de traço canônico normal semifinito fiel, lei de escala dual de um traço construído, predual ou pacote completo de `ContinuousCoreData`. A ação dual concreta sobre a álgebra gerada não supre esses objetos por nomenclatura.
- **Three Locks e física:** nenhum `P_F` é construído ou identificado nestes cinco arquivos. Canto finito positivo, H1–H3 compatíveis e demais requisitos físicos continuam fora das conclusões auditadas. Não há aprovação de QG.
- **Topologias:** continuidade forte pontual não é continuidade em norma de operador; fechamento em WOT não prova a conversa do teorema do bicomutante nem, sozinho, normalidade de um mapa ou de um traço.

## Hashes e evidências reproduzíveis

| Módulo | SHA-256 dev congelado | SHA-256 integrado |
|---|---|---|
| L2CharacterMultiplier | `de33feb2aa4356a0897a4079367a1c29728bb49f2c391b21bd0cf993d81f507b` | `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3` |
| GeneratedEquivariance | `908b7d2117a1b4b885b018d459bebde391a8d17aa4bb01bad1410f5267a7bada` | `0e1091b93efa8b498fefdc2e6289e57697dc0e6967a4e78cae7f4022c2f24011` |
| RegularDualAction | `fe85111dc2a976d584e276170507d383460459a31f0c30f1f3cc8f039fe865b1` | `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c` |
| L2BoundedStrongContinuity | `afc18b6b9c10d8427ef5f5750ae612b22cae485950e7577b6122273b9bf0f5dc` | `2060f158c4ef52035373fdb31b03507f37d455fdd6c952dfb26e26d92dee399a` |
| RegularTopology | `a9a0f1296dae3b109dabcf773179988f0a780f46afae05967805db5865b9980d` | `13c92b1d8948bc4d2c3891d4cbfa9bf43ac353a95e9126e2c128b1379db0ebd5` |

- [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/manifest.json>) e [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/compilation.json>): fontes, dependências, comandos, hashes de binários, retornos e axiomas da revisão dos quatro módulos.
- [DualFullAudit.stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/logs/DualFullAudit.stdout.txt>): todas as 54 assinaturas e dependências axiomáticas.
- [dependency_source_check.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/dependency_source_check.json>): as 305 fontes de dependências coincidem com o congelamento anterior; inclui a versão declarada no manifesto local de Mathlib.
- [type_probes.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/type_probes.json>) e [DualTypeBoundary.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/sources/DualTypeBoundary.lean>): sondas de sinal, inversa inteira, inclusão e filtros.
- [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/topology_addendum_20260911_213211_681604/manifest.json>), [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/topology_addendum_20260911_213211_681604/compilation.json>) e [TopologyFullAudit.stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/topology_addendum_20260911_213211_681604/logs/TopologyFullAudit.stdout.txt>): adendo WOT e auditoria dos três teoremas.
- [Estrato 17 — conferência](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/final_integrated_20260911_212635_991087/verification.json>) e [Estrato 18 — conferência final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/final_integrated_20260911_213244_821394/verification.json>): cópias dos relatórios, fontes integradas e logs de cada estrato.
- [integration_scope_check.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/integration_scope_check.json>) e [integration_reuse.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/dual_independent_20260911_212514_079909/topology_addendum_20260911_213211_681604/integration_reuse.json>): escopo do gate e reaproveitamento entre etapas.

**Preservação final:** SHA-256 do parecer anterior reconferido `2a5b2a315987bb06a44d816edcd9c231c9cef413f7aa96876d80be8a30f23026`; conteúdo intacto. As cinco fontes dev e integradas mantêm os hashes congelados. Esta revisão não editou implementação, memórias globais ou originais, nem executou/importou `um.py`. Todas as escritas permaneceram em `revisao`; não houve transposição ao canônico.
