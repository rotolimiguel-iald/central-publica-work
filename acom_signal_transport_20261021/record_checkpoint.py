"""Custody a partial engineering checkpoint, never a deployment claim."""
import hashlib
import json
from pathlib import Path
import task

items = ['science/SOURCE_FINDINGS_R2.json', 'review/LUMINIDIC_REVIEW_R1.json',
         'prototype_R2/PROVENANCE_ADDENDUM.json', 'CONTROL_DELIVERY_R2.json',
         'review/FINAL_CONTROL_R2.json', 'client_server_stage/DELIVERY.json',
         'review/INTEROP_FINAL_R1.json']
evidence = []
for name in items:
    p = task.W / name
    evidence.append({'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
baseline = json.loads((task.W / 'RUNTIME_BASELINE.json').read_bytes())
for item in baseline['files']:
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256'], 'runtime changed'
delivery = {'status': 'PARTIAL_ENGINEERING_VERIFIED_NOT_DEPLOYED',
    'unit': task.UNIT, 'reference': str(task.REF), 'evidence': evidence,
    'completed': ['Computational luminidio sources located and pinned',
                  'Known-parameter luminidic predictor plus exact residual control reviewed',
                  '65 block transport controls independently verified',
                  '88 JS/Python interoperability checks independently verified'],
    'pending': ['Production authentication/CSRF/HTTP adapter integration and regression',
                'Safari and device compatibility', 'Network latency measurement',
                'Controlled deployment and affected mobile distributions'],
    'decision': 'Keep running app unchanged; isolated controls are not production authorization evidence or a general holographic speed benchmark.',
    'runtime_unchanged': True, 'model_calls': 0,
    'scientific_limit': 'Exact bytes require residual; known-parameter synthetic chirps are not arbitrary-file fitting. Fixture alpha2 is an explicit test value, not a verified historical constant or canonical beta.'}
task.new('ENGINEERING_CHECKPOINT_R1.json', delivery)
state = task.call({'operation': 'get', 'reference': str(task.REF)}, False)
# Read the current projection; only update known handles, preserving their identities.
p = task.project()
handles = p['projection']['flow']['handles'] + p['projection'].get('terminal_handles', [])
for handle in handles:
    if handle['id'] in ('science', 'prototype', 'review'):
        handle['status'] = 'completed'
source = task.W / 'ENGINEERING_CHECKPOINT_R1.json'
result = task.call({'operation': 'transition', 'reference': str(task.REF),
    'actor': {'id': task.OWNER, 'kind': 'agent'}, 'expected_revision': p['receipt']['revision'],
    'event_id': 'acom-engineering-checkpoint-r1',
    'changes': {'records': [{'id': 'engineering-checkpoint-r1', 'kind': 'fact', 'statute': 'REAL',
        'text': 'Fontes computacionais de luminidio localizadas; controles isolados revisados, 65 testes de transporte e 88 de interoperabilidade. Resultado limitado a prototipos locais. App preservado; integracao HTTP/auth/CSRF, Safari, medicao de rede e implantacao continuam pendentes. Nao declara missao integral concluida.',
        'sources': [{'kind': 'artifact', 'ref': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}]}],
        'flow': {'phase': 'prototype_verified_integration_pending',
                 'next_action': 'Integrar adaptadores em staging autenticado, revisar e validar no navegador antes da implantacao; preservar escopo cientifico e originais.',
                 'handles': handles}}}, False)
task.new('ENGINEERING_CHECKPOINT_MEMORY_R1.json', result)
print(json.dumps({'status': delivery['status'], 'receipt': result}, ensure_ascii=False))
