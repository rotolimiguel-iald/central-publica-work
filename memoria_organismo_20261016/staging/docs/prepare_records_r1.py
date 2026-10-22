"""Prepare documentation records and append plan only; never mutate canonical memory."""
from pathlib import Path
import datetime,hashlib,json,os,sys
D=Path(__file__).resolve().parent;W=D.parents[1]
sys.path.insert(0,str(W))
from mission_io import project,save,pin
x,projection=project()
task=next(t for t in x['projection']['active'] if t['id']=='M')
event_path=Path(r'C:\IALD\PROGRAMA_IALD\eventos.jsonl')
with event_path.open('rb') as f:
    for line in f:
        event=json.loads(line)
        if event.get('seq')==930:break
    else:raise AssertionError('Claim930 not found')
assert event['tipo']=='reivindicar' and event['dados']['unidade']=='F9.MEMORIA_ORGANISMO_20261016'
claim={'path':str(event_path),'seq':930,'exact_line_sha256':hashlib.sha256(line).hexdigest(),'event':event}
save(D/'CLAIM_930_SOURCE_R1.json',claim)
C=Path(r'C:\IALD\Central de Patentes');CM=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
surfaces=[
 ('instruction',Path(r'C:\Users\rotol\.codex\AGENTS.md'),'Short operational rule and protocol pointer; no diary.'),
 ('instruction',Path(r'C:\Users\rotol\.claude\CLAUDE.md'),'Short operational rule and protocol pointer.'),
 ('native_instruction',Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'),'Same runtime/API and deployment limits for app/native.'),
 ('diary',C/'memory/DIARIO_CONSTRUCAO_QG.md','Dated operational delivery, evidence and independent review; no new scientific claim.'),
 ('atlas',C/'memory/TGL_ATLAS.md','Dated additive entry in update register; adaptation is software control, not physical proof.'),
 ('index',C/'memory/TGL_INDICE_VIVO.md','Short route to exact reference, protocol and final delivery.'),
 ('management',C/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md','Delivery/limits for management; no self-AUDITADA/FECHADA.'),
 ('claude_diary',CM/'MEMORY_2.md','Dated diary; preserve all previous bytes.'),
 ('readme',Path(r'C:\IALD\MEMORIA_IALD\README.md'),'Add direct pointer to ACTIVITY_PROTOCOL.md and distinctions installation/loading.'),
 ('mission_protocol',Path(r'C:\IALD\MEMORIA_IALD\MISSION_PROTOCOL.md'),'Add ActivityRuntime/C2 protocol, uncertainty, no automatic semantic acceptance.'),
]
rows=[]
for kind,p,purpose in surfaces:
    assert p.is_file(),str(p)
    rows.append({'kind':kind,'path':str(p),'baseline':pin(p),'bytes':p.stat().st_size,
                 'operation':'append_only_after_fresh_baseline','purpose':purpose})
index=CM/'MEMORY.md';assert index.is_file()
evidence_paths=[W/'validation_final/V_ACCEPTED_R1.json',W/'validation_final/V_ROOT_REVIEW_R1.json',
 W/'validation_final/V_DELIVERY_R1.json',W/'validation_final/COVERAGE_MATRIX_R1.json',
 W/'review_core_r2/C2_ACCEPTED_R1.json',W/'CORE_C2_DELIVERY_R1.json',
 W/'review_jev/J_ACCEPTED_R1.json',W/'tests_jev/J_DELIVERY_R1.json',
 W/'tests_jev/JEV_REAL_J_MEASUREMENT_R1.json',W/'tests_jev/PRIMARY_DOCS_R1.json',
 W/'review_queue/Q2_ACCEPTED_R1.json',W/'APP_DELIVERY_R1.json',W/'NATIVE_DELIVERY_R1.json',
 W/'ACTIVITY_API_R1.txt',W/'ACTIVITY_API_C2_R1.txt',
 W/'staging/core_r2/lib/iald_memory/activity.py',W/'staging/queue/r3/iald_orchestrator/activity_bridge.py',
 W/'staging/sessions/queue_activity_session.py',W/'staging/bench_wrapper/bench_activity_cli.py',
 W/'staging/app/iald_activity_ui.py']
evidence=[pin(p) for p in evidence_paths]
plan={'status':'DECLARADO_PLAN_NOT_APPLIED','requirement':'M','reference':str(W/'SESSION_REFERENCE.json'),
 'revision':x['receipt']['revision'],'criterion':task['criterion'],'depends_on':task['depends_on'],
 'claim':pin(D/'CLAIM_930_SOURCE_R1.json'),'actor':'codex-organism-docs-preparation',
 'primary_surface_count':8,'additional_protocol_surface_count':2,'surfaces':rows,
 'conditional_index':{'path':str(index),'baseline':pin(index),'bytes':index.stat().st_size,
   'operation':'Append only one short pointer if needed and if 24KiB budget permits; diary stays in MEMORY_2.md. Do not truncate existing index.',
   'counted_in_primary_eight':False},
 'new_document':{'candidate':pin(D/'ACTIVITY_PROTOCOL_R1.md'),'intended_path':r'C:\IALD\MEMORIA_IALD\ACTIVITY_PROTOCOL.md',
   'operation':'Create exclusively after review; if path already exists, stop and prepare an additive version, never overwrite by assumption.'},
 'before_apply':['Fresh project exact reference; verify D evidence and M claim/check under actual owner.',
   'Recheck claim930 expiry/owner and exact notes; revalidate every target baseline against concurrent edits.',
   'Finalize deployment/mobile/auth/Apple matrix using actual D receipts; do not convert this staging preparation into installation evidence.',
   'Review append text and measured source pins independently; retain earlier artifacts.'],
 'append_transaction':['For each existing memory, read bytes once, save immediate same-folder .bak_YYYYMMDD_HHMMSS_microseconds with exclusive create, fsync and verify exact bytes/hash.',
   'Prepare old_bytes + dated UTF8 append preserving existing line-ending convention and all old bytes; marker must be absent.',
   'Write same-folder temporary, fsync, verify prefix/size/hash; recheck original still equals baseline, then atomic replace.',
   'Verify new file equals prepared bytes and grows by exactly append length; on failure stop visibly and preserve backups/receipts. Restore only the owned failed mutation, without overwriting concurrent work.',
   'Record per-target before/after/backup hashes, sizes, marker count and timestamp. Never delete backups.'],
 'additional_operational_updates':[
   {'surface':r'C:\IALD\MAPA_DE_ROTAS','method':'Existing rotas.py registrar with a new measured delivery entry; do not edit ledger files directly.'},
   {'surface':r'C:\IALD\PROGRAMA_IALD','method':'Existing iald.py avancar for F9.MEMORIA_ORGANISMO_20261016, ENTREGUE with final evidence; AUDITADA/FECHADA belongs to management.'},
   {'surface':'ACOM exact SESSION_REFERENCE.json','method':'Fresh CAS, material conclusion source and DECLARADO/REAL scope; reconcile only owned handles. M submit and distinct real review; no automatic accept.'}],
 'exclusions':['No append applied here; no board/map write, production update or requirement acceptance.',
   'No science/kernel/gate/acervo change. Physical-device decision remains separate from operational memory.',
   'Previous app-specific HANDOFF/mobile files are not silently substituted for the eight claim930 surfaces.'],
 'evidence':evidence}
save(D/'MEMORY_APPEND_PLAN_R1.json',plan)
record={'status':'DECLARADO_DOCUMENTATION_CANDIDATE','requirement':'M','requirement_satisfied':False,
 'reference':str(W/'SESSION_REFERENCE.json'),'revision':x['receipt']['revision'],'current_M_status':task['status'],
 'prepared_by':'codex-organism-docs-preparation','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'project':pin(projection),'document':pin(D/'ACTIVITY_PROTOCOL_R1.md'),'append_plan':pin(D/'MEMORY_APPEND_PLAN_R1.json'),
 'claim_source':pin(D/'CLAIM_930_SOURCE_R1.json'),'evidence':evidence,
 'limits':['M depends on D; this is authorized preparation only, no M claim, submit or accept.',
           'D live authenticated app, Apple/mobile availability and actual loaded-process evidence must be read fresh before final memory entry.',
           '170 integration tests and 100-turn measurements are local/synthetic; no inference call claimed.'],
 'memory_writes':0,'production_writes':0,'providers_called':0}
save(D/'ACTIVITY_PROTOCOL_RECORD_R1.json',record)
print(json.dumps({'revision':x['receipt']['revision'],'document':record['document'],'record':pin(D/'ACTIVITY_PROTOCOL_RECORD_R1.json'),
 'plan':record['append_plan'],'surfaces':len(rows),'conditional_index_bytes':index.stat().st_size},ensure_ascii=False))
