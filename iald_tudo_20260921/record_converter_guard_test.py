"""Record converter integration evidence and semantic repairs."""
import record_haiku_preparation as record
record.MARKER = 'IALD_CLAUDE_REAL_CONVERTER_GUARD_TEST_20260922'
record.NOTE = '''[REAL — teste de integração local com conversor atual] test_claude_guard_real_converter.py importou somente iald_motor_claude.py, rede bloqueada e sem SDK/chave/servidor. Três testes passaram: Sonnet mantém prefixo/cache/ferramentas no limite de contagem; Haiku com adaptive/effort atual é recusado e aceita parâmetros específicos preparados; tool_result real convertido é contado antes de envio e overflow impede callback de geração. Fonte reconferida byte a byte inalterada. Todos os números de tokens são fixtures, não medição real do provedor. Sete testes da guarda continuam separados; nada disso substitui T4 real.

[REAL — segunda cápsula corrigida] interface_is_light.md repõe ledger0_modv135 versus0_abs, setorqONTO/CONJ, papéis/limites das12entradas externas,10âncoras de form_content e caminhos inequívocos. Backup em bytes antes, escrita temporária/CAS. SHA81ae82b68e19c8eebe261bcc5c4589f15e379e2b52e10ee7de0e37d9eaec6a44. Enviada à reavaliação focal de Cicero; ainda não integrada. Economia anterior538 não pode ser atribuída à versão corrigida; consultar recibo novo de measure_interface.py.

[OPEN] Próxima integração deve separar parâmetros do Haiku e Sonnet, contar wire final, preservar autorização/consentimento/custo e ligar núcleo validado. Produção intacta, nenhuma chamada paga. Meta180k e objetivoT1–T5 seguem incompletos conforme pendências anteriores.
'''
if __name__ == '__main__':
    record.main()
