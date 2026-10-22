from pathlib import Path
import json
import chat_wire_codec as c
import jobs_transport_adapter as a
R=Path(__file__).resolve().parent
results=[]
def check(name,value):
    results.append(dict(name=name,passed=bool(value)))
    assert value,name
scope='review_generation'
obj=dict(account=scope,request_id='review_1',iald_conv='conv_1',messages=[dict(role='user',content=[dict(type='document',data='AABB'*6000),dict(type='image_url',image_url=dict(url='data:image/png;base64,AAAA'))])])
raw=c.dump(obj);wire=c.request_candidate(raw,scope);parsed=json.loads(wire)
legacy=dict(messages=[])
check('legacy_object_identity',a.decode_before_submit(b'{}',legacy,scope,lambda _:False) is legacy)
observed=[]
payload=a.decode_before_submit(wire,parsed,scope,lambda p:observed.append(p) or False)
check('attachments_original_and_guard_receives_decoded',payload==obj and observed==[obj])
refused=False
try:a.decode_before_submit(wire,parsed,scope,lambda _:True)
except c.WireError as e:refused=e.code=='new_audio_video_blocked' and e.status==415 and e.no_dispatch_this_submission
check('AV_guard_refusal_before_admission',refused)
session=dict(account=scope,marker=17);cap=a.session_capabilities(session)
check('session_fields_no_mutation',session==dict(account=scope,marker=17) and cap['account']==scope and cap['marker']==17 and cap['transport']==c.capabilities())
check('page_identity_without_optin',a.encode_existing_page(raw,scope,'job1',0,None) is raw)
page=a.encode_existing_page(raw,scope,'job1',0,c.QUERY)
check('optin_page_exact',c.decode_page(page,scope,dict(kind='page',job_id='job1',after=0))==raw)
(R/'review_adapter_python.json').write_text(json.dumps(dict(status='PASS',checks=results,scope='Synthetic callback; no application auth/media implementation imported'),indent=2),encoding='utf-8')
print(json.dumps(dict(status='PASS',assertions=len(results))))
