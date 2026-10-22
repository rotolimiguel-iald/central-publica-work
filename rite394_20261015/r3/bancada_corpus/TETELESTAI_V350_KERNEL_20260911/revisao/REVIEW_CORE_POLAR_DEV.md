# Revisão DEV core polar — estrato parcial

CORE_POLAR_DEV_REVIEW

Data: 2026-09-12T20:29:22.136749-03:00. **PARCIAL: quatro módulos/23 alvos conferidos; pacote pretendido de cinco/28 ainda não concluído.**

[REAL] Sem achados P0–P2 nas quatro fontes finais integralmente lidas e reproduzidas. `CorePolarInclusion` permanece excluído até aviso de fonte final; este estrato não certifica ainda a inclusão polar do core.

O fechamento deste estrato usa recompilação própria: quatro fontes e dois auditores (18+5 alvos), seis processos rc0. Os 23 tipos foram impressos com universos, os 23 conjuntos de axiomas são exatamente `propext`, `Classical.choice`, `Quot.sound`; os quatro `.olean` próprios são byte a byte iguais aos finais do autor. A estrutura auxiliar `FiniteFibreSet` também recebeu `#check`, sem inflar a contagem.

| Fonte DEV (kernel/TGLV350) | Alvos | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---:|---|---|
| FiniteSetFibreRead.lean | 6 | `0a51c8275ba7d68dd7e074cfacc3bf429698fa55b41b9df277d77825eb8b838c` | `c4962b3f3a33ecff6d667d9dfc67471e94c55c04e2f6212edd4a77a979516066` |
| FibreSlices.lean | 8 | `a3d7abbaf5d4202dddfd05e1c929124f68aa2e3a08a185deaf913b719fee82d4` | `394c466bae959df6144286ab141c1a87e95b2e0d2bdbe8c553b24ed52f06de4f` |
| ReducingCommutantTransport.lean | 4 | `53f5abe0d9023a3ec720353bea9dc279655f011dd9d5aafa5c66b02e7f46ccf9` | `e831150425300086e91c19953a5aee1331f4bdbdfcaef046f840088a2d074d37` |
| ScalarGNSGeneratorTransport.lean | 5 | `ad3622560d08a960a6cda5bc0320ddae9d16e7359a2578ce25eea6e99f57abc6` | `9f856605e3af85f595628258f8201a35b0e9ec03ad2b54357c5dd1ad0cf115cf` |

Conferências semânticas:

- `FiniteSetFibreRead.lean:12,32,40,48`: conjuntos mensuráveis de medida finita; norma do indicador com fator raiz da medida; adjunto igual à integral de Bochner vetorial. A família de leituras é conjuntamente separante; não se afirma injetividade de cada indicador nem se divide pela medida de conjunto nulo. A integrabilidade dos recortes é explícita, e a separação Lp não exige separabilidade global de H ou interseção AE não enumerável.
- `FibreSlices.lean:25,30,61,86`: coeficientes E_s* T E_t, orientações esquerda/direita e separação recuperam a igualdade do operador inteiro. A passagem ao bicomutante usa a estrela de ambos os geradores; não presume que T seja uma fibra constante.
- `ReducingCommutantTransport.lean:15,19,30,55`: extensão por zero no complementar e projeção do subespaço redutor. Invariância para a e a* vem da mesma representação estrela. `hgen` é hipótese explícita do auxiliar genérico, sem ser ocultada; a extensão por zero não é apresentada como homomorfismo unital.
- `ScalarGNSGeneratorTransport.lean:15,29,43,68`: amplificação seguida da conjugação pelo implementador unitário efetivo de `DualOrbitVonNeumann` transporta a geração. Fechamento dos geradores por estrela inclui t↦−t. A aplicação final paga `hgen` por `dualOrbit_core_commutation_from_generators`; o tipo impresso recebe somente P, T e a comutação nos geradores. A representação restrita é por definição a mesma `scalarGNSRepresentation` no mesmo `ScalarGNSHilbert`.

Limite do ponto sobre J: estas quatro fontes não aplicam ainda conjugação dupla pelo J concreto. Conferir essa composição e a inclusão Jπ(N)J⊆π(N)′ permanece tarefa do quinto módulo. Mesmo essa inclusão não será confundida com igualdade de comutantes, KMS, identificação de Δ^it, traço ou promoção de flags.

Proveniência e evidência:

- `core_polar_slices_independent_20260912_201934_315097`: manifesto `ae522fd3b45f7e2b7538ec08233a421f32cd85959c676a36450e302c8d5990cb`; `compilation.json` `7fd307a19bc28a5e9e8d1adde433e53cc213b9baace680046b700f10c42688a9`.
- `core_polar_generator_independent_20260912_202528_426668`: manifesto `d484180521f04348bb8c2a3fb0ba8fe0d06d900ca73753561a8c7232537d8a69`; `compilation.json` `bcca053608fd112fbff7e7d1ff62232dcdb2069455d6d26487a2fad6b77bfe73`.

