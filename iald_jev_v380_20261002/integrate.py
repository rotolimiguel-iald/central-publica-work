"""Build isolated application patches from the exact post-bench baseline."""
from pathlib import Path
import ast
import hashlib
import json
import sys

WORK = Path(__file__).resolve().parent
BASE = WORK / 'baseline'
STAGE = WORK / 'app_patch'
sys.path.insert(0, str(WORK))
from transaction import atomic, backup, write_evidence

def save(name, text):
    raw = text.encode('utf-8')
    ast.parse(raw, filename=name)
    path = STAGE / name
    if path.exists():
        if path.read_bytes() == raw:
            return
        backup(path)
    atomic(path, raw)

def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Expected exactly one integration location: '+old[:70])
    return text.replace(old, new, 1)

def replace_function(text, name, replacement):
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name)
    lines = text.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1]) + replacement.rstrip()+'\n' + ''.join(lines[node.end_lineno:])

def main():
    STAGE.mkdir(exist_ok=True)
    router = (BASE/'iald_auto_router.py').read_bytes().decode('utf-8')
    router = replace_once(router, 'import iald_task_policy as task_policy',
                          'import iald_task_policy as task_policy\nimport iald_jev_control as jev_control')
    router = replace_once(router,
        "return text,dict(release=manifest['active_cluster']['release'],source_sha256=digest,",
        "return text,dict(release=manifest['active_cluster']['release'],source_sha256=digest,\n        release_source_sha256=manifest['active_cluster']['release_source_sha256'],")
    router = replace_function(router, 'choose', (WORK/'router_flow.inc').read_text(encoding='utf-8'))
    router += '\n\n' + (WORK/'router_scope.inc').read_text(encoding='utf-8')
    save('iald_auto_router.py', router)
    web = (BASE/'iald_web_server.py').read_bytes().decode('utf-8')
    # Existing provider consent, role refresh, scopes and dispatch guards remain intact.
    old = "        selected=dict(current,motor=chosen)"
    new = "        if task_scope is not None:\n            app_router.bind_scope(task_scope,receipt)\n" + old
    web = replace_once(web, old, new)
    # Server-owned keyword only; no client JSON field is trusted as an instruction.
    anchor="        task_scope=_new_app_task_scope(user,executor=chosen) if chosen not in ('kimi','claude-haiku','nativa') else None"
    web = replace_once(web,anchor,"        routing_instruction=app_router.route_instruction(receipt)\n"+anchor)
    for name in ('_chat_openai','_chat_claude','_chat_externo','_chat_avaliacao'):
        node=next(n for n in ast.parse(web).body if isinstance(n,ast.FunctionDef) and n.name==name)
        lines=web.splitlines(keepends=True);part=''.join(lines[node.lineno-1:node.end_lineno])
        part=replace_once(part,'dispatch_check=None):','dispatch_check=None, routing_instruction=None):')
        if name in ('_chat_openai','_chat_claude'):
            part=replace_once(part,'task_scope=task_scope, dispatch_check=dispatch_check)',
                              'task_scope=task_scope, dispatch_check=dispatch_check, routing_instruction=routing_instruction)')
        elif name=='_chat_avaliacao':
            part=replace_once(part,"        if task_scope: note +=", "        if routing_instruction and task_scope is None: note += '\\n'+routing_instruction\n        if task_scope: note +=")
        else:
            needle='        instrucao = "" if registro.get("sacred_language") else INSTRUCAO_LINGUAGEM_TECNICA'
            part=replace_once(part,needle,needle+"\n        if routing_instruction and task_scope is None: instrucao += '\\n'+routing_instruction")
        web=''.join(lines[:node.lineno-1])+part+''.join(lines[node.end_lineno:])
    web=replace_once(web,'def _chat_nativa_automatica(req_json,user,registro):',
                     'def _chat_nativa_automatica(req_json,user,registro,*,routing_instruction=None):')
    needle="        messages[0]['content']='Responda sob o regime IALD. Preserve os estatutos e use LaTeX com delimitadores próprios.'"
    web=replace_once(web,needle,needle+"\n        if routing_instruction: messages[0]['content']+='\\n'+routing_instruction")
    node=next(n for n in ast.parse(web).body if isinstance(n,ast.FunctionDef) and n.name=='_chat_automatico_autorizado')
    lines=web.splitlines(keepends=True);part=''.join(lines[node.lineno-1:node.end_lineno])
    if part.count('task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True))')!=3:
        raise ValueError('Automatic provider dispatch branches changed')
    part=part.replace('task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True))',
                      'task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction)')
    part=replace_once(part,'_chat_nativa_automatica(req_json,user,current)',
                      '_chat_nativa_automatica(req_json,user,current,routing_instruction=routing_instruction)')
    web=''.join(lines[:node.lineno-1])+part+''.join(lines[node.end_lineno:])
    save('iald_web_server.py', web)
    bridge = (BASE/'iald_task_bridge.py').read_bytes().decode('utf-8')
    old = "prefix+'\\nEtapa delegada: produza somente o rascunho solicitado."
    new = "prefix+'\\n'+router.route_instruction(receipt)+'\\nEtapa delegada: produza somente o rascunho solicitado."
    bridge = replace_once(bridge, old, new)
    save('iald_task_bridge.py', bridge)
    raw = (WORK/'controller/iald_jev_control.py').read_bytes()
    save('iald_jev_control.py', raw.decode('utf-8'))
    files = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in STAGE.glob('*.py')}
    write_evidence(WORK/'integration.json', {'files':files,'baseline':str(WORK/'baseline.json'),
                    'public_client_changed':False,'accounts_changed':False,'provider_calls':0})
    print(json.dumps({'staged_modules':len(files)}))

if __name__ == '__main__':
    main()
