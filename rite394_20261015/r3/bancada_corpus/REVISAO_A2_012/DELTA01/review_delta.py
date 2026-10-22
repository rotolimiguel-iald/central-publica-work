from pathlib import Path
import datetime, difflib, hashlib, json, os, re, subprocess, sys, time, uuid

ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent
AUTHOR=PRIOR.parent/'TETELESTAI_V351_FECHO_MATEMATICO'/'A2_012'
BASE=AUTHOR.parent/'RETOMADA_A1B_012'/'k'
SRC=ROOT/'src'
OUT=ROOT/'build'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
REMOVED=['scalarTrace_finite_positive_seed','scalarTrace_finite_projection_exists']
QUALIFIED=['TGLV350.Regular.'+n for n in REMOVED]
ALLOWED={'propext','Classical.choice','Quot.sound'}
sys.stdout.reconfigure(encoding='utf-8')

def stamp(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def info(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,b):
    p=Path(p); assert p.resolve().is_relative_to(ROOT)
    if isinstance(b,str): b=b.encode('utf-8')
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes(); backup=p.with_name(p.name+'.bak_'+stamp())
        with backup.open('xb') as f: f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert tmp.stat().st_size==len(b)
    os.replace(tmp,p); assert p.read_bytes()==b
def record(p,d): write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def current(x): return info(Path(x['path']))==x
def modulepath(m): return Path(*m.split('.')).with_suffix('.lean')

def prune_expected(old,name):
    # Boundaries read from the previously sealed source, not the author's delta claims.
    if name=='scalarTrace_finite_positive_seed':
        start=old.index(b"/-- An actual finite positive seed in A1's regular core. -/")
        end=old.index(b'/-- Kernel projections stay in the same von Neumann algebra.',start)
    else:
        start=old.index(b'theorem scalarTrace_finite_projection_exists ')
        end=old.index(b'#print axioms positive_operator_has_threshold_projection',start)
    block=old[start:end]
    assert len(re.findall(rb'^theorem\s+',block,re.M))==1
    changed=old[:start]+old[end:]
    printline=b'#print axioms '+name.encode()+b'\n'
    assert changed.count(printline)==1
    return changed.replace(printline,b'',1),block

def prepare():
    assert not SRC.exists() and not OUT.exists()
    olddata=read(PRIOR/'INPUTS.json'); oldmanifest=read(PRIOR/'MANIFESTO_A2.json'); oldseal=read(PRIOR/'SELO_A2.json')
    history=oldmanifest['files']+oldmanifest['new_objects']+oldseal['files']
    assert all(current(x) for x in history), 'Prior frozen receipt or artifact changed'
    prior_pins=[info(PRIOR/n) for n in ['RECIBO_REVISAO_A2.md','AUDITORIA_A2_INDEPENDENTE.json','MANIFESTO_A2.json','SELO_A2.json','INPUTS.json','CONTROLS.json']]
    claims=read(AUTHOR/'DELTA01_PODA.json'); claimed_names=read(AUTHOR/'AUDIT_NAMES_DELTA01.json')
    snapshots=[]
    for name in ['DELTA01_PODA.json','AUDIT_NAMES_DELTA01.json']:
        p=AUTHOR/name; q=ROOT/'inputs'/name; write(q,p.read_bytes())
        snapshots.append(dict(source=info(p),copy=info(q)))
    modules=[m for m in olddata['new_graph'] if m.startswith('TGLExt.V354')]
    diffs=[]; allnames=[]; graph={}; change_map={x['module']:x for x in claims['changes']}
    expected_changed={'V354FiniteTraceSupport':REMOVED[0],'V354SpectralThreshold':REMOVED[1]}
    for m in modules:
        rel=modulepath(m); old=PRIOR/'src'/rel; live=AUTHOR/'src'/rel; copy=SRC/rel
        before=old.read_bytes(); after=live.read_bytes(); short=m.split('.')[-1]
        write(copy,after); snapshots.append(dict(module=m,source=info(live),copy=info(copy)))
        if short in expected_changed:
            expected,block=prune_expected(before,expected_changed[short])
            assert after==expected, f'Unrequested byte change: {m}'
            c=change_map[short]
            assert c['before']['sha256']==info(old)['sha256'] and c['before']['bytes']==len(before)
            assert c['after']==info(live)
            backups=[p for p in live.parent.glob(live.name+'.bak_*') if p.read_bytes()==before]
            assert backups, f'No byte-identical author backup: {m}'
            diff=dict(module=m,before=info(old),after=info(copy),only_requested_removal=True,
                removed_name=expected_changed[short],removed_block=block.decode('utf-8'),author_backups=[info(p) for p in backups])
        else:
            assert before==after, f'Unchanged dependent modified: {m}'
            diff=dict(module=m,before=info(old),after=info(copy),unchanged=True)
        diffs.append(diff)
        patch=''.join(difflib.unified_diff(before.decode('utf-8').splitlines(True),after.decode('utf-8').splitlines(True),fromfile=str(old),tofile=str(live)))
        if patch: write(ROOT/'diffs'/(short+'.diff'),patch)
        code=after.decode('utf-8')
        names=re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev|structure)\s+(\w+)',code,re.M)
        allnames+=['TGLV350.Regular.'+n for n in names]
        graph[m]=[n for n in re.findall(r'^import\s+(\S+)',code,re.M) if n in modules]
        assert not any(re.search(r'\b'+n+r'\b',code) for n in REMOVED)
    old_names=[n for n in olddata['expected_public_names'] if n.startswith('TGLV350.Regular.')]
    expected_names=[n for n in old_names if n not in QUALIFIED]
    assert len(allnames)==33 and len(set(allnames))==33
    assert set(allnames)==set(expected_names)==set(claimed_names['names'])
    assert len(claimed_names['names'])==33
    for item in claimed_names['sources']:
        assert current({k:item[k] for k in ['path','bytes','sha256']})
    audit=AUTHOR/'src'/'TGLExt'/'AuditA2RegularSupport.lean'
    afteraudit=audit.read_bytes(); auditclaims=claims['audit_change']
    assert auditclaims['after']==info(audit)
    auditbackups=[p for p in audit.parent.glob(audit.name+'.bak_*') if info(p)['sha256']==auditclaims['before']['sha256'] and info(p)['bytes']==auditclaims['before']['bytes']]
    assert len(auditbackups)>=1
    oldaudit=auditbackups[0].read_bytes(); expectedaudit=oldaudit
    for n in QUALIFIED:
        b=('#print axioms '+n+'\n').encode(); assert expectedaudit.count(b)==1
        expectedaudit=expectedaudit.replace(b,b'',1)
    assert expectedaudit==afteraudit, 'Audit changed beyond the two removed prints'
    actual_prints=re.findall(r'^#print axioms\s+(\S+)',afteraudit.decode(),re.M)
    assert len(actual_prints)==33 and set(actual_prints)==set(allnames)
    write(SRC/'TGLExt'/'AuditA2RegularSupport.lean',afteraudit)
    snapshots.append(dict(module='TGLExt.AuditA2RegularSupport',source=info(audit),copy=info(SRC/'TGLExt'/audit.name)))
    write(ROOT/'diffs'/'AuditA2RegularSupport.diff',''.join(difflib.unified_diff(oldaudit.decode().splitlines(True),afteraudit.decode().splitlines(True),fromfile=str(auditbackups[0]),tofile=str(audit))))
    changed={m for m in modules if m.split('.')[-1] in expected_changed}
    affected=set(changed)
    while True:
        nxt=affected|{m for m,deps in graph.items() if set(deps)&affected}
        if nxt==affected: break
        affected=nxt
    assert affected==set(modules), 'Record actual reverse dependency closure'
    cachelinks=[]
    for row in olddata['accepted_objects']:
        p=Path(row['hardlink']['path'])
        assert current(row['source']) and current(row['hardlink'])
        q=OUT/p.relative_to(PRIOR/'accepted_cache')
        assert not q.exists(); q.parent.mkdir(parents=True,exist_ok=True); os.link(p,q)
        cachelinks.append(dict(source=row['source'],borrowed_from=info(p),review=info(q)))
    core_before=PRIOR/'src'/'TGL'/'CoreSupport.lean'
    assert (AUTHOR/'src'/'TGL'/'CoreSupport.lean').read_bytes()==core_before.read_bytes()
    core_result=read(PRIOR/'BUILD.json')['modules']['TGL.CoreSupport']
    assert core_result['returncode']==0 and current(core_result['object']) and current(core_result['source'])
    for p in sorted((PRIOR/'build'/'TGL').glob('CoreSupport.*')):
        if p.is_file():
            q=OUT/'TGL'/p.name; assert not q.exists(); os.link(p,q)
            cachelinks.append(dict(source=info(p),borrowed_from=info(p),review=info(q)))
    for m in modules:
        assert not (OUT/Path(*m.split('.'))).with_suffix('.olean').exists(), 'No stale V354 objects'
    write(SRC/'Audit33Independent.lean','import TGLExt.V354TraceReaderWall\nset_option pp.universes true\n'+
        '\n'.join('#check '+n+'\n#print axioms '+n for n in allnames)+'\n')
    write(SRC/'RemovedNamesAbsent.lean','import TGLExt.V354TraceReaderWall\n'+
        '\n'.join('#check '+n for n in QUALIFIED)+'\n')
    (ROOT/'tmp').mkdir(exist_ok=True)
    record(ROOT/'DELTA_COMPARISON.json',dict(changes=diffs,old_names=old_names,remaining_names=allnames,
        old_count=len(old_names),new_count=len(allnames),removed=QUALIFIED,
        only_requested_byte_removals=True,author_audit_exact_removal=True,author_audit_backup=[info(p) for p in auditbackups],
        changed_modules=sorted(changed),affected_modules=sorted(affected),graph=graph,
        snapshots=snapshots,prior_receipt_pins=prior_pins,prior_full_manifest_checked=len(history),
        reused_core_support=core_result,cache_links=cachelinks,
        reviewer_identity=oldseal['reviewer_identity'],semantic_controls_rerun=False,
        justification='Only deletion changed; prior semantic controls and remaining proof bodies preserved. Fresh affected builds, complete axiom coverage and removed-name lookup are motivated checks.'))
    print('Verified exact deletion; 35 -> 33; affected modules',len(affected),'read-only cached objects',len(cachelinks),flush=True)

