"""Prepare the finite R4 refinement and immutable cache chain; never invokes CAMB."""
from pathlib import Path
import ast,hashlib,json,itertools,difflib,sys
H=Path(__file__).resolve().parent;OLD=H.parent/'r2_refinement_r3'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def main():
    result=json.loads((OLD/'RESULT_R3.json').read_bytes())
    if result['exit_code']!=0 or result['total_physical_calls_across_R1_R3']!=729:raise RuntimeError('Incomplete R3')
    delivery=json.loads((OLD/'DELIVERY_REFINEMENT_R3.json').read_bytes())
    for pin in delivery['artifacts']:
        if sha(Path(pin['path']).read_bytes())!=pin['sha256']:raise RuntimeError('Changed R3 pin '+pin['path'])
    review=json.loads((OLD/'REVIEW_TERMINAL_R3.json').read_bytes())
    if review['status']!='PASS_WITH_SCOPE_NUMERICAL_INCONCLUSIVE':raise RuntimeError('Missing terminal review')
    for p in (OLD/'copies').iterdir():
        if p.is_file():put(H/'copies'/p.name,p.read_bytes())
    put(H/'cache_equivalence_r3_base.py',(OLD/'cache_equivalence_r3.py').read_bytes())
    sys.path.insert(0,str(H/'copies'));import theta_integrator as ti
    cfg=json.loads((OLD/'CONFIGURATION_R3.json').read_bytes());oldpoints={tuple(p['theta']):p for p in cfg['points']}
    points=[]
    for indices in itertools.product(range(17),repeat=3):
        theta=list(ti._theta(ti._node_key(indices,16)))
        points.append(oldpoints.get(tuple(theta),{'id':'r4_'+'_'.join(map(str,indices)),'theta':theta}))
    if len(points)!=4913 or sum(tuple(p['theta']) in oldpoints for p in points)!=729:raise RuntimeError('Nested grid mismatch')
    cfg['points']=points;cfg['resources'].update(points=4913,max_solver_calls=4184,wall_seconds=1800)
    cfg.update(request_id='f3-integration-full-prior-refinement-r4',point_selection='Nested dyadic levels3/4;729 exact prior nodes reused and4184 new nodes')
    put(H/'CONFIGURATION_R4.json',enc(cfg))
    recipe=json.loads((OLD/'RECIPE_R3.json').read_bytes());recipe.update(first_level=3,last_level=4,max_solver_calls=4184)
    put(H/'RECIPE_R4.json',enc(recipe))
    for name in ['CONFIGURATION_R3.json','CONSUMER_ADMISSION_R3.json','LOADED_BINDING_R3.json','THETA_RESULT_R3.json','RESULT_R3.json']:
        put(H/'original_context'/name,(OLD/name).read_bytes())
    for name in ['y_native.f64le','C_native.f64le','origin.f64le']:put(H/'frozen_inputs'/name,(OLD/name).read_bytes())
    cache=[]
    for source_root,dest_root in [(OLD/'nodes',H/'original_nodes'),(OLD/'original_nodes',H/'ancestry'/'nodes'),(OLD/'original_context',H/'ancestry'/'context')]:
        for source in sorted(source_root.rglob('*')):
            if source.is_file():
                b=source.read_bytes();dest=dest_root/source.relative_to(source_root);put(dest,b)
                cache.append({'source':str(source),'copy':dest.relative_to(H).as_posix(),'sha256':sha(b),'bytes':len(b)})
    put(H/'CACHE_CUSTODY_R4.json',enc({'completed_physical_calls':729,'direct_R3_receipts':604,'R3_bridges_to_direct_R2_receipts':125,'entries':cache,'source_delivery':str(OLD/'DELIVERY_REFINEMENT_R3.json'),'source_delivery_sha256':sha((OLD/'DELIVERY_REFINEMENT_R3.json').read_bytes()),'terminal_review_sha256':sha((OLD/'REVIEW_TERMINAL_R3.json').read_bytes())}))
    oldcode=(OLD/'run_refinement_r3a.py').read_text(encoding='utf-8')
    code=oldcode.replace('PLAN_R3A.json','PLAN_R4.json').replace('_R3','_R4').replace('cache_equivalence_r3 as ce','cache_equivalence_r4 as ce')
    for key in ['CONFIGURATION','CONSUMER_ADMISSION','LOADED_BINDING']:
        code=code.replace('original_context/'+key+'_R2.json','original_context/'+key+'_R3.json')
    code=code.replace('calls>=604','calls>=4184').replace('-start>600','-start>1800')
    code=code.replace("':nested-refinement-r3'","':nested-refinement-r4'")
    code=code.replace("'first_level':2,'last_level':3,'max_callback_calls':729","'first_level':3,'last_level':4,'max_callback_calls':4913")
    code=code.replace('calls==604 and len(cache)==729','calls==4184 and len(cache)==4913').replace("==729 and set(result['models'])","==4913 and set(result['models'])")
    code=code.replace('exactly729_accumulated','exactly4913_accumulated').replace('729_callbacks','4913_callbacks')
    code=code.replace("'reused_completed_calls':125,'total_physical_calls_across_R1_R4':calls+125","'reused_completed_calls':729,'total_physical_calls_accumulated':calls+729")
    assert "'reused_completed_calls':729" in code
    put(H/'run_refinement_r4.py',code.encode())
    launcher=(OLD/'launch_r3a.py').read_text(encoding='utf-8').replace('PLAN_R3A','PLAN_R4').replace('_R3','_R4').replace('run_refinement_r3a','run_refinement_r4').replace('launch_r3a','launch_r4').replace("'600s'","'1800s'")
    put(H/'launch_r4.py',launcher.encode())
    put(H/'EXECUTION_LIMITS_R4.txt',b'R4 single synthetic campaign: max4184 new CAMB calls +729 completed reused=4913 cumulative unique. One process and one thread. WSL timeout1800s with kill-after10s. Runner checks1800s before each new call; outer timeout enforces whole process. No individual-worker deadline; no automatic retry. No observed data. All criteria/data/priors preserved.\n')
    put(H/'DELTA_R4.diff',''.join(difflib.unified_diff(oldcode.splitlines(True),code.splitlines(True),fromfile='run_refinement_r3a.py',tofile='run_refinement_r4.py')).encode())
    for f in H.glob('*.py'):ast.parse(f.read_text(encoding='utf-8'))
    files=[p for p in H.rglob('*') if p.is_file()]
    plan={'schema':'F3_NESTED_PHYSICAL_REFINEMENT_R4','execution_pins':[{'path':p.relative_to(H).as_posix(),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in files],'first_level':3,'last_level':4,'reused_physical_calls':729,'max_new_CAMB_calls':4184,'max_accumulated_CAMB_calls':4913,'new_experiment':False,'observed_data':False,'unchanged':['data bytes','covariance','prior','five models','precision tolerances','.01 diagnostic threshold','physical code/runtime'],'cache_contract':'Full R2-direct -> R3-bridge -> R4 transport explicitly verified for125;604 R3 direct receipts verified; originals preserved','conditional_reuse':'All729 old conditional numerical results reused under exact context equality;125 ancestry bridges checked','no_automatic_retry':True,'wall_seconds':1800,'threads':1}
    put(H/'PLAN_R4.json',enc(plan));print(sha((H/'PLAN_R4.json').read_bytes()))
if __name__=='__main__':main()
