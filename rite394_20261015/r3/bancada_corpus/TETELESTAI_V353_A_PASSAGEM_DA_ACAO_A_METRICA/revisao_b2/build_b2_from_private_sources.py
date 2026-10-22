from pathlib import Path
from datetime import datetime
import hashlib,json,os,subprocess,sys,time,traceback

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT=R/'revisao_b2'; S=R/'s'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
ATT=OUT/('build_'+STAMP)

def now():return datetime.now().astimezone().isoformat()
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):
    b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+STAMP)
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p)

def main():
    ATT.mkdir()
    snap_ptr=json.loads((OUT/'B2_FINAL_SNAPSHOT_POINTER.json').read_bytes())
    snap_path=Path(snap_ptr['snapshot']['path']); assert pin(snap_path)==snap_ptr['snapshot']
    snap=json.loads(snap_path.read_bytes())
    for rec in snap['sources']:
        assert pin(Path(rec['copy']['path']))==rec['copy']
        assert pin(Path(rec['source']['path']))==rec['source']
    protected_paths=[R/'revisao'/'REVIEW_B1_FINAL.md',R/'revisao'/'REVIEW_B1_FINAL.json',R/'r'/'compilation.json',R/'r'/'run.json',R/'MANIFESTO_B1.json']
    protected=[pin(p) for p in protected_paths]
    env=os.environ.copy()
    for k in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(k,None)
    env['PATH']=str(BIN)+os.pathsep+env.get('PATH','')
    env['GIT_OPTIONAL_LOCKS']='0'
    manifest=json.loads((S/'lake-manifest.json').read_bytes())
    start_count=int(env.get('GIT_CONFIG_COUNT','0'))
    safe=[]
    for i,pkg in enumerate(manifest['packages'],start_count):
        p=(S/'.lake'/'packages'/pkg['name']).resolve()
        assert p.is_relative_to(S.resolve())
        safe.append(str(p))
        env['GIT_CONFIG_KEY_'+str(i)]='safe.directory'
        env['GIT_CONFIG_VALUE_'+str(i)]=str(p).replace('\\','/')
    env['GIT_CONFIG_COUNT']=str(start_count+len(safe))
    save(ATT/'environment_scope.json',dict(safe_directories_process_only=safe,global_git_config_modified=False,lean_path_removed=True,source_snapshot=pin(snap_path),script=pin(Path(__file__)),protected_before=protected))
    allruns=[]
    for label,targets in [('suppliers',['TGLExt.GeneralMetricEinstein']),('b2',['TGLExt.FLRWGeometry','TGLExt.FLRWFieldEquations','TGLExt.AuditFLRW','TGLExt.ReviewFLRW'])]:
        d=ATT/label;d.mkdir()
        cmd=[str(BIN/'lake.exe'),'build',*targets]
        start=time.time()
        with (d/'lake_stdout.txt').open('xb') as out,(d/'lake_stderr.txt').open('xb') as err:
            proc=subprocess.Popen(cmd,cwd=S,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
            process=dict(pid=proc.pid,command=cmd,cwd=str(S),started=now(),label=label)
            save(d/'process.json',process)
            save(OUT/'state.json',dict(status='LAKE_RUNNING',attempt=str(ATT),run_directory=str(d),**process))
            print('LAKE_STARTED',label,proc.pid,str(d),flush=True)
            rc=proc.wait()
        run=dict(returncode=rc,elapsed_seconds=time.time()-start,finished=now(),command=cmd,cwd=str(S),streams=[pin(d/'lake_stdout.txt'),pin(d/'lake_stderr.txt')],toolchain=subprocess.check_output([str(BIN/'lean.exe'),'--version'],env=env).decode().strip(),executables=[pin(BIN/'lean.exe'),pin(BIN/'lake.exe')])
        save(d/'run.json',run);allruns.append(dict(label=label,run=pin(d/'run.json'),returncode=rc))
        print('LAKE_EXIT',label,rc,flush=True)
        if rc!=0:
            save(OUT/'state.json',dict(status='LAKE_FAILED',label=label,attempt=str(ATT),returncode=rc,runs=allruns))
            return rc
    checks=[]
    for rec in snap['sources']:
        checks.append(dict(module=rec['module'],source_unchanged=pin(Path(rec['source']['path']))==rec['source'],copy_unchanged=pin(Path(rec['copy']['path']))==rec['copy']))
    unchanged=all(pin(Path(p['path']))==p for p in protected)
    objects=[]
    build=S/'.lake'/'build'/'lib'/'lean'
    for p in sorted(build.rglob('*.olean')):
        if p.relative_to(build).parts[0] in ['TGL','TGLExt']:objects.append(pin(p))
    assert all(x['source_unchanged'] and x['copy_unchanged'] for x in checks)
    assert unchanged
    save(ATT/'completion.json',dict(status='BUILDS_RC0__FINAL_AUDIT_PENDING',runs=allruns,source_checks=checks,project_objects=objects,protected_unchanged=unchanged,source_snapshot=pin(snap_path),timestamp=now()))
    save(OUT/'state.json',dict(status='BUILDS_RC0__FINAL_AUDIT_PENDING',attempt=str(ATT),runs=allruns,project_objects=len(objects),B1_protected_unchanged=unchanged))
    print('B2_BUILDS_RC0',len(objects),'PROJECT_OBJECTS','B1_UNCHANGED',unchanged,flush=True)
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception:
        if ATT.exists():save(ATT/'driver_failure.json',dict(timestamp=now(),error=traceback.format_exc()))
        raise