As árvores copiaram respectivamente 306 e 388 dependências de projeto das árvores próprias anteriores; união nesta inspeção: 388 módulos. Fontes/binários foram relidos e pinados. O LEAN_PATH contém somente o build isolado e oito diretórios externos de pacotes readonly. Nenhum build autoral de projeto entra na busca; bibliotecas herdadas não foram recompiladas neste estrato. Não houve nova importação de binário canônico de projeto. Os lemas Mathlib de integral/indicador e separação Lp foram lidos e receberam pins adicionais em `semantic_inspection.json`.

Mãe `base_polar_custody.json`: `ea25a6ecfa766d1c460b32cff1fdba4e86c44cf8381f1ad8a83ccac9603557c0`. A verificação dos 34 pares de memória/backup e sua preservação consta dos dois manifestos/compilações. Pareceres antigos, fontes e binários autorais, gate e cópia um.py permaneceram com seus hashes pinados; não se executou monólito, helper autoral ou recorder.

Os 5 registros autorais rc1 anteriores e seus streams foram preservados em `author_history/` e excluídos da aceitação, inclusive prints contaminados por `sorryAx`. Somente fonte final pinada com rc0 e auditor próprio verde sustenta a conclusão. Logs finais aceitos:

- `FiniteSetFibreRead_20260912_201002_063704.json` — SHA `42098a580ae419d5fb3e9f4378c3141dff4f48291575c2991f3a657b8dd94414`.
- `FibreSlices_20260912_201526_180864.json` — SHA `2c8f0409600f74691f380a918de6b93453da2478c392dc9f0a79d17932206ee9`.
- `ReducingCommutantTransport_20260912_201358_264616.json` — SHA `a5c8c823fa9b758dc3646a5133930fb9ff1686b49bf690063f556ba2c193a135`.
- `ScalarGNSGeneratorTransport_20260912_201757_089240.json` — SHA `3919d9346818a3a474c0d8e7dc2a73308b72e5137ab80b5488348b075cfc78d5`.

[OPEN neste parecer] Falta a fonte final de `CorePolarInclusion`, o manifesto/relatório final do lote e o auditor cumulativo de 28 alvos. Não há integração ou custódia nova certificada por este documento. O próximo estrato deverá preservar estes bytes por backup e append.

---

## Adendo final — cinco módulos/28 alvos

2026-09-12T20:36:14.979780-03:00 — **CORE_POLAR_DEV_REVIEW concluído para o pacote DEV. Integração pendente.**

**Sem achados P0–P2.** O estrato parcial acima permanece como histórico. Os cinco módulos, manifesto, relatório e helpers finais foram integralmente lidos. A aplicação concreta demonstra Jπ(N)J⁻¹⊆π(N)′ no mesmo `ScalarGNSHilbert P`, com `scalarGNSRepresentation P` e o J efetivo `scalarTomitaPolarFactor P`; não sobra hipótese `hgen`, de normalidade ou de densidade a fornecer pelo chamador.

`CorePolarInclusion.lean:14,25` deriva a involutividade da conjugação a partir da involutividade explícita de U e preserva a ordem dos produtos sob conjugação. O passo de comutação apenas troca os dois operadores da relação. Em `:34`, `scalarTomitaPolarFactor_involutive P` paga essa hipótese para o J concreto; os dois ramos dos geradores usam exatamente `base_polar_commutes` e `scalarTomitaPolar_regular_generator_commutes`. Em `:52`, a geração já demonstrada fecha a comutação para quaisquer A,B∈N. Em `:58`, aplicar também B* e `map_star` fornece a pertinência ao comutante estrela da imagem de π. Não há circularidade com a inclusão pretendida nem inferência da inclusão inversa.

A reprodução acumulada tem **cinco fontes + três auditores próprios (18, 5 e 28 alvos), oito processos Lean rc0**; nenhum módulo verde foi recompilado. O auditor final imprimiu os 28 tipos com universos e exatamente os 28 conjuntos de axiomas do manifesto, todos restritos a `propext`, `Classical.choice`, `Quot.sound`. Os 23 tipos anteriores coincidem com os auditores já lidos. Os lemas Hilbert genéricos estão no universo declarado `H : Type`; não se afirma aqui uma generalização adicional de universos. Os cinco binários próprios coincidem byte a byte com os finais do autor.

