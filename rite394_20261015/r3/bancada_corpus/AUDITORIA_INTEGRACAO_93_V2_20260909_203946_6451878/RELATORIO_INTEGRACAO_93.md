# Auditoria estática da integração93 — versão 2, base histórica

PASS_STATIC_INTEGRATION_SCOPE

[REAL — medido] 93 módulos; 1286 teoremas e 352 outras declarações, incluindo 12 instâncias locais nomeadas; 1638 termos explícitos auditados.

A genealogia foi percorrida: snapshot histórico do canônico → lote63 → delta9 → delta5 → delta6 → delta10. O scanner deste script, separado do integrador, confere nomes, transposições e hashes. A configuração e os recibos de cada camada são lidos; o delta de uma camada não substitui o inventário cumulativo.

O estágio inicial usa o snapshot preservado, cujo tamanho e hash são conferidos contra os registros source_um e original_copy da época. O caminho do source_um vivo é apenas o endereço histórico registrado; seus bytes atuais não são usados como base.

AST e bytes fora da tabela de arquivos embutidos foram comparados em toda a cadeia, a partir desse snapshot histórico. Sentinelas, flags e gate são preservados. Dentro da tabela, entram 10 módulos e acréscimos nos agregadores. Não foi executado/importado nenhum um.py.

Verificações: 2191/2191. Arquivos embutidos: 699; arquivos Lean: 695. Resultado conjunto lido: PASS_TRANSPOSED_SCOPE.

Diagnóstico separado do canônico vivo: 11048796 bytes; SHA-256 7748416797668ffc3521fbaa60b000996981c749cf91d51be61267935c1c08f0. Difere do source_um histórico: True. Mudou entre as duas observações desta auditoria: False. As observações não são base da integração nem um teste de preservação da versão atual.

O limite de auditoria permanece explícito: dependências externas transitivas não foram todas recompiladas ou integralmente hashadas. A compilação incremental reaproveita cache com genealogia conferida. Não há afirmação de rodada do programa, novo selo ou veredito físico.

[Recibo completo](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_INTEGRACAO_93_V2_20260909_203946_6451878/AUDITORIA_INTEGRACAO_93.json>).
