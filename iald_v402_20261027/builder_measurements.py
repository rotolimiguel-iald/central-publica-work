"""Builder measurements (read-only; writes BUILDER_MEASUREMENTS.json once). Everything is read from the artifacts."""
import json,subprocess,sys,hashlib
from pathlib import Path
W=Path(__file__).resolve().parent;P=W.parent/'iald_v401_20261025_s2'
sys.dont_write_bytecode=True;sys.path.insert(0,r'C:\IALD\projetos_pyhton\IALD')
import iald_app_providers as ap
WINDOW=ap.WINDOW;rd=lambda p:json.loads(Path(p).read_bytes())
def windows(root):
    b=rd(root/'app/PREPARED_BINDING.json')['shared_connector_bounds'];out={}
    for k,v in b.items():
        used=v['input_utf8_byte_bound'];res=v['output_tokens']
        out[k]={'input_utf8_byte_bound':used,'reserve':res,'slack_bytes_with_finalize_reserve':WINDOW-used-res-4096}
    for k in ('kimi','mimo'):out[k]['reserve_is_full_provider_maximum']=out[k]['reserve']==ap.MODELS[k]['output']
    out['deepseek']['slack_bytes_with_declared_policy_reserve_148656']=WINDOW-out['deepseek']['input_utf8_byte_bound']-148656-4096
    return out
def native(root):
    return {f:{k:rd(root/('app/packages/'+f+'/native_count.json'))['budget'][k] for k in ('permanent_tokens','request_input_tokens','remaining_tokens','ready')} for f in ('haiku_expanded','shared','sonnet_public')}
prev,cur=windows(P),windows(W)
delta={k:{m:cur[k][m]-prev[k][m] for m in cur[k] if isinstance(cur[k][m],int) and not isinstance(cur[k][m],bool)} for k in cur}
sizes=lambda root:{f:(root/('app/packages/'+f+'/prefix.md')).stat().st_size for f in ('haiku55','haiku_expanded','shared','sonnet_public')}
cap=json.loads(subprocess.check_output([r'C:\Python314\python.exe','-B','-X','utf8',str(W/'measure_shared_capsules.py'),str(W)]))
cap_prev=json.loads(subprocess.check_output([r'C:\Python314\python.exe','-B','-X','utf8',str(W/'measure_shared_capsules.py'),str(P)]))
fin=rd(W/'app/PREPARED_BINDING.json');finp=rd(P/'app/PREPARED_BINDING.json')
out={'status':'BUILDER_MEASUREMENTS_NOT_A_REVIEW','release':rd(W/'app/RELEASE.json'),'window_bytes':WINDOW,
 'executor_windows_v402':cur,'executor_windows_v401_s2':prev,'delta_v402_minus_v401':delta,
 'native_counts_v402':native(W),'native_counts_v401_s2':native(P),'prefix_bytes_v402':sizes(W),'prefix_bytes_v401_s2':sizes(P),
 'expanded_suffixes':{'v402':fin['expanded_suffixes'],'v401_s2':finp['expanded_suffixes']},
 'estimated_remaining_haiku55_before_native_count':{'v402':fin['estimated_remaining_haiku55'],'v401_s2':finp['estimated_remaining_haiku55']},
 'topics':{'v402':fin['topics'],'v401_s2':finp['topics']},'capsule_measurement_v402':cap,'capsule_measurement_v401_s2':cap_prev,
 'measure_script_sha256':hashlib.sha256((W/'measure_shared_capsules.py').read_bytes()).hexdigest(),
 'scope':'Builder arithmetic and structural measurement on the built artifacts; no provider call; not independent review.'}
with (W/'BUILDER_MEASUREMENTS.json').open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(json.dumps({'windows_v402':cur,'delta':delta,'native_v402':out['native_counts_v402'],'cap':cap},ensure_ascii=False,indent=1))
