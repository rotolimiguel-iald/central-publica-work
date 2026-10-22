# Sincronização permanente da memória científica

Helper local reutilizável, versão lida dos originais admitidos em canonical_memory.CATALOG: selo e atribuição literal UM_VERSION no programa são conferidos sem executar/importar um.py. São13 fontes textuais; PDFs excluídos pelo builder existente. Nomes históricos de registros estatuto_* são preservados integralmente, com transcrição ao lado. Nenhum gate é promovido.

Comandos (Python absoluto com -B -X utf8):
- scientific_memory_sync.py : check padrão, somente leitura.
- scientific_memory_sync.py prepare --unit F0.3.MEMORIA_CIENTIFICA_SYNC --member codex-coordenadora : exige unidade reivindicada; snapshot/release novo fica INATIVO.
- scientific_memory_sync.py verify --epoch <epoch medido> : hashes, selo/prova/programa, fontes originais estáveis, FTS integral, chunks/linhas reproduzidos dos bytes.decode('utf-8-sig') sem conversão CRLF e recuperação em três modos. ACTIVE intocado.
- scientific_memory_sync.py activate --epoch <epoch medido> --unit F0.3.MEMORIA_CIENTIFICA_SYNC --member codex-coordenadora : verificação fresca + sources estáveis + claim; chama APENAS canonical_memory.activate_release existente. Ativação já igual retorna sem reescrever.

O agente só criou helper/patch/testes nesta pasta e executou check real. Não preparou nem ativou release de produção. Root fará preparação e auditoria/ativação separadas. Primeiro implantar por root, após revisão, o patch mínimo candidate/iald_orchestrator/canonical_memory.py: permite identidade exata recorrente na API, sem remover require_claim. Backup imediato de bytes do módulo vigente, temporário fsync/tamanho/CAS/replace/rehash; não reiniciar sessões/app/MCP. Builder/load/snapshot verificadores permanecem iguais. Não usar build_release.py do app.

No heartbeat: após consulta inicial da fila e regras/estado/ACOM, rodar check antes de nova unidade científica. Se CURRENT, seguir a fila. SEALED_ADVANCE_PENDING_SYNC é preparação pendente, não autorização automática para ativo ou redefinição de constraints. Localizar/claim unidade recorrente, preparar geração medida, auditoria/verify, ativar pelo protocolo autorizado e registrar recibo. Pendências específicas de pedidos, memory_generation fixada e envios incertos continuam protegidos: se pedido exigir geração anterior, carregá-la por versão; nunca mudar campo para forçar envio.

Releases imutáveis usam epoch=<versão lida>_<generation[:16]>. Generation usa exatamente ordem de catálogo e algoritmo do builder. Fonte mudando durante inspeção/preparo/verify bloqueia. Diretório preexistente sem recibo não é refeito automaticamente: recuperar evidência. safe_files provê backups byte a byte e replacement para metadados tocados; snapshots científicos não são reencodados.

10 testes descartáveis passaram: check sem escrita, geração/nome/CRLF, prepare+verify sem ACTIVE, ativação existente idempotente, claim faltante, unidade indevida, divergência programa/selo, source alterada, snapshot adulterado sem rebuild, índice adulterado e release parcial. Claims são simulados somente nos testes; zero provedores/Work. Check real mediu v392_f2941ea8f293aa2b contra ACTIVEv391_f9096efaabee6edf. Este é retrato, próximas versões vêm da fonte.
