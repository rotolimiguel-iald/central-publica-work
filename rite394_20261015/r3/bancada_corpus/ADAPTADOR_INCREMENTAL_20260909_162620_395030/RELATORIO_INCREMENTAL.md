# Build incremental preparado — 45 módulos reutilizados e 18 novos

[REAL] Preparação concluída sem executar Lean e sem executar/importar um.py. O build sequencial em curso permaneceu intacto; seus logs e seus binários novos de saída não foram lidos. Foram usados apenas o plano atual congelado, suas fontes .lean e as entradas predeterminadas do overlay de dependências.

O diretório novo BUILD_INCREMENTAL_20260909_162634_176093 contém as 66 fontes do plano atual: 63 módulos e três agregadores/auditorias. Foram copiados 588 artefatos do overlay canônico já materializado e 90 artefatos produzidos pelo build anterior dos 45 módulos (.olean e .ilean; nenhum .olean.server/.olean.private adicional estava presente para estes módulos).

## Compatibilidade conferida

- As 45 fontes Lean transpostas têm bytes exatamente iguais entre os dois builds. Não foi usada normalização de fim de linha nesta comparação.
- O recibo anterior é PASS_TRANSPOSED_SCOPE, com 48 processos válidos, exit 0, nenhum aviso e axiomas no trio permitido. O hash do plano anterior coincide com aquele registrado no recibo.
- Todos os 1.247 registros de dependências externas do plano anterior existem no plano novo com os mesmos caminhos, tamanhos e hashes. A lista de bibliotecas externas é igual. A preparação comparou estes pins já medidos; não releu arquivos canônicos.
- Cada artefato reaproveitado foi medido ao copiar, copiado por bytes e reconferido. Fontes, planos e recibos anteriores permaneceram idênticos durante a preparação.

[Limite de custódia explícito] O recibo antigo atesta o build e os pins de suas fontes/entradas, mas não havia gravado hashes dos binários gerados. Os hashes desses binários foram medidos agora. O recibo não apresenta essa medição atual como se fosse uma selagem histórica. As novas auditorias carregarão os binários efetivos e verificarão novamente os termos.

## Plano novo e execução

O plano novo tem **21 processos**: 18 folhas novas, FullTGLExtRoot, FullTGLAudit e NewModulesAudit. Todas as 63 folhas serão carregadas pelos agregadores; a auditoria dedicada cobre os 1.098 termos, incluindo as sete instâncias locais nomeadas. Os 45 módulos cacheados não serão recompilados.

O runner sucessor reaproveita por extração AST as funções rec/new/run do builder congelado. Acrescenta a verificação explícita de 45 módulos cacheados, 21 processos e os três agregadores obrigatórios; restringe os caminhos de saída ao novo build; registra e confere os pins do cache antes/depois; conserva o laço Lean, timeout, checagem de axiomas e verificação geral de entradas. Nenhuma função do runner foi executada nesta preparação.

Execução prevista pelo orquestrador:
python -B run_incremental.py BUILD_INCREMENTAL_20260909_162634_176093/BUILD_PLAN.json

Os campos cached_modules, cached_build_receipt, cached_build_plan e cached_boundary_unchanged constam do plano e serão transportados ao resultado. cached_modules guarda os registros da fonte antiga, da fonte atual, dos artefatos/cópias e da rodada anterior. O runner verificará os arquivos canônicos apontados pelo plano e todos os registros do cache antes e depois da compilação. cached_boundary_unchanged no recibo de preparação se refere aos arquivos do cache/planos efetivamente relidos, não a uma nova leitura do acervo canônico.

[OPEN nesta preparação] Ainda não foi executado o plano de 21 processos por este agente. O finalizador deve relatar 21 processos novos mais 45 folhas reaproveitadas do build anterior de 48 processos, evitando dizer que os 63 módulos foram recompilados agora. Não houve alteração de gate, flags, sentinelas, memórias canônicas ou cópias existentes.

Evidências: RECIBO_PREPARACAO_INCREMENTAL.json, RECIBO_RUNNER.json, run_function.diff, BUILD_INCREMENTAL_20260909_162634_176093/BUILD_PLAN.json.
