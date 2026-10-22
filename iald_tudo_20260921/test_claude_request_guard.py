"""Failure modes at the paid-send boundary, using no network or credentials."""
import hashlib
import unittest
from claude_profiles import HAIKU, SONNET
from claude_request_guard import MemoryMeasurement, ContextRejected, guarded_call

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.request = {'model': HAIKU.model, 'max_tokens': 4096,
                        'system': [{'type': 'text', 'text': 'fixture-memory'}],
                        'messages': [{'role': 'user', 'content': 'question'}]}
        self.memory = MemoryMeasurement(HAIKU.model, hashlib.sha256(b'fixture-memory').hexdigest(), 180000)
        self.sent = []

    def call(self, counter, memory=None):
        return guarded_call(self.request, authorized_model=HAIKU.model,
                            memory=memory or self.memory, count_request=counter,
                            send_request=lambda r: self.sent.append(r) or 'stream')

    def test_tool_growth_requires_new_count_and_stops_overflow(self):
        seen = []
        def count(r):
            seen.append(r)
            return 181000 if len(r['messages']) == 1 else 197000
        result, decision = self.call(count)
        self.assertEqual(result, 'stream')
        self.assertTrue(decision['ready'])
        self.request['messages'].append({'role': 'user', 'content': [{'type':'tool_result', 'tool_use_id':'x', 'content':'evidence'}]})
        with self.assertRaises(ContextRejected):
            self.call(count)
        self.assertEqual(len(seen), 2)
        self.assertEqual(len(self.sent), 1)

    def test_prefix_change_model_change_and_short_memory_never_send(self):
        changed = MemoryMeasurement(HAIKU.model, '0'*64, 180000)
        wrong_model = MemoryMeasurement(SONNET.model, self.memory.prefix_sha256, 180000)
        too_short = MemoryMeasurement(HAIKU.model, self.memory.prefix_sha256, 179999)
        for memory in (changed, wrong_model, too_short):
            with self.subTest(memory=memory):
                with self.assertRaises(ValueError):
                    self.call(lambda r: 181000, memory)
        self.assertFalse(self.sent)

    def test_count_failure_does_not_fall_back_to_estimation(self):
        for value in (None, 0, True, '181000'):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.call(lambda r: value)
        def fail(r):
            raise TimeoutError('fake provider count timeout')
        with self.assertRaises(TimeoutError):
            self.call(fail)
        self.assertFalse(self.sent)

    def test_mutated_counter_input_never_sent(self):
        def mutate(r):
            r['messages'].append({'role':'user', 'content':'unmeasured'})
            return 181000
        with self.assertRaises(ValueError):
            self.call(mutate)
        self.assertFalse(self.sent)

    def test_caller_mutation_during_count_cannot_change_send(self):
        def count(r):
            self.request['messages'][0]['content'] = 'changed after snapshot'
            return 181000
        self.call(count)
        self.assertEqual(self.sent[0]['messages'][0]['content'], 'question')

    def test_client_cannot_switch_to_sonnet(self):
        self.request['model'] = SONNET.model
        with self.assertRaises(ValueError):
            self.call(lambda r: 181000)
        self.assertFalse(self.sent)

    def test_sonnet_reasoning_rejected_for_haiku(self):
        self.request['thinking'] = {'type':'adaptive'}
        with self.assertRaises(ValueError):
            self.call(lambda r: 181000)
        self.assertFalse(self.sent)

if __name__ == '__main__':
    unittest.main()
