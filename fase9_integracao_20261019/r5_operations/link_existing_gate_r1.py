"""Exercise the new admission consumer after the existing byte gate, read-only.

This verifies documentary sources, not an observed composite. No D-H act is
provided, so the end-to-end result must remain pending with two declared IDs.
"""
from pathlib import Path
import hashlib,json,importlib.util,sys
from preflight_bridge import prepare_with_admission
HERE=Path(__file__).resolve().parent
SOURCE=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
if __name__=='__main__':
    target=HERE/'ACTUAL_GATE_LINK_R1.json'
    if target.exists():raise FileExistsError(target)
    copied=HERE/'reused_gate';copied.mkdir(exist_ok=False)
    pins=[]
    for name in ['f9_reader_gate.py','f9_reader_gate_v1x_e1_bytes.py']:
        raw=(SOURCE/name).read_bytes()
        with (copied/name).open('xb') as f:f.write(raw)
        assert (copied/name).read_bytes()==raw
        pins.append({'source':pin(SOURCE/name),'copy':pin(copied/name)})
    sys.path.insert(0,str(copied))
    spec=importlib.util.spec_from_file_location('fase9_existing_gate',copied/'f9_reader_gate_v1x_e1_bytes.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    binding=SOURCE/'VINCULO_DOCUMENTAL_V1X_E1_BYTES_20261008.json'
    binding_pin=pin(binding)
    gate=module.verify_v1x_binding(binding,expected_binding_sha256=binding_pin['sha256'],
        allowed_source_root=SOURCE.parents[1]/'ORDEM_018',expected_spec_sha256=module.E1_SPEC_SHA256)
    result=prepare_with_admission(gate,expected_spec_sha256=module.E1_SPEC_SHA256,
        source_root=SOURCE.parents[1]/'ORDEM_018')
    assert result['n_alvos_declarados']==2 and result['required_sources_admitted'] is False
    assert result['may_open_data'] is False and result['verdict'] is None
    output={'status':'PASS_END_TO_END_DOCUMENTARY_PENDING','copies':pins,'binding':binding_pin,
            'consumer_pins':[pin(HERE/'preflight_bridge.py'),pin(HERE/'admission.py')],
            'result':result,'source_centers_composed':False,'D_H_act_created':False,
            'limit':'Read documentary sources via existing gate; no observed statistical execution, freeze or scientific verdict.'}
    with target.open('xb') as f:f.write(json.dumps(output,ensure_ascii=False,indent=2).encode('utf-8'))
    print(json.dumps(result,ensure_ascii=False))
