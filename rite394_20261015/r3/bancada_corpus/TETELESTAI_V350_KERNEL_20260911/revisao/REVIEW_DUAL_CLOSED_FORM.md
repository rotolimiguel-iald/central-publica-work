# Revisão independente — leis quadráticas e formas positivas fechadas

Data: 11/09/2026. Bancada exclusiva: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911`.

**Parecer final delimitado [REAL]: as duas fontes Lean corrigidas e estabilizadas passaram na recompilação independente; nenhum defeito P0–P2 permanece identificado nessas provas.** Foram auditadas 23 declarações escritas e nove declarações geradas pelas estruturas, totalizando **32 alvos**, todos sem axiomas além de `propext`, `Classical.choice` e `Quot.sound`.

Há **um P2 documental** na versão inspecionada da minuta do recorder: a frase que atribui “exatamente essas leis” a `ClosedPositiveForm` inclui, por referência ao parágrafo precedente, uma lei entre operadores distintos que é provada separadamente para a família `dualQuadraticIntegral`. A precisão é detalhada abaixo. O erro de compilação da primeira versão de `DualClosedForm` foi corrigido pelo autor e a correção foi validada independentemente.

O conteúdo estabelecido é: leis de forma positiva estendida, semicontinuidade inferior, domínio finito vetorial como submódulo, subníveis fechados e invariância pelo comutante unitário da mesma álgebra. **Não se estabelece um operador auto-adjunto espectral, um cone ampliado construído em Lean, peso dual canônico, semifinitude, traço ou Three Locks.**

## 1. Achados priorizados e seu estado

### P1 histórico — erro de elaboração corrigido, não pendente

Na primeira tentativa do autor, [DualClosedForm.lean:105](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:105>) usava `U.inner_map_map`, embora U tivesse o tipo de um elemento do subtipo `unitary`. O campo não era resolvido; houve exit 1 e o elaborador deixou `sorryAx` nas duas declarações dependentes. A tentativa falha está identificada pelo hash de fonte `d79c571fff007f6f62725de25e8862ae678ac1e95021c38669f7d7ffa7a38df1` e por [seu log original preservado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/author_failed_attempt/DualClosedForm_20260911_230623_951830.stdout.txt>).

A versão corrigida usa `Unitary.inner_map_map U`. Foi congelada em bytes e recompilada nesta revisão com exit 0; o audit independente final não contém `sorryAx`. Não houve edição Lean pelo revisor. A primeira versão foi inspecionada antes da correção, mas **não foi copiada em bytes pelo revisor antes de ser substituída pelo autor**: a evidência preservada dessa tentativa consiste nos logs e no hash de fonte neles registrado. Não se apresenta essa tentativa como uma recompilação independente bem-sucedida.

### P2 documental — separar a estrutura de uma forma da lei da família de operadores

Localização: [record_closed_form_progress.py:129](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/record_closed_form_progress.py:129>), na minuta do relatório ainda não executado. O parágrafo anterior enumera `q_A(c v)`, o paralelogramo e `q_(r A)=r q_A`; em seguida afirma que `ClosedPositiveForm` reúne exatamente essas leis. Contudo, [DualClosedForm.lean:15](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:15>) tem uma única função `value : H → ENNReal`: seus campos são valor zero, homogeneidade **vetorial**, paralelogramo e semicontinuidade inferior. A homogeneidade em A vive em [DualQuadraticLaws.lean:61](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:61>) e relaciona membros distintos da família, não sendo campo da estrutura.

Redação sugerida, sem alteração pelo revisor: **“`ClosedPositiveForm` reúne homogeneidade vetorial, paralelogramo, semicontinuidade inferior e q(0)=0; a homogeneidade em A foi provada separadamente para `dualQuadraticIntegral`.”** Isso preserva o resultado sem ampliar o contrato. O snapshot da minuta tem SHA-256 `bc32b3ebb9df30ed0d7acc9dce56ae83e03f3290740967978808a12483947331` e está [preservado aqui](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/documentation_snapshot/record_closed_form_progress.py>).

No restante do texto matemático examinado da minuta, a distinção entre finitude vetorial e domínio de peso está correta: não exige densidade de `D(q_A)` para todo A positivo; reconhece que `D(q_I)={0}` não decide semifinitude de um peso futuro; separa invariância da forma de representação espectral e de identificação com a base. Por precisão bibliográfica, A.13 é definição, A.14 é lema e A.15 é teorema. Esta inspeção foi **estática**: o recorder não foi executado, importado ou autorizado por este parecer a escrever memórias. O seu mecanismo de gravação não foi objeto de auditoria operacional exaustiva.

## 2. `DualQuadraticLaws`: hipóteses, infinito e semicontinuidade

[DualQuadraticLaws.lean:14](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:14>) e [DualQuadraticLaws.lean:20](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:20>) são identidades algébricas das avaliações reais de um CLM complexo. Valem para A arbitrário: a primeira usa o produto do escalar com seu conjugado, a segunda expande as duas parcelas sem hipóteses de positividade. A convenção de produto interno complexo foi respeitada.

[DualQuadraticLaws.lean:27](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:27>) e [DualQuadraticLaws.lean:36](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:36>) transportam a homogeneidade vetorial para ENNReal. O fator é `ofReal (‖c‖²)`, que é não negativo e finito. As igualdades valem também para `c=0` e avaliações infinitas: a multiplicação de ENNReal usa `0 * ∞ = 0`, em acordo com a lei `q(0)=0` já existente. Não há divisão por c, exigência implícita `c≠0` ou cancelamento de infinito.

[DualQuadraticLaws.lean:44](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:44>) identifica explicitamente a ação de um escalar real com a coerção complexa no mesmo operador. [DualQuadraticLaws.lean:61](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:61>) exige **`r ≥ 0`**, embora não exija A positivo: a definição total com `ofReal` permite a multiplicação por um escalar real não negativo. Não se afirma homogeneidade para r negativo.

No paralelogramo em ENNReal, a hipótese A positivo é indispensável à prova escrita: [DualQuadraticLaws.lean:68](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:68>) usa `hA : 0 ≤ A` antes de cada aplicação de `ENNReal.ofReal_add`. [DualQuadraticLaws.lean:81](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:81>) integra as funções mensuráveis e usa apenas somas e produtos distributivos; não subtrai infinitos nem conclui finitude de uma parcela a partir de igualdade entre dois infinitos. Assim, o fato de a definição de q ser total para A arbitrário não elimina `hA` das leis que a tornam forma positiva.

[DualQuadraticLaws.lean:102](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:102>) obtém

`q_A(v+w) ≤ 2 q_A(v) + 2 q_A(w)`

por ordem e adição em ENNReal. Essa desigualdade é suficiente para provar a estabilidade do domínio finito por soma no módulo seguinte, sem invocar Cauchy–Schwarz ou polarização ainda não construídas.

[DualQuadraticLaws.lean:110](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:110>) demonstra continuidade da avaliação de **cada operador de corte limitado** em função do vetor, com o mesmo fator `(2π)⁻¹`. A prova reescreve o produto em ENNReal como `ofReal` de um produto real, evitando qualquer hipótese indevida de continuidade global da multiplicação em pontos `0·∞`.

[DualQuadraticLaws.lean:122](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualQuadraticLaws.lean:122>) exige A positivo, usa a igualdade já construída `q_A(v)=sup_n avaliação_do_corte_n(v)` e aplica semicontinuidade inferior do supremo de funções contínuas. Não pressupõe normalidade de um peso nem representação espectral da forma. A igualdade com os cortes, e não uma simples desigualdade inferior, é o que justifica a conclusão sobre q_A.

## 3. `DualClosedForm`: o que os tipos efetivamente contêm

[DualClosedForm.lean:15](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:15>) define uma função não negativa estendida sobre todo H, valor zero, homogeneidade pelo módulo quadrado do escalar complexo, paralelogramo e semicontinuidade inferior. Não contém campos de densidade do domínio, operador auto-adjunto, medida espectral, predual ou traço. O nome `ClosedPositiveForm` designa essa apresentação por leis; uma equivalência Lean com outros tipos de forma fechada não foi construída neste incremento.

[DualClosedForm.lean:30](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:30>) constrói de fato `Submodule ℂ H` com portador `{v | Q.value v < ⊤}`. Zero pertence por `map_zero`; a soma é finita pela desigualdade quadrática e por finitude de `2 q(v)+2 q(w)`; o produto escalar é finito porque `ofReal(‖c‖²)<∞`. A linearidade do domínio não é uma hipótese entregue ao construtor. [DualClosedForm.lean:44](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:44>) expõe o critério por igualdade definicional.

[DualClosedForm.lean:47](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:47>) prova `IsClosed {v | Q.value v ≤ c}` para cada c em ENNReal. **Isso não é `IsClosed D(q)`**: reunir todos os valores finitos não equivale a um único subnível finito, e a fonte não faz essa passagem. Tampouco contém um campo `Dense D(q)` ou uma identificação automática entre domínio finito e seu fecho.

[DualClosedForm.lean:52](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:52>) usa exatamente `dualQuadraticIntegral A`, com `hA : 0 ≤ A`. As leis são fornecidas pelas provas anteriores; nenhuma delas é substituída por um rótulo `Prop` sem conteúdo. O objeto vive em `RegularHilbert H`, o mesmo L² de Lebesgue utilizado pelos cortes.

Os extremos foram provados, e não postulados:

- [DualClosedForm.lean:61](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:61>): `D(q_I)=⊥`, isto é, somente o vetor zero. Para v não nulo usa `q_I(v)=∞`, incompatível com `q_I(v)<∞`.
- [DualClosedForm.lean:75](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:75>): `D(q_0)=⊤`, pois q_0 é zero em todos os vetores.

Esses resultados não precisam de uma hipótese de Hilbert não trivial. Se o Hilbert for trivial, os submódulos ⊥ e ⊤ coincidem; não há contradição nos enunciados. Em espaço não trivial, o primeiro exemplo mostra por que não se pode exigir universalmente densidade do domínio vetorial em todo H.

## 4. Mesmo comutante, mesma álgebra e afiliação da forma

[DualClosedForm.lean:84](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:84>) estende a forma por uma condição explícita: para **todo** unitário U que comuta com **todos** os B de N, `q(Uv)=q(v)` para todo vetor v. Não se limita a uma lista de geradores ou a unitários escolhidos do comutante. O campo descreve invariância da forma; seu tipo não contém um operador espectral afiliado.

[DualClosedForm.lean:89](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:89>) assume separadamente A positivo, A pertencente a `regularCoreAlgebra P`, U unitário e comutação com essa mesma álgebra. A prova usa a representação de q por supremo de cortes. Cada corte pertence à álgebra concreta; portanto U comuta com esse corte. Aplicar essa igualdade a v e usar `Unitary.inner_map_map U` preserva a avaliação de cada termo. A igualdade passa então ao supremo em ENNReal, sem pressupor finitude de q ou um vetor do domínio finito.

[DualClosedForm.lean:107](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/DualClosedForm.lean:107>) junta a forma construída e essa prova para **`AffiliatedPositiveForm (regularCoreAlgebra P)`**. As coerções e o Hilbert são os mesmos; não se introduz uma nova realização nem se troca a álgebra pelo modelo base. Em particular, invariância por N′ não é invariância automaticamente estabelecida pelo comutante, em geral maior, da imagem da base.

## 5. Fonte primária e compatibilidade conceitual — não teorema Lean adicional

[KNOWN — leitura visual] Na definição A.13, formas positivas admitem infinito e a convenção `0∞=0`. A.14 usa **`K=closure D(q)`**, com barra visível; A.15 relaciona semicontinuidade inferior à representação sobre K, sem exigir K=H. A restrição finita tem domínio D(q), denso em K; não se confunde D(q) com K. Conferi as páginas impressas 154–155 do PDF, após a captura web falhar. [Hiai, A.13–A.15](https://arxiv.org/pdf/2004.02383v1#page=154).

[DERIVED — rota compatível, ainda não formalizada] As leis construídas e a invariância pelo comutante são compatíveis com a rota de representação e afiliação do §8.1: construir K, a representação espectral e a eventual parte infinita em K⊥, então a avaliação sobre funcionais normais positivos. Isso forneceria uma ponte ao cone ampliado de N; chegar à imagem da base ainda requer identificar os pontos fixos da ação dual. Esta rota não autoriza declarar tais objetos já construídos em Lean. [Hiai, teorema 8.3 e sua prova](https://arxiv.org/pdf/2004.02383v1#page=69).

O PDF usado foi pinado por SHA-256 `a287a32777b854ad635349f1c4b0988111df90ca5d65d7bbcf5d904fef66790c`. [Registro de URL e hash](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/references/reference.json>). A extração textual consultada omitia a barra sobre D(q); a leitura visual resolveu a ambiguidade. Nenhuma conclusão deste parecer assume que D(q) seja um subespaço fechado de H.

## 6. Domínio da forma versus domínio de um peso

`finiteDomain` é um submódulo de **vetores**: D(q_A) varia com um operador A fixado. Já as obrigações de semifinitude de um peso futuro concernem um domínio/ideal de **elementos da álgebra**, determinado pelos valores desse peso. A fonte não constrói esse peso nem seu ideal.

Logo, os teoremas `D(q_I)=⊥` e `D(q_0)=⊤` não decidem semifinitude. Não se deduz falta de semifinitude pela ausência de vetores não nulos com q_I finita, nem se deduz semifinitude por haver um submódulo vetorial construído. Também não se deduz que q_A tenha domínio finito denso em H para todo A positivo. Essa separação está correta na minuta, à parte o ajuste de escopo dos campos assinalado no P2.

## 7. Recompilação independente e preservação

Compilador: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`. O manifesto registra seu hash, as dependências e o `LEAN_PATH` completo.

