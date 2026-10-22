"""Generate staged transport against current runtime, never install."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

W=Path(__file__).resolve().parent;R=Path('C:/IALD/projetos_pyhton/IALD')
raw=(R/'iald_app_providers.py').read_bytes();original=raw.decode('utf-8');s=original
def replace(old,new):
    global s
    if s.count(old)==0 and '\n' in old and s.count(old.replace('\n','\r\n'))==1:
        old=old.replace('\n','\r\n')
    assert s.count(old)==1,old
    s=s.replace(old,new,1)
replace('import iald_app_memory as app_memory','import iald_app_memory as app_memory\nfrom private_media_store import contains_refs, contains_media, reject_worker_media, MediaError')
replace('def image_parts(parts, *, images_authorized=False, media_authorized=False):',
    'def image_parts(parts, *, images_authorized=False, media_authorized=False, private_media=None):')
replace("        if part.get('type') in ('input_audio','video_url'):",'''        if part.get('type') == 'iald_media':
            if private_media is None or media_authorized is not True:
                raise MediaError('Private media requires authenticated scope and consent')
            result.append(private_media.canonical_part(part))
            continue
        if part.get('type') in ('input_audio','video_url'):''')
replace("def wire_messages(messages, prefix, profile='', *, provider=None, images_authorized=False, media_authorized=False):",
    "def wire_messages(messages, prefix, profile='', *, provider=None, images_authorized=False, media_authorized=False, private_media=None):")
replace("    result = [{'role': 'system', 'content': prefix + ('\\n\\n' + profile if profile else '')}]",'''    reject_worker_media(messages, provider=provider)
    if contains_refs(messages):
        if private_media is None: raise MediaError('Private media scope required')
        messages = private_media.canonicalize(messages, provider=provider)
    result = [{'role': 'system', 'content': prefix + ('\\n\\n' + profile if profile else '')}]''')
replace("parts = image_parts(item['content'], images_authorized=images_authorized, media_authorized=media_authorized)",
    "parts = image_parts(item['content'], images_authorized=images_authorized, media_authorized=media_authorized, private_media=private_media)")
replace("elif kind in ('image_url','input_audio','video_url'):",'''elif kind == 'iald_media':
                    if part.get('kind') not in ('audio','video'): raise ValueError('Invalid private media kind')
                    counts[part['kind']] += 1
                elif kind in ('image_url','input_audio','video_url'):''')
replace("p.get('type') in ('image_url', 'input_audio', 'video_url')", "p.get('type') in ('image_url', 'input_audio', 'video_url', 'iald_media')")
replace('def observe(self, flow, model, *, rates=None, memory_sha256=None, messages=None):',
    'def observe(self, flow, model, *, rates=None, memory_sha256=None, messages=None, private_media=None):')
# Both observer and stream lifecycle use the same existing stamp, with ref metadata only.
assert s.count('routing_metrics.stamp(record, messages)')==2
s=s.replace('routing_metrics.stamp(record, messages)','routing_metrics.stamp(record, private_media.metrics_view(messages) if private_media is not None else messages)')
replace('task_tool_names=()):\n        """One active request per account.',
    'task_tool_names=(), private_media=None):\n        """One active request per account.')
replace('        scoped_task_names(tools,task_tool_names,authorize)', '''        reject_worker_media(messages, provider=provider, worker=bool(private_media.worker) if private_media is not None else False)
        if contains_refs(messages):
            if private_media is None: raise MediaError('Private media scope required')
            messages = private_media.canonicalize(messages, provider=provider)
        scoped_task_names(tools,task_tool_names,authorize)''')
replace('active_response, record, started, http_post, spending, authorize, task_tool_names)',
    'active_response, record, started, http_post, spending, authorize, task_tool_names, private_media)')
replace('def _api(self, provider, messages, tools, execute_tool, emit, cancel, responses, record, started, http_post, spending=None, authorize=None, task_tool_names=()):',
    'def _api(self, provider, messages, tools, execute_tool, emit, cancel, responses, record, started, http_post, spending=None, authorize=None, task_tool_names=(), private_media=None):')
replace("            reserve = output_budget(body, spec['output'])\n            body['max_tokens' if provider == 'deepseek' else 'max_completion_tokens'] = reserve\n            bound = check_window(body, reserve)",'''            if contains_media(body['messages']):
                if private_media is None: raise MediaError('Private media scope required')
                admission = private_media.admit(body, spec['output'], WINDOW)
                reserve, bound = admission['output_reserved_tokens'], admission['input_tokens_bound']
                record['media_admission'] = admission
            else:
                reserve = output_budget(body, spec['output'])
                bound = check_window(body, reserve)
            body['max_tokens' if provider == 'deepseek' else 'max_completion_tokens'] = reserve'''.replace('\n','\r\n') if '\r\n' in s else '''            if contains_media(body['messages']):
                if private_media is None: raise MediaError('Private media scope required')
                admission = private_media.admit(body, spec['output'], WINDOW)
                reserve, bound = admission['output_reserved_tokens'], admission['input_tokens_bound']
                record['media_admission'] = admission
            else:
                reserve = output_budget(body, spec['output'])
                bound = check_window(body, reserve)
            body['max_tokens' if provider == 'deepseek' else 'max_completion_tokens'] = reserve''')
replace('                if spending is not None: spending.before(provider, body, bound)', '''                if spending is not None:
                    if contains_media(body['messages']): private_media.reserve(spending, body, admission)
                    else: spending.before(provider, body, bound)''')
replace("                record['calls'].append(dict(status='dispatched', usage=None, input_bytes_bound=bound, output_reserved_tokens=reserve))",'''                # Purely local resolution failures are not uncertain remote calls.
                try:
                    wire_body = private_media.expand(body, provider=provider, plan=admission) if contains_media(body['messages']) else body
                except BaseException:
                    if spending is not None: spending.discard_undispatched()
                    raise
                record['calls'].append(dict(status='dispatched', usage=None, input_bytes_bound=bound, output_reserved_tokens=reserve))''')
replace("spec['url'], json=body, headers=headers,", "spec['url'], json=wire_body, headers=headers,")
ast.parse(s)
(W/'iald_app_providers.py').write_text(s,encoding='utf-8',newline='')
(W/'providers.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='a/iald_app_providers.py',tofile='b/iald_app_providers.py')),encoding='utf-8')
(W/'PROVIDER_SOURCE.json').write_text(json.dumps({'runtime_sha256':hashlib.sha256(raw).hexdigest(),'staging_sha256':hashlib.sha256((W/'iald_app_providers.py').read_bytes()).hexdigest(),'runtime_unchanged':raw==(R/'iald_app_providers.py').read_bytes()},indent=2),encoding='utf-8')
