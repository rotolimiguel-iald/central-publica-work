"""Prepare/count exact public bounded prefixes. No generation; no retries."""
from pathlib import Path
from types import SimpleNamespace
import argparse,hashlib,json,sys
R=Path(__file__).resolve().parent
sys.path[:0]=[str(R/'runtime'),r'C:\IALD\projetos_pyhton\IALD']
from iald_science_snapshot import ScienceSnapshot
from claude_profiles import HAIKU,SONNET,context_budget,reasoning_parameters
from claude_native_counter import count_native_request,native_count_parameters
from iald_motor_claude import converter_pedido
from claude_context_snapshot import native_tools_sha256
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory

def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,data):
    raw=json.dumps(data,ensure_ascii=False,indent=2).encode()
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw

def main():
    p=argparse.ArgumentParser();p.add_argument('--release',required=True);p.add_argument('--output',required=True);p.add_argument('--count',action='store_true');a=p.parse_args()
    snap=ScienceSnapshot.capture(a.release);out=Path(a.output)
    if not a.count:out.mkdir(parents=True,exist_ok=False)
    tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
    requests=[];prepared=[]
    for label,profile in [('haiku55',HAIKU),('sonnet',SONNET)]:
        folder=out/label
        if not a.count:folder.mkdir()
        prefix=snap.prefix;cfg=SimpleNamespace(modelo=profile.model,max_saida=profile.default_output,cache_ttl='5m',esforco_claude='medium' if profile is HAIKU else 'high')
        wire=converter_pedido(cfg,{'model':profile.model,'max_completion_tokens':profile.default_output,
             'messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da '+snap.identity['release']+'.'}], 'tools':tools},prefixo=prefix)
        wire.update(reasoning_parameters(profile.model,profile.default_output))
        minimal={'model':profile.model,'system':wire['system'],'messages':[{'role':'user','content':'.'}],**reasoning_parameters(profile.model,profile.default_output)}
        for phase,body in [('permanent',minimal),('whole_request',wire)]:
            requests.append({'package':label,'phase':phase,'model':profile.model,'request_sha256':sha(json.dumps(native_count_parameters(body),sort_keys=True,ensure_ascii=False).encode()),'prefix_sha256':sha(prefix.encode())})
        prepared.append((folder,profile,prefix,wire,minimal))
    if not a.count:
        write(out/'PREFLIGHT.json',{'endpoint':'https://api.anthropic.com/v1/messages/count_tokens','identity':snap.check(),'requests':requests,'generation':False})
        for folder,profile,prefix,wire,minimal in prepared:
            (folder/'prefix.md').write_bytes(prefix.encode())
        print('OFFLINE_PREFLIGHT_FOUR_COUNTS_READY');return
    expected=json.loads((out/'PREFLIGHT.json').read_bytes());assert expected['requests']==requests and expected['identity']==snap.check()
    import anthropic,httpx2
    from dotenv import dotenv_values
    endpoint=expected['endpoint']
    def only_count(request):
        if request.method!='POST' or str(request.url)!=endpoint:raise ValueError('Non-count destination refused')
    key=dotenv_values(Path(r'C:\IALD\projetos_pyhton\IALD')/'.env').get('IALD_CLAUDE_API_KEY');assert key
    client=anthropic.Anthropic(api_key=key,base_url='https://api.anthropic.com',max_retries=0,timeout=120,
        http_client=httpx2.Client(follow_redirects=False,timeout=120,event_hooks={'request':[only_count]}));del key
    try:
        for folder,profile,prefix,wire,minimal in prepared:
            values={}
            for phase,body in [('permanent',minimal),('whole_request',wire)]:
                intent=folder/(phase+'_intent.json');assert not intent.exists(),'Uncertain/completed count must not repeat'
                write(intent,next(r for r in requests if r['package']==folder.name and r['phase']==phase))
                value=count_native_request(client,body);values[phase]=value
                write(folder/(phase+'_result.json'),{'input_tokens':value,'intent_sha256':sha(intent.read_bytes())})
            budget=context_budget(profile.model,counted_model=profile.model,permanent_tokens=values['permanent'],request_input_tokens=values['whole_request'],reserved_output_tokens=profile.default_output,bounded_versioned=True)
            manifest={'schema':'iald.claude.memory.v1','model':profile.model,'prefix_file':'prefix.md','prefix_sha256':sha(prefix.encode()),
                'memory_policy':'BOUNDED_VERSIONED_RETRIEVAL','deployment':snap.check(),'budget':budget,
                'tools_sha256':native_tools_sha256(wire['tools'][:7]),'measurement_receipt':str(folder/'whole_request_result.json')}
            write(folder/'manifest.json',manifest)
            if not budget['ready']:raise ValueError('Native admission refused')
            print(json.dumps({'package':folder.name,'budget':budget}),flush=True)
    finally:client.close()
if __name__=='__main__':main()
