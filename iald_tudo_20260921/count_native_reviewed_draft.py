"""Free counts of reviewed memory through the prepared native-wire adapter."""
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace
import hashlib
import json
import sys
from dotenv import dotenv_values
import anthropic
from verify_reviewed_draft import verify
from claude_native_counter import count_native_request
from claude_profiles import HAIKU, reasoning_parameters, context_budget

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
import iald_kernel
import iald_fontes_publicas
import iald_core_indexado
from iald_motor_claude import converter_pedido

def main():
    path = Path(sys.argv[1]).resolve()
    checked = verify(path)
    raw = path.read_bytes()
    prefix = raw.decode('utf-8')
    if '<ATLAS_CANONICO' in prefix:
        raise ValueError('Private Atlas forbidden')
    definitions = (iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions())
    names = [t['function']['name'] for t in definitions]
    if set(names) != {'iald_kernel_verification','iald_kernel_search','iald_kernel_read','iald_kernel_list','iald_public_read','search_tgl','fetch_tgl'}:
        raise ValueError('Public tool set changed')
    cfg = SimpleNamespace(modelo=HAIKU.model,max_saida=4096,cache_ttl='5m',esforco_claude='high')
    payload = {'model':HAIKU.model,'max_tokens':4096,'messages':[
        {'role':'system','content':prefix},
        {'role':'user','content':'Quem é o autor da TGL? Explique Hamiltoniano, Lindblad e dephasing no escopo documentado.'}],
        'tools':definitions}
    wire = converter_pedido(cfg,payload,prefixo=prefix)
    wire.pop('output_config',None)
    wire.update(reasoning_parameters(HAIKU.model,4096))
    prefix_only = {'model':HAIKU.model,'system':wire['system'],
                   'messages':[{'role':'user','content':'.'}], 'thinking':{'type':'disabled'}}
    key = dotenv_values(ROOT/'.env').get('IALD_CLAUDE_API_KEY')
    if not key:
        raise ValueError('Credential absent')
    with anthropic.Anthropic(api_key=key,max_retries=0,timeout=120) as client:
        permanent = count_native_request(client,prefix_only)
        whole = count_native_request(client,wire)
    decision = context_budget(HAIKU.model,counted_model=HAIKU.model,
        permanent_tokens=permanent,request_input_tokens=whole,reserved_output_tokens=4096)
    result = {'time_utc':datetime.now(timezone.utc).isoformat(),'model':HAIKU.model,
        'status':'NATIVE_WIRE_COUNTED_NOT_DEPLOYED','draft_sha256':checked['draft_sha256'],
        'draft_path':str(path),'permanent_measurement_includes_minimal_user_message':True,
        'budget':decision,'tool_names':names,
        'native_tools_sha256':hashlib.sha256(json.dumps(wire['tools'],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
        'not_included':['runtime user profile/service note','conversation history','tool result turns'],
        'count_requests':2,'generation_requests':0}
    target = WORK / ('haiku_native_wire_count_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
    with target.open('xb') as stream:
        stream.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(result,ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'FAILED','exception_type':type(exc).__name__}))
        raise SystemExit(1)
