"""Single minimal official API probe; no secrets or conversation in receipt."""
from pathlib import Path
from datetime import datetime,timezone
import json
import sys
import time

W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(ROOT))
from iald_openai_credential import load
import requests


def main():
    intent=W/'NEW_CREDENTIAL_PROBE_INTENT.json'
    key=load()
    if not key:raise RuntimeError('Credential not enrolled or unavailable')
    request={'model':'gpt-5.6-luna','messages':[{'role':'user','content':'Reply only OK.'}],
             'max_completion_tokens':32,'stream':False}
    endpoint='https://api.openai.com/v1/chat/completions'
    started=datetime.now(timezone.utc).isoformat()
    with intent.open('x',encoding='utf8') as handle:
        json.dump({'at':started,'endpoint':endpoint,'payload':request,'attempts':1},handle,indent=2)
    result={'at':started,'endpoint':endpoint,'model':request['model'],'attempts':1,
            'private_data_sent':False,'scientific_context_sent':False,'key_exposed':False}
    clock=time.monotonic()
    try:
        response=requests.post(endpoint,headers={'Authorization':'Bearer '+key},json=request,timeout=60)
        result['http_status']=response.status_code
        result['request_id']=response.headers.get('x-request-id')
        try:body=response.json()
        except ValueError:body={}
        if response.status_code==200:
            result['status']='AUTHENTICATED'
            result['usage']=body.get('usage')
            result['model_returned']=body.get('model')
            choices=body.get('choices') or []
            result['answer_ok']=bool(choices and (choices[0].get('message',{}).get('content') or '').strip()=='OK')
        else:
            error=body.get('error',{}) if isinstance(body,dict) else {}
            result['status']='REFUSED'
            result['error_code']=error.get('code') if isinstance(error,dict) else None
            result['error_type']=error.get('type') if isinstance(error,dict) else None
    except requests.RequestException as exc:
        result['status']='TRANSPORT_UNCERTAIN'
        result['exception_type']=type(exc).__name__
    result['elapsed_seconds']=round(time.monotonic()-clock,3)
    with (W/'NEW_CREDENTIAL_PROBE.json').open('x',encoding='utf8') as handle:json.dump(result,handle,indent=2)
    print(json.dumps(result))


if __name__=='__main__':main()
