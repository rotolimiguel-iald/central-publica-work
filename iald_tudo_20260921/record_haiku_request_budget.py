"""Persist the measured request budget and remaining integration work."""
import json
from pathlib import Path
import record_haiku_preparation as record
record.MARKER = 'IALD_HAIKU_PUBLIC_REQUEST_BUDGET_20260922'
data = json.loads((Path(__file__).resolve().parent / 'haiku_app_request_count.json').read_bytes())
assert data['budget']['fits'] and data['generation_requests'] == 0
record.NOTE = '''[REAL — contagem oficial, não geração] count_haiku_app_request.py contou o candidato atual com as7 ferramentas públicas reais (kernel verification/search/read/list, public_read, search_tgl, fetch_tgl) e pergunta técnica sintética. Não importou o servidor nem alterou suas rotas. Entrada186033 tokens; reserva de saída4096, margem1024; saldo8847 dentro da janela200000. Prefixo medido anteriormente184555 inclui mensagem mínima. O alvo permanente mínimo180000 foi atingido nesta composição de bancada. Recibo haiku_app_request_count.json vincula hashes do candidato e ferramentas. Nenhuma resposta paga.

[ESCOPO] Saldo8847 NÃO é teste de conversa longa: nota de serviço/perfil, histórico real e resultados de ferramentas ainda não estão nessa medição. Recontar na integração e a cada resultado. Também comparar o candidato com todos os componentes da montagem atual (incluindo published_evidence/contrato e blocos Lean nucleares), para não certificar ausência de contexto essencial com um teste estreito. Kernel de linguagem v5 integral no candidato não equivale ao kernel Lean inteiro no contexto. Kernel Lean íntegro continua no catálogo do servidor; cobertura e recuperação devem ser verificadas.

[REAL — mobile, somente leitura] Git status do app mostra www/iald.js e www/index.html modificados e www/operational_deadlines.js não rastreado. package.json continua sem Filesystem/Share/Printer; portanto plugins da build18/17 ainda não instalados. Comando sem elevação perdeu cwd e tentou C:\\package.json; refeito com caminhos absolutos e leitura elevada, sem alterações. Nenhuma build iniciada ou distribuída.

[OPEN] Aprovação específica da extensão pointer continua pendente; ação rejeitada não foi repetida ou contornada. Integração de perfis Haiku/Sonnet, acesso, preços, memória e recuperação ainda não realizada. Antes de produção, auditoria semântica, orçamento completo, testes de isolamento e resposta/custo. T4 testes pagos/cache e T5 compilação/distribuição/exportação física continuam abertos. Objetivo integral não concluído.
'''
if __name__ == '__main__':
    record.main()
