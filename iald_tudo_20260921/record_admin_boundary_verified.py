"""Append verified deployment state; preserve index-only memory and byte backups."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('memory_helper', WORK.parent / 'iald_context_math_20260915/record_prepared.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
MARKER = 'IALD_ADMIN_BOUNDARY_RUNTIME_VERIFIED_20260922'
RULE_MARKER = 'IALD_OPERATIONAL_ALERTS_ADMIN_ONLY_GLOBAL_20260922'

NOTE = '''[INPUT — regra permanente] Vencimentos de chaves, TestFlight, testes, saldo e infraestrutura são exclusivos da Central/painel administrativo interno protegido. Não aparecem na interface do app nem nas conversas, inclusive para o operador. Corrige o alcance do pedido anterior de visibilidade de prazos; não desliga o controle administrativo.

[REAL — produção conferida] Quatro testes de rotas/cliente executados contra os arquivos realmente instalados passaram. /api/alertas contém somente alertas vazios; /admin/api/prazos verifica require_admin antes da leitura e usa no-store. A função _alerta_saldo_operador também retorna None: créditos operacionais não são injetados nas conversas. Clientes web e mobile sem importação, consulta ou renderização dos avisos; Node --check passou em ambos. Processo web 70816, supervisor 41020, início 15:54:59; /health local 200; duas rotas protegidas retornam401 sem sessão. CORS local reconhece X-IALD-Context. Conferidos os16 hashes da implantação instalada, todos iguais ao recibo. Recibo: admin_boundary_runtime_20260922_160345_062814.json. Limitação distinta: pedidos públicos via Python retornaram403, e a navegação do navegador a /health foi bloqueada pelo cliente; não equivalem a teste visual autenticado nem a prova de queda do servidor.

[REAL — distribuição lida novamente na Apple às16h] iOS4.1(20) está Em testes em IALD Equipe e IALD Piloto. A linha do operador agora exibe Instalado4.1(20), superando a observação anterior19; isso é telemetria da Apple, não inspeção física da tela. Convites de Alana/Liana permanecem Convidado. Android4.1(19) APK/AAB assinados conforme admin_only_delivery_status.json; download exige login e GooglePlay depende de cadastro/DUNS. Web corrigida. Nenhuma nova compilação criada nesta conferência.

[REAL — continuidade Haiku, instalado DESATIVADO] A integração stage154903 e o pacote183135 tokens foram instalados; reinício web completado. Anterior recibo haiku_installed_disabled_20260922_155423_551001.json dizia RESTART_PENDING, superado por esta verificação. Revisão independente integration_154903_recheck_20260922_185208_137137.json confirmou correções I1(resposta assíncrona antiga) e I2(manifesto inválido). Contagem nativa do payload final, sete ferramentas conferidas, preservação de histórico e guardas de custo integrados. Reserva de saída4096, margem1024; referência184609 com ferramentas. Não ativado para público ou operador nesta entrega; não alterado .env/orçamento; zero gerações pagas nesta etapa. Mobile20 não contém ainda o cliente Haiku; servidor recusa esse caminho em clientes antigos, sem corte silencioso.

[REAL — memória] Reparo memory_index_repair_20260922_153609_551818.json moveu o diário integral de14:11 em diante de MEMORY.md para MEMORY_2.md com backups de bytes. MEMORY.md permanece índice (22069bytes na medição do reparo); notas extensas agora só no diário. Este registro preserva a regra.

[OPEN] Meta geral ativa. Haiku: orçamento público e teste pago específico ainda pendentes; preparar e verificar antes de ativar. Sonnet: duas chamadas controladas/cache não declaradas concluídas. Central: confirmação visual pelo operador; exportações: testes físicos pendentes. Preservar trabalho paralelo do Selo antes de sincronização integral/build seguinte. Não criar AdminAPIkey Anthropic sem autorização específica. Este adendo não altera cânone, fontes, gate ou estatutos científicos.
'''

def append(path, marker, title, note, stamp, now):
    before = path.read_bytes()
    if marker.encode() in before:
        return {'path': str(path), 'status': 'already_recorded'}
    backup = path.with_name(path.name + '.bak_' + stamp)
    helper.create(backup, before)
    newline = '\r\n' if b'\r\n' in before else '\n'
    addition = '\n\n## ' + now.strftime('%d/%m/%Y %H:%M') + ' — ' + title + '\n\n<!-- ' + marker + ' -->\n\n' + note + '\n'
    after = before + addition.replace('\n', newline).encode('utf8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    helper.create(temp, after)
    assert path.read_bytes() == before, 'Concurrent memory edit'
    temp.replace(path)
    assert path.read_bytes() == after and len(after) > len(before)
    return {'path': str(path), 'backup': str(backup), 'sha256': hashlib.sha256(after).hexdigest()}

def main():
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    targets = [p.with_name('MEMORY_2.md') if p.name == 'MEMORY.md' else p for p in helper.TARGETS]
    rows = [append(p, MARKER, 'Avisos somente na administração; implantação conferida', NOTE, stamp, now) for p in targets]
    rule = '''[INPUT — correção expressa do operador] O adendo “Prazos operacionais da IALD” de22/09/2026 09:47 refere-se exclusivamente à Central/painel administrativo interno protegido. Validades de chaves, TestFlight, testes, saldo e infraestrutura NÃO devem aparecer no aplicativo de conversa nem ser injetadas nas respostas da IA, inclusive quando o próprio operador usa o app. Manter alertas e datas apenas na administração; nas próximas atualizações preservar essa separação em web, iOS e Android. Este adendo corrige o alcance do anterior, preservado como história.'''
    rows.append(append(Path(r'C:\Users\rotol\.codex\AGENTS.md'), RULE_MARKER, 'Correção: prazos são de consumo interno', rule, stamp, now))
    receipt = WORK / ('admin_boundary_memory_record_' + stamp + '.json')
    helper.create(receipt, json.dumps(rows, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'surfaces': len(rows), 'receipt': str(receipt)}))

if __name__ == '__main__':
    main()
