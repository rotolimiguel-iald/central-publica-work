"""One authorized job; local readonly replay, fake credential/wallet/HTTP boundary."""
import ast,base64,hashlib,importlib.util,json,sqlite3,sys,threading,types,zlib,io,wave
from pathlib import Path
W=Path(__file__).resolve().parent;P=W.parent;R=Path('C:/IALD/projetos_pyhton/IALD');M=Path('C:/IALD/MEMORIA_IALD/state')
sys.path[:0]=[str(R),str(P/'backend_stage'),str(P/'routing_stage')]
import capture_manual_audio as cap
import private_media_store as private
import iald_mimo_multimodal as media

def sha(b):return hashlib.sha256(b).hexdigest()
def ro(path):
 d=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True);d.row_factory=sqlite3.Row;d.execute('PRAGMA query_only=ON');return d
c=json.loads((W/'MANUAL_AUDIO_RESULT.json').read_bytes());job=c['job']['id'];conversation=c['job']['conversation_id'];principal=c['acom']['activity_handles'][0].get('principal')
with ro(M/'memory.sqlite3') as d:
 row=d.execute('select objective_blob,objective_sha256,scope_json from contexts where context_id=?',(c['acom']['context_id'],)).fetchone()
 rawobjective=zlib.decompress(row['objective_blob']);assert sha(rawobjective)==row['objective_sha256'];scopejson=json.loads(row['scope_json'])
