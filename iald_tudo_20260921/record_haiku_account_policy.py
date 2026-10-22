import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_ACCOUNT_POLICY_PREPARED_20260922'
record.NOTE = '''[REAL — diagnóstico de integração] Leitura atual de iald_motores.pode_usar_claude e iald_web_server._opcoes_de_motor/api_motor_escolha confirmou que a permissão Claude é única e depende de pode_usar_nativa mais lista de contas. Para cumprir Haiku público/Sonnet exclusivo luiz, a integração deve separar modelo autorizado sem conceder IALD Nativa aos testadores. Conta bloqueada/não aprovada continua sem acesso; autenticação/consentimento/cotas permanecem portas separadas.

[REAL — preparado, NÃO implantado] claude_account_policy.py em work/iald_tudo_20260921 seleciona apenas modelos verificados: Haiku para conta aprovada somente quando implantação pronta; Sonnet apenas nome autenticado luiz quando pronto. Defaults fechados, flags estritamente booleanas, modelo não verificado recusado, sem fallback automático pago. Seis testes passaram para anônimo/bloqueado, público sem Sonnet, luiz exclusivo (outro admin não basta), falta de prontidão, alias conhecido/modelo desconhecido, flags string. Inputs devem vir do servidor, nunca do JSON do cliente; módulo ainda não ligado às rotas. Nenhuma conta, segredo, consentimento, cota ou motor em produção alterado.

[OPEN] Contagem corrente ainda excede janela; agente existente continua preparando lote de cápsulas públicas para revisão independente. A política preparada não é liberação pública. Login web luiz solicitado no formulário assíncrono para dois testes Sonnet/cache já autorizados. Demais pendências preservadas.
'''

if __name__ == '__main__':
    record.main()
