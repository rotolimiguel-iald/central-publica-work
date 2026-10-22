import io
import json
import threading
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from iald_orchestrator import antigravity


class CapturedInput(io.StringIO):
    def close(self):
        self.saved = self.getvalue()
        super().close()


class FakeProcess:
    def __init__(self, events):
        self.stdin = CapturedInput()
        self.stdout = io.StringIO(''.join(json.dumps(e)+'\n' for e in events))
        self.returncode = None
        self.killed = False

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        self.returncode = 0
        return 0

    def kill(self):
        self.killed = True
        self.returncode = -1


INIT = {'event': 'init', 'init': {'tools': [], 'agent': 'iald-text'}}
DONE = {'event': 'result', 'result': {'status': 'SUCCESS', 'response': '42', 'num_turns': 1,
                                    'usage': {'input_tokens': 50, 'output_tokens': 2}}}


class AntigravityProtocolTests(unittest.TestCase):
    def run_events(self, events, prompt='test', cancel=None):
        process = FakeProcess(events)
        self.process = process
        with patch.object(antigravity.subprocess, 'Popen', return_value=process) as launch:
            result = antigravity.execute(prompt, cancel=cancel)
            self.args = launch.call_args.args[0]
            return result

    def test_one_turn_over_stdin_with_actual_usage(self):
        prompt = 'PRIVATE_SENTINEL_123'
        result = self.run_events([INIT, DONE], prompt)
        self.assertEqual(result['text'], '42')
        self.assertEqual(result['usage']['input_tokens'], 50)
        self.assertNotIn(prompt, ' '.join(self.args))
        self.assertEqual(json.loads(self.process.stdin.saved)['message']['content'], prompt)

    def test_tools_prevent_prompt_transmission(self):
        with self.assertRaises(RuntimeError):
            self.run_events([{'event': 'init', 'init': {'tools': ['run_command'], 'agent': 'iald-text'}}])
        self.assertEqual(self.process.stdin.saved, '')

    def test_known_build_inventory_with_verified_empty_agent(self):
        inventory = json.loads(antigravity.INVENTORY.read_bytes())['advertised_tools']
        result = self.run_events([{'event':'init', 'init':{'agent':'iald-text','tools':inventory}},DONE])
        self.assertEqual(result['text'], '42')

    def test_divergent_global_profile_prevents_launch(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'agent.md'
            path.write_bytes(b'not the validated profile')
            with patch.object(antigravity, 'GLOBAL_AGENT', path):
                with patch.object(antigravity.subprocess, 'Popen') as launch:
                    with self.assertRaises(RuntimeError):antigravity.execute('private prompt')
                    launch.assert_not_called()

    def test_profile_with_enabled_tool_prevents_launch(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            data=antigravity.AGENT.read_bytes().replace(b'tools: []',b'tools: [view_file]')
            agent=root/'agent.md';agent.write_bytes(data)
            global_agent=root/'global.md';global_agent.write_bytes(data)
            flat=root/'.agents/agents/iald-text.md';flat.parent.mkdir(parents=True);flat.write_bytes(data)
            with patch.object(antigravity,'AGENT',agent), patch.object(antigravity,'GLOBAL_AGENT',global_agent), patch.object(antigravity,'WORK',root):
                with patch.object(antigravity.subprocess, 'Popen') as launch:
                    with self.assertRaises(RuntimeError):antigravity.execute('private prompt')
                    launch.assert_not_called()

    def test_unknown_agent_prevents_prompt_transmission(self):
        with self.assertRaises(RuntimeError):
            self.run_events([{'event': 'init', 'init': {'tools': [], 'agent': 'other'}}])
        self.assertEqual(self.process.stdin.saved, '')

    def test_truncated_stream_is_not_success(self):
        with self.assertRaises(RuntimeError):
            self.run_events([INIT, {'event': 'step_update', 'step_update': {'step_type': 'agent_response', 'text_delta': 'partial'}}])

    def test_unexpected_tool_event_fails(self):
        with self.assertRaises(RuntimeError):
            self.run_events([INIT, {'event': 'step_update', 'step_update': {'step_type': 'tool'}}, DONE])

    def test_error_result_is_not_success(self):
        with self.assertRaises(RuntimeError):
            self.run_events([INIT, {'event': 'result', 'result': {'status': 'ERROR', 'response': 'partial'}}])

    def test_duplicate_result_fails(self):
        with self.assertRaises(RuntimeError):
            self.run_events([INIT, DONE, DONE])

    def test_cancel_before_prompt(self):
        cancel = threading.Event(); cancel.set()
        with self.assertRaises(RuntimeError):
            self.run_events([INIT, DONE], cancel=cancel)
        self.assertEqual(self.process.stdin.saved, '')


if __name__ == '__main__':
    unittest.main()
