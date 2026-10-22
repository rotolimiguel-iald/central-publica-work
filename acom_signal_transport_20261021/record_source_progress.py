"""Record bounded source discovery; does not activate a transport."""
import hashlib
import json
from pathlib import Path
import task

task.check('engineering')
report = task.W / 'science' / 'SOURCE_FINDINGS_R2.json'
data = json.loads(report.read_bytes())
verified = []
for item in data['sources']:
    path = Path(item['path'])
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != item['sha256']:
        raise RuntimeError('source_changed: ' + path.name)
    verified.append({'path': str(path), 'sha256': digest})
evidence = {'status': 'STATIC_SOURCES_VERIFIED', 'sources': verified,
            'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
            'runtime_changed': False,
            'finding': 'Computational LUMINIDIO and LUMINIDIC_CHIRP located; quantized/approximate routes are distinct from exact byte reconstruction.'}
task.new('SOURCE_PARENT_VERIFIED_R2.json', evidence)
state = task.call({'operation': 'project', 'reference': str(task.REF), 'max_chars': 100000}, False)
result = task.call({'operation': 'transition', 'reference': str(task.REF),
    'actor': {'id': task.OWNER, 'kind': 'agent'},
    'expected_revision': state['receipt']['revision'],
    'event_id': 'acom-computational-luminidio-located-r2',
    'changes': {'records': [{'id': 'computational-luminidio-located-r2', 'kind': 'fact',
        'statute': 'REAL', 'text': 'Uso computacional de luminidio localizado nas fontes ACOM da raiz indicada pelo operador. Hashes das sete fontes conferidos; leitura estatica, sem executar originais. Caminhos quantizados/aproximados nao garantem por si igualdade de bytes. Controle de atomo com residuo exato e interoperabilidade JS/Python em preparacao; runtime preservado.',
        'sources': [{'kind': 'artifact', 'ref': str(report), 'sha256': evidence['report_sha256']}]}],
        'flow': {'phase': 'luminidic_residual_and_interoperability',
                 'next_action': 'Conferir testes do atomo com residuo exato, interoperabilidade e revisao independente antes de decidir implantacao.'}}}, False)
task.new('SOURCE_PROGRESS_RECEIPT_R2.json', result)
print(json.dumps({'ok': True, 'verified_sources': len(verified), 'receipt': result}, ensure_ascii=False))
