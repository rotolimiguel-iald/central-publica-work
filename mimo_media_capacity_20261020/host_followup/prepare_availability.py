"""Prepare only availability; keep all historic routing receipts unchanged."""
import ast,difflib,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent/'availability_R1';HERE.mkdir(exist_ok=True)
LIVE=Path('C:/IALD/projetos_pyhton/IALD/iald_auto_router.py')
raw=LIVE.read_bytes();before=raw.decode().replace('\r\n','\n');tree=ast.parse(before)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='available')
replacement='''def _verified_local_routing_refusal(row):
    if row.get('status')!='failed_or_uncertain' or row.get('error_type')!='BudgetRefusal':return False
    health=row.get('connection_health',{})
    if (health.get('status')=='response_received' and health.get('http_status')==200
            and health.get('model')=='jev-1.13.0' and isinstance(health.get('response_sha256'),str)
            and len(health['response_sha256'])==64
            and all(c in '0123456789abcdef' for c in health['response_sha256'])):return True
    # Legacy repair is additive evidence, never an edited route or fake success.
    evidence=json.loads((Path(ROOT)/'iald_jev_connection_evidence.json').read_bytes())
    raw=json.dumps(row,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()
    entry=evidence.get('verified_local_refusals',{}).get(hashlib.sha256(raw).hexdigest())
    if not isinstance(entry,dict) or entry.get('request_sha256')!=row.get('request_sha256'):return False
    digest=entry.get('response_artifact_sha256','')
    if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):return False
    path=Path('C:/IALD/MEMORIA_IALD/state/activity_artifacts')/(digest+'.json')
    response_raw=path.read_bytes()
    if hashlib.sha256(response_raw).hexdigest()!=digest:return False
    artifact=json.loads(response_raw)
    if artifact.get('context_id')!=entry.get('context_id') or artifact.get('scope')!=entry.get('scope'):return False
    payload=artifact['payload']
    wire=payload['wire_utf8'].encode('utf-8')
    if hashlib.sha256(wire).hexdigest()!=payload['wire_sha256'] or len(wire)!=payload['wire_bytes']:return False
    data=json.loads(wire);answer=data['answers']['media_policy']
    result_digest=entry.get('result_artifact_sha256','')
    if len(result_digest)!=64 or any(c not in '0123456789abcdef' for c in result_digest):return False
    result_raw=(path.parent/(result_digest+'.json')).read_bytes()
    if hashlib.sha256(result_raw).hexdigest()!=result_digest:return False
    result_artifact=json.loads(result_raw)
    if result_artifact.get('context_id')!=artifact['context_id'] or result_artifact.get('scope')!=artifact['scope']:return False
    result=result_artifact['payload']['data']['result']
    if result.get('http_status')!=200 or result['response']['ref']['sha256']!=digest:return False
    return (entry.get('http_status')==200 and data.get('model')=='jev-1.13.0'
            and entry.get('reason')=='MEDIA_POLICY_CONFIDENCE_BELOW_REQUIRED_THRESHOLD'
            and type(answer.get('confidence')) in (int,float) and 0<=answer['confidence']<.7)


def available():
    try:
        # Backend ready is the existing validated connection/activation receipt;
        # a route decision is not a connection probe or a successful execution.
        if backend().availability().get('status')!='ready':return False
        for row in report():
            status=row.get('status')
            if status=='started':continue
            # Only the dedicated local media-budget/policy exception is safe to
            # ignore here. Network/auth/protocol/unknown failures stay closed.
            # Never change the failed receipt, retry it, or promote it to selected.
            if _verified_local_routing_refusal(row):continue
            return status=='selected'
        return False  # No prior selected validation; never manufacture success.
    except Exception:return False
'''
lines=before.splitlines(True);after=''.join(lines[:node.lineno-1])+replacement+''.join(lines[node.end_lineno:]);ast.parse(after)
needle="        if data['answers']['executor'].get('type')!='choice':raise ValueError('Invalid executor type')"
insert=needle+"\n        if data.get('model')=='jev-1.13.0':\n            record['connection_health']=dict(status='response_received',http_status=200,model=data['model'],\n                response_sha256=hashlib.sha256(encode(data)).hexdigest())"
assert needle in after;after=after.replace(needle,insert,1);ast.parse(after)
staged=after.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode()
(HERE/'iald_auto_router.py').write_bytes(staged)
(HERE/'availability.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='runtime/iald_auto_router.py',tofile='staging/iald_auto_router.py')),encoding='utf-8')
(HERE/'BASELINE.json').write_text(json.dumps(dict(path=str(LIVE),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),indent=2),encoding='utf-8')
