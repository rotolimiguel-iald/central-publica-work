"""Prepare an additive nested refinement; no solver and no observations."""
from pathlib import Path
import ast,hashlib,json,itertools,difflib,sys
H=Path(__file__).resolve().parent;OLD=H.parent/'r2_full_integration/recovery_r2'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def main():
    result=json.loads((OLD/'RESULT_R2.json').read_bytes())
    if result['exit_code']!=0 or result['total_physical_calls_across_R1_R2']!=125:raise RuntimeError('Old result incomplete')
    for x in json.loads((OLD/'PLAN_R2.json').read_bytes())['execution_pins']:
        if sha((OLD/x['path']).read_bytes())!=x['sha256']:raise RuntimeError('Old pin changed')
    for p in (OLD/'copies').iterdir():
        if p.is_file():put(H/'copies'/p.name,p.read_bytes())
    sys.path.insert(0,str(H/'copies'));import theta_integrator as ti
    cfg=json.loads((OLD/'CONFIGURATION_R2.json').read_bytes());oldpoints={tuple(p['theta']):p for p in cfg['points']}
    points=[]
    for indices in itertools.product(range(9),repeat=3):
        theta=list(ti._theta(ti._node_key(indices,8)))
        points.append(oldpoints.get(tuple(theta),{'id':'r3_'+'_'.join(map(str,indices)),'theta':theta}))
    cfg['points']=points;cfg['resources'].update(points=729,max_solver_calls=604)
    cfg.update(request_id='f3-integration-full-prior-refinement-r3',point_selection='Nested dyadic levels2/3;125 exact prior nodes reused and604 new nodes')
    put(H/'CONFIGURATION_R3.json',enc(cfg))
    recipe=json.loads((OLD/'RECIPE_R2.json').read_bytes());recipe.update(first_level=2,last_level=3,max_solver_calls=604)
    put(H/'RECIPE_R3.json',enc(recipe))
    for name in ['CONFIGURATION_R2.json','CONSUMER_ADMISSION_R2.json','LOADED_BINDING_R2.json','THETA_RESULT_R2.json','RESULT_R2.json']:
        put(H/'original_context'/name,(OLD/name).read_bytes())
    for name in ['y_native.f64le','C_native.f64le','origin.f64le']:put(H/'frozen_inputs'/name,(OLD/name).read_bytes())
    cache=[]
    for directory in sorted((OLD/'nodes').iterdir()):
        for name in ['claim.json','result.json','receipt.json','packet.json','assembly.json','precision.json','conditional.json']:
            source=directory/name;dest=H/'original_nodes'/directory.name/name;b=source.read_bytes();put(dest,b)
            cache.append({'source':str(source),'copy':dest.relative_to(H).as_posix(),'sha256':sha(b),'bytes':len(b)})
    put(H/'CACHE_CUSTODY_R3.json',enc({'completed_physical_calls':125,'entries':cache,'source_delivery':str(OLD.parent/'DELIVERY_FULL_R2.json'),'source_delivery_sha256':sha((OLD.parent/'DELIVERY_FULL_R2.json').read_bytes()),'terminal_review_sha256':sha((OLD.parent/'REVIEW_TERMINAL_R2.json').read_bytes())}))
    oldcode=(OLD/'run_full_prior_r2.py').read_text();code=oldcode.replace('_R2','_R3')
    code=code.replace('import linear_gaussian as lg','import linear_gaussian as lg\n        import cache_equivalence_r3 as ce')
    first=code.index('        cache={}');last=code.index('        def background(point):',first)
    init='''        cache={}; old_nodes={}
        custody=json.loads((H/'CACHE_CUSTODY_R3.json').read_bytes())
        for item in custody['entries']:
            if sha((H/item['copy']).read_bytes())!=item['sha256']:raise RuntimeError('Original cache bytes changed')
        old_config_raw=(H/'original_context/CONFIGURATION_R2.json').read_bytes();old_config=json.loads(old_config_raw)
        old_admission=json.loads((H/'original_context/CONSUMER_ADMISSION_R2.json').read_bytes())
        old_loaded=json.loads((H/'original_context/LOADED_BINDING_R2.json').read_bytes())
        for directory in sorted((H/'original_nodes').iterdir()):
            point=next(x for x in cfg['points'] if x['id']==directory.name)
            original_packet=(directory/'packet.json').read_bytes()
            record,bridge=ce.rebind_background(original_packet,(directory/'receipt.json').read_bytes(),(directory/'result.json').read_bytes(),old_config,cfg,point,engine_sha256=sha((H/'copies/background_controls.py').read_bytes()),runtime_sha256=sha(runtime_raw),old_configuration_sha256=sha(old_config_raw))
            bridge.update(original_configuration_sha256=sha(old_config_raw),new_configuration_sha256=sha(config_raw))
            bridge_raw=put('nodes/'+point['id']+'/receipt.json',bridge)
            record['identity']['engine_configuration_sha256']=sha(config_raw)
            record['identity']['execution_receipt_sha256']=sha(bridge_raw)
            packet=put('nodes/'+point['id']+'/packet.json',record)
            put('nodes/'+point['id']+'/result.json',record['result'])
            cache[tuple(point['theta'])]=(packet,{'id':point['id']+':equivalent-physical-input-bridge','sha256':sha(bridge_raw)})
            old_nodes[point['id']]=directory
'''
    code=code[:first]+init+code[last:]
    code=code.replace('if calls>=123 or','if calls>=604 or')
    code=code.replace("':transport-recovery-r2'","':nested-refinement-r3'")
    code=code.replace("'first_level':1,'last_level':2,'max_callback_calls':125","'first_level':2,'last_level':3,'max_callback_calls':729")
    code=code.replace("calls==123 and len(cache)==125","calls==604 and len(cache)==729")
    code=code.replace("==125 and set(result['models'])","==729 and set(result['models'])")
    code=code.replace('exactly125_unique_physical_calls','exactly729_accumulated_unique_physical_calls').replace('125_callbacks_all_five_models','729_callbacks_all_five_models')
    code=code.replace("'reused_completed_calls':2,'total_physical_calls_across_R1_R2':calls+2","'reused_completed_calls':125,'total_physical_calls_accumulated':calls+125")
    # Freeze data bytes, rather than constructing a new experiment from the refined grid.
    code=code.replace("y=np.array(cent['models']['H1_TGL']['mean_without_nuisance'],dtype='<f8')/scales","expected_y=np.array(cent['models']['H1_TGL']['mean_without_nuisance'],dtype='<f8')/scales\n        y=np.frombuffer((H/'frozen_inputs/y_native.f64le').read_bytes(),dtype='<f8').copy()\n        if y.tobytes()!=expected_y.tobytes():raise RuntimeError('Synthetic center changed')")
    code=code.replace("for name,array in [('y_native',y),('C_native',C),('origin',origin)]:","if C.tobytes()!=(H/'frozen_inputs/C_native.f64le').read_bytes() or origin.tobytes()!=(H/'frozen_inputs/origin.f64le').read_bytes():raise RuntimeError('Frozen covariance/origin changed')\n        for name,array in [('y_native',y),('C_native',C),('origin',origin)]:")
    needle="            result=p.integrate_at_fixed_theta(joint,araw,assembly_sha256=sha(araw),background_json=packet,consumer_module=c,precision_json=praw,precision_sha256=sha(praw),services=services)"
    replacement='''            if point['id'] in old_nodes:
                directory=old_nodes[point['id']]
                original=json.loads((directory/'conditional.json').read_bytes())
                result,bridge=ce.rebind_conditional(original,json.loads((directory/'assembly.json').read_bytes()),assembled,json.loads((directory/'precision.json').read_bytes()),precision,old_admission,admission,old_loaded,json.loads(runtime),new_background_sha256=sha(packet),new_assembly_sha256=sha(araw),new_consumer_sha256=sha(adm_raw),new_precision_sha256=sha(praw))
                put('nodes/'+point['id']+'/conditional_bridge.json',bridge)
            else:
                result=p.integrate_at_fixed_theta(joint,araw,assembly_sha256=sha(araw),background_json=packet,consumer_module=c,precision_json=praw,precision_sha256=sha(praw),services=services)'''
    if needle not in code:raise RuntimeError('Conditional anchor missing')
    code=code.replace(needle,replacement)
    put(H/'run_refinement_r3.py',code.encode())
    launcher=(OLD/'launch_r2.py').read_text().replace('_R2','_R3').replace('run_full_prior_r2.py','run_refinement_r3.py').replace('launch_r2.py','launch_r3.py')
    put(H/'launch_r3.py',launcher.encode());put(H/'EXECUTION_LIMITS_R3.txt',(OLD/'EXECUTION_LIMITS_R2.txt').read_bytes()+b'\nR3: global limit600s unchanged; max604 new calls,125 reused,729 aggregate.\n')
    put(H/'DELTA_R3.diff',''.join(difflib.unified_diff(oldcode.splitlines(True),code.splitlines(True),fromfile='run_full_prior_r2.py',tofile='run_refinement_r3.py')).encode())
    for f in H.glob('*.py'):ast.parse(f.read_text())
    files=[p for p in H.rglob('*') if p.is_file()]
    plan={'schema':'F3_NESTED_PHYSICAL_REFINEMENT_R3','execution_pins':[{'path':p.relative_to(H).as_posix(),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in files],
      'first_level':2,'last_level':3,'reused_physical_calls':125,'max_new_CAMB_calls':604,'max_accumulated_CAMB_calls':729,'new_experiment':False,'observed_data':False,'unchanged':['data bytes','covariance','prior','models','precision tolerances','.01 diagnostic threshold','background physics','code/runtime'],
      'cache_contract':'Explicit consumed-input equality bridge, preserving original packet/receipt and result; catalog hash changes openly','conditional_reuse':'Exact numerical context/assembly/precision equality, explicit provenance bridge; no old services repeated','no_automatic_retry':True,'wall_seconds':600,'threads':1}
    put(H/'PLAN_R3.json',enc(plan));print(sha((H/'PLAN_R3.json').read_bytes()))
if __name__=='__main__':main()
