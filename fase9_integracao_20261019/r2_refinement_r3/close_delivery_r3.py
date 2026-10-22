"""Inspect terminal receipts and make an additive delivery; never calls a solver."""
from pathlib import Path
import hashlib,json,math,datetime
H=Path(__file__).resolve().parent;D=H;OLD=H.parent/'r2_full_integration'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def put(p,x):
    b=(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(b)
def main():
    result=read(D/'RESULT_R3.json');cmd=read(D/'COMMAND_RESULT_R3.json');theta=read(D/'THETA_RESULT_R3.json')
    if cmd['exit_code']!=0 or result['exit_code']!=0:raise RuntimeError('Not a completed result')
    old=read(OLD/'DELIVERY_FULL_R2.json')
    if old['recovery']['aggregate_unique_CAMB_calls']+result['solver_calls']!=729 or result['reused_completed_calls']!=125:raise RuntimeError('Aggregate count mismatch')
    if not all(x['passed'] for x in result['checks']):raise RuntimeError('Failed check')
    for folder,plan_name in [(H,'PLAN_R3A.json')]:
        for pin in read(folder/plan_name)['execution_pins']:
            if sha(folder/pin['path'])!=pin['sha256']:raise RuntimeError('Changed pin '+pin['path'])
    records=[];ks=[];betas=[];checks=[]
    for directory in sorted((D/'nodes').iterdir()):
        r=read(directory/'receipt.json');p=read(directory/'packet.json');a=read(directory/'assembly.json')
        if p['identity']['execution_receipt_sha256']!=sha(directory/'receipt.json'):raise RuntimeError('Receipt mismatch')
        if r.get('status')=='REUSED_COMPLETED_NOT_NEW_EXECUTION':
            origin=H/'original_nodes'/directory.name
            if r['original_packet_sha256']!=sha(origin/'packet.json') or read(origin/'packet.json')['result']!=p['result'] or not (directory/'conditional_bridge.json').exists():raise RuntimeError('Reused provenance mismatch')
        elif r.get('exit_code')!=0 or r['result_sha256']!=sha(directory/'result.json'):raise RuntimeError('New execution mismatch')
        models=a['models'];b=a['beta_TGL_runtime'];betas.append(b);ks.append(math.exp(p['result']['I_law']*b))
        checks.append(models['H1_TGL']['mean_without_nuisance'][:16]==models['H2_LCDM']['mean_without_nuisance'][:16])
        checks.append(models['H5_rd_free']['mean_without_nuisance'][:3]==models['H2_LCDM']['mean_without_nuisance'][:3])
        records.append({'point':directory.name,'theta':p['identity']['theta'],'receipt_sha256':sha(directory/'receipt.json'),'conditional_sha256':sha(directory/'conditional.json')})
    if len(records)!=729 or len({tuple(x['theta']) for x in records})!=729 or not all(checks) or len(set(betas))!=1:raise RuntimeError('Model/grid mismatch')
    quality=theta['conditional_precision_summary'];refinement=theta['refinement']
    numerical_ready=refinement['indicator_satisfied'] and quality['service_unassessed']==0 and quality['service_not_converged']==0 and quality['conditional_underflowed_nodes']==0
    report={'schema':'F3_PHYSICAL_REFINEMENT_DELIVERY_R3','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ENGINEERING_INTEGRATION_COMPLETE_NUMERICAL_DIAGNOSTIC_'+('PASS' if numerical_ready else 'INCONCLUSIVE'),'scope':'SYNTHETIC_ONLY_ONE_SPD_CONTEXT_NOT_OBSERVED','previous_delivery':{'file':str(OLD/'DELIVERY_FULL_R2.json'),'sha256':sha(OLD/'DELIVERY_FULL_R2.json'),'calls_completed':125},'original_failure':{'file':str(OLD/'FAILURE_R1.json'),'sha256':sha(OLD/'FAILURE_R1.json'),'calls_completed':2},'recovery':{'new_CAMB_calls':result['solver_calls'],'reused_completed_calls':125,'aggregate_unique_CAMB_calls':729,'exit_code':cmd['exit_code'],'seconds_scientific':result['seconds'],'seconds_launcher':cmd['seconds']},'models':theta['models'],'synthetic_lnB_against_H2':theta['lnB_against_H2_same_context'],'prior':theta['prior'],'normalization':theta['normalization'],'theta_marginalized':True,'K_grid_range':[min(ks),max(ks)],'K_scope':'Range on finite prior grid, not observational confidence interval; common theta used by every row and model','beta_runtime':betas[0],'beta_fixed_through_grid':True,'normalization_transport_repair':'np.float64 normalization.log_prefactor -> binary-identical native float; no broad coercion','checks':result['checks']+ [{'name':'all729_same_background_and_H5_CMB_identity','passed':all(checks)}],'refinement':refinement,'conditional_precision_summary':quality,'numerical_ready_diagnostic_only':numerical_ready,'scientific_verdict':None,'sigma':None,'observed_lnB':None,'operator_acts_created':False,'limitations':['This is ROOT/joint283row engineering structure, not scalarV2 combination','One synthetic SPD covariance not600systematiccases','H5 is BAO-only rd-free, not arbitrary background','MM remains CONDITIONAL_UNRATIFIED','CAMB approximation/theory error not globally bounded','Two-grid difference is diagnostic, not certified convergence','No observed data, admission, freeze, d72, production, memory or gate change'],'nodes':records}
    sources=[p for p in H.rglob('*') if p.is_file() and p.name not in ['DELIVERY_REFINEMENT_R3.json'] and '__pycache__' not in p.parts]
    report['artifacts']=[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(sources)]
    put(H/'DELIVERY_REFINEMENT_R3.json',report)
    print(json.dumps({k:report[k] for k in ['status','recovery','K_grid_range','refinement','conditional_precision_summary']},ensure_ascii=False))
    print('DELIVERY_SHA256',sha(H/'DELIVERY_REFINEMENT_R3.json'))
if __name__=='__main__':main()
