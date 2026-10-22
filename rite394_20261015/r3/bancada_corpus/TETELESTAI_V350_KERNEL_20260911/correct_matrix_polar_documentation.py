"""Correct the reviewed domain/range wording, preserving immediate byte backups."""
from pathlib import Path
from datetime import datetime
import ast
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
STAMP = datetime.now().astimezone().strftime('%Y%m%d_%H%M%S_%f')
OLD = 'A igualdade polar estende S=JB da imagem densa da MESMA B; não escolhe J.'
NEW = ('Usando S=JB em D(B), prova-se √r·J R_ij=π(e_ij*)J em Ran(B); '
       'a densidade de Ran(B) e a continuidade dos dois membros estendem '
       'essa identidade a H_I. O fator polar J é o mesmo já construído.')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def replace_bytes(path, before, after):
    assert path.read_bytes() == before
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as stream:
        stream.write(before)
    assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(after)
    assert temp.read_bytes() == after and len(after) >= len(before)
    assert path.read_bytes() == before
    os.replace(temp, path)
    assert path.read_bytes() == after
    return {'path': str(path), 'backup': str(backup),
            'before_sha256': digest(before), 'after_sha256': digest(after)}

manifest_path = ROOT / 'matrix_polar_draft_status.json'
manifest_before = manifest_path.read_bytes()
manifest = json.loads(manifest_before)
report = ROOT / 'RELATORIO_CONJUGACAO_POLAR_MATRICIAL_DEV.md'
assert digest(report.read_bytes()) == manifest['report_sha256']
changes = []
for name, count in [('RELATORIO_CONJUGACAO_POLAR_MATRICIAL_DEV.md', 1),
                    ('record_matrix_polar_draft.py', 1),
                    ('record_matrix_polar_progress.py', 2),
                    ('make_matrix_polar_helpers.py', 1)]:
    path = ROOT / name
    before = path.read_bytes()
    assert before.count(OLD.encode()) == count, name
    after = before.replace(OLD.encode(), NEW.encode())
    if path.suffix == '.py':
        ast.parse(after.decode('utf-8'))
    changes.append(replace_bytes(path, before, after))
manifest['report_sha256'] = digest(report.read_bytes())
manifest['documentation_correction'] = {
    'timestamp': datetime.now().astimezone().isoformat(),
    'review': str(ROOT / 'revisao/REVIEW_MATRIX_POLAR_DEV.md'),
    'review_sha256': digest((ROOT / 'revisao/REVIEW_MATRIX_POLAR_DEV.md').read_bytes()),
    'scope': 'Domain/range wording only; Lean sources and evidence unchanged',
    'changes': changes,
}
after = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
changes.append(replace_bytes(manifest_path, manifest_before, after))
print(json.dumps({'documentation_corrected': True, 'changes': changes}, ensure_ascii=False, indent=2))