| Fonte recompilada | Linhas | Declarações escritas | Exit | SHA-256 da fonte |
| --- | ---: | ---: | ---: | --- |
| [DualQuadraticLaws.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/sources/TGLV350/DualQuadraticLaws.lean>) | 141 | 12 | 0 | `b9af0dac5020997765a297e4de081ea73272b3179c6c48978d55ec9e0f61413c` |
| [DualClosedForm.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/sources/TGLV350/DualClosedForm.lean>) | 123 | 11 | 0 | `755584c8e296f48e4ca49ddbfc1c5c4e7f2af3244cfea4d929b443f5d2d99edc` |

Foram congeladas **318 dependências de projeto**, com fontes e binários identificados por hash. `DualClosedForm` foi recompilado contra o `DualQuadraticLaws` produzido pelo revisor, não contra seu `.olean` novo do pai. Os builds vivos do projeto pai e do projeto canônico não entram no `LEAN_PATH`; entram a árvore própria e os pacotes instalados em leitura.

**Base de confiança declarada:** o compilador e os pacotes, incluindo Mathlib, não foram reconstruídos nem integralmente duplicados nesta revisão. O congelamento por fonte/binário aqui declarado cobre os módulos de projeto. A reutilização dessas dependências não foi descrita como uma nova prova de cada módulo histórico.

