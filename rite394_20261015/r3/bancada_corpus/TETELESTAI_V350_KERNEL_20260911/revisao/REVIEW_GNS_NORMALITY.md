# Revisão independente — normalidade em ordem da representação GNS

2026-09-12T08:15:17-03:00. **DEV concluído: dois módulos/sete alvos. Nenhum achado P0, P1 ou P2 nas fontes finais e na rota examinada.** [REAL — leitura integral, recompilação e auditor independente] A mesma representação π_I de N em B(H_I) é positiva, monótona e preserva supremos internos de famílias positivas crescentes, não vazias e dirigidas, com resultado de supremo no ambiente B(H_I). O limite forte necessário é construído dentro da prova; não é premissa do teorema de normalidade.

Escopo novo: `ScalarGNSStrongContinuity.lean` (1 alvo) e `ScalarGNSNormality.lean` (6). A rota `ROTA_NORMALIDADE_GNS_RASCUNHO.md` foi lida integralmente. [REVIEW_TOMITA_INITIAL_DOMAIN.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_TOMITA_INITIAL_DOMAIN.md>) e todos os pareceres/custódias anteriores permanecem somente leitura. Não se construiu fechabilidade nem se examinou nova integração.

## Enunciados, ordem e composição

**ScalarGNSStrongContinuity.lean:16–27.** O teorema transporta para o mesmo H_I um limite forte **dado** na representação regular: recebe Tᵢ∈N, B∈N, `∀i, ‖Tᵢ‖≤C` e `∀v, Tᵢv→Bv` ao longo de `l : Filter ι`, para `ι : Type u` arbitrário. Aplica a transferência ambiente já revisada ao vetor `v.val` e `tendsto_subtype_rng` à restrição que define π_I. Não troca o espaço nem a ação por um homônimo; a coerção de π_I é a mesma representação ambiente restrita ao subespaço fechado. A conclusão é convergência em norma de H_I para cada vetor, não convergência em norma de operador. O filtro é arbitrário, sem topologia, enumerabilidade, separabilidade ou condição de não trivialidade adicional. A hipótese SOT deste lema de transferência é explícita e adequada; ela será **provada**, não pressuposta, na aplicação de normalidade.

**ScalarGNSNormality.lean:12–37 — positividade e monotonicidade (4 alvos).** A ordem é a ordem de Loewner herdada da Mathlib: A≤B significa positividade do operador B−A. `operator_le_of_sub_nonneg` usa essa ordem, não uma ordem escalar ou ponto a ponto inventada. `dualOrbitRepresentation_nonneg` usa a instância de monotonicidade do `StarAlgHom` ambiente e `map_zero`; não recebe positividade/normalidade da representação como hipótese. Na restrição a H_I, `isPositive_iff_complex` preserva tanto a realidade quanto a não negatividade de ⟨Tv,v⟩, via `v.val` e o produto interno herdado. Não se verificou somente a parte real deixando de exigir simetria. A monotonicidade de π_I segue da positividade de π_I(B−A), `map_sub` e positividade da diferença. Nenhuma premissa de normalidade é usada nesses passos.

**ScalarGNSNormality.lean:41–59 — IsLUB interno → IsLUB ambiente.** O tipo exato recebe `[Preorder ι] [IsDirectedOrder ι] [Nonempty ι]`, T:ι→N, B∈N, `∀i,0≤Tᵢ`, `Monotone T` e `IsLUB (range T) B` **no subtipo N**. A conclusão é `IsLUB (range (π_I∘T)) (π_I B)` **em todos os CLM de H_I**. O índice conserva o universo livre `u_1` no auditor; não há redução a sequências ou conjuntos enumeráveis. O Hilbert é o H_I concreto associado ao mesmo `SiteProfile P`.

A cadeia foi conferida nos termos e nas dependências congeladas:

