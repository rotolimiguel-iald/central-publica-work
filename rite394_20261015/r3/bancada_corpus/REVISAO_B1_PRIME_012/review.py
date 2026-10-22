from pathlib import Path
import concurrent.futures as futures
import datetime, hashlib, json, os, re, subprocess, sys, time, uuid

ROOT = Path(__file__).resolve().parent
AUTHOR = ROOT.parent / 'B1_PRIME_012'
K = ROOT / 'kernel'
BIN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
NEW = ['TheSameBetaReadsFourFaces', 'ActionCouplingControls', 'AuditSameBetaFourFaces']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
sys.stdout.reconfigure(encoding='utf-8')

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')

def info(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=str(p.resolve()), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def write(p, data):
    p = Path(p)
    assert p.resolve().is_relative_to(ROOT)
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str): data = data.encode('utf-8')
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp())
        with backup.open('xb') as f: f.write(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    with tmp.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert tmp.stat().st_size == len(data)
    os.replace(tmp, p)
    assert p.read_bytes() == data

def record(p, obj):
    write(p, json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def lean_code(text):
    # Preserve line positions and remove nested Lean comments and strings for scans.
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        c, pair = text[i], text[i:i+2]
        if depth:
            if pair == '/-': depth += 1; out.extend('  '); i += 2; continue
            if pair == '-/': depth -= 1; out.extend('  '); i += 2; continue
            out.append('\n' if c == '\n' else ' '); i += 1; continue
        if string:
            if c == '\\': out.extend('  '); i += 2; continue
            if c == '"': string = False
            out.append('\n' if c == '\n' else ' '); i += 1; continue
        if pair == '/-': depth = 1; out.extend('  '); i += 2; continue
        if pair == '--':
            j = text.find('\n', i)
            if j == -1: j = len(text)
            out.extend(' ' * (j-i)); i = j; continue
        if c == '"': string = True; out.append(' '); i += 1; continue
        out.append(c); i += 1
    assert depth == 0 and not string
    return ''.join(out)

def imports(p):
    code = lean_code(p.read_text(encoding='utf-8-sig'))
    return re.findall(r'^\s*(?:public\s+)?import\s+([\w.]+)', code, re.M)

def prepare():
    assert not K.exists(), 'Fresh build root required'
    graph, snapshots = {}, []
    def visit(mod):
        if mod in graph: return
        src = AUTHOR / 'kernel' / Path(*mod.split('.')).with_suffix('.lean')
        deps = imports(src)
        graph[mod] = [x for x in deps if x.startswith(('TGL.', 'TGLExt.'))]
        dest = K / src.relative_to(AUTHOR / 'kernel')
        write(dest, src.read_bytes())
        snapshots.append(dict(module=mod, source=info(src), copy=info(dest), imports=deps))
        for dep in graph[mod]: visit(dep)
    visit('TGLExt.AuditSameBetaFourFaces')
    docs = ['ENTREGA_B1_PRIME.md', 'AUDITORIA_B1_PRIME.json', 'REAPROVEITAMENTO_B1_PRIME.md',
            'REAPROVEITAMENTO_B1_PRIME.json', 'LIMITES.md', 'PROPOSTA_CONSUMIDOR.json',
            'negative_controls.py', 'audit.py', 'AUDIT_NAMES.json', 'MANIFESTO_B1_PRIME.json',
            'HASHES_ENTREGA.json', 'INSTALACAO_FONTES.json', 'ADENDO_REAPROVEITAMENTO.md']
    for rel in docs:
        src = AUTHOR / rel; dest = ROOT / 'inputs' / rel
        write(dest, src.read_bytes()); snapshots.append(dict(source=info(src), copy=info(dest)))
    for name in NEW:
        src = AUTHOR / 'sources' / (name+'.lean')
        dest = ROOT / 'inputs' / 'sources' / src.name
        write(dest, src.read_bytes())
        snapshots.append(dict(source=info(src), copy=info(dest)))
        assert src.read_bytes() == (K/'TGLExt'/src.name).read_bytes()
    order = ROOT.parent/'TUNEL'/'PARA_CHATGPT'/'ORDEM_012_RECIBO_E_ADENDO_001_quarta_face_e_sequencia.md'
    write(ROOT/'inputs'/order.name, order.read_bytes())
    snapshots.append(dict(source=info(order), copy=info(ROOT/'inputs'/order.name)))
    memory = ROOT.parent.parent/'memory'
    context = [info(memory/'TGL_ATLAS.md'), info(memory/'TGL_INDICE_VIVO.md'),
               info(Path(r'C:\Users\rotol\.agents\skills\tgl-atlas\SKILL.md'))]
    for name in ['TheImportedEquilibrium', 'TowerModular', 'TheDammingByExpansion',
                 'FLRWMetricOnly', 'SectorFluidClosure', 'ThermodynamicFriedmann']:
        src = AUTHOR/'kernel'/'TGLExt'/(name+'.lean')
        if src.exists():
            dest = ROOT/'inputs'/'suppliers'/src.name
            write(dest, src.read_bytes()); snapshots.append(dict(source=info(src), copy=info(dest)))
    controls = AUTHOR/'semantic_controls'/'20260915_153016_999798'
    for src in sorted(controls.glob('Bad*.lean')):
        dest=ROOT/'controls'/'author'/src.name
        write(dest, src.read_bytes()); snapshots.append(dict(source=info(src), copy=info(dest)))
    assert len(list((ROOT/'controls'/'author').glob('Bad*.lean'))) == 9
    for rel in ['lean-toolchain', 'lakefile.toml', 'lake-manifest.json']:
        src=AUTHOR/'kernel'/rel
        write(ROOT/'inputs'/rel, src.read_bytes())
        snapshots.append(dict(source=info(src), copy=info(ROOT/'inputs'/rel)))
    (ROOT/'tmp').mkdir(exist_ok=True)
    record(ROOT/'INPUTS.json', dict(created_utc=stamp(), snapshots=snapshots, context_read_only=context, graph=graph,
        author_execution=False, author_local_oleans_used=False, author_new_sources_equal=True))
    record(ROOT/'PRIMARY_ACCESS.json', dict(status='DECLARADO_do_adendo',
        attempted_directory=r'C:\IALD\Artigo\Haja_Luz',
        command="Get-ChildItem -LiteralPath 'C:\\IALD\\Artigo\\Haja_Luz' -Filter 'tgl_paper_unified.py' -Recurse -ErrorAction Stop",
        result="Access to the path 'C:\\IALD\\Artigo\\Haja_Luz' is denied.",
        primary_read=False, source_read=info(order)))
    print('Prepared', len(graph), 'local source modules;', len(snapshots), 'snapshots', flush=True)

def env():
    e=os.environ.copy()
    e.pop('LEAN_PATH', None); e.pop('LEAN_SRC_PATH', None)
    packages=AUTHOR/'kernel'/'.lake'/'packages'
    paths=[K/'.lake'/'build'/'lib'/'lean']
    paths += [p/'.lake'/'build'/'lib'/'lean' for p in sorted(packages.iterdir()) if p.is_dir()]
    paths = [paths[0]] + [p for p in paths[1:] if p.is_dir()]
    e['LEAN_PATH']=os.pathsep.join(map(str,paths))
    e['PATH']=str(BIN)+os.pathsep+e['PATH']
    e['TEMP']=e['TMP']=str(ROOT/'tmp')
    e['PYTHONDONTWRITEBYTECODE']='1'
    return e

def run_lean(src, log_dir, output=None):
    cmd=[str(BIN/'lean.exe'), '-R', str(K if src.resolve().is_relative_to(K) else ROOT)]
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        assert not output.exists(), 'Do not reuse local objects'
        cmd+=['-o',str(output)]
    cmd += [str(src)]
    before=info(src); start=stamp(); t=time.monotonic()
    p=subprocess.run(cmd,cwd=K,env=env(),capture_output=True)
    write(log_dir/'stdout.txt',p.stdout); write(log_dir/'stderr.txt',p.stderr)
    out=(p.stdout+p.stderr).decode('utf-8',errors='replace')
    result=dict(command=cmd,cwd=str(K),started_utc=start,finished_utc=stamp(),seconds=time.monotonic()-t,
        returncode=p.returncode,source=before,source_unchanged=before==info(src),
        stdout=info(log_dir/'stdout.txt'),stderr=info(log_dir/'stderr.txt'))
    if output: result['object']=info(output) if output.exists() else None
    record(log_dir/'result.json',result)
    return result,out

def build():
    data=json.loads((ROOT/'INPUTS.json').read_text(encoding='utf-8'))
    graph=data['graph']; results={}; completed=set()
    record(ROOT/'TOOLCHAIN.json', dict(lean=info(BIN/'lean.exe'),
        version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),
        environment={n:env()[n] for n in ['LEAN_PATH','TEMP','TMP']},
        cache_policy='Mathlib and eight auxiliary packages read only; not rebuilt; no author TGL/TGLExt objects on search path'))
    while len(completed)<len(graph):
        ready=sorted(m for m,deps in graph.items() if m not in completed and set(deps)<=completed)
        assert ready, 'Dependency cycle'
        def job(m):
            rel=Path(*m.split('.'))
            r,out=run_lean((K/rel).with_suffix('.lean'),ROOT/'build_logs'/m,
                           (K/'.lake'/'build'/'lib'/'lean'/rel).with_suffix('.olean'))
            print(m, r['returncode'], round(r['seconds'],2), flush=True)
            if r['returncode']: print(out[-5000:],flush=True)
            return m,r
        with futures.ThreadPoolExecutor(max_workers=3) as pool:
            rows=list(pool.map(job,ready))
        results.update(rows)
        record(ROOT/'BUILD_PROGRESS.json',results)
        if any(r['returncode'] or not r['object'] for _,r in rows):
            raise RuntimeError('Source build failed; development failure is not evidence')
        completed.update(ready)
    record(ROOT/'BUILD.json',dict(modules=results,count=len(results),
        all_pass=all(r['returncode']==0 and r['object'] and r['source_unchanged'] for r in results.values())))

def control_runs():
    assert json.loads((ROOT/'BUILD.json').read_text(encoding='utf-8'))['all_pass']
    rows=[]
    for src in sorted((ROOT/'controls'/'author').glob('Bad*.lean')):
        r,out=run_lean(src,ROOT/'control_logs'/src.stem)
        r['name']=src.stem
        r['semantic_type_rejection']=(r['returncode']!=0 and 'Type mismatch' in out and
            not re.search(r'unexpected token|unknown (identifier|constant|namespace|module)|object file .* does not exist|failed to',out,re.I))
        r['diagnostic']=out
        rows.append(r); print(r['name'],r['returncode'],r['semantic_type_rejection'],flush=True)
    record(ROOT/'AUTHOR_CONTROLS_RERUN.json',dict(controls=rows,count=len(rows),
        all_semantic=len(rows)==9 and all(r['semantic_type_rejection'] for r in rows)))

if __name__=='__main__':
    {'prepare':prepare,'build':build,'controls':control_runs}[sys.argv[1]]()
