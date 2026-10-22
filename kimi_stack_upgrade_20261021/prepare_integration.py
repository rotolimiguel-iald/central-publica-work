"""Prepare local retrieval integration without touching the running stack."""
from pathlib import Path
import hashlib,json
import task
task.check('integration_prepare')
base=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
out=task.W/'integration';out.mkdir(exist_ok=True)
pins=[]
for rel in ['transport_cli.py','iald_orchestrator/nos_packet.py']:
    src=base/rel;raw=src.read_bytes();text=raw.decode('utf8')
    pins.append(dict(path=str(src),sha256=hashlib.sha256(raw).hexdigest()))
    if rel=='transport_cli.py':
        text=text.replace('    transport = Transport()\n    operation = request.get(\'operation\')', '''    operation = request.get('operation')
    if operation == 'retrieve_knowledge':
        from iald_orchestrator.layered_retrieval import retrieve
        if not isinstance(request, dict) or set(request) - {'operation','query','budget_bytes','mandatory_ids'}:
            raise ValueError('Invalid local retrieval request')
        result = retrieve(request['query'], budget_bytes=request.get('budget_bytes',48000),
                          mandatory_ids=request.get('mandatory_ids',()))
        print(json.dumps(result, ensure_ascii=False))
        return
    transport = Transport()''')
    else:
        text=text.replace('    parts=[header]; refs=[]; seen=set(); rejected=0','''    from .layered_retrieval import rank_nodes
    hits = rank_nodes([dict(row) for row in hits], u['titulo']+' '+u.get('criterio_de_fechado',''))
    if len(header) > max_chars:
        raise ValueError('Required scientific header exceeds packet budget')
    parts=[header]; refs=[]; seen=set(); rejected=0; skipped_budget=0''')
        text=text.replace('''        chosen=block[:remaining]
        parts.append(chosen)''','''        if len(block)>remaining:
            skipped_budget+=1
            continue
        chosen=block
        parts.append(chosen)''')
        text=text.replace('"allowed_sources":allowed_sources,"no_permitted_source_hits":not refs,','''"allowed_sources":allowed_sources,"no_permitted_source_hits":not refs,
             "ranking_policy":"layered-relevance-v1","whole_blocks":True,
             "skipped_budget":skipped_budget,"retrieval_scope":"CANDIDATES_ONLY_NOT_EXHAUSTIVE",''')
    dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(text.encode())
task.new('integration/BASELINE.json',pins)
print('PREPARED')
