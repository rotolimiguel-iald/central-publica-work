"""Two bounded public-context streaming calls, never retry an uncertain send."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime, timezone
import json, sys, time, hashlib
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'stage'),str(R),'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages']
import anthropic
from dotenv import dotenv_values
import iald_motor_claude as adapter
import iald_kernel,iald_fontes_publicas,iald_core_indexado
from claude_profiles import HAIKU
from claude_memory_package import load_package
from claude_context_snapshot import snapshot_from_manifest,CheckedAdapter
from claude_guarded_transport import post_guarded

def save(path,value):
    raw=json.dumps(value,ensure_ascii=False,indent=2).encode()
    temp=path.with_suffix('.tmp');temp.write_bytes(raw)
    assert temp.read_bytes()==raw;temp.replace(path)

def main():
    target=W/'validation/live_haiku55.json';target.parent.mkdir(exist_ok=True)
    if target.exists():raise RuntimeError('Receipt exists: never repeat uncertain calls')
    package=load_package(W/'package',canonical_manifest=R/'iald_nucleo_fixo.json')
    snap=snapshot_from_manifest(json.loads((W/'package/manifest.json').read_bytes()),package)
    definitions=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()
    checked=CheckedAdapter(adapter,snap,trusted_openai_tools=definitions)
    cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=4096,cache_ttl='5m',esforco_claude='medium')
    messages=[{'role':'system','content':package.prefix},{'role':'user','content':
        'Teste de integração autorizado. Primeiro consulte iald_kernel_list uma única vez, com limite 1, '
        'apenas para validar o acesso ao acervo. Depois da ferramenta, responda em até 250 palavras: '
        'quem é o autor da TGL, qual a versão efetivamente carregada, e articule a solução matemática '
        'documentada usando Hamiltoniano limitado inferiormente, equação mestra e dephasing. '
        'Preserve os estatutos e distinga solução matemática de confirmação externa. Não use outras ferramentas.'}]
    policy=dict(username='luiz',account_approved=True,haiku_ready=True,sonnet_ready=True)
    state=adapter.EstadoClaude()
    receipt=dict(status='PREPARED',model=HAIKU.model,prefix_sha256=package.measurement.prefix_sha256,
        private_atlas_sent=False,max_generation_calls=2,max_cost_usd=1.0,calls=[],utc=datetime.now(timezone.utc).isoformat())
    save(target,receipt)
    key=dotenv_values(R/'.env').get('IALD_CLAUDE_API_KEY')
    catalog=iald_kernel.KernelCatalog(Path(json.loads((R/'iald_nucleo_fixo.json').read_bytes())['active_cluster']['kernel_bundle']))
    with anthropic.Anthropic(api_key=key,max_retries=0,timeout=180) as client:
        for round_no in range(2):
            receipt['status']='SENDING_NO_AUTOMATIC_RETRY';receipt['attempt']=round_no+1;save(target,receipt)
            started=time.monotonic();calls={};chunks=[];events=0;usage={};errors=[]
            payload=dict(model=HAIKU.model,max_completion_tokens=4096,messages=messages,tools=definitions,stream=True)
            response,decision=post_guarded(checked,cfg,payload,requested_model=HAIKU.model,server_policy=policy,
                prefix=package.prefix,memory=package.measurement,state=state,timeout=180,client=client)
            if response.status_code!=200:
                receipt.update(status='REFUSED_OR_UNCERTAIN',http_status=response.status_code,error=response.json(),decision=decision)
                save(target,receipt);print(json.dumps({k:receipt[k] for k in ('status','http_status','error')},ensure_ascii=False));return
            try:
                for raw in response.iter_lines():
                    line=raw.decode() if isinstance(raw,bytes) else raw
                    if not line.startswith('data:') or line[5:].strip()=='[DONE]':continue
                    event=json.loads(line[5:]);events+=1
                    if 'error' in event:errors.append(event['error'])
                    if event.get('usage'):usage=event['usage']
                    for choice in event.get('choices',[]):
                        delta=choice.get('delta',{});chunks.append(delta.get('content',''))
                        for item in delta.get('tool_calls',[]):
                            obj=calls.setdefault(item['index'],{'id':'','type':'function','function':{'name':'','arguments':''}})
                            obj['id']=item.get('id') or obj['id']
                            for part in ('name','arguments'):
                                obj['function'][part]+=item.get('function',{}).get(part,'')
            finally:response.close()
            details=usage.get('prompt_tokens_details',{});prompt=usage.get('prompt_tokens',0)
            cached=details.get('cached_tokens',0);write=details.get('cache_write_tokens',0)
            estimated=((prompt-cached-write)*.5+cached*.05+write*.625+usage.get('completion_tokens',0)*2.5)/1e6
            row=dict(round=round_no+1,elapsed_seconds=round(time.monotonic()-started,3),events=events,
                usage=usage,estimated_usd=estimated,stop_reason=state.ultima_parada,text=''.join(chunks),
                tools=[x['function']['name'] for x in calls.values()],decision=decision,errors=errors)
            receipt['calls'].append(row);receipt['status']='ROUND_COMPLETE';save(target,receipt)
            if errors or state.ultima_parada not in ('tool_use','end_turn'):break
            if not calls:break
            if round_no:break
            values=list(calls.values())
            blocks=state.blocos_para([x['id'] for x in values])
            receipt['thinking_preserved']=bool(blocks and any(b.get('type') in ('thinking','redacted_thinking') for b in blocks))
            messages.append({'role':'assistant','content':row['text'],'tool_calls':values})
            for call in values:
                name=call['function']['name'];args=json.loads(call['function']['arguments'])
                if name!='iald_kernel_list' or state.entrada_invalida(call['id']):raise ValueError('Unexpected tool: no execution')
                args['limit']=1
                result=iald_kernel.execute_tool(catalog,name,args)
                messages.append({'role':'tool','tool_call_id':call['id'],'content':json.dumps(result,ensure_ascii=False)})
    receipt['total_estimated_usd']=sum(x['estimated_usd'] for x in receipt['calls'])
    receipt['status']='PASS' if len(receipt['calls'])==2 and receipt['calls'][-1]['stop_reason']=='end_turn' and receipt['calls'][0]['tools']==['iald_kernel_list'] else 'INCOMPLETE'
    save(target,receipt)
    print(json.dumps({k:receipt.get(k) for k in ('status','total_estimated_usd','thinking_preserved')},ensure_ascii=False))
    print(receipt['calls'][-1]['text'])

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'status':'FAILED_DO_NOT_RETRY','error_type':type(exc).__name__}))
        raise SystemExit(1)
