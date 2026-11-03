"""Reviewer (sonnet-app-v405-revisor-d): installed-release loaders in a FRESH process, own code, audit hook
(no network / subprocess / writes / secrets). Prints one JSON object. The runtime modules are imported
read-only; nothing is executed against a provider; no Lean / um.py.
Adapted from the v404 reviewer's d2_loaders.py; extended for D4 (JEV core packet, contract file) and D5
(claude_context_snapshot.load_snapshot + claude_profiles.context_budget on the installed haiku55 package)."""
import os,sys,json,hashlib
from pathlib import Path
R=Path(r'C:\IALD\projetos_pyhton\IALD')
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime'/'tokenizer_cache')
sys.dont_write_bytecode=True
BLOCKED_NAMES=('.env','iald_stack_v7.py','iald_psion_state.json','.iald_secret_key','auth.json','.credentials.json','.iald_keys','.tgl_site','.iald_privado')
attempts={'blocked_events':[],'opens':0}
def guard(event,args):
    if event in('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
        attempts['blocked_events'].append(event);raise RuntimeError('blocked '+event)
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        attempts['opens']+=1
        p=Path(os.fsdecode(path)).resolve()
        if p.name in BLOCKED_NAMES:raise RuntimeError('secret input forbidden: '+p.name)
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing:raise RuntimeError('write forbidden: '+str(p))
sys.addaudithook(guard)
sys.path.insert(0,str(R))
sha=lambda b:hashlib.sha256(b).hexdigest()
from claude_memory_package import load_package
from claude_context_snapshot import load_snapshot,context_metadata,HaikuUnavailable
from claude_profiles import HAIKU,context_budget
from iald_kernel import KernelCatalog
from iald_release_binding import load_release
from iald_native_memory import load_native_context
from iald_jev_control import load_contract
from iald_memoria_canonica import CanonicalMemory
manifest=R/'iald_nucleo_fixo.json'
cfg=json.loads(manifest.read_bytes());cl=cfg['active_cluster']
cat=KernelCatalog(cl['kernel_bundle'],cl['kernel_verification'])
rel=load_release(manifest,source_sha=cat.source_sha)
out={'identity':rel.identity,'kernel_sources':len(cat.records),'kernel_source_sha':cat.source_sha}
pk={};snap={}
for name in('haiku55','haiku'):
    d=R/'.iald_runtime'/name
    p=load_package(d,canonical_manifest=manifest,source_sha=cat.source_sha)
    pk[name]={'permanent_tokens':p.measurement.permanent_tokens,'prefix_bytes':len(p.prefix.encode()),'prefix_sha256':sha(p.prefix.encode()),'model':getattr(p.measurement,'model',None),
              'reserved_output_tokens':p.reserved_output_tokens,'available_dynamic_tokens':p.available_dynamic_tokens,'tools_sha256':p.tools_sha256}
    # D5: the snapshot/profile layer (claude_context_snapshot + claude_profiles), exactly as the server loads it
    try:
        package,s=load_snapshot(d,lambda dd,_m=manifest,_s=cat.source_sha:load_package(dd,canonical_manifest=_m,source_sha=_s))
        meta=context_metadata(s)
        nc=json.loads((d/'native_count.json').read_bytes());b=nc['budget']
        recomputed=context_budget(HAIKU.model,counted_model=HAIKU.model,permanent_tokens=b['permanent_tokens'],request_input_tokens=b['request_input_tokens'],reserved_output_tokens=b['reserved_output_tokens'],margin_tokens=b['margin_tokens'])
        man=json.loads((d/'manifest.json').read_bytes())
        snap[name]={'loaded':True,'permanent':s.permanent,'reference_input':s.reference_input,'output':s.output,'margin':s.margin,'reference_remaining':s.reference_remaining,
                    'prefix_sha256':s.prefix_sha256,'tools_sha256':s.tools_sha256,'measurement_receipt':s.measurement_receipt,
                    'meta_reserva_dinamica_medida':meta['reserva_dinamica_medida'],'meta_memoria_tokens_medidos':meta['memoria_tokens_medidos'],'meta_janela':meta['janela'],'meta_modelo':meta['modelo'],
                    'native_count_budget_equals_recomputed_context_budget':recomputed==b,'native_count_budget_equals_manifest_budget':man['budget']==b,
                    'native_count_prefix_sha256':nc['prefix_sha256'],'native_count_deployment_equals_release':nc['deployment']==rel.identity,'native_count_public_commit':nc['public_commit'],
                    'native_count_tools_sha256':nc['native_tools_sha256'],'manifest_counted_scoped_tools_sha256':man.get('counted_scoped_tools_sha256'),
                    'native_count_generation_requests':nc['generation_requests'],'native_count_private_atlas_included':nc['private_atlas_included'],'native_count_operator_context_sent':nc['operator_context_sent'],
                    'floor_remaining_ge_10000':s.reference_remaining>=10000,'memory_target':HAIKU.memory_target,'memory_target_met':s.permanent>=HAIKU.memory_target}
    except HaikuUnavailable as exc:
        snap[name]={'loaded':False,'refusal':str(exc)}
out['packages']=pk;out['snapshots']=snap
native,ident=load_native_context(manifest,cat)
out['native']={'bytes':len(native.encode()),'sha256':sha(native.encode()),'identity_equals_release':ident==rel.identity}
c=load_contract(R)
cj=R/cfg['jev_control']['path'] if not Path(cfg['jev_control']['path']).is_absolute() else Path(cfg['jev_control']['path'])
cp=c.get('core_packet') or {}
out['jev']={'release':c['release'],'schema':c['schema'],'source_sha256':c['source_sha256'],'contract_file':str(cj),'contract_file_exists':cj.is_file(),'contract_file_sha256':sha(cj.read_bytes()),
            'manifest_pin':cfg['jev_control']['sha256'],'core_packet_file':cp.get('arquivo'),'core_packet_sha256':cp.get('sha256'),'core_packet_um_version':cp.get('um_version'),
            'core_packet_root_sha256':sha((R/cp['arquivo']).read_bytes()) if cp.get('arquivo') else None}
public,meta=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=manifest).prompt('',cat,public=True)
out['public_prompt']={'bytes':len(public.encode()),'sha256':sha(public.encode()),'private_atlas_included':meta.get('private_atlas_included'),'atlas_marker_in_text':'<ATLAS_CANONICO' in public}
out['audit']={'blocked_events_attempted':attempts['blocked_events'],'open_events_seen':attempts['opens']}
print(json.dumps(out,ensure_ascii=False))
