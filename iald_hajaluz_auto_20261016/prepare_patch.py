from pathlib import Path
import hashlib,json,ast
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
for d in ('baseline','staging','validation'):(W/d).mkdir(exist_ok=True)
def baseline(name):
    p=W/'baseline'/name
    if not p.exists():
        with p.open('xb') as f:f.write((R/name).read_bytes())
    return p.read_bytes().decode('utf-8')
def replace(text,old,new):
    assert text.count(old)==1, old[:100]
    return text.replace(old,new)
def save(name,text):
    ast.parse(text)
    p=W/'staging'/name; data=text.encode()
    tmp=p.with_suffix('.tmp');tmp.write_bytes(data);assert tmp.read_bytes()==data;tmp.replace(p)
m=baseline('iald_app_memory.py')
m=replace(m,"'projection_receipt': packet['receipt'], 'scope': 'SCOPED_OPERATIONAL_DATA_NO_AUTHORITY'}", """'projection_receipt': packet['receipt'], 'scope': 'SCOPED_OPERATIONAL_DATA_NO_AUTHORITY',
            'coverage': {'required_chars': packet['required_chars'], 'actual_chars': packet['actual_chars'],
                         'omitted_records': len(packet['omitted_record_ids']),
                         'projection_sha256': packet['projection_sha256'],
                         'policy': 'whole_optional_records_only; complete_ledger_recoverable_by_memory_id_and_revision'}}""")
save('iald_app_memory.py',m)
r=baseline('iald_auto_router.py')
r=replace(r,'import iald_app_memory as app_memory','import iald_app_memory as app_memory\nimport iald_bootstrap_intent as bootstrap_intent')
insert='''class RoutingContextOverflow(jev_control.ControlError):
    """Required state cannot fit; no provider request has been sent."""


def _fit_routing_payload(body):
    """Fit only routing retrieval. Never truncate an inscription or executor context.

    ACOM selects whole optional candidate records; mandatory decisions, pending
    operations and their correction lineage remain complete or visibly refuse.
    Counts use the same escaped JSON encoding as check_payload, not characters.
    """
    size = lambda value: len(json.dumps(value, ensure_ascii=True, allow_nan=False).encode('ascii'))
    longest = max(size(q) for q in body['questions'].values())
    def excess():
        state = size(body['state'])
        return max(state - jev_control.MAX_STATE_BYTES, state + longest - 32000,
                   size(body) - jev_control.MAX_REQUEST_BYTES, 0)
    state = body['state']
    source = dict(state['source'])
    source['coverage'] = 'PARTIAL_ROUTING_CONTEXT'
    state['source'] = source
    common = state.get('common_memory')
    reference = common['projection_receipt'] if common else None
    target = common['coverage']['actual_chars'] if common else 0
    while True:
        source['characters'] = len(state['canonical_memory'])
        over = excess()
        if not over:
            return jev_control.check_payload(body)
        # The scientific excerpt is retrieval, not the source-bound control or
        # the fixed scientific package supplied intact to the answering model.
        if len(state['canonical_memory']) > 1024:
            keep = max(1024, len(state['canonical_memory']) - max(over, 256))
            state['canonical_memory'] = state['canonical_memory'][:keep]
            continue
        if common is not None and target > common['coverage']['required_chars']:
            target = max(common['coverage']['required_chars'], target - max(over, 256))
            try:
                projected = app_memory.routing_state(max_chars=target)
            except app_memory.ProjectionOverflow as exc:
                # The compulsory part may itself exceed the retrieval target.
                projected = app_memory.routing_state(max_chars=exc.required_chars)
                target = exc.required_chars
            if projected is None or projected['projection_receipt'] != reference:
                raise jev_control.ControlError('Operational memory changed during routing admission')
            common = projected
            state['common_memory'] = projected
            continue
        raise RoutingContextOverflow('Required routing context exceeds admission bounds')


'''
r=replace(r,'def choose(prompt,candidates,root=ROOT,',insert+'def choose(prompt,candidates,root=ROOT,')
r=replace(r,"    task=task_policy.classify(prompt)","    intent = None if worker else bootstrap_intent.classify(prompt)\n    task=task_policy.classify(prompt)")
r=replace(r,"    guide=execution_guide.routing_guide", "    if intent is not None:\n        questions['work_path']['instructions'] += '\\n' + bootstrap_intent.instructions()\n        if common_memory is not None:\n            questions['memory_continuity']['instructions'] += '\\n' + bootstrap_intent.instructions()\n    guide=execution_guide.routing_guide")
r=replace(r,"    if common_memory is not None: body['state']['common_memory']=common_memory", "    if common_memory is not None: body['state']['common_memory']=common_memory\n    if intent is not None: body['state']['recognized_intent']=intent")
start=r.index('    # UTF-8 bytes are a conservative admission proxy')
end=r.index('    regime=jev_control.new_receipt',start)
r=r[:start]+'''    encode=lambda value:json.dumps(value,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()
    wire_size=lambda value:len(json.dumps(value,ensure_ascii=True,allow_nan=False).encode('ascii'))
    admission=_fit_routing_payload(body)
    source=body['state']['source']
    common_memory=body['state'].get('common_memory')
    raw=encode(body)
'''+r[end:]
r=replace(r,"'execution_guide_version':execution_guide.VERSION,", "'recognized_intent':intent,\n            'execution_guide_version':execution_guide.VERSION,")
r=replace(r,"    if receipt.get('memory_continuity')=='reconcile':", "    if receipt.get('recognized_intent') is not None:\n        text += '\\n' + bootstrap_intent.instructions()\n    if receipt.get('memory_continuity')=='reconcile':")
save('iald_auto_router.py',r)
w=baseline('iald_web_server.py')
old="    except (ValueError,PermissionError,OSError,KeyError,TypeError,RuntimeError):\r\n        return _sse_aviso('Não foi possível concluir a escolha automática."
new="    except app_router.RoutingContextOverflow:\r\n        return _sse_aviso('A memória obrigatória desta conversa excede o espaço do seletor automático. Nada foi enviado aos provedores. Abra uma nova conversa para continuar; a conversa anterior permanece salva.','roteamento_contexto_excedido')\r\n"+old
w=replace(w,old,new)
save('iald_web_server.py',w)
print(json.dumps({'staged':['iald_auto_router.py','iald_app_memory.py','iald_web_server.py'],'production_modified':False}))
