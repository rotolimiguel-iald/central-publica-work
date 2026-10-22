"""Authenticated, server-served activity review. Never registered as a model tool."""
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid

import iald_app_memory as memory
from iald_memory.mission import MissionController


def _loaded_sources():
    """Capture once at import; later HTTP requests never re-hash changed disk files."""
    names = ('iald_app_memory', 'iald_activity_operations', 'iald_activity_ui',
        'iald_auto_router', 'iald_app_providers', 'iald_task_bridge', 'iald_task_session',
        'iald_chat_jobs', 'iald_motores', 'iald_memory.activity', 'iald_memory.mission',
        'iald_memory.store', 'iald_native_memory', 'iald_native_activity')
    result = {}
    for name in names:
        module = sys.modules.get(name)
        path = getattr(module, '__file__', None)
        if not path:
            result[name] = {'status': 'not_imported_at_capture'}
            continue
        result[name] = {'status': 'imported', 'source_sha256_at_capture':
            hashlib.sha256(Path(path).read_bytes()).hexdigest()}
    server = sys.modules.get('iald_web_server') or sys.modules.get('__main__')
    path = getattr(server, '__file__', '')
    if Path(path).name == 'iald_web_server.py':
        result['iald_web_server'] = {'status': 'executing', 'source_sha256_at_capture':
            hashlib.sha256(Path(path).read_bytes()).hexdigest()}
    return {'protocol': 'iald-app-import-receipt/v1', 'modules': result,
        'scope': 'Loaded module provenance plus source bytes captured at activity UI import; not a claim that every path executed.'}


IMPORT_RECEIPT = _loaded_sources()


def _context(principal, conversation):
    if not principal or not isinstance(conversation, str) or not memory._CONV.fullmatch(conversation):
        raise ValueError('Conversa inválida.')
    scope = {'house': 'IALD_APP', 'principal': principal}
    return memory.Binding(memory.MemoryStore(memory._SHARED_ROOT),
        'app_' + memory.digest(principal + ':' + conversation), scope, 'review')


def state(principal, conversation):
    binding = _context(principal, conversation)
    controller = MissionController(binding.store, binding.context_id, binding.scope)
    snapshot, mission, _ = controller.load()
    if mission is None:
        return {'revision': snapshot['revision'], 'tasks': [], 'handles': [], 'legacy': True,
            'loaded_version': IMPORT_RECEIPT}
    request_tasks = {}
    results = {}
    for record in snapshot['q']['records']:
        metadata = record.get('meta', {}).get('iald_activity_v1', {})
        value = metadata.get('data', {})
        if metadata.get('kind') == 'request':
            request_tasks[value['request_id']] = value['task_id']
        if metadata.get('kind') == 'result' and value.get('terminal'):
            results[value['request_id']] = value['result']
    outputs = {request_tasks[r]: value for r, value in results.items() if r in request_tasks}
    # No filesystem paths, lease capabilities, account IDs or provider credentials.
    tasks = [{'id': i, 'criterion': t['criterion'], 'status': t['status'],
        'epoch': t['epoch'], 'output': outputs.get(i),
        'evidence_sha256': [p['sha256'] for p in t['evidence']]}
        for i, t in mission['tasks'].items()]
    handles = [{k: h[k] for k in ('id', 'status', 'kind', 'task_id') if k in h}
        for h in snapshot['p']['handles']
        if h.get('status') not in ('completed', 'returned', 'closed', 'failed', 'cancelled')]
    return {'revision': snapshot['revision'], 'tasks': tasks, 'handles': handles,
        'loaded_version': IMPORT_RECEIPT,
        'notice': 'Execução concluída não significa requisito aceito. Revise somente os resultados selecionados.'}


