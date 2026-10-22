# A1 — revisão final da forma dual estendida na base

2026-09-14T08:48:20.856186-03:00

**[REAL — reprodução independente] Aceito o módulo delimitado de 14 declarações, sem achados P0–P2. Há transporte efetivo para formas afiliadas à base, incluindo valores infinitos. A1(b) permanece NÃO PAGO.**

Li integralmente o [candidato final](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351ExtendedBaseDualWeight.lean>), a ficha MD/JSON e os logs final/recusado, retomando as interfaces já examinadas na [consulta conceitual](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/CONSULTA_A1_RESTRICAO_FORMAS_BASE.md>). Esta última e os pareceres A1 anteriores permanecem intactos. Nenhuma integração ou alteração de gate faz parte deste aceite.

**Tipos e provas conferidos — locadores na fonte final:**

| Linhas / declarações | Conclusão |
|---|---|
| 16–35, `fixedFormOnBase` | Restrição por `testVectorIsometry` entre Hilberts distintos, com os campos construídos diretamente. A continuidade transporta semicontinuidade inferior. Para TODO U unitário em M′, `fibreRepresentation` fornece o unitário amplificado; `dualFixedCore_eq_amplified_base` descarrega sua comutação com TODO F e `fibre_testVector` conclui a invariância. Nenhuma afiliação residual é recebida como premissa além da afiliação de Q a F. |
| 39–49, `baseDualWeight`, valor e avaliação escalar | Saída `AffiliatedPositiveForm (theFactorObject P)` para todo input em `PositiveCoreInput P`, sem hipótese de limitação do output ou finitude de valor. A avaliação no mesmo `hOmega P` é o mesmo `scalarDualWeight`, em ENNReal. A igualdade por `rfl` é coerência de definições; o ganho matemático está na afiliação demonstrada acima. |
| 51–85, zero/soma/escala/bimódulo/ordem | As leis são transportadas das já existentes. Escala NNReal preserva 0·∞=0. No bimódulo, o input usa o **mesmo** `fixedBaseEquiv P B`, cuja aplicação é `fibre B.val`; o output usa B na base. Não há troca de representação por homonímia. Monotonia não é apresentada como reflexão genérica de ordem. |
| 87–96, fidelidade | A forma de saída zero implica sua avaliação no vácuo zero; `scalarDualWeight_faithful` conclui A=0. Não há suposição de injetividade de uma restrição arbitrária de formas. |
| 98–115, normalidade | Supremos internos de positivos crescentes em N; índice em universo arbitrário, preordenado dirigido e não vazio. O IsLUB alvo é demonstrado pela igualdade pontual do integral em `testVector v`, testando qualquer majorante no cone da base. Não é inferido apenas da monotonia e não recebe SOT como premissa. |
| 117–122, caso limitado | Compatibilidade correta com o valor-base D sob a hipótese explícita `hrep` em todos os vetores regulares. Este lema não constrói D nem acrescenta sua positividade: a existência positiva para outputs limitados vem dos fornecedores anteriores. |
| 126–138, infinito e média | A unidade tem valor ∞ em TODO v≠0, usando a norma da isometria; zero permanece zero. O quadrado da mesma média de comprimento 1 vale 1 no mesmo vácuo, com Haar já herdado. Não há `toReal`, supressão do setor infinito ou constante de normalização nova. |

**Recompilação e proveniência.** [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/extended_base_independent_20260914_084553_472856/compilation.json>) e [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/extended_base_independent_20260914_084553_472856/verification.json>).

