# Recibo da cópia integrada — 14 módulos

[REAL — integração estática e compilação] Concluída a cópia nova
[um.py](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/um.py>), sem executar nem importar o programa.
Ela acrescenta ao original 14 módulos, 236 teoremas e 77 outras declarações
(definições, estruturas e abreviações). Em relação à cópia anterior de sete módulos,
são 7 módulos, 121 teoremas e 37 outras declarações adicionais.

A [cópia anterior](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_114310_143963/um.py>) foi preservada.
O original canônico, seu snapshot nesta pasta e os hashes de todas as fontes foram novamente conferidos
ao concluir a build. Nenhum original foi alterado.

## O que foi modificado

Somente a tabela _EMBEDDED_KERNEL_FILES recebeu alterações:
605 → 619 arquivos embutidos.
As fontes anteriores foram preservadas; TGLExt.lean recebeu os imports e TGL/Audit.lean
recebeu os novos prints de axiomas. Nenhuma entrada ou print anterior foi removido.
Os imports entre módulos novos foram transpostos mecanicamente para o prefixo TGLExt.
A normalização de fim de linha e a recuperação de todas as strings foram verificadas.

Todo o AST e todos os bytes fora dessa tabela permaneceram iguais ao original.
Flags, gate, sentinelas e lógica de execução foram preservados.
O controle AffineSamplingObstruction entrou como fonte auditada, sem flag de fechamento.

## Verificação concluída

- 17 processos Lean terminaram com exit 0 e zero warnings.
- Os 14 módulos transpostos auditaram 313 declarações.
- TGLExt.lean e TGL/Audit.lean foram extraídos da cópia e compilados, não reconstruídos à mão.
- O Audit completo emitiu 4722 registros (4715 nomes distintos), com todas as sentinelas verificadas.
- O auditor dedicado conferiu 236 teoremas distintos, exatamente uma ocorrência por nome.
- Os axiomas impressos pertencem ao trio propext, Classical.choice e Quot.sound.
- A fronteira de entradas da build permaneceu inalterada antes/depois.

A revisão independente do agente /root/review_remaining_hypotheses confirmou separadamente
AST/bytes, as 14 fontes e transposições, a preservação de entradas anteriores e os
236 prints únicos. Essa revisão foi estática, sem recompilação independente do lote.

## Módulos

| Módulo | Teoremas | Outras declarações |
|---|---:|---:|
| [SelectionAngleReconstruction](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/SelectionAngleReconstruction.lean>) | 7 | 2 |
| [SelectedAmplitudeGeometry](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/SelectedAmplitudeGeometry.lean>) | 17 | 10 |
| [ModularOpticalIdentity](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/ModularOpticalIdentity.lean>) | 17 | 4 |
| [ConeVolumeReconstruction](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/ConeVolumeReconstruction.lean>) | 12 | 3 |
| [GeneralMetricEinstein](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/GeneralMetricEinstein.lean>) | 15 | 2 |
| [GeneralAngularTensorCodec](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/GeneralAngularTensorCodec.lean>) | 32 | 12 |
| [GeneralLinearizedGauge](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/GeneralLinearizedGauge.lean>) | 20 | 7 |
| [FisherInformationTensor](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/FisherInformationTensor.lean>) | 22 | 5 |
| [SelectionOutcomeRecord](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/SelectionOutcomeRecord.lean>) | 24 | 11 |
| [GeneralMetricClausius](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/GeneralMetricClausius.lean>) | 6 | 3 |
| [ProbabilityRecordState](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/ProbabilityRecordState.lean>) | 19 | 6 |
| [AffineSamplingObstruction](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/AffineSamplingObstruction.lean>) | 11 | 2 |
| [ScatteringOutcomeRecord](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/ScatteringOutcomeRecord.lean>) | 23 | 8 |
| [FisherCorrectedEinstein](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/transposed_sources/TGLExt/FisherCorrectedEinstein.lean>) | 11 | 2 |

## Diagnósticos e limites

Três nomes curtos se repetem entre namespaces diferentes:
phaseReading, tensor_quad_smul, decodeRecord.
O diagnóstico foi preservado em [DIAGNOSTICO_NOMES_CURTOS.json](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/DIAGNOSTICO_NOMES_CURTOS.json>).
Não são colisões de nomes completos em Lean. O índice Python não foi executado;
nenhuma correção de índice foi presumida ou introduzida.

[REAL — escopo matemático] A nova correspondência continua condicionada às leis de matching declaradas.
O controle afim demonstra que aplicar universalmente o mesmo campo por P(x+t·v) restringe
a entropia e o balanço nulo de Ricci; ele não prova planura nem refuta a TGL.
O tensor de Fisher é positivo semidefinido e não é identificado com a assinatura lorentziana.
Conservação de fonte efetiva e produção física dos registros não são deduzidas por este integrador.

A build usou 587 módulos canônicos locais copiados por bytes para um overlay novo;
1189 arquivos compõem sua fronteira medida.
As dependências canônicas transitivas não foram integralmente recompiladas, e as dependências
Mathlib transitivas não foram todas individualmente medidas.
Não houve rodada de runtime, selo, rito físico, alteração de gate ou confirmação física.

## Hashes lidos ao concluir

| Artefato | Bytes | SHA-256 |
|---|---:|---|
| Original canônico | 9852172 | f1f330e24120f9bece3473bfd8af59038bb9dcd09af079d0ddaae7bfb228503a |
| Cópia anterior, sete módulos | 9917128 | 35a561dd9ae0e4019b94cb20056801d819127ed35a9679f9fa6028b8d051b86c |
| Nova cópia, 14 módulos | 9997895 | e4bba7b18002d91c8cccc8b68ba8933cac2b1cba49039735c5c2ffae50295d5e |

Recibos:
[INTEGRATION_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/INTEGRATION_RESULT.json>) ·
[BUILD_PLAN.json](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/BUILD_TRANSPOSED_20260909_123213_271199/BUILD_PLAN.json>) ·
[TRANSPOSED_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/BUILD_TRANSPOSED_20260909_123213_271199/TRANSPOSED_RESULT.json>).

Os scripts e configuração estão em
[INTEGRADOR_LOTE14](<C:/IALD/Central de Patentes/Chatgpt/INTEGRADOR_LOTE14_20260909_123141_078980/CONFIG_14_MODULOS_APROVADOS.json>).
A consulta inicial de preparação que falhou por decodificação do caminho foi documentada;
a correção usou UTF-8 explícito. Esta geração e sua build transposta passaram na primeira execução.
As falhas anteriores dos módulos permanecem em suas respectivas pastas de bancada.
