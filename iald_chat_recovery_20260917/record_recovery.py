from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('record_helpers', WORK.parent / 'iald_context_math_20260915/record_prepared.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
MARKER = 'IALD_CHATGPT_RECOVERED_PINNED_PUBLIC_RELEASE_20260917'


def main():
    prepared = json.loads((WORK / 'prepared.json').read_bytes())
    installed = json.loads((WORK / 'installed.json').read_bytes())
    probe = json.loads((WORK / 'provider_probe.json').read_bytes())
    assert installed['status'] == 'INSTALLED_PINNED_RELEASE'
    assert probe['http_status'] == 200 and probe['answer'] == 'OK'
    note = f'''[INPUT] Operador relatou que o ChatGPT não funcionava na IALD. Diagnóstico e correção operacional autorizados pelo pedido e pelo trabalho vigente.

[REAL — causa reproduzida] Servidor web72056, nativa34128 e saúde local/pública200. O app, autenticado com a conta beta existente, mostrava “modelo fora do ar”. Os documentos do manifesto v357 apontavam para o checkout científico mutável, atualizado para v364. Quatro dos sete documentos tinham hashes diferentes; o programa, resultado e relatório formal também haviam avançado. A montagem pública e a do operador falhavam com “Documento público diverge da publicação verificada.” A trava de integridade funcionou; o erro de implantação era depender do checkout vivo para uma versão fixada. Não foi falta de crédito nem revogação demonstrada da chave. A conta luiz estava selecionada em nativa, com consentimento OpenAI existente e apenas limite global; essa preferência não foi alterada.

[REAL — correção instalada] Recuperados dez arquivos públicos diretamente dos blobs do commit {prepared['commit']}, derivando caminhos das URLs existentes e conferindo git ls-tree e hashes. Cópia da publicação aprovada em {prepared['destination']}. Somente os caminhos locais em iald_nucleo_fixo.json mudaram: URLs, hashes, papéis, v5, Memory Core, núcleo v357, catálogo Lean e regras de validação permaneceram idênticos. Backup imediato de bytes e substituição atômica, com comparação contra alteração concorrente. Nenhum código Python/JS, .env, credencial, limite financeiro, checkout científico, Atlas canônico ou binário móvel foi substituído. Não se trata de cópia/fork do Atlas: a cópia contém apenas a publicação pública fixada. O programa um.py não foi executado nem importado.

[REAL — verificação] Antes: contextos público/operador bloqueados. Depois: ambos validados, {installed['validation'][0]['context_tokens']} tokens no público e {installed['validation'][1]['context_tokens']} no operador; evidências publicadas conferidas. 6 testes de published_evidence e 11 de kernel_catalog passaram. A página recarregada passou a exibir “Online” e gpt-5.6-luna. Não houve reinício: manifesto relido pelo processo existente. Uma chamada mínima ao provedor, “Responda apenas: OK”, devolveu HTTP200, OK, finish stop, 12 tokens de entrada e4 de saída; teto reservado US${probe['single_call_cap_usd']:.7f}, dentro do teto global vigente US$3/dia. Sem núcleo/Atlas privado enviado nesse ping, sem troca de modelo. Conta beta usada apenas para observar disponibilidade e depois desconectada; consentimento dela não foi aceito em nome de terceiro.

[OPEN — evolução independente] Publicação v364 presente no repositório, HEAD {prepared['current_repository_head']}, preservada. Núcleo fixo do app permanece explicitamente v357; não alegar integração automática da v364. Atualização futura deve montar um pacote coerente de programa, selo, resultados, provas, catálogo, núcleo e documentos, validar em bancada e só então trocar o manifesto. Consultas às portas públicas continuam disponíveis. Não aumentar limite, afrouxar hash ou misturar gerações para evitar bloqueio.

[REAL/OPEN — alcance] Corrigida a causa reproduzida e verificado o provedor; nenhuma conversa real do operador foi enviada para teste, instalação física não verificada. Orientação ao operador: reabrir/recarregar o app e selecionar ChatGPT no topo se continuar em IALD Nativa. A pergunta sobre texto específico do erro ficou sem resposta e não foi necessária para localizar esta causa. TestFlight/Google Play não foram alterados nem reconsultados nesta etapa.

Evidências: {WORK}\\prepared.json, installed.json, provider_probe.json, recovery_record.json. Não usar números/hashes de memória em futuras validações: reler os artefatos.
'''
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    initial = {p: p.read_bytes() for p in helpers.TARGETS}
    assert not any(MARKER.encode() in x for x in initial.values())
    rows = []
    for path, before in initial.items():
        assert path.read_bytes() == before
        backup = path.with_name(path.name + '.bak_' + stamp)
        helpers.create(backup, before)
        eol = '\r\n' if b'\r\n' in before else '\n'
        addition = '\n\n### ' + now.strftime('%d/%m/%Y %H:%M %z') + ' — ChatGPT recuperado; publicação do app isolada do checkout vivo\n\n'
        addition += '<!-- ' + MARKER + ' -->\n\n' + note
        after = before + addition.replace('\n', eol).encode('utf-8')
        temp = path.with_name(path.name + '.tmp_' + stamp)
        helpers.create(temp, after)
        assert path.read_bytes() == before
        temp.replace(path)
        assert path.read_bytes() == after and len(after) > len(before)
        rows.append({'path': str(path), 'backup': str(backup), 'sha256': hashlib.sha256(after).hexdigest()})
    receipt = {'at': now.isoformat(), 'status': 'RECOVERED', 'ui_status': 'Online',
               'model': probe['model'], 'provider_http': probe['http_status'], 'provider_answer': probe['answer'],
               'targeted_tests_passed': 17, 'app_release': 'v357', 'repository_release': 'v364',
               'latest_release_not_integrated': True, 'services_restarted': False, 'memories': rows}
    helpers.create(WORK / 'recovery_record.json', json.dumps(receipt, ensure_ascii=False, indent=2).encode())
    print(json.dumps({'status': receipt['status'], 'memories_updated': len(rows)}))


if __name__ == '__main__':
    main()
