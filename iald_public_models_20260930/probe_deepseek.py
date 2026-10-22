"""A new controlled tool round-trip, not a replay of failed user requests."""
from pathlib import Path
import sys,json,datetime
W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'stage'),str(ROOT)]
import iald_app_providers as p
from claude_memory_package import load_package

def main():
    result=W/'deepseek_probe.json'
    if result.exists():raise RuntimeError('Probe already recorded; never repeat it.')
    started=W/'deepseek_probe_started.json'
    with started.open('x') as f:json.dump({'status':'started','at':datetime.datetime.now().isoformat()},f)
    p.MODELS['deepseek']['output']=1024
    p.MAX_ROUNDS=2
    pack=load_package(ROOT/'.iald_runtime/haiku')
    calls=[]
    def execute(name,args):
        calls.append(name)
        assert name=='get_current_datetime'
        return json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'controlled connectivity test'})
    ev=p.Evaluation(W/'probe_runtime')
    def bounded_post(url,**kw):
        import requests
        records=ev.report()['records']
        completed=[c for r in records for c in r['calls'] if c.get('status')=='completed']
        spent=sum(c['cost_estimate_usd'] for c in completed)
        upper=(len(json.dumps(kw['json'],ensure_ascii=False).encode())+4096)*0.30/1e6+1024*1.20/1e6
        if spent+upper>0.25:raise RuntimeError('Authorized cost ceiling reached before send')
        return requests.post(url,**kw)
    definitions=[{'type':'function','function':{'name':'get_current_datetime','description':'Return UTC date and time','parameters':{'type':'object','properties':{},'additionalProperties':False}}}]
    output=[]
    for row in ev.stream('deepseek',p.wire_messages([{'role':'user','content':'Teste técnico do conector: use get_current_datetime uma única vez para obter a hora atual e responda apenas com a hora retornada. Não consulte nenhuma outra fonte.'}],pack.prefix),definitions,execute,memory_sha256=pack.measurement.prefix_sha256,http_post=bounded_post):
        output.append(row)
    receipt={'records':ev.report()['records'],'tool_calls_executed':calls,'output_bytes':len(''.join(output).encode()),'generation_test':True}
    with result.open('x',encoding='utf-8')as f:json.dump(receipt,f,indent=2)
    print(json.dumps(receipt,ensure_ascii=False))
if __name__=='__main__':main()
