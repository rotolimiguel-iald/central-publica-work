"""Rebuild the isolated V7 films from a coherent scientific seal.

Default: data, replay, narration, browser render, encodes, public manifest.
--data-only performs no TTS, browser launch or rendering.
--reuse-render only admits completed jobs whose full source pins still match.
This program never writes into the seal's canonical directory or publishes.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, math, os, re, subprocess, sys, time
import urllib.request, webbrowser

ROOT = Path(__file__).resolve().parent
PY = sys.executable
sys.path.insert(0,str(ROOT/"cinema"))
from render_sources import collect as collect_render_sources

def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def atomic(p, data):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() and p.read_bytes() == data: return
    if p.exists(): p.with_name(p.name + '.bak_' + str(time.time_ns())).write_bytes(p.read_bytes())
    q = p.with_name(p.name + '.tmp'); q.write_bytes(data)
    assert q.stat().st_size == len(data) > 0
    os.replace(q, p)

def save(p, obj):
    atomic(p, (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

def read(p): return json.loads(Path(p).read_bytes())

def run(script, *args, capture=False):
    command = [PY, '-B', '-X', 'utf8', str(ROOT / script), *map(str, args)]
    result = subprocess.run(command, cwd=ROOT, text=True, encoding='utf-8', capture_output=True)
    if result.returncode:
        raise RuntimeError(script + ': ' + result.stderr[-3000:])
    if capture: return json.loads(result.stdout)
    print(script + ' complete', flush=True)

def capture_sources(seal_path):
    seal_path = seal_path.resolve(); seal_bytes = seal_path.read_bytes(); seal = json.loads(seal_bytes)
    version = seal['um_version']; pins = seal['sha256']
    if not re.fullmatch(r'v\d+', version): raise ValueError('Invalid seal version')
    archive = Path(r'C:\IALD\Central de Patentes\work\cadeia_de_selo') / version / ('dry_' + version)
    roots = [seal_path.parent, ROOT / 'source', archive]
    selected = {}
    for name in ['um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json']:
        expected = pins[name]
        candidates = [p / name for p in roots if (p / name).is_file()]
        source = next((p for p in candidates if sha(p) == expected), None)
        if source is None: raise ValueError('No source matches seal: ' + name)
        selected[name] = source
    stdout = 'rodada_' + version + '_stdout.txt'
    selected[stdout] = next((p / stdout for p in roots if (p / stdout).is_file()), None)
    if selected[stdout] is None: raise ValueError('Missing matching-version stdout')
    records = []
    for name, source in selected.items():
        raw = source.read_bytes(); digest = hashlib.sha256(raw).hexdigest()
        if name in pins and digest != pins[name]: raise ValueError('Source changed: ' + name)
        target = ROOT / 'source' / name
        atomic(target, raw)
        records.append({'name': name, 'bytes': len(raw), 'sha256': digest,
                        'seal_bound': name in pins})
    if seal_path.read_bytes() != seal_bytes: raise ValueError('Seal changed during capture')
    atomic(ROOT / 'source/um_absoluto_selo.json', seal_bytes)
    save(ROOT / 'audit/SOURCE_CAPTURE.json', {'source': version, 'source_sha256': pins['um.py'], 'version': version,
         'seal_sha256': hashlib.sha256(seal_bytes).hexdigest(), 'files': records,
         'stdout_scope': 'Same-version recorded stdout, independently byte-pinned; no new rite executed.'})
    return seal

def data_stage(seal_path):
    start = time.perf_counter(); seal = capture_sources(seal_path)
    run('guard_export.py')
    run('replay/build_replay.py', '--source', ROOT / 'source/um.py', '--hud', ROOT / 'data/hud.json')
    run('replay/test_replay.py')
    run('replay/vendor_pyodide.py')
    provenance = read(ROOT / 'data/PROVENANCE_PUBLIC.json')
    assert provenance['anchors_all_ok']
    atomic(ROOT / 'PROVENANCE_PUBLIC.json', (ROOT / 'data/PROVENANCE_PUBLIC.json').read_bytes())
    save(ROOT / 'audit/DATA_BUILD.json', {'source': seal['um_version'], 'source_sha256': seal['sha256']['um.py'], 'version': seal['um_version'], 'elapsed_seconds': time.perf_counter()-start,
         'files': {n: sha(ROOT / 'data' / n) for n in ['hud.json','frames.json','scene.json','PROVENANCE_PUBLIC.json','STDOUT_LINES.json']},
         'scope': 'Deterministic numeric data/provenance; no new Lean compilation or empirical run.'})
    return seal

def valid_job(path, kind):
    try:
        j = read(path); m = j['metadata']
        duration = 16 if kind == 'loop' else read(ROOT / ('data/' + kind + '.json'))['duration' if kind == 'film2' else 'total_seconds']
        if m['kind'] != kind or m['fps'] != 60 or abs(m['duration']-duration) > .001: return False
        if j['render']['encoded'] != round(duration*60): return False
        raw = path.with_suffix('.h264')
        if not raw.is_file() or sha(raw) != j['sha256']: return False
        expected_size=(1920,1080) if kind=='loop' else (3840,2160)
        if (m['width'],m['height'])!=expected_size or m['total']!=round(duration*60) or m['startTime']!=0: return False
        if j['source_files']!=collect_render_sources(ROOT): return False
        return True
    except (KeyError, OSError, ValueError): return False

def find_job(kind):
    paths = sorted((ROOT / 'cinema/render/jobs').glob(kind + '_*.json'), key=lambda p:p.stat().st_mtime, reverse=True)
    return next((p for p in paths if '.progress.' not in p.name and valid_job(p,kind)), None)

def ensure_server():
    url = 'http://127.0.0.1:8797/cinema/index.html'
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
            if b'Teoria da Gravita' in r.read(): return None
        raise RuntimeError('Port 8797 belongs to another service')
    except urllib.error.URLError:
        log = (ROOT / 'audit/server.log').open('ab')
        proc = subprocess.Popen([PY,'-B',str(ROOT / 'cinema/serve_studio.py')], cwd=ROOT,
               stdout=log, stderr=log, creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        for _ in range(20):
            if proc.poll() is not None: raise RuntimeError('Local server failed')
            try:
                with urllib.request.urlopen(url, timeout=1) as r:
                    if r.status == 200: return proc
            except urllib.error.URLError: time.sleep(.25)
        raise RuntimeError('Local server did not become ready')

def render_stage(reuse, no_open):
    if reuse:
        jobs = {k: find_job(k) for k in ['film1','film2','loop']}
        if not all(jobs.values()): raise ValueError('No current completed render; stale jobs are never reused')
        return jobs
    existing = {k: find_job(k) for k in ['film1','film2','loop']}
    if all(existing.values()): return existing
    ensure_server()
    url = 'http://127.0.0.1:8797/cinema/index.html?pipeline=all'
    print('Render UI: ' + url, flush=True)
    if not no_open: webbrowser.open(url)
    started = time.time()
    while time.time()-started < 7200:
        jobs = {k: find_job(k) for k in ['film1','film2','loop']}
        if all(jobs.values()): return jobs
        time.sleep(2)
    raise RuntimeError('Render incomplete after deadline; existing jobs preserved')

def verify_pin(entry):
    p=Path(entry['file'])
    if not p.is_file() or p.stat().st_size!=entry['bytes'] or sha(p)!=entry['sha256']: raise ValueError('Stale artifact: '+str(p))

def validate_encodes(jobs):
    build=read(ROOT/'audio/NARRATION_BUILD.json')
    # tts records whether this invocation contacted the service; cached audio is valid.
    if build.get('status')!='COMPLETED' or build.get('pending') or build.get('tts_inflight'): raise ValueError('Audio build incomplete')
    current_plan=run('audio/build_narration.py','plan',capture=True)
    if build.get('plan_sha256')!=current_plan['plan_sha256']: raise ValueError('Audio plan is stale')
    if any(build.get('reports',{}).get(f'film{n}',{}).get('status')!='AUDIO_MEASURED' for n in [1,2]): raise ValueError('Measured audio missing')
    verified=set()
    for n in [1,2]:
        receipt=read(ROOT/f'render/ENCODE_FILM{n}.json')
        if receipt['source_job']['sha256']!=sha(jobs[f'film{n}']): raise ValueError('Encode belongs to another render')
        verify_pin(receipt['source_job'])
        for stage in receipt['stages']:
            if stage['status']!='COMPLETE': raise ValueError('Incomplete encode stage')
            for item in [*stage['inputs'],*stage['outputs'],stage['parameters']['script'],stage['parameters']['ffmpeg']]:
                token=(item['file'],item['sha256'],item['bytes'])
                if token not in verified: verify_pin(item);verified.add(token)
        tl=read(ROOT/f'data/film{n}_narration_timeline.json')
        if tl.get('status')!='AUDIO_MEASURED' or tl['plan_sha256']!=build['plan_sha256']: raise ValueError('Narration timeline mismatch')
        for lang in ['en','pt-BR']:
            if tl['loudness'][lang]!=build['reports'][f'film{n}']['loudness'][lang]: raise ValueError('Audio measurement differs from build')
            for extension,expected in [('wav',tl['loudness'][lang]['sha256']),('m4a',tl['loudness'][lang]['aac']['sha256'])]:
                if sha(ROOT/f'audio/film{n}/{lang}.{extension}')!=expected: raise ValueError('Narration audio mismatch')
            for measure in [tl['loudness'][lang]['after'],tl['loudness'][lang]['aac']['measurement']]:
                loudness=float(measure['input_i'])
                if not math.isfinite(loudness) or abs(loudness+16)>1: raise ValueError('Narration loudness outside target')
    # Loop/asset stage receipts bind their outputs to inputs. Movie stages were checked above.
    receipts=list((ROOT/'render/.pipeline').glob('*.json'))
    output_pins={}
    for p in receipts:
        record=read(p)
        if record.get('status')!='COMPLETE': continue
        for out in record['outputs']: output_pins[str(Path(out['file']).resolve())]=(out,record)
    for p in [*(ROOT/'render').glob('*.jpg'),*(ROOT/'render').glob('*loop*.mp4'),*(ROOT/'render').glob('*loop*.webm'),*(ROOT/'render/stills').glob('*.jpg')]:
        if str(p.resolve()) not in output_pins: raise ValueError('No stage receipt for '+p.name)
        output,record=output_pins[str(p.resolve())];verify_pin(output)
        for item in [*record['inputs'],record['parameters']['script'],record['parameters']['ffmpeg']]: verify_pin(item)
        if 'loop' in p.name:
            expected_paths=[jobs['loop'],jobs['loop'].with_suffix('.h264')]
            for source in expected_paths:
                if not any(Path(item['file']).resolve()==source.resolve() and item['sha256']==sha(source) and item['bytes']==source.stat().st_size for item in record['inputs']): raise ValueError('Loop belongs to another render')
    return True

def collect_public(jobs):
    h = read(ROOT / 'data/hud.json'); render = {}
    validate_encodes(jobs)
    for kind, path in jobs.items():
        j = read(path); rows = j['render'].get('samples',[])
        failures = [r for r in rows if not r.get('transition') and r['width_fraction'] < .6]
        if failures: raise ValueError('Object coverage below threshold: ' + kind)
        render[kind] = {'job_sha256': sha(path), 'metadata':j['metadata'],
            'encoded_sha256':j['sha256'], 'render':j['render'], 'source_files':j['source_files']}
    scene_source=(ROOT/'cinema/cinema-scene.mjs').read_text(encoding='utf-8');finish_source=(ROOT/'cinema/render-support.mjs').read_text(encoding='utf-8')
    parameter_lines=[line.strip() for line in scene_source.splitlines() if any(k in line for k in ['this.bloom=','this.bokeh=','this.shutter=','toneMappingExposure='])]+[line.strip() for line in finish_source.splitlines() if 'grain:{value:' in line]
    params = {'exact_source_parameter_lines':parameter_lines,'bloom':'UnrealBloomPass, values pinned in cinema-scene.mjs',
              'depth':'BokehPass, values pinned in cinema-scene.mjs',
              'grading':'ACES filmic tone mapping; vignette and deterministic grain in render-support.mjs',
              'geometry_statute':'ONTO explanatory geometry; optical Jacobi example with declared INPUT parameters',
              'cost_scope':'Scene CPU submission and overlay CPU wall-clock measured, not isolated GPU cost. Full frame re-render is required; no unsupported incremental speedup claimed.'}
    save(ROOT / 'RENDER_MANIFEST.json', {'schema':'tgl.render.v7','source':h['seal_version'],'version':h['seal_version'],
        'source_sha256':h['seal_pin'],'parameters':params,'jobs':render})
    files = set()
    def include(p):
        if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name: files.add(p.relative_to(ROOT).as_posix())
    for n in ['PROVENANCE_PUBLIC.json','RENDER_MANIFEST.json']: include(ROOT/n)
    for p in (ROOT/'data').glob('*.json'): include(p)
    for p in (ROOT/'subs').rglob('*.vtt'): include(p)
    for p in (ROOT/'render').glob('*'):
        if p.suffix in ['.mp4','.webm','.jpg']: include(p)
    for p in (ROOT/'render/stills').glob('*.jpg'): include(p)
    for name in ['filmes.html','filmes.css','filmes.mjs','bg_scene.js','bg_demo.html','fonts.css','favicon.svg']:
        include(ROOT/'web'/name)
    for p in (ROOT/'web/fonts').glob('*'): include(p)
    for name in read(ROOT/'replay/DELIVERY_C.json')['public_files']: include(ROOT/name)
    # Resolve every relative JS import from the public entry points; no unused vendor tree.
    queue = [ROOT/n for n in files if n.endswith(('.js','.mjs'))]
    visited = set()
    while queue:
        p = queue.pop()
        if p in visited: continue
        visited.add(p)
        if 'pyodide' in p.parts: continue  # Complete pinned runtime subset is explicitly included above.
        module_source = re.sub(r'/\*.*?\*/', '', p.read_text(encoding='utf-8'), flags=re.S)
        for ref in re.findall(r'(?:from\s*|import\s*\(?)\s*[\'\"]([^\'\"]+)[\'\"]',module_source):
            if not ref.startswith('.'): raise ValueError('Non-local JS import: '+ref+' in '+str(p))
            target = (p.parent/ref).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file(): raise ValueError('Missing local import: '+ref)
            include(target)
            if target.suffix in ['.js','.mjs']: queue.append(target)
    required = [f'render/filme{n}_{res}{suffix}.mp4' for n in [1,2] for res in ['1080p','720p'] for suffix in ['','_pt-BR']]
    required += [f'render/filme{n}_1080p.webm' for n in [1,2]]
    required += ['render/filme1_loop_titulo.mp4','render/filme1_loop_titulo.webm','render/filme1_poster.jpg','render/filme2_poster.jpg','render/og_1200x630.jpg']
    if any(n not in files for n in required): raise ValueError('Missing media: '+str([n for n in required if n not in files]))
    entries=[{'path':n,'bytes':(ROOT/n).stat().st_size,'sha256':sha(ROOT/n)} for n in sorted(files)]
    manifest={'schema':'tgl.public-delivery.v7','source':h['seal_version'],'version':h['seal_version'],'source_sha256':h['seal_pin'],
      'source_seal_timestamp':h['seal_timestamp'],'title_proposals_en':['The emergence of gravity','From identity to geometry'],
      'audio':'Separate EN and pt-BR MP4 files; four synchronized subtitle languages for each voice.',
      'private_masters':'render/private (excluded)','public_files':entries,
      'anchors_all_ok':read(ROOT/'PROVENANCE_PUBLIC.json')['anchors_all_ok'],
      'scope':'Construction delivery for management review and publication; no site modification.'}
    save(ROOT/'PUBLIC_DELIVERY_V7.json',manifest)
    save(ROOT.parent/'PUBLIC_DELIVERY_V7.json', {'schema':'tgl.delivery-pointer.v7','source':h['seal_version'],'source_sha256':h['seal_pin'],'delivery':'delivery_v7/PUBLIC_DELIVERY_V7.json',
      'sha256':sha(ROOT/'PUBLIC_DELIVERY_V7.json'),'public_files':[{**e,'path':'delivery_v7/'+e['path']} for e in entries]})
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selo',type=Path,required=True)
    p.add_argument('--data-only',action='store_true');p.add_argument('--reuse-render',action='store_true')
    p.add_argument('--no-open',action='store_true');p.add_argument('--finalize-only',action='store_true')
    narration=p.add_mutually_exclusive_group()
    narration.add_argument('--narration-cache-only',action='store_true',help='Rebuild narration from verified successful clips without network')
    narration.add_argument('--bounded-retry-authorization',type=Path,help='Explicit human authorization receipt for bounded failed-utterance retries')
    a=p.parse_args()
    if a.data_only and a.finalize_only: p.error('--data-only and --finalize-only are mutually exclusive')
    original_seal=sha(a.selo)
    if not a.finalize_only:
        data_stage(a.selo)
        if a.data_only: return
        plan=run('audio/build_narration.py','plan',capture=True)
        save(ROOT/'audio/APPROVED_BUILD_PLAN.json',plan)
        if a.narration_cache_only:
            run('audio/build_narration.py','build','--cache-only')
        else:
            narration_args=['--tts','--approved-plan-sha256',plan['plan_sha256']]
            if a.bounded_retry_authorization: narration_args.extend(['--bounded-retry-authorization',a.bounded_retry_authorization])
            run('audio/build_narration.py','build',*narration_args)
    jobs=render_stage(a.reuse_render,a.no_open)
    if not a.finalize_only:
        run('cinema/media_v7.py','assets','--job-ready','--poster2-key','review_240')
        for n in [1,2]: run('cinema/media_v7.py','film','--film',n,'--job',jobs['film'+str(n)],'--audio-dir',ROOT/'audio','--job-ready')
        run('cinema/media_v7.py','loop','--job',jobs['loop'],'--job-ready')
    current_seal=read(a.selo);current_hud=read(ROOT/'data/hud.json')
    if current_seal['sha256']['um.py']!=current_hud['seal_pin'] or current_seal['um_version']!=current_hud['seal_version']: raise ValueError('Requested seal differs from rendered source')
    if sha(a.selo)!=original_seal: raise ValueError('Seal advanced during build; output remains a versioned candidate')
    manifest=collect_public(jobs);print(json.dumps({'status':'BUILT_FOR_REVIEW','files':len(manifest['public_files']),'manifest_sha256':sha(ROOT/'PUBLIC_DELIVERY_V7.json')}))

if __name__=='__main__':
    try: main()
    except Exception as error: print('REFUSED: '+str(error),file=sys.stderr);sys.exit(1)
