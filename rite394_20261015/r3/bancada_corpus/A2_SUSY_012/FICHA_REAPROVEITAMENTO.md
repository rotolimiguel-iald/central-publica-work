# Ficha de reaproveitamento — A2 SUSY 012

[REAL — leitura] [OPEN — ponte a construir]

2026-09-15T13:44:45.145796-03:00

Raiz exclusiva: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012

Consumidor: `TGLExt.susy_relative_gives_breuer`; proposta para exame de `gpf_H1_internal_susy_relative_gap_discharged`, sem editar bandeiras.

- Construir/adaptar reticulado de subespaços fechados invariantes sob o comutante, com projeções realmente em N. Identificar ordem/supremo/ínfimo e transportar tauA1 sem mudar o traço.
- Investigar polar limitado genérico dentro de N a partir de CFC.sqrt(star A*A) e extensão por norma. Se faltar, registrar enunciado exato e tentativas, sem assumir o resultado.
- Subaditividade por Kaplansky ou equivalente precisa prova; não embutir como hipótese e chamar de descarga.
- Consumir suporte regularFiniteSupport, kernel e gap de regularMinimalLock já pagos. Instanciar SusyRelativeData somente após preencher efetivamente suas obrigações.

## Fontes efetivamente consultadas

- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\REAPROVEITAMENTO_A2.md` — Contrato e decisões A2; primeira consulta. Leitura: integral. 11617 B; SHA256 `55f8d295d8cfaabe255b97d481cea95440ead7d62d1dcdcd21fc22138cb87242`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\AUDIT_NAMES_DELTA01.json` — 33 nomes sobreviventes; não usar auditoria antiga de 35 como selo corrente. Leitura: integral. 5375 B; SHA256 `83aefa5ef0fd4646d039801f4a9af423fe306f17be42ad2bc32a34365a46f9ec`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354FiniteEqualSplit.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 3193 B; SHA256 `72876fa3cf13dbd947ab02f1f4bd378c8d0dc7b2ed9beb39d98d7bed8079552e`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354FiniteTraceSupport.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 1897 B; SHA256 `7edd9fb4ef524e95b8c71d71bb7467512f9b89f7b04c21a5114686e894b1d323`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354NormalizedSplit.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 2452 B; SHA256 `5e90a1c08de4dc4593e65d9b8dde4a4bd5a1e074b68f8be357d17d25bbebe91a`.
- **DELIMITAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354PositiveTraceReader.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 4075 B; SHA256 `8133d88dcaf9ac3d58d739ecaf997312d7951be2c11fe1d08f21c8f90badf3ea`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354RegularMatrixCorner.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 2641 B; SHA256 `1f469df09c8ce12c58d7c8388dbedadb3fc9336a9c97757113693e7322e596f9`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354RegularSupport.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 6756 B; SHA256 `c80d99c73be4a676bcdc8cc21d476c249911d08f93fd914fda0d788019b1063e`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354SpectralThreshold.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 6267 B; SHA256 `9c33191344d07e4947a6d78a23ca0fc17e6b75206c13c511219f3a7a3b65085d`.
- **DELIMITAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\A2_012\src\TGLExt\V354TraceReaderWall.lean` — A2 atual; suporte/split/gap já construídos; leitor total fora desta tarefa. Leitura: integral. 2630 B; SHA256 `7882c9df649971790dfa9545e802df5b2b4e31c8bc16d536cecfd4d64203efcc`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\SusyRelativeGap.lean` — Consumidor TGLExt.susy_relative_gives_breuer; SubadditiveTraceData e SusyRelativeData. Leitura: integral. 8700 B; SHA256 `3aa058b5c4f098e3218ffed0bc8271a28947b56af81750019e1360754873e7f2`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\LocalBreuerGap.lean` — SemifiniteTraceData exige tau, monotonicidade e fidelidade; consumidor BreuerGapData. Leitura: primeiras 160 linhas. 20228 B; SHA256 `8ec73c7d9e703d6c775f53351a784ab98b27ad2dd3d253b79a3d34992e0d5d3d`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceContract.lean` — Mesmo cone positivo do regularCoreAlgebra P; traço A1 com tracialidade de quadrados. Leitura: integral. 5624 B; SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceConstruction.lean` — scalarInverseLimitTraceData, nunca substituir pelo traço dimensão. Leitura: declaração na ficha A2. 1095 B; SHA256 `f741525cfa335d89221834fdb01e3f3c6b8efa435b107f0a355cc5679fe06b40`.
- **RECUSAR_PARA_ESTE_ALVO** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\TheMasterFires.lean` — Ponte antiga vive em outro Hilbert e usa dimOrTop: não reutilizável para mesmo N/tauA1. Leitura: primeiras 110 linhas. 5834 B; SHA256 `862fc44434b23cb37a5eef412b6f829f84a0e0fe64fa58c8c7b260e8a8f32328`.
- **REUSAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\InvariantProjection.lean` — Projeções de subespaços invariantes; identidade entre comutação e invariância. Leitura: integral. 8798 B; SHA256 `fef79118c7b544f4d7d301e20e5c40f19db9fd8bb0e81ebe9c1418c532e99b40`.
- **ADAPTAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean` — IsStarProjection.mem_iff: pertinência em N via invariância sob N commutant. Leitura: declaração em ficha A2. 7086 B; SHA256 `bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86`.
- **ADAPTAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\Algebra\Module\ClosedSubmodule.lean` — Subespaços fechados; supremo é fecho da soma. Leitura: linhas 1-265. 14554 B; SHA256 `729757da7fb3b92dda878debbd0f7cda895e70089bae843acea79566aa534b9d`.
- **ADAPTAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\Projection.lean` — le_iff_mul_eq_left/right: ordem concreta das projeções. Leitura: integral. 5227 B; SHA256 `e7ca137f460a7e58e0585b32d45270321b3a46c94e4591ac3bf2471324940e16`.
- **ADAPTAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Normed\Operator\Extend.lean` — compLeftInverse/extendOfNorm: extensão contínua com estimativa efetiva; candidato ao polar. Leitura: linhas 136-225. 17432 B; SHA256 `726abde3ef827816dc3fca8a0003652a2131b49cdf5f7ad9176d4ccd4ceeef03`.
- **ADAPTAR** `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\Projection\Basic.lean` — starProjection, range/ker, composição sob inclusão. Leitura: busca por declarações. 33174 B; SHA256 `833c7b4ef410230086bd5b879ee51234e0e359e2aca3c9233d75cec5162fa5b2`.
- **CONTRATO** `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_012_a_passagem_da_acao_a_metrica.md` — Disciplina de reaproveitamento; tarefa lateral especificada pelo operador. Leitura: consulta com saída truncada; cláusulas pertinentes localizadas. 29534 B; SHA256 `a9cb2a7b812afc435f019d1af9089740ff38b22db76473126a5dfce454c7325e`.
- **CONTRATO** `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_012_RECIBO_E_ADENDO_001_quarta_face_e_sequencia.md` — Disciplina de reaproveitamento; tarefa lateral especificada pelo operador. Leitura: consulta com saída truncada; cláusulas pertinentes localizadas. 37599 B; SHA256 `679cdc94d90f4fea72dacfefb8a4ebf55a3ca87510d333b7c1b9c6c05c21f4e9`.

## Buscas e limites

- Busca SusyRelativeData/SubadditiveTraceData/Kaplansky no TGLExt A1 encontrou contratos e ponte ellTwo em TheMasterFires; esta usa outro traço.
- Busca polarDecomposition/PartialIsometry em fontes locais não encontrou fornecedor limitado geral. LocalBasePolarCommutation refere-se a polar antiunitário Tomita, objeto distinto.
- Mathlib ClosedSubmodule e Extend fornecem peças concretas. Busca ampla de projeções e leitura das ordens truncaram saída; não se declara exaustividade. Um caminho adivinhado LinearAlgebra/InvariantSubmodule.lean não existe; erro 2 preservado como falha de localização.
- Traço total e relação xy↔yx são trabalho do principal, fora do escopo.
- Nenhum reticulado ENNReal/dimOrTop substitui projeções do mesmo N e tauA1.
- Polar geral e subaditividade permanecem OPEN nesta ficha.
- Sem atribuir operador microscópico nem física a regularMinimalLock por nome.
- Revisão independente reservada à gerência/operador; esta é construção autoral.
