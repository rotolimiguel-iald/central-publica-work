from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
CANON = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
pins = []


def read(path):
    data = path.read_bytes()
    pins.append({'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return data


def new(path, data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and data
    tmp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == data
    tmp.rename(path)
    assert path.read_bytes() == data


prior = json.loads(read(ROOT / 'REEXAME_SUFICIENCIA_082_20260910/ESTADO_CANONICO_082.json'))
raw = read(CANON / 'um.py')
tree = ast.parse(raw.decode('utf-8-sig'))
assignments = [node for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == '_EMBEDDED_KERNEL_FILES' for target in node.targets)]
assert len(assignments) == 1
embedded = ast.literal_eval(assignments[0].value)
seal = json.loads(read(CANON / 'um_absoluto_selo.json'))
read(CANON / 'tgl_kernel_proof_manifest.json')
read(CANON / 'rodada_v338_stdout.txt')
plan = json.loads(read(ROOT / 'INTEGRADOR_SIGMA_GIBBS_ASSINADO_20260909_210226_8753655/BUILD_SUCCESSOR_20260909_211448_468856/BUILD_PLAN.json'))
names = [module['module'] for module in plan['modules']]
assert len(names) == len(set(names)) == 98
presence = [{'module': name, 'present': 'TGLExt/' + name + '.lean' in embedded} for name in names]
prior_pins = {entry['path']: entry for entry in prior['pins']}
comparisons = [{'path': entry['path'], 'unchanged': entry == prior_pins[entry['path']]} for entry in pins if entry['path'] in prior_pins and Path(entry['path']).parent == CANON]
assert len(comparisons) == 4
for entry in pins:
    data = Path(entry['path']).read_bytes()
    assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256']
result = {
    'status': 'READ_ONLY_STABLE_SNAPSHOT',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'embedded_files': len(embedded),
    'modules': presence,
    'present': sum(module['present'] for module in presence),
    'absent': [module['module'] for module in presence if not module['present']],
    'comparison_with_delivery082': comparisons,
    'seal_um_hash_matches': seal['sha256']['um.py'] == hashlib.sha256(raw).hexdigest(),
    'seal_excerpt': {key: seal[key] for key in ('qg_closure_verdict', 'renormalization_wall_verdict', 'fail_closed_selftest') if key in seal},
    'pins': pins,
    'all_read_sources_unchanged': True,
    'um_executed_or_imported': False,
    'originals_written': False,
    'scope': 'Read-only AST presence and stable byte snapshot. Existing canonical execution evidence is read, not rerun.'
}
new(OUT / 'ESTADO_CANONICO_083.json', (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({key: result[key] for key in ('status', 'embedded_files', 'present', 'absent', 'comparison_with_delivery082', 'seal_um_hash_matches', 'seal_excerpt')}, ensure_ascii=True))
