"""Two explicit, budgeted public-memory probes after the operator saved a new key."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,uuid,time
import requests
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(R))
import iald_auto_router as router
backend=router.backend()
from iald_orchestrator.safe_files import save_json
from iald_orchestrator.jev_secret_store import key_metadata
BUDGET=0.01
RATE=.042/1000000

def main():
    marker=W/'jev_rotated_key_probe_started.json'
    current=backend._activation()
    assert current.get('probe_status')=='configured_not_tested','Inspect existing probe; never replay'
    key_stamp=key_metadata()['mtime_ns']
    context,source=router.memory_slice(R)
    assert len(context)<=9000
    prompt='Audite uma demonstração matemática com hipóteses e passos formais explícitos.'
    body={'model':'jev-1.13.0','state':{'task':prompt,'canonical_memory':context,'source':source},
        'questions':{'complexity':{'type':'choice','instructions':'Classify task complexity only. Do not perform the task.',
        'criteria':{'standard':'Direct answer without formal audit','deep':'Multiple-step mathematical audit'}}}}
    raw=json.dumps(body,ensure_ascii=False).encode()
    assert len(raw)<28000
    # Reserve both complete UTF-8 bounds up front. The second router enforces 28k.
    upper=(len(raw)+28000)*RATE
    assert upper<=BUDGET
    with marker.open('x',encoding='utf-8') as out:
        json.dump({'key_mtime_ns':key_stamp,'budget_usd':BUDGET,'two_call_upper_estimate_usd':upper,'payload_sha256':hashlib.sha256(raw).hexdigest()},out)
    record={'enabled':False,'probe_status':'dispatching','probe_id':uuid.uuid4().hex,
        'started_at':datetime.now(timezone.utc).isoformat(),'scope':'STRUCTURED_ROUTING_ONLY',
        'payload_sha256':hashlib.sha256(raw).hexdigest(),'source':source,'provider_calls':1}
    assert backend._activation()==current
    save_json(backend.ACTIVATION,record)
    headers={'Authorization':'Bearer '+backend._key(),'Content-Type':'application/json'}
    started=time.monotonic()
    try:
        try:
            response=requests.post(backend.ENDPOINT,json=body,headers=headers,allow_redirects=False,timeout=(10,25))
        finally:headers.clear()
        try:
            record['http_status']=response.status_code
            if response.status_code!=200:raise ValueError('Connection refused')
            data=response.json()
        finally:response.close()
        assert data.get('model')=='jev-1.13.0'
        classification=backend.parse_answer(data,prompt)
        assert classification['complexity']=='deep'
        assert key_metadata()['mtime_ns']==key_stamp,'Credential changed during test'
        record.update(enabled=True,probe_status='ready',model=data['model'],usage=data.get('usage'),
            validated_at=datetime.now(timezone.utc).isoformat(),choice=classification['complexity'])
    except Exception as exc:
        record.update(enabled=False,probe_status='rejected' if record.get('http_status') not in (None,200) else 'uncertain',error_type=type(exc).__name__)
        raise
    finally:
        record['elapsed_seconds']=round(time.monotonic()-started,3)
        save_json(backend.ACTIVATION,record)
        save_json(W/'jev_rotated_key_connection.json',record)
    # This is a distinct typed-selector test, not a retry of the connection probe.
    selected,receipt=router.choose('Desenvolva a lagrangiana e a equação mestra da TGL com as hipóteses e as fontes. Prefiro uma resposta detalhada com ferramentas de consulta.',
        ['openai','mimo','kimi','claude-haiku','claude-sonnet'],root=R,validation_probe=True)
    save_json(W/'jev_rotated_key_selector.json',{'selected':selected,'receipt':receipt,'generation_calls':0})
    assert router.available()
    print(json.dumps({'authentication':'verified','connection':'ready','selected':selected,
        'router_available':True,'connection_usage':record.get('usage'),'selector_input_tokens':receipt.get('input_tokens'),
        'budget_usd':BUDGET,'two_call_upper_estimate_usd':upper,'generation_calls':0},ensure_ascii=False))

if __name__=='__main__':main()
