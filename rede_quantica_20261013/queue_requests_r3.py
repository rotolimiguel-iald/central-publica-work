"""Preview/submit exactly the persisted R3 requests through the official client."""
import datetime as dt
import json
import subprocess
import sys
import time
from diary_r1 import ROOT, OUT, PY, claim, new, pin

DEST=OUT/'orchestration_r3'
BASE=ROOT/'Chatgpt/IALD_ORQUESTRACAO_20260923'

def main():
    mode,provider=sys.argv[1:3]
    revision=sys.argv[3] if len(sys.argv)>3 else 'R3'
    assert revision in ('R3','R3_1')
    assert mode in ('preview','submit') and provider in ('mimo','deepseek')
    claim()
    path=DEST/f'REQUEST_{provider.upper()}_{revision}.json'
    payload=json.loads(path.read_text(encoding='utf-8'))
    if mode=='preview':payload['operation']='preview_execution'
    else:
        preview=json.loads((DEST/f'PREVIEW_{provider.upper()}_{revision}.json').read_text(encoding='utf-8'))['response']
        assert preview.get('selected') == provider, 'Provider selection must be explicit'
        assert (DEST/f'SCOPE_REVIEW_{revision}.json').exists()
        assert json.loads((DEST/f'SCOPE_REVIEW_{revision}.json').read_text(encoding='utf-8'))['verdict']=='PASS_SCOPE'
    stem=f'{mode.upper()}_{provider.upper()}_{revision}'
    intent=DEST/(stem+'_INTENT.json'); receipt=DEST/(stem+'.json')
    if intent.exists() or receipt.exists(): raise FileExistsError('Inspect existing attempt; no blind retry')
    new(intent,{'payload':pin(path),'operation':payload['operation'],'request_id':payload['request_id'],'created_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    start=dt.datetime.now(dt.timezone.utc); clock=time.perf_counter()
    cp=subprocess.run([PY,'-B','-X','utf8',str(BASE/'transport_cli.py')],input=json.dumps(payload,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
    try:response=json.loads(cp.stdout)
    except json.JSONDecodeError:response=None
    result={'request_id':payload['request_id'],'operation':payload['operation'],'start_utc':start.isoformat(),'end_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'seconds':time.perf_counter()-clock,'exit_code':cp.returncode,'response':response,'stderr':cp.stderr}
    if response is None:result['unparsed_stdout']=cp.stdout
    new(receipt,result)
    if cp.returncode:raise RuntimeError({'receipt':str(receipt),'stderr':cp.stderr[-1500:]})
    print(json.dumps({'receipt':pin(receipt),'response_keys':list(response) if isinstance(response,dict) else None,'selected':response.get('selected') if isinstance(response,dict) else None,'job_id':response.get('id',response.get('job_id')) if isinstance(response,dict) else None,'stage':response.get('stage') if isinstance(response,dict) else None},ensure_ascii=False))

if __name__=='__main__':main()
