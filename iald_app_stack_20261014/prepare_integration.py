"""Prepare current server-only compatibility changes and a measured shared package."""
from prepare_science import W,S,R,C,save,write,sha
import json

def main():
    baseline={row['name']:row for row in json.loads((W/'routing/baseline.json').read_bytes())}
    current=(R/'iald_web_server.py').read_bytes()
    assert sha(current)==baseline['iald_web_server.py']['sha256']
    text=current.decode('utf-8').replace('\r\n','\n')
    pairs=[
        ('# Keep other providers on their audited compact v390 prefix. Its old count\n    # is provenance only; each connector still admits its own actual request.',
         '# Shared semantic package tracks the active scientific release. Anthropic\n    # measurement is provenance only; each connector admits its actual request.'),
        ('source_sha=KERNEL_EXTERNO.source_sha, expected_model=_LEGACY_HAIKU_PROFILE.model)',
         'source_sha=KERNEL_EXTERNO.source_sha, expected_model=_HAIKU_PROFILE.model)'),
        ('    _verify_haiku_tools(wire, snapshot)\n    return package',
         '    _verify_haiku_tools(wire, snapshot, trusted_tools=wire["tools"])\n    return package'),
        ("        app_providers.check_window({'messages': messages, 'tools': definitions}, app_providers.MODELS[motor]['output'])",
         "        admission = {'messages': messages, 'tools': definitions}\n        reserve = (app_providers.MODELS[motor]['output'] if motor == 'kimi' else\n            app_providers.output_budget(admission, app_providers.MODELS[motor]['output']))\n        app_providers.check_window(admission, reserve)"),
    ]
    for a,b in pairs:
        assert text.count(a)==1, a
        text=text.replace(a,b)
    compile(text,'iald_web_server.py','exec')
    rendered=text.replace('\n','\r\n').encode() if b'\r\n' in current else text.encode()
    save(W/'integration/iald_web_server.py',rendered)
    provider=(R/'iald_app_providers.py').read_bytes()
    ptext=provider.decode('utf-8').replace('\r\n','\n')
    budget='''def output_budget(payload, maximum):
    """Reserve the largest safe output without reducing any input or memory.

    UTF-8 size is a conservative admission bound, not measured provider tokens.
    The 128-byte allowance covers the output field added after this calculation.
    Reject before loading credentials if a useful response cannot be reserved.
    """
    if type(maximum) is not int or maximum < 1:
        raise ValueError('Invalid output maximum')
    used = len(json.dumps(payload, ensure_ascii=False).encode('utf-8'))
    available = WINDOW - used - 4096 - 128
    reserve = min(maximum, available)
    if reserve < min(16384, maximum):
        raise ValueError('A memória e esta conversa não deixam espaço seguro para a resposta. '
                         'Nada foi enviado; o núcleo e o histórico foram preservados.')
    return reserve


'''
    assert ptext.count('def check_window(payload, reserve):')==1
    ptext=ptext.replace('def check_window(payload, reserve):',budget+'def check_window(payload, reserve):')
    replacements=[
        ("            body['max_tokens' if provider == 'deepseek' else 'max_completion_tokens'] = spec['output']\n",''),
        ("            bound = check_window(body, spec['output'])", "            reserve = output_budget(body, spec['output'])\n            body['max_tokens' if provider == 'deepseek' else 'max_completion_tokens'] = reserve\n            bound = check_window(body, reserve)"),
        ("dict(status='dispatched', usage=None, input_bytes_bound=bound)","dict(status='dispatched', usage=None, input_bytes_bound=bound, output_reserved_tokens=reserve)"),
        ("dict(status='completed', input_bytes_bound=bound, **measured)","dict(status='completed', input_bytes_bound=bound, output_reserved_tokens=reserve, **measured)"),
    ]
    for a,b in replacements:
        assert ptext.count(a)==1,a
        ptext=ptext.replace(a,b)
    compile(ptext,'iald_app_providers.py','exec')
    pdata=ptext.replace('\n','\r\n').encode() if b'\r\n' in provider else ptext.encode()
    save(W/'integration/iald_app_providers.py',pdata)
    write(W/'integration/baseline.json',{'iald_web_server.py':baseline['iald_web_server.py'], 'iald_app_providers.py':{'name':'iald_app_providers.py','sha256':sha(provider)}})
    shared=S/'shared_count'
    prefix=(S/'memory_stage/shared_prefix.md').read_bytes()
    save(shared/'package/prefix.md',prefix)
    prov=json.loads((S/'public_memory_provenance.json').read_bytes())
    prov.update(prefix_sha256=sha(prefix),coverage='ALL_CURRENT_CORE_TOPICS_SEMANTIC_COMPACT_FULL_SOURCES_RETRIEVABLE')
    write(shared/'public_memory_provenance.json',prov)
    code=(S/'count_package.py').read_text(encoding='utf-8').replace('FULL_PUBLIC_CONTEXT_V392_NOT_PRIVATE_ATLAS_NOT_ALL_LEAN_FILES_IN_PROMPT','SEMANTIC_COMPACT_V392_ALL_TOPICS_RETRIEVABLE_NOT_PRIVATE_ATLAS')
    save(shared/'count_package.py',code.encode())
    write(W/'integration/changes.json',{'server_source_sha256':sha(current),'candidate_sha256':sha(rendered),'changes':['load shared package measured for current Haiku5.5 while keeping per-connector actual request guards','validate seven fixed Haiku tool schemas plus server-owned ACOM scope; no client schemas accepted'],'client_files_changed':False})
    print('INTEGRATION_STAGED')

if __name__=='__main__': main()
