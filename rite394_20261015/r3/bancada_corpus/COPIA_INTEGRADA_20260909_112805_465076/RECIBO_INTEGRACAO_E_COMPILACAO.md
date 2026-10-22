# Cópia integrada — resultado de 09/09/2026

[REAL] A cópia um.py contém seis módulos acrescentados mecanicamente: SelectionAngleReconstruction, SelectionOutcomeRecord, ScatteringOutcomeRecord, SelectedAmplitudeGeometry, ModularOpticalIdentity e ConeVolumeReconstruction.

A tabela embutida passou de 605 a 611 entradas. Só mudaram a tabela, seus dois agregadores e as seis entradas novas. O restante da AST e os bytes externos à tabela são iguais; flags, gate e sentinelas permanecem idênticos. As seis strings foram extraídas novamente e comparadas aos textos transpostos.

## Prova compilada da integração

Resultado: PASS_TRANSPOSED_SCOPE.

- 100 teoremas acrescentados à auditoria da cópia: 93 desta etapa e sete da bancada angular anterior.
- 138 declarações nos seis módulos (100 teoremas e 38 demais), todas auditadas no trio.
- TGLExt.lean efetivamente extraído da cópia compilou.
- TGL/Audit.lean efetivamente extraído da cópia compilou: 4586 relatórios de axiomas, 4579 nomes distintos, sentinelas presentes.
- Auditoria dedicada dos teoremas novos: 100/100.
- Nove processos Lean com retorno zero; 0 linhas de warning.
- 587 módulos canônicos locais fornecidos por cópias binárias isoladas. Entradas, dependências copiadas e fontes originais lidas permaneceram iguais por hash.

A build válida é BUILD_TRANSPOSED_20260909_113239_271293. O plano exato está em BUILD_PLAN.json e os resultados por processo em TRANSPOSED_RESULT.json. A primeira falha de resolução do namespace TGLExt e o plano intermediário não executado foram preservados.

## O que este recibo atesta

A nova cópia é sintaticamente válida, conserva a parte Python fora da tabela e carrega fontes que compilam juntas com seus agregadores. O registro de espalhamento usa probabilidade do ramo, possui leitor próprio e permite reconstrução da forma principal por peso mais rótulo. O leitor de reflexão da base continua separado; ver ADENDO_REGISTRO_ESPALHAMENTO na bancada.

A geometria selecionada realiza uma família concreta de ondas; ConeVolumeReconstruction fornece unicidade de métrica sob os dados/contratos expressos. O módulo óptico demonstra identidades unitárias no setor formal. Não são afirmações de quitação geral de todas as hipóteses gravitacionais.

Não executei nem importei o um.py original ou a cópia. Não foi produzida rodada de runtime, selftest integral, artigo atualizado ou selo da cópia. As dependências canônicas não foram reconstruídas integralmente; a Mathlib foi usada em seus binários existentes. Não há promoção a confirmação física nem novas flags JSON individuais.

## Integrador e revisão

Scripts: INTEGRADOR_LOTE_20260909_112210_127268/integrate_approved_copy.py e build_transposed.py. O primeiro usa configuração de hashes aprovados; o segundo prepara e executa apenas Lean em uma build nova.

O crítico independente relatou concordância da AST e dos bytes: seis chaves novas, nenhuma removida, apenas agregadores antigos alterados, flags/gate/sentinelas iguais. Sua revisão foi estática; ele não reexecutou a compilação. O original foi conferido novamente ao gerar este recibo e permanece idêntico ao snapshot.