def env():
    e=os.environ.copy(); e.pop('LEAN_SRC_PATH',None)
    paths=[OUT]+sorted(p/'.lake/build/lib/lean' for p in (BASE/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir())
    e['LEAN_PATH']=os.pathsep.join(map(str,paths)); e['PATH']=str(BIN)+os.pathsep+e['PATH']
    e['TEMP']=e['TMP']=str(ROOT/'tmp'); return e

def run(source,folder,output=None):
    folder.mkdir(parents=True,exist_ok=True)
    cmd=[str(BIN/'lean.exe'),'-R',str(SRC)]
    if output:
        assert output.resolve().is_relative_to(OUT) and not output.exists()
        output.parent.mkdir(parents=True,exist_ok=True); cmd+=['-o',str(output)]
    cmd+=[str(source)]
    before=info(source); write(folder/source.name,source.read_bytes()); started=stamp(); t=time.monotonic()
    p=subprocess.run(cmd,cwd=ROOT,env=env(),capture_output=True)
    write(folder/'stdout.txt',p.stdout); write(folder/'stderr.txt',p.stderr)
    row=dict(source=before,source_unchanged=info(source)==before,command=cmd,cwd=str(ROOT),
        started_utc=started,finished_utc=stamp(),seconds=time.monotonic()-t,returncode=p.returncode,
        stdout=info(folder/'stdout.txt'),stderr=info(folder/'stderr.txt'))
    if output: row['object']=info(output) if output.exists() else None
    record(folder/'RESULT.json',row)
    return row,(p.stdout+p.stderr).decode('utf-8',errors='replace')

def build():
    d=read(ROOT/'DELTA_COMPARISON.json'); graph=d['graph']; done=set(); results={}
    record(ROOT/'TOOLCHAIN.json',dict(lean=info(BIN/'lean.exe'),version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),
        lean_path=env()['LEAN_PATH'].split(os.pathsep),cache_policy='Accepted A1 and previously recompiled unchanged CoreSupport reused read only; no V354 object reused'))
    while len(done)<len(graph):
        ready=[m for m,deps in graph.items() if m not in done and set(deps)<=done]
        assert ready
        for m in ready:
            r,out=run(SRC/modulepath(m),ROOT/'build_logs'/m,(OUT/Path(*m.split('.'))).with_suffix('.olean'))
            results[m]=r; record(ROOT/'BUILD_PROGRESS.json',results)
            print(m,r['returncode'],round(r['seconds'],2),flush=True)
            if r['returncode'] or not r['object']: print(out[-5000:],flush=True); raise RuntimeError('Source build failed')
            done.add(m)
    audits={}
    for m in ['TGLExt.AuditA2RegularSupport','Audit33Independent']:
        r,out=run(SRC/modulepath(m),ROOT/'build_logs'/m,(OUT/Path(*m.split('.'))).with_suffix('.olean'))
        audits[m]=r; print(m,r['returncode'],flush=True)
        if r['returncode']: print(out[-5000:]); raise RuntimeError('Audit failed')
    absent,out=run(SRC/'RemovedNamesAbsent.lean',ROOT/'removed_names_check')
    missing=[n for n in QUALIFIED if re.search(r'Unknown (?:identifier|constant)[^\n]*'+re.escape(n),out,re.I)]
    absent['diagnostic']=out
    absent['both_removed_names_unavailable']=absent['returncode']!=0 and set(missing)==set(QUALIFIED) and not re.search(r'unknown module|object file .*does not exist|unexpected token',out,re.I)
    record(ROOT/'BUILD_DELTA01.json',dict(modules=results,audits=audits,removed_name_check=absent,
        source_count=len(results),all_builds_ok=all(r['returncode']==0 for r in list(results.values())+list(audits.values()))))
    print('Removed names absent:',absent['both_removed_names_unavailable'],flush=True)

if __name__=='__main__': {'prepare':prepare,'build':build}[sys.argv[1]]()
