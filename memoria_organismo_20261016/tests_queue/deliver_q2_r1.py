"""Freeze Q2 candidate/source manifest; never migrate production or install."""
import ast,datetime as dt,json,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W))
from mission_io import call,save,pin
A={'id':'codex-organism-legacy-migration-build','kind':'agent'};ref=str(W/'SESSION_REFERENCE.json')
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
tests=W/'tests_queue/Q2_TEST_RESULT_R2.json';t=json.loads(tests.read_bytes())
assert t['verdict']=='PASS' and t['tests_run']==44 and t['failures']==t['errors']==0
for x in t['sources']+t['core_pins']:assert pin(x['path'])=={k:x[k] for k in ('path','sha256')}
qplan=json.loads((W/'tests_queue/QUEUE_INSTALL_PLAN_R2.json').read_bytes())
for x in qplan['files']:assert pin(x['source']['path'])=={k:x['source'][k] for k in ('path','sha256')}
entries=[]
for relative in ['iald_orchestrator/legacy_activity_migration.py','queue_activity_migrate.py']:
    source=W/'staging/queue/r3'/relative;destination=B/relative
    assert not destination.exists();ast.parse(source.read_text(encoding='utf-8'))
    entries.append({'source':dict(pin(source),bytes=source.stat().st_size),'destination':str(destination),
                    'baseline':{'exists':False,'path':str(destination),'sha256':None,'bytes':None}})
plan=W/'tests_queue/Q2_INSTALL_PLAN_R1.json'
save(plan,{'schema':'organism-Q2-file-plan/v1','author':A,'files':entries,'parent_plan':pin(W/'tests_queue/QUEUE_INSTALL_PLAN_R2.json'),
    'core_pins':t['core_pins'],'installed':False,'scope':'Two additive files only. Q R2/MCP/session/Bancada sources unchanged.'})
p,pr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'q2_delivery_project')
task=next(x for x in p['projection']['active'] if x['id']=='Q2')
assert task['status']=='working' and task['lease']['owner']==A['id']
_,ck=call('mission_cli.py',{'operation':'check','reference':ref,'actor':A,'task_id':'Q2','lease_id':task['lease']['id'],
    'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']},'q2_delivery_check')
out=W/'tests_queue/Q2_DELIVERY_R1.json'
save(out,{'schema':'organism-Q2-delivery/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'Q2','author':A,'reference':pin(W/'SESSION_REFERENCE.json'),
    'status':'DECLARADO_CANDIDATE_FOR_INDEPENDENT_REVIEW','requirement_satisfied':False,
    'criterion':task['criterion'],'revision':p['receipt']['revision'],'lease':task['lease'],
    'project':pin(pr),'preflight':pin(ck),'installation_plan':pin(plan),
    'implementation':[pin(x['source']['path']) for x in entries],'api':pin(W/'tests_queue/LEGACY_MIGRATION_API_R1.txt'),
    'tests':pin(tests),'summary':{k:t[k] for k in ['tests_run','new_tests','regression_tests','seconds','failures','errors']},
    'prior_failed_test':pin(W/'tests_queue/Q2_TEST_RESULT_R1.json'),
    'test_erratum':'First run: 41/42 passed; refusal fixture exceeded existing five-pending-job limit before reaching its assertions. New fixture closes each rejected private row between cases; no production/controller relaxation.',
    'compatibility':{'Q_R2_unchanged':True,'MCP_unchanged':True,'core_used':t['core_pins'],'C2_final_required_in_V':True},
    'limits':['Existing explicit IALD/operator scope; OS-authenticated privileged local CLI, no model tool or arbitrary identity/evidence path.',
      'Only never-dispatched legacy coordination stages with exact original ACOM context. Unsafe/history-bearing jobs remain visibly refused.',
      'No global transaction across queue and ACOM: per-write durable intents + exact idempotent replay bridge crashes; concurrent external revisions refuse without rebasing.',
      'Semantic job fields/supplement remain byte-identical; version increments once, activity_version enabled only after ACOM receipt/check. Later dispatch keeps existing authorizations/guards.',
      'Provider, HTTP and canonical package are inert fixtures. Real private SQLite/Activity/ACOM and fresh CLI tested; no real legacy request migrated.',
      'Source-on-disk changes do not reload existing processes. Installation/activation/independent V remain separate.'],
    'production_migrations':0,'provider_calls':0,'worker_starts_by_migration':0,'installed':False,'accepted':False})
print(json.dumps({'delivery':pin(out),'plan':pin(plan),'revision':p['receipt']['revision'],'files':len(entries)},ensure_ascii=False))
