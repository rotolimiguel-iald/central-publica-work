"""Exercise the current production converter read-only, with network forbidden.

All token counts are fixtures. No SDK/client, credentials or server is loaded.
"""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import importlib.util
import socket
import unittest
from claude_profiles import HAIKU, SONNET, reasoning_parameters
from claude_request_guard import MemoryMeasurement, guarded_call, ContextRejected

SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD\iald_motor_claude.py')
BEFORE = SOURCE.read_bytes()
def forbid_network(*args, **kwargs):
    raise AssertionError('Network forbidden in converter test')
socket.create_connection = forbid_network
socket.socket.connect = forbid_network
spec = importlib.util.spec_from_file_location('iald_converter_readonly', SOURCE)
converter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converter)

class ConverterGuard(unittest.TestCase):
    def build(self, model):
        cfg = SimpleNamespace(modelo=model, max_saida=4096, cache_ttl='5m', esforco_claude='high')
        prefix = 'MEASURED TEST PREFIX\n'
        payload = {'model':model, 'max_tokens':4096,
                   'messages':[{'role':'system','content':prefix+'service note'},
                               {'role':'user','content':'question'}],
                   'tools':[{'type':'function','function':{'name':'fetch_tgl','description':'Public source',
                             'parameters':{'type':'object','properties':{'id':{'type':'string'}}}}}]}
        wire = converter.converter_pedido(cfg, payload, prefixo=prefix)
        measurement = MemoryMeasurement(model, hashlib.sha256(prefix.encode()).hexdigest(), 180000)
        return wire, measurement

    def test_sonnet_converter_keeps_prefix_and_tools_at_count_boundary(self):
        wire, memory = self.build(SONNET.model)
        seen = []
        def count(r):
            self.assertEqual(r['tools'][0]['name'], 'fetch_tgl')
            self.assertEqual(r['thinking']['type'], 'adaptive')
            self.assertEqual(r['system'][0]['cache_control']['type'], 'ephemeral')
            seen.append(r)
            return 182000
        sent = []
        guarded_call(wire, authorized_model=SONNET.model, memory=memory,
                     count_request=count, send_request=sent.append)
        self.assertEqual(seen, sent)

    def test_haiku_current_wire_rejected_then_profile_parameters_accepted(self):
        wire, memory = self.build(HAIKU.model)
        sent = []
        with self.assertRaisesRegex(ValueError, 'Sonnet-only'):
            guarded_call(wire, authorized_model=HAIKU.model, memory=memory,
                         count_request=lambda r:182000, send_request=sent.append)
        self.assertFalse(sent)
        # Prepared integration: replace only the model-specific reasoning fields.
        wire.pop('output_config', None)
        wire.update(reasoning_parameters(HAIKU.model, wire['max_tokens']))
        guarded_call(wire, authorized_model=HAIKU.model, memory=memory,
                     count_request=lambda r:182000, send_request=sent.append)
        self.assertEqual(sent[0]['thinking'], {'type':'disabled'})
        self.assertNotIn('output_config', sent[0])

    def test_actual_tool_result_shape_is_counted_before_next_send(self):
        cfg = SimpleNamespace(modelo=SONNET.model, max_saida=4096, cache_ttl='5m', esforco_claude='high')
        prefix = 'MEASURED TEST PREFIX\n'
        payload = {'model':SONNET.model, 'max_tokens':4096, 'messages':[
            {'role':'system','content':prefix}, {'role':'user','content':'consult'},
            {'role':'assistant','content':'','tool_calls':[{'id':'call_1','type':'function',
             'function':{'name':'fetch_tgl','arguments':'{"id":"source"}'}}]},
            {'role':'tool','tool_call_id':'call_1','content':'public evidence'}]}
        wire = converter.converter_pedido(cfg, payload, prefixo=prefix)
        memory = MemoryMeasurement(SONNET.model, hashlib.sha256(prefix.encode()).hexdigest(),180000)
        def count(r):
            blocks = [b for m in r['messages'] if isinstance(m['content'],list) for b in m['content']]
            self.assertTrue(any(b.get('type')=='tool_result' and b.get('content')=='public evidence' for b in blocks))
            return 999000
        sent = []
        with self.assertRaises(ContextRejected):
            guarded_call(wire, authorized_model=SONNET.model, memory=memory,
                         count_request=count, send_request=sent.append)
        self.assertFalse(sent)

    @classmethod
    def tearDownClass(cls):
        assert SOURCE.read_bytes() == BEFORE, 'Production converter changed'

if __name__ == '__main__':
    unittest.main()
