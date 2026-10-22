from review import *

SUSY=PRIOR.parent/'A2_SUSY_012'
EXTRA=['V354CoreProjectionLattice','V354ProjectionTraceSubadditivity','V354RegularSusy','V354RegularLegacyWitness']

def prepare():
    initial=read(ROOT/'INPUTS.json')
    assert all(current(r['source']) and current(r['copy']) for r in initial['snapshots'])
    d=read(PRIOR/'DELTA01/BUILD_DELTA01.json')
    seal=read(PRIOR/'DELTA01/SELO_DELTA01.json')
    assert all(current(r) for r in seal['files'])
    links=[]
    for m,r in d['modules'].items():
        assert r['returncode']==0 and current(r['source']) and current(r['object'])
        p=Path(r['object']['path']); q=OUT/'TGLExt'/p.name
        assert not q.exists(); os.link(p,q)
        susy_copy=SUSY/'k/TGLExt'/(m.split('.')[-1]+'.lean')
        assert susy_copy.read_bytes()==Path(r['source']['path']).read_bytes()
        links.append(dict(source=r['source'],borrowed=r['object'],review=info(q),susy_source=info(susy_copy)))
    core=read(PRIOR/'BUILD.json')['modules']['TGL.CoreSupport']
    assert core['returncode']==0 and current(core['object']) and current(core['source'])
    q=OUT/'TGL/CoreSupport.olean'; assert not q.exists(); os.link(core['object']['path'],q)
    links.append(dict(source=core['source'],borrowed=core['object'],review=info(q)))
    assert (SUSY/'k/TGLExt/V354BoundedPolar.lean').read_bytes()==(SRC/'TGLExt/V354BoundedPolar.lean').read_bytes()
    snapshots=[]; names=[]; scan=[]
    for m in EXTRA:
        author=(AUTHOR/'src' if m=='V354RegularLegacyWitness' else SUSY/'k')/'TGLExt'/(m+'.lean')
        p=SRC/'TGLExt'/author.name; before=info(author); write(p,author.read_bytes()); assert current(before)
        clean=code_only(p.read_text(encoding='utf-8'))
        public=re.findall(r'^(?:@\[[^\n]*?\]\s*)?(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev|structure)\s+([\w.]+)',clean,re.M)
        ns='TGLV354.TraceCompletion.' if m=='V354RegularLegacyWitness' else 'TGLV354.'
        qualified=[ns+n for n in public]; names+=qualified
        forbidden=re.findall(r'\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b',clean,re.M)
        assert not forbidden
        snapshots.append(dict(module='TGLExt.'+m,source=before,copy=info(p)))
        scan.append(dict(source=info(p),names=qualified,anonymous_instances=len(re.findall(r'^instance\b',clean,re.M)),forbidden=forbidden))
    for name,path in [('AUDIT_NAMES_FULL.json',AUTHOR/'AUDIT_NAMES_FULL.json'),('SUSY_AUDIT_NAMES.json',SUSY/'AUDIT_NAMES.json')]:
        write(ROOT/'inputs'/name,path.read_bytes())
    write(SRC/'DiscoverAllExports.lean','import TGLExt.V354RegularLegacyWitness\nimport TGLExt.V354RegularSusy\n#print prefix TGLV354\n')
    record(ROOT/'ASSEMBLY_INPUTS.json',dict(snapshots=snapshots,explicit_public_names=names,source_scan=scan,
        A2_reused_objects=links,prior_delta_seal=info(PRIOR/'DELTA01/SELO_DELTA01.json'),
        same_polar_bytes=True,anonymous_instance_count=sum(r['anonymous_instances'] for r in scan),
        scope='Exact legacy assembly plus concrete SUSY on full projection lattice; no physical or canonical integration'))
    print('Prepared',len(snapshots),'additional modules;',len(names),'explicit public names; anonymous instances',sum(r['anonymous_instances'] for r in scan),flush=True)

def build():
    results={}
    for m in EXTRA:
        p=SRC/'TGLExt'/(m+'.lean')
        r,out=run(p,ROOT/'assembly_logs'/m,OUT/'TGLExt'/(m+'.olean'))
        results['TGLExt.'+m]=r; record(ROOT/'ASSEMBLY_BUILD_PROGRESS.json',results)
        print(m,r['returncode'],round(r['seconds'],2),flush=True)
        if r['returncode'] or not r['object']: print(out[-6000:]); raise RuntimeError('Assembly build failed')
    discovery,out=run(SRC/'DiscoverAllExports.lean',ROOT/'assembly_logs/DiscoverAllExports')
    record(ROOT/'ASSEMBLY_BUILD.json',dict(modules=results,discovery=discovery))
    print('Export discovery',discovery['returncode'],flush=True)
    if discovery['returncode']: print(out[-6000:]); raise RuntimeError('Discovery failed')

if __name__=='__main__': {'prepare':prepare,'build':build}[sys.argv[1]]()
