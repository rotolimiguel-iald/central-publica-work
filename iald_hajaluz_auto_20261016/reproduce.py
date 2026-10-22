"""Read-only live source + operator scope; provider, wallet and memory writes stubbed."""
from pathlib import Path
import json,sys,hashlib,types,traceback
from unittest.mock import patch
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
staged='--staged' in sys.argv
sys.path[:0]=([str(W/'staging')] if staged else [])+[str(R)]
import iald_auto_router as router
import iald_app_memory as am
u=json.loads((R/'iald_users.json').read_bytes())['luiz'];owner=hashlib.sha256(('iald-account:luiz:'+str(u.get('created','legacy'))).encode()).hexdigest();del u
rows=json.loads((W/'diagnostic_memory.json').read_bytes())['matched']
load=router.jev_control.load_contract;memory=router.memory_slice
out=[]
for row in rows:
    binding=am.Binding(am.MemoryStore(am._SHARED_ROOT),row['context_id'],{'house':'IALD_APP','principal':owner},'offline-diagnostic','haja luz')
    details={'context_id':row['context_id'],'provider_calls':0}
    def post(*args,**kw):
        details['provider_calls']+=1;body=kw['json'];ans={}
        for key,q in body['questions'].items():
            choices=q['criteria'];v={'executor':'mimo','scientific_mode':'explanation','work_path':'answer','memory_action':'use_loaded','collaboration':'direct','memory_continuity':'continue'}[key]
            ans[key]={'type':'choice','choice':v,'confidence':.95,'probabilities':{k:float(k==v) for k in choices}}
        return types.SimpleNamespace(status_code=200,json=lambda:{'model':'jev-1.13.0','answers':ans,'usage':{'input_tokens':100}})
    check=router.jev_control.check_payload
    def measured(body):
        size=lambda x:len(json.dumps(x,ensure_ascii=True,allow_nan=False).encode('ascii'))
        details['state_sizes']={k:size(v) for k,v in body['state'].items()}
        details['state_bytes']=size(body['state']); details['request_bytes']=size(body)
        return check(body)
    backend=types.SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda x:x,ENDPOINT='offline://jev',_key=lambda:'fixture')
    with am.bound(binding), patch.object(router,'backend',return_value=backend), patch.object(router,'observations',return_value={}), patch.object(router.jev_control,'load_contract',side_effect=lambda root:load(R)), patch.object(router,'memory_slice',side_effect=lambda root:memory(R)), patch.object(router.jev_control,'check_payload',side_effect=measured), patch.object(am,'routing_result'), patch.object(router.wallet_runtime,'enabled',return_value=False),patch.object(router.wallet_runtime,'routing_begin'),patch.object(router.wallet_runtime,'routing_end'):
        try:
            selected,receipt=router.choose('haja luz',['mimo','openai','kimi'],root=W/'fixture',post=post,validation_probe=True)
            details.update(status='selected',selected=selected)
        except Exception as exc:details.update(status='refused',error_type=type(exc).__name__,error=str(exc),frames=[f'{x.name}:{x.lineno}' for x in traceback.extract_tb(exc.__traceback__)])
    out.append(details)
blob=json.dumps({'results':out,'network_calls':0,'source_files_unchanged':True},ensure_ascii=False,indent=2).encode()
with (W/('reproduction_fixed.json' if staged else 'reproduction.json')).open('xb') as f:f.write(blob)
print(blob.decode())
