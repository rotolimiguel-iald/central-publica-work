import ast,hashlib,json,sqlite3,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;LIVE=Path('C:/IALD/projetos_pyhton/IALD')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
s=json.loads((HERE/'SCOPED_ACOM_INPUT.json').read_text());owner=s['scope']['principal']
job='cfe3165d-67b3-4e1e-bbb9-ac906080ec71'
path=LIVE/'.iald_runtime/monthly_wallet/wallet.sqlite3'
with sqlite3.connect(path.as_uri()+'?mode=ro',uri=True) as db:
    db.row_factory=sqlite3.Row
    calls=[dict(r) for r in db.execute('SELECT event_id,provider,model,status,cap FROM calls WHERE owner=? AND task_id=?',(owner,job))]
    entries=[dict(r) for r in db.execute("SELECT event_id,provider,model,cost_status,delta FROM entries WHERE owner=? AND task_id=? AND kind='cost'",(owner,job))]
ledger=dict(exact_owner_task_filter=True,task_id=job,calls=calls,cost_entries=entries,
            note='Calls are ledger admission receipts, not by themselves proof of network dispatch. Received scoped transport below proves one JEV response.')
(HERE/'SCOPED_LEDGER_RECEIPT.json').write_text(json.dumps(ledger,indent=2),encoding='utf-8')
r=subprocess.run([sys.executable,'-X','utf8',str(HERE/'test_followup.py')],capture_output=True)
(HERE/'TEST_RESULTS.txt').write_bytes(r.stdout+r.stderr);assert r.returncode==0
wirepath=Path('C:/IALD/MEMORIA_IALD/state/activity_artifacts/532f6902924d86e0f05a798a334bee442cc0a3d416788d17c3f7a3fc2cefe973.json')
w=json.loads(wirepath.read_text());response=json.loads(w['payload']['wire_utf8'])
assert w['context_id']==s['context_id'] and w['scope']==s['scope']
assert pin(wirepath)['sha256']==wirepath.stem
base=json.loads((HERE/'FIX_BASELINE.json').read_text())
assert pin(LIVE/'iald_web_server.py')['sha256']==base['sha256']
def defs(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_bytes()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
old=defs(LIVE/'iald_web_server.py');new=defs(HERE/'iald_web_server.py')
changed=[k for k in old if old[k]!=new.get(k)]
assert set(changed)=={'_chat_automatico_autorizado','_chat_avaliacao'}
report=dict(status='REPRODUCED_DIAGNOSTIC_FIX_STAGED_NOT_INSTALLED',job_id=job,context_id=s['context_id'],
    root_exception_class='BudgetRefusal',sanitized_reason='MEDIA_POLICY_CONFIDENCE_BELOW_REQUIRED_THRESHOLD',
    source_reason='Uncertain media policy; no automatic quality substitution',confidence=.68,required_confidence=.70,
    capacity_overflow=False,full_public_science_preserved=True,
    actual_dispatch_evidence=dict(confirmed_received_JEV_responses=1,usage=response['usage'],estimated_JEV_cost_usd=response['usage']['input_tokens']*.042/1000000,
        transport=pin(wirepath),http_status=200,MiMo_received_responses_in_scoped_ACOM=0,
        caution='No MiMo result handle in this scope. Historical dispatch absence is not independently proven solely by SSE; ledger receipt contains exact job entries. No claim of zero cost.'),
    ledger=pin(HERE/'SCOPED_LEDGER_RECEIPT.json'),tests=dict(passed=2,output=pin(HERE/'TEST_RESULTS.txt')),
    patch_scope='Classify uncertain policy separately; sanitize other failures, say selector may have been called. Preserve .70 gate, source input, full science, no retry/fallback or automatic quality substitution. This corrects diagnosis, does not authorize the refused decision.',
    changed_functions=changed,source=pin(HERE/'iald_web_server.py'),baseline_sha256=base['sha256'],
    evidence=[pin(HERE/n) for n in ('test_followup.py','SCOPED_JOB_METADATA.json','SCOPED_ACOM_INPUT.json','diagnostic.patch')],
    new_network_calls=0,new_provider_calls=0,runtime_writes=0,installed=False)
(HERE/'DIAGNOSIS_FIX_RECEIPT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(receipt=pin(HERE/'DIAGNOSIS_FIX_RECEIPT.json'),source=report['source'],ledger=ledger,changed=changed)))
