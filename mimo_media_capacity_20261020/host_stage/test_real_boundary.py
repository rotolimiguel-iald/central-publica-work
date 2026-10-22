"""One real maximum-byte local WAV pipeline; no request to a provider."""
import ast
from contextlib import closing
import hashlib
import io
import json
import math
from pathlib import Path
import sqlite3
import threading
import wave

from test_host import HERE, WORK, LIVE, HostTests, media
from claude_memory_package import load_package
from iald_orcamento import SpendingGuard, BudgetError

fixture = HostTests('test_lazy_caps_no_storage_and_scope_binding')
fixture.setUp()
try:
    # Complete valid PCM container, not a forged Content-Length or tiny input.
    frames = (media.MAX_RAW_BYTES - 44) // 2
    stream = io.BytesIO()
    with wave.open(stream, 'wb') as audio:
        audio.setnchannels(1);audio.setsampwidth(2);audio.setframerate(8000)
        audio.writeframes(b'\0\0' * frames)
    raw = stream.getvalue()
    assert len(raw) == media.MAX_RAW_BYTES == 37_499_904
    package = load_package(LIVE/'.iald_runtime/haiku', canonical_manifest=LIVE/'iald_nucleo_fixo.json')
    app, called = fixture.app()
    client = app.test_client()
    headers = {'Authorization': 'Bearer synthetic-valid'}
    response = client.post(fixture.upload_path(), data=raw,
                           content_type='audio/wav', headers=headers)
    assert response.status_code == 201, (response.status_code, response.get_json())
    part = response.get_json()
    assert part.pop('media_scope') == fixture.host.capabilities('alice','c_test')['media_scope']
    assert part['bytes'] == len(raw) and part['sha256'] == hashlib.sha256(raw).hexdigest()
    metadata = client.get(fixture.metadata_path(part), headers=headers)
    assert metadata.status_code == 200 and fixture.cipher.reads == 0
    too_big = client.post(fixture.upload_path(), data=raw+b'\0',
                          content_type='audio/wav', headers=headers)
    assert too_big.status_code == 413

    messages = [dict(role='system', content=package.prefix),
                dict(role='user', content='Previous text preserved'),
                dict(role='assistant', content='Previous answer preserved'),
                dict(role='user', content=[dict(type='text',text='Analyze this synthetic tone'),part])]
    runtime = fixture.host.runtime('alice', messages, 'c_test', automatic=True)
    # Pure definitions extracted without importing a server or task runtime.
    artifact_tree = ast.parse((LIVE/'iald_task_artifacts.py').read_bytes())
    artifact = next(n.value for n in artifact_tree.body if isinstance(n,ast.Assign)
                    and any(isinstance(t,ast.Name) and t.id=='TOOL_DEFINITION' for t in n.targets))
    task_tree = ast.parse((LIVE/'iald_task_session.py').read_bytes())
    nodes = [n for n in task_tree.body if isinstance(n,ast.FunctionDef) and n.name in ('definition','definitions')]
    definitions = {}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'pure task tool definitions','exec'), definitions)
    extensions = next(n.value for n in artifact_tree.body if isinstance(n,ast.Assign)
                      and any(isinstance(t,ast.Name) and t.id=='EXTENSIONS' for t in n.targets))
    artifact_value = eval(compile(ast.Expression(artifact),'pure public artifact definition','eval'),
                          {'__builtins__':{}, 'list':list, 'EXTENSIONS':ast.literal_eval(extensions)})
    tools = definitions['definitions'](artifact_value)
    body = dict(model='mimo-v2.6-pro', messages=messages, tools=tools, stream=True,
                stream_options={'include_usage':True}, thinking={'type':'enabled'})
    plan = runtime.admit(body, 131072)
    body['max_completion_tokens'] = plan['output_reserved_tokens']

    spend_tree = ast.parse((HERE/'iald_app_spend.py').read_bytes())
    nodes = [n for n in spend_tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in ('PublicAccount','_positive')]
    spend_ns = dict(math=math,json=json,BudgetError=BudgetError,
                    MODELS={'mimo':dict(model='mimo-v2.6-pro', output=131072, rates=(.435,.0036,.87))})
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'staged real PublicAccount','exec'),spend_ns)
    account = spend_ns['PublicAccount'].__new__(spend_ns['PublicAccount'])
    account._lock=threading.RLock();account.closed=False;account.pending=None
    account.account_key_hash='a'*64;account.daily=100.;account.total=100.;account.group=100.
    spend_path=fixture.root/'isolated_spending.sqlite3'
    account.guard=SpendingGuard(spend_path)
    reservation=runtime.reserve(account,body,plan)
    with closing(sqlite3.connect(spend_path)) as db:
        row=db.execute('SELECT cap,status FROM calls WHERE id=?',(reservation,)).fetchone()
    assert row and row[1]=='reserved'

    expanded=runtime.expand(body,provider='mimo',plan=plan)
    assert expanded['messages'][0]['content']==package.prefix
    assert expanded['messages'][1:3]==messages[1:3]
    uri=expanded['messages'][-1]['content'][1]['input_audio']['data']
    assert uri.startswith('data:audio/wav;base64,') and len(uri.encode())<=50_000_000
    assert fixture.cipher.reads==1
    wire_bytes=len(json.dumps(expanded,ensure_ascii=True,allow_nan=False).encode('ascii'))
    assert wire_bytes<=64_000_000
    account.discard_undispatched()  # Local-only reservation released, never dispatched.
    report=dict(status='PASS_LOCAL_MAXIMUM_BYTE_BOUNDARY',raw_bytes=len(raw),one_above_bytes=len(raw)+1,
        upload_http=response.status_code,one_above_http=too_big.status_code,
        request_property='READ_ONLY_CUSTOM_PER_ROUTE',metadata_without_decrypt=True,
        duration_seconds=part['duration_seconds'],public_prefix_chars=len(package.prefix),
        public_prefix_sha256=hashlib.sha256(package.prefix.encode()).hexdigest(),public_prefix_preserved=True,
        full_history_preserved=True,task_tool_definitions=len(tools),input_tokens_bound=plan['input_tokens_bound'],
        output_reserved_tokens=plan['output_reserved_tokens'],media_tokens_estimate=plan['media_tokens_estimate'],
        encoded_uri_bytes=len(uri.encode()),final_wire_json_bytes=wire_bytes,
        isolated_sqlite_reservation=True,reservation_cap_usd=row[0],reservation_released_undispatched=True,
        real_DPAPI_at_rest=True,provider_calls=0,network_calls=0,runtime_writes=0,
        scope='One synthetic PCM/WAV; full verified public package and five pure task definitions. Local admission/reservation/expansion, not remote maximum acceptance or perception.')
    (HERE/'REAL_BYTE_BOUNDARY.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(report))
finally:
    fixture.doCleanups()
