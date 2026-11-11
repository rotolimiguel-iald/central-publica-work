"""Finalize the actual v409 delivery only after distinct technical acceptance."""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import task
import preservation_guard

W = Path(__file__).resolve().parent
def read(p): return json.loads(Path(p).read_bytes())
def pin(p): return {'path': str(p), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def replace_with_backup(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    old = path.read_bytes()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    backup = path.with_name(path.name + '.bak_' + stamp)
    with backup.open('xb') as f: f.write(old)
    assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as f: f.write(raw)
    assert temp.read_bytes() == raw and path.read_bytes() == old
    os.replace(temp, path)
    assert path.read_bytes() == raw
    return pin(backup)

project = task.project()
assert project['projection']['tetelestai'] is True
assert not project['projection']['active'] and not project['projection']['unresolved_handles']
protected = preservation_guard.verify()
technical = read(W / 'TECHNICAL_DELIVERY_R1.json')
for row in technical['artifacts']:
    assert pin(Path(row['path']))['sha256'] == row['sha256']
verify = next(row for row in project['projection']['settled'] if row['id'] == 'verify')
assert verify['status'] == 'satisfied'
final = {**technical, 'status': 'V409_ACTIVATED_TECHNICALLY_REVIEWED',
         'verification_acceptance': verify, 'mission_revision': project['receipt']['revision'],
         'scope_note': 'Technical activation accepted under explicit amended criterion. Live chat response and physical device check remain unperformed; this is not scientific confirmation.',
         'memory_deposit': read(W / 'MEMORY_DELIVERY_RECEIPT.json'),
         'final_artifacts': [pin(W / 'VERIFY_SCOPE_AMENDMENT.json'), pin(W / 'ACTIVATED_TRANSITION_RECEIPT.json'),
                             pin(W / 'MEMORY_DELIVERY_RECEIPT.json')],
         'preservation_verified_again': all(protected.values())}
task.new('FINAL_DELIVERY_R1.json', final)
registry = {'ordem': 'ORDEM_009', 'estado': 'cumprida', 'autor': task.OWNER,
            'escopo': 'Ativacao tecnica app/JEV v409 e fila F0.3; sem teste de conversa real ou aparelho.',
            'arquivos': [pin(W / 'FINAL_DELIVERY_R1.json'), pin(W / 'INSTALLED_VERIFICATION.json'),
                         pin(W / 'RELEASE.json'), pin(W / 'deployment.json'), pin(W / 'LICOES_v409.md'),
                         pin(W / 'LICOES_v409_COMPLEMENTO.md'), pin(W / 'TORRE_RESULT.json')],
            'o_que_falta': [],
            'limites': final['limitations'], 'disponibilidade': final['availability'],
            'referencia': str(task.REF)}
target = Path(r'C:\IALD\TUNEL_CLAUDE_APP\RESULTADOS\009_RESULTADO.json')
assert read(target)['estado'] == 'parcial'
prior = replace_with_backup(target, registry)
task.new('TUNNEL_FINAL_RECEIPT.json', {'target': pin(target), 'prior_partial_backup': prior})
route = read(W / 'ROUTE_PREPARED_R1.json')
route.update(tipo='RESULTADO', titulo='App/JEV e fila v409 ativados e verificados',
             resultado='1788 destinos instalados; app/JEV v409 carregados; fila13fontes/33036trechos; HTTP200; recuperacao local e186casos sinteticos de streaming aprovados.',
             veredito='V409_ACTIVATED_TECHNICALLY_REVIEWED',
             defeito='Sem conversa real ou teste fisico. Tarefa agendada de relogio fora do escopo permanece defasada.',
             nao_refazer='Nao repetir contagens, implantacao ou ativacao CAS. Recibos e versoes anteriores preservados.',
             proximo_passo='Gerencia confere recibo na fonte; uso real no aparelho e etapa distinta.',
             artefatos=[str(W / 'FINAL_DELIVERY_R1.json'), str(W / 'INSTALLED_VERIFICATION.json'), str(target)],
             nota='Corrige ao lado o estado parcial anterior. Nenhuma ciencia original ou gate alterado.')
task.new('ROUTE_DELIVERED_R1.json', route)
commands = [
    ('BOARD_DELIVERED_R1.json', [r'C:\Python314\python.exe', '-B', '-X', 'utf8', r'C:\IALD\PROGRAMA_IALD\iald.py',
       'avancar', task.UNIT, '--quem', task.OWNER, '--status', 'ENTREGUE', '--evidencia', str(W / 'FINAL_DELIVERY_R1.json'),
       '--nota', 'Ativacao v409 e verificacao tecnica aceitas independentemente; AUDITADA/FECHADA competem a gerencia. Live/aparelho nao alegados.']),
    ('ROUTE_DELIVERED_RECEIPT.json', [r'C:\Python314\python.exe', '-B', '-X', 'utf8', r'C:\IALD\MAPA_DE_ROTAS\rotas.py',
       'registrar', str(W / 'ROUTE_DELIVERED_R1.json'), '--quem', task.OWNER]),
]
for name, command in commands:
    r = subprocess.run(command, capture_output=True, text=True, encoding='utf8')
    task.new(name, {'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
    assert r.returncode == 0, name
current = task.call({'operation': 'get', 'reference': str(task.REF)}, False)
changes = {'records': [{
    'id': 'v409_final_technical_delivery', 'kind': 'fact', 'statute': 'REAL',
    'text': 'Independent technical acceptance completed; ORDEM_009 durable result updated to cumprida with prior partial byte backup. Board ENTREGUE, map updated, c1 memory deposit pending triage. Live model response and physical validation remain explicitly unperformed.',
    'sources': [{'kind': 'artifact', 'ref': str(W / 'FINAL_DELIVERY_R1.json'), 'sha256': pin(W / 'FINAL_DELIVERY_R1.json')['sha256']}]
}], 'flow': {**current['p'], 'phase': 'v409_technical_delivery_complete',
            'next_action': 'No further deployment under this receipt; c1 custody review and optional physical/live user validation remain separate.'}}
task.new('FINAL_TRANSITION_CHANGES.json', changes)
r = task.call({'operation': 'transition', 'reference': str(task.REF), 'expected_revision': current['revision'],
               'event_id': 'v409-final-technical-delivery', 'actor': {'id': task.OWNER, 'kind': 'agent'},
               'changes_file': str(W / 'FINAL_TRANSITION_CHANGES.json'),
               'changes_sha256': pin(W / 'FINAL_TRANSITION_CHANGES.json')['sha256']}, False)
task.new('FINAL_TRANSITION_RECEIPT.json', r)
print(json.dumps({'status': final['status'], 'final': pin(W / 'FINAL_DELIVERY_R1.json'),
                  'tunnel': pin(target), 'revision': r.get('revision')}))
