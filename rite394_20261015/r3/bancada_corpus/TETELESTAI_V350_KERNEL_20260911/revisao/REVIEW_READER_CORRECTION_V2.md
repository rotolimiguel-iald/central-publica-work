# Revisão do candidato V2 — dois leitores e insumos

2026-09-13T10:26:28.006006-03:00

**[REAL] Aceite restrito do candidato V2 para instalação e nova rodada. Nenhum P0–P2 pendente no patch e nos insumos examinados.** A execução futura ainda precisa produzir sua própria evidência; os resultados arquivados da rodada 02 não devem ser corrigidos à mão.

Candidato: `95e8cf8eb0b33c5d65e244195021b71977cca1a91836ef0d314964a8e2f97c43`. Fonte de partida: `fd611111866dc6ff30e9ed355b62bec32cdba505b742d550ffa3351ffd08e566`. A V1 `7dd78…` está superada, sem aceite para instalação.

- Reconstrução independente por bytes confirmou alterações somente em `prove_the_assembly_and_the_single_debt` e `prove_the_atlas_and_the_index`. AST: nenhuma função adicionada/removida; 922 embutidos, contratos, helpers de proveniência e avaliador principal inalterados.
- Reproduzi **38 verificações dos leitores**, mais **uma conferência do results.json staged: 39/39**. Foram avaliadas somente as duas funções puras e as duas guardas existentes extraídas por AST. Não executei/importei o monólito, preparador ou runtime.
- Montagem: 7/8 pendente e 8/8 passam; 8/8 sem bandeira é explicitamente pendente. Ausência de cada uma das nove chaves `red_clause_*` esperadas, bandeira acesa com oitava falsa, remoção individual dos quatro termos/pontes e `sorryAx` em cada um são rejeitados. O retorno não exige regredir a sete cláusulas.
- A V2 consome `v350_frontier_flag_has_proof` para oitava e Ato III. A função existente exige build/Audit válidos, termo e ponte de tipo exato com axiomas permitidos. Assim dois booleanos `True` sem os provedores não bastam. As pontes Lean já revisadas continuam no alcance **PRODUCT_TOWER**, sem nova identificação de J ou condição matemática.
- Atlas mantém suas doze entradas próprias obrigatórias; qgf/gpf globais são diagnóstico. A perda de cada entrada própria reprova; flag alheia não reprova Atlas. As avaliações sobre baseline e rodada 02 preservaram o **core inteiro**, incluindo flags.

**Insumos:** a conferência anterior de bytes dos dois REVOLVER e do documento Stokes foi reaproveitada; ambos FITS têm GALZONE. O quarto arquivo, `runtime_inputs_pending/results.json`, foi conferido independentemente contra o provedor externo já lido: SHA `bcb828091d4dff2bc5f6661b1878b4481e4727474bb7596913a99ff0d5c1198f`, 314.296 bytes, entrada `beta_acoustic_crosslock=-0.01696958621339946`. Os três primeiros estão em `manifest.json`; o quarto em `manifest_results.json`. Aceitos como preparação com os caminhos relativos registrados, sem instalação pelo revisor e sem predizer o resultado dos ritos após reposição.

Os P2 dos dois consumidores ficam corrigidos **no candidato**. A falha de preparação tem insumos existentes identificados e staged; seu efeito só será encerrado depois da aplicação e da execução correspondente. Não é aprovação retroativa de integração completa da rodada 02, nem dispensa do próximo autoteste ou de conferir seus selos.

Evidência própria: [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/reader_candidate_v2_review_20260913_102521_881121/verification.json>); [diff restrito](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/reader_candidate_v2_review_20260913_102521_881121/two_readers.diff>). Originais, ROOT/um.py, rodada 02, memórias e pareceres anteriores permaneceram intocados pelo revisor. Não foi repetida auditoria formal ampla.
