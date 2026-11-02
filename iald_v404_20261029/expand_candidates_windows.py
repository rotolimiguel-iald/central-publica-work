"""Read-only: executor windows per candidate (replicates finalize.py bounds section on each scratch shared prefix)."""
import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path.insert(0,str(R))
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory,iald_app_providers as ap
SP=Path(r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad')
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
WINDOW=ap.WINDOW
def bounds(shared,rel='v404'):
    out={}
    for provider in ('kimi','mimo','deepseek'):
        body={'messages':[{'role':'system','content':shared},{'role':'user','content':'Explique o alcance documentado da '+rel+'.'}],'tools':[] if provider=='kimi' else tools}
        if provider!='kimi':body.update(model=ap.MODELS[provider]['model'],stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
        if provider=='deepseek':body['reasoning_effort']='max'
        reserve=ap.MODELS[provider]['output'] if provider=='kimi' else ap.output_budget(body,ap.MODELS[provider]['output'])
        if provider!='kimi':body['max_tokens' if provider=='deepseek' else 'max_completion_tokens']=reserve
        used=ap.check_window(body,reserve)
        d={'input_utf8_byte_bound':used,'reserve':reserve,'slack_full_reserve':WINDOW-used-reserve-4096}
        if provider=='deepseek':d['slack_declared_policy_reserve_148656']=WINDOW-used-148656-4096
        out[provider]=d
    return out
res={}
for n in 'ABCD':
    shared=(SP/('cand'+n)/'iald_v404_20261029/app/packages/shared/prefix.md').read_text(encoding='utf8')
    res[n]={'shared_bytes':len(shared.encode()),'windows':bounds(shared)}
print(json.dumps(res,indent=1))
