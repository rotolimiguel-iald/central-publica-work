"""Pin final integration evidence and check unchanged accepted/production bytes."""
from pathlib import Path
import ast, datetime, hashlib, json, os
V=Path(__file__).resolve().parent;W=V.parent
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def save(p,value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    tmp=p.with_name('.report_tmp')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==raw;os.rename(tmp,p)
assembly=read(V/'ASSEMBLY_PROVENANCE_R1.json')
for row in assembly['files']:
    for k in ('source','copy'):assert pin(Path(row[k]['path']))==row[k],row[k]
core={p.name:pin(p)['sha256'] for p in (V/'staging/core_r2/lib/iald_memory').glob('*.py')}
assert all(pin(p)['sha256']==core[p.name] for p in (V/'staging/core/lib/iald_memory').glob('*.py'))
production=[]
def expected(p,sha,origin):
    actual=pin(Path(p));assert actual['sha256']==sha,(p,sha,actual)
    production.append({**actual,'baseline':origin})
for row in read(W/'tests_app/APP_SOURCE_BASELINE_R2.json')['files']:
    expected(row['source'],row['sha256'],'APP_SOURCE_BASELINE_R2')
for row in read(W/'NATIVE_BASELINE_R1.json')['sources']:
    expected(row['path'],row['sha256'],'NATIVE_BASELINE_R1')
for row in read(W/'tests_queue/QUEUE_BASELINE_R1.json')['files']:
    s=row['source'];expected(s['path'],s['sha256'],'QUEUE_BASELINE_R1')
for row in read(W/'tests_jev/J_BASELINE_R1.json')['files']:
    s=row['production_baseline'];expected(s['path'],s['sha256'],'J_BASELINE_R1')
science=read(W/'tests_jev/JEV_REAL_J_MEASUREMENT_R1.json')['science_manifest']
expected(science['path'],science['sha256'],'JEV_REAL_J_MEASUREMENT_R1')
wallet=[pin(p) for p in Path(r'C:\IALD\projetos_pyhton\IALD').glob('iald*wallet*.py')]
assert not any('wallet' in Path(r['copy']['path']).name for r in assembly['files'])
# Verify sensitive existing server policy functions were carried without AST edits.
def functions(p):
    return {n.name:ast.dump(n) for n in ast.walk(ast.parse(p.read_bytes())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
old=functions(Path(r'C:\IALD\projetos_pyhton\IALD\iald_web_server.py'))
new=functions(V/'staging/app/iald_web_server.py')
names=[n for n in old if any(t in n.lower() for t in ('wallet','consent','identificacao_json_post','chat_account_generation'))]
policy=[{'function':n,'unchanged_ast':old[n]==new.get(n)} for n in names]
assert all(x['unchanged_ast'] for x in policy if x['function']!='_api_post_with_wallet'),policy
old_tree=ast.parse(Path(r'C:\IALD\projetos_pyhton\IALD\iald_web_server.py').read_bytes())
wallet_node=next(n for n in ast.walk(old_tree) if isinstance(n,ast.FunctionDef) and n.name=='_api_post_with_wallet')
def global_compressor(node):
    return any(isinstance(x,ast.Attribute) and isinstance(x.value,ast.Name) and x.value.id=='HOLO_MEMORY' and x.attr=='compress_context' for x in ast.walk(node))
removed=[n for n in wallet_node.body if global_compressor(n)]
assert len(removed)==1 and isinstance(removed[0],ast.If)
wallet_node.body=[n for n in wallet_node.body if n not in removed]
assert ast.dump(wallet_node)==new['_api_post_with_wallet']
policy.append({'function':'_api_post_with_wallet','only_change':'Removed exactly the former global HOLO_MEMORY compression block; wallet/auth/billing statements otherwise AST-identical. Scoped N replacement separately tested.'})
save(V/'PRESERVATION_R1.json',{'status':'PASS','accepted_and_copied_files_unchanged':len(assembly['files']),
 'production_baselines':production,'wallet_source_pins_read_only':wallet,'server_policy_functions':policy,
 'science_manifest':science,'live_accounts_or_wallet_databases_read':False,
 'meaning':'Code and guarded writes checked; no assertion about private account database content. Scientific original not executed; contract/science reader verification performed locally by J tests.'})
processes=[]
for p in sorted((V/'process_receipts').glob('*.json')):
    d=read(p)
    for m in d['modules']:
        assert m['final_tree'] and m['sha256']==core[Path(m['path']).name],(p,m)
    assert set(d['denied'])<= {'socket.bind'},d
    processes.append({'receipt':pin(p),'pid':d['pid'],'argv':d['argv'],'core_modules':len(d['modules']),
                      'denied':d['denied'],'local_stdlib_socketpair':d.get('stdlib_loopback_socketpair',[])})
save(V/'PROCESS_CORE_PROVENANCE_R1.json',{'status':'PASS','core_expected':core,'processes':processes,
 'scope':'All completed instrumented Python processes which loaded iald_memory loaded final byte-identical modules, including fresh CLI/session/MCP children. Killed sandbox diagnostics are separate failed receipts.',
 'external_provider_calls':0,'production_writes':0,'socketpair_scope':'Windows asyncio internal local IPC only; no HTTP/socket connection to providers or existing services.'})
groups={k:read(V/('results_r2' if k=='native' else 'results')/(k+'_result.json')) for k in ('core','native','queue','app','jev')}
assert all(d['status']=='PASS' for d in groups.values())
assert {k:d['tests_run'] for k,d in groups.items()}=={'core':70,'native':20,'queue':44,'app':23,'jev':13}
mcp=read(V/'tests_queue/MCP_STDIO_RESULT_V3.json');assert mcp['verdict']=='PASS'
ids=[t for g in groups.values() for t in g['test_ids']]
categories={
 'steering_goal_and_stale_return':['steering','epoch_change','cancel_during','stale','premise_change'],
 'concurrency_and_single_dispatch':['writers','parallel','concurrent','single_use','no_repeat','no_resend'],
 'user_generation_conversation_partition':['scope','account','cross_context','isolation','generation'],
 'restart_cli_mcp_and_workers':['restart','fresh_cli','worker','recovery','checkpoint'],
 'poda_tetelestai_and_no_semantic_autoaccept':['tetelestai','settled','candidate','review_pending','human_review','pending_semantics'],
 'projection_integrity_and_lossless_overflow':['tamper','overflow','unknown','criteria','semantic_records','literal'],
 'return_custody_and_uncertainty':['partial','uncertain','raw_return','durable','utf8','sse'],
 'native_real_hooks_and_tools':['real_auto','real_worker','hooks','structured_media','counted'],
 'auth_csrf_and_authoritative_review':['auth','csrf','identity_or_stale','authority','bridge_rejects'],
 'jev_actual_100turn_context_single_send':['real_packets','single','timeout','boundary','unicode','invalid','long_header'],
 'legacy_queue_continuity':['migration_','legacy_and_partial','read_only_recovery'],
}
matrix=[{'criterion':name,'tests':[t for t in ids if any(term in t.lower() for term in terms)]} for name,terms in categories.items()]
assert all(x['tests'] for x in matrix)
save(V/'COVERAGE_MATRIX_R1.json',{'status':'REAL_LOCAL_TESTS','rows':matrix,'counts':{k:d['tests_run'] for k,d in groups.items()},
 'mcp_checks':mcp['checks'],'total_unique_unit_cases':170,'limits':['Provider transports simulated; native tokenizer endpoint simulated.',
 'Server functions extracted from final source; production server not started.',
 'No physical web/iOS/Android execution, mobile build, store publishing or production install.',
 'J admission is conservative escaped-byte policy, not exact tokenization; 25s HTTP timeout not tested against a live provider.',
 '100-turn fixtures reuse frozen C2 real private snapshots and actual routing contract; no user conversations or private account data.']})
evidence=[V/'ASSEMBLY_PROVENANCE_R1.json',V/'FIXTURE_REPAIR_R1.json',V/'MCP_GUARD_REPAIR_R1.json',
 V/'SOCKETPAIR_DIAGNOSTIC_R1.json',V/'PRESERVATION_R1.json',V/'PROCESS_CORE_PROVENANCE_R1.json',V/'COVERAGE_MATRIX_R1.json',
 V/'run_all.py',V/'run_suite.py',V/'run_suite_r2.py',V/'sitecustomize.py',V/'guard_r2/sitecustomize.py',V/'run_mcp_r3.py',
 V/'EXECUTIONS_R1.json',V/'native_execution_r2.json',V/'mcp_execution_r2.json',V/'mcp_execution_r3.json',
 V/'tests_queue/MCP_STDIO_RESULT_R4.json',V/'tests_queue/MCP_STDIO_RESULT_V2.json',V/'tests_queue/MCP_STDIO_RESULT_V3.json',
 W/'review_core_r2/C2_ACCEPTED_R1.json',W/'review_jev/J_ACCEPTED_R1.json',W/'tests_jev/JEV_REAL_J_MEASUREMENT_R1.json']
for k in groups:
    folder=V/('results_r2' if k=='native' else 'results');evidence.extend([folder/(k+'_result.json'),folder/(k+'_log.txt')])
report={'status':'DECLARADO','verification':'PASS_LOCAL_INTEGRATION','requirement':'V','requirement_satisfied':False,
 'actor':'codex-organism-integration-build','reference':str(W/'SESSION_REFERENCE.json'),
 'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'tree':str(V),'source_manifest':pin(V/'ASSEMBLY_PROVENANCE_R1.json'),
 'tests':{k:{f:d[f] for f in ('tests_run','seconds','failures','errors')} for k,d in groups.items()},
 'total_tests':170,'mcp_checks':len(mcp['checks']),'mcp_tool_count':mcp['tool_count'],
 'provider_calls':0,'production_installed':False,'requirement_acceptance':'Independent root review still required.',
 'repairs':'Only test assembly: baseline fixture, shorter Windows private path, MCP socketpair sandbox diagnosis. No accepted implementation changed. Initial failed evidence preserved.',
 'evidence':[pin(p) for p in evidence],
 'next_action':'Independent integrated review of V before any production installation plan.'}
save(V/'V_DELIVERY_R1.json',report)
print(json.dumps({'delivery':pin(V/'V_DELIVERY_R1.json'),'tests':170,'mcp_checks':len(mcp['checks']),'production_baselines':len(production),'processes':len(processes),'policy_functions':policy},ensure_ascii=False))