Foram executados três processos Lean independentes: as duas fontes e `ClosedFormFullAudit.lean`. Os 32 nomes auditados são as 23 declarações escritas, mais construtores e projeções selecionados das duas estruturas. O conjunto impresso coincidiu com o esperado; todos os axiomas estão no trio permitido. Não foram realizados outros testes Lean de fronteiras abertas nesta etapa.

Evidência: [manifesto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/manifest.json>), [comandos, exit codes e hashes dos binários próprios](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/compilation.json>), [tipos completos e axiomas impressos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/logs/ClosedFormFullAudit.stdout.txt>). Os hashes das fontes permaneceram iguais durante a revisão e todos os pareceres anteriores identificados no manifesto foram preservados. A versão inicial falha permanece separada como evidência de erro do autor, não como binário aceito.

## 8. Snapshot integrado final — inspeção estática e hashes

**SHA-256 experimental conferido:** `80d168b66d543803444f970aaebbc18030ceeeaaaaff6ec13b1ca42549f4c0c0`. Coincide com `integration.json` e `gate_tests.json`. O AST foi lido como dados; não se executou nem importou `um.py`.

| Fonte integrada | SHA-256 conferido |
| --- | --- |
| DualQuadraticLaws | `7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3` |
| DualClosedForm | `69a47c01fc1a366a61b871b86e1d7114e43e865b025a04cd57918f09ed7c5be7` |

