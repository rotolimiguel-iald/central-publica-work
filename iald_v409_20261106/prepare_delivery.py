"""Aggregate measured installation evidence and prepare the memory deposit."""
import json
from pathlib import Path
import hashlib
import task
W = Path(__file__).resolve().parent
Q = W.parent / 'scientific_memory_sync_20261106_v409'
def read(p): return json.loads(Path(p).read_bytes())
def pin(p): return {'path': str(p), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}
inst = read(W / 'INSTALLED_VERIFICATION.json')
live = read(W / 'LIVE_BACKEND.json')
queue = read(Q / 'DELIVERY_TECHNICAL_R1.json')
tower = read(W / 'TORRE_RESULT.json')
assert inst['status'] == live['status'] == 'PASS'
assert inst['identity']['release'] == inst['JEV_release'] == queue['release'] == 'v409'
assert tower['jev_current']
assert read(W / 'review/QUEUE_ACTIVATION_R1.json')['status'] == 'PASS'
files = ['APROVACAO_V409.json', 'RELEASE.json', 'install_plan.json', 'deployment.json', 'restart.json',
         'validation/review_final.json', 'validation/review_deploy.json', 'INSTALLED_VERIFICATION.json',
         'LIVE_BACKEND.json', 'INSTALLED_RETRIEVAL.json', 'TORRE_RESULT.json',
         'LICOES_v409.md', 'LICOES_v409_COMPLEMENTO.md', 'LESSONS_PIN_RECOVERY.json',
         'review/QUEUE_ACTIVATION_R1.json', 'review/QUEUE_FINAL_PATHS.json']
result = {
    'status': 'INSTALLED_AND_VERIFIED_TECHNICAL_SCOPE', 'order': 'ORDEM_009',
    'identity': inst['identity'], 'jev_release': inst['JEV_release'],
    'files_verified': inst['files_verified'], 'preservation_files': len(inst['prior_reliability_pins']),
    'kernel_topics': 483, 'queue': {k: queue[k] for k in ('status', 'release', 'generation', 'documents', 'chunks', 'previous_releases_preserved')},
    'runtime_http': live['login_http'], 'stream_synthetic_cases': live['stream_cases_on_installed_source'],
    'fresh_process_loaders': True, 'local_retrieval_verified': True,
    'native_counts': 6, 'paid_generation_calls': 0,
    'scope': 'Data/memory release and existing runtime preservation; no source theorem execution or scientific gate change.',
    'availability': {
        'web': 'v409 backend loaded and local HTTP200; browser chat not exercised.',
        'ios_internal': 'Existing app uses shared v409 backend; no client change or new TestFlight build needed.',
        'ios_external': 'Existing app uses shared v409 backend; no client change or new TestFlight build needed.',
        'android': 'Existing app uses shared v409 backend; no client change or new APK needed.',
        'stores': 'No new store distribution or group inspection in this server-only release.',
        'physical_devices': 'Not tested in this release.'
    },
    'limitations': ['No live model response or physical device validation.',
                    'Context admission remains per real conversation; indexed corpus does not all fit in every request.',
                    'Torre reports one stale scheduled clock task, outside ORDEM_009; not created or changed.'],
    'artifacts': [pin(W / f) for f in files] + [pin(Q / 'DELIVERY_TECHNICAL_R1.json'), pin(Q / 'ACTIVATION_ACCEPT_R1.json')],
    'reference': str(task.REF),
}
task.new('TECHNICAL_DELIVERY_R1.json', result)
text = f'''06/11/2026 — App/JEV e fila científica ativados na v409 por autorização humana específica.

[REAL] Fontes custodiadas/publicadas conferidas; {inst['files_verified']} destinos instalados, 483 tópicos e 13 pinos operacionais preservados. Reiniciado somente o filho web8082 sob o mesmo supervisor; HTTP200. Loaders em processo novo confirmaram v409 e ferramentas locais recuperaram o novo enunciado com hash/linhas. Nenhuma execução de um.py/Lean ou alteração de gate.
[REAL] P2 preserva v409/v408 e índice inteiro; 174 literais sem referência removidos do dicionário economizaram43.711bytes sem mudar a reconstrução. Shared847.129bytes. Seis contagens nativas públicas, zero geração paga; Haiku expandido891.783tokens permanentes. Limites de conversas reais permanecem.
[REAL] Fila:13fontes/{queue['chunks']}trechos; conferência integral antes do CAS e geração{queue['generation']} recebida em três modos em processo novo.18releases anteriores preservadas. Revisão independente de staging, caminhos finais e ativação.
[REAL] Torre regenerada com JEVv409; único DEFASADO é a tarefa agendada de relógio, fora desta ordem. Sem criar automação. Recebeu186casos sintéticos de streaming no código instalado.
[OPEN] Sem resposta real de modelo ou teste físico nesta entrega. Backend compartilhado web/iOS/Android; nenhuma alteração de cliente ou nova build necessária. Grupos/lojas não reinspecionados. Notas posteriores foram separadas das lições já pinadas; recuperação exata registrada emLESSONS_PIN_RECOVERY.json.
Fonte: {W / 'TECHNICAL_DELIVERY_R1.json'}. Referência própria: {task.REF}. Aceite final e depósito são atos documentados separadamente.
'''
task.new('MEMORY_DEPOSIT_v409.md', text.encode())
print(json.dumps({'status': result['status'], 'artifact': pin(W / 'TECHNICAL_DELIVERY_R1.json')}))
