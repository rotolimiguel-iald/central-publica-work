from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, os, re, shutil, subprocess, sys, time, traceback

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT = ROOT / 'revisao_b2'
OWN = ROOT / 's'
SOURCE = ROOT / 'kernel'
CACHE_SOURCE = ROOT / 'r' / '.lake' / 'packages'
BIN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
TARGET = 'TGLExt.GeneralMetricEinstein'
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
ATTEMPT = OUT / ('suppliers_' + STAMP)

def now():
    return datetime.now().astimezone().isoformat()

def win(p):
    return '\\\\?\\' + str(p.absolute())

def digest(p):
    h = hashlib.sha256()
    with open(win(p), 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def pin(p):
    return dict(path=str(p), bytes=p.stat().st_size, sha256=digest(p))

def save(p, data):
    b = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf8')
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:
            f.write(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + STAMP)
    with tmp.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == b
    os.replace(tmp, p)

def copy_pin(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    assert not dst.exists(), dst
    before = digest(src)
    shutil.copyfile(win(src), win(dst))
    assert digest(dst) == before == digest(src), src
    return dict(source=str(src), copy=str(dst), bytes=dst.stat().st_size, sha256=before)

def remove_comments(s):
    result, i, depth = [], 0, 0
    while i < len(s):
        if s.startswith('/-', i):
            depth += 1
            i += 2
        elif depth and s.startswith('-/', i):
            depth -= 1
            i += 2
        elif depth:
            if s[i] == '\n':
                result.append('\n')
            i += 1
        elif s.startswith('--', i):
            j = s.find('\n', i)
            i = len(s) if j < 0 else j
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)

def main():
    assert OWN.resolve().parent == ROOT.resolve()
    assert OUT.resolve().parent == ROOT.resolve()
    assert not OWN.exists() or not any(OWN.iterdir()), 'Only empty short root allowed; preserve any existing attempt.'
    ATTEMPT.mkdir(parents=True)
    OWN.mkdir(exist_ok=True)
    save(OUT / 'state.json', dict(status='PREPARING', attempt=str(ATTEMPT), own=str(OWN), timestamp=now()))
    print('PREPARING', str(OWN), flush=True)
    protected = [ROOT/'revisao'/'REVIEW_B1_FINAL.md', ROOT/'revisao'/'REVIEW_B1_FINAL.json', ROOT/'r'/'compilation.json', ROOT/'r'/'run.json', ROOT/'MANIFESTO_B1.json']
    protected_pins = [pin(p) for p in protected]
    docs = [copy_pin(ROOT/n, ATTEMPT/n) for n in ['REAPROVEITAMENTO_B2.md', 'REAPROVEITAMENTO_B2.json', 'DEPENDENCIAS_LAKE_V353.json']]
    sources, visited, external = [], set(), set()
    def visit(module):
        if module in visited:
            return
        assert 'FLRW' not in module, 'Unfrozen B2 source excluded'
        visited.add(module)
        path = SOURCE / (module.replace('.', '/') + '.lean')
        b = path.read_bytes()
        code = remove_comments(b.decode('utf-8-sig'))
        imports = []
        for line in code.splitlines():
            m = re.match(r'^\s*(?:public\s+)?import\s+(.+?)\s*$', line)
            if m:
                imports.extend(m.group(1).split())
        for dep in imports:
            if dep == 'TGL' or dep == 'TGLExt' or dep.startswith(('TGL.', 'TGLExt.')):
                visit(dep)
            else:
                external.add(dep)
        rec = copy_pin(path, OWN / path.relative_to(SOURCE))
        rec.update(module=module, imports=imports)
        sources.append(rec)
    visit(TARGET)
    configs = [copy_pin(SOURCE/n, OWN/n) for n in ['lakefile.toml', 'lake-manifest.json', 'lean-toolchain']]
    assert not (OWN/'.lake'/'build').exists()
    manifest = json.loads((OWN/'lake-manifest.json').read_bytes())
    assert (ROOT/'r'/'lake-manifest.json').read_bytes() == (OWN/'lake-manifest.json').read_bytes()
    packages = []
    env = os.environ.copy()
    env['GIT_OPTIONAL_LOCKS'] = '0'
    print('PROJECT_SOURCES', len(sources), 'AUTHOR_PROJECT_OBJECTS_COPIED', 0, flush=True)
    save(ATTEMPT/'source_snapshot.json', dict(target=TARGET, project_sources=sources, configs=configs, documents=docs, external_imports=sorted(external), protected_before=protected_pins))
    for package in manifest['packages']:
        name = package['name']
        origin = CACHE_SOURCE/name
        dest = OWN/'.lake'/'packages'/name
        rev = subprocess.run(['git', '-C', str(origin), 'rev-parse', 'HEAD'], capture_output=True, check=True, env=env).stdout.decode().strip()
        assert rev == package['rev'], (name, rev, package['rev'])
        jobs = []
        for base, dirs, files in os.walk(origin):
            db = dest/Path(base).relative_to(origin)
            db.mkdir(parents=True, exist_ok=True)
            for fn in files:
                sp = Path(base)/fn
                assert not sp.is_symlink(), ('cache symlink', sp)
                jobs.append((sp, db/fn))
        def cache_one(job):
            sp, dp = job
            sh = digest(sp)
            shutil.copyfile(win(sp), win(dp))
            assert digest(dp) == sh, sp
            return dict(relative=str(sp.relative_to(origin)), bytes=dp.stat().st_size, sha256=sh)
        with ThreadPoolExecutor(max_workers=8) as pool:
            records = list(pool.map(cache_one, jobs))
        pins = ATTEMPT/('cache_'+name+'_pins.json')
        save(pins, records)
        packages.append(dict(name=name, origin=str(origin), copy=str(dest), revision=rev, files=len(records), bytes=sum(x['bytes'] for x in records), pins=pin(pins), inheritance='B1 private cache, package bytes re-read and copied; not independently rebuilt'))
        print('PACKAGE_COPIED', name, len(records), flush=True)
    assert not (OWN/'.lake'/'build').exists(), 'No project build objects may be copied'
    save(ATTEMPT/'snapshot.json', dict(project_sources=sources, configs=configs, documents=docs, packages=packages, author_project_objects_copied=False, B2_sources_snapshotted=False, protected_before=protected_pins, script=pin(Path(__file__))))
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH']:
        env.pop(key, None)
    env['PATH'] = str(BIN) + os.pathsep + env.get('PATH', '')
    cmd = [str(BIN/'lake.exe'), 'build', TARGET]
    start = time.time()
    with (ATTEMPT/'lake_stdout.txt').open('xb') as out, (ATTEMPT/'lake_stderr.txt').open('xb') as err:
        process = subprocess.Popen(cmd, cwd=OWN, env=env, stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
        proc = dict(pid=process.pid, command=cmd, cwd=str(OWN), started=now(), lean_path_removed=True)
        save(ATTEMPT/'process.json', proc)
        save(OUT/'state.json', dict(status='LAKE_RUNNING', attempt=str(ATTEMPT), **proc))
        print('LAKE_STARTED', process.pid, str(ATTEMPT), flush=True)
        rc = process.wait()
    unchanged = all(pin(Path(p['path'])) == p for p in protected_pins)
    source_checks = [dict(source=r['source'], copy=r['copy'], unchanged=digest(Path(r['source']))==r['sha256'], copy_unchanged=digest(Path(r['copy']))==r['sha256']) for r in sources]
    objects = [pin(p) for p in sorted((OWN/'.lake'/'build'/'lib'/'lean').rglob('*.olean')) if p.relative_to(OWN/'.lake'/'build'/'lib'/'lean').parts[0] in ['TGL','TGLExt']]
    run = dict(returncode=rc, command=cmd, cwd=str(OWN), elapsed_seconds=time.time()-start, finished=now(), toolchain=subprocess.check_output([str(BIN/'lean.exe'),'--version'],env=env).decode().strip(), executables=[pin(BIN/'lean.exe'),pin(BIN/'lake.exe')], streams=[pin(ATTEMPT/'lake_stdout.txt'),pin(ATTEMPT/'lake_stderr.txt')], B1_protected_unchanged=unchanged, source_checks=source_checks, project_objects=objects, B2_accepted=False)
    save(ATTEMPT/'run.json', run)
    save(OUT/'state.json', dict(status='LAKE_FINISHED', returncode=rc, attempt=str(ATTEMPT), finished=now(), project_objects=len(objects), B1_protected_unchanged=unchanged, B2_accepted=False))
    print('LAKE_EXIT', rc, 'PROJECT_OBJECTS', len(objects), 'B1_UNCHANGED', unchanged, flush=True)
    return rc

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        if ATTEMPT.exists():
            save(ATTEMPT/'preparation_failure.json', dict(timestamp=now(), error=traceback.format_exc()))
        raise
