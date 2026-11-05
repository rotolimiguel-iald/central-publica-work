"""Build patch artifacts ONLY below this staging directory. Never import server.

The server has a legacy secret in its preamble: deliver a scoped diff plus an
AST-extracted function fixture, NOT a copy containing that preamble. The reviewed
integrator can apply the patch against the exact baseline pinned in BASELINE.
"""
import ast
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD')


def once(text, before, after):
    if text.count(before) != 1:
        raise ValueError('Patch anchor missing or ambiguous')
    return text.replace(before, after, 1)


def preserve_unchanged_bytes(raw, changed):
    """Keep untouched lines byte-for-byte, including mixed CRLF/LF endings."""
    old = raw.decode('utf-8').splitlines(keepends=True)
    new = changed.splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(a=[s.rstrip('\r\n') for s in old],
                                     b=[s.rstrip('\r\n') for s in new], autojunk=False)
    output = []
    for tag, i, j, a, b in matcher.get_opcodes():
        if tag == 'equal':
            output.extend(old[i:j])
        elif tag in ('insert', 'replace'):
            context = old[min(i, len(old)-1)] if old else '\n'
            ending = '\r\n' if context.endswith('\r\n') else '\n'
            output.extend(s.replace('\n', ending) for s in new[a:b])
    return ''.join(output).encode('utf-8')


def motor_patch(text):
    text = once(text, 'def linhas_com_espera(fazer_request, intervalo=15.0):',
                'def linhas_com_espera(fazer_request, intervalo=15.0, *, recovery=None):')
    text = once(text, '                r = fazer_request()\n',
                '                if recovery is not None: recovery.before_send()\n                r = fazer_request()\n')
    text = once(text, '                if r.status_code == 200:\n',
                '                if recovery is not None: recovery.inspect(r)\n                if r.status_code == 200:\n')
    text = once(text, 'def transmitir(fazer_request, ao_uso, ao_texto=None, intervalo=15.0, avisos=False):',
                'def transmitir(fazer_request, ao_uso, ao_texto=None, intervalo=15.0, avisos=False, *, recovery=None):')
    text = once(text, 'for tipo, linha in linhas_com_espera(fazer_request, intervalo):',
                'for tipo, linha in linhas_com_espera(fazer_request, intervalo, recovery=recovery):')
    return text


