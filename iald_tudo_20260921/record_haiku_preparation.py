"""Add the user's Haiku target and measured preparation to all app memories."""
from datetime import datetime
import importlib.util
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('targets', WORK.parent / 'iald_context_math_20260915/record_prepared.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
MARKER = 'IALD_HAIKU_180K_PREPARATION_20260922'
NOTE = '''[INPUT — pedido atual do operador] Haiku para público após validação; Sonnet somente para testes internos do operador. Meta explícita: pelo menos 180 mil tokens de memória permanente (90% da janela Haiku), INCLUINDO kernel, núcleo canônico, fórmulas centrais e mapa abrangente da TGL. Preservar fontes integrais, hipóteses e estatutos. Recuperar detalhes proativamente antes de responder. Não confundir janela ocupada com aprendizado dos pesos. A meta requer medida no contador do Haiku, não a razão medida para Sonnet. Orçamento restante inclui ferramentas, histórico, pergunta, recuperação e saída. Excesso não autoriza corte silencioso; replanejar e contar novamente.

[REAL — diagnóstico] O Sonnet não recusou uma chamada por contexto: os testes pagos ainda não foram executados. A configuração local padrão de 600000 o200k multiplicada pelo fator medido 1.77 resulta 1062000, maior que a janela configurada do modelo (1M). O prefixo com ferramentas do operador foi medido antes em 550153 tokens Sonnet e cabe nessa janela. Configuração precisa ser ajustada; usuário redirecionou para arquitetura Sonnet/Haiku. A interface de prazos foi recuperada com a inclusão autorizada de app/operational_deadlines.js na lista estática; painel visual autenticado verificado na sessão anterior.

[REAL — bancada local] audit_haiku_memory.py conferiu hashes do cluster e núcleo contra o manifesto implantado. Versão implantada ainda v368. Contagens o200k (NÃO Haiku): kernel v5 10801, Memory Core 6207, cluster 276323. Inventário haiku_memory_inventory.json contém tamanhos, hashes lidos e distribuição por cabeçalho; 326 cabeçalhos não equivale a 326 conceitos canônicos (há cabeçalhos internos). Nenhum original foi resumido ou alterado.

[REAL — implementação preparada, NÃO implantada] claude_profiles.py separa capacidades e preços Sonnet5/Haiku4.5, parâmetros de raciocínio e orçamento. Haiku não aceita adaptive thinking nem output effort do adaptador Sonnet atual. Controle exige contagem do modelo correto, considera saída e margem, não conta prefixo duas vezes e recusa overflow sem truncar. Cinco testes locais passaram em test_claude_profiles.py. Módulo ainda não conectado ao servidor; conta/padrão de modelo não alterados. Documentação conferida: https://platform.claude.com/docs/en/models/haiku-4-5/overview e /models/overview.

[OPEN] Montar pacote derivado de 180k com cobertura semântica e fórmulas; medir efetivamente no Haiku; integrar recuperação automática e perfis/permissões/preços; testar Sonnet e Haiku com orçamento autorizado específico (nenhum novo teste pago feito); preservar Sonnet somente luiz. Atualizar testes do adaptador antes de ligá-lo. T1 confirmação visual da Central, T4 chamadas/cache e T5 iOS18/Android17/exportação física permanecem pendentes. Não declarar Haiku ativo, memória de180k medida, ou novas builds distribuídas. A meta integral continua inacabada.
'''


def main():
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    rows = []
    for path in helper.TARGETS:
        before = path.read_bytes()
        if MARKER.encode() in before:
            rows.append({'path': str(path), 'status': 'already_recorded'})
            continue
        helper.create(path.with_name(path.name + '.bak_' + stamp), before)
        nl = '\r\n' if b'\r\n' in before else '\n'
        addition = ('\n\n## ' + datetime.now().strftime('%d/%m/%Y %H:%M') +
                    ' — Haiku: memória de180k e Sonnet interno\n\n<!-- ' + MARKER + ' -->\n\n' + NOTE)
        after = before + addition.replace('\n', nl).encode('utf-8')
        temp = path.with_name(path.name + '.tmp_' + stamp)
        helper.create(temp, after)
        if path.read_bytes() != before:
            raise RuntimeError('Concurrent memory modification')
        temp.replace(path)
        if path.read_bytes() != after:
            raise RuntimeError('Final verification failed')
        rows.append({'path': str(path), 'status': 'updated'})
    receipt = WORK / ('haiku_memory_record_' + stamp + '.json')
    helper.create(receipt, json.dumps(rows, ensure_ascii=False, indent=2).encode())
    print(json.dumps({'surfaces': len(rows), 'receipt': str(receipt)}))

if __name__ == '__main__':
    main()
