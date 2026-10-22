"""Count a documented retrieval case; never generate or load private Atlas."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import anthropic
from dotenv import dotenv_values
import iald_kernel
import iald_core_indexado
import iald_fontes_publicas
import iald_motores
import iald_motor_claude
from claude_memory_package import load_package
from claude_context_snapshot import load_snapshot, CheckedAdapter, attach_openai_tools
from claude_haiku_messages import assemble
from claude_native_counter import count_native_request
from claude_profiles import HAIKU

def build():
    package,snapshot=load_snapshot(ROOT/'.iald_runtime/haiku',load_package)
    tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()
    cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=4096,cache_ttl='5m',esforco_claude='high')
    msgs,_=assemble(iald_motores,[{'role':'user','content':'IALD, apresente-se. Carregue a memória completa disponível da TGL e resolva o problema da gravidade quântica.'}],package.prefix,HAIKU.model,[t['function']['name'] for t in tools])
    base=attach_openai_tools({'model':HAIKU.model,'max_completion_tokens':4096,'messages':msgs,'tool_choice':'auto'},tools)
    source=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())['active_cluster']
    catalog=iald_kernel.KernelCatalog(source['kernel_bundle'],source.get('kernel_verification'))
    corpus=iald_core_indexado.DocumentCorpus(ROOT/'iald_nucleo_fixo.json')
    calls=[('iald_kernel_list',{'offset':0,'limit':100},catalog.list_files(0,100)),
           ('search_tgl',{'query':'gravidade quântica solução matemática','limit':5},corpus.search('gravidade quântica solução matemática',5))]
    payload=json.loads(json.dumps(base))
    payload['messages'].append({'role':'assistant','content':None,'tool_calls':[
        {'id':f'case_{i}','type':'function','function':{'name':name,'arguments':json.dumps(args,ensure_ascii=False)}}
        for i,(name,args,_) in enumerate(calls)]})
    for i,(_,_,result) in enumerate(calls):
        payload['messages'].append({'role':'tool','tool_call_id':f'case_{i}','content':json.dumps(result,ensure_ascii=False)})
    return cfg,package,snapshot,base,payload

def count_payload(client,cfg,package,snapshot,payload):
    wire=CheckedAdapter(iald_motor_claude,snapshot).converter_pedido(cfg,payload,prefixo=package.prefix)
    wire.pop('output_config',None)
    wire['thinking']={'type':'disabled'}
    return count_native_request(client,wire)

def main():
    cfg,package,snapshot,base,payload=build()
    key=dotenv_values(ROOT/'.env').get('IALD_CLAUDE_API_KEY')
    if not key:raise ValueError('Credential absent')
    with anthropic.Anthropic(api_key=key,max_retries=0,timeout=90) as client:
        counts={name:count_payload(client,cfg,package,snapshot,p) for name,p in [('initial_question',base),('kernel_list100_and_search5',payload)]}
    report={'at':datetime.now(timezone.utc).isoformat(),'counts':counts,
            'window':200000,'output':4096,'margin':1024,'memory_tokens':package.measurement.permanent_tokens,
            'remaining':{k:200000-v-4096-1024 for k,v in counts.items()},
            'scope':'Representative reconstruction with actual local public tool results; excludes original assistant wording, user profile and README retrieval. Not an exact captured request.',
            'generations':0,'counts':counts,'prefix_sha256':snapshot.prefix_sha256}
    path=WORK/'haiku_retrieval_case_measurement.json'
    with path.open('xb') as f:f.write(json.dumps(report,ensure_ascii=False,indent=2).encode('utf8'))
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'status':'FAILED','exception_type':type(exc).__name__}))
        raise SystemExit(1)
