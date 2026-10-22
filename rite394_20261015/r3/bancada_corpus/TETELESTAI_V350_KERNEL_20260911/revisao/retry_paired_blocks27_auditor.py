from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time
REV=Path(__file__).resolve().parent;ROOT=REV.parent;RUN=Path((REV/'paired_blocks27_latest_run.txt').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
hf=lambda p:sha(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
def put(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;os.replace(tmp,p)
def save(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json')
assert c['records'][0]['returncode']==0 and c['records'][0]['binary_equals_author']
assert c['records'][1]['returncode']==1
allowed_changes={str(ROOT/'PROXIMA_ETAPA_COTA_BLOCOS.md'),str(ROOT/'proxima_etapa_cota_blocos_pins.json')}
changes=[]
for p,h in m['readonly_pins'].items():
    now=hf(p)
    if now!=h:
        assert p in allowed_changes,p
        changes.append({'path':p,'old_sha256':h,'new_sha256':now,'scope':'future OPEN route only; no new Lean targets'})
        m['readonly_pins'][p]=now;m['document_pins'][p]=now
        put(RUN/'documents'/Path(p).name,Path(p).read_bytes())
m['document_refreshes']=changes
save(RUN/'document_refreshes.json',changes);save(RUN/'manifest.json',m)
rel='PairedBlocksAudit27Final.lean';sp=RUN/'sources'/rel;bp=RUN/'build'/Path(rel).with_suffix('.olean')
put(sp,('import TGLV350.ScalarWeightedProjectionTest\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in m['declarations'])).encode())
assert not bp.exists()
env=os.environ.copy();env['LEAN_PATH']=m['lean_path'];env['TMP']=env['TEMP']=str(RUN/'tmp')
cmd=[m['compiler'],'-o',str(bp),str(sp)];start=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
out=RUN/'logs/PairedBlocksAudit27Final.stdout.txt';err=RUN/'logs/PairedBlocksAudit27Final.stderr.txt';put(out,r.stdout);put(err,r.stderr)
ax={n:sorted(x.strip() for x in v.split(',') if x.strip()) for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",r.stdout.decode(),re.S)}
row={'module':rel,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-start,3),'source_sha256':hf(sp),
 'output_sha256':hf(bp) if bp.exists() else None,'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),
 'axioms':ax,'exact_targets':set(ax)==set(m['declarations']),'axioms_match_author':ax==m['author_axioms'],
 'axioms_allowed':bool(ax) and all(set(v)=={'propext','Classical.choice','Quot.sound'} for v in ax.values())}
result={**c,'records':[c['records'][0],row],
 'excluded_own_auditor_attempts':[{'reason':'own audit source imported module3 instead of module4; two final names absent from imported environment','record':c['records'][1]}],
 'document_refreshes':changes,'all_exit_zero':r.returncode==0,'exact_27_targets':row['exact_targets'],
 'all_axioms_allowed':row['axioms_allowed'],'all_axioms_match_author':row['axioms_match_author'],
 'readonly_artifacts_preserved':all(hf(p)==h for p,h in m['readonly_pins'].items()),
 'dependencies_preserved':all(hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256'] and hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['sha256'] for d in m['dependencies'].values()),
 'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in m['external_direct_pins'].values())}
save(RUN/'compilation.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['records','excluded_own_auditor_attempts','document_refreshes']}))
