"""Explicit transport of completed results between equivalent point catalogs.

No solver. Equality concerns the frozen prediction_worker/check_theta inputs,
not the whole configuration hash. Original receipts always remain visible.
"""
import hashlib,json,math
FIELDS=('prior','background','accuracy_profiles','redshifts','precision','h5_candidate')
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def projection(configuration,point,*,engine_sha256,runtime_sha256):
    if point not in configuration['points']:raise ValueError('Point not in catalog')
    return {'consumed_configuration':{k:configuration[k] for k in FIELDS},'selected_point':point,'profile_id':'reference','engine_sha256':engine_sha256,'runtime_sha256':runtime_sha256}
def rebind_background(old_packet,old_receipt,old_result,old_config,new_config,point,*,engine_sha256,runtime_sha256,old_configuration_sha256):
    p=json.loads(old_packet);r=json.loads(old_receipt);result=json.loads(old_result)
    if p['status']!='ENGINEERING_RESULT' or p['error'] is not None or r['exit_code']!=0 or r['attempts']!=1 or r['successes']!=1:raise ValueError('Incomplete/uncertain background')
    ident=p['identity']
    if ident['engine_configuration_sha256']!=old_configuration_sha256 or r['identity']['engine_configuration_sha256']!=old_configuration_sha256:raise ValueError('Original configuration pin differs')
    if ident['execution_receipt_sha256']!=sha(old_receipt) or r['result_sha256']!=sha(old_result) or enc(p['result'])!=enc(result):raise ValueError('Original receipt/result mismatch')
    if ident['engine_sha256']!=engine_sha256 or ident['runtime_sha256']!=runtime_sha256 or ident['theta']!=point['theta'] or result['theta']!=point['theta'] or result['point_id']!=point['id']:raise ValueError('Physical identity mismatch')
    oldpoint=next(x for x in old_config['points'] if x['id']==point['id'])
    oldproj=projection(old_config,oldpoint,engine_sha256=engine_sha256,runtime_sha256=runtime_sha256)
    newproj=projection(new_config,point,engine_sha256=engine_sha256,runtime_sha256=runtime_sha256)
    if enc(oldproj)!=enc(newproj):raise ValueError('Non-equivalent physical inputs')
    return p,{'schema':'F3_EQUIVALENT_PHYSICAL_INPUT_BRIDGE_R3','status':'REUSED_COMPLETED_NOT_NEW_EXECUTION','original_packet_sha256':sha(old_packet),'original_receipt_sha256':sha(old_receipt),'original_result_sha256':sha(old_result),'consumed_input_projection_sha256':sha(enc(oldproj)),'point':point,'basis':'All config objects consumed by prediction_worker/check_theta and same code/runtime; unrelated catalog entries excluded','solver_calls_in_bridge':0}
def rebind_conditional(original,old_assembly,new_assembly,old_precision,new_precision,old_admission,new_admission,old_loaded,new_loaded,*,new_background_sha256,new_assembly_sha256,new_consumer_sha256,new_precision_sha256):
    # Exact equality of every numerical input and structural identity; provenance differs.
    for key in ['models','row_ids','row_units','native_to_output_row_scale','nuisance','response_columns','beta_TGL_runtime','certification']:
        if enc(old_assembly[key])!=enc(new_assembly[key]):raise ValueError('Changed conditional assembly '+key)
    for key in ['input_sha256','structure_sha256','source_pins','coordinates','output_measure','common_measure_id','MM_status','expected_support_rank','tolerances','data_kind']:
        if enc(old_admission[key])!=enc(new_admission[key]):raise ValueError('Changed conditional context '+key)
    for key in ['source_pins','services','max_quadrature_evaluations','max_window_evaluations','absolute_log_error_target','absolute_scaled_error_target','relative_scaled_error_target']:
        if enc(old_precision[key])!=enc(new_precision[key]):raise ValueError('Changed precision '+key)
    for key in ['numpy','python','runtime_sha256','class_module']:
        if old_loaded[key]!=new_loaded[key]:raise ValueError('Changed numerical runtime')
    if original['provenance']['assembly_sha256']!=sha(enc(old_assembly)) or original['provenance']['precision_sha256']!=sha(enc(old_precision)) or original['provenance']['consumer_admission_sha256']!=sha(enc(old_admission)):raise ValueError('Original conditional linkage broken')
    copied=json.loads(enc(original));copied['provenance'].update(assembly_sha256=new_assembly_sha256,background_sha256=new_background_sha256,consumer_admission_sha256=new_consumer_sha256,precision_sha256=new_precision_sha256)
    bridge={'schema':'F3_CONDITIONAL_VALUE_TRANSPORT_R3','status':'REUSED_NUMERICAL_RESULT_NOT_RECOMPUTED','original_conditional_sha256':sha(enc(original)),'original_provenance':original['provenance'],'new_provenance':copied['provenance'],'unchanged_fields':[k for k in original if k!='provenance'],'physical_calls':0,'precision_service_calls':0}
    return copied,bridge
