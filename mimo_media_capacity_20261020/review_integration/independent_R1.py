"""Bounded reviewer controls on captured candidates; no live server import."""
from contextlib import closing
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SNAP = ROOT / 'snapshot_R1'
sys.path[:0] = [str(SNAP/'host_stage'), str(SNAP/'backend_stage'), str(SNAP/'routing_stage'),
               r'C:\IALD\projetos_pyhton\IALD']
def audit(event, args):
    if event in ('socket.connect','socket.getaddrinfo'): raise AssertionError('Network forbidden')
sys.addaudithook(audit)
import private_media_store as media
import iald_media_budget as budget
import test_host


class Cipher:
    def seal(self, raw): return raw
    def open(self, raw): return raw


def facts(raw, mime): return dict(kind='audio',duration_seconds=1,has_audio=True)
def store_at(root): return media.PrivateMediaStore(root,authorize_scope=lambda s:True,validate_media=facts,cipher=Cipher())
SCOPE = media.Scope('synthetic-a','g','draft_first')


if len(sys.argv)>1 and sys.argv[1]=='crash':
    import os
    class Stream:
        def read(self, n): os._exit(21)
    store_at(Path(sys.argv[2])).put(Stream(),scope=SCOPE,mime='audio/wav',content_length=8)
    raise AssertionError('Expected process termination')


def run():
    result = {'actor':'codex-mimo-capacity-reviewer','checks':[],'reproductions':{},
              'provider_calls':0,'production_changes':False}
    def check(name): result['checks'].append(name)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix='own_') as directory:
        folder=Path(directory)
        for deletion in ('conversation','account'):
            store=store_at(folder/deletion)
            def revoke(raw,mime):
                if deletion=='conversation': store.revoke_conversation(SCOPE)
                else: store.revoke_account(SCOPE,authorize_account_deletion=lambda *_:True)
                return facts(raw,mime)
            store.validate_media=revoke
            try:store.put(io.BytesIO(b'fixture!'),scope=SCOPE,mime='audio/wav',content_length=8)
            except media.MediaUnavailable:pass
            else:raise AssertionError('Revocation still returned success')
            assert list(store.blobs.iterdir())==[]
            with closing(store._db()) as db:
                assert db.execute('SELECT status FROM media').fetchall()==[('revoked',)]
            check('M1: '+deletion+' deletion during upload refuses and leaves no orphan')
        for _ in range(4):
            proc=subprocess.run([sys.executable,'-B',str(Path(__file__)),'crash',str(folder/'crash')],capture_output=True)
            assert proc.returncode==21, proc.stderr
        store=store_at(folder/'crash')
        part=store.put(io.BytesIO(b'fixture!'),scope=media.Scope('other','g','first'),mime='audio/wav',content_length=8)
        assert store.metadata(part['media_ref'],media.Scope('other','g','first'))==part
        with closing(store._db()) as db:
            assert db.execute("SELECT count(*) FROM media WHERE status='abandoned'").fetchone()[0]==4
        check('M2: four actual crashes recovered; another user admitted by fresh store')

    rates=dict(input=.435,cache_read=.0036,output=.87)
    item=dict(id='a'*32,kind='video',sha256='b'*64,decoded_bytes=12,encoded_bytes=16,
              duration_seconds=1024.1,width=640,height=480,has_audio=False)
    body=dict(messages=[dict(role='system',content='SCIENCE_UNCHANGED'),
                        dict(role='user',content=[dict(type='iald_media',media_ref=item['id'],kind='video')])])
    saved=copy.deepcopy(body)
    plans=budget.options(body,[item],{'2fps':dict(fps=2.,media_resolution='default'),
                                    '1fps':dict(fps=1.,media_resolution='default')},rates=rates)
    assert plans['2fps']['status']=='REFUSED'
    assert plans['1fps']['status']=='ESTIMADO'
    assert plans['1fps']['items'][0]['requested_frames']==1025
    assert plans['1fps']['items'][0]['sampled_frames']==1026
    assert body==saved
    check('2048 coverage: 1024.1s at2fps refused; explicit1fps covers duration without body mutation')
    disallowed=budget.options(body,[item],{'1fps':dict(fps=1.,media_resolution='default')},rates=rates,intent_limits={'min_fps':2})
    assert disallowed['1fps']['status']=='REFUSED'
    check('Intent minimum FPS prevents cheaper policy substitution')
    view=budget.routing_options(plans);encoded=json.dumps(view)
    assert all(x not in encoded for x in ('media_ref','sha256','SCIENCE_UNCHANGED','data:'))
    check('JEV policy projection contains only whitelisted metadata/cost numbers')
    body['messages'].append(dict(role='assistant',content='TOOL_RESULT_EXACT'))
    body['max_completion_tokens']=plans['1fps']['output_reserved_tokens']
    try:budget.spending_bound(body,plans['1fps'])
    except budget.BudgetRefusal:pass
    else:raise AssertionError('Changed history accepted under old reservation')
    check('Changed history/tool result requires fresh local plan before wallet reservation')

    host=test_host.HostTests(methodName='runTest');host.setUp()
    try:
        app,_=host.app();client=app.test_client()
        with client.session_transaction() as session: session.update(authenticated=True,username='alice')
        alice_scope=host.host.capabilities('alice')['media_scope']
        # Another tab changes the authenticated cookie after the old tab read capabilities.
        with client.session_transaction() as session: session.update(authenticated=True,username='bob')
        response=client.post('/api/private-media?conversation_id=c_test',data=test_host.wav(),
                             content_type='audio/wav',headers={'Origin':'http://localhost'})
        assert response.status_code==201,response.get_json()
        part=response.get_json()
        with closing(host.host.store._db()) as db:
            owner,generation=db.execute('SELECT owner,generation FROM media WHERE id=?',(part['media_ref'],)).fetchone()
        assert owner=='bob' and generation=='gb'
        result['reproductions']['account_switch_upload']={
            'old_client_partition':alice_scope,'new_server_owner':'bob','status':response.status_code,
            'request_has_expected_partition':False,'stored_under_new_account':True,
            'canonical_response_has_owner_generation_or_partition':bool(set(part)&{'owner','generation','media_scope'}),
            'scope':'Actual staged Flask registration/Host callbacks; synthetic session changes and local WAV only'}
    finally: host.doCleanups()
    result['passed']=True
    output=ROOT/'INDEPENDENT_CONTROLS_R1.json'
    raw=json.dumps(result,ensure_ascii=False,indent=2).encode();temp=output.with_suffix('.tmp')
    temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.replace(output)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__': run()
