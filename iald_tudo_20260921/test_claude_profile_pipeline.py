"""End-to-end local boundary tests using the real converter, no network or key."""
from copy import deepcopy
import hashlib
from types import SimpleNamespace
import unittest
from test_claude_guard_real_converter import converter, SOURCE, BEFORE
from claude_profiles import HAIKU, SONNET
from claude_request_guard import MemoryMeasurement, ContextRejected
from claude_profile_pipeline import profile_call


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.prefix = 'FIXTURE KERNEL: explicit hypotheses and formulas.\n'
        self.cfg = SimpleNamespace(modelo=SONNET.model, max_saida=4096,
                                   cache_ttl='5m', esforco_claude='high')
        self.sent = []
        self.counted = []

    def call(self, model, *, user='testador', count=182000, tool_result=False,
             payload_model=None):
        messages = [{'role':'system','content':self.prefix+'dynamic note'},
                    {'role':'user','content':'question'}]
        if tool_result:
            messages += [
                {'role':'assistant','content':'','tool_calls':[{'id':'c1','type':'function',
                 'function':{'name':'fetch_tgl','arguments':'{"id":"public"}'}}]},
                {'role':'tool','tool_call_id':'c1','content':'public evidence'}]
        payload = {'model':payload_model or model,'max_tokens':4096,'messages':messages}
        before = deepcopy(payload)
        memory = MemoryMeasurement(model, hashlib.sha256(self.prefix.encode()).hexdigest(), 180000)
        def counter(wire):
            self.counted.append(deepcopy(wire))
            return count
        try:
            return profile_call(requested_model=model,
                server_policy=dict(username=user, account_approved=True,
                                   haiku_ready=True, sonnet_ready=True),
                cfg=self.cfg, payload=payload, prefix=self.prefix, memory=memory,
                converter=converter.converter_pedido,
                count_request=counter, send_request=self.sent.append)
        finally:
            self.assertEqual(payload, before)
            self.assertEqual(self.cfg.modelo, SONNET.model)

    def test_haiku_real_conversion_preserves_measured_prefix_cache_and_request(self):
        self.call(HAIKU.model)
        self.assertEqual(self.counted, self.sent)
        wire = self.sent[0]
        self.assertEqual(wire['thinking'], {'type':'disabled'})
        self.assertNotIn('output_config', wire)
        self.assertEqual(wire['system'][0]['text'], self.prefix)
        self.assertEqual(wire['system'][0]['cache_control']['type'], 'ephemeral')

    def test_public_sonnet_rejected_before_count_or_send(self):
        with self.assertRaises(PermissionError):
            self.call(SONNET.model)
        self.assertFalse(self.counted)
        self.assertFalse(self.sent)

    def test_luiz_sonnet_keeps_existing_parameters(self):
        self.call(SONNET.model, user='luiz')
        self.assertEqual(self.sent[0]['thinking']['type'], 'adaptive')
        self.assertEqual(self.sent[0]['output_config']['effort'], 'high')

    def test_forged_payload_model_is_not_silently_rerouted(self):
        with self.assertRaises(PermissionError):
            self.call(HAIKU.model, payload_model=SONNET.model)
        self.assertFalse(self.counted)
        self.assertFalse(self.sent)

    def test_haiku_tool_result_overflow_stops_before_paid_transport(self):
        with self.assertRaises(ContextRejected):
            self.call(HAIKU.model, count=199000, tool_result=True)
        blocks = [b for m in self.counted[0]['messages']
                  if isinstance(m['content'], list) for b in m['content']]
        self.assertTrue(any(b.get('type')=='tool_result' and
                            b.get('content')=='public evidence' for b in blocks))
        self.assertFalse(self.sent)

    @classmethod
    def tearDownClass(cls):
        assert SOURCE.read_bytes() == BEFORE, 'Production source changed'


if __name__ == '__main__':
    unittest.main()
