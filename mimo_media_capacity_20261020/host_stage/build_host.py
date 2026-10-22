"""Build assigned host files in staging; never import or write the live server."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIVE = Path('C:/IALD/projetos_pyhton/IALD')
raw = (LIVE / 'iald_web_server.py').read_bytes()
original = raw.decode('utf-8').replace('\r\n', '\n')
source = original
source = source.replace('import iald_task_policy as task_policy',
    'import new_private_media_host as private_media_host\n'
    'from private_media_store import MediaError, MediaUnavailable, contains_refs, MAX_RAW_BYTES\n'
    'from iald_media_budget import BudgetRefusal as MediaBudgetError\n'
    'import iald_task_policy as task_policy', 1)
source = source.replace('        if self.path == "/v1/chat/completions":',
    '        if self.path == "/api/private-media" and self.method == "POST":\n'
    '            return MAX_RAW_BYTES\n'
    '        if self.path == "/v1/chat/completions":', 1)
helpers = '''
def _private_media_origin_ok():
    origin = request.headers.get('Origin', '')
    origins = set(ORIGENS_APP) | {URL_PUBLICA.rstrip('/'), request.host_url.rstrip('/')}
    if origin and origin not in origins:return False
    if request.headers.get('Sec-Fetch-Site') == 'cross-site' and origin not in ORIGENS_APP:return False
    if not origin and not getattr(g,'app_bearer',False) and request.method != 'GET':return False
    return True


def _private_runtime_for(req_json,user,*,automatic=False):
    if not private_media_host.has_private_or_typed_media(req_json.get('messages')):return None
    conversation=req_json.get('iald_conv') or getattr(g,'iald_private_conversation',None)
    return PRIVATE_MEDIA_HOST.runtime(user,req_json.get('messages'),conversation,automatic=automatic)


def _private_preview_body(client,user,registro,runtime):
    # Same full public science and complete history as the answering engine.
    package=_load_shared_science_package()
    if not package.prefix or _memoria_modo_integral(MOTORES_CFG) or iald_motor_claude.MARCA_ATLAS_INTEGRAL in package.prefix:
        raise MediaError('Unverified public science')
    profile,search_instruction=iald_motores.extrair_do_cliente(client)
    note='Modelo de inferência: '+app_providers.MODELS['mimo']['label']+'. Preserve o regime IALD e os estatutos das fontes. '
    note += 'Use LaTeX com delimitadores \\\\( \\\\) ou \\\\[ \\\\]. Nunca altere uma fórmula apenas para mudar sua apresentação.'
    note += '\\n'+task_policy.INSTRUCTIONS
    if search_instruction:note += '\\n'+iald_motores.LUPA_CANONICA
    messages=app_providers.wire_messages(client,package.prefix,note+('\\nUSER CONTEXT:\\n'+profile if profile else ''),
        provider='mimo',images_authorized=True,media_authorized=True,private_media=runtime)
    definitions=iald_kernel.tool_definitions()+iald_core_indexado.tool_definitions()+iald_fontes_publicas.tool_definitions()
    definitions += [t for t in _ferramentas_para('app') if (t.get('function') or {}).get('name') in app_providers.TOOL_NAMES]
    definitions=list({t['function']['name']:t for t in definitions if t['function']['name'] in app_providers.TOOL_NAMES}.values())
    # Pure definition construction; do not create a task/sandbox to estimate it.
    definitions += task_session.definitions(task_artifacts.TOOL_DEFINITION)
    if operator_bench.is_operator(registro,user):definitions += list(operator_bench.TOOLS)
    return dict(model=app_providers.MODELS['mimo']['model'],messages=messages,tools=definitions,
        stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})


'''
source = source.replace('@app.route(\'/api/task-capabilities\')',helpers+"@app.route('/api/task-capabilities')",1)
source = source.replace("    capabilities=dict(task_policy.capabilities())", "    capabilities=dict(task_policy.capabilities())\n    capabilities.update(PRIVATE_MEDIA_HOST.capabilities(user))",1)
source = source.replace('        capabilities = media_capabilities()',
    '        capabilities = media_capabilities()\n        capabilities.update(PRIVATE_MEDIA_HOST.capabilities(user))',1)
source = source.replace('    # ── SELO IALD (22/09/2026)',
    "    g.iald_private_conversation = req_json.get('iald_conv') if isinstance(req_json,dict) else None\n    # ── SELO IALD (22/09/2026)",1)

def get_function(text,name):
    node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
    return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

auto=get_function(source,'_chat_automatico_autorizado')
auto=auto.replace("        media = app_providers.request_media(client)",
    "        private_media = _private_runtime_for(req_json,user,automatic=True)\n"
    "        if private_media is not None:\n"
    "            client=private_media.canonicalize(client,provider='mimo')\n"
    "            req_json=dict(req_json,messages=client)\n"
    "        media = app_providers.request_media(client)",1)
auto=auto.replace('images_authorized=has_media,media_authorized=has_media)',
                  'images_authorized=has_media,media_authorized=has_media,private_media=private_media)',1)
auto=auto.replace('        chosen,receipt=app_router.choose(',
    "        media_budget_options=None\n"
    "        if private_media is not None:\n"
    "            private_media.authorize_dispatch()\n"
    "            preview=_private_preview_body(client,user,registro,private_media)\n"
    "            policies=private_media_host.video_proposals(private_media.budget_metadata(client))\n"
    "            media_budget_options=private_media.routing_options(preview,proposals=policies)\n"
    "        chosen,receipt=app_router.choose(",1)
auto=auto.replace('multimodal=has_media,media=media,media_integrated=has_media)',
                  'multimodal=has_media,media=media,media_integrated=has_media,media_budget_options=media_budget_options)',1)
auto=auto.replace('        # Recheck permissions/consent',
    "        if private_media is not None:\n"
    "            if chosen!='mimo':raise MediaUnavailable('Incompatible private media destination')\n"
    "            selected_media_plan=private_media.select_routing_policy(receipt['media_policy_id'])\n"
    "            if selected_media_plan!=receipt['media_budget']:raise MediaError('Changed policy receipt')\n"
    "        # Recheck permissions/consent",1)
auto=auto.replace('response=_chat_avaliacao(req_json,user,selected,is_stream,chosen,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction)',
    "response=_chat_avaliacao(req_json,user,selected,is_stream,chosen,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction,private_media=private_media,media_admission=receipt.get('media_budget'))",1)
auto=auto.replace('    except app_router.RoutingContextOverflow:',
    "    except MediaUnavailable:\n"
    "        return _sse_aviso(private_media_host.PUBLIC_REFERENCE_REFUSAL,'anexo_indisponivel')\n"
    "    except (MediaError,MediaBudgetError):\n"
    "        return _sse_aviso(private_media_host.PUBLIC_BUDGET_REFUSAL,'anexo_excede_contexto')\n"
    "    except app_router.RoutingContextOverflow:",1)
source=source.replace(get_function(source,'_chat_automatico_autorizado'),auto,1)

evaluation=get_function(source,'_chat_avaliacao')
evaluation=evaluation.replace('routing_instruction=None):','routing_instruction=None, private_media=None, media_admission=None):',1)
evaluation=evaluation.replace("        profile, search_instruction = iald_motores.extrair_do_cliente(client or [])",
    "        private_media=private_media or _private_runtime_for(req_json,user,automatic=False)\n"
    "        if private_media is not None:\n"
    "            if motor!='mimo':raise MediaUnavailable('Incompatible media destination')\n"
    "            client=private_media.canonicalize(client,provider=motor)\n"
    "            if media_admission is not None and private_media.video_policy!=media_admission['policy']:\n"
    "                raise MediaError('Selected media policy changed')\n"
    "        profile, search_instruction = iald_motores.extrair_do_cliente(client or [])",1)
evaluation=evaluation.replace("media_authorized=(motor=='mimo' and consent['dado']))",
    "media_authorized=(motor=='mimo' and consent['dado']),private_media=private_media)",1)
start=evaluation.index("        admission = {'messages': messages, 'tools': definitions}")
end=evaluation.index('    except (ValueError, OSError, TypeError, KeyError):',start)
evaluation=evaluation[:start]+'''        admission = {'messages': messages, 'tools': definitions}
        if private_media is not None:
            private_media.authorize_dispatch()
            full_body=dict(model=app_providers.MODELS[motor]['model'],messages=messages,tools=definitions,
                stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
            media_admission=private_media.admit(full_body,app_providers.MODELS[motor]['output'])
        else:
            reserve = (app_providers.MODELS[motor]['output'] if motor == 'kimi' else
                app_providers.output_budget(admission, app_providers.MODELS[motor]['output']))
            app_providers.check_window(admission, reserve)
    except MediaUnavailable:
        return _sse_aviso(private_media_host.PUBLIC_REFERENCE_REFUSAL,'anexo_indisponivel')
    except (MediaError,MediaBudgetError):
        return _sse_aviso(private_media_host.PUBLIC_BUDGET_REFUSAL,'anexo_excede_contexto')
'''+evaluation[end:]
evaluation=evaluation.replace('task_tool_names=_task_scope_names(task_scope))',
    'task_tool_names=_task_scope_names(task_scope),private_media=private_media)',1)
source=source.replace(get_function(source,'_chat_avaliacao'),evaluation,1)
# Include private refs in the existing manual-executor rejection before dispatch.
source=source.replace("part.get('type') in ('input_audio','video_url')", "part.get('type') in ('input_audio','video_url','iald_media')")
registration='''
# Lazy encrypted attachment custody; account generation is already defined above.
PRIVATE_MEDIA_HOST = private_media_host.Host(SERVE_DIR,generation=_chat_account_generation,
    users=load_users_estrito,allowed=app_router.allowed,app_memory=app_memory,
    dispatch_guard=_dispatch_guard,budget_available=_automatic_budget_available,
    rates=app_providers.MODELS['mimo']['rates'],
    validate_upload=__import__('iald_mimo_multimodal').validate_upload)
PRIVATE_MEDIA_HOST.admitted_task = lambda:wallet_runtime.current() if wallet_runtime.enabled() else None
PRIVATE_MEDIA_ROUTES = private_media_host.register(app,PRIVATE_MEDIA_HOST,
    authenticated_user=lambda:session.get('username','') if session.get('authenticated') else '',
    binary_origin_ok=_private_media_origin_ok,json_guard=_identificacao_json_post)

'''
source=source.replace('if __name__ == "__main__":',registration+'if __name__ == "__main__":',1)
ast.parse(source)
newline='\r\n' if raw.count(b'\r\n') else '\n'
staged=source.replace('\n',newline).encode('utf-8')
(HERE/'iald_web_server.py').write_bytes(staged)
(HERE/'server_glue.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),source.splitlines(True),fromfile='runtime/iald_web_server.py',tofile='host_stage/iald_web_server.py')),encoding='utf-8')

# Goodall's narrow reservation change; production PublicAccount remains untouched.
p=LIVE/'iald_app_spend.py';before=p.read_bytes();spend=before.decode().replace('\r\n','\n')
spend=spend.replace('def before(self, provider, body, input_bound):','def before(self, provider, body, input_bound, *, media_plan=None):',1)
spend=spend.replace("                size = len(json.dumps(body, ensure_ascii=False, allow_nan=False).encode('utf-8'))",'''                if media_plan is not None:
                    if provider!='mimo':raise ValueError('Media budgets are MiMo-only')
                    import iald_media_budget
                    checked=iald_media_budget.spending_bound(body,media_plan)
                    if input_bound!=checked:raise ValueError('Changed multimodal bound')
                    size=iald_media_budget.text_bound(body)
                else:
                    size = len(json.dumps(body, ensure_ascii=False, allow_nan=False).encode('utf-8'))''',1)
spend=spend.replace('cap = (input_bound * max(rates[0], rates[1]) + maximum * rates[2]) / 1_000_000',
    "cap = (input_bound * max(rates[0], rates[1]) + (output if media_plan is not None else maximum) * rates[2]) / 1_000_000\n                if media_plan is not None:cap=max(cap,media_plan['reservation_usd'])",1)
ast.parse(spend);(HERE/'iald_app_spend.py').write_bytes(spend.replace('\n','\r\n' if before.count(b'\r\n') else '\n').encode())
sha=lambda b:hashlib.sha256(b).hexdigest()
(HERE/'BASELINE.json').write_text(json.dumps({'server_sha256':sha(raw),'spend_sha256':sha(before),'new_module':'new_private_media_host.py','runtime_writes':False},indent=2),encoding='utf-8')
print(json.dumps({'status':'STAGED','server_bytes':len(staged),'runtime_writes':False}))
