from pathlib import Path
import sys,json,tempfile,unittest
from unittest.mock import patch
from types import SimpleNamespace
W=Path(__file__).resolve().parent
sys.path[:0]=[str(W/'stage'),r'C:\IALD\projetos_pyhton\IALD']
import iald_auto_router as a
import iald_app_providers as p

class RouterTests(unittest.TestCase):
    def test_approved_accounts(self):
        for user in ('guest','alanacaroline','liana'):
            self.assertTrue(a.allowed({'admin':False},user))
        self.assertFalse(a.allowed({'bloqueado':True},'luiz'))
        self.assertTrue(a.allowed({'admin':True},'luiz'))

    def answer(self,choice='mimo',confidence=.9):
        return {'model':'jev-1.13.0','answers':{'executor':{'choice':choice,'confidence':confidence,
            'probabilities':{'mimo':.9,'openai':.1}}},'usage':{'input_tokens':100}}

    def test_decision_does_not_grant_access(self):
        d=self.answer();d['answers']['executor']['choice']='claude-sonnet'
        with self.assertRaises(ValueError):a.parse_answer(d,['mimo','openai'])
        with self.assertRaises(ValueError):a.parse_answer(self.answer(),['openai'])
        for v in (float('nan'),True,-1,2):
            d=self.answer(confidence=v)
            with self.assertRaises(ValueError):a.parse_answer(d,['mimo','openai'])

    def test_low_confidence_before_dispatch_default(self):
        selected,decision=a.parse_answer(self.answer('openai',.3),['mimo','openai'])
        self.assertEqual(selected,'mimo');self.assertEqual(decision['decision_rule'],'operator_default_before_dispatch')

    def test_no_retry_or_prompt_in_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            seen=[]
            def post(*args,**kw):seen.append(args);return SimpleNamespace(status_code=403,close=lambda:None)
            with patch.object(a,'backend',return_value=SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda *x,**k:None,_key=lambda:'test-key',ENDPOINT='https://example.invalid')):
                with patch.object(a,'memory_slice',return_value=('public text',{'release':'test'})):
                    with self.assertRaises(ValueError):a.choose('private test prompt',['mimo','openai'],root=Path(tmp),post=post,validation_probe=True)
            self.assertEqual(len(seen),1)
            text=json.dumps(a.report(Path(tmp)))
            for secret in ('private test prompt','test-key'):self.assertNotIn(secret,text)
            self.assertIn('403',text)

    def test_selected_receipt_and_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(a,'backend',return_value=SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda *x,**k:None,_key=lambda:'test-key',ENDPOINT='https://example.invalid')):
                with patch.object(a,'memory_slice',return_value=('public text',{'release':'test'})):
                    selected,r=a.choose('Explain a theorem',['mimo','openai'],root=Path(tmp),post=lambda *x,**k:SimpleNamespace(status_code=200,json=self.answer,close=lambda:None),validation_probe=True)
            self.assertEqual(selected,'mimo');self.assertEqual(r['status'],'selected')
            self.assertEqual(a.report(Path(tmp))[0]['selected'],'mimo')

    def test_unverified_pilot_never_dispatches(self):
        with patch.object(a,'available',return_value=False), patch.object(a,'backend',return_value=SimpleNamespace(availability=lambda:{'status':'ready'})):
            with patch.object(a,'memory_slice') as memory:
                with self.assertRaisesRegex(ValueError,'jev_pilot_unverified'):
                    a.choose('question',['mimo'])
                memory.assert_not_called()

    def test_lease_is_exclusive_and_release_is_idempotent(self):
        lease=a.acquire('unit-user')
        self.assertIsNotNone(lease)
        self.assertIsNone(a.acquire('unit-user'))
        other=a.acquire('other-user');self.assertIsNotNone(other)
        lease.release();lease.release();other.release()
        next_lease=a.acquire('unit-user');self.assertIsNotNone(next_lease);next_lease.release()

    def test_inflight_choice_preserves_verified_availability(self):
        with patch.object(a,'backend',return_value=SimpleNamespace(availability=lambda:{'status':'ready'})):
            with patch.object(a,'report',return_value=[{'status':'started'},{'status':'selected'}]):
                self.assertTrue(a.available())

    def test_inflight_choice_never_authorizes_unverified_or_failed_connection(self):
        with patch.object(a,'backend',return_value=SimpleNamespace(availability=lambda:{'status':'ready'})):
            for rows in ([],[{'status':'started'}],
                         [{'status':'started'},{'status':'failed_or_uncertain'},{'status':'selected'}]):
                with self.subTest(rows=rows),patch.object(a,'report',return_value=rows):
                    self.assertFalse(a.available())

    def test_backend_revocation_overrides_completed_validation(self):
        with patch.object(a,'backend',return_value=SimpleNamespace(availability=lambda:{'status':'configured_not_tested'})):
            with patch.object(a,'report',return_value=[{'status':'started'},{'status':'selected'}]):
                self.assertFalse(a.available())

if __name__=='__main__':unittest.main(verbosity=2)
