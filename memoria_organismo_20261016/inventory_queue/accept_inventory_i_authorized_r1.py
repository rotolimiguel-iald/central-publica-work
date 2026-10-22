"""Only I acceptance, with newly verified explicit human authorization."""
from pathlib import Path
import importlib.util, json
W=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('i_accept_authorized_io',W/'mission_io.py')
io=importlib.util.module_from_spec(spec);spec.loader.exec_module(io)
A={'id':'codex-mission-memory-review','kind':'agent'}
ref=W/'SESSION_REFERENCE.json'
authorization=W/'I_HUMAN_AUTHORIZATION_VERIFIED_R1.json'
auth=json.loads(authorization.read_bytes())
assert auth['source_tool']=='mcp__codex_app__read_thread'
assert auth['thread_id']=='01a11878-6e36-7d10-83c4-cd72e757fdd0'
assert auth['user_message_id']=='01a146ef-2834-7092-8237-107151b7b251'
assert auth['user_text']=='Aceito. Prossiga'

def project(label):
 return io.call('mission_cli.py',{'operation':'project','reference':str(ref),'actor':A,'max_chars':125000},label)

fresh,before_path=project('I_accept_human_authorized_fresh')
t=next(x for x in fresh['projection']['active']+fresh['projection']['settled'] if x['id']=='I')
review=W/'REVIEW_INVENTORY_I_R1.json'
review_doc=json.loads(review.read_bytes())
assert review_doc['verdict']=='PASS_INVENTORY_AND_COMMON_CONTRACT'
assert review_doc['criterion']==t['criterion']
assert review_doc['reviewer']==A
for item in review_doc['evidence']:
 assert io.pin(item['path'])=={'path':item['path'],'sha256':item['sha256']}
assert {(x['path'],x['sha256']) for x in review_doc['evidence']}=={(x['path'],x['sha256']) for x in t['evidence']}
old=json.loads((W/'I_ACCEPT_REQUEST_R1.json').read_bytes())
assert old['review_evidence']==[io.pin(review)]
if t['status']=='satisfied':
 assert t['reviewed_by']==A['id'] and t['review_evidence']==old['review_evidence']
 result={'already_applied':True,'receipt':fresh['receipt']};accepted_path=before_path
else:
 assert t['status']=='review_pending' and t['submitted_by']!=A['id']
 request={**old,'expected_revision':fresh['receipt']['revision'],'projection_sha256':fresh['projection_sha256'],
  'event_id':'organism-I-human-authorized-independent-accept-r1',
  'note':'Aceite técnico independente do inventário I, autorizado pela mensagem humana 01a146ef-2834-7092-8237-107151b7b251 (Aceito. Prossiga), verificada pela ferramenta oficial. Implementação/testes/implantação continuam pendentes.'}
 io.save(W/'I_ACCEPT_REQUEST_AUTHORIZED_R1.json',request)
 result,accepted_path=io.call('mission_cli.py',request,'I_accept_human_authorized')
after,after_path=project('I_accept_human_authorized_verify')
row=next(x for x in after['projection']['settled'] if x['id']=='I')
assert row['status']=='satisfied' and row['reviewed_by']==A['id']
assert row['review_evidence']==[io.pin(review)]
def others(v):
 return {x['id']:{k:x[k] for k in ['status','epoch','criterion','depends_on','evidence','review_evidence','lease']}
  for x in v['projection']['active']+v['projection']['settled'] if x['id']!='I'}
assert others(fresh)==others(after)
assert fresh['projection']['flow']==after['projection']['flow']
c=next(x for x in after['projection']['active'] if x['id']=='C')
assert c['status']=='open' and c['ready'] is True
receipt={'schema':'organism-I-authorized-accept/v1','actor':A,'reference':io.pin(ref),
 'human_authorization':io.pin(authorization),'review':io.pin(review),
 'previous_refusal_preserved':io.pin(W/'I_ACCEPT_BLOCKED_R1.json'),
 'before':io.pin(before_path),'accept_receipt':io.pin(accepted_path),'after':io.pin(after_path),
 'transition_result':result,'revision_before':fresh['receipt']['revision'],
 'revision_after':after['receipt']['revision'],'I_status':row['status'],'reviewer':row['reviewed_by'],
 'other_requirements_unchanged':True,'flow_handles_unchanged':True,
 'C_status':c['status'],'C_ready':c['ready'],'tetelestai':after['projection']['tetelestai'],
 'scope':'Somente aceite I; nenhum outro aceite, claim, instalação ou chamada de provedor.'}
io.save(W/'I_ACCEPTED_R1.json',receipt)
print(json.dumps({'receipt':io.pin(W/'I_ACCEPTED_R1.json'),'revision_before':receipt['revision_before'],
 'revision_after':receipt['revision_after'],'I_status':receipt['I_status'],'C_ready':True},ensure_ascii=False,indent=2))