def _artifact(binding, value):
    raw = memory.canonical(value).encode('utf-8')
    memory.guard.assert_clean_text(raw.decode(), 'app.human_review')
    sha = hashlib.sha256(raw).hexdigest()
    folder = Path(binding.store.root) / 'app_reviews'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (sha + '.json')
    if path.exists():
        if path.read_bytes() != raw: raise ValueError('Review evidence mismatch')
    else:
        tmp = folder / (uuid.uuid4().hex[:12] + '.tmp')
        with tmp.open('xb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        if tmp.read_bytes() != raw: raise OSError('Review write verification failed')
        tmp.replace(path)
    return {'path': str(path), 'sha256': sha}


def review(principal, data):
    """Called only after server authentication + origin/JSON guard, never by LLM.

    The actor below names this server's authenticated-human adapter. The receipt
    records its origin; the actor's spelling is not proof of authentication.
    """
    allowed = {'conversation', 'revision', 'tasks', 'confirmed', 'comment'}
    if not isinstance(data, dict) or set(data) - allowed or data.get('confirmed') is not True:
        raise ValueError('Confirmação humana explícita necessária.')
    ids = data.get('tasks')
    if (not isinstance(ids, list) or not 1 <= len(ids) <= 20 or len(set(ids)) != len(ids)
            or any(not isinstance(i, str) or not re.fullmatch(r'req_[0-9a-f]{64}', i) for i in ids)
            or type(data.get('revision')) is not int):
        raise ValueError('Seleção inválida.')
    comment = data.get('comment', '')
    if not isinstance(comment, str) or len(comment) > 2000: raise ValueError('Comentário inválido.')
    binding = _context(principal, data['conversation'])
    controller = MissionController(binding.store, binding.context_id, binding.scope)
    projection = controller.project(max_chars=2000000)
    current = projection['projection']
    if current['revision'] != data['revision']: raise ValueError('Estado mudou. Atualize antes de revisar.')
    tasks = {t['id']: t for t in current['active']}
    if any(i not in tasks or tasks[i]['status'] != 'review_pending' for i in ids):
        raise ValueError('Somente candidatos pendentes podem ser aceitos.')
    pinned = {i: {'epoch': tasks[i]['epoch'], 'evidence': tasks[i]['evidence']} for i in ids}
    evidence = _artifact(binding, {'protocol': 'iald-app-human-review/v1',
        'authenticated_principal': principal, 'context_id': binding.context_id,
        'scope': binding.scope, 'origin': 'authenticated_http_human_selection',
        'revision': current['revision'], 'selection': pinned, 'confirmed': True, 'comment': comment})
    actor = {'id': 'app.human-review.' + memory.digest(principal), 'kind': 'agent'}
    accepted = []
    expected = current['revision']
    for i in ids:
        # Mechanical CAS reconciliation only between these explicit selections.
        # Any competing update stops the batch, preserving accepted receipts.
        projection = controller.project(max_chars=2000000)
        if projection['receipt']['revision'] != expected:
            return {'accepted': accepted, 'pending': [j for j in ids if j not in accepted],
                'requires_refresh': True, 'revision': projection['receipt']['revision']}
        result = controller.action({'operation': 'accept', 'actor': actor,
            'task_id': i, 'expected_revision': expected,
            'projection_sha256': projection['projection_sha256'],
            'event_id': 'app-human-' + memory.digest(evidence['sha256'] + ':' + i),
            'review_evidence': [evidence], 'note': 'Seleção explícita do titular autenticado; não é aceite automático do modelo.'})
        accepted.append(i)
        expected = result['receipt']['revision']
    return {'accepted': accepted, 'pending': [], 'revision': expected, 'review_sha256': evidence['sha256']}


PAGE = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atividades da conversa — IALD</title><style>body{font:16px system-ui;max-width:60rem;margin:2rem auto;padding:1rem;background:#101723;color:#edf2f7}input,button,textarea{font:inherit;padding:.6rem;margin:.3rem}article{padding:1rem;border:1px solid #526278;margin:1rem 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}button{cursor:pointer}label{display:block}</style>
<h1>Atividades da conversa</h1><p>As respostas ficam disponíveis sem aprovação obrigatória. Aceite apenas atividades que você revisou; executar não equivale a satisfazer o pedido.</p>
<input id="conversation" type="hidden" maxlength="64"><p>Abra este painel a partir da conversa no app.</p><button id="load">Atualizar progresso</button>
<p id="status" role="status"></p><main id="tasks"></main><label>Comentário da revisão <textarea id="comment" maxlength="2000"></textarea></label>
<button id="review">Aceitar as atividades selecionadas</button><script>
let revision;const el=id=>document.getElementById(id);el('conversation').value=new URLSearchParams(location.search).get('conversation')||'';
async function load(){const r=await fetch('/api/activities?conversation='+encodeURIComponent(el('conversation').value));const d=await r.json();if(!r.ok)throw Error(d.error);revision=d.revision;el('tasks').replaceChildren();el('status').textContent='Revisão '+revision+' · '+d.tasks.length+' atividades · '+d.handles.length+' operações pendentes';for(const t of d.tasks){const a=document.createElement('article');const l=document.createElement('label');const c=document.createElement('input');c.type='checkbox';c.value=t.id;c.disabled=t.status!=='review_pending';l.append(c,document.createTextNode(t.status+' · '+t.criterion));const p=document.createElement('pre');p.textContent=t.output==null?'Resultado ainda não integrado.':JSON.stringify(t.output,null,2);a.append(l,p);el('tasks').append(a)}}
el('load').onclick=()=>load().catch(e=>el('status').textContent=e.message);
el('review').onclick=async()=>{try{const tasks=[...document.querySelectorAll('input[type=checkbox]:checked')].map(x=>x.value);if(!tasks.length)throw Error('Selecione atividades já revisadas.');if(!confirm('Você revisou os resultados e confirma que atendem aos pedidos selecionados?'))return;const r=await fetch('/api/activities/review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({conversation:el('conversation').value,revision,tasks,confirmed:true,comment:el('comment').value})});const d=await r.json();if(!r.ok)throw Error(d.error);await load()}catch(e){el('status').textContent=e.message}};
if(el('conversation').value)load().catch(e=>el('status').textContent=e.message);
</script></html>'''


def register(app, *, account_key, json_guard):
    from flask import request, session, jsonify, Response

    def principal():
        if not session.get('authenticated') or not session.get('username'):
            raise PermissionError('Não autenticado.')
        return account_key(session['username'])

    @app.route('/app/activities')
    def app_activity_page():
        principal()
        return Response(PAGE, content_type='text/html; charset=utf-8',
            headers={'Cache-Control': 'private, no-store',
                'Content-Security-Policy': "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'"})

    @app.route('/api/activities', methods=['GET'])
    def app_activity_state():
        try:
            identity = principal()
            result = ({'loaded_version': IMPORT_RECEIPT} if request.args.get('view') == 'version'
                else state(identity, request.args.get('conversation', '')))
        except Exception: return jsonify(error='Atividade indisponível nesta conta/conversa.'), 409
        response = jsonify(result); response.headers['Cache-Control'] = 'private, no-store'; return response

    @app.route('/api/activities/review', methods=['POST'])
    def app_activity_review():
        identity = principal()
        data, error = json_guard({'conversation', 'revision', 'tasks', 'confirmed', 'comment'})
        if error: return error
        try: result = review(identity, data)
        except Exception: return jsonify(error='Revisão recusada. Atualize o estado e confira a seleção.'), 409
        response = jsonify(result); response.headers['Cache-Control'] = 'private, no-store'; return response
