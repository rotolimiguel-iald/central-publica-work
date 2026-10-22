# Auditoria independente da integração — 09/09/2026

[REAL] PASS_INDEPENDENT_STATIC_AUDIT. Leitura AST/literal e comparação independente; nenhum um.py executado/importado, nenhuma recompilação Lean paralela.

[REAL] 28 módulos, 444 teoremas + 137 outras declarações = 581 termos. Tabela embutida: 605 → 633 arquivos.

[REAL] Prefixo e sufixo de bytes em torno do valor da tabela preservados. AST completo idêntico após substituir somente o valor da tabela. Isso inclui alvos da atribuição, núcleo Python, flags, gate e sentinelas. As entradas antigas mudaram apenas em TGLExt.lean e TGL/Audit.lean, por adição.

[REAL] Fontes e recibos foram relidos, seus hashes conferidos e cada string embutida comparada com a transposição mecânica independente dos imports. O Audit acrescenta exatamente um print para cada novo teorema, sem retirar prints antigos.

[REAL] Colisões por nome completo envolvendo declarações novas: 0. Colisões de nome curto: 3; os nomes completos distinguem seus referentes. Elas afetam consultas por nome curto e não são automaticamente conflitos Lean.

- decodeRecord: ChatgptAudit.AngularTensorCodec.decodeRecord; ChatgptAudit.SelectionRecord.decodeRecord
- phaseReading: ChatgptAudit.Angular034.phaseReading; ChatgptAudit.SelectionAngle.phaseReading
- tensor_quad_smul: ChatgptAudit.ConeVolume.tensor_quad_smul; ChatgptAudit.FisherEinstein.tensor_quad_smul

[REAL — errata histórica] ERRATA_DE_LINHAGEM.json registra os bytes/hash lidos das cópias6,7,14. O campo genérico herdado associa o hash da cópia7 ao conjunto de metadados que também inclui o caminho da cópia6. O predecessor efetivo deste lote é a cópia14. Os campos herdados não são usados no mecanismo de geração. CONFIG_APROVADA.json, INTEGRATION_RESULT.json e arquivos do build em curso permaneceram intactos.

[OPEN — escopo] Esta auditoria não atesta execução do programa, confirmação física nem recompilação canônica integral. A compilação transposta fica registrada separadamente pela tarefa principal.

SHA-256 da cópia, lido: a578254bfe0e2835fd9423d5e665b4d92cabd97df86719c30176ba25109d9c6e
