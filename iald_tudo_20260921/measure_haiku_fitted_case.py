"""Independent free native-count verification of the proposed tool-only fit."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import measure_haiku_retrieval_case as case

STAGE=case.WORK/'haiku_window_diagnostic_20260923_085246_281422'
spec=importlib.util.spec_from_file_location('reviewed_tool_budget',STAGE/'claude_tool_budget.py')
fitter=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fitter)

def main():
    cfg,package,snapshot,base,payload=case.build()
    source=json.loads((case.ROOT/'iald_nucleo_fixo.json').read_bytes())['active_cluster']
    catalog=case.iald_kernel.KernelCatalog(source['kernel_bundle'],source.get('kernel_verification'))
    for i,path in enumerate(['TGLExt/TheMasterFires.lean','TGLExt/ConcreteFourFrame.lean','TGLExt/V354RegularSusy.lean'],start=2):
        args={'path':path,'max_lines':80}
        payload['messages'][2]['tool_calls'].append({'id':f'case_{i}','type':'function',
            'function':{'name':'iald_kernel_read','arguments':json.dumps(args)}})
        payload['messages'].append({'role':'tool','tool_call_id':f'case_{i}',
            'content':json.dumps(catalog.read_file(**args),ensure_ascii=False)})
    before=json.dumps(payload,sort_keys=True,ensure_ascii=False)
    key=case.dotenv_values(case.ROOT/'.env').get('IALD_CLAUDE_API_KEY')
    if not key:raise ValueError('Credential absent')
    cache={}
    with case.anthropic.Anthropic(api_key=key,max_retries=0,timeout=90) as client:
        def count(candidate):
            token=hashlib.sha256(json.dumps(candidate,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            if token not in cache:
                if len(cache)>=6:raise ValueError('Count probe cap exceeded')
                cache[token]=case.count_payload(client,cfg,package,snapshot,candidate)
            return cache[token]
        initial=count(payload)
        fitted=fitter.fit_latest_tool_results(payload,count,200000)
        final=count(fitted)
    assert before==json.dumps(payload,sort_keys=True,ensure_ascii=False)
    assert fitted['messages'][:3]==payload['messages'][:3]
    assert fitted['tools']==payload['tools']
    assert fitted['tool_choice']=='none'
    assert final+4096+1024<=200000
    assert initial+4096+1024>200000
    result={'at':datetime.now(timezone.utc).isoformat(),'before':initial,'after':final,
            'permanent':package.measurement.permanent_tokens,'remaining':200000-final-4096-1024,
            'count_requests':len(cache),'generation_requests':0,
            'prefix_history_question_tool_calls_and_schemas_unchanged':True,
            'original_payload_unchanged':True,'final_tool_choice':'none',
            'helper_sha256':hashlib.sha256((STAGE/'claude_tool_budget.py').read_bytes()).hexdigest(),
            'scope':'Representative overloaded batch using five actual public retrieval results and the real fixed memory. Not an exact captured user request or a generated answer.'}
    target=case.WORK/'haiku_fitted_case_measurement.json'
    with target.open('xb') as f:f.write(json.dumps(result,ensure_ascii=False,indent=2).encode('utf8'))
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'status':'FAILED','type':type(exc).__name__}))
        raise SystemExit(1)
