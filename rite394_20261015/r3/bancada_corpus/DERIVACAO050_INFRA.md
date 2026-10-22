# Derivação prévia050 — compilação limpa com baseline049 selada
[INPUT — infraestrutura antes da implementação050]

Os seis fontes049 são somente leitura e terão seus bytes comparados com os pins do manifesto049. Este lote recompila cópias exatas desses fontes, junto com os novos050 e um importador conjunto, em diretório exclusivo. Não usa oleans históricos locais nem fallback para o kernel canônico.

A contagem separa teoremas/definições/instâncias novos050 daqueles da baseline049 recompilada. Todos os termos recompilados recebem checagem exata de axiomas. O scanner recusa tokens de declaração não censados, além de escapes de prova e linters desligados. A fronteira externa continua sendo Mathlib/stdlib, com imports diretos/companheiros medidos, não recompilação de toda a biblioteca.

São congelados durante a rodada: scripts do runner, manifesto049, fontes originais/copias, derivações050, ferramenta/configurações e dependências externas diretas. Logs e snapshots permanecem preservados. Sondas de desenvolvimento não são selo. O auditor independente deve reconstruir as dependências e verificar os pins da baseline e os censos separados antes de selar a entrega050.

Nenhuma escrita em arquivos049, memórias, Atlas, índice, um.py, kernel ou gate. Revisões dos novos arquivos preservam backups de bytes na mesma pasta; resultados físicos e meta ampla continuam OPEN.
