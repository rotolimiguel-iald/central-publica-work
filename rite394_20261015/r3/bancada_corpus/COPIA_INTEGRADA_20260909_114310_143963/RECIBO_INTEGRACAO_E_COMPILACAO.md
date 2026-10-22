# Cópia integrada final — sete módulos, 09/09/2026

[REAL] A sucessora um.py está congelada nesta pasta. A cópia anterior de seis módulos e o acervo original foram preservados e conferidos por hash ao final.

A tabela embutida passou de 605 a 612 entradas. Somente duas entradas anteriores, TGLExt.lean e TGL/Audit.lean, recebem adições; sete entradas são novas. O restante da AST e os bytes externos à tabela são iguais. Flags, gate e sentinelas permanecem idênticos. As sete strings foram extraídas novamente e comparadas aos textos transpostos.

| Módulo | Teoremas | Outras declarações |
|---|---:|---:|
| SelectionAngleReconstruction | 7 | 2 |
| SelectedAmplitudeGeometry | 17 | 10 |
| ModularOpticalIdentity | 17 | 4 |
| ConeVolumeReconstruction | 12 | 3 |
| GeneralMetricEinstein | 15 | 2 |
| SelectionOutcomeRecord | 24 | 11 |
| ScatteringOutcomeRecord | 23 | 8 |

## Verificação efetivamente realizada

Resultado: PASS_TRANSPOSED_SCOPE.

- 115 teoremas acrescentados à auditoria da cópia, sendo sete da bancada angular anterior e 108 desta etapa.
- 155 declarações nos sete módulos (115 teoremas e 40 demais), todas auditadas no trio.
- Os sete módulos foram recompilados nesta rodada; não foram reutilizados os seis binários da cópia predecessora.
- TGLExt.lean extraído da cópia compilou.
- TGL/Audit.lean extraído da cópia compilou: 4601 relatórios, 4594 nomes distintos, sentinelas presentes.
- Auditoria dedicada dos teoremas novos: 115/115.
- 10 processos Lean com retorno zero; 0 linhas de warning.
- 587 módulos canônicos locais foram fornecidos por cópias binárias isoladas. Entradas, cópias e fontes originais lidas permaneceram iguais por hash.

A build válida é BUILD_TRANSPOSED_20260909_114324_004906. BUILD_PLAN.json contém comandos, ambiente e hashes exatos; TRANSPOSED_RESULT.json contém os resultados por processo. As falhas e os planos anteriores da cópia predecessora continuam preservados.

## Conteúdo e alcance

O registro de espalhamento usa o peso do ramo, possui leitor próprio e permite reconstrução da forma principal por peso mais rótulo. O leitor de reflexão da base tem outra convenção; ambos têm suas imagens e identidades de retorno próprias. A referência de estado do espalhamento é rhoOut, sem confusão com a densidade inteira plusDensity.

SelectedAmplitudeGeometry realiza uma família concreta de ondas. ConeVolumeReconstruction fornece unicidade de métrica sob os dados e contratos expressos. GeneralMetricEinstein acrescenta a reconstrução condicional a partir da métrica e de suas hipóteses, construindo a inversa e retirando a exigência de uma tetrada independente nessa passagem. ModularOpticalIdentity trata identidades unitárias no setor formal. O alcance acompanha os enunciados e suas hipóteses; não constitui promoção automática a confirmação física.

## Limites da integração e do índice

Nenhum um.py foi executado ou importado. Não houve rodada de runtime, selftest integral, emissão de artigo ou selo da cópia. As fontes das dependências canônicas não foram reconstruídas integralmente; Mathlib foi usada em seus binários existentes. Não foram acrescentadas flags JSON individuais.

O índice operacional conserva uma ambiguidade de nome curto: phaseReading em ChatgptAudit.Angular034 e em ChatgptAudit.SelectionAngle. São funções de tipos e namespaces distintos; não há colisão Lean. A revisão estática confirma que o algoritmo preserva a primeira entrada e marca ambiguo. Consultar os nomes completos e conservar esse diagnóstico. O índice não foi executado nesta rodada.

O crítico independente confirmou hashes das sete fontes, AST e bytes fora da tabela idênticos, somente agregadores antigos alterados, nenhuma entrada retirada e exatamente uma entrada nova de auditoria para cada um dos 115 teoremas. Sua revisão foi estática; a compilação acima foi executada pela bancada.

## Reprodução

Os scripts integrate_approved_copy.py e build_transposed.py estão em INTEGRADOR_LOTE_20260909_112210_127268. CONFIG_APROVADA.json nesta pasta fixa o snapshot de sete módulos autorizado. O primeiro script gera uma pasta nova; o segundo prepara uma build nova e chama somente Lean. A cópia e o original continuam sem execução.
