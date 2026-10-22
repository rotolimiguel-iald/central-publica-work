"""Narrow phase guard controls only. No client regression replay or execution."""
from pathlib import Path
import ast,copy,json,sys,subprocess
from unittest.mock import patch
S=Path(__file__).resolve().parent;W=S.parent;OUT=S/'mobile_R9_preparation_R2'
sys.path.insert(0,str(S));import release_lineage_guard_R9 as guard
def main():
    config=json.loads((OUT/'R8_RELEASE_CONTRACT.json').read_bytes());checks={}
    for n in ['prepare_mobile_R9_R2.py','release_lineage_guard_R9.py']:
        ast.parse((S/n).read_bytes());checks[n+'_syntax']=True
    phase=json.loads((W/'REVIEW_BUILD_PUSH_PHASE_R8.json').read_bytes())
    assert phase['status']=='PASS_BUILD_PUSH_TECHNICAL_SCOPE'
    plan=dict(release_binding={'fixture':'config'},main_plan_current_pin=dict(sha256='synthetic_final_digest'))
    base=dict(status='PASS',actor='distinct-fixture-reviewer',phase_review_sha256=config['engineering_phase_review']['sha256'],final_manifest_sha256='synthetic_final_digest',execution_plan_sha256={k:'synthetic_plan_digest' for k in ['android30_build','private_mobile_commit','private_mobile_push']})
    for op in base['execution_plan_sha256']:
        receipt=dict(operation=op,plan_sha256='synthetic_plan_digest',phase_binding_addendum={'fixture':'addendum'},execution_authorized_now=True)
        def mocked(item,work):
            if item==plan['release_binding']:return config
            if item==config['engineering_phase_review']:return phase
            if item==receipt['phase_binding_addendum']:return base
            raise RuntimeError('Pending pinned evidence')
        with patch.object(guard,'verify_final_state',return_value={}),patch.object(guard,'pinned',side_effect=mocked):
            checks[op+'_engineering_gate_has_no_autotest_requirement']=guard.verify_release_admission(receipt,plan,W) is True
            blocked=receipt.copy();blocked['execution_authorized_now']=False
            try:guard.verify_release_admission(blocked,plan,W)
            except RuntimeError as e:checks[op+'_concrete_parent_go_required']='Concrete parent' in str(e)
            else:checks[op+'_concrete_parent_go_required']=False
            bad=copy.deepcopy(base);bad['final_manifest_sha256']='old_digest'
            with patch.object(guard,'pinned',side_effect=lambda i,w:bad if i==receipt['phase_binding_addendum'] else mocked(i,w)):
                try:guard.verify_release_admission(receipt,plan,W)
                except RuntimeError:checks[op+'_old_final_binding_refused']=True
                else:checks[op+'_old_final_binding_refused']=False
    checks['label4_is_last_layer']=config['layers'][-1]['role']=='label4' and config['layers'][-1]['count']==4
    checks['latest_mobile_js_5bc']=all(v=='5bc89f6f9ffc9a78d0b49d8805589dc1a77cc60af87274439bda2b4d46d94fb6' for k,v in config['mobile6'].items() if Path(k).name=='iald.js')
    label=S/'media_label_R8';p=json.loads((label/'install_plan_LABEL_R8.json').read_bytes())['files'][0]['source']
    cp=subprocess.run(['node','--check',p],capture_output=True);checks['label_node_syntax']=cp.returncode==0
    assert all(checks.values()),checks
    result=dict(status='PASS_NARROW_ENGINEERING_PHASE_GUARDS',checks=checks,count=len(checks),regression164_repeated=False,
        scope='Positive permission checks used only in-memory fixtures and mocked final-state validation. No real phase addendum/go/autotest was created or accepted. Actual binding still requires all five reviewed/installed layers, current19/science/mobile pins.',build=False,commit=False,push=False,provider_calls=0)
    with (OUT/'ENGINEERING_PHASE_TESTS_R9.json').open('xb') as f:f.write(json.dumps(result,indent=2).encode())
    print(json.dumps(dict(status=result['status'],checks=len(checks))))
if __name__=='__main__':main()