Os dois arquivos TGLExt coincidem com os snapshots recompilados, exceto pelos caminhos de importação; seus bytes também coincidem com as entradas do dicionário embutido. Foram encontrados 729 fontes embutidos.

**Evidência do autor conferida por leitura e hashes:** 27/27 registros Lean com exit 0, hashes de fonte e `.olean` válidos, 50/50 controles Python marcados aprovados e 5937 declarações distintas no Audit, sem axiomas além do trio. Esses totais **não são recompilações das raízes nem testes Python executados pelo revisor**: a execução independente foi a dos dois módulos e sua auditoria própria.

Em relação ao estrato 25/48/5.922, os 23 módulos anteriores conservaram os hashes de fonte e binário; as quatro novas compilações correspondem aos dois módulos e às duas raízes. Não houve remoção de fontes embutidos. Entre os antigos, somente `TGLExt.lean` e `TGL/Audit.lean` mudaram. O AST Python fora do dicionário embutido é idêntico ao backup de hash `cb7b87f8f64a7bb0483767809d6712d1d381c6530c24d733de87473a5d2ba7b1`; `gate_extension.py` é byte a byte igual ao desse estrato.

Foram inspecionados os controles novos `closed_form_affiliation_does_not_supply_canonical_trace` e `constructed_finite_domain_does_not_supply_semifinitude_or_three_locks`. Eles constam como aprovados no relatório do autor; a estrutura de forma não foi usada para quitar traço, canto, H1 ou testemunha total. A função legada não foi reexecutada nesta revisão e o runtime integral permanece pendente.