- Módulo próprio **rc0**, sem avisos, 24.439s; auditor próprio **rc0**, sem avisos, 19.321s. `#check` com universos e `#print axioms` conferem exatamente **14 declarações (2 definições e 12 teoremas)**, somente `propext`, `Classical.choice`, `Quot.sound`. Sufixos de universo são registrados no stream e normalizados no parser. `.olean` próprio idêntico byte a byte ao autoral.
- O manifesto novo tem **359 pares** fonte/objeto: 358 já disponíveis e uma nova cópia, `V350FixedBaseEquivalence`. Os hashes de fonte, build autoral e objeto de origem foram comparados. A árvore isolada contém **377 objetos de projeto**: 375 dependências pinadas herdadas da revisão A1 + o contrato A1 recompilado por este revisor + FixedBaseEquivalence herdado. Esse conjunto cobre também o import do contrato; 359 não é a contagem total do build usado nesta reprodução.
- As 375 dependências continuam sendo binários herdados da origem anterior, agora relidos e copiados por hash; **não** afirmo tê-las reconstruído independentemente. FixedBaseEquivalence também não foi recompilado nesta rodada. LEAN_PATH de projeto aponta somente à árvore própria; pacotes externos são herança read-only. Não recompilei Mathlib nem o corpus.
- Run autoral aceito: `20260914_084253_409522`, fonte/snapshot/stream conferidos. A tentativa `084206_268140` retorna rc1 por coerção entre `testVector` e `testVectorIsometry` no controle infinito; o `sorryAx` impresso ali foi recusado integralmente. A prova final por norma elimina o erro e foi reproduzida; nenhum verde parcial da tentativa antiga entrou no aceite.
- A ficha contém **11 registros (incluindo o consumidor)**, todos com hash conferido. As duas capturas adicionais de busca e os quatro manifests de buscas herdadas tiveram os pins relidos. Não reexecutei buscas nem reivindico inventário universal de fornecedores. O registro da ficha antecede a tentativa final, conforme sua data declarada e o histórico de tentativas; não foi produzida nova camada Python de aplicação.

**Consumidor e alcance parcial.** O alvo de reaproveitamento é coerente com A1: esta é uma ponte intermediária da identificação `regular_scalar_weight_is_dual_weight`, preparando a perturbação do peso. Ela **ainda não preenche um campo de `RegularCoreTraceData` nem fornece um habitante desse contrato**. Importar o contrato não altera esse fato; as provas não o recebem como hipótese.

A estrutura alvo é uma forma estendida sobre vetores da base, com invariância pelo comutante. O arquivo não prova isomorfismo genérico de cones, representação em funcionais positivos do predual, independência de decomposições desses funcionais, implementação modular, KMS ou existência do traço. O próximo elo ainda é identificar esses outputs com o cone positivo estendido usado pelo consumidor e compatibilizar operações/avaliações; só depois a rota modular/gerador/perturbação fornece τ. As recusas do contrato A1 e sua auditoria continuam aceitas; **A1(b) não se fecha neste módulo**.

A ressalva da consulta sobre semifinitude permanece válida: para ν não tracial, o domínio n_ν fracamente denso é a condição pertinente; não cobrar dele automaticamente a fórmula tracial de todos os minorantes positivos finitos. O módulo atual não prova um novo teorema de semifinitude nem promete fazê-lo. O campo mais forte do contrato de τ permanece intocado. GNS e fecho do S já identificados não foram reabertos.

**Pins finais lidos:**

| Artefato | SHA-256 |
|---|---|
| Fonte | `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87` |
| Binário próprio = autoral | `75d88c1f7a929319f789cc7f7da9d2fd49995f9b2ef3128aaca65c5ff7827c81` |
| Ficha MD | `32612e27914a462514fd623cc7dfcd62d4a46042e5d4c34c66b1874f5f8b08ca` |
| Ficha JSON | `f2f75fb0cf675c328eccdbccb9bcb220b5d1dca82e6e8ca581a5ea1b512aa44c` |
| Manifesto 359 dependências | `9f55f56e9075f11ba3b119770c8a698981a9ab7a9bac74f1a15ee08e7c2d6125` |
| Compilação independente | `ba30922cf32eed1fafadb7c366fdeaaf52bfaa9459eb7258430d8a22a220e8ff` |
| Verificação independente | `f99729f44d264ceba34f44d58388fb24e35ae92e7cae8404738743e5121a5328` |
| `um.py` preservado | `95e8cf8eb0b33c5d65e244195021b71977cca1a91836ef0d314964a8e2f97c43` |

Somente `revisao/` recebeu arquivos. Fonte e binário autorais, programa, memórias, Atlas, consultas e pareceres anteriores não foram alterados. Nenhum monólito, integrador ou recorder autoral foi executado. Revisão do delta encerrada, sem bloqueio ou análise necessária pendente neste escopo.