content=json.loads(rawobjective);parts=[p for p in content if p.get('type')=='iald_media'];assert len(parts)==1
part=parts[0];scope=private.Scope('luiz',scopejson['principal'],conversation)
# Existing read methods, readonly DB override; constructor never runs (no recovery/mkdir/write).
store=private.PrivateMediaStore.__new__(private.PrivateMediaStore)
store.db_path=R/'.iald_runtime/private_media/media.sqlite3';store.blobs=store.db_path.parent/'blobs';store.authorize_scope=lambda s:s==scope;store.cipher=cap.cipher
import time
store.clock=time.time;store._db=lambda:ro(store.db_path)
audio,metadata=store.read(part['media_ref'],scope,part['sha256']);assert metadata==part
fact=media.validate_upload(audio,part['mime']);assert fact['duration_seconds']==120
# Load test harness definitions only; setUp is not invoked, no fixture upload.
spec=importlib.util.spec_from_file_location('boundary_harness',P/'backend_stage/test_provider_boundary.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
tree=ast.parse((R/'iald_app_providers.py').read_text(encoding='utf-8'))
names={'image_parts','wire_messages','transport_tool_options','output_budget','check_window','scoped_task_names'}
h.nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]+[next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_api')]
t=h.ProviderBoundaryTests();t.setUp()
try:
 runtime=private.PrivateMediaRuntime(store,scope,authorize_dispatch=lambda:True,rates={'input':.435,'cache_read':.0036,'output':.87})
 t.runtime=runtime;t.part=part;t.raw=audio
 # Replace AST compiled harness with installed-source functions using same isolated stubs.
 exec(compile(ast.Module(body=h.nodes,type_ignores=[]),'installed exact provider AST','exec'),t.ns)
 prefixbytes=(R/'.iald_runtime/haiku/prefix.md').read_bytes();prefix=prefixbytes.decode('utf-8')
 messages=t.ns['wire_messages']([{'role':'user','content':content}],prefix,provider='mimo',images_authorized=True,media_authorized=True,private_media=runtime)
 try:t.api(messages,t.spending())
 except h.BoundaryReached:pass
 else:raise AssertionError('HTTP boundary not reached')
 wire=json.dumps(t.captured,allow_nan=False).encode('utf-8');decoded=json.loads(wire)
 typed=[p for m in decoded['messages'] if isinstance(m.get('content'),list) for p in m['content'] if p.get('type')=='input_audio'];assert len(typed)==1
 uri=typed[0]['input_audio']['data'];header,b64=uri.split(',',1);final=base64.b64decode(b64,validate=True)
 assert final==audio and sha(final)==part['sha256'];assert decoded['messages'][0]['content'].startswith(prefix)
 with wave.open(io.BytesIO(final)) as wav:wavfacts={'channels':wav.getnchannels(),'sample_rate':wav.getframerate(),'sample_width':wav.getsampwidth(),'frames':wav.getnframes(),'duration_seconds':wav.getnframes()/wav.getframerate()}
 replay={'status':'OFFLINE_TRANSPORT_PRESERVED','job_id':job,'installed_source_sha256':{n:sha((R/n).read_bytes()) for n in ['iald_app_providers.py','private_media_store.py','iald_mimo_multimodal.py','iald_media_budget.py']},'objective_sha256':sha(rawobjective),'typed_part_type':'input_audio','data_uri_header':header,'decoded_bytes':len(final),'decoded_sha256':sha(final),'stored_metadata_hash_matches':True,'wav':wavfacts,'serialized_json_bytes':len(wire),'serialized_json_sha256':sha(wire),'scientific_prefix_sha256':sha(prefixbytes),'scientific_prefix_bytes':len(prefixbytes),'scientific_prefix_integral':True,'projection_and_wallet':'Identity ACOM/system projection and fake wallet/key; actual installed provider AST/admission/expand/Requests-compatible JSON serialization. Historical full projected request not available.','historical_raw_request_available':False,'historical_wire_proved':False,'causality_measured':False,'remote_calls':0,'runtime_writes':False,'conclusion':'PERCEPTION_FAILURE observed; offline replay finds no typed-audio byte loss; no proven transport cause or proposed patch.'}
 with (W/'MANUAL_AUDIO_OFFLINE_REPLAY.json').open('x',encoding='utf-8') as f:json.dump(replay,f,ensure_ascii=False,indent=2)
finally:t.tearDown()
with ro(R/'.iald_runtime/monthly_wallet/wallet.sqlite3') as d:
 ledger={table:[dict(row) for row in d.execute('select * from '+table+' where task_id=?',(job,))] for table in ['tasks','calls','entries']}
assert ledger['tasks'] and all(row['owner']==scope.generation for rows in ledger.values() for row in rows)
ledgercost=-sum(row['delta'] for row in ledger['entries'] if row['kind']=='cost')/1e9
# Do not hide lifecycle discrepancy: job completed while wallet task cancelled.
c.update({'semantic_result':'PERCEPTION_FAILURE','ledger':ledger,'ledger_cost_usd':ledgercost,'ledger_matches_metric_cost':abs(ledgercost-c['known_cost_estimate_usd'])<1e-10,'lifecycle_discrepancy':'Job completed; wallet task cancelled; measured call settled. Preserved, cause not diagnosed.','offline_replay':{'path':str(W/'MANUAL_AUDIO_OFFLINE_REPLAY.json'),'sha256':sha((W/'MANUAL_AUDIO_OFFLINE_REPLAY.json').read_bytes())},'historical_raw_request_available':False,'causality_measured':False})
# Preserve initial capture before enrichment; exclusive new snapshot and atomic replace.
original=(W/'MANUAL_AUDIO_RESULT.json').read_bytes()
with (W/'MANUAL_AUDIO_RESULT_CAPTURE_ORIGINAL.json').open('xb') as f:f.write(original)
tmp=W/'MANUAL_AUDIO_RESULT_ENRICHED.tmp'
with tmp.open('x',encoding='utf-8') as f:json.dump(c,f,ensure_ascii=False,indent=2)
tmp.replace(W/'MANUAL_AUDIO_RESULT.json')
print(json.dumps({'status':replay['status'],'semantic_result':c['semantic_result'],'bytes':len(final),'wav':wavfacts,'ledger_cost_usd':ledgercost,'ledger_task_status':ledger['tasks'][0]['status'],'historical_wire_proved':False}))
