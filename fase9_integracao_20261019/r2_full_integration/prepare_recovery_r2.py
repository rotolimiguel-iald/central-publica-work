"""Additive transport repair; reuse two completed physical calls without retry."""
from pathlib import Path
import hashlib,json,difflib
H=Path(__file__).resolve().parent;D=H/'recovery_r2'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def main():
    oldplan=json.loads((H/'PLAN_R1.json').read_bytes())
    for pin in oldplan['execution_pins']:
        if sha((H/pin['path']).read_bytes())!=pin['sha256']:raise RuntimeError('R1 changed')
    for f in (H/'copies').iterdir():
        if f.is_file():put(D/'copies'/f.name,f.read_bytes())
    for name in ['CONFIGURATION','RECIPE','COPIED_SOURCE_PINS']:put(D/(name+'_R2.json'),(H/(name+'_R1.json')).read_bytes())
    cache=[]
    for node in ['p_2_2_2','p_0_0_0']:
        r=json.loads((H/'nodes'/node/'receipt.json').read_bytes());b=(H/'nodes'/node/'result.json').read_bytes()
        if r['exit_code']!=0 or r['successes']!=1 or sha(b)!=r['result_sha256']:raise RuntimeError('Uncertain cache forbidden')
        for name in ['claim.json','result.json','receipt.json','packet.json']:
            source=H/'nodes'/node/name;b=source.read_bytes();target=D/'nodes'/node/name;put(target,b)
            cache.append({'source':str(source),'copy':target.relative_to(D).as_posix(),'sha256':sha(b)})
    put(D/'CACHE_CUSTODY_R2.json',enc({'completed_physical_calls':2,'uncertain_calls':0,'entries':cache,'original_configuration_sha256':sha((H/'CONFIGURATION_R1.json').read_bytes())}))
    source=(H/'run_full_prior_r1.py').read_text(encoding='utf-8')
    code=source.replace('_R1','_R2')
    code=code.replace("cache={}\n",'''cache={}
        custody=json.loads((H/'CACHE_CUSTODY_R2.json').read_bytes())
        for item in custody['entries']:
            if sha((H/item['copy']).read_bytes())!=item['sha256']:raise RuntimeError('Custodied cache changed')
        for node in ['p_2_2_2','p_0_0_0']:
            packet=(H/'nodes'/node/'packet.json').read_bytes()
            record=json.loads(packet);receipt_raw=(H/'nodes'/node/'receipt.json').read_bytes()
            if record['identity']['engine_configuration_sha256']!=sha(config_raw) or record['identity']['runtime_sha256']!=sha(runtime_raw) or record['identity']['execution_receipt_sha256']!=sha(receipt_raw):raise RuntimeError('Cache physical identity differs')
            cache[tuple(record['identity']['theta'])]=(packet,{'id':node+':physical-background','sha256':sha(receipt_raw)})
''')
    code=code.replace('if calls>=125 or','if calls>=123 or')
    code=code.replace("'execution_unit_id':recipe['unit_id']","'execution_unit_id':recipe['unit_id']+':transport-recovery-r2'")
    needle="            result_raw=put('nodes/'+point['id']+'/conditional.json',ti._json_ready(result))"
    replacement="""            # Only the known normalization scalar is normalized. No broad coercion.
            value=result['normalization']['log_prefactor']
            if type(value) is np.float64:
                native=float(value)
                if not math.isfinite(native) or np.asarray(native,dtype='<f8').tobytes()!=np.asarray(value,dtype='<f8').tobytes():raise RuntimeError('Nonexact scalar conversion')
                result['normalization']['log_prefactor']=native
            elif type(value) is not float or not math.isfinite(value):raise RuntimeError('Unsupported normalization scalar')
            result_raw=put('nodes/'+point['id']+'/conditional.json',ti._json_ready(result))"""
    if needle not in code:raise RuntimeError('Patch anchor missing')
    code=code.replace(needle,replacement)
    code=code.replace("calls==125 and len(cache)==125","calls==123 and len(cache)==125")
    code=code.replace("'solver_calls':calls,","'solver_calls':calls,'reused_completed_calls':2,'total_physical_calls_across_R1_R2':calls+2,")
    put(D/'run_full_prior_r2.py',code.encode())
    launch=(H/'launch_r1.py').read_text(encoding='utf-8').replace('_R1','_R2').replace('run_full_prior_r1.py','run_full_prior_r2.py').replace('launch_r1.py','launch_r2.py')
    put(D/'launch_r2.py',launch.encode())
    put(D/'EXECUTION_LIMITS_R2.txt',(H/'EXECUTION_LIMITS_R1.txt').read_bytes())
    put(D/'TRANSPORT_DELTA_R2.diff',''.join(difflib.unified_diff(source.splitlines(True),code.splitlines(True),fromfile='run_full_prior_r1.py',tofile='run_full_prior_r2.py')).encode())
    files=[p for p in D.rglob('*') if p.is_file()]
    plan={'schema':'F3_TRANSPORT_REPAIR_CONTINUATION_R2','execution_pins':[{'path':p.relative_to(D).as_posix(),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in files],
      'parent_plan_sha256':sha((H/'PLAN_R1.json').read_bytes()),'parent_failure_sha256':sha((H/'FAILURE_R1.json').read_bytes()),'max_new_CAMB_calls':123,'reuse_completed_calls':2,'max_total_CAMB_calls':125,'criteria_changed':False,'observed_data':False,'no_automatic_retry':True,
      'repair':'Exact np.float64 to native float only at normalization.log_prefactor; reject nonfinite/other types; no numerical or scientific parameter change',
      'authorization':'Parent /root explicitly authorized transport correction and continuation with cache2+new<=123; preserve failureR1'}
    put(D/'PLAN_R2.json',enc(plan));print(sha((D/'PLAN_R2.json').read_bytes()))
if __name__=='__main__':main()
