"""Isolated, pinned data preparation for the authorized v402 film update."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

C = Path(__file__).resolve().parent
W = C.parent
V = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/video_um/delivery_v7')
N = V.parent.parent / 'Nós'
B = C / 'baseline_v401'
S = C / 'candidate_v402'
ORDER = Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_022_ADENDO_E_render_v402_autorizado.md')
sys.path.insert(0, str(W))
import mission

def read(p): return json.loads(p.read_bytes())
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()
def pin(p): return {'path':str(p), 'sha256':sha(p), 'bytes':p.stat().st_size}
def save(p, value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    atomic(p,raw)
def atomic(p, raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes()
        if old==raw:return
        backup=p.with_name(p.name+'.bak_'+str(time.time_ns()))
        backup.write_bytes(old);assert backup.read_bytes()==old
    q=p.with_name(p.name+'.tmp');q.write_bytes(raw);assert q.read_bytes()==raw and raw
    os.replace(q,p)
def check():
    p=mission.project();t=next(t for t in p['projection']['active']+p['projection']['settled'] if t['id']=='V402_DATA')
    ctx={'actor':{'id':'codex-video-replay','kind':'agent'},'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
    r=mission.call({'operation':'check',**ctx,'task_id':'V402_DATA','lease_id':t['lease']['id'],'max_chars':100000})
    assert r['ready'];return r
def stable_seal():
    current=read(N/'um_absoluto_selo.json')
    initial=read(C/'SOURCE_CAPTURE.json')
    assert current['um_version']=='v402', 'STOP: seal version advanced'
    assert pin(N/'um_absoluto_selo.json')==initial['canonical_seal'], 'STOP: seal bytes changed'
    return current
def prepare():
    preflight=check();assert not B.exists() and not S.exists()
    assert read(V/'source/um_absoluto_selo.json')['um_version']=='v401'
    data=['hud.json','frames.json','scene.json','PROVENANCE_PUBLIC.json','STDOUT_LINES.json','MANIFEST.json']
    paths=[V/'data'/n for n in data]+[V/'PROVENANCE_PUBLIC.json']
    paths += [p for p in (V/'source').iterdir() if p.is_file() and '.bak_' not in p.name]
    paths += [p for p in (V/'replay').iterdir() if p.is_file() and '.bak_' not in p.name and '.tmp' not in p.name]
    public=read(V/'replay/DELIVERY_C.json')['public_files']
    paths += [V/p for p in public] + [V/'web/replay-demo.html']
    paths += [V/p for p in ['export_data.py','extend_export.py','guard_export.py','audit/SOURCE_CAPTURE.json','audit/DATA_BUILD.json','audit/TEST_OFFLINE.json'] if (V/p).is_file()]
    records=[]
    for p in sorted(set(paths)):
        q=B/p.relative_to(V);raw=p.read_bytes();atomic(q,raw);assert q.read_bytes()==raw
        records.append({'relative':p.relative_to(V).as_posix(),'original':pin(p),'backup':pin(q)})
    save(C/'BASELINE_MANIFEST.json',{'source':'v401','files':records,'source_order':pin(ORDER),'preflight':preflight})
    stage=['export_data.py','extend_export.py','guard_export.py','replay/build_replay.py','replay/test_replay.py','replay/test_browser.cjs','replay/vendor_pyodide.py','replay/PYODIDE_VENDOR.json','web/replay-demo.html']+public
    for rel in set(stage):atomic(S/rel,(V/rel).read_bytes())
    seal_path=N/'um_absoluto_selo.json';seal_bytes=seal_path.read_bytes();seal=json.loads(seal_bytes)
    assert seal['um_version']=='v402','STOP: current seal is not authorized v402'
    assert seal['sha256']['um.py'].startswith('6a5033dc3f29324c'), 'STOP: authorized source pin differs'
    intake=read(C/'SOURCE_INTAKE.json')
    assert pin(seal_path)==next(x for x in intake['sources'] if Path(x['path']).name=='um_absoluto_selo.json'), 'STOP: intake seal changed'
    source_records=[]
    for name in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json','rodada_v402_stdout.txt']:
        p=N/name;raw=p.read_bytes()
        if name in seal['sha256']:assert hashlib.sha256(raw).hexdigest()==seal['sha256'][name],name
        atomic(S/'source'/name,raw);source_records.append({'canonical':pin(p),'isolated':pin(S/'source'/name),'seal_bound':name in seal['sha256']})
    assert seal_path.read_bytes()==seal_bytes
    atomic(S/'source/um_absoluto_selo.json',seal_bytes)
    save(C/'SOURCE_CAPTURE.json',{'source':'v402','source_sha256':seal['sha256']['um.py'],'canonical_seal':pin(seal_path),'isolated_seal':pin(S/'source/um_absoluto_selo.json'),'files':source_records,'source_order':pin(ORDER),'preflight':preflight})
    print(json.dumps({'status':'PREPARED','baseline_files':len(records),'source':seal['um_version'],'source_sha256':seal['sha256']['um.py']}))
def build():
    preflight=check();stable_seal();runs=[]
    commands=[['guard_export.py'],['replay/build_replay.py','--source',str(S/'source/um.py'),'--hud',str(S/'data/hud.json')],['replay/test_replay.py'],['replay/vendor_pyodide.py']]
    for index,args in enumerate(commands):
        start=time.perf_counter();r=subprocess.run([sys.executable,'-B','-X','utf8',str(S/args[0]),*args[1:]],cwd=S,capture_output=True)
        for label,raw in [('stdout',r.stdout),('stderr',r.stderr)]:
            if raw:atomic(C/f'DATA_STAGE_{index}_{label}.txt',raw)
        runs.append({'script':args[0],'returncode':r.returncode,'seconds':time.perf_counter()-start})
        save(C/'DATA_EXECUTION.json',{'source':'v402','source_sha256':read(C/'SOURCE_CAPTURE.json')['source_sha256'],'preflight':preflight,'runs':runs})
        if r.returncode:raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-3000:])
    atomic(S/'PROVENANCE_PUBLIC.json',(S/'data/PROVENANCE_PUBLIC.json').read_bytes());stable_seal()
    print(json.dumps({'status':'BUILT_ISOLATED','runs':runs}))
if __name__=='__main__':{'prepare':prepare,'build':build}[sys.argv[1]]()
