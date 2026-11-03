"""Reviewer (sonnet-app-v405-revisor): executor windows (Kimi, MiMo, DeepSeek), Haiku/Sonnet native-count arithmetic + chain, Jev contract/packet.
Runtime imported READ-ONLY with an audit hook that refuses sockets, subprocess and any file write outside the scratch dir. No Lean/um.py executed."""
import os,sys,json,hashlib
from pathlib import Path
W=Path(sys.argv[1]);SCRATCH=Path(sys.argv[2]).resolve()
R=Path(r'C:\IALD\projetos_pyhton\IALD');ST=W/'app/science/memory_stage'
sys.dont_write_bytecode=True
def guard(event,args):
    if event in('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('blocked '+event)
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name in('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('private input forbidden')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(SCRATCH):raise RuntimeError('write outside scratch: '+str(p))
sys.addaudithook(guard)
sys.path.insert(0,str(R))
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory,iald_app_providers as ap,iald_jev_control as jc
sha=lambda b:hashlib.sha256(b).hexdigest()
out={}
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
shared=(W/'app/packages/shared/prefix.md').read_text('utf-8')
rel=W.name.split('_')[1]
win={}
for provider in('kimi','mimo','deepseek'):
    body={'messages':[{'role':'system','content':shared},{'role':'user','content':'Explique o alcance documentado da '+rel+'.'}],'tools':[] if provider=='kimi' else tools}
    if provider!='kimi':body.update(model=ap.MODELS[provider]['model'],stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
    if provider=='deepseek':body['reasoning_effort']='max'
    reserve=ap.MODELS[provider]['output'] if provider=='kimi' else ap.output_budget(body,ap.MODELS[provider]['output'])
    if provider!='kimi':body['max_tokens' if provider=='deepseek' else 'max_completion_tokens']=reserve
    used=ap.check_window(body,reserve)
    own=len(json.dumps(body,ensure_ascii=False,separators=(',',':')).encode('utf-8'))  # independent wire size (compact JSON)
    own2=len(json.dumps(body,ensure_ascii=False).encode('utf-8'))
    win[provider]={'input_utf8_byte_bound':used,'reserve':reserve,'slack_full_reserve':ap.WINDOW-used-reserve-4096,'own_json_bytes_compact':own,'own_json_bytes_default':own2,
                   'admission_ge_own_json':used>=own2,'provider_max_output':ap.MODELS[provider]['output']}
win['deepseek']['slack_declared_policy_reserve_148656']=ap.WINDOW-win['deepseek']['input_utf8_byte_bound']-148656-4096
out['window_bytes']=ap.WINDOW;out['executor_windows']=win
out['shared_prefix_bytes']=len(shared.encode())
# Haiku / Sonnet native-count arithmetic + chain
nat={}
for f in('haiku_expanded','shared','sonnet_public'):
    root=W/'app/packages'/f;nc=json.loads((root/'native_count.json').read_bytes());man=json.loads((root/'manifest.json').read_bytes())
    pre=(root/'prefix.md').read_bytes();b=nc['budget']
    pi=json.loads((root/'permanent_count_intent.json').read_bytes());pr=json.loads((root/'permanent_count_result.json').read_bytes())
    wi=json.loads((root/'whole_request_count_intent.json').read_bytes());wr=json.loads((root/'whole_request_count_result.json').read_bytes())
    rem=1000000-b['request_input_tokens']-b['reserved_output_tokens']-b['margin_tokens']
    nat[f]={'prefix_sha256_file':sha(pre),'chain':{'native_count':nc['prefix_sha256']==sha(pre),'manifest':man['prefix_sha256']==sha(pre),'perm_intent':pi['prefix_sha256']==sha(pre),'whole_intent':wi['prefix_sha256']==sha(pre),
            'perm_result_to_intent':pr['intent_sha256']==sha((root/'permanent_count_intent.json').read_bytes()),'whole_result_to_intent':wr['intent_sha256']==sha((root/'whole_request_count_intent.json').read_bytes()),
            'tokens_equal_results':pr['input_tokens']==b['permanent_tokens'] and wr['input_tokens']==b['request_input_tokens']},
            'remaining_declared':b['remaining_tokens'],'remaining_recomputed':rem,'floor_10000_ok':rem>=10000,'generation_requests':nc['generation_requests'],'operator_context_sent':nc['operator_context_sent'],'private_atlas_included':nc['private_atlas_included'],
            'tokens_per_byte':round(b['permanent_tokens']/len(pre),4),'bytes':len(pre),'max_retries':[pi['max_retries'],wi['max_retries']]}
out['native']=nat
out['native_complete']=json.loads((W/'app/NATIVE_COUNTS_COMPLETE.json').read_bytes())
# Jev
try:
    c=jc.load_contract(ST);jv={'load_contract':'PASS','release':c['release'],'contract_bytes':len(jc.canonical_bytes(c))}
    text,meta=jc.load_core_packet(ST,c);jv['load_core_packet']='PASS';jv['packet_bytes']=meta['packet_bytes'];jv['packet_chars']=meta['characters']
    esc=lambda s:len(json.dumps(s,ensure_ascii=True).encode())
    jv['state_headroom']=jc.MAX_STATE_BYTES-esc(text)-esc(json.dumps(c,ensure_ascii=True))
    jv['contract_le_10000']=jv['contract_bytes']<=jc.MAX_CONTRACT_BYTES
except Exception as e:
    jv={'error':type(e).__name__+': '+str(e)[:200]}
out['jev']=jv
print(json.dumps(out,ensure_ascii=False,indent=1))
