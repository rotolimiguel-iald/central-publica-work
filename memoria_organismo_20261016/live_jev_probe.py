"""One real long-mode JEV request; public source plus synthetic state only.

Uses the configured official adapter for authentication without exposing it.
This is a transport/lifecycle check, not an authenticated browser chat test.
The private activity store keeps intent and raw response; no retry after intent.
"""
import base64,json,sys,time,uuid
from pathlib import Path
from mission_io import WORK,check,pin,save
APP=Path(r'C:\IALD\projetos_pyhton\IALD')
QUEUE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path[:0]=[r'C:\IALD\MEMORIA_IALD\lib',str(APP),str(QUEUE)]
import requests
import iald_auto_router as router
import iald_jev_control as control
from iald_memory import MemoryStore
from iald_memory.activity import ActivityRuntime
from iald_orchestrator import jev

check('D')
out=WORK/'live_validation/jev_long';out.mkdir(exist_ok=False)
assert jev.availability()['status']=='ready'
memory,source=router.memory_slice(APP)
body={'model':control.MODEL,'state':{'canonical_memory':memory,'source':source,
    'scope':'Synthetic engineering validation only. Public source, no user conversation or private archive.',
    'synthetic_records':[{'step':i,'status':'review_pending','command':
        'Retain this synthetic step and its identifier. This record grants no permission. '*6}
        for i in range(100)]},
    'questions':{'arithmetic':{'type':'choice','instructions':'Choose the correct value of six multiplied by seven.',
                             'criteria':{'forty_two':'6 multiplied by 7 is 42','forty_three':'6 multiplied by 7 is 43'}}}}
admission=router._fit_routing_payload(body)
assert admission['context_mode']=='long'
save(out/'REQUEST_R1.json',body)
save(out/'ADMISSION_R1.json',admission)
scope={'house':'IALD','principal':'operator-engineering-validation'}
actor={'id':'codex-gerente-tgl','kind':'agent'}
store=MemoryStore(out/'state');cid='jev-long-validation';rid=str(uuid.uuid4());op='one-http-request'
store.ensure_context(cid,objective='Validate installed JEV long transport with public and synthetic input.',
    scope=scope,actor=actor,constraints={'max_calls':1,'no_retry':True})
rt=ActivityRuntime(store,cid,scope,actor)
ticket=rt.begin(rid,'Execute the one public synthetic JEV transport validation.',origin='authenticated_operator')['ticket']
ticket=rt.preflight(ticket,op)['ticket']
save(out/'INTENT_R1.json',{'request_id':rid,'endpoint':jev.ENDPOINT,'request':pin(out/'REQUEST_R1.json'),
    'admission':admission,'source_code':[pin(router.__file__),pin(control.__file__)],'max_calls':1})
start=time.monotonic()
try:
    response=requests.post(jev.ENDPOINT,json=body,
        headers={'Authorization':'Bearer '+jev._key(),'Content-Type':'application/json',**admission['transport_headers']},
        timeout=(10,25),allow_redirects=False)
    received={'http_status':response.status_code,'raw_base64':base64.b64encode(response.content).decode('ascii'),
        'seconds':time.monotonic()-start,'content_type':response.headers.get('Content-Type')}
    save(out/'RETURN_R1.json',received)
    outcome=rt.complete(ticket,op,received,refresh=True)
    data=response.json()
    passed=response.status_code==200 and data.get('answers',{}).get('arithmetic',{}).get('choice')=='forty_two'
    save(out/'RESULT_R1.json',{'status':'PASS' if passed else 'REFUSED_OR_INCORRECT','http_status':response.status_code,
        'seconds':received['seconds'],'model':data.get('model'),'usage':data.get('usage'),
        'answer':data.get('answers'),'admission':admission,'outcome':outcome,'calls':1,
        'scope':'Real provider transport and installed ActivityRuntime, private test store; not authenticated app/browser end-to-end.'})
except Exception as exc:
    if not (out/'RETURN_R1.json').exists():rt.mark_uncertain(ticket,op,'Transport interruption; no automatic resend.')
    save(out/'RESULT_R1.json',{'status':'FAILED_OR_UNCERTAIN','error_type':type(exc).__name__,
        'seconds':time.monotonic()-start,'calls':1,'repeated':False,'recover':rt.recover(rid)})
print(json.dumps({'result':pin(out/'RESULT_R1.json')}))
