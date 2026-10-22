from pathlib import Path
import hashlib,json
V=Path(__file__).resolve().parent;W=V.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
tests=json.loads((V/'independent_final_tests.json').read_bytes())
pins=json.loads((V/'independent_final_inputpins.json').read_bytes())
drift=[p for p,v in pins.items() if sha(Path(p).read_bytes())!=v['sha256']]
assert not drift,drift
assert tests['plan_sha256']==sha((W/'install_plan.json').read_bytes())
assert tests['findings'] and any(f['severity']=='MEDIO' for f in tests['findings'])
findings=tests['findings'];findings[0]['line']=116
names=['ORIGEM_FINAL_REVIEW.txt','independent_final_audit.py','independent_final_inputpins.json',
 'independent_final_tests.json','independent_integration_output.txt','transaction_race_reproduction.json',
 'transaction_additional_tests.py','transaction_additional_tests.json','routing_main_review.json','final_checks.json']
report={'status':'CHANGES_REQUIRED','reviewer':'codex-science-review',
 'reviewed_plan_sha256':tests['plan_sha256'],
 'authorization':'NO_INSTALLATION_APPROVAL; no PASS/plan_sha256 gate issued',
 'scope':'Independent review of scientific compact, JEV binding, integration, adaptive output, transaction and plan; own routing excluded',
 'findings':findings,
 'passed':{
   'files_hash_baseline_checked':1257,'shared_prefix_bytes':626307,'shared_topics':411,
   'compact_reproduced_byte_exact':True,'shared_native_count_receipt':314674,'full_native_count_receipt':648972,
   'counts_scope':'Existing pinned Anthropic receipts, not fresh counts and not native DeepSeek/Kimi counts',
   'JEV_validate_contract_and_loader':True,'JEV_source_anchors':3,
   'integration_tests_rerun':9,'adaptive_output_boundary_cases':14,'output_maximum':393216,'output_floor':16384,
   'input_truncated':False,'overflow_refused_before_credentials_or_network':True,
   'transaction_baseline_source_conflict_and_rollback_tests':3,
   'privacy':'No private Atlas input in reproduced compact; ACOM/tools remain host-scoped; no credential files read; no provider calls',
   'routing':'PASS from main, file hashes checked against routing_main_review.json; not re-audited by its author'},
 'limitations':['Historical scientific details remain recoverable references, not all literal context.',
   'JSON UTF-8 byte admission is a conservative proxy; provider-specific tokenization not measured here.',
   'Transaction race reproduced only in isolated fixture; production untouched.',
   'App store state is excluded from this backend plan review.'],
 'artifacts':[{'path':str(V/n),'sha256':sha((V/n).read_bytes())} for n in names],
 'deployment_performed':False,'network_calls':0}
out=V/'review_final.json';assert not out.exists();out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'status':report['status'],'finding':'TX-01 MEDIO','reviewed_plan_sha256':report['reviewed_plan_sha256']}))
