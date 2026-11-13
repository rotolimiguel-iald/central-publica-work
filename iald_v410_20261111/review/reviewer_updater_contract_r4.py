import sys,json,tempfile,hashlib
from pathlib import Path
A=Path(r'C:\IALD\Central de Patentes\work\iald_v410_20261111')
sys.path.insert(0,str(A/'app/R4/continuous_update'))
from continuous_update_adapter import Adapter
from continuous_source_prepare import dump,digest
W=Path(__file__).parent
checks=[]
with tempfile.TemporaryDirectory(dir=W) as td:
 root=Path(td);candidate=root/'candidate';candidate.mkdir();(candidate/'package').mkdir()
 manifest=candidate/'package/release.json';manifest.write_bytes(b'{}');pin=digest(b'{}')
 ref=root/'SESSION_REFERENCE.json';ref.write_bytes(b'{}')
 plan=candidate/'install_plan.json';plan.write_bytes(b'plan')
 binding=candidate/'REVIEW_BINDING.json'
 data={'manifest_sha256':pin,'reference':str(ref),'requirement':'candidate','final_pins':[{'path':str(plan),'sha256':digest(b'plan')}]}
 binding.write_bytes(dump(data))
 task={'id':'candidate','status':'satisfied','submitted_by':'builder','reviewed_by':'independent','review_evidence':[{'path':str(binding),'sha256':digest(binding.read_bytes())}],'evidence':[{'path':str(manifest),'sha256':pin}]}
 projection={'hold':False,'active':[],'settled':[task]}
 adapter=Adapter.__new__(Adapter);adapter.root=root
 adapter.command=lambda *a,**k:dump({'ok':True,'result':{'projection':projection}})
 assert adapter.review(candidate,pin);checks.append('valid_synthetic_distinct_acceptance')
 task['status']='review_pending';assert adapter.review(candidate,pin) is False;checks.append('pending_refused');task['status']='satisfied'
 projection['hold']=True;assert adapter.review(candidate,pin) is False;checks.append('hold_refused');projection['hold']=False
 task['reviewed_by']='builder'
 try:adapter.review(candidate,pin)
 except ValueError:checks.append('self_review_refused')
 else:raise AssertionError('self review')
 task['reviewed_by']='independent';task['review_evidence'][0]['sha256']='0'*64
 try:adapter.review(candidate,pin)
 except ValueError:checks.append('binding_pin_mismatch_refused')
 else:raise AssertionError('binding mismatch')
 task['review_evidence'][0]['sha256']=digest(binding.read_bytes());plan.write_bytes(b'changed')
 try:adapter.review(candidate,pin)
 except ValueError:checks.append('post_review_plan_change_refused')
 else:raise AssertionError('plan change')
output=W/'reviewer_updater_contract_r4.json'
assert not output.exists()
result={'status':'PASS_NARROW_OFFLINE','checks':checks,'synthetic_acom_only':True,'real_acom_acceptance':False,'adapter_sha256':digest((A/'app/R4/continuous_update/continuous_update_adapter.py').read_bytes()),'script_sha256':digest(Path(__file__).read_bytes())}
output.write_bytes(dump(result));print(json.dumps(result))
