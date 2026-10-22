"""Pin the completed independent core review; no shared-memory mutation."""
import datetime as dt
import importlib.util
import json
from pathlib import Path

W = Path(__file__).resolve().parents[1]
s = importlib.util.spec_from_file_location('review_finalize_io', W / 'mission_io.py')
io = importlib.util.module_from_spec(s)
s.loader.exec_module(io)
A = {'id': 'codex-mission-memory-review', 'kind': 'agent'}

def verify(value):
    if isinstance(value, dict):
        if 'path' in value and 'sha256' in value:
            assert io.pin(value['path']) == {k: value[k] for k in ('path', 'sha256')}, value['path']
        for child in value.values():
            verify(child)
    elif isinstance(value, list):
        for child in value:
            verify(child)

delivery = json.loads((W / 'CORE_DELIVERY_R1.json').read_bytes())
submitted = json.loads((W / 'CORE_SUBMITTED_R1.json').read_bytes())
tests = json.loads((W / 'review_core/TEST_RESULT_REVIEW_R1.json').read_bytes())
for value in (delivery, submitted, tests):
    verify(value)
assert tests['successful'] and tests['tests_run'] == 64
assert tests['production_baseline_unchanged'] and tests['source_bytes_unchanged']
fresh, receipt = io.call('mission_cli.py', {
    'operation': 'project', 'reference': str(W / 'SESSION_REFERENCE.json'),
    'actor': A, 'max_chars': 125000}, 'core_review_final_project')
t = next(t for t in fresh['projection']['active'] if t['id'] == 'C')
assert t['status'] == 'review_pending' and t['submitted_by'] != A['id']
assert t['criterion'] == delivery['criterion']
verify(t['evidence'])
source = W / 'staging/core/lib/iald_memory/activity.py'
costs = list((W / 'review_core/frozen_r1/tests_core/runs').glob('*/projection_cost.json'))
assert len(costs) == 1, costs
cost = json.loads(costs[0].read_bytes())
review = {
    'schema': 'organism-core-independent-review/v1',
    'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'statute': 'REAL_LOCAL_VERIFICATION', 'reviewer': A,
    'unit': 'F9.MEMORIA_ORGANISMO_20261016', 'requirement': 'C',
    'reference': io.pin(W / 'SESSION_REFERENCE.json'),
    'revision': fresh['receipt']['revision'], 'snapshot': io.pin(receipt),
    'criterion': t['criterion'], 'evidence': t['evidence'],
    'delivery': io.pin(W / 'CORE_DELIVERY_R1.json'),
    'submission': io.pin(W / 'CORE_SUBMITTED_R1.json'),
    'contracts': delivery['contracts'], 'implementation': delivery['implementation'],
    'api': delivery['api'], 'independent_tests': io.pin(W / 'review_core/TEST_RESULT_REVIEW_R1.json'),
    'test_runner': io.pin(Path(__file__).parent / 'run_independent_r1.py'),
    'verdict': 'PASS_CORE_WITH_SCOPE', 'requirement_satisfied': True,
    'test_result': {k: tests[k] for k in ('tests_run', 'builder_tests_rerun', 'independent_tests', 'failures', 'errors', 'seconds')},
    'coverage': [
        'Mesmo MemoryStore/contexto; APIs antigas comparadas à biblioteca instalada sobre banco privado, sem divergência.',
        'Origem explícita e delegação como proveniência; actor/scope/ticket e payload idempotente conferidos. Caminhos fornecidos em resultado de modelo permanecem dados.',
        'CAS concorrente concede uma única intenção; orientação alterada depois do append impede despacho; crash após intenção não permite reenvio.',
        'Retorno recebido é preservado como candidate/DECLARADO mesmo com pin de admissão rompido, hold concorrente ou orientação obsoleta.',
        'Crash após submit é reconciliado; quatro limites de begin parcial conservam uma inscrição/requisito/handle; nenhum resultado autoaceito.',
        'Projeção usa um snapshot, preserva conteúdo obrigatório e overflow, não escreve eventos; retomada em processo separado e handle alheio incerto preservados.',
        'Regressão do controlador: CAS, dependências, invalidação, evidência mutada, erratas, hold, lease, poda e parada com incerteza.'
    ],
    'source_anchors': [
        {'path': str(source), 'line': 111, 'subject': 'Validação do artefato durável e pin de admissão'},
        {'path': str(source), 'line': 125, 'subject': 'Orientações autenticadas e validação de identidade/epoch/lease'},
        {'path': str(source), 'line': 176, 'subject': 'Admissão recuperável, origens e requisito no contexto existente'},
        {'path': str(source), 'line': 254, 'subject': 'Intenção única e revalidação após append'},
        {'path': str(source), 'line': 305, 'subject': 'Custódia do retorno, submit e reconciliação de interrupção'},
        {'path': str(source), 'line': 401, 'subject': 'Incerteza/recuperação sem permissão de reenvio'},
        {'path': str(source), 'line': 433, 'subject': 'Composição ACOM/missão do mesmo snapshot'}
    ],
    'measured_cost': {'receipt': io.pin(costs[0]), 'measurement': cost,
        'scope': '12 projeções locais de um banco privado pequeno; não é benchmark prolongado, de tokens ou de provedor.'},
    'blocking_findings': [],
    'limits': [
        'Consumidor autentica ator/escopo/origem e valida vínculo de delegação. origin_ref não é autenticação nem herança automática do requisito pai; ticket não é credencial.',
        'Preflight e efeito externo não formam transação distribuída: mudança posterior exige conciliar retorno; intenção incerta não autoriza repetir.',
        'Artefatos e diário crescem. CAS da custódia usa tentativas locais limitadas, com artefato preservado para conciliação se esgotadas.',
        'Aceite técnico exclusivo de C em staging. Integrações A/N/Q, revisão conjunta V, implantação D e memória M permanecem pendentes.',
        'Nenhuma chamada de provedor, instalação, alteração científica/gate ou alegação de memória nos pesos.'
    ],
    'production_sources_unchanged': True, 'builder_sources_unchanged': True,
    'provider_calls': 0, 'installed': False,
}
path = W / 'review_core/CORE_INDEPENDENT_REVIEW_R1.json'
io.save(path, review)
print(json.dumps({'review': io.pin(path), 'revision': review['revision'], 'verdict': review['verdict'], 'cost': cost}, ensure_ascii=False, indent=2))
