"""Freeze measured Q delivery/installation inputs; no production writes."""
import ast,datetime as dt,hashlib,importlib.util,json
from pathlib import Path
W=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('q_delivery_io',W/'mission_io.py');io=importlib.util.module_from_spec(s);s.loader.exec_module(io)
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
A={'id':'codex-organism-queue-build','kind':'agent'}
def sized(p):return dict(io.pin(p),bytes=Path(p).stat().st_size)
baseline=json.loads((W/'tests_queue/QUEUE_BASELINE_R1.json').read_bytes())
tests=json.loads((W/'tests_queue/QUEUE_TEST_RESULT_R3.json').read_bytes())
mcp=json.loads((W/'tests_queue/MCP_STDIO_RESULT_R4.json').read_bytes())
assert tests['verdict']==mcp['verdict']=='PASS'
assert tests['tests_run']==29 and tests['failures']==tests['errors']==0
for item in baseline['files']:assert sized(item['source']['path'])==item['source']
for item in baseline['core']:assert sized(item['path'])==item
for item in tests['sources']:assert sized(item['path'])==item
old={x['source']['path']:x['source'] for x in baseline['files']}
destinations=[]
for p in (W/'staging/queue/r2').rglob('*.py'):
    dst=B/p.relative_to(W/'staging/queue/r2')
    if str(dst) in old and sized(p)['sha256']==old[str(dst)]['sha256']:continue
    destinations.append((p,dst))
destinations.extend([(W/'staging/sessions/queue_activity_session.py',B/'queue_activity_session.py'),
                     (W/'staging/bench_wrapper/bench_activity_cli.py',B/'bench_activity_cli.py')])
assert len(destinations)==10,len(destinations)
entries=[]
for source,destination in destinations:
    ast.parse(source.read_text(encoding='utf-8'),filename=str(source))
    if str(destination) in old:
        before={'exists':True,**old[str(destination)]}
    else:
        assert not destination.exists(),str(destination)
        before={'exists':False,'path':str(destination),'sha256':None,'bytes':None}
    entries.append({'source':sized(source),'destination':str(destination),'baseline':before})
plan={'schema':'organism-Q-file-plan/v1','author':A,'files':entries,
      'baseline':io.pin(W/'tests_queue/QUEUE_BASELINE_R1.json'),
      'required_core':baseline['core'],'installed':False,
      'scope':'Only changed/new source files. 33 fixture copies are NOT an installation list. No Bancada destination.'}