1. `Tᵢ≤B` vem apenas da parte de majorante do IsLUB interno. Positividade dá `‖Tᵢ‖≤‖B‖` pela ordem C*. A cota é derivada, e `‖B‖≥0`. Não se exige uma nova hipótese `0≤B`: ela também segue de positividade e não vazio da família, e o lema de norma não a pede separadamente.
2. `vonNeumann_exists_positive_isLUB` (`RegularNormality.lean:52–67`) constrói um limite forte D ambiente pela convergência monótona de operadores positivos limitados. O fechamento WOT da mesma N coloca D em N; só depois o supremo ambiente de D é restringido a um IsLUB interno. **Não usa normalidade de π_I nem a promoção de um IsLUB interno arbitrário a ambiente como premissa.**
3. A unicidade entre o IsLUB interno recém-construído e o hB dado prova D=B. Assim obtém-se Tᵢ→B fortemente dentro da prova. A direção ambiente→interno na construção e a unicidade impedem circularidade na passagem inversa.
4. O lema de transferência fornece π_I(Tᵢ)v→π_I(B)v. A monotonicidade já provada permite aplicar `monotone_strong_limit_isLUB` (`TGLExt/MonotoneOperatorLimit.lean:204–220`). Esse lema aceita **qualquer majorante ambiente D em B(H_I)**: a positividade de D−π_I(Tᵢ) passa ao limite, dando D−π_I(B)≥0. A conclusão não se limita a majorantes pertencentes a π_I(N).

Não vazio e direção asseguram `atTop.NeBot`, usado na conservação de positividade, na pertença ao fechado WOT e na construção do limite. Portanto os passos de fechamento não exploram limites vacuamente válidos num filtro vazio. A transferência isolada aceita todos os filtros; o teorema de supremo usa especificamente a rede dirigida com `atTop`. Nenhuma convergência forte, continuidade SOT geral ou normalidade aparece como premissa final.

**ScalarGNSNormality.lean:63–82 — conjuntos dirigidos.** O último alvo recebe um conjunto S⊆N explicitamente **não vazio**, dirigido e positivo, com supremo interno B. O subtipo S fornece o índice e suas instâncias, a inclusão é monótona, e as igualdades entre `range` e S, e entre `range` da representação e π_I''S, são provadas. Conclui supremo contra todos os majorantes de B(H_I), com as mesmas hipóteses de ordem. Não presume existência universal de supremos de famílias não limitadas ou inclui o conjunto vazio.

O alcance demonstrado é **normalidade em ordem**, por preservação dos supremos positivos dirigidos internos. Não se afirma uma equivalência Lean geral com continuidade ultra-fraca/predual, nem se empacota aqui uma nova interface de representação normal. Esse limite não é um defeito das proposições solicitadas.

## Evidência independente

**Dois módulos + auditor, três processos rc0, sem warnings.** O auditor próprio faz sete `#check` com universos visíveis e sete `#print axioms`, cobrindo exatamente todas as declarações nomeadas das duas fontes. Sua saída foi lida integralmente. Todos os alvos dependem apenas de `propext`, `Classical.choice`, `Quot.sound`; não há `sorryAx` ou axioma extra. Os dois binários independentes são byte a byte iguais aos autorais finais.

| Fonte DEV | Alvos | SHA256 fonte viva = congelada | SHA256 .olean próprio = autoral |
|---|---:|---|---|
| ScalarGNSStrongContinuity | 1 | `8316f26c053942f8150428dd49d7d215572efb8cfdb1517cef7b6218d94ea252` | `fd9893c0b15c60645ae15a640de70dfa1e568d1a296975bdbe7435c19e5ea05c` |
| ScalarGNSNormality | 6 | `847cec0d790b3c72661ab8e1e21cfcec419bafb3c3df8890e00e9c073ad6a705` | `42e5f3d403ad04de28fc6b44e9d2790826ff3ede860ecf5be213798626e49143` |

