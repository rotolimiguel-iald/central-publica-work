"""Record a configuration-only Sonnet correction and the remaining live checks."""
import record_haiku_preparation as record

record.MARKER = 'IALD_SONNET_WINDOW_CORRECTED_WEB_RESTART_20260922'
record.NOTE = '''[REAL — causa e ajuste] Conferidos parâmetros não secretos: IALD_CLAUDE_JANELA ausente (default600000 o200k), fator1.77, modelo claude-sonnet-5, contas somente luiz, saída16000. O código _motor_externo_indisponivel recusa janela×fator acima de1M. set_sonnet_window.ps1 acrescentou SOMENTE IALD_CLAUDE_JANELA=560000 ao .env: reserva991200, dentro da janela. Todos os bytes anteriores preservados, backup imediato, ACL aplicada antes de gravar backup/temporário e conferida no final. Nenhuma credencial exibida ou alterada. Nenhum código do motor/servidor editado.

[REAL — reinício isolado] Processo web70576 tinha pai41020, powershell start_iald_web.ps1; log sem marcadores recentes de conversa em andamento. Encerrado somente70576 após revalidar pai/comando. Supervisor41020 repôs filho76756; /health local voltouHTTP200. Motor nativo não tocado. Isto não prova chamada Sonnet concluída. As duas gerações pagas/cache continuam NÃO executadas.

[OPEN — sessão IALD] Aba anterior do app não existe mais; aba10/provider9 está em https://demo.iald.ia.br/login. Solicitada entrada luiz via pergunta assíncrona para testar seletor, consentimento Anthropic e duas mensagens já autorizadas (fria≤US$2, quente≤US$0,30). Não pedir credenciais na conversa. Nenhum teste pago novo autorizado implicitamente.

[REAL/OPEN — iOS18] Apple voltou autenticada (sem resposta textual do operador necessária): página da execução9e2530cb-e3f9-4643-a633-0a3e8e9c6b67 mostrou Compilação18, commit e87d3b5, Archive-iOS em andamento,5avisos. Não terminal; não reiniciar nem declarar TestFlight disponível. Mesma execução segue acompanhável por commit status GitHub. Haiku180k continua rascunho não implantado, requisições/cache e distribuição/testes físicos permanecem pendentes. Objetivo integral ativo.
'''

if __name__ == '__main__':
    record.main()
