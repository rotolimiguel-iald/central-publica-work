# Sucessora preparada: cópia63 → cópia72

[REAL — preparação estática] A nova cópia preserva a cópia63 congelada e acrescenta nove módulos: os cinco de interação local geral, SmoothSelectedAtlasGluing, CentralScalarPhase, UnitaryCocycleUniqueness e LocalInteractionUniqueness. Os nove módulos têm recibos individuais PASS e fontes congeladas. Seus pins foram lidos e conferidos na configuração aprovada.

A alteração contém **116 teoremas e 22 outras declarações**. O conjunto da bancada soma **72 módulos, 972 teoremas e 264 outras declarações**, com **1.236 termos**. As entradas embutidas passaram de 669 para 678. A nova cópia fica em C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_170914_653192/um.py.

## Linhagem exata da cópia

O source_um desta integração é a cópia63 congelada, e não uma nova coleta do um.py canônico. Por isso, um_ORIGINAL_SNAPSHOT.py na pasta sucessora contém o snapshot dessa cópia63. A configuração e o resultado apontam explicitamente para o INTEGRATION_RESULT anterior e para seu recibo de build; esses registros mantêm a ligação histórica ao snapshot canônico v337.

A validação de ida e volta por AST/literal aprovou a geração. Fora da tabela embutida, bytes e AST permanecem idênticos ao predecessor. As fontes antigas permanecem iguais, salvo os acréscimos à raiz TGLExt e ao TGL/Audit. Não houve execução/importação de um.py, mudança de flags, gate ou sentinelas.

## Transposição e plano incremental

O integrador sucessor reconhece imports locais tanto entre os nove módulos novos quanto para os módulos TGLExt já embutidos no predecessor. Essa é a diferença necessária para acrescentar um lote à cópia existente. Cada declaração é conferida contra seu #print axioms e contra os metadados da integração; não há nova instância local neste lote.

O plano novo copia as 75 fontes necessárias: 72 módulos e os três agregadores/auditorias. Reutiliza os 63 módulos aprovados, com comparação exata entre suas fontes transpostas e as fontes embutidas na cópia sucessora. A proveniência do cache63 é composta: 18 folhas foram compiladas na rodada anterior e 45 vieram do cache aprovado daquela rodada. O preparador verifica ambos os caminhos; não exige ficticiamente 66 novos processos daquele recibo incremental.

Os artefatos dos 63 módulos foram copiados por bytes para um diretório novo. Os 45 que já tinham pins de cache foram comparados também com esses registros; os 18 binários produzidos na rodada anterior foram medidos ao reutilizar, sem fingir que esse hash novo já constava do recibo histórico.

O novo plano prevê **12 processos**: nove folhas novas, FullTGLExtRoot, FullTGLAudit e NewModulesAudit. A auditoria dedicada carrega os 1.236 termos, incluindo os sete local instances já presentes no lote anterior. O TGL/Audit mantém o padrão de acréscimo de teoremas.

Plano: C:/IALD/Central de Patentes/Chatgpt/INTEGRADOR_LOCAL_GERAL_20260909_170426_647362/BUILD_SUCCESSOR_20260909_171052_146967/BUILD_PLAN.json

## Guardas do runner e revisão

run_successor.py conserva o laço Lean e as verificações de axiomas, resultados e pins antes/depois. Acrescenta contagens derivadas do plano, os registros do cache e **recusa qualquer aviso em todos os processos, inclusive FullTGLAudit**. Quatro casos sintéticos do fragmento AST dessa decisão passaram: auditoria completa e folha, cada uma com e sem aviso. Nenhum subprocesso Lean foi chamado nesse teste.

[REAL — revisão de código] A raiz leu integralmente o preparador e o diff do integrador; depois revisou o plano final e o diff do runner com a recusa de avisos. A conclusão foi favorável. Essa revisão de preparação não substitui o recibo da compilação ou a auditoria estática independente da cópia, que têm evidências próprias.

[DECLARADO pela raiz] Após a revisão, a raiz iniciou o build de 12 processos. Este agente não iniciou uma compilação concorrente. O presente relatório atesta a preparação e seus testes; não declara antecipadamente o resultado da compilação em andamento.

## Preservação e limites

Scripts, configuração, plano e cópia foram congelados antes da execução pela raiz. Nenhum arquivo anterior foi alterado; as adaptações em cópias dos scripts têm backups imediatos dos bytes e diffs preservados. A preparação copiou binários, não criou links para destinos canônicos graváveis. Fontes e dependências canônicas foram somente lidas quando necessário para conferir os novos imports.

Não há recompilação de toda a cadeia transitiva, rodada de natureza, nova custódia, normalização automática de estado ou afirmação de fechamento físico da gravidade quântica. Os limites matemáticos e físicos de cada módulo permanecem nos relatórios próprios.

Arquivos principais: CONFIG_NOVE_APROVADA.json, integrate_approved_copy.py, prepare_successor.py, run_successor.py, RECIBO_PREPARACAO_SUCESSORA.json, VALIDACAO_PREPARADOR_RUNNER.json e MANIFESTO_PREPARACAO_SUCESSORA.json.
