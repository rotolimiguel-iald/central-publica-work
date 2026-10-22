import sys,json,socket
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'backend'))
import test_backend as t
case=t.Routes('test_session_capabilities_legacy_account');case.setUp()
try:
    with patch.object(t.wire,'decode_request',side_effect=AssertionError('decode must not run')):
        r=case.client.post('/api/chat-jobs',json=case.wrapped(case.payload()),base_url='http://demo.iald.ia.br',headers={'Origin':'https://demo.iald.ia.br','X-Forwarded-Proto':'https'})
    # Separate cookie domain must be authenticated explicitly for this simulation.
    with case.client.session_transaction(base_url='http://demo.iald.ia.br') as s:s.update(authenticated=True,username='alice')
    with patch.object(t.wire,'decode_request',side_effect=AssertionError('decode must not run')):
        r=case.client.post('/api/chat-jobs',json=case.wrapped(case.payload()),base_url='http://demo.iald.ia.br',headers={'Origin':'https://demo.iald.ia.br','X-Forwarded-Proto':'https'})
    assert r.status_code==403 and r.json['code']=='transport_auth_or_csrf'
    result={'status':403,'code':r.json['code'],'origin':'https://demo.iald.ia.br','wsgi_host_url':'http://demo.iald.ia.br','forwarded_proto_does_not_rewrite_without_trusted_middleware':True,'admissions':len(case.begins),'scope':'Synthetic WSGI proxy topology matches source HTTP waitress without trusted proxy/url_scheme config; no live request observed.'}
    # Exercise actual staged page route fallback with a valid large legacy page.
    page=json.loads((ROOT/'legacy_page.json').read_bytes())
    with patch.object(t.jobs.ChatJobs,'get',return_value=page):
        page_response=case.client.get('/api/chat-jobs/'+page['id']+'?after=0&iald_transport='+t.wire.QUERY)
    assert page_response.status_code==200 and 'iald_transport' not in page_response.json
    assert len(page_response.data)>t.wire.PAGE_LIMIT
    result['actual_route_legacy_fallback_bytes']=len(page_response.data)
    (ROOT/'PROXY_RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
finally:case.doCleanups()
