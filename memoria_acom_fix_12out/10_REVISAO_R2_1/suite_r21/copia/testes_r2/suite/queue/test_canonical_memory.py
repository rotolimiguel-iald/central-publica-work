"""Scientific-memory boundaries; every external transport is simulated."""
from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from iald_orchestrator import canonical_memory as memory, providers, operational_memory as om

class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.rite_patch = patch.object(providers, 'rite_markers', return_value=[])
        self.rite_patch.start()
        self.addCleanup(self.rite_patch.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root/'um_absoluto_forma_canonica.md'
        self.source.write_text('# TGL\n[POSTULATE] omega(I)=1\n\nPonte Cartan: preservar hipóteses.\n', encoding='utf-8')
        self.catalog = self.root/'catalog.json'
        self.catalog.write_text(json.dumps({'files': [{'source': str(self.source), 'sha256': memory.digest(self.source.read_bytes())}]}))
        self.index = self.root/'index'
        memory.build(self.index, self.catalog)
    def tearDown(self):
        self.temp.cleanup()
    def test_packet_has_verifiable_source_and_partial_coverage(self):
        packet = memory.prepare('Cartan', self.index)
        self.assertIn('omega(I)=1', packet['prompt'])
        self.assertEqual(packet['receipt']['sources'][0]['sha256'], memory.digest(self.source.read_bytes()))
        self.assertEqual(packet['receipt']['coverage'], 'PARTIAL_RETRIEVAL_NOT_FULL_CORPUS')
    def test_standard_memory_respects_projection_cap_with_long_prompt(self):
        self.source.write_text("Ponte Cartan: preservar hipóteses.\n" * 500, encoding="utf-8")
        memory.build(self.index, self.catalog)
        prompt = "Cartan " + "a " * 6000
        packet = memory.prepare(prompt, self.index, max_chars=18000)
        self.assertLessEqual(len(packet["prompt"]), 18000)
        self.assertTrue(packet["receipt"]["sources"])

    def test_tampered_index_prevents_call(self):
        with (self.index/'index.sqlite3').open('ab') as handle:
            handle.write(b'tampered')
        with self.assertRaisesRegex(ValueError, 'Integridade'):
            memory.prepare('Cartan', self.index)
    def test_changed_source_requires_refresh(self):
        self.source.write_text('changed', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'desatualizada'):
            memory.load(self.index, refresh=False)
    def test_secret_request_is_rejected(self):
        with self.assertRaises(ValueError):
            memory.prepare('ler C:/IALD/.env', self.index)
    def test_blocked_source_chunk_is_never_forwarded(self):
        self.source.write_text('iald_stack_v7.py\n', encoding='utf-8')
        memory.build(self.index, self.catalog)
        with self.assertRaisesRegex(ValueError, 'Nenhum trecho'):
            memory.prepare('TGL', self.index)
    def test_missing_index_fails_before_transport(self):
        with self.assertRaises(ValueError):
            memory.prepare('TGL', self.root/'absent')
    def test_every_executor_receives_same_packet_without_network(self):
        packet = om.attach(memory.prepare('Cartan', self.index),
                           om.preview_projection('Cartan', {}), providers.SYSTEM, 'local', {})
        receipt = packet['receipt']
        received = {}
        with ExitStack() as stack:
            stack.enter_context(patch('iald_orchestrator.canonical_memory.prepare', return_value=packet))
            stack.enter_context(patch('iald_orchestrator.providers.client_command', return_value=['mock-client']))
            for name in ('antigravity','kimi','mimo'):
                stack.enter_context(patch(f'iald_orchestrator.{name}.connection_status', return_value='ready'))
                def execute(prompt, _name=name, **kwargs):
                    received[_name] = prompt
                    return {'text':'ok','usage':{}}
                stack.enter_context(patch(f'iald_orchestrator.{name}.execute', side_effect=execute))
            def local(request, **kwargs):
                received['local'] = json.loads(request.data)['messages'][1]['content']
                response = MagicMock()
                response.__enter__.return_value.read.return_value = json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'ok'}}]}).encode()
                return response
            stack.enter_context(patch('iald_orchestrator.providers.urllib.request.urlopen', side_effect=local))
            def process(args, **kwargs):
                name = 'codex' if 'exec' in args else 'claude'
                proc = MagicMock(returncode=0)
                def communicate(prompt, **kw):
                    received[name] = prompt
                    if name == 'codex':
                        return '\n'.join(json.dumps(x) for x in [{'type':'item.completed','item':{'type':'agent_message','text':'ok'}},{'type':'turn.completed','usage':{}}]), ''
                    return json.dumps({'subtype':'success','result':'ok','usage':{}}), ''
                proc.communicate.side_effect = communicate
                return proc
            stack.enter_context(patch('iald_orchestrator.providers.subprocess.Popen', side_effect=process))
            for name in ('local','codex','claude','gemini','kimi','mimo'):
                result = providers.execute(name, 'Cartan', self.root, memory_packet=packet)
                self.assertEqual(result['canonical_memory'], receipt)
        self.assertEqual(len(received), 6)
        for text in received.values():
            self.assertIn(packet['prompt'], text)
    def test_changed_packet_fails_before_network(self):
        packet = om.attach(memory.prepare('Cartan', self.index),
                           om.preview_projection('Cartan', {}), providers.SYSTEM, 'local', {})
        packet['prompt'] += ' altered'
        with patch('iald_orchestrator.providers.urllib.request.urlopen') as network:
            with self.assertRaisesRegex(ValueError, 'Transport packet altered'):
                providers.execute('local', 'Cartan', self.root, memory_packet=packet)
            network.assert_not_called()

if __name__ == '__main__':
    unittest.main()
