"""Offline R8 admission negatives. No synthetic PASS receipt is written to disk."""
from pathlib import Path
import ast,copy,json,sys
from unittest.mock import patch
S=Path(__file__).resolve().parent;W=S.parent;D=S/'mobile_R8_preparation_R2'
sys.path.insert(0,str(S));import release_lineage_guard_R8_R2 as guard
def main():
    config=json.loads((D/'R8_RELEASE_CONTRACT.json').read_bytes());checks={}
    for n in ['release_lineage_guard_R8_R2.py','prepare_mobile_R8_R2.py']:
        ast.parse((S/n).read_bytes());checks[n+'_syntax']=True
    expected=guard.check_chain(config,W,installed=False);guard.check_science(config,W)
    checks['ordered_union19']=len(expected)==19
    checks['latest_router_from_availability']=expected[str(guard.R/'iald_auto_router.py')]==json.loads(Path(config['layers'][-1]['plan']['path']).read_bytes())['files'][0]['sha256']
    checks['only_added_health_file']=set(expected)-set(config['layers'][0]['destinations'])=={str(guard.R/'iald_jev_connection_evidence.json')}
    checks['six_client_pins_unchanged']=all(expected[k]==v for k,v in config['mobile6'].items())
    real=guard.pinned;marker=dict(path='IN_MEMORY_FIXTURE_ONLY',sha256='not-execution-evidence')
    def final_fixture(data):
        return patch.object(guard,'pinned',side_effect=lambda item,work:data if item is marker else real(item,work))
    fixture=dict(status='PASS',files=[dict(path=p,sha256=h) for p,h in expected.items()])
    with final_fixture(fixture):
        result=guard.check_final(config,marker,W,installed=False,runtime=False)
        checks['synthetic19_shape_only_accepts']=result==expected
        missing=copy.deepcopy(config);missing['layers'][-1]['deployment']['sha256']=None
        try:guard.check_final(missing,marker,W,installed=True,runtime=True)
        except RuntimeError:checks['no_actual_availability_receipt_blocks']=True
        else:checks['no_actual_availability_receipt_blocks']=False
    for label,change in [('unknown20th',lambda f:f['files'].append(dict(path=str(guard.R/'unapproved.json'),sha256='0'*64))),
       ('original18_stale_router',lambda f:next(x for x in f['files'] if x['path']==str(guard.R/'iald_auto_router.py')).update(sha256='763cc541e5668e5ce3733be5a46821a4f25e84ea44410e6c33f48b797fd720c0')),
       ('not_pass',lambda f:f.update(status='PENDING')),
       ('duplicate',lambda f:f['files'].append(f['files'][0].copy()))]:
        data=copy.deepcopy(fixture);change(data)
        with final_fixture(data):
            try:guard.check_final(config,marker,W,installed=False,runtime=False)
            except RuntimeError:checks[label+'_refused']=True
            else:checks[label+'_refused']=False
    layer=config['layers'][1];bad=json.loads(Path(layer['plan']['path']).read_bytes());bad['files'][0]['baseline']='0'*64
    with patch.object(guard,'pinned',side_effect=lambda item,work:bad if item==layer['plan'] else real(item,work)):
        try:guard.check_chain(config,W,installed=False)
        except RuntimeError as e:checks['overlay_baseline_gap_refused']='baseline' in str(e)
        else:checks['overlay_baseline_gap_refused']=False
    fake=json.loads(Path(config['science_baseline']['path']).read_bytes());fake['files'][0]['sha256']='0'*64
    with patch.object(guard,'pinned',side_effect=lambda item,work:fake if item==config['science_baseline'] else real(item,work)):
        try:guard.check_science(config,W)
        except RuntimeError:checks['changed_science_refused']=True
        else:checks['changed_science_refused']=False
    for name,test in [('missing_autotest',None),('basic_ui_only',dict(status='BASIC_UI_PASS_PROVIDER_DISPATCH_PENDING'))]:
        p=dict(main_plan_current_pin=dict(sha256='x'),accepted_js_sha256='y')
        with patch.object(guard,'verify_final_state',return_value=expected),patch.object(guard,'pinned',side_effect=(RuntimeError('Pending pinned evidence') if test is None else lambda *a:test)):
            try:guard.verify_release_admission(dict(autotest_verification=None),p,W)
            except RuntimeError:checks[name+'_refused']=True
            else:checks[name+'_refused']=False
    checks['no_final_manifest_fabricated']=not (D/'FINAL_RUNTIME_PINS.json').exists()
    assert all(checks.values()),checks
    result=dict(status='PASS_OFFLINE_PREPARATION_GUARDS',checks=checks,count=len(checks),
        scope='Contract/schema and refusal controls only. Positive final19 fixture stayed in memory with installed=False/runtime=False. No actual final19/build/dispatch success asserted.',build=False,push=False,commit=False,runtime_writes=False)
    with (D/'R8_TEST_RESULTS_R1.json').open('xb') as f:f.write(json.dumps(result,indent=2).encode())
    print(json.dumps(dict(status=result['status'],checks=len(checks))))
if __name__=='__main__':main()
