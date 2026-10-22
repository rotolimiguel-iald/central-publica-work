"""Independent C2 review and technical acceptance only; no deployment."""
import datetime as dt,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parent;sys.path.insert(0,str(W))
from mission_io import call,save,pin
A={'kind':'agent','id':'codex-mission-memory-review'};ref=str(W/'SESSION_REFERENCE.json')
delivery=W/'CORE_C2_DELIVERY_R1.json';d=json.loads(delivery.read_bytes())
submission=W/'CORE_C2_SUBMITTED_R1.json';sub=json.loads(submission.read_bytes())
tests=json.loads((R/'C2_INDEPENDENT_TEST_RESULT_R1.json').read_bytes())
measures=json.loads((R/'C2_INDEPENDENT_MEASUREMENTS_R1.json').read_bytes())
assert tests['status']==measures['status']=='PASS' and tests['tests_run']==78
assert tests['failures']==tests['errors']==0
assert pin(delivery)==sub['delivery']
checked_pins=d['files']+d['evidence']+tests['test_pins']+[tests['log'],tests['freeze']]
checked_pins += [sub[k] for k in ('preflight','submit','completed_handle','final_projection')]
for x in checked_pins:assert pin(x['path'])==x
for x in measures['rows']:assert pin(x['snapshot']['path'])==x['snapshot']
p,pr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'c2_review_final_project')
t=next(x for x in p['projection']['active'] if x['id']=='C2')
assert t['status']=='review_pending' and t['submitted_by']==d['author'] and t['submitted_by']!=A['id']
assert t['evidence']==[pin(delivery)]
report=R/'C2_INDEPENDENT_REVIEW_R1.json'
save(report,{'schema':'organism-independent-review/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'C2','reviewer':A,'author':d['author'],
    'reference':pin(W/'SESSION_REFERENCE.json'),'review_revision':p['receipt']['revision'],
    'criterion':t['criterion'],'verdict':'PASS_WITH_SCOPE','requirement_satisfied':True,'findings':[],
    'delivery':pin(delivery),'submission':pin(submission),'source_pins':d['files'],'checked_artifact_pins':checked_pins,
    'independent_execution':pin(R/'C2_INDEPENDENT_TEST_RESULT_R1.json'),
    'independent_measurements':pin(R/'C2_INDEPENDENT_MEASUREMENTS_R1.json'),'project':pin(pr),
    'checks':[
      'Independent execution: 70 builder tests reproduced plus 8 adversarial tests, 78 PASS; source/baseline bytes checked before and after.',
      'AST comparison confirms only existing project changed and one private mechanical index helper added; lifecycle/CAS/accept methods unchanged.',
      'Exact completed request/intent schema, admission, artifact bytes, same context/epoch/submitter, final result/evidence and completed handles checked before indexing.',
      'Literal commands, general facts, corrections, criteria, note, evidence and review_evidence preserved; review_pending remains active. No execution completion promoted to acceptance.',
      'Missing/changed recognized pins and cross-context record rejected; failed/null/unknown/uncertain handles and extra semantic metadata kept full or refused visibly.',
      'Six pinned 1/10/100 pending/reviewed snapshots reprojected independently; original state unchanged, all mechanical-record and runtime-handle digests verified against complete exported snapshots.',
      'Overflow minimum reproduced exactly; API structured activity stays complete and compact projection hash remains distinct from MissionController CAS hash.'
    ],
    'measured_required_chars':[{k:x[k] for k in ('turns','reviewed_fixture','required_chars','baseline_required_chars','refused_24000')} for x in measures['rows']],
    'limits':[
      'C2 is mechanical projection correctness, not unbounded memory or a guarantee that genuine mandatory content fits a model window.',
      '100 pending/reviewed fixtures require143927/177894characters; both refuse24k. All100 commands and criteria persist; reviewed notes/evidence persist.',
      'Six-snapshot verification is pure projection of pinned archived snapshots with current artifact-byte verification; it does not claim historical get support.',
      'Reviewer actors in size fixtures are simulated and are not human approvals. This review/accept uses the actual distinct reviewer actor.',
      'JEV envelope policy is separate requirement J. Crossconsumer final integration belongs to V; installation/activation belongs to D. No production/provider call here.'
    ],'providers_called':0,'production_modified':False,'deployment_authorized_by_this_review':False})
# Refresh immediately before accept; no owner lease impersonation for review.
fresh,fr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'c2_accept_fresh_project')
current=next(x for x in fresh['projection']['active'] if x['id']=='C2')
assert current['status']=='review_pending' and current['criterion']==t['criterion'] and current['evidence']==t['evidence']
for x in checked_pins:assert pin(x['path'])==x
request={'operation':'accept','reference':ref,'actor':A,'task_id':'C2','event_id':'organism-C2-independent-accept-r1',
    'expected_revision':fresh['receipt']['revision'],'projection_sha256':fresh['projection_sha256'],
    'review_evidence':[pin(report)],'note':'Revisao independente PASS: 78 testes executados e 6 medidas conferidas. Compactacao apenas mecanica; overflow obrigatorio permanece. V/D separados.'}
save(R/'C2_ACCEPT_REQUEST_R1.json',request)
result,ar=call('mission_cli.py',request,'c2_independent_accept')
final,fp=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'c2_accepted_final_project')
settled=next(x for x in final['projection']['settled'] if x['id']=='C2')
assert settled['status']=='satisfied' and settled['reviewed_by']==A['id']
out=R/'C2_ACCEPTED_R1.json'
save(out,{'requirement':'C2','actor':A,'reference':ref,'revision':final['receipt']['revision'],'status':settled['status'],
    'review':pin(report),'request':pin(R/'C2_ACCEPT_REQUEST_R1.json'),'fresh_project':pin(fr),'accept_receipt':pin(ar),
    'final_project':pin(fp),'V_ready':next(x for x in final['projection']['active'] if x['id']=='V')['ready'],'installed':False})
print(json.dumps({'review':pin(report),'acceptance':pin(out),'revision':final['receipt']['revision'],
    'V_ready':next(x for x in final['projection']['active'] if x['id']=='V')['ready']},ensure_ascii=False))
