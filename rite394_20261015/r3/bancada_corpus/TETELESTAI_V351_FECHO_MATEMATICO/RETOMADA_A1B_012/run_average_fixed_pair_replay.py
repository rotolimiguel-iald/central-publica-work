from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
R = Path(__file__).resolve().parent
K = R / 'k'
BIN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def load(p): return json.loads(p.read_text(encoding='utf8'))
def put(p, b):
    assert p.is_relative_to(R) and not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    q = p.with_name(p.name + '.tmp')
    q.write_bytes(b)
    assert q.read_bytes() == b
    os.replace(q, p)
base = R / 'attempts/20260914_173309_164705/run.json'
b = load(base)
assert b['returncode'] == 0 and b['sources_unchanged_during_build']
assert (R / 'AUDITORIA_MEDIA_ACAO_DIREITA_A1B.json').exists(), 'Finish the preceding sequential build first'
for row in load(R / 'FONTES_REPLAY.json'):
    assert pin(Path(row['original']['path'])) == row['original']
    assert pin(Path(row['copy']['path'])) == row['copy']
sources = [pin(K/'TGLExt'/n) for n in ['V351AverageFixedPair.lean', 'AuditA1AverageFixedPair.lean']]
env = os.environ.copy()
env.pop('LEAN_PATH', None)
env.pop('LEAN_SRC_PATH', None)
env['PATH'] = str(BIN) + os.pathsep + env['PATH']
packages = sorted(p for p in (K/'.lake/packages').iterdir() if (p/'.git').exists())
env['GIT_CONFIG_COUNT'] = str(len(packages))
for i, p in enumerate(packages):
    env[f'GIT_CONFIG_KEY_{i}'] = 'safe.directory'
    env[f'GIT_CONFIG_VALUE_{i}'] = str(p)
A = R/'average_fixed_pair_attempts'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A.mkdir(parents=True)
cmd = [str(BIN/'lake.exe'), 'build', 'TGLExt.AuditA1AverageFixedPair']
put(A/'sources.json', json.dumps(sources, ensure_ascii=False, indent=2).encode('utf8'))
print(A, flush=True)
with (A/'stdout.txt').open('wb') as out, (A/'stderr.txt').open('wb') as err:
    p = subprocess.Popen(cmd, cwd=K, env=env, stdout=out, stderr=err)
    put(A/'process.json', json.dumps(dict(pid=p.pid, command=cmd, cwd=str(K)), indent=2).encode('utf8'))
    rc = p.wait()
same = all(pin(Path(s['path'])) == s for s in sources)
d = dict(timestamp=datetime.datetime.now().astimezone().isoformat(), returncode=rc,
    command=cmd, cwd=str(K), sources=sources, sources_unchanged_during_build=same,
    base_cold_build=pin(base), external_package_cache_inherited=True,
    own_previous_project_objects_reused=True, external_project_objects_inherited=False,
    dev_objects_used=False, lean_path_removed=True, stdout=pin(A/'stdout.txt'), stderr=pin(A/'stderr.txt'))
put(A/'run.json', json.dumps(d, ensure_ascii=False, indent=2).encode('utf8'))
print('EXIT', rc, 'UNCHANGED', same)
print((A/'stdout.txt').read_text(encoding='utf8')[-8000:])
sys.exit(rc if same else 2)
