"""One bounded public-science decision test; no executor/tool dispatch."""
from pathlib import Path
from datetime import datetime,timezone
import json
import sys

W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'app_patch'),str(R),str(W),'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages']
from transaction import write_evidence
import iald_auto_router as router
import requests

CASES=[
 ('mathematics','Articule a solução matemática do problema da gravidade quântica na TGL, distinguindo a demonstração formal da confirmação experimental.',False,{'answer','retrieve'}),
 ('website','Crie uma página HTML de apresentação da TGL para baixar como arquivo.',False,{'create_artifact'}),
 ('bench','Na bancada da IALD, calcule o dephasing. Antes, consulte o mapa de pesquisa para reutilizar a mesma rota se já existir. Quero os resultados em JSON.',True,{'operator_bench'}),
 ('calculation','Calcule em Python 6 vezes 7 e entregue o código e o JSON do resultado.',False,{'execute_calculation'}),
]

def main():
    path=W/'live_jev_probe.json'
    if path.exists():raise RuntimeError('Probe already inscribed: inspect its result, do not repeat')
    record={'status':'STARTED','scope':'PUBLIC_SCIENTIFIC_CONTEXT_V380_ONLY','started_at':datetime.now(timezone.utc).isoformat(),
            'budget_usd':.01,'cases':[],'executor_calls':0,'bench_operations':0,'anthropic_calls':0}
    write_evidence(path,record)
    reserved=0.;actual=0.
    def post(url,**kwargs):
        nonlocal reserved
        if url!='https://api.typesafe.ai/v1/systemone':raise ValueError('Unexpected provider destination')
        raw=json.dumps(kwargs['json'],ensure_ascii=True,allow_nan=False).encode()
        # Each byte as an input token is conservative for this textual test.
        ceiling=len(raw)*.042/1000000
        if reserved+ceiling>.01:raise ValueError('Test budget exhausted before dispatch')
        reserved+=ceiling
        return requests.post(url,**kwargs)
    try:
        for label,prompt,operator,expected in CASES:
            item={'case':label,'status':'STARTED','expected_paths':sorted(expected)}
            record['cases'].append(item);write_evidence(path,record)
            context={'role':'operador','capabilities':['local_scientific_bench','resident_RAM','durable_research_map'],
                     'protocol':'bench_capabilities, bench_map, bench_plan then bench_run; duplicate route is reused.'} if operator else None
            selected,receipt=router.choose(prompt,['mimo','openai','deepseek'],root=W,post=post,
                                           validation_probe=True,operator_context=context)
            actual+=receipt['estimated_cost_usd']
            item.update(status='RETURNED',selected=selected,routing_id=receipt['id'],control=receipt['control'],
                        input_tokens=receipt['usage']['input_tokens'],cost_usd=receipt['estimated_cost_usd'],
                        elapsed_s=receipt['elapsed_s'],path_matches=receipt['control']['work_path'] in expected)
            if label=='mathematics':
                item['mode_matches']=receipt['control']['scientific_mode']=='mathematical_solution'
            write_evidence(path,record)
        record['status']='PASS' if all(c.get('path_matches') and c.get('mode_matches',True) for c in record['cases']) else 'BEHAVIOR_REVIEW_REQUIRED'
    except Exception as exc:
        record.update(status='FAILED_OR_UNCERTAIN_NO_RETRY',error_type=type(exc).__name__)
        raise
    finally:
        record.update(finished_at=datetime.now(timezone.utc).isoformat(),estimated_actual_usd=actual,reserved_upper_usd=reserved)
        write_evidence(path,record)
    print(json.dumps({'status':record['status'],'cases':[{k:c.get(k) for k in ('case','status','path_matches','mode_matches','input_tokens','cost_usd')} for c in record['cases']],
                      'estimated_actual_usd':actual,'executor_calls':0,'bench_operations':0}))

if __name__=='__main__':main()
