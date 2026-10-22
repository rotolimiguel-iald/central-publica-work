from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;os.replace(t,p)
def save(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
if len(sys.argv)==1:
    run=REV/('difference_squares_probe_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    catalog={};origins=[]
    for ptr in ['square_resolvent_latest_run.txt','bidual_support_final_latest_run.txt']:
        b=Path((REV/ptr).read_text().strip());m=load(b/'manifest.json');c=load(b/'compilation.json')
        assert c['all_exit_zero'] and c['dependencies_preserved']
        origins.append({'run':str(b),'manifest_sha256':hf(b/'manifest.json'),'compilation_sha256':hf(b/'compilation.json')})
        for n,d in m['dependencies'].items():
            catalog.setdefault(n,dict(source=d['frozen_source'],binary=d['frozen_binary'],source_sha256=d['source_sha256'],binary_sha256=d['sha256']))
        for rel,d in m['sources'].items():
            row=next((r for r in c['records'] if r['module']==rel),None)
            if row is not None:
                catalog[rel[:-5].replace('/','.')]=dict(source=d['snapshot'],binary=row['command'][2],source_sha256=d['sha256'],binary_sha256=row['output_sha256'])
        for n,d in m.get('inherited_bidual',{}).items() if False else []:pass
    src=ROOT/'kernel/TGLV350/ScalarRightSquareApproximation.lean';raw=src.read_bytes()
    write(run/'author_snapshot.lean',raw)
    needed=set()
    def visit(n):
        if n in needed or n.split('.')[0] not in {'TGL','TGLExt','TGLV350'}:return
        assert n in catalog,n
        needed.add(n)
        for x in re.findall(r'^import\s+([\w.]+)',Path(catalog[n]['source']).read_text(encoding='utf-8'),re.M):visit(x)
    for n in re.findall(r'^import\s+([\w.]+)',raw.decode(),re.M):visit(n)
    deps={}
    for n in sorted(needed):
        d=catalog[n];sp=Path(d['source']);bp=Path(d['binary'])
        assert sp.resolve().is_relative_to(REV) and bp.resolve().is_relative_to(REV)
        assert hf(sp)==d['source_sha256'] and hf(bp)==d['binary_sha256'],n
        rel=Path(*n.split('.'));dst=run/'build'/rel.with_suffix('.olean')
        write(dst,bp.read_bytes());companions={}
        for p in bp.parent.glob(bp.name+'.*'):
            if p.is_file():
                q=dst.with_name(p.name);write(q,p.read_bytes());companions[str(q)]=hf(q)
        deps[n]={**d,'copied_binary':str(dst),'companions':companions}
    lp=os.pathsep.join([str(run/'build')]+m['lean_path'].split(os.pathsep)[1:])
    assert str(ROOT/'build') not in lp
    assert hf(m['compiler'])==m['compiler_sha256']
    manifest={'run':str(run),'author_source':str(src),'snapshot_sha256':sha(raw),'origins':origins,'dependencies':deps,'compiler':m['compiler'],'compiler_sha256':m['compiler_sha256'],'lean_path':lp,'scope':'DIAGNOSTIC_ONLY_NOT_DEV_ACCEPTANCE'}
    save(run/'manifest.json',manifest)
    prefix=raw.decode().split('set_option diagnostics true in\ntheorem scalarRightSquareApproximation_difference_of_squares')[0]
    assert 'theorem scalarRightSquareApproximation_difference_of_squares' not in prefix
    body=raw.decode().split('set_option diagnostics true in\ntheorem scalarRightSquareApproximation_difference_of_squares')[1].split('\ntheorem scalarRightSquareApproximation_vector')[0]
    baseline=prefix+'set_option diagnostics true in\ntheorem scalarRightSquareApproximation_difference_of_squares'+body+'\n#print axioms scalarRightSquareApproximation_difference_of_squares\nend\nend TGLV350.Regular\n'
    write(run/'Baseline.lean',baseline.encode())
    print(json.dumps({'prepared':str(run),'dependencies':len(deps),'source_sha256':sha(raw)}),flush=True)
    mode='Baseline'
else:run=Path(sys.argv[1]);mode=sys.argv[2];manifest=load(run/'manifest.json')
env=os.environ.copy();env['LEAN_PATH']=manifest['lean_path'];(run/'tmp').mkdir(exist_ok=True);env['TMP']=env['TEMP']=str(run/'tmp')
sp=run/(mode+'.lean');bp=run/(mode+'.olean');assert not bp.exists()
cmd=[manifest['compiler'],'-o',str(bp),str(sp)];start=time.monotonic()
r=subprocess.run(cmd,cwd=run,env=env,capture_output=True)
write(run/(mode+'.stdout.txt'),r.stdout);write(run/(mode+'.stderr.txt'),r.stderr)
row={'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'output_sha256':hf(bp) if bp.exists() else None,'dependencies_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] and hf(d['copied_binary'])==d['binary_sha256'] for d in manifest['dependencies'].values())}
save(run/(mode+'.json'),row);print(json.dumps(row),flush=True)
print(r.stdout.decode('utf-8',errors='replace'),flush=True)