| Fonte | Log autoral final lido, não executado | SHA256 JSON do log |
|---|---|---|
| ScalarGNSStrongContinuity | ScalarGNSStrongContinuity_20260912_075221_992373.json | `5ae9f0458ccac531e0b2c7e347aecfc293b2c92ff9ee17fa1fa982405f71f257` |
| ScalarGNSNormality | ScalarGNSNormality_20260912_080437_845416.json | `0bbd10db646c85a99a70912c4d501dbfee503bc030558e5192a0cde3d9265081` |

Em [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_normality_independent_20260912_081001_179488/compilation.json>) estão os comandos próprios, tempos, rc e hashes. [verification_dev.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_normality_independent_20260912_081001_179488/verification_dev.json>) registra comparação com status/log autoral, fonte inalterada durante o build, hash do binário, hashes de stdout/stderr e igualdade dos streams às cópias congeladas. Tentativas de elaboração anteriores não foram tratadas como erros pendentes dos bytes finais. Não houve falha de compilação própria nesta etapa.

Auditor: fonte `6ffffc0f39d44bfc5e7593e6d6e63b536c0944304edcee16b13909477b02ee93`, binário `ce638594fb0896fce8d9e702c7d44a8980bc65790e6596eabcd38bfb60230d8f`, stdout `62b9d546d5eaa8a3e45dcfe39a08d55ba8454457a45c1578929de0c9286cdf25`. Tipos completos: [GNSNormalityAudit.stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_normality_independent_20260912_081001_179488/logs/GNSNormalityAudit.stdout.txt>). Os sete conjuntos de axiomas coincidem com o status, não apenas com o número declarado pelo autor.

**Herança e isolamento.** [manifest.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_normality_independent_20260912_081001_179488/manifest.json>) pina as 383 dependências de projeto necessárias, fontes e binários provenientes da árvore própria anterior de Tomita/GNS. Nenhum build autoral de projeto entrou no `LEAN_PATH`; a entrada de projeto é somente `revisao/.../build`, seguida dos pacotes existentes, usados readonly. As dependências e a biblioteca não foram recompiladas. Versão `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`; compilador SHA256 `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`. Fonte do autor e originais não foram editados.

A exceção histórica continua explícita: `DualSemifiniteIdeal` usa a fonte própria `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3` e o binário próprio `6a242f29df8816cf7e741cb043f6c24f88fb9e844fc60f90d3bce25a4c1f26df`; a fonte viva corrigida é `f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3`. A diferença literal exclusivamente de comentário, já revisada, foi novamente reconhecida ao congelar; provas intactas. Não se afirma reprodução binária integral da cadeia herdada. A limitação anterior de `RegularScalarWeightCertificate` não é usada, pois esse módulo não integra o fecho de imports atual. Todos os pins próprios e pareceres anteriores foram preservados.

## Documento, bibliografia e limites

Status autoral congelado: `7d37eb1bb6becd6d9e12d4bb441ad07cf8a88b28571cf8484d32499b99c46f89`. Rota integralmente lida: `ef74437dc475a1be87d06590f30e1fe65855e63fd33b53da5cbc8142c7f936d1`. As linhas 11–17 descrevem corretamente a rede **positiva crescente com supremo interno** e a conclusão ambiente; o texto não omite essas hipóteses. O último teorema corresponde ao conjunto não vazio dirigido mencionado. As linhas 26–31 mantêm separados fechabilidade, fidelidade, normalidade e domínio máximo; não generalizam a propriedade separante de η, antes obtida para F, à álgebra N.

