from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os

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
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    assert tmp.read_bytes() == data
    tmp.rename(path)
    assert path.read_bytes() == data

prior = json.loads(read(ROOT / 'REEXAME_SUFICIENCIA_066_20260909/ESTADO_CANONICO_066.json'))
previous_result = json.loads(read(ROOT / 'REEXAME_SUFICIENCIA_066_20260909/RESULTADO_INTEGRACAO_066.json'))
raw = read(CANON / 'um.py')
tree = ast.parse(raw.decode('utf-8-sig'))
assignments = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)]
assert len(assignments) == 1
embedded = ast.literal_eval(assignments[0].value)
seal = json.loads(read(CANON / 'um_absoluto_selo.json'))
read(CANON / 'tgl_kernel_proof_manifest.json')
read(CANON / 'rodada_v338_stdout.txt')
plan = json.loads(read(ROOT / 'INTEGRADOR_SIGMA_GIBBS_ASSINADO_20260909_210226_8753655/BUILD_SUCCESSOR_20260909_211448_468856/BUILD_PLAN.json'))
names = [m['module'] for m in plan['modules']]
assert len(names) == len(set(names)) == 98
presence = [{'module': name, 'present': 'TGLExt/' + name + '.lean' in embedded} for name in names]
prior_pins = {p['path']: p for p in prior['pins']}
comparisons = [{'path': p['path'], 'unchanged': p == prior_pins[p['path']]} for p in pins if p['path'] in prior_pins and Path(p['path']).parent == CANON]
assert len(comparisons) == 4
for pin in pins:
    data = Path(pin['path']).read_bytes()
    assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256']
result = {
    'status': 'READ_ONLY_STABLE_SNAPSHOT', 'created_utc': datetime.now(timezone.utc).isoformat(),
    'embedded_files': len(embedded), 'modules': presence, 'present': sum(m['present'] for m in presence),
    'absent': [m['module'] for m in presence if not m['present']],
    'comparison_with_delivery066': comparisons,
    'seal_um_hash_matches': seal['sha256']['um.py'] == hashlib.sha256(raw).hexdigest(),
    'seal_excerpt': {k: seal[k] for k in ('qg_closure_verdict', 'renormalization_wall_verdict', 'fail_closed_selftest') if k in seal},
    'pins': pins, 'all_read_sources_unchanged': True, 'um_executed_or_imported': False, 'originals_written': False,
    'scope': 'Source AST presence of 98 benchmark modules and fresh source/seal/manifest/run byte hashes; recorded v338 execution is prior evidence, not rerun here.'
}
new(OUT / 'ESTADO_CANONICO_067.json', (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({k: result[k] for k in ('status', 'embedded_files', 'present', 'absent', 'comparison_with_delivery066', 'seal_um_hash_matches', 'seal_excerpt')}, ensure_ascii=False))
