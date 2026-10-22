"""Transport completed R3 values with explicit R2->R3 ancestry; no solver."""
from pathlib import Path
import json
import cache_equivalence_r3_base as base
enc,sha,projection=base.enc,base.sha,base.projection
H=Path(__file__).resolve().parent

def load(p):return json.loads(p.read_bytes())

def verify_r3_bridge(point,old_packet,old_receipt,old_result,old_config,engine_sha256,runtime_sha256):
    """A bridge is not a solver receipt: recover and verify its actual R2 parent."""
    d=H/'ancestry'/'nodes'/point['id'];ctx=H/'ancestry'/'context'
    if not d.is_dir():raise ValueError('Missing direct-execution ancestor')
    c2raw=(ctx/'CONFIGURATION_R2.json').read_bytes();c2=json.loads(c2raw)
    packet,expected=base.rebind_background((d/'packet.json').read_bytes(),(d/'receipt.json').read_bytes(),(d/'result.json').read_bytes(),c2,old_config,point,engine_sha256=engine_sha256,runtime_sha256=runtime_sha256,old_configuration_sha256=sha(c2raw))
    expected.update(original_configuration_sha256=sha(c2raw),new_configuration_sha256=sha((H/'original_context'/'CONFIGURATION_R3.json').read_bytes()))
    if enc(expected)!=enc(json.loads(old_receipt)):raise ValueError('R3 bridge differs from verified R2 transport')
    packet['identity']['engine_configuration_sha256']=expected['new_configuration_sha256']
    packet['identity']['execution_receipt_sha256']=sha(old_receipt)
    if enc(packet)!=enc(json.loads(old_packet)) or enc(packet['result'])!=enc(json.loads(old_result)):raise ValueError('R3 transported packet altered')
    current=H/'original_nodes'/point['id'];ctx3=H/'original_context'
    transported,cbridge=base.rebind_conditional(load(d/'conditional.json'),load(d/'assembly.json'),load(current/'assembly.json'),load(d/'precision.json'),load(current/'precision.json'),load(ctx/'CONSUMER_ADMISSION_R2.json'),load(ctx3/'CONSUMER_ADMISSION_R3.json'),load(ctx/'LOADED_BINDING_R2.json'),load(ctx3/'LOADED_BINDING_R3.json'),new_background_sha256=sha(old_packet),new_assembly_sha256=sha((current/'assembly.json').read_bytes()),new_consumer_sha256=sha((ctx3/'CONSUMER_ADMISSION_R3.json').read_bytes()),new_precision_sha256=sha((current/'precision.json').read_bytes()))
    if enc(transported)!=enc(load(current/'conditional.json')) or enc(cbridge)!=enc(load(current/'conditional_bridge.json')):raise ValueError('R3 conditional ancestry mismatch')
    return {'status':'R2_DIRECT_EXECUTION_THEN_VERIFIED_R3_BRIDGE','original_direct_receipt_sha256':sha((d/'receipt.json').read_bytes()),'original_direct_packet_sha256':sha((d/'packet.json').read_bytes()),'R3_bridge_sha256':sha(old_receipt),'R3_conditional_bridge_sha256':sha((current/'conditional_bridge.json').read_bytes())}

def rebind_background(old_packet,old_receipt,old_result,old_config,new_config,point,*,engine_sha256,runtime_sha256,old_configuration_sha256):
    receipt=json.loads(old_receipt)
    if receipt.get('status')!='REUSED_COMPLETED_NOT_NEW_EXECUTION':
        packet,bridge=base.rebind_background(old_packet,old_receipt,old_result,old_config,new_config,point,engine_sha256=engine_sha256,runtime_sha256=runtime_sha256,old_configuration_sha256=old_configuration_sha256)
        bridge['ancestry']={'status':'R3_DIRECT_EXECUTION','direct_receipt_sha256':sha(old_receipt)}
        return packet,bridge
    ancestry=verify_r3_bridge(point,old_packet,old_receipt,old_result,old_config,engine_sha256,runtime_sha256)
    packet=json.loads(old_packet);ident=packet['identity']
    if ident['engine_configuration_sha256']!=old_configuration_sha256 or ident['execution_receipt_sha256']!=sha(old_receipt):raise ValueError('Current R3 identity broken')
    previous=next(x for x in old_config['points'] if x['id']==point['id'])
    a=projection(old_config,previous,engine_sha256=engine_sha256,runtime_sha256=runtime_sha256)
    b=projection(new_config,point,engine_sha256=engine_sha256,runtime_sha256=runtime_sha256)
    if enc(a)!=enc(b):raise ValueError('Changed physical input')
    return packet,{'schema':'F3_EQUIVALENT_PHYSICAL_INPUT_BRIDGE_R4','status':'REUSED_COMPLETED_NOT_NEW_EXECUTION','original_packet_sha256':sha(old_packet),'original_receipt_sha256':sha(old_receipt),'original_result_sha256':sha(old_result),'consumed_input_projection_sha256':sha(enc(a)),'point':point,'basis':'R2 direct receipt -> verified R3 transport -> equal consumed R4 inputs','ancestry':ancestry,'solver_calls_in_bridge':0}

rebind_conditional=base.rebind_conditional
