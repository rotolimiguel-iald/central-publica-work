"""Record prepared per-request budget enforcement and limitations."""
import record_haiku_preparation as record
record.MARKER = 'IALD_CLAUDE_PER_REQUEST_GUARD_PREPARED_20260922'
record.NOTE = '''[REAL — guarda preparada, não integrada] Criados claude_request_guard.py e test_claude_request_guard.py no diretório de trabalho. O código recebe pedido Anthropic final, modelo autorizado pelo servidor e medição do prefixo conferida pelo hash; exige núcleo no primeiro bloco system. Conta o pedido inteiro por callback antes de cada envio (inclusive após ferramenta), aplica context_budget com >=180kHaiku + reserva de saída/margem, e envia cópia independente do snapshot contado. Ausência/erro/overflow não cai em estimativa nem corta memória. Recusa troca de modelo em payload e parâmetros adaptive/effort do Sonnet no Haiku.

[REAL — sete testes locais] Passaram crescimento após ferramenta/overflow, prefixo/modelo/volume errado, falha/contagem inválida, mutação pelo contador, mutação do chamador durante contagem, troca cliente→Sonnet e adaptiveHaiku. Nenhuma API ou credencial usada. Fixture180k é contagem falsa injetada para testar limites, não medição do pacote real.

[OPEN — integração] Módulo ainda não ligado ao motor/servidor. Adapter de contagem do pedido nativo, autorização de conta/consentimento, preço/reserva e ativação precisam ser integrados e verificados. Fonte atual converter_pedido aplica adaptive a qualquer Claude, e pode_usar_claude exige conta ampliada/lista; ambos precisarão adaptação explícita para Haiku público e Sonnetluiz. Arquivos de produção protegidos pela ordem de coordenação não foram alterados. Memória180k e testes reais continuam pendentes; objetivo integral ativo.
'''
if __name__ == '__main__':
    record.main()
