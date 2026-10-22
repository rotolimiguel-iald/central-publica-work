"""Synthetic Flask test-client bridge over local stdio; no listening socket."""
import sys
sys.dont_write_bytecode=True
import base64,json
from pathlib import Path
from flask import Response,request
from test_backend import Routes
case=Routes();case.setUp();case.generation['alice']='a'*64
def produce():
    case.calls.append(request.get_json())
    events=[{'choices':[{'delta':{'content':'resposta íntegra 😀 '*20000}}]},
            {'choices':[{'delta':{'content':'fim 🧪'}}]}]
    return Response(''.join('data: '+json.dumps(v,ensure_ascii=False)+'\n\n' for v in events)+'data: [DONE]\n\n',content_type='text/event-stream')
case.app.view_functions['produce']=produce
records=[]
try:
    for line in sys.stdin:
        req=json.loads(line)
        response=case.client.open(req['path'],method=req.get('method','GET'),
            data=base64.b64decode(req['body']),headers={**req.get('headers',{}),'Origin':'https://demo.iald.ia.br'})
        if req.get('method')=='POST':case.join_all()
        records.append(dict(path=req['path'],status=response.status_code,bytes=len(response.data),envelope=isinstance(response.json,dict) and 'iald_transport' in response.json))
        print(json.dumps(dict(status=response.status_code,headers=dict(response.headers),body=base64.b64encode(response.data).decode())),flush=True)
finally:
    case.join_all()
    (Path(__file__).parent/'RPC_RECEIPT.json').write_text(json.dumps(dict(provider_calls=0,synthetic_producer_calls=len(case.calls),network_connections=0,requests=records),ensure_ascii=False,indent=2),encoding='utf-8')
    case.doCleanups()
