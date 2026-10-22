"""One controlled local calculation, through the installed operator bridge.
No LLM/provider inference, no RAM load/release, no canonical source modification.
"""
from contextlib import closing
from datetime import datetime,timezone
from pathlib import Path
import ast,hashlib,http.client,json,math,sqlite3,sys,time

W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(R))
import iald_operator_bench as bench
from iald_task_artifacts import ArtifactStore
import iald_auto_router as router
import iald_motores as motores
from deploy import snapshot,atomic

def authorize(provider='task'):
    record=json.loads((R/'iald_users.json').read_bytes()).get('luiz',{})
    if not router.allowed(record,'luiz') or not motores.consentiu(record,router.AUTO):raise PermissionError('Missing existing automatic authorization')
    return record

def run_count():
    p=bench.BENCH/'state/runs.sqlite3'
    with closing(sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)) as db:
        return db.execute('SELECT COUNT(*) FROM runs').fetchone()[0]

def main():
    assert not (W/'live_validation.json').exists(),'Read previous evidence; do not replay a successful validation'
    before=snapshot();prepared=json.loads((W/'prepared.json').read_bytes())
    assert before==prepared['bench_before'],'Resident bench changed; investigate instead of reloading'
    users=json.loads((R/'iald_users.json').read_bytes())
    assert [u for u,r in users.items() if bench.is_operator(r,u)]==['luiz']
    store=ArtifactStore(R);api=bench.OperatorBench(R,'luiz',authorize,store)
    cap=api.execute('bench_capabilities',{});assert len(cap['operations'])==34
    n=run_count()
    plan=api.execute('bench_plan',{'operation':'dephasing','parameters':{'omega_rad_s':2,'tau_s':0.5,'duration_s':3},
        'objective':'Verificar a integração local da bancada ao chat, com cálculo controlado e inscrição antes do despacho.',
        'hypothesis':'Gamma=beta*tau*omega^2/2 e coerência=exp(-Gamma*t), usando alpha de entrada do motor existente.',
        'falsifier':'Divergência numérica maior que 1e-12, mais de uma execução nativa ou alteração da carga residente.'})
    assert plan.get('status') in ('PLANNED','REUSED'),plan.get('status')
    identifier=plan['route_id'];atomic(W/'live_route.json',json.dumps({'route_id':identifier,'native_runs_before':n},indent=2).encode())
    started=api.execute('bench_run',{'route_id':identifier})
    result=api.execute('bench_result',{'route_id':identifier,'wait_seconds':20})
    assert result['status']=='COMPLETED',result['status']
    data=json.loads(result['text']);values=data['result']['values']
    source=ast.parse((bench.BENCH/'app.py').read_bytes())
    alpha=next(ast.literal_eval(node.value) for node in source.body if isinstance(node,ast.Assign)
               and any(isinstance(target,ast.Name) and target.id=='ALPHA_FINE_CODATA_2018' for target in node.targets))
    expected=alpha*math.sqrt(math.e)*.5*2*2/2
    assert abs(values['gamma_per_s']-expected)<1e-12
    assert abs(values['coherence_fraction']-math.exp(-expected*3))<1e-12
    count_after=run_count();assert count_after==n+(plan['status']=='PLANNED')
    repeated=api.execute('bench_run',{'route_id':identifier});assert repeated['status']=='COMPLETED' and run_count()==count_after
    artifact=result['artifact'];path,meta=store.resolve('luiz',artifact['id'])
    assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256']
    denied=False
    try:store.resolve('taveiraneto',artifact['id'])
    except (ValueError,PermissionError):denied=True
    assert denied,'Owner isolation failed'
    historical=api.execute('bench_map',{});assert historical['counts']['routes']>=1
    after=snapshot();assert after==before,'Resident data changed during numerical validation'
    c=http.client.HTTPConnection('127.0.0.1',8082,timeout=10)
    try:
        c.request('GET','/api/task-capabilities');response=c.getresponse();response.read();assert response.status in (401,403)
    finally:c.close()
    evidence={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','route_id':identifier,
        'installed_tools':len(bench.NAMES),'catalog_operations':len(cap['operations']),
        'operator_accounts':['luiz'],'other_accounts_cannot_use_bench':True,'artifact_owner_isolation':denied,
        'native_runs_before':n,'native_runs_after':count_after,'duplicate_run_reused':True,
        'gamma_per_s':values['gamma_per_s'],'coherence_fraction':values['coherence_fraction'],
        'math_tolerance':1e-12,'scope':'CONTROLLED_NUMERICAL_INTEGRATION_TEST_NOT_NATURE_TEST',
        'map_counts':historical['counts'],'map_history':historical['history'],
        'artifact':artifact,'resident_state_unchanged':True,'bench_before':before,'bench_after':after,
        'web_unauthenticated_capabilities_denied':True,'paid_calls':0,'new_ram_loads':0}
    atomic(W/'live_validation.json',json.dumps(evidence,ensure_ascii=False,indent=2).encode())
    print(json.dumps({k:evidence[k] for k in ('status','route_id','operator_accounts','catalog_operations','native_runs_before','native_runs_after','duplicate_run_reused','map_counts','resident_state_unchanged','paid_calls')}))

if __name__=='__main__':main()
