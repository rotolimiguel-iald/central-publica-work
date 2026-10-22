import json
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.coordination import Coordination
from iald_orchestrator.transport import Transport

class TransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.runtime = Runtime(self.tmp.name, recover=False)
        self.c = Coordination(self.runtime)
        self.t = Transport(self.c)
        self.config = {'enabled': True, 'new_project_tasks_authorized': True}
        self.p = patch('iald_orchestrator.transport.configuration', return_value=self.config)
        self.p.start()
        self.source = patch.object(self.runtime, 'source_status', return_value={'ok': True})
        self.source.start()
    def tearDown(self):
        self.source.stop(); self.p.stop(); self.tmp.cleanup()
    def job(self):
        return self.t.submit('Resuma este teste de transporte.', str(uuid.uuid4()))
    def test_idle_does_not_discover_or_call_providers(self):
        with patch('iald_orchestrator.providers.discover') as discover, patch('iald_orchestrator.providers.execute') as execute:
            self.assertEqual(self.t.next_job()['state'], 'idle')
            discover.assert_not_called(); execute.assert_not_called()
    def test_resume_active_before_new_request(self):
        a = self.job(); b = self.job()
        self.c.act(b['id'], 'begin_draft')
        self.assertEqual(self.t.next_job()['job']['id'], b['id'])
    def test_missing_creation_authorization_blocks_new_handoff(self):
        self.job(); self.config['new_project_tasks_authorized'] = False
        self.assertEqual(self.t.next_job()['state'], 'needs_project_task_authorization')
    def test_disabled_never_advances_job(self):
        j = self.job(); self.config['enabled'] = False
        self.assertEqual(self.t.next_job()['state'], 'paused')
        self.assertEqual(self.c.get(j['id'])['stage'], 'awaiting_dispatch')
    def test_submit_is_idempotent(self):
        rid = str(uuid.uuid4())
        a = self.t.submit('Pedido autorizado.', rid)
        self.assertEqual(a['id'], self.t.submit('Pedido autorizado.', rid)['id'])
        with self.assertRaises(ValueError): self.t.submit('Pedido diferente.', rid)
    def test_terminal_jobs_are_not_replayed(self):
        j = self.job(); self.c.act(j['id'], 'cancel')
        self.assertEqual(self.t.next_job()['state'], 'idle')
    def test_receipt_has_no_prompt_and_keeps_byte_backup(self):
        j = self.job(); self.t.receipt('progress', j['id'])
        p = Path(self.tmp.name)/'transport_last_check.json'; old = p.read_bytes()
        self.t.receipt('completed', j['id'])
        self.assertEqual(next(p.parent.glob(p.name+'.bak_*')).read_bytes(), old)
        self.assertNotIn('prompt', json.loads(p.read_bytes()))

if __name__ == '__main__': unittest.main()
