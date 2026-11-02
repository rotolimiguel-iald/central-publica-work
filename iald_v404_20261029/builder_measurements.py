"""Builder measurements (read-only; writes BUILDER_MEASUREMENTS.json once). Everything is read from the artifacts."""
import json,subprocess,sys,hashlib
from pathlib import Path
W=Path(__file__).resolve().parent;P=W.parent/'iald_v402_20261027'
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
 'executor_windows_v404':cur,'executor_windows_v402':prev,'delta_v404_minus_v402':delta,
 'native_counts_v404':native(W),'native_counts_v402':native(P),'prefix_bytes_v404':sizes(W),'prefix_bytes_v402':sizes(P),
 'expanded_suffixes':{'v404':fin['expanded_suffixes'],'v402':finp['expanded_suffixes']},
 'estimated_remaining_haiku55_before_native_count':{'v404':fin['estimated_remaining_haiku55'],'v402':finp['estimated_remaining_haiku55']},
 'topics':{'v404':fin['topics'],'v402':finp['topics']},'capsule_measurement_v404':cap,'capsule_measurement_v402':cap_prev,
 'measure_script_sha256':hashlib.sha256((W/'measure_shared_capsules.py').read_bytes()).hexdigest(),
 'expand_override_decision':{'value':[],'policy':'D (decisao da gerencia a7, 29/10/2026): nenhum sufixo expandido no haiku55; A/B/C estouram a folga; os topicos _v404 entram compactos com ponteiro @; redesenhar a politica antes da v406','candidates_table_source':'EXPAND_AND_COMMIT_MEASUREMENTS.json','candidates':{k:{kk:vv for kk,vv in v.items() if kk in ('expand_suffixes','haiku_expanded_bytes','estimated_remaining_finalize_0.60_tok_per_byte','projected_remaining_at_observed_v402_ratio','finalize_result','shared_bytes','executor_windows')} for k,v in rd(W/'EXPAND_AND_COMMIT_MEASUREMENTS.json')['candidates'].items()}},
 'espelho_pin':{'pinned_commit':fin['commit'],'custody_commit':'3ae6f43fcb11bea868673415a54ce5933eaa3527','custody_is_ancestor_of_pinned':True,'differing_files_between_custody_and_pinned_among_those_prepare_reads':rd(W/'EXPAND_AND_COMMIT_MEASUREMENTS.json')['espelho_pin']['differing'],'reason':'decisao da gerencia a7 29/10: README.md e read-brief.md do commit pinado trazem a correcao ao lado (18 calculadas e 0 literais)'},
 'revision':'r2',
 'management_decisions_29_10_gerencia_a7':{
   'C_shared_p2_window':'decoupled from the haiku55 EXPAND_OVERRIDE: release_cfg.SHARED_P2_SUFFIXES read by prepare.py (None = previous behaviour); EXPAND_OVERRIDE=() stays for haiku55 only',
   'F_value':"SHARED_P2_SUFFIXES = ('_v401','_v402','_v403','_v404') (variant F: the installed v402 window plus the new releases)",
   'F1_waived':'bandeiras_do_gate_v403 correcting statements (estatuto, scope 18...0 literais, limites, diz, nao_diz) are inline in haiku55; "present in full" was over-strict wording in the brief',
   'F3_accepted':'the old wording 15 calculadas e 3 literais survives only inside the sealed v392 record, quoted there as superseded; the correction is in every prefix; sealed records are not rewritten'},
 'literal_carriage_real_build':{k:v for k,v in rd(W/'LITERAL_CARRIAGE_R2.json').items() if k not in ('per_topic','note','root')},
 'literal_carriage_detail_file':'LITERAL_CARRIAGE_R2.json (+ NO_REGRESSION_R2.txt: reviewer r11 script on the real build)',
 'r1_superseded_to':'superseded_r1/ (MOVED_MANIFEST.json); r1 evidence stays pinned in the mission history',
 'scope':'Builder arithmetic and structural measurement on the built artifacts; no provider call; not independent review.'}
with (W/'BUILDER_MEASUREMENTS.json').open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(json.dumps({'windows_v404':cur,'delta':delta,'native_v404':out['native_counts_v404'],'cap':cap},ensure_ascii=False,indent=1))