def server_patch(text):
    text = once(text, 'import iald_auto_router as app_router',
                'import iald_auto_router as app_router\nimport iald_auto_recovery as app_recovery')
    text = once(text, 'yield from iald_motores.linhas_com_espera(fazer, intervalo=AGENT_KEEPALIVE_SEC)',
                "yield from iald_motores.linhas_com_espera(fazer, intervalo=AGENT_KEEPALIVE_SEC,\n                        recovery=getattr(motor, 'recovery_attempt', None))")
    # Only the authenticated AUTO caller supplies recovery_attempt; manual
    # callers and the private service keep the default None.
    before = 'def _chat_openai(req_json, user, registro, is_stream, tokens_in, *, task_scope=None, dispatch_check=None, routing_instruction=None):'
    text = once(text, before, before[:-2] + ', recovery_attempt=None):')
    text = once(text, 'return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.OPENAI, task_scope=task_scope, dispatch_check=dispatch_check, routing_instruction=routing_instruction)',
                'return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.OPENAI, task_scope=task_scope, dispatch_check=dispatch_check, routing_instruction=routing_instruction, recovery_attempt=recovery_attempt)')
    before = 'def _chat_externo(req_json, user, registro, is_stream, tokens_in, motor=iald_motores.OPENAI, *, task_scope=None, dispatch_check=None, routing_instruction=None):'
    text = once(text, before, before[:-2] + ', recovery_attempt=None):')
    text = once(text, '    claude = motor == iald_motores.CLAUDE\n',
                '    claude = motor == iald_motores.CLAUDE\n    if claude: recovery_attempt = None\n')
    text = once(text, '            if haiku:\n                adaptador.context_notices',
                '            adaptador.recovery_attempt = recovery_attempt\n            if haiku:\n                adaptador.context_notices')
    text = once(text, '                except (iald_motores.CotaEsgotada, iald_orcamento.BudgetError) as exc:\n                    yield from _linhas_da_recusa',
                '                except app_recovery.DefinitiveRefusal as exc:\n                    conta.descartar_ultima_chamada()\n                    exc.settled = True\n                    raise\n                except (iald_motores.CotaEsgotada, iald_orcamento.BudgetError) as exc:\n                    yield from _linhas_da_recusa')
    text = once(text, '                                    avisos=claude):',
                '                                    avisos=claude, recovery=recovery_attempt):')
    text = once(text, '                        except iald_motores.ErroProvedor as exc:\n',
                '                        except app_recovery.DefinitiveRefusal as exc:\n                            conta.descartar_ultima_chamada()\n                            exc.settled = True\n                            raise\n                        except iald_motores.ErroProvedor as exc:\n')
    text = once(text, 'def _chat_automatico_autorizado(req_json,user,registro,is_stream,tokens_in):\n',
        '''def _chat_automatico_autorizado(req_json,user,registro,is_stream,tokens_in,*,_recovery=None):
    from copy import deepcopy
    from flask import stream_with_context
    recovery = _recovery or app_recovery.Recovery(req_json, MOTORES_CFG)
    if _recovery is None:
        recovery.wallet = wallet_runtime.current()
        recovery.memory = app_memory.current()
    elif (wallet_runtime.current() is not recovery.wallet
            or app_memory.current() is not recovery.memory
            or _motor_do_usuario(user)[0] != app_router.AUTO):
        return _sse_aviso('O estado ou a autorização da tarefa mudou.', 'motor_indisponivel')
''')
    text = once(text, "        candidates=[key for key in candidates if _automatic_budget_available(registro,user,key)]",
                "        candidates=[key for key in candidates if key not in recovery.excluded\n            and _automatic_budget_available(registro,user,key)]")
    text = once(text, '        if private_media is not None:\n            if chosen',
                "        if chosen not in candidates:raise PermissionError('Executor outside admitted candidates')\n        recovery.check_science(receipt)\n        if private_media is not None:\n            if chosen")
    text = once(text, "        routing_instruction=app_router.route_instruction(receipt)\n        task_scope=_new_app_task_scope(user,executor=chosen) if chosen not in ('kimi','nativa') else None\n        if task_scope is not None:\n            app_router.bind_scope(task_scope,receipt)",
                "        if not _automatic_budget_available(current,user,chosen):raise PermissionError('Executor budget changed')\n        routing_instruction=app_router.route_instruction(receipt)\n        task_scope=recovery.scope\n        if task_scope is None and chosen not in ('kimi','nativa'):\n            task_scope=_new_app_task_scope(user,executor=chosen)\n        if task_scope is not None:\n            task_scope.executor=chosen\n            recovery.bind_scope(task_scope,receipt,app_router)")
    text = once(text, 'response=_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction)',
                "response=_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction,\n                recovery_attempt=(recovery.attempt if not recovery.reselected and private_media is None and not has_media else None))")
    text = once(text, '        if task_scope:response.iald_task_control=task_scope.control\n        return response',
                "        if task_scope:response.iald_task_control=task_scope.control\n        if _recovery is None and isinstance(response,Response) and response.mimetype=='text/event-stream':\n            response=recovery.wrap(response,lambda: _chat_automatico_autorizado(\n                deepcopy(recovery.request),user,load_users_estrito().get(user,{}),is_stream,tokens_in,_recovery=recovery))\n            response.response=stream_with_context(response.response)\n        return response")
    return text


FUNCTIONS = {'agent_loop', '_chat_automatico', '_chat_automatico_autorizado',
             '_chat_openai', '_chat_externo', '_dispatch_guard', '_medir_saida_sse',
             '_identificar_resposta', '_check_reserved_dispatch', '_sse_aviso'}


def build():
    if (ROOT/'BASELINE.json').exists():
        for entry in json.loads((ROOT/'BASELINE.json').read_text()):
            if hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('Runtime baseline changed; rebase requires review')
    baseline = []
    for name, transform in [('iald_motores.py', motor_patch), ('iald_web_server.py', server_patch)]:
        raw = (SOURCE / name).read_bytes()
        original = raw.decode('utf-8').replace('\r\n', '\n')
        changed = transform(original)
        ast.parse(changed)
        patch = ''.join(difflib.unified_diff(original.splitlines(True), changed.splitlines(True),
                    fromfile='a/'+name, tofile='b/'+name, n=3))
        (ROOT / (name + '.patch')).write_text(patch, encoding='utf-8', newline='\n')
        # Keep original newline encoding; do not deliver the server's preamble.
        output = preserve_unchanged_bytes(raw, changed)
        baseline.append(dict(path=str(SOURCE/name), sha256=hashlib.sha256(raw).hexdigest(),
                             bytes=len(raw), patched_sha256=hashlib.sha256(output).hexdigest()))
        if name == 'iald_motores.py':
            (ROOT / name).write_bytes(output)
        else:
            nodes = [node for node in ast.parse(changed).body
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in FUNCTIONS]
            lines = changed.splitlines(True)
            fixture = '\n\n'.join(''.join(lines[node.lineno-1:node.end_lineno]) for node in nodes)
            (ROOT/'server_functions.py').write_text(fixture, encoding='utf-8', newline='\n')
    (ROOT/'BASELINE.json').write_text(json.dumps(baseline, indent=2), encoding='utf-8')
    print(json.dumps({'modified_runtime_files': len(baseline), 'server_preamble_copied': False}))


if __name__ == '__main__':
    build()
