"""Append the corrected product boundary to every app memory, with byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib
import importlib.util
import json

work = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('record_helper', work / 'record_haiku_preparation.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
marker = 'IALD_OPERATIONAL_ALERTS_ADMIN_ONLY_20260922'
note = '''[INPUT — correção expressa e permanente do operador] Avisos de validade de chaves, TestFlight, testes, saldo e infraestrutura pertencem exclusivamente à Central/painel administrativo interno da IALD. NÃO devem aparecer no aplicativo de conversa, inclusive quando usado pelo próprio operador. O pedido anterior de manter vencimentos à vista referia-se ao painel interno. Esta correção prevalece sobre a implementação anterior em app/web e mobile, preservada apenas como história.

[REAL — correção instalada] /api/alertas conserva compatibilidade retornando somente alertas vazios, sem prazos ou saldo. /admin/api/prazos aplica require_admin antes da leitura e Cache-Control:no-store. Painel administrativo consulta essa rota. Retirados importação, renderização e polling de avisos operacionais do app; módulo antigo permanece apenas como stub de remoção para compatibilidade. Quatro testes de rotas/cliente passaram. Web reiniciado isoladamente após zero reservas pagas/slots ativos; supervisor preservado; health200. Inspeção HTTP externa sem sessão retorna401 nas duas rotas, sem dados. Essa inspeção externa não substitui um teste autenticado visual.

[REAL — consentimento] Operador confirmou que o aceite do Claude passou a funcionar depois de atualizar o aplicativo. Log do servidor registra consentimento Anthropic de luiz em22/09/2026 às15:00:54. Não repetir diagnóstico de botão quebrado com base na estatística antiga de instalação4.1(17) da Apple.

[REAL — escopo e concorrência] Código web de exportação/Selo alterado em sessão paralela foi preservado. Nativehotfix parte da versão19 já distribuída e remove apenas avisos internos; não leva mudanças incompletas de Selo. Não copiar integralmente app/iald.js para mobile sem reconciliar também HTML/CSS/exportação da outra sessão. Commit, assinaturas, arquivos e disponibilidade da entrega constam no recibo indicado abaixo.

[REAL — preparação Haiku ainda NÃO implantada] Pacote medido mantém183135 tokens permanentes e184609 com sete ferramentas, saída4096, margem1024, dinâmica10271. NativeAccount usa contagem nativa e preços efetivos, preserva reserva quando resultado é incerto, bloqueia nova rodada pendente e permite repetir persistência após falha anterior ao commit sem duplicar linhas já concluídas.18 testes locais de conta/ponte passaram; revisão independente posterior passou6 testes N1/N2/N3. Não certifica recuperação após commit ambíguo/queda. Público continua desligado sem orçamento explicitamente aceito; pergunta deUS$1/pessoa/dia eUS$5/grupo/dia pendente. Nenhuma inferência paga nova nesta etapa.

[OPEN — continuidade] Haiku exige integrar S3/S4 e DeferredStartAccount ao payload final, corrigir metadados de contexto e validar hash das sete ferramentas; preparar novo stage sobre o servidor corrente. Stageclaude_routes_stage_20260922_145545_134624 é anterior à correção de avisos e NÃO pode sobrescrever produção. Preservar correção admin-only e trabalho paralelo do Selo. Ordem de saldoAnthropic automático localizada, ainda não examinada nesta etapa. Meta geral permanece ativa; T1 visualCentral,T4 verificações controladas/cache,T5exportações físicas e ativaçãoHaiku não são declarados concluídos por este hotfix.
'''

def main():
    delivery = json.loads((work / 'admin_only_delivery_status.json').read_text(encoding='utf8'))
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    text = ('\n\n## ' + now.strftime('%d/%m/%Y %H:%M') +
            ' — Avisos operacionais exclusivamente na administração\n\n<!-- ' + marker + ' -->\n\n' + note +
            '\n[REAL — matriz de disponibilidade desta entrega]\n' +
            json.dumps(delivery, ensure_ascii=False, indent=2) + '\n')
    rows = []
    for path in helper.helper.TARGETS:
        before = path.read_bytes()
        if marker.encode() in before:
            raise RuntimeError('Already recorded: ' + str(path))
        backup = path.with_name(path.name + '.bak_' + stamp)
        helper.helper.create(backup, before)
        newline = '\r\n' if b'\r\n' in before else '\n'
        after = before + text.replace('\n', newline).encode('utf8')
        temp = path.with_name(path.name + '.tmp_' + stamp)
        helper.helper.create(temp, after)
        assert path.read_bytes() == before, 'Concurrent modification'
        temp.replace(path)
        assert path.read_bytes() == after and len(after) > len(before)
        rows.append({'path': str(path), 'backup': str(backup),
                     'sha256': hashlib.sha256(after).hexdigest()})
    receipt = work / ('admin_only_memory_record_' + stamp + '.json')
    helper.helper.create(receipt, json.dumps(rows, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'surfaces': len(rows), 'receipt': str(receipt)}))

if __name__ == '__main__':
    main()