plan_path=W/'tests_queue/QUEUE_INSTALL_PLAN_R2.json';io.save(plan_path,plan)
fresh,project_path=io.call('mission_cli.py',{'operation':'project','reference':str(W/'SESSION_REFERENCE.json'),'actor':A,'max_chars':125000},'queue_delivery_project')
t=next(x for x in fresh['projection']['active'] if x['id']=='Q')
assert t['status']=='working' and t['lease']['owner']==A['id']
checked,check_path=io.call('mission_cli.py',{'operation':'check','reference':str(W/'SESSION_REFERENCE.json'),'actor':A,'task_id':'Q','lease_id':t['lease']['id'],'expected_revision':fresh['receipt']['revision'],'projection_sha256':fresh['projection_sha256']},'queue_delivery_check')
delivery={
    'schema':'organism-Q-delivery/v2','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'Q','author':A,
    'status':'DECLARADO_CANDIDATE_FOR_INDEPENDENT_REVIEW','requirement_satisfied':False,
    'reference':io.pin(W/'SESSION_REFERENCE.json'),'revision':fresh['receipt']['revision'],
    'criterion':t['criterion'],'lease':t['lease'],'project':io.pin(project_path),'preflight':io.pin(check_path),
    'installation_plan':io.pin(plan_path),'api':io.pin(W/'tests_queue/QUEUE_ACTIVITY_API_R2.txt'),
    'tests':io.pin(W/'tests_queue/QUEUE_TEST_RESULT_R3.json'),'mcp_stdio':io.pin(W/'tests_queue/MCP_STDIO_RESULT_R4.json'),
    'superseded_delivery':io.pin(W/'tests_queue/QUEUE_DELIVERY_R1.json'),
    'material_fix':'R1 raw_return required current binding before custody. R2 separates immutable admission identity from freshness; prompt/constraints/binding mutation during provider preserves whole return and refuses integration/retry.',
    'previous_test_receipts_preserved':[io.pin(W/'tests_queue/QUEUE_TEST_RESULT_R1.json'),io.pin(W/'tests_queue/MCP_STDIO_RESULT_R1.json'),io.pin(W/'tests_queue/MCP_STDIO_RESULT_R2.json')],
    'test_summary':{'tests':29,'failures':0,'errors':0,'seconds':tests['seconds'],'mcp_checks':len(mcp['checks']),'mcp_tools':mcp['tool_count'],'new_mcp_tools':len(mcp['new_tools'])},
    'core_reuse':{'acceptance':io.pin(W/'review_core/C_ACCEPTED_R1.json'),'pins':baseline['core'],'unchanged':True},
    'production_bench_proxy_unchanged':sized(Path(r'C:\IALD\Bancada_Um\mcp_um.py')),
    'changes':[
      'New queue entities bind Activity to original request/context and explicit IALD/operator scope; children validate parent job, exact prepared prompt and deterministic execution UUID in server ledger.',
      'Provider/Work stages use durable operation-specific intents, post-intent projection and live validation. Existing provider constraints/generation/scientific guards remain in force.',
      'Whole returns are durable before freshness, cancellation, accounting or shadow; scientific premise changes hold the context before integration. Reconciliation is local, never remote retry or acceptance.',
      'Legacy/partial queued entities preserve state and ordering and require explicit migration/admission recovery; existing local cancellations remain available.',
      'CLI/MCP/session tools expose exact ledger IDs and shared project/recover/reconcile, no model-selected actor/path/reviewer. All entrypoints use recover=False.',
      'External Bancada wrapper pins admitted body/action, uses existing loopback routes without modifying calculation/book/guards, preserves asynchronous IDs and unknown outcomes; explicit GET observation does not repeat POST.'
    ],
    'scope_limits':[
      'Trusted local OS/server authentication boundary. App user identity is never inferred from legacy operator; cross-account app delegation needs its authenticated adapter.',
      'Tests use real local queue/coordination/ACOM/Activity/SQLite and subprocess CLI/MCP; canonical packet, model transports and HTTP are inert. No live provider/science verification.',
      'Existing long-lived MCP/worker sessions are NOT reloaded by source-on-disk changes. No process was killed except the private smoke process after its timeout; no production process instantiated for health.',
      'First sandbox stdio timeout preserved. R2 harness also corrected expected legacy tool names to those in source; final R4 reran actual R2 code outside sandbox for asyncio IPC, with HTTP/provider disabled.',
      'Direct Bancada MCP and unlisted endpoints remain legacy; wrapper covers estado/avaliar/ajustar/comparar/amostrar and fixed returned task GET only. No restart or hidden redirect of old clients.',
      'Projection capacity is explicit and may refuse mandatory data; artifacts/journal grow. Independent V and deployment D remain separate. No semantic/scientific autoaccept.'
    ],
    'production_writes':0,'provider_calls':0,'real_bench_calls':0,'science_builds':0,'installed':False,
    'other_agents_sources_untouched':True,'core_sources_unchanged':True,
    'availability':{'queue_cli':'candidate tested in fresh private process','mcp':'candidate stdio tested, old processes not changed','sessions':'same queue envelope through new local adapter','bench_wrapper':'external candidate; fake HTTP verified','production':'not installed'}
}
path=W/'tests_queue/QUEUE_DELIVERY_R2.json';io.save(path,delivery)
print(json.dumps({'delivery':sized(path),'plan':sized(plan_path),'revision':fresh['receipt']['revision'],'files':len(entries)},ensure_ascii=False,indent=2))
