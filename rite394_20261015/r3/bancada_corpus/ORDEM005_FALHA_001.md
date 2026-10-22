[REAL] Registro da primeira tentativa de audit_order005.py, 05/09/2026.

A execução terminou com exit 1 no controle A_correct. O leitor numérico tentava float('6015650200401571/500000000000000000'), recusando a representação racional exata fornecida pelo teste. A máquina devolveu INCONCLUSIVE/INVALID_INPUT, não um falso sucesso. Corrigido para analisar Fraction primeiro e depois conferir finitude. Fontes anteriores preservados em backups de bytes.

Os arquivos de massa e especificação já tinham sido criados antes da falha. A repetição passa a conferir igualdade byte a byte e reutilizar saídas idênticas; continua recusando sobrescrever conteúdo diferente.
