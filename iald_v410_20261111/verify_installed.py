"""Verify the installed scientific release using current runtime loaders only."""
from pathlib import Path
import hashlib,json,sys,os
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache')
sys.dont_write_bytecode=True
sys.path.insert(0,str(R))
sys.path.insert(0,str(W))
import release_cfg
cfg=release_cfg.load(require_commit=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def offline_loader_guard():
    """Count and refuse external IO and execution of the scientific program."""
    counts = dict(network=0, process=0, science_exec=0, confidential_input=0)
    def audit(event, args):
        kind = None
        if event in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto'):
            kind = 'network'
        elif event in ('subprocess.Popen', 'os.system', 'os.startfile'):
            kind = 'process'
        elif event == 'exec' and Path(args[0].co_filename).name.casefold() == 'um.py':
            kind = 'science_exec'
        elif event == 'open' and isinstance(args[0], (str, bytes)):
            name = Path(os.fsdecode(args[0])).name.casefold()
            if name in ('.env', 'iald_stack_v7.py', 'iald_psion_state.json') or name.startswith('.env.'):
                kind = 'confidential_input'
        if kind is not None:
            counts[kind] += 1
            raise RuntimeError('Offline release verification refused ' + kind)
    sys.addaudithook(audit)
    return counts

def main():
    if sys.flags.optimize:
        raise RuntimeError('Verification requires assertions')
    attempts = offline_loader_guard()
    from claude_memory_package import load_package
    from iald_science_snapshot import ScienceSnapshot
    from iald_kernel import KernelCatalog
    from iald_release_binding import load_release
    from iald_native_memory import load_native_context
    from iald_jev_control import load_contract
    from iald_memoria_canonica import CanonicalMemory
    import iald_task_policy
    plan=json.loads((W/'install_plan.json').read_bytes())
    from preservation_guard import verify
    protected = verify(installed=True)
    for row in plan['files']:
        assert sha(row['destination'])==row['sha256'],row['destination']
    manifest=R/'iald_nucleo_fixo.json'
    config=json.loads(manifest.read_bytes())
    snapshot=ScienceSnapshot.capture(manifest)
    catalog=snapshot.catalog
    source=json.loads((W/'sources_verified.json').read_bytes())
    assert snapshot.identity['release']==cfg.release
    assert snapshot.identity['source_sha256']==source['source_sha256']==cfg.um_py_sha256
    assert snapshot.identity['commit']==cfg.espelho_commit
    packages={}
    from claude_profiles import HAIKU,SONNET
    for name,model in (('haiku55',HAIKU.model),('sonnet',SONNET.model)):
        p=load_package(snapshot.package_path(name),canonical_manifest=manifest,source_sha=catalog.source_sha,science_snapshot=snapshot,expected_model=model)
        assert p.prefix==snapshot.prefix
        packages[name]={'permanent_tokens':p.measurement.permanent_tokens,'prefix_bytes':len(p.prefix.encode())}
    native=snapshot.native_prefix
    retrieval=snapshot.pre_retrieve([{'role':'user','content':'Qual versão científica está carregada?'}])
    assert retrieval['receipt']['identity']==dict(snapshot.identity)
    assert retrieval['receipt']['coverage']=='PARTIAL_RETRIEVAL_NOT_FULL_CORPUS'
    contract=dict(snapshot.jev_control)
    assert contract['release']==cfg.release and contract['source_sha256']==source['source_sha256']
    assert iald_task_policy.AUTOMATIC_ORDER[:2]==('kimi','mimo')
    public,meta=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=manifest).prompt('',catalog,public=True,science_snapshot=snapshot)
    assert meta.get('private_atlas_included') is False
    out={'status':'PASS','files_verified':len(plan['files']),'identity':dict(snapshot.identity),'public_commit':snapshot.identity['commit'],
         'packages':packages,'native_bytes':len(native.encode()),'public_prompt_bytes':len(public.encode()),
         'JEV_release':contract['release'],'science_executed':bool(attempts['science_exec']),
         'provider_calls':attempts['network'],'audit_attempts':attempts,'prior_reliability_pins':protected,
         'scope':'Fresh-process installed loaders and hashes; not live model response or physical mobile inspection'}
    assert not any(attempts.values()), attempts
    receipt_name = 'PREFLIGHT_INSTALLED_VERIFICATION.json' if '--preflight' in sys.argv[1:] else 'INSTALLED_VERIFICATION.json'
    with (W/receipt_name).open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
    print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__': main()