Quinto módulo: fonte `c6168763788c84e31e91bb7f1fbef04d462b4fdeec7416d0d4bd0c9085fc76db`; `.olean` próprio=autor `14f21dcca07261ae8b850e798f0a48b9ecbdb028f5f070a19aea3dbe752e1c73`; log `CorePolarInclusion_20260912_202528_997974.json`, SHA `570d1f90619171ce740eeaedc1d1258b467d2af497832b223c69a507ef2d7af2`; stdout autoral `cc15da7bbdab5c1e8830c113a59da63cdfae5b9a240824a5f77d67e8ce4dd56e`. Seus cinco tipos não contêm premissa nova sobre P além do próprio `SiteProfile`.

Evidência final em `core_polar_independent_20260912_203148_639288`: `manifest.json` SHA `4288d2379828e7568a21e1322792814cab0ce8b33e400d7ce36ee0ad87bc09fc`; `compilation.json` SHA `b1e2c0bd7b288ad11fb0a5c50684a78927ee4f93d105446929e6d1cc65582d4f`; auditor28 stdout SHA `7ccad1bb3a0f429644c8d61353ed8d472dc63d8852baa52ea3b93619928a1d4e`; `verification.json` SHA `70ebab700dda504aa5858d48f97b82c2e17b4f0f08cf4531e3554a191c3057c7`.

A árvore final contém 617 dependências pinadas, incluindo os quatro módulos novos já reproduzidos. Foram reutilizadas somente cópias de projeto da revisão e oito caminhos externos readonly de pacotes. **Limite herdado:** 150 dependências transitivas conservam a proveniência canônica congelada/verificada na revisão anterior da base; não receberam recompilação independente nesta etapa. Não se apresenta o lote como reconstrução independente de toda a biblioteca. Um ensaio de preparação própria parou antes de chamar Lean por catálogo incompleto (`ScalarRegularPolarCommutation`); seu registro foi preservado, e a referência à árvore própria `regular_polar` resolveu a localização. Nenhum build autoral foi adicionado ao LEAN_PATH.

Manifesto final `core_polar_draft_status.json`: `eea8ca22c11fca4cd372de7b1605906221a03bbc641af422a0ae498490848e75`. Relatório `RELATORIO_INCLUSAO_POLAR_CORE_DEV.md`: `f05a6e4983df28c80f742e8d1571f5ef39a24263d5e2743a13a32db5472b79b4`. Todos os pins de fonte/binário/log/streams dos cinco foram relidos e confrontados ao manifesto. Os 6 históricos autorais rc1, inclusive o primeiro `CorePolarInclusion` com `sorryAx`, permanecem excluídos; a aceitação usa exclusivamente as versões finais e os processos próprios verdes.

Inspeção estática dos helpers, sem execução:

- `make_core_polar_helpers.py` e `record_core_polar_draft.py`: texto consistente com operadores de inserção E_S, admitindo medida zero; totalidade conjunta, mesmos N, π, J e H_I; pins finais e estado DEV pendente explícitos.
- `prepare_core_polar_stage.py`: cinco nomes/28 alvos; parent e 34 memórias verificados antes de alteração; exige leitura humana (`--review-read`) e marcador. A transformação textual foi simulada em memória e parseada: batch 463→491, cinco módulos na ordem de dependências antes das raízes, um grupo adicional de fronteira; nada disso foi aplicado pelo revisor.
- `record_core_polar_progress.py`: exige também parecer integrado, relê pares fonte/binário, preservação AST fora do dicionário, Audit atual/histórico e 34 superfícies da mãe. Cada append prevê backup imediato de bytes, prefixo, crescimento, temporário e substituição após conferir o estado anterior. Essa atomicidade é por arquivo; não se afirma transação indivisível das 34 memórias.
- `verify_core_polar_custody.py`: relê fontes/oleans dos registros integrados, fontes DEV e os pares memória/backup. Os resultados e contagens futuros dependerão de execução e revisão integrada próprias; a inspeção estática não declara nova custódia gravada.

Pins integrais dos cinco scripts e verificações estáticas: `helper_static_inspection.json`, SHA `e725a326fdd3743c9b8d8a94654d65596e0ae4a3b4a9365b01b14985d9f6fbd7`. Parent `ea25a6ecfa766d1c460b32cff1fdba4e86c44cf8381f1ad8a83ccac9603557c0`; cópia ainda `a350b674810a40693bc9b6fe4be2fc401757a9045747e096621f077b317cfa40`. As 34 memórias e respectivos backups permanecem nos pins da mãe; seis flags falsas, gate e monólito inalterados. Nenhum helper autoral ou monólito foi executado/importado por esta revisão.

**Escopo DEV encerrado.** Permanecem fora da conclusão: inclusão reversa/igualdade global de comutantes, identificação de Δ^it com o fluxo/KMS, traço, Three Locks, obrigações físicas, consumo por certificados e runtime. Essas aberturas não são defeitos deste incremento. O marcador deste documento não substitui a leitura humana nem autoriza antecipar resultados de integração.
