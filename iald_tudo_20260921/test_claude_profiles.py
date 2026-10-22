import unittest
from claude_profiles import context_budget, reasoning_parameters


class ProfilesTests(unittest.TestCase):
    def test_haiku_never_receives_sonnet_parameters(self):
        params = reasoning_parameters('claude-haiku-4-5', 4096, 1024)
        self.assertEqual(params, {'thinking': {'type': 'enabled', 'budget_tokens': 1024}})
        with self.assertRaises(ValueError):
            reasoning_parameters('claude-haiku-4-5', 1024, 1024)

    def test_memory_is_not_double_counted(self):
        result = context_budget('claude-haiku-4-5', counted_model='claude-haiku-4-5-20251001',
                                permanent_tokens=180000, request_input_tokens=184000,
                                reserved_output_tokens=4096)
        self.assertEqual(result['remaining_tokens'], 10880)
        self.assertTrue(result['fits'])
        self.assertTrue(result['memory_target_met'])

    def test_tool_result_overflow_is_visible(self):
        result = context_budget('claude-haiku-4-5', counted_model='claude-haiku-4-5',
                                permanent_tokens=180000, request_input_tokens=198000,
                                reserved_output_tokens=4096)
        self.assertFalse(result['fits'])
        self.assertEqual(result['action'], 'rebuild_explicitly_then_recount')

    def test_underfilled_haiku_memory_cannot_be_sent_even_when_it_fits(self):
        for permanent in (0, 100000, 179999):
            with self.subTest(permanent=permanent):
                result = context_budget('claude-haiku-4-5', counted_model='claude-haiku-4-5',
                                        permanent_tokens=permanent, request_input_tokens=181000,
                                        reserved_output_tokens=4096)
                self.assertTrue(result['fits'])
                self.assertFalse(result['ready'])
                self.assertEqual(result['action'], 'load_required_memory_then_recount')

    def test_exact_haiku_target_and_sonnet_have_separate_admission_rules(self):
        for model, permanent in (('claude-haiku-4-5', 180000), ('claude-sonnet-5', 550153)):
            with self.subTest(model=model):
                result = context_budget(model, counted_model=model,
                                        permanent_tokens=permanent, request_input_tokens=permanent + 2000,
                                        reserved_output_tokens=4096)
                self.assertTrue(result['ready'])
                self.assertEqual(result['action'], 'send')

    def test_sonnet_measurement_cannot_certify_haiku(self):
        with self.assertRaises(ValueError):
            context_budget('claude-haiku-4-5', counted_model='claude-sonnet-5',
                           permanent_tokens=180000, request_input_tokens=181000,
                           reserved_output_tokens=4096)

    def test_empty_or_unknown_measurements_fail_closed(self):
        with self.assertRaises(ValueError):
            context_budget('claude-haiku-4-5', counted_model='claude-haiku-4-5',
                           permanent_tokens=None, request_input_tokens=181000,
                           reserved_output_tokens=4096)
        with self.assertRaises(ValueError):
            reasoning_parameters('claude-new-unknown', 4096)


if __name__ == '__main__':
    unittest.main()