Evidência congelada: [verificação AST/hash e comparação entre estratos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/final_integrated_20260911_231413_933750/verification.json>), [compilações integradas do autor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/final_integrated_20260911_231413_933750/integrated_compile.json>), [controles do autor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/final_integrated_20260911_231413_933750/gate_tests.json>) e [Audit extraído](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/final_integrated_20260911_231413_933750/axioms.json>).

## 9. Limites finais e encerramento do escopo

[OPEN] Representação por operador auto-adjunto e resolução espectral; construção do cone ampliado e identificação com a base; peso dual canônico, seu domínio na álgebra e semifinitude; traço e sua lei de escala; Three Locks e conclusões físicas/QG. O fechamento matemático da revisão não promove essas pendências a teoremas Lean.

A inspeção delimitada dos enunciados, da composição, dos tipos, da fonte primária e do texto matemático da minuta foi concluída. A execução do recorder e a revisão operacional completa de suas gravações não fazem parte desta entrega. O ajuste documental P2 é uma recomendação ao autor e não foi aplicado pelo revisor. Este parecer não declara a documentação já corrigida.

Todas as gravações do revisor ficaram sob `revisao`: snapshots, scripts, logs, binários independentes, referência bibliográfica e este relatório. Fontes do autor, raízes, integração, monólito, originais e memórias do pai não foram alterados. Não há aprovação de QG, transposição ao canônico ou atribuição dos resultados às flags abertas.


## 10. Adendo documental — 11/09/2026 23:24:00 -0300 — P2 encerrado

**[REAL — inspeção documental, sem nova execução] O P2 documental está corrigido e encerrado no recorder conferido neste adendo.** As observações anteriores sobre sua pendência permanecem como registro do snapshot original; este adendo atualiza seu estado exclusivamente para a versão identificada abaixo.

Conferidos no texto de [record_closed_form_progress.py:129](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/record_closed_form_progress.py:129>) os campos da forma: homogeneidade vetorial, paralelogramo, semicontinuidade inferior e q(0)=0. Nas linhas 130–131, a homogeneidade em A está expressamente separada como teorema sobre a família `dualQuadraticIntegral`, sem ser atribuída à estrutura `ClosedPositiveForm`. A redação corresponde aos campos de `DualClosedForm.lean:15–20` e à distinção já examinada no parecer. **A correção resolve o achado sem ampliar o contrato matemático.**

Conferida também, na linha 146, a identificação bibliográfica **definição A.13, lema A.14 e teorema A.15**, conforme a fonte primária já examinada nesta revisão. As linhas 186–188 registram a correção e a preservação do snapshot original. O trecho mantém a representação espectral como ainda não formalizada e preserva a distinção entre domínio finito vetorial da forma e domínio/ideal de um peso na álgebra.

Evidência de bytes lida nesta conferência:

- Recorder corrigido: 12813 bytes; SHA-256 `6f562e3cce11d00ba041b5b62996b05fdc7ca535305cd4aadbaca3d277858114`. [Cópia exata preservada](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/documentary_addendum_20260911_232400_471376/record_closed_form_progress.py>).
- [Snapshot original preservado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/closed_form_independent_20260911_230903_418368/documentation_snapshot/record_closed_form_progress.py>): 12373 bytes; SHA-256 `bc32b3ebb9df30ed0d7acc9dce56ae83e03f3290740967978808a12483947331`.
- [Backup imediato do parecer anterior](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_CLOSED_FORM.md.bak_20260911_232400_471376>): 22686 bytes; SHA-256 `9eadd221aee4fec1eee6249027496601c96e03de00849f8da1841fc68154bff9`. A igualdade byte a byte foi conferida antes da substituição; o parecer anterior permanece integralmente como prefixo deste arquivo.

Este adendo resulta somente da leitura e comparação documental e da preservação dos respectivos bytes. O recorder e `um.py` não foram executados nem importados; não houve nova compilação, auditoria Lean ou teste Python. As evidências anteriores de recompilação independente e de integração conservam o alcance e a distinção já registrados. Nenhuma fonte do autor, integração, log original ou memória foi alterada pelo revisor.

**Escopo encerrado, sem achado pendente no pacote delimitado.** Permanecem os limites do parecer: representação espectral, cone ampliado construído em Lean, peso dual canônico, semifinitude, traço e Three Locks não são certificados por esta revisão; nenhuma flag é quitada por este adendo.