A referência bibliográfica das linhas 33–39 foi conferida no texto primário: o Teorema 3.12 e seu esboço, p. 45, tratam a correspondência com álgebras de Hilbert e destacam a fechabilidade da involução; o esboço usa a aproximação de um peso por funcionais normais positivos dominados. Isso sustenta a orientação documental, sem prover uma prova Lean deste peso. O livro remetido não foi consultado nem se investigou a próxima construção. [Masuda, Teorema 3.12, p. 45](https://www.math.okayama-u.ac.jp/mjou/mjou60/_02_Masuda.pdf). Consulta via PDF na web, sem pin binário do PDF; os pins acima são dos arquivos locais efetivamente medidos.

Custódia anterior: `74032b182c679e3e82b55e5af9d85146eb5b2f043468b563865eb2b50bb173bc`; pin do parecer Tomita confirmado por hash vivo `e0a3762340e569a8095ae6a16719a7881d96a3ce87d534083371a6f2b31c2a42`. O snapshot anterior `940f72d47b0458b1696395253d6e66bb0bf85b59f346f06e891da571957ddaae`, 96 registros/69 controles/6330 Audit, é **herança da custódia do domínio inicial**. Não são contagens de integração dos dois módulos novos. Não foram repetidos recorder/verifier nem os backups dessa custódia.

**Conclusão DEV encerrada sem achados pendentes.** Foram conferidos sete alvos novos: transferência de limites fortes uniformemente limitados, positividade/monotonicidade e preservação de supremos positivos dirigidos na mesma representação. Não houve inspeção ou certificação de nova integração, build de raízes, execução de controles, monólito, recorders ou verifiers autorais. Toda saída nova está em `revisao/`.

Continuam fora deste parecer: fechabilidade/univalência do fecho do gráfico de Tomita, operador fechado e decomposição polar, identificação do domínio máximo de ν, KMS/identificação modular, traço, interface geral espectral/predual/operatorial, Three Locks/H1–H3/física, consumo de certificado pelo gate e runtime. Nenhuma análise necessária dos dois módulos finais ficou incompleta; não se promoveu gate nem se estendeu a revisão a fontes posteriores. Pareceres congelados permanecem intocados.


## Adendo integrado — 2026-09-12T08:25:24-03:00

**Conferência integrada concluída, sem achados P0–P2.** Escopo exclusivo: `ScalarGNSStrongContinuity` e `ScalarGNSNormality`, sete alvos. Mantém-se integralmente o parecer DEV acima. Este adendo acrescenta inspeção independente de fontes, hashes, imports, AST, logs e documentação; não acrescenta recompilações próprias nem execução de testes autorais.

[REAL — hashes e comparação estática medidos aqui] A cópia `um.py` tem SHA256 **`ba8c069e6cd1a563e186239ff0255fb172c5964e76732d307b4b167a78c1eecd`**, coincidente com `integration.json` e `gate_tests.json`, e contém **800** arquivos. A base local e o original canônico, relidos apenas para hash, têm ambos `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`, igual ao pin de base. Nenhum monólito foi executado/importado.

| Evidência | Resultado e limite |
|---|---|
| Recompilação própria DEV, estrato anterior | Dois módulos + auditor rc0; sete `#check` e sete `#print axioms`; somente trio. Os dois binários DEV próprios coincidiram com os autorais. Dependências próprias congeladas e limitações de herança permanecem as do primeiro estrato. |
| Build integrado autoral, inspecionado | **98 registros rc0**, todos com fonte e `.olean` relidos e seus hashes conferidos. **94** preservam fonte/binário da custódia Tomita; **quatro** compilações novas: dois módulos + `TGLExt.lean` + `TGL/Audit.lean`. Não são 98 recompilações. |
| Auditor integrado autoral, inspecionado | **6337 declarações distintas**, somente `propext`, `Classical.choice`, `Quot.sound`. Mapa extraído do stdout igual ao de `kernel_incremental_evidence.json`; os sete alvos coincidem em nomes e conjuntos de axiomas com o auditor próprio. |
| Controles autorais, inspecionados | **70/70** registrados como passados. Foram conferidos o vínculo ao snapshot e a alteração do controle; não houve execução de testes pelo revisor. |
| Gate e runtime | Seis flags maiores `false`, `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`, conforme os registros. Nenhuma quitação de gate ou liberação de runtime. |

**Preservação dos enunciados e imports.** As duas fontes `TGLExt/V350*.lean` são exatamente os DEV congelados após substituir somente o prefixo de import `TGLV350.` por `TGLExt.V350`. Nem normalização adicional de finais de linha foi necessária. Cada fonte integrada coincide byte a byte com o respectivo texto embutido; ambas as raízes importam explicitamente os dois módulos. Contra a cópia Tomita anterior, há somente essas duas entradas novas, nenhuma removida e apenas as duas raízes alteradas entre entradas preexistentes. Os sete tipos e corpos revisados no DEV foram conservados; esta comparação de tipos por identidade textual não é um novo `#check` das raízes integradas.

| Módulo | SHA256 fonte integrada | SHA256 `.olean` integrado autoral lido |
|---|---|---|
| ScalarGNSStrongContinuity | `a01a6e42e191d7bc7ce2a37e529fead8d04463b62d19f081fd640f249e2b3938` | `506cda327ba14cd161678ccd5659c14e069643e98dc35ec221851979a5bb9ddd` |
| ScalarGNSNormality | `adef4ae98893c92165d9d8b40ab7a1a298cfcd9da7e11fb42a2e7a906c6181fc` | `812d06e915b4c89a3921b869b5827bd3939a88392eafac2a515cb2f118516f9b` |

As quatro compilações novas registram fonte inalterada durante a execução e não contêm warnings. Seus timestamps e hashes de **stdout e stderr**, com comparação aos streams congelados, estão em [supplemental_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_normality_independent_20260912_081001_179488/final_integrated_20260912_082213_298026/supplemental_verification.json>). Fontes e streams dos 98 registros foram congelados no mesmo diretório. Não se reivindica recompilação independente da árvore integrada inteira ou identidade binária de toda a cadeia herdada.

**AST e controle.** O baseline foi localizado em backup cujo hash é `940f72d47b0458b1696395253d6e66bb0bf85b59f346f06e891da571957ddaae` e validado contra `tomita_domain_custody.json` (SHA256 `74032b182c679e3e82b55e5af9d85146eb5b2f043468b563865eb2b50bb173bc`). Removida somente a atribuição `_EMBEDDED_KERNEL_FILES`, a AST inteira de Python é igual à anterior. `gate_extension.py` é idêntico em bytes, SHA256 `c819810b5540747f0a0b7b07b36bb9d7f5e9dd868192ad7410ea15829c566a9e`. O parecer Tomita permanece no hash selado `e0a3762340e569a8095ae6a16719a7881d96a3ce87d534083371a6f2b31c2a42`.

Em `test_gate_extension.py:356–367`, o único controle novo é `GNS_order_normality_does_not_discharge_closed_Tomita_KMS_trace`: exige cinco declarações sobre transferência, positividade, monotonicidade e supremos, juntamente com as seis flags maiores falsas. O exame dos axiomas cobre os sete alvos, inclusive os dois auxiliares. Retirada somente a chamada nova, toda a AST do teste coincide com a anterior; nenhuma chamada antiga foi removida ou alterada. Há 37 chamadas literais contra 36 anteriores, contagem sintática distinta dos 70 controles registrados. Esse teste protege a fronteira declarada; não demonstra fechabilidade, KMS ou traço.

**Matemática e documentação.** A minuta foi lida integralmente. `MINUTA_NORMALIDADE_GNS.md:5–19` distingue corretamente SOT vetorial de norma de operador e normalidade em ordem de uma equivalência geral ultra-fraca/predual. O teorema de transferência recebe o limite forte a transferir; os teoremas finais de supremo **constroem** esse limite na mesma N, identificam-no com o supremo interno por unicidade e concluem supremo contra todos os majorantes em B(H_I). Conservam positividade, monotonicidade, direção e não vacuidade; não recebem normalidade ou fechabilidade como premissa. A quantificação de filtros/índices permanece a conferida no auditor DEV. Não se acrescentou uma alegação sobre famílias sem supremo interno dado.

O recorder e o verifier foram lidos integralmente e tiveram a AST analisada, sem execução. O texto principal do recorder (`158–178`) e os campos `GNS_normality_scope`/`GNS_general_predual_equivalence_proved` (`243–245`) conservam esse estatuto. O mecanismo previsto utiliza backup de bytes e substituição por temporário; o verifier prevê conferir hashes e prefixos. Isso é inspeção estática, não certificação de uma custódia ainda não executada. Os placeholders da minuta são dados de registro futuro, não evidência de execução. As escritas previstas nesses scripts não foram realizadas pelo revisor.

`DualCutLinearMap`, `ScalarBoundedCuts` e `ScalarCutNormality` foram confirmados ausentes do dicionário e das referências embutidas. A nota posterior do recorder os marca como DEV sem integração nem revisão independente e os conta separadamente. Seus teoremas, fontes, logs e binários não foram examinados ou recompilados para este adendo; a leitura da nota verifica somente essa separação de estatutos. O inventário I/O continua histórico, SHA256 `34133956b6a47012805003adfae734e7439b27e1f611466829af624b1857d89c`, ligado à fonte histórica `c712532dc079b832d9eb1ecc26ea50f2d49aa2c387afa435cc777eb302e96e09` conforme os campos da custódia anterior; não é inventário executado nem liberação da cópia atual.

| Artefato lido e congelado | SHA256 |
|---|---|
| integration.json | `348adf66aa20a1d30d85eeb7bbdae74706863994d7dac80cb737e057c7d410ab` |
| integrated_compile.json | `349a7049676c229e84821e3eb29709e01b6c98e6f1628ecb8a25f33e750ffcd3` |
| gate_tests.json | `1ee3193aab87d38d2b2755b8fbf084fffe8ed575652fa0c5e0726980083cbcfa` |
| kernel_incremental_evidence.json | `6a97ab6ea408b77fb34c1ad6312a336d254bf2e9189a7823e6cd2505ab86c257` |
| MINUTA_NORMALIDADE_GNS.md | `9eb90751476d9cd1e73443508dea0f5ba5a5667d2f57de763ab0dfa17560d899` |
| record_gns_normality_progress.py | `8b6a83d1ec8d5628d3d013a80572856221d6860c1d977eba3ab642cbc41421e6` |
| verify_gns_normality_custody.py | `caeb650ff7b4e3d4d718aea20a22701f444c01c24532c8acf976b714ef8a7ca3` |

Evidência verificável: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_normality_independent_20260912_081001_179488/final_integrated_20260912_082213_298026/verification.json>) e [supplemental_verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/gns_normality_independent_20260912_081001_179488/final_integrated_20260912_082213_298026/supplemental_verification.json>). Todos os artefatos pinados foram reconferidos antes deste append. Os 24 pareceres anteriores continuam iguais aos pins do manifesto; fontes autorais, originais, monólito, memórias e custódias não foram alterados.

**Conclusão delimitada:** a integração preserva a normalidade em ordem da mesma representação π_I:N→B(H_I), com o alcance dos sete alvos revisados. Fechabilidade do gráfico inicial, domínio escalar máximo, equivalência geral predual/ultra-fraca, Tomita fechado, KMS, traço e os demais fechamentos de gate/runtime não decorrem deste pacote. As observações de “sem integração” no primeiro estrato continuam retratando aquela execução DEV; este adendo acrescenta exclusivamente a inspeção integrada acima.

Preservação: backup imediato dos **12805 bytes** anteriores, SHA256 `d31269b07b5af9960e15e96b37286b63193e9f71be3a0553d8461e019bde3037`, em [REVIEW_GNS_NORMALITY.md.bak_20260912_082524_864105](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_GNS_NORMALITY.md.bak_20260912_082524_864105>). O novo parecer conserva esse prefixo byte a byte; nenhuma escrita saiu de `revisao/`.
