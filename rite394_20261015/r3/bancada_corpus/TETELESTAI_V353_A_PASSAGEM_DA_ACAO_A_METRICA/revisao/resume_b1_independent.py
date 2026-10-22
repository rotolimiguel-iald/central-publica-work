from pathlib import Path
from datetime import datetime
import hashlib, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
REVIEW = ROOT / 'revisao'
OWN = REVIEW / 'b1_20260914_145853'
OWN.mkdir(exist_ok=True)
if (OWN/'state.json').exists():
    (OWN/'serial_preparation_state.json').write_bytes((OWN/'state.json').read_bytes())
BIN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
SOURCE = ROOT / 'kernel'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def save(p, data):
    b = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf8')
    temp = p.with_name(p.name + '.tmp')
    with temp.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == b
    os.replace(temp, p)

def win(p):
    return '\\\\?\\' + str(p)

def copy_pin(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    b = src.read_bytes()
    if not dst.exists():
        with open(win(dst), 'xb') as f:
            f.write(b)
    assert dst.read_bytes() == b
    return dict(source=str(src), copy=str(dst), bytes=len(b), sha256=sha(b))

print('OWN', OWN, flush=True)
save(OWN / 'state.json', {'status': 'PREPARING', 'root': str(OWN), 'started': datetime.now().astimezone().isoformat()})
sources = []
for base, dirs, files in os.walk(SOURCE):
    dirs[:] = [d for d in dirs if d != '.lake']
    for name in files:
        src = Path(base) / name
        if name.endswith('.lean') or src.parent == SOURCE and name in ['lakefile.toml', 'lake-manifest.json', 'lean-toolchain']:
            sources.append(copy_pin(src, OWN / src.relative_to(SOURCE)))
docs = [copy_pin(ROOT / n, OWN / 'review_inputs' / n) for n in ['REAPROVEITAMENTO_B1.md', 'REAPROVEITAMENTO_B1.json', 'CUSTODIA_V353_FONTES.json', 'DEPENDENCIAS_LAKE_V353.json']]
print('PROJECT_SOURCES', len(sources), 'NO_AUTHOR_PROJECT_OBJECTS', flush=True)

packages = []
manifest = json.loads((SOURCE / 'lake-manifest.json').read_bytes())
for pkg in manifest['packages']:
    name = pkg['name']
    src = SOURCE / '.lake' / 'packages' / name
    dest = OWN / '.lake' / 'packages' / name
    h = subprocess.run(['git', '-C', str(src), 'rev-parse', 'HEAD'], capture_output=True, check=True).stdout.decode().strip()
    assert h == pkg['rev'], (name, h, pkg['rev'])
    jobs = [(Path(base)/fn, dest/(Path(base)/fn).relative_to(src)) for base, dirs, files in os.walk(src) for fn in files]
    def cache_one(job):
        sp, dp = job
        dp.parent.mkdir(parents=True, exist_ok=True)
        def digest(p):
            h=hashlib.sha256()
            with open(win(p),'rb') as f:
                for chunk in iter(lambda:f.read(1024*1024),b''):
                    h.update(chunk)
            return h.hexdigest()
        sh=digest(sp)
        if not dp.exists() or dp.stat().st_size!=sp.stat().st_size or digest(dp)!=sh:
            temp=dp.with_name(dp.name+'.copytmp')
            shutil.copyfile(win(sp),win(temp))
            assert digest(temp)==sh,sp
            os.replace(win(temp),win(dp))
        return {'relative':str(sp.relative_to(src)), 'bytes':sp.stat().st_size, 'sha256':sh}
    with ThreadPoolExecutor(max_workers=8) as pool:
        records=list(pool.map(cache_one,jobs))
    save(OWN / ('cache_' + name + '_pins.json'), records)
    packages.append({'name': name, 'origin': str(src), 'copy': str(dest), 'git_rev': h, 'files': len(records), 'bytes': sum(x['bytes'] for x in records), 'pins': str(OWN / ('cache_' + name + '_pins.json'))})
    print('CACHE_COPIED', name, len(records), flush=True)

author_audit = (OWN / 'TGLExt' / 'AuditSameBeta.lean').read_text(encoding='utf8')
targets = re.findall(r'^#print axioms\s+(\S+)', author_audit, re.M)
assert len(targets) == len(set(targets)) == 10
audit = 'import TGLExt.TheSameBetaReadsThreeFaces\n\nset_option pp.universes true\n\n'
for target in targets:
    audit += '#check ' + target + '\n#print axioms ' + target + '\n\n'
ap = OWN / 'TGLExt' / 'ReviewSameBeta.lean'
ap.write_bytes(audit.encode('utf8'))
snapshot = {'sources': sources, 'documents': docs, 'packages': packages, 'author_project_objects_copied': False, 'own_auditor': {'path': str(ap), 'sha256': sha(ap.read_bytes()), 'targets': targets}}
save(OWN / 'snapshot.json', snapshot)
env = os.environ.copy()
for key in ['LEAN_PATH', 'LEAN_SRC_PATH']:
    env.pop(key, None)
env['PATH'] = str(BIN) + os.pathsep + env.get('PATH', '')
cmd = [str(BIN / 'lake.exe'), 'build', 'TGLExt.TheSameBetaReadsThreeFaces', 'TGLExt.AuditSameBeta', 'TGLExt.ReviewSameBeta']
start = time.time()
with (OWN / 'lake_stdout.txt').open('wb') as out, (OWN / 'lake_stderr.txt').open('wb') as err:
    p = subprocess.Popen(cmd, cwd=OWN, env=env, stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
    save(OWN / 'process.json', {'pid': p.pid, 'command': cmd, 'cwd': str(OWN), 'started': datetime.now().astimezone().isoformat(), 'lean_path_removed': True})
    print('LAKE_STARTED', p.pid, flush=True)
    rc = p.wait()
run = {'returncode': rc, 'command': cmd, 'cwd': str(OWN), 'elapsed_seconds': time.time()-start, 'finished': datetime.now().astimezone().isoformat(), 'version': subprocess.check_output([str(BIN / 'lean.exe'), '--version']).decode().strip(), 'lean_binary_sha256': sha((BIN / 'lean.exe').read_bytes()), 'lake_binary_sha256': sha((BIN / 'lake.exe').read_bytes()), 'streams': []}
for n in ['lake_stdout.txt', 'lake_stderr.txt']:
    f = OWN / n
    run['streams'].append({'path': str(f), 'bytes': f.stat().st_size, 'sha256': sha(f.read_bytes())})
save(OWN / 'run.json', run)
save(OWN / 'state.json', {'status': 'LAKE_FINISHED', 'returncode': rc, 'root': str(OWN)})
print('LAKE_EXIT', rc, str(OWN), flush=True)
sys.exit(rc)
