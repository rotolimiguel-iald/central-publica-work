"""Offline security regressions; no Flask, production import, DPAPI or network.

Assertions describe required behavior and intentionally expose unfixed bugs.
All stored data is synthetic and every worker is released during cleanup.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import uuid
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent / 'server'))
import iald_chat_jobs as jobs_module


CLIENT_PROBE = r"""
import {readFileSync} from 'node:fs';
const input=JSON.parse(readFileSync(0,'utf8'));
const module=await import('data:text/javascript;base64,'+readFileSync(input.client).toString('base64'));
const values=new Map();let requests=0;
const jobs=module.createDurableChatJobs({
  storage:{getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)},
  randomUUID:()=>input.body.request_id,
  request:async(path,options)=>{
    if(++requests>4)throw Error('Unexpected retry in audit');
    if(path==='/api/chat-jobs/session')return {ok:true,status:200,json:async()=>({account:input.account})};
    if(path==='/api/chat-jobs')return {ok:true,status:202,json:async()=>input.page};
    return input.expired
      ? {ok:false,status:410,json:async()=>({error:'Esta resposta temporária expirou.'})}
      : {ok:true,status:200,json:async()=>input.page};
  },sleep:async()=>{throw Error('Unexpected polling in audit');}
});
jobs.setOwner(input.account);
const record=await jobs.begin(input.body),events=[];let error=null;
try{for await(const event of jobs.stream(record))events.push(event);}
catch(e){error={name:e.name,message:e.message,httpStatus:e.httpStatus,terminal:e.terminal,pending:e.pending};}
console.log(JSON.stringify({events,error,requests}));
"""


class TestCipher:
    """Reversible test transport only; makes no cryptographic claim."""
    def seal(self, raw): return b'test-only:' + raw[::-1]
    def open(self, raw): return raw[len(b'test-only:'):][::-1]


class ChatJobAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.jobs = jobs_module.ChatJobs(self.tmp.name, cipher=TestCipher())
        self.release = threading.Event()

    def tearDown(self):
        self.release.set()
        deadline = time.monotonic() + 3
        while self.jobs.controls and time.monotonic() < deadline:
            time.sleep(.005)
        self.assertFalse(self.jobs.controls, 'An audit worker was left running')
        self.tmp.cleanup()

    @staticmethod
    def body(conversation='conversation-1'):
        return dict(request_id=str(uuid.uuid4()), iald_conv=conversation, stream=True,
                    messages=[dict(role='user', content='Synthetic audit request')])

    def wait(self, identity):
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            with self.jobs.lock:
                if identity not in self.jobs.controls:
                    return
            time.sleep(.005)
        self.fail('Audit worker did not finish')

    def test_moderation_retraction_clears_text_even_at_storage_limit(self):
        body = self.body()
        forbidden = json.dumps({'choices': [{'delta': {'content': 'REMOVED_TEXT_' * 100}}]})
        withdrawn = json.dumps({'iald_aviso': {'retirar_resposta': True}})
        def produce(*args):
            yield 'data: ' + forbidden + '\n\n'
            yield 'data: ' + withdrawn + '\n\n'
            yield 'data: [DONE]\n\n'
        # Enough room for either event independently, not both together.
        cap = len(self.jobs.cipher.seal(forbidden.encode()))
        with patch.object(jobs_module, 'MAX_EVENT_BYTES', cap):
            self.jobs.submit('alice', body, produce)
            self.wait(body['request_id'])
        result = self.jobs.get('alice', body['request_id'])
        self.assertNotIn('REMOVED_TEXT_', json.dumps(result),
                         'Storage quota prevented moderation from deleting saved answer')

    def test_delete_conversation_keeps_slot_until_old_worker_ends(self):
        entered = threading.Event()
        def blocked(*args):
            entered.set()
            if not self.release.wait(3): raise AssertionError('Audit worker not released')
            yield 'data: [DONE]\n\n'
        first = self.body()
        self.jobs.submit('alice', first, blocked)
        self.assertTrue(entered.wait(2))
        self.jobs.purge('alice', first['iald_conv'])
        self.assertIn(first['request_id'], self.jobs.controls)
        with self.assertRaises(jobs_module.JobError) as error:
            self.jobs.submit('alice', self.body('conversation-2'), blocked)
        self.assertEqual(error.exception.status, 409)

    def test_inflight_append_cannot_repopulate_deleted_conversation(self):
        entered = threading.Event()
        seal = self.jobs.cipher.seal
        def slow_seal(raw):
            entered.set()
            if not self.release.wait(3): raise AssertionError('Audit encryption not released')
            return seal(raw)
        self.jobs.cipher.seal = slow_seal
        body = self.body()
        def produce(*args):
            yield 'data: {"text":"SYNTHETIC_DELETED_TEXT"}\n\n'
            yield 'data: [DONE]\n\n'
        self.jobs.submit('alice', body, produce)
        self.assertTrue(entered.wait(2))
        self.jobs.purge('alice', body['iald_conv'])
        self.release.set();self.wait(body['request_id'])
        with self.jobs.db() as db:
            count = db.execute('SELECT count(*) FROM events WHERE job=?', (body['request_id'],)).fetchone()[0]
        self.assertEqual(count, 0, 'A late append wrote output after deletion acknowledged success')

    def test_get_alone_enforces_seven_day_expiry(self):
        body = self.body()
        def produce(*args):
            yield 'data: {"text":"SYNTHETIC_EXPIRED_TEXT"}\n\n'
            yield 'data: [DONE]\n\n'
        self.jobs.submit('alice', body, produce);self.wait(body['request_id'])
        with self.jobs.db() as db:
            db.execute('UPDATE jobs SET updated=? WHERE id=?',
                       (time.time() - jobs_module.RETENTION - 1, body['request_id']))
        with self.assertRaises(jobs_module.JobError) as error:
            self.jobs.get('alice', body['request_id'])
        self.assertEqual(error.exception.status, 410)

    def client_probe(self, body, page, expired=False):
        node = shutil.which('node')
        if node is None: self.skipTest('Node runtime unavailable; no dependency installation')
        payload = dict(body=body, page=page, expired=expired, account=jobs_module.owner_key('alice'),
                       client=str(Path(__file__).parent / 'client' / 'chat_jobs.js'))
        run = subprocess.run([node, '--input-type=module', '-e', CLIENT_PROBE],
                             input=json.dumps(payload), text=True, encoding='utf-8',
                             capture_output=True, timeout=10, check=True)
        return json.loads(run.stdout)

    def test_reconnect_after_moderation_delivers_withdrawal_notice(self):
        body = self.body()
        def produce(*args):
            yield 'data: {"choices":[{"delta":{"content":"SYNTHETIC_REMOVED"}}]}\n\n'
            yield 'data: {"iald_aviso":{"retirar_resposta":true}}\n\n'
            yield 'data: [DONE]\n\n'
        self.jobs.submit('alice', body, produce);self.wait(body['request_id'])
        page = self.jobs.get('alice', body['request_id'])
        self.assertNotIn('SYNTHETIC_REMOVED', json.dumps(page))
        result = self.client_probe(body, page)
        self.assertTrue(any('retirar_resposta' in event for event in result['events']), result)

    def test_expired_job_is_terminal_for_reconnecting_client(self):
        body = self.body()
        self.jobs.submit('alice', body, lambda *args: iter(['data: [DONE]\n\n']))
        self.wait(body['request_id'])
        page = self.jobs.get('alice', body['request_id'])
        result = self.client_probe(body, page, expired=True)
        self.assertTrue((result['error'] or {}).get('terminal'), result)


if __name__ == '__main__': unittest.main(verbosity=2)
