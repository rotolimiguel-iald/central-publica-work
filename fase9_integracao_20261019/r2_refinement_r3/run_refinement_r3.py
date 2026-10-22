"""Five physical models, one frozen synthetic context, full theta prior. Single-use."""
from pathlib import Path
import datetime, hashlib, json, math, os, sys, time, traceback
H=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(name,value):
    p=H/name;p.parent.mkdir(exist_ok=True,parents=True)
    b=enc(value);temp=p.with_suffix(p.suffix+'.new')
    if p.exists():raise FileExistsError(p)
    with temp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(b):raise RuntimeError('Incomplete output')
    temp.rename(p);return b
def main():
    plan_raw=(H/'PLAN_R3.json').read_bytes();plan=json.loads(plan_raw)
    if sys.argv[1:]!=[sha(plan_raw)]:raise RuntimeError('Plan pin required')
    for pin in plan['execution_pins']:
        if sha((H/pin['path']).read_bytes())!=pin['sha256']:raise RuntimeError('Pin mismatch '+pin['path'])
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        if os.environ.get(key)!='1':raise RuntimeError('Single-thread environment required')
    put('START_R3.json',{'started_utc':now(),'plan_sha256':sha(plan_raw),'execution_count':1})
    start=time.perf_counter();calls=0;checks=[];integrator=None
    try:
        sys.path.insert(0,str(H/'copies'))
        import numpy as np
        import background_controls as bg
        import theta_integrator as ti
        import five_model_assembly as a
        import likelihood_consumer as c
        import physical_prior as p
        import precision_services as ps
        import linear_gaussian as lg
        import cache_equivalence_r3 as ce
        recipe=json.loads((H/'RECIPE_R3.json').read_bytes());cfg=json.loads((H/'CONFIGURATION_R3.json').read_bytes())
        config_raw=(H/'CONFIGURATION_R3.json').read_bytes();runtime_raw=(H/'copies/RUNTIME_METADATA.json').read_bytes()
        layout_raw=(H/'copies/LAYOUT_ESTRUTURAL_3CMB_13BAO.json').read_bytes();design_raw=(H/'copies/ESPECIFICACAO_LINEAR.json').read_bytes()
        bg.runtime_check()
        runtime=put('LOADED_BINDING_R3.json',{'numpy':np.__version__,'python':sys.version,'runtime_sha256':sha(runtime_raw),'class_module':lg.FlatNuisanceGaussian.__module__,'sources':plan['execution_pins'],'runtime_file_check':True})
        reference={'id':recipe['unit_id']+':synthetic-recipe','sha256':sha((H/'RECIPE_R3.json').read_bytes())}
        assembly_admission={'schema':'F9_ASSEMBLY_ADMISSION_V1','status':'ENGINEERING_STRUCTURAL_ADMISSION','layout_sha256':sha(layout_raw),'sources':a.SOURCE_PINS,'engine_configuration_sha256':sha(config_raw),'runtime_sha256':sha(runtime_raw)}
        ad_raw=put('ASSEMBLY_ADMISSION_R3.json',assembly_admission)
        cache={}; old_nodes={}
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
        def background(point):
            nonlocal calls
            key=tuple(point['theta'])
            if key in cache:
                packet,receipt=cache[key]
                disk=(H/'nodes'/point['id']/'packet.json').read_bytes()
                if sha(disk)!=sha(packet):raise RuntimeError('Cache identity mismatch')
                return packet,receipt,'VERIFIED_DURABLE_CACHE'
            if calls>=604 or time.perf_counter()-start>600:raise RuntimeError('Resource budget exhausted')
            calls+=1;begin=now();t=time.perf_counter()
            identity={'theta':point['theta'],'engine_configuration_sha256':sha(config_raw),'runtime_sha256':sha(runtime_raw),'engine_sha256':sha((H/'copies/background_controls.py').read_bytes())}
            put('nodes/'+point['id']+'/claim.json',{'attempt':calls,'started_utc':begin,'identity':identity})
            # No catch/retry at the solver boundary. An uncertain claim remains terminal.
            result=bg.prediction_worker(cfg,point['id'],'reference')
            result_raw=put('nodes/'+point['id']+'/result.json',result)
            receipt_raw=put('nodes/'+point['id']+'/receipt.json',{'identity':identity,'started_utc':begin,'ended_utc':now(),'seconds':time.perf_counter()-t,'exit_code':0,'attempts':1,'successes':1,'result_sha256':sha(result_raw)})
            packet=put('nodes/'+point['id']+'/packet.json',{'schema':'F9_BACKGROUND_PACKET_V1','status':'ENGINEERING_RESULT','identity':{'engine_sha256':a.SOURCE_PINS['background_engine']['sha256'],'protocol_sha256':a.SOURCE_PINS['background_protocol']['sha256'],'engine_configuration_sha256':sha(config_raw),'runtime_sha256':sha(runtime_raw),'theta':point['theta'],'z_law':cfg['redshifts']['z_star_law'],'units':a.BACKGROUND_UNITS,'execution_receipt_sha256':sha(receipt_raw)},'result':result,'error':None})
            receipt={'id':point['id']+':physical-background','sha256':sha(receipt_raw)}
            cache[key]=(packet,receipt)
            return packet,receipt,'NEW_EXECUTION'
        def assemble(theta,packet):
            common=dict(zip(a.THETA_NAMES,theta))
            pars={m:{**common,**{k:recipe['anchors'][k] for k in a.EXTRAS[m]}} for m in a.MODELS}
            return a.assemble_five(pars,design_json=design_raw,layout_json=layout_raw,background_json=packet,admission_json=ad_raw,admission_sha256=sha(ad_raw))
        center=next(x for x in cfg['points'] if x['id']==recipe['center']['point_id'])
        if center['theta']!=recipe['center']['theta']:raise RuntimeError('Center mismatch')
        center_packet,_,_=background(center)
        cent=assemble(center['theta'],center_packet);cent_raw=put('CENTER_ASSEMBLY_R3.json',cent)
        structure_raw=c.extract_structure(cent_raw,assembly_sha256=sha(cent_raw));structure=json.loads(structure_raw)
        scales=np.array(structure['native_to_output_row_scale'],dtype='<f8')
        expected_y=np.array(cent['models']['H1_TGL']['mean_without_nuisance'],dtype='<f8')/scales
        y=np.frombuffer((H/'frozen_inputs/y_native.f64le').read_bytes(),dtype='<f8').copy()
        if y.tobytes()!=expected_y.tobytes():raise RuntimeError('Synthetic center changed')
        sig=np.array(recipe['covariance']['sigma_first3']+[recipe['covariance']['sigma_BAO']]*13+[recipe['covariance']['sigma_local']]*267)
        corr=np.eye(283)
        for i,j,v in recipe['covariance']['cross_correlations']:corr[i,j]=corr[j,i]=v
        C=(corr*sig[:,None]*sig[None,:])/scales[:,None]/scales[None,:];C=np.asarray(C,dtype='<f8');origin=np.zeros(283,dtype='<f8')
        if C.tobytes()!=(H/'frozen_inputs/C_native.f64le').read_bytes() or origin.tobytes()!=(H/'frozen_inputs/origin.f64le').read_bytes():raise RuntimeError('Frozen covariance/origin changed')
        for name,array in [('y_native',y),('C_native',C),('origin',origin)]:
            with (H/(name+'.f64le')).open('xb') as f:f.write(array.tobytes())
        loaded_ref={'id':'loaded-physical-and-statistical-objects','sha256':sha(runtime)}
        backend=put('BACKEND_BINDING_R3.json',{'schema':'F9_QUALIFIED_BACKEND_CALLER_RECEIPT_V1','source_pins':{k:c.SOURCE_PINS[k] for k in ('linear_gaussian','support')},'runtime_reference':loaded_ref,'class_module':lg.FlatNuisanceGaussian.__module__,'class_name':'FlatNuisanceGaussian','caller_verification_reference':loaded_ref})
        admission={'schema':'F9_CONSUMER_ADMISSION_V1','scope':'ENGINEERING_POINTWISE_ONLY','scenario_id':'one-explicit-synthetic-SPD-context','data_kind':'SYNTHETIC','input_sha256':{'y_native_f64le':sha(y.tobytes()),'C_native_f64le':sha(C.tobytes()),'affine_origin_native_f64le':sha(origin.tobytes()),'row_ids_canonical_json':sha(c._canonical(structure['row_ids']))},'structure_sha256':sha(structure_raw),'source_pins':c.SOURCE_PINS,'backend_receipt_sha256':sha(backend),'prediction_admission_sha256':sha(ad_raw),'coordinates':c.COORDINATES,'output_measure':c.OUTPUT_MEASURE,'common_measure_id':'synthetic-common-kappa-deta-r1','MM_status':'CONDITIONAL_UNRATIFIED','expected_support_rank':283,'tolerances':recipe['tolerances'],'references':{k:reference for k in ['statistical_model','covariance_and_cross_blocks','fixed_affine_support','compression_and_offsets','common_nuisance_measure','MM_conditional_model','structure_review','synthetic_fixture']}}
        adm_raw=put('CONSUMER_ADMISSION_R3.json',admission);put('STRUCTURE_R3.json',structure)
        joint=c.prepare_joint(y,C,structure['row_ids'],affine_origin_native=origin,structure_json=structure_raw,admission_json=adm_raw,admission_sha256=sha(adm_raw),backend_receipt_json=backend,numpy_module=np,flat_gaussian_class=lg.FlatNuisanceGaussian)
        def check(name,value):
            checks.append({'name':name,'passed':bool(value)})
            if not value:raise AssertionError(name)
        check('283_rows_63_eta_full_support',joint._engine.n==283 and joint._engine.p==63 and joint._engine.support.rank==283)
        check('five_models_preserved',tuple(cent['models'])==a.MODELS)
        check('H5_preserves_CMB',cent['models']['H5_rd_free']['mean_without_nuisance'][:3]==cent['models']['H2_LCDM']['mean_without_nuisance'][:3])
        check('H3_zero_equals_LCDM',cent['models']['H3_beta_free']['mean_without_nuisance']==cent['models']['H2_LCDM']['mean_without_nuisance'])
        check('H4_zero_equals_LCDM',cent['models']['H4_Cepheid']['mean_without_nuisance']==cent['models']['H2_LCDM']['mean_without_nuisance'])
        code_sha=sha(Path(__file__).read_bytes());callback_ref={'id':'physical-five-model-prior-callback-r1','sha256':code_sha}
        theta_plan={'schema':'F9_THETA_INTEGRATION_PLAN_V1','preparation_request_id':ti.REQUEST_ID,'execution_unit_id':recipe['unit_id']+':nested-refinement-r3','source_pins':ti.SOURCE_PINS,'consumer_admission_sha256':sha(adm_raw),'assembly_admission_sha256':sha(ad_raw),'engine_configuration_sha256':sha(config_raw),'callback_reference':callback_ref,'controller_reference':{'id':'single-use-synthetic-driver-r1','sha256':code_sha},'first_level':2,'last_level':3,'max_callback_calls':729,'absolute_log_refinement_target':recipe['absolute_log_refinement_target'],'common_measure_id':admission['common_measure_id']}
        theta_raw=put('THETA_PLAN_R3.json',theta_plan)
        services={k:getattr(ps,k) for k in ['log_exp_quad_interval','positive_quad_1d']}
        def callback(descriptor):
            point=next(x for x in cfg['points'] if x['theta']==descriptor['theta'])
            packet,receipt,origin_kind=background(point)
            assembled=assemble(descriptor['theta'],packet);araw=put('nodes/'+point['id']+'/assembly.json',assembled)
            precision={'schema':'F9_PHYSICAL_PRIOR_PRECISION_V1','source_pins':p.SOURCE_PINS,'consumer_admission_sha256':sha(adm_raw),'assembly_sha256':sha(araw),'services':{k:{'id':getattr(ps,'LOG_SERVICE_ID' if k.startswith('log_') else 'QUAD_SERVICE_ID'),'sha256':sha((H/'copies/precision_services.py').read_bytes())} for k in services},**recipe['precision'],'caller_verification_reference':loaded_ref}
            praw=put('nodes/'+point['id']+'/precision.json',precision)
            if point['id'] in old_nodes:
                directory=old_nodes[point['id']]
                original=json.loads((directory/'conditional.json').read_bytes())
                result,bridge=ce.rebind_conditional(original,json.loads((directory/'assembly.json').read_bytes()),assembled,json.loads((directory/'precision.json').read_bytes()),precision,old_admission,admission,old_loaded,json.loads(runtime),new_background_sha256=sha(packet),new_assembly_sha256=sha(araw),new_consumer_sha256=sha(adm_raw),new_precision_sha256=sha(praw))
                put('nodes/'+point['id']+'/conditional_bridge.json',bridge)
            else:
                result=p.integrate_at_fixed_theta(joint,araw,assembly_sha256=sha(araw),background_json=packet,consumer_module=c,precision_json=praw,precision_sha256=sha(praw),services=services)
            # Only the known normalization scalar is normalized. No broad coercion.
            value=result['normalization']['log_prefactor']
            if type(value) is np.float64:
                native=float(value)
                if not math.isfinite(native) or np.asarray(native,dtype='<f8').tobytes()!=np.asarray(value,dtype='<f8').tobytes():raise RuntimeError('Nonexact scalar conversion')
                result['normalization']['log_prefactor']=native
            elif type(value) is not float or not math.isfinite(value):raise RuntimeError('Unsupported normalization scalar')
            result_raw=put('nodes/'+point['id']+'/conditional.json',ti._json_ready(result))
            return {'conditional_result':result,'receipt':{'node_id':descriptor['node_id'],'execution_unit_id':descriptor['execution_unit_id'],'callback_reference':descriptor['callback_reference'],'conditional_result_reference':{'id':point['id']+':conditional','sha256':ti.canonical_conditional_sha256(result)},'background_execution_reference':receipt,'background_attempts':1,'background_successes':1,'background_origin':origin_kind,'background_calls_this_callback':int(origin_kind=='NEW_EXECUTION'),'assembly_admission_sha256':sha(ad_raw),'engine_configuration_sha256':sha(config_raw)}}
        integrator=ti.ThetaIntegrator(theta_raw,plan_sha256=sha(theta_raw),evaluate_node=callback)
        result=integrator.run();put('THETA_RESULT_R3.json',result)
        check('exactly729_accumulated_unique_physical_calls',calls==604 and len(cache)==729)
        check('729_callbacks_all_five_models',result['callback_counts']['completed']==729 and set(result['models'])==set(a.MODELS))
        check('normalized_theta_prior_once',result['prior']['unit_cube_density_exact']=='1')
        check('no_observed_or_scientific_verdict',result['sigma'] is None and result['p'] is None and result['verdict'] is None)
        put('RESULT_R3.json',{'status':'SYNTHETIC_INTEGRATION_COMPLETE','exit_code':0,'started_utc':json.loads((H/'START_R3.json').read_bytes())['started_utc'],'ended_utc':now(),'seconds':time.perf_counter()-start,'solver_calls':calls,'reused_completed_calls':2,'total_physical_calls_across_R1_R3':calls+2,'checks':checks,'refinement':result['refinement'],'conditional_precision_summary':result['conditional_precision_summary'],'observed_data':False,'limits':recipe['limits'],'plan_sha256':sha(plan_raw),'theta_result_sha256':sha((H/'THETA_RESULT_R3.json').read_bytes())})
        print(json.dumps({'status':'complete','calls':calls,'seconds':time.perf_counter()-start,'refinement':result['refinement']}))
    except BaseException as exc:
        put('FAILURE_R3.json',{'status':'FAILED_TERMINAL_NO_RETRY','exit_code':1,'ended_utc':now(),'seconds':time.perf_counter()-start,'solver_calls_attempted':calls,'checks':checks,'exception':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc(),'diagnostics':None if integrator is None else integrator.diagnostics()})
        raise
if __name__=='__main__':main()
