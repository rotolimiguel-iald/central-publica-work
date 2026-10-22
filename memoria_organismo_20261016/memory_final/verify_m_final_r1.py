"""Independent read-only byte review; writes only new review artifacts in WORK."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import sys

W = Path(__file__).resolve().parents[1]
F = W / 'memory_final'
sys.path.insert(0, str(W))
from mission_io import call, pin, save
A = {'kind': 'agent', 'id': 'codex-mission-memory-review'}
def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):
    return hashlib.sha256(b).hexdigest()
checked = {}
def checkpin(p):
    got = pin(p['path'])
    assert got['sha256'] == p['sha256'], p
    checked[got['path']] = got
    return got
def walkpins(x):
    if isinstance(x, dict):
        if 'path' in x and 'sha256' in x:
            checkpin(x)
        else:
            for v in x.values(): walkpins(v)
    elif isinstance(x, list):
        for v in x: walkpins(v)

p, project_receipt = call('mission_cli.py', {'operation': 'project',
    'reference': str(W/'SESSION_REFERENCE.json'), 'actor': A, 'max_chars': 125000},
    'M_final_review_verified')
task = next(x for x in p['projection']['active'] if x['id'] == 'M')
assert task['status'] == 'review_pending'
walkpins(task['evidence'])
plan = read(F/'PLAN_R1.json')
applied = read(F/'APPLIED_R1.json')
assert applied['status'] == 'APPLIED_VERIFIED'
checkpin(applied['plan'])
assert len(plan['surfaces']) == len(applied['surfaces']) == 10
rows = []
for wanted, actual in zip(plan['surfaces'], applied['surfaces']):
    target = Path(wanted['path'])
    backup = Path(actual['backup']['path'])
    assert target == Path(actual['after']['path'])
    assert target.parent == backup.parent
    assert backup.name.startswith(target.name + '.bak_')
    before, after = backup.read_bytes(), target.read_bytes()
    addition = Path(wanted['append']['path']).read_bytes()
    checkpin(wanted['append']); checkpin(actual['after']); checkpin(actual['backup'])
    assert sha(before) == wanted['before']['sha256'] == actual['before']['sha256']
    assert sha(after) == wanted['after_sha256']
    assert len(before) == wanted['before_bytes'] == actual['before_bytes']
    assert len(after) == wanted['after_bytes'] == actual['after_bytes']
    assert after == before + addition
    assert before.count(plan['marker'].encode()) == 0
    assert after.count(plan['marker'].encode()) == 1
    rows.append({'target': pin(target), 'backup': pin(backup),
                 'append': pin(wanted['append']['path']), 'prefix_byte_exact': True,
                 'before_bytes': len(before), 'after_bytes': len(after)})
new = plan['new_document']
checkpin(new['source']); checkpin(applied['new_document'])
assert Path(new['path']).read_bytes() == Path(new['source']['path']).read_bytes()
for name in ['DELIVERY_R1.json', 'memory_final/REGISTRATION_R1.json']:
    walkpins(read(W/name))
checkpin(applied['preflight'])
preflight = read(applied['preflight']['path'])
assert preflight['ok']
map_result = read(F/'MAP_REGISTER_RESULT_R1.json')
board_result = read(F/'BOARD_DELIVER_RESULT_R1.json')
assert map_result['exit_code'] == board_result['exit_code'] == 0
mr, br = json.loads(map_result['stdout']), json.loads(board_result['stdout'])
assert mr['ok'] and br['ok']
assert mr['gravados'][0]['seq'] == 1185
assert br['evento'] == 932 and br['para'] == 'ENTREGUE'
events = []
for path, seq in [(Path(r'C:\IALD\MAPA_DE_ROTAS\rotas.jsonl'), 1185),
                  (Path(r'C:\IALD\PROGRAMA_IALD\eventos.jsonl'), 932)]:
    matches = [(line, json.loads(line)) for line in path.read_bytes().splitlines()
               if line.strip() and json.loads(line).get('seq') == seq]
    assert len(matches) == 1
    raw, value = matches[0]
    events.append({'path': str(path), 'seq': seq, 'line_sha256': sha(raw), 'record': value})
assert events[0]['record']['rota_id'] == 'infra.memoria_organismo.atividade_20261016'
assert events[1]['record']['dados']['unidade'] == 'F9.MEMORIA_ORGANISMO_20261016'
assert events[1]['record']['dados']['para'] == 'ENTREGUE'
for evidence in events[0]['record']['artefatos'] + events[1]['record']['dados']['evidencia']:
    checkpin({'path': evidence['caminho'], 'sha256': evidence['sha256']})
report = {
    'status': 'PASS_WITH_SCOPE', 'requirement_satisfied': True,
    'reviewer': A, 'author_of_applied_material': 'codex-gerente-tgl',
    'time_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'reference': pin(W/'SESSION_REFERENCE.json'), 'task_id': 'M',
    'criterion': task['criterion'], 'revision_reviewed': p['receipt']['revision'],
    'projection_receipt': pin(project_receipt),
    'source_pins': [pin(F/'PLAN_R1.json'), pin(W/'apply_memory_final.py'),
        pin(F/'APPLIED_R1.json'), pin(F/'REVIEW_R1.json'), pin(W/'DELIVERY_R1.json'),
        pin(W/'ENTREGA_MEMORIA.md'), pin(F/'REGISTRATION_R1.json')],
    'surface_checks': rows, 'new_protocol': pin(new['path']),
    'verified_references': list(checked.values()), 'registered_events': events,
    'findings': [],
    'conclusion': 'Dez prefixos e backups byte a byte, apendices exatos e protocolo novo conferidos. Mapa 1185 e quadro 932 ENTREGUE verificados no diario real e nos recibos. Entrega registra estado, desempenho medido e dispositivo separado; criterio tecnico M atendido.',
    'scope': ['Sem repetir testes, servicos, builds ou provedores; resultados de D/V reutilizados por pinos.',
        '170 casos locais e 7 verificacoes MCP; um JEV real nao demonstra contexto infinito ou ganho cognitivo.',
        'Login do app e TestFlight/build/grupos pendentes; Bancada indisponivel; MCPs antigos nao recarregados.',
        'APK/AAB28 locais; nenhum APK/loja publicado nesta verificacao. Variacao do push privado permanece explicita na entrega.',
        'CAS de arquivos cooperativo, sem transacao global; a integridade posterior foi efetivamente medida.',
        'Aceite tecnico M nao e AUDITADA/FECHADA pela gerencia c1, nao move gate e nao fornece a ponte fisica do dispositivo.'],
    'review_script': pin(__file__)
}
save(F/'M_FINAL_REVIEW_R1.json', report)
print(json.dumps({'status': report['status'], 'revision': p['receipt']['revision'],
                  'surfaces': len(rows), 'pins': len(checked), 'report': pin(F/'M_FINAL_REVIEW_R1.json')}, ensure_ascii=False))
