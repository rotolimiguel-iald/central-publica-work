"""Original audio + installed transport/projection code; intercept HTTP before send."""
import ast
import base64
import binascii
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sqlite3
import sys
import threading
import types
import wave
import zlib

sys.dont_write_bytecode=True
RELEASE=Path(__file__).resolve().parent
W=RELEASE.parent/'live_stage';R=Path('C:/IALD/projetos_pyhton/IALD');M=Path('C:/IALD/MEMORIA_IALD/state')
receipt=json.loads((W/'AUDIO_RESULT.json').read_bytes());cid=receipt['acom']['context_id']
sys.path.insert(0,'C:/IALD/MEMORIA_IALD/lib')
from iald_memory import store as core
def sha(raw):return hashlib.sha256(raw).hexdigest()
with sqlite3.connect((M/'memory.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
    db.row_factory=sqlite3.Row
    anchor=db.execute('SELECT * FROM contexts WHERE context_id=?',(cid,)).fetchone()
    original=zlib.decompress(anchor['objective_blob']);assert sha(original)==anchor['objective_sha256']
    parts=json.loads(original)
    state=core._initial_state()
    for row in db.execute('SELECT * FROM events WHERE context_id=? AND revision<=12 ORDER BY revision',(cid,)):
        changes=json.loads(row['changes_json']);changes.setdefault('records',[]);changes.setdefault('flow',{})
        core._apply_inplace(state,changes)
        assert sha(core._dump(state).encode())==row['state_sha256']
        head=dict(row)
    scope=json.loads(anchor['scope_json']);a=json.loads(anchor['anchor_json'])
snapshot=dict(context_id=cid,scope=scope,objective=original.decode(),objective_sha256=anchor['objective_sha256'],
    constraints=a['constraints'],parent_id=a['parent_id'],q=state['q'],p=state['p'],
    receipt=dict(context_id=cid,scope=scope,revision=head['revision'],state_sha256=head['state_sha256'],event_hash=head['event_hash']))
class Binding:
    context_id=cid
    def snapshot(self):return copy.deepcopy(snapshot)
    def projection(self,max_chars=None):
        return core.MemoryStore.project_snapshot(object.__new__(core.MemoryStore),self.snapshot(),max_chars=1000000,current_input=original.decode())
binding=Binding();binding.scope=scope

def load_pure(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
view=load_pure('view_audio_replay',R/'iald_router_media_view.py')
media=load_pure('iald_mimo_multimodal',R/'iald_mimo_multimodal.py');sys.modules['iald_mimo_multimodal']=media
memory=types.ModuleType('iald_app_memory');memory.current=lambda:binding
memory.__dict__.update(copy=copy,_START='\n<IALD_COMMON_MEMORY_V1>\n',_END='\n</IALD_COMMON_MEMORY_V1>\n')
mem_tree=ast.parse((R/'iald_app_memory.py').read_text(encoding='utf-8'))
node=next(n for n in mem_tree.body if isinstance(n,ast.FunctionDef) and n.name=='project_messages')
exec(compile(ast.Module(body=[node],type_ignores=[]),'installed projection','exec'),memory.__dict__)
sys.modules['iald_app_memory']=memory
claude=types.ModuleType('iald_motor_claude');claude.__dict__.update(base64=base64,re=re,binascii=binascii)
t=ast.parse((R/'iald_motor_claude.py').read_text(encoding='utf-8'))
nodes=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_tipo_pelos_bytes' or isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='_ASSINATURAS_DE_IMAGEM' for v in n.targets)]
exec(compile(ast.Module(body=nodes,type_ignores=[]),'installed signature','exec'),claude.__dict__);sys.modules['iald_motor_claude']=claude
candidate='--candidate' in sys.argv
provider_source=RELEASE/'iald_app_providers.py' if candidate else R/'iald_app_providers.py'
source=provider_source.read_text(encoding='utf-8');tree=ast.parse(source)
names={'image_parts','wire_messages','transport_tool_options','output_budget','check_window','scoped_task_names'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
method=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_api')
nodes.append(method)
captured={}
class BoundaryReached(BaseException):pass
def intercept(label,fn,*args,**kwargs):
    assert label=='model.mimo';captured.update(kwargs['json']);raise BoundaryReached()
memory.http_call=intercept
requests=types.ModuleType('requests');requests.post=lambda *a,**k: (_ for _ in ()).throw(AssertionError('NETWORK_FORBIDDEN'));sys.modules['requests']=requests
ns=dict(base64=base64,binascii=binascii,json=json,copy=copy,app_memory=memory,router_media_view=view,
    MODELS={'mimo':{'model':'mimo-v2.6-pro','output':131072,'url':'https://api.xiaomimimo.com/v1/chat/completions'}},
    WINDOW=1048576,MAX_ROUNDS=4,MAX_TOOLS=4,MAX_PARSED_TOOLS=32,TASK_TOOL_NAMES=frozenset(),TOOL_NAMES=frozenset(),
    adapter=lambda _:types.SimpleNamespace(load_mimo=lambda:'OFFLINE_DUMMY_NOT_A_CREDENTIAL'))
exec(compile(ast.Module(body=nodes,type_ignores=[]),'installed exact transport functions','exec'),ns)
prefix_path=R/'.iald_runtime/haiku/prefix.md';prefix=prefix_path.read_text(encoding='utf-8')
view._View(binding) # Explicit scope/custody consistency before projection.
view.project_system_messages=lambda messages: view_original(messages,binding=binding)
view_original=load_pure('original_view_audio_replay',R/'iald_router_media_view.py').project_system_messages
messages=ns['wire_messages']([{'role':'user','content':parts}],prefix,provider='mimo',images_authorized=True,media_authorized=True)
try:
    ns['_api'](types.SimpleNamespace(save=lambda _:None),'mimo',messages,[],None,None,threading.Event(),[],{'calls':[]},0,None)
except BoundaryReached:pass
assert captured
actual=next(m for m in reversed(captured['messages']) if m['role']=='user')['content']
audio=next(p['input_audio']['data'] for p in parts if p['type']=='input_audio')
typed=next(p['input_audio']['data'] for p in actual if p['type']=='input_audio')
assert typed==audio and actual==parts
raw=base64.b64decode(audio.split(',',1)[1],validate=True)
with wave.open(io.BytesIO(raw)) as wav:
    wav_info=dict(seconds=wav.getnframes()/wav.getframerate(),sample_rate=wav.getframerate(),channels=wav.getnchannels(),sample_width=wav.getsampwidth())
system=captured['messages'][0]['content'];assert system.startswith(prefix)
if candidate:assert 'MIMO_TYPED_MEDIA_CLARIFICATION_V1' in system
tokens=re.findall(r'\[IALD_MEDIA_CUSTODY:[0-9a-f]{64}\]',system)
result=dict(status='OFFLINE_REPLAY_PASS',job=receipt['job']['id'],context_revision=12,
    original_objective_sha256=anchor['objective_sha256'],typed_audio_sha256=sha(raw),typed_audio_bytes=len(raw),wav=wav_info,
    final_typed_user_parts_preserved=True,data_uri_preserved=True,media_bytes_present_at_http_boundary=True,
    system_custody_marker_count=len(tokens),system_has_provenance='IALD_ROUTER_MEDIA_VIEW_V1' in system,
    scientific_prefix_bytes_preserved=True,scientific_prefix_sha256=sha(prefix.encode()),
    installed_sources={name:sha((R/name).read_bytes()) for name in ['iald_app_providers.py','iald_app_memory.py','iald_router_media_view.py','iald_mimo_multimodal.py']},
    limitation='Exact installed functions and original typed audio with verified replay through revision12. Entire current science prefix preserved; tool definitions/profile/routing notes were not reconstructed, so this is not a bit-identical historical HTTP request. No outbound request body was archived; actual prior wire payload cannot be certified byte-for-byte.',
    diagnosis='No typed audio loss reproduced. System ACOM duplicates become custody references while user audio remains actual bytes. Context confusion is plausible but causal effect not measured; short tone perception remains another hypothesis.',
    candidate=candidate,transport_source=str(provider_source),transport_source_sha256=sha(provider_source.read_bytes()),
    causal_effect_measured=False,remote_calls=0,credential_reads=0,runtime_writes=0)
with (RELEASE/'validation/audio_offline_replay.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))
